#!/usr/bin/env python3
"""
subtitle_tool.py - Helper for the demo-video-subtitle skill.

Subcommands:
  probe   VIDEO
      Print JSON metadata: duration, width, height, fps, nb_frames, has_audio.

  frames  VIDEO OUTDIR [--interval 2.5] [--scale 960] [--start 0] [--end 0] [--quality 3]
      Extract one frame every INTERVAL seconds into OUTDIR as frame_00001.jpg ...
      Writes OUTDIR/manifest.json = [{"file": "...", "t": <seconds>, "tc": "HH:MM:SS.mmm"}].
      These frames are meant to be read by the model (vision) to understand the screen.

  keyframes VIDEO OUTDIR --times 3.0,7.5,12.0 [--scale 1280] [--quality 2]
      Extract frames at EXACT timestamps (comma-separated seconds). Use to refine
      subtitle timing or capture a specific moment precisely.

  burn    VIDEO SRT OUT [--font "Malgun Gothic"] [--fontsize 22] [--marginv 40]
                        [--outline 2] [--shadow 0] [--primary FFFFFF] [--back 000000]
                        [--back_alpha 90] [--crf 20] [--position bottom]
      Hard-burn (render) styled subtitles into the video. Re-encodes video.
      Colors are RRGGBB hex. back_alpha 0-100 (0 transparent, 100 opaque box).
      position: bottom | top.

  mux     VIDEO SRT OUT
      Add a soft (toggleable) subtitle track without re-encoding video (fast).
      Player must support the subtitle track; use `burn` for guaranteed visibility.

ffmpeg/ffprobe are auto-located from PATH or the winget install location.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys


def _find_tool(name):
    p = shutil.which(name)
    if p:
        return p
    exe = name + ".exe"
    patterns = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\**" + os.sep + exe),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links" + os.sep + exe),
        r"C:\ffmpeg\bin" + os.sep + exe,
        os.path.expandvars(r"%ProgramData%\chocolatey\bin" + os.sep + exe),
    ]
    for pat in patterns:
        hits = glob.glob(pat, recursive=True)
        if hits:
            return hits[0]
    return None


FFMPEG = _find_tool("ffmpeg")
FFPROBE = _find_tool("ffprobe")


def _require_tools(need_probe=True, need_mpeg=True):
    missing = []
    if need_mpeg and not FFMPEG:
        missing.append("ffmpeg")
    if need_probe and not FFPROBE:
        missing.append("ffprobe")
    if missing:
        sys.exit("ERROR: could not locate %s. Install with: winget install --id Gyan.FFmpeg -e"
                 % ", ".join(missing))


def _fmt_tc(seconds):
    ms = int(round(seconds * 1000))
    h = ms // 3600000
    ms -= h * 3600000
    m = ms // 60000
    ms -= m * 60000
    s = ms // 1000
    ms -= s * 1000
    return "%02d:%02d:%02d.%03d" % (h, m, s, ms)


def cmd_probe(a):
    _require_tools(need_mpeg=False)
    out = subprocess.run(
        [FFPROBE, "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", a.video],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    data = json.loads(out.stdout or "{}")
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    has_audio = any(s.get("codec_type") == "audio" for s in data.get("streams", []))
    fps = 0.0
    rate = v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1"
    try:
        num, den = rate.split("/")
        fps = round(float(num) / float(den), 3) if float(den) else 0.0
    except Exception:
        pass
    dur = float(data.get("format", {}).get("duration", 0) or 0)
    print(json.dumps({
        "duration": round(dur, 3),
        "duration_tc": _fmt_tc(dur),
        "width": v.get("width"),
        "height": v.get("height"),
        "fps": fps,
        "nb_frames": v.get("nb_frames"),
        "has_audio": has_audio,
        "codec": v.get("codec_name"),
    }, ensure_ascii=False, indent=2))


def cmd_frames(a):
    _require_tools()
    os.makedirs(a.outdir, exist_ok=True)
    vf = "fps=1/%s" % a.interval
    if a.scale:
        vf += ",scale=%s:-2" % a.scale
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error"]
    if a.start:
        cmd += ["-ss", str(a.start)]
    if a.end and a.end > (a.start or 0):
        cmd += ["-to", str(a.end)]
    cmd += ["-i", a.video, "-vf", vf, "-q:v", str(a.quality),
            os.path.join(a.outdir, "frame_%05d.jpg")]
    subprocess.run(cmd, check=True)
    files = sorted(glob.glob(os.path.join(a.outdir, "frame_*.jpg")))
    manifest = []
    base = a.start or 0
    for i, f in enumerate(files):
        t = base + i * a.interval
        manifest.append({"file": os.path.basename(f), "t": round(t, 3), "tc": _fmt_tc(t)})
    with open(os.path.join(a.outdir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(json.dumps({"count": len(files), "outdir": a.outdir,
                      "manifest": os.path.join(a.outdir, "manifest.json")},
                     ensure_ascii=False))


def cmd_keyframes(a):
    _require_tools()
    os.makedirs(a.outdir, exist_ok=True)
    times = [float(x) for x in a.times.split(",") if x.strip() != ""]
    manifest = []
    for i, t in enumerate(times):
        out = os.path.join(a.outdir, "key_%03d_%s.jpg" % (i, str(t).replace(".", "p")))
        cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
               "-ss", str(t), "-i", a.video, "-frames:v", "1", "-q:v", str(a.quality)]
        if a.scale:
            cmd += ["-vf", "scale=%s:-2" % a.scale]
        cmd += [out]
        subprocess.run(cmd, check=True)
        manifest.append({"file": os.path.basename(out), "t": t, "tc": _fmt_tc(t)})
    with open(os.path.join(a.outdir, "keyframes.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(json.dumps({"count": len(times), "outdir": a.outdir}, ensure_ascii=False))


def _hex_to_ass(rrggbb, alpha_pct=0):
    """RRGGBB (+alpha 0-100, 0=opaque..100=transparent handling below) -> ASS &HAABBGGRR."""
    rrggbb = rrggbb.lstrip("#")
    r = rrggbb[0:2]
    g = rrggbb[2:4]
    b = rrggbb[4:6]
    aa = "%02X" % max(0, min(255, int(round((alpha_pct / 100.0) * 255))))
    return "&H%s%s%s%s" % (aa, b, g, r)


def cmd_burn(a):
    _require_tools()
    srt_dir = os.path.dirname(os.path.abspath(a.srt)) or "."
    srt_name = os.path.basename(a.srt)
    # back_alpha: 100 => opaque box, 0 => fully transparent. ASS alpha is inverted (00=opaque).
    back_ass_alpha = 100 - a.back_alpha
    primary = _hex_to_ass(a.primary, 0)
    back = _hex_to_ass(a.back, back_ass_alpha)
    outline_col = _hex_to_ass("000000", 0)
    alignment = 2 if a.position == "bottom" else 8  # 2=bottom-center, 8=top-center
    border_style = 4 if a.back_alpha > 0 else 1     # 4=opaque box, 1=outline+shadow
    style = (
        "FontName=%s,FontSize=%d,Bold=1,"
        "PrimaryColour=%s,OutlineColour=%s,BackColour=%s,"
        "BorderStyle=%d,Outline=%d,Shadow=%d,Alignment=%d,MarginV=%d,MarginL=40,MarginR=40"
        % (a.font, a.fontsize, primary, outline_col, back,
           border_style, a.outline, a.shadow, alignment, a.marginv)
    )
    vf = "subtitles=%s:force_style='%s'" % (srt_name, style)
    # optional top/bottom crop of browser chrome (tabs, address bar). Applied BEFORE subtitles
    # so subtitles still position from the new bottom. Height auto-adjusts to stay even.
    crop_parts = []
    if a.crop_top or a.crop_bottom:
        keep = "in_h-%d" % (a.crop_top + a.crop_bottom)
        crop_parts.append("crop=in_w:%s:0:%d" % (keep, a.crop_top))
    if crop_parts:
        vf = ",".join(crop_parts) + "," + vf
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-stats",
           "-i", os.path.abspath(a.video), "-vf", vf,
           "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf),
           "-c:a", "copy", os.path.abspath(a.out)]
    print("Running ffmpeg burn (cwd=%s)..." % srt_dir)
    subprocess.run(cmd, check=True, cwd=srt_dir)
    print("DONE: %s" % os.path.abspath(a.out))


def cmd_mux(a):
    _require_tools()
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-i", a.video, "-i", a.srt,
           "-c", "copy", "-c:s", "mov_text",
           "-metadata:s:s:0", "language=kor", a.out]
    subprocess.run(cmd, check=True)
    print("DONE: %s" % os.path.abspath(a.out))


def _parse_ts(ts):
    ts = ts.strip().replace(".", ",")
    hms, ms = ts.split(",")
    h, m, s = hms.split(":")
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def _ms_to_ts(ms):
    if ms < 0:
        ms = 0
    h = ms // 3600000
    ms -= h * 3600000
    m = ms // 60000
    ms -= m * 60000
    s = ms // 1000
    ms -= s * 1000
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def cmd_shift(a):
    """Shift all SRT cue times by --seconds (positive = later/delay, negative = earlier)."""
    delta = int(round(a.seconds * 1000))
    with open(a.srt, "r", encoding="utf-8-sig") as fh:
        lines = fh.readlines()
    out = []
    for line in lines:
        if "-->" in line:
            left, right = line.split("-->")
            l = _ms_to_ts(_parse_ts(left) + delta)
            r = _ms_to_ts(_parse_ts(right) + delta)
            out.append("%s --> %s\n" % (l, r))
        else:
            out.append(line)
    dest = a.out or a.srt
    with open(dest, "w", encoding="utf-8") as fh:
        fh.writelines(out)
    print("DONE: shifted %+.3fs -> %s" % (a.seconds, os.path.abspath(dest)))


def main():
    p = argparse.ArgumentParser(description="Demo video subtitle helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("probe"); sp.add_argument("video"); sp.set_defaults(func=cmd_probe)

    sf = sub.add_parser("frames")
    sf.add_argument("video"); sf.add_argument("outdir")
    sf.add_argument("--interval", type=float, default=2.5)
    sf.add_argument("--scale", type=int, default=960)
    sf.add_argument("--start", type=float, default=0)
    sf.add_argument("--end", type=float, default=0)
    sf.add_argument("--quality", type=int, default=3)
    sf.set_defaults(func=cmd_frames)

    sk = sub.add_parser("keyframes")
    sk.add_argument("video"); sk.add_argument("outdir")
    sk.add_argument("--times", required=True)
    sk.add_argument("--scale", type=int, default=1280)
    sk.add_argument("--quality", type=int, default=2)
    sk.set_defaults(func=cmd_keyframes)

    sb = sub.add_parser("burn")
    sb.add_argument("video"); sb.add_argument("srt"); sb.add_argument("out")
    sb.add_argument("--font", default="Malgun Gothic")
    sb.add_argument("--fontsize", type=int, default=18)
    sb.add_argument("--marginv", type=int, default=18)
    sb.add_argument("--outline", type=int, default=0)
    sb.add_argument("--shadow", type=int, default=0)
    sb.add_argument("--primary", default="FFFFFF")
    sb.add_argument("--back", default="000000")
    sb.add_argument("--back_alpha", type=int, default=80)
    sb.add_argument("--crf", type=int, default=20)
    sb.add_argument("--position", choices=["bottom", "top"], default="bottom")
    sb.add_argument("--crop_top", type=int, default=0,
                    help="pixels to crop off the top (browser tabs/address bar)")
    sb.add_argument("--crop_bottom", type=int, default=0,
                    help="pixels to crop off the bottom (e.g. OS taskbar)")
    sb.set_defaults(func=cmd_burn)

    sm = sub.add_parser("mux")
    sm.add_argument("video"); sm.add_argument("srt"); sm.add_argument("out")
    sm.set_defaults(func=cmd_mux)

    ss = sub.add_parser("shift")
    ss.add_argument("srt")
    ss.add_argument("--seconds", type=float, required=True,
                    help="positive = delay (later), negative = earlier")
    ss.add_argument("--out", default=None, help="output srt (default: overwrite input)")
    ss.set_defaults(func=cmd_shift)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()

# demo-video-subtitle skill installer
# Downloads the demo-video-subtitle skill into ~/.copilot/m-skills/demo-video-subtitle (Microsoft Scout).
# For GitHub Copilot CLI, change 'm-skills' to 'skills'.
# No GitHub CLI or sign-in required (public repo, raw download).

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$repo   = 'microsoft/KoreaCopilotAgent'
$branch = 'main'
$src    = 'templates/skill_demo-video-subtitle'
$dest   = Join-Path $HOME '.copilot/m-skills/demo-video-subtitle'

$files = @(
  'SKILL.md',
  'scripts/subtitle_tool.py'
)

Write-Host ""
Write-Host "  demo-video-subtitle 스킬 설치" -ForegroundColor Cyan
Write-Host "  -> $dest" -ForegroundColor DarkGray
Write-Host ""

foreach ($f in $files) {
  $url    = "https://raw.githubusercontent.com/$repo/$branch/$src/$f"
  $target = Join-Path $dest $f
  $dir    = Split-Path $target -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  Invoke-WebRequest -Uri $url -OutFile $target -UseBasicParsing
  Write-Host "  + $f" -ForegroundColor Green
}

Write-Host ""
Write-Host "  설치 완료. Scout를 재시작한 뒤 /demo-video-subtitle 로 실행하세요." -ForegroundColor Cyan
Write-Host "  (ffmpeg 필요: winget install --id Gyan.FFmpeg -e)" -ForegroundColor DarkGray
Write-Host ""

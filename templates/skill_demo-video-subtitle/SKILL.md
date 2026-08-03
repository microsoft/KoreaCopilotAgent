---
name: "demo-video-subtitle"
description: "Copilot·Microsoft 365 데모 영상에 한국어 자막을 다는 Skill. ffmpeg으로 프레임을 뽑아 화면(어떤 앱·어떤 에이전트·어떤 동작인지)을 vision으로 정확히 파악하고, Microsoft 공식 제품·기능 용어(리서치 도구/Researcher, Copilot in Word·PowerPoint·Excel, 분석가/Analyst, Cowork, Work IQ 등)를 정확히 반영해 타임코드 SRT를 만든 뒤, 영상에 구워넣거나(soft mux) 사이드카 SRT로 산출한다. 트리거: '데모 영상 자막', '이 영상에 자막 달아줘', 'subtitle/캡션', 'SRT 만들어줘', 'Copilot 데모 자막'. 화면 녹화 데모(리서치→Word→PowerPoint 흐름 등)에 최적화. 제외: 순수 음성 받아쓰기만 필요한 오디오 전용 파일(그건 화면 파악 단계를 생략)."
---

# Demo Video Subtitle Skill

Copilot / Microsoft 365 화면 녹화 데모 영상에 **정확한 한국어 자막**을 다는 스킬. 핵심 원칙은 "화면을 실제로 보고, 공식 용어로 쓴다"이다. 자막을 상상해서 지어내지 않는다 — 프레임을 뽑아 눈으로 확인한 내용과 (있다면) 음성만 자막으로 옮긴다.

## 도구 준비 (Prerequisites)

- **ffmpeg / ffprobe** 필요. 없으면 설치:
  `winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements`
  (macOS: `brew install ffmpeg`, Linux: 배포판 패키지 매니저). PATH가 세션에 반영 안 되면 ffmpeg `bin` 폴더를 `$env:Path`에 임시 추가한다.
- **헬퍼 스크립트**: `scripts/subtitle_tool.py` (이 스킬 폴더). ffmpeg/ffprobe 경로를 PATH·winget·choco 등에서 자동 탐색한다. 서브커맨드: `probe / frames / keyframes / burn / mux / shift`. Windows 한글(cp949) 인코딩 문제를 피하려 UTF-8로 캡처한다.
- 실행 예:
  `python "~/.copilot/m-skills/demo-video-subtitle/scripts/subtitle_tool.py" probe "<video>"`
  (GitHub Copilot CLI는 경로가 `~/.copilot/skills/...`)

## 워크플로 (반드시 순서대로)

### 1. 영상 찾기 · 메타 파악
- 데모 영상 위치를 사용자에게 확인한다(보통 `OneDrive`, `Downloads`, `Videos\화면 녹화` 등). 여러 개면 `m_ask_user`로 어떤 영상인지 확정.
- `probe`로 duration·해상도·fps·has_audio 확인. 길이에 따라 프레임 간격을 정한다(아래).

### 2. 프레임 추출 → 화면 파악 (이 스킬의 핵심)
- `frames`로 일정 간격 프레임을 뽑는다. 작업용 임시 디렉터리를 쓴다(예: `<작업폴더>/subs_<영상명>/frames`).
  - 간격 기준: **≤1분 → 1.5~2s, 1~3분 → 2.5~3s, 3~6분 → 4~5s, 그 이상 → 6~8s.** 화면 전환이 빠른 구간은 `keyframes`로 보완.
  - 예: `frames "<video>" "<outdir>" --interval 3 --scale 960`
- 추출된 `frame_*.jpg`를 **view 툴로 여러 장 병렬로 읽어** 각 시점에서 무슨 일이 일어나는지 파악한다. `manifest.json`이 각 프레임의 타임코드를 준다.
- 파악할 것: **어떤 앱/표면**(Copilot Chat, Word, PowerPoint, Excel, Teams, Cowork 등), **어떤 에이전트/기능**(리서치 도구, 분석가, 이미지 생성 등), **입력한 프롬프트 텍스트**(화면의 프롬프트 칩·입력창을 읽어 그대로 반영), **산출물 변화**(초안 생성, 표/차트/슬라이드 생성, 편집 결과). 화면의 한글/영문 UI 텍스트를 근거로 삼는다.
- 오디오가 있으면(내레이션) 그 말도 자막 후보다. 화면과 내레이션이 다르면 **내레이션 우선**, 화면 정보는 보조.
- **모델·모드 선택 드롭다운처럼 항목이 여러 개인 UI는 저해상도 프레임에서 개수를 잘못 셀 수 있다.** 해당 영역만 풀해상도로 크롭(`crop`)해 확대한 프레임으로 다시 확인한다.

### 3. 용어 검증 (Microsoft 공식)
- 아래 **용어집**을 1차 기준으로 삼되, 최신·모호한 기능명은 아래 **공식 참고 사이트**에서 확인한다. 확신 없는 신규 기능은 영문 원명을 괄호 병기.
- 절대 임의 번역 금지(예: Researcher를 '연구원'으로 쓰지 않는다 → **리서치 도구(Researcher)**).

### 4. SRT 작성
- 파악한 흐름을 타임코드에 맞춰 한국어 SRT로 쓴다(스타일 규칙은 아래). 파일은 UTF-8로 저장.
- 타임코드는 프레임 manifest의 실제 시점에 맞춘다. 경계가 애매하면 `keyframes --times a,b,c`로 해당 순간을 정밀 확인해 in/out을 조정.
- **화면 녹화 데모는 자막이 화면 동작보다 살짝 앞서는 경향이 있다.** 앞선 느낌이 나면 `shift`로 전체를 조금 뒤로 민다(기본 +0.8초 권장). 예: `shift "<srt>" --seconds 0.8 --out "<srt_shift>"`. 음수면 당긴다. 특정 큐만 문제면 그 큐의 in/out만 손본다.

### 5. 미리보기 사용자 확인
- 굽기 전에 **SRT 전문을 사용자에게 보여주고 확인**받는다(용어·타이밍·톤). 데모는 대외 공유가 잦으므로 정확도가 중요.

### 6. 자막 산출 (burn 또는 mux)
- **burn**(하드번, 재인코딩): 어디서 재생하든 보이게 자막을 영상에 구워넣음. 대외 공유·발표용 기본값.
  `burn "<video>" "<srt>" "<out.mp4>"`  ← 스크립트 기본값이 곧 확정 스타일이라 옵션 없이 그대로 쓰면 됨.
  - 브라우저 탭·주소창을 화면에서 잘라내려면 `--crop_top <px>`(상단), `--crop_bottom <px>`(하단). 잘라낼 픽셀 수는 프레임을 크롭 테스트해 seam(경계)을 찾아 정한다.
- **mux**(소프트, 무재인코딩·빠름): 껐다 켤 수 있는 자막 트랙. 원본 화질 보존이 필요하고 재생기가 자막을 지원할 때.
  `mux "<video>" "<srt>" "<out.mp4>"`
- 산출물 이름은 `<원본명>_자막.mp4`. **원본을 덮어쓰지 않는다.** SRT 사이드카(`<원본명>.srt`)도 함께 남긴다.

### 7. QA
- burn 결과에서 `keyframes --times ...`로 자막이 있는 순간을 뽑아 **view로 렌더링을 눈으로 검증**(한글 깨짐·잘림·겹침·가독성, 크롭 경계). 문제 있으면 폰트/크기/여백/박스 투명도/크롭을 조정 후 재굽기.
- 끝나면 프레임 등 임시 파일 정리.

## 자막 작성 스타일 규칙 (한국어)

- **한 자막 = 한 호흡.** 한 줄 최대 ~28자, 최대 2줄. 길면 두 자막으로 분할.
- 표시 시간: 대략 **글자수 × 0.15초 + 0.7초**, 최소 1.2초·최대 6초. 자막 간 최소 간격 100ms.
- **간결한 설명체**를 기본으로. 내레이션이 있으면 말투를 살리되 군더더기·필러 제거. 내레이션이 없으면 "무엇을 하는지"를 담담히 서술(예: "리서치 도구로 4주간 이슈를 정리합니다").
- 프롬프트를 보여주는 장면은 **실제 입력한 프롬프트 요지**를 자막으로(따옴표 인용 가능). 화면에 뜬 프롬프트 텍스트를 근거로.
- **가운뎃점(·) 남용·엠대시(—) 금지.** 나열은 쉼표나 '와/과', 구획은 세로줄(|).
- AI 티 나는 상투어("~를 통해 손쉽게", "혁신적인") 배제. 담백하게. (필요시 `/korean-proofread`로 최종 교열)
- 영문 UI/기능명은 공식 한국어명을 쓰고, 처음 등장 시만 영문 병기.

## 용어집 (Microsoft 365 Copilot 공식 · 한국어 UI 기준)

| 화면/영문 | 자막 표기 |
|---|---|
| Researcher | 리서치 도구 (Researcher) — 이후 '리서치 도구' |
| Analyst | 분석가 (Analyst) |
| Copilot Chat | Copilot 채팅 / Copilot Chat |
| Copilot in Word | Word의 Copilot |
| Copilot in PowerPoint | PowerPoint의 Copilot |
| Copilot in Excel | Excel의 Copilot |
| Copilot in Outlook | Outlook의 Copilot |
| Cowork | Cowork (작업 기반 워크스페이스) |
| Work IQ | Work IQ |
| Agent / agents | 에이전트 |
| Prompt / prompt gallery | 프롬프트 / 프롬프트 갤러리 |
| Pages / Copilot Pages | Copilot 페이지 |
| Notebook | 전자 필기장 |
| Create image / Designer | 이미지 생성 / Microsoft Designer |
| Grounding, references, citations | 근거·참조·출처 |
| Draft with Copilot | Copilot으로 초안 작성 |
| Reference a file with "/" | '/'로 파일 참조(멘션) |

주의: **Researcher = 리서치 도구**, **Analyst = 분석가**가 한국어 UI 공식 표기다. 사람 직급으로 오역하지 말 것.

## 공식 참고 사이트 (용어·기능 검증용)

용어나 기능 동작이 모호하면 굽기 전에 확인한다. 도메인이 신뢰 기준이다.
- **support.microsoft.com** (한국어 `ko-kr`) — 기능 사용법·정식 명칭. 예: Researcher/Analyst, Copilot in Word/PowerPoint/Excel.
- **learn.microsoft.com/microsoft-365-copilot/** — 관리자·개념 문서, 정식 기능명.
- **microsoft.com/microsoft-365/blog** 및 **microsoft.com/en-us/microsoft-365/copilot** — 신규 기능 발표·정의.
- **adoption.microsoft.com/copilot** — 시나리오·프롬프트 표준 표현.
- 검색 팁: 추측 URL은 404가 잦으니 `web_fetch`로 검색해 실제 문서 링크를 먼저 확보한 뒤 그 문서를 연다. 한국어 UI 표기는 `ko-kr` 페이지에서 확인.

## 명령어 요약

```
# 메타
python <스크립트> probe "<video>"
# 프레임(파악용)
python <스크립트> frames "<video>" "<outdir>" --interval 3 --scale 960
# 특정 순간 정밀 프레임
python <스크립트> keyframes "<video>" "<outdir>" --times 12.0,18.5,25.0
# 자막 타이밍 통째 이동(+지연/-당김) — 화면보다 앞설 때 보정
python <스크립트> shift "<srt>" --seconds 0.8 --out "<srt_shift>"
# 하드번(공유용 기본) — 기본값이 곧 확정 스타일. 상단 크롭 옵션 병행 가능
python <스크립트> burn "<video>" "<srt>" "<out_자막.mp4>" [--crop_top 176]
# 소프트 자막(빠름·원본화질)
python <스크립트> mux "<video>" "<srt>" "<out_자막.mp4>"
```

burn 스타일 옵션: `--font "Malgun Gothic"`(한글 기본), `--fontsize`, `--marginv`(하단 여백), `--position bottom|top`, `--primary RRGGBB`(글자색), `--back RRGGBB` + `--back_alpha 0-100`(자막 박스 불투명도, 0=투명·100=꽉찬 박스), `--outline`(글씨 테두리 두께), `--crf`(화질, 낮을수록 고화질), `--crop_top`/`--crop_bottom`(브라우저 탭·주소창·작업표시줄 잘라내기).

**확정 기본 스타일 (옵션 없이 그대로 사용):**
`--font "Malgun Gothic" --fontsize 18 --marginv 18 --back_alpha 80 --outline 0` → **흰색 굵은 글씨(테두리 없음) + 80% 반투명 검정 박스 + 한 줄 + 하단(살짝 낮게) 배치**. 화면 녹화 데모 기준으로 확정됨. 자막이 텍스트를 감싸는 작은 박스로 나오며 화면 UI를 최소한만 가린다. 이 값이 스크립트 기본값이라 `burn`을 옵션 없이 호출하면 이 스타일로 나온다. 특별한 요청이 없으면 기본값을 바꾸지 말 것.
- 주의: libass 폰트 스케일은 영상 세로 해상도 기준이라 4K·QHD 영상도 fontsize 18 안팎이면 적정 크기다(fontsize를 40+로 올리면 화면을 덮음). 박스가 있으므로 `--outline 0`(글씨 테두리 없음)이 기본이다.
- 타이밍: 화면 녹화 데모는 자막이 화면보다 조금 앞서는 경우가 많다. 앞서 보이면 `shift --seconds 0.8`로 통째 뒤로 밀어 보정한다(위 워크플로 4단계 참고).

## 출력·버전 관리

- 산출물은 원본과 같은 폴더 또는 작업 `files/`에 `<원본명>_자막.mp4` + `<원본명>.srt`. 원본 보존.
- 여러 버전을 반복하면 `versions/vNN_설명/`에 이전본을 보관하고 최신본만 밖에 둔다.

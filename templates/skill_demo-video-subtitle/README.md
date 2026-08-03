# demo-video-subtitle (데모 영상 한국어 자막 스킬)

Copilot / Microsoft 365 **화면 녹화 데모 영상**에 정확한 한국어 자막을 다는 **Microsoft Scout 스킬**입니다. (GitHub Copilot CLI에서도 같은 포맷으로 동작합니다.)

핵심 원칙은 **"화면을 실제로 보고, 공식 용어로 쓴다"** 입니다. 자막을 상상해서 지어내지 않고, ffmpeg으로 프레임을 뽑아 vision으로 확인한 화면(어떤 앱·어떤 에이전트·어떤 프롬프트·어떤 결과)과 (있다면) 내레이션만 자막으로 옮깁니다. Microsoft 공식 제품·기능 용어(리서치 도구/Researcher, 분석가/Analyst, Copilot in Word·PowerPoint·Excel, Cowork, Work IQ 등)를 정확히 반영합니다.

> 이 폴더는 선언형 에이전트(Cowork/declarative agent)나 프롬프트가 아니라, Microsoft Scout(및 GitHub Copilot CLI)에서 동작하는 **커스텀 스킬(skill)** 입니다. `SKILL.md`와 `scripts/`로 구성되며 `/demo-video-subtitle` 로 호출합니다.

## 구성

| 파일 | 설명 |
|---|---|
| `SKILL.md` | 스킬 본문(진입점). 워크플로, 용어집, 자막 스타일 규칙, 가드레일 정의 |
| `scripts/subtitle_tool.py` | ffmpeg 헬퍼. `probe / frames / keyframes / burn / mux / shift` 서브커맨드. ffmpeg 경로 자동 탐색 |

## 사전 준비: ffmpeg

프레임 추출·자막 굽기에 **ffmpeg**가 필요합니다.

```powershell
winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
```

(macOS: `brew install ffmpeg` / Linux: 배포판 패키지 매니저) — 스크립트가 PATH·winget·choco 등에서 ffmpeg를 자동으로 찾습니다.

## 설치 (두 줄이면 끝)

### 1. Scout 채팅창에 붙여넣기: 스킬을 내려받아 설치합니다

```powershell
iex (iwr https://raw.githubusercontent.com/microsoft/KoreaCopilotAgent/main/templates/skill_demo-video-subtitle/install.ps1 -UseBasicParsing).Content
```

이 명령을 그대로 Scout에 붙여넣으면 Scout가 실행해 `~/.copilot/m-skills/demo-video-subtitle/` 에 스킬을 설치합니다. GitHub CLI나 로그인은 필요 없습니다(공개 레포에서 바로 내려받음). PowerShell 창에서 직접 실행해도 됩니다.

### 2. Scout를 재시작한 뒤 실행

```
/demo-video-subtitle
```

> **GitHub Copilot CLI** 로 쓴다면 설치 위치만 `~/.copilot/skills/demo-video-subtitle/` 로 바꾸면 됩니다(스킬 포맷은 동일).
>
> **macOS / Linux (bash)** 를 쓴다면:
> ```bash
> mkdir -p ~/.copilot/m-skills/demo-video-subtitle/scripts
> base="https://raw.githubusercontent.com/microsoft/KoreaCopilotAgent/main/templates/skill_demo-video-subtitle"
> curl -fsSL "$base/SKILL.md" -o ~/.copilot/m-skills/demo-video-subtitle/SKILL.md
> curl -fsSL "$base/scripts/subtitle_tool.py" -o ~/.copilot/m-skills/demo-video-subtitle/scripts/subtitle_tool.py
> ```

<details>
<summary>수동 설치 (직접 복사)</summary>

이 폴더를 통째로 아래 위치에 넣어도 됩니다. (GitHub Copilot CLI는 `m-skills` 대신 `skills`)

```
~/.copilot/m-skills/demo-video-subtitle/
├── SKILL.md
└── scripts/
    └── subtitle_tool.py
```

복사 후 Scout를 재시작하면 `/demo-video-subtitle` 로 호출할 수 있습니다.
</details>

## 트리거 예시

- "이 데모 영상에 자막 달아줘"
- "Copilot 데모 자막 만들어줘"
- "SRT 만들어줘 / 캡션 넣어줘"
- "브라우저 탭이랑 주소창은 잘라내고 자막만"

## 동작 방식 (요약)

1. `probe` 로 길이·해상도·fps 확인
2. `frames` 로 일정 간격 프레임을 뽑아 **화면을 눈으로 파악**(앱·에이전트·프롬프트·결과)
3. Microsoft 공식 용어로 타임코드 SRT 작성 → 사용자 확인
4. `burn` 으로 자막을 영상에 구워넣기 (기본 스타일: 흰 굵은 글씨 + 반투명 검정 박스 + 하단 한 줄). 필요하면 `--crop_top` 으로 브라우저 탭·주소창 크롭
5. 결과 프레임을 다시 뽑아 **QA**, 앞서는 자막은 `shift` 로 보정

기본 산출물은 `<원본명>_자막.mp4` + 사이드카 `.srt` 이며 **원본은 보존**합니다.

## 함께 쓰면 좋은 스킬

- `/korean-proofread` — 자막 문구 최종 교열(AI 티 제거, 어문 규범)

## 제외

- 화면 없이 음성만 받아쓰는 오디오 전용 파일(화면 파악 단계가 핵심이라 이 스킬의 강점이 아님)

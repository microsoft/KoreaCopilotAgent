# korean-proofread (한국어 교열 스킬)

회사에서 쓰는 한국어 문서를 두 축으로 다듬는 **Microsoft Scout 스킬**입니다. (GitHub Copilot CLI에서도 같은 포맷으로 동작합니다.)

1. **회사 문서답게 정확하게** — 국립국어원 어문 규범과 공공언어 원칙에 따라 맞춤법, 띄어쓰기, 문법, 주어와 서술어 호응, 높임법, 문서 유형별 형식(공문, 보도자료, 이메일, 보고서, 발표 자료, 사내 공지)을 점검합니다.
2. **AI 티 안 나게** — 줄표와 가운뎃점 남용, 번역투, 상투어, 균질한 리듬 같은 'AI가 쓴 티'를 걷어내 자연스러운 한국어로 만듭니다. 논리 허점도 함께 봅니다.

> 이 폴더는 선언형 에이전트(Cowork/declarative agent)나 프롬프트가 아니라, Microsoft Scout(및 GitHub Copilot CLI)에서 동작하는 **커스텀 스킬(skill)** 입니다. `SKILL.md`와 `references/`로 구성되며 `/korean-proofread` 로 호출합니다.

## 구성

| 파일 | 설명 |
|---|---|
| `SKILL.md` | 스킬 본문(진입점). 검토 흐름, 모드, 가드레일 정의 |
| `references/quick-rules.md` | 경량 점검용 빠른 규칙과 자체 점검 체크리스트 |
| `references/public-language.md` | 공공언어 2대 축, 문장 바로쓰기, 문서 유형별 기준 |
| `references/ai-tell-and-translationese.md` | AI 티와 번역투 분류(패턴, 예, 예외, 처방, 심각도) |
| `references/scholarship.md` | 지적의 학술과 규범 근거 |

## 설치 (두 줄이면 끝)

### 1. Scout 채팅창에 붙여넣기: 스킬을 내려받아 설치합니다

```powershell
iex (iwr https://raw.githubusercontent.com/microsoft/KoreaCopilotAgent/main/templates/skill_korean-proofread/install.ps1 -UseBasicParsing).Content
```

이 명령을 그대로 Scout에 붙여넣으면 Scout가 실행해 `~/.copilot/m-skills/korean-proofread/` 에 스킬을 설치합니다. GitHub CLI나 로그인은 필요 없습니다(공개 레포에서 바로 내려받음). PowerShell 창에서 직접 실행해도 됩니다.

### 2. Scout를 재시작한 뒤 실행

```
/korean-proofread
```

> **GitHub Copilot CLI** 로 쓴다면 설치 위치만 `~/.copilot/skills/korean-proofread/` 로 바꾸면 됩니다(스킬 포맷은 동일).
>
> **macOS / Linux (bash)** 를 쓴다면:
> ```bash
> mkdir -p ~/.copilot/m-skills/korean-proofread/references
> base="https://raw.githubusercontent.com/microsoft/KoreaCopilotAgent/main/templates/skill_korean-proofread"
> curl -fsSL "$base/SKILL.md" -o ~/.copilot/m-skills/korean-proofread/SKILL.md
> for f in quick-rules public-language ai-tell-and-translationese scholarship; do \
>   curl -fsSL "$base/references/$f.md" -o ~/.copilot/m-skills/korean-proofread/references/$f.md; done
> ```

<details>
<summary>수동 설치 (직접 복사)</summary>

이 폴더를 통째로 아래 위치에 넣어도 됩니다. (GitHub Copilot CLI는 `m-skills` 대신 `skills`)

```
~/.copilot/m-skills/korean-proofread/
├── SKILL.md
└── references/
    ├── quick-rules.md
    ├── public-language.md
    ├── ai-tell-and-translationese.md
    └── scholarship.md
```

복사 후 Scout를 재시작하면 `/korean-proofread` 로 호출할 수 있습니다.
</details>

## 트리거 예시

- "AI 티 없애줘"
- "이 공문 다듬어줘"
- "보도자료 검수해줘"
- "자연스럽게 고쳐줘"
- "맞춤법 확인해줘"

`/pptx`, `/docx`, `/malgun-typography`, `/weekly-report`로 한글 산출물을 만든 뒤 **출고 전 최종 QA 단계**로 함께 쓰면 좋습니다.

## 제외

- 번역 그 자체
- 내용 추가·삭제를 동반한 재집필

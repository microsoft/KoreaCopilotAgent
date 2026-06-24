# Deck Design Studio: 사용 안내

Copilot Cowork로 발표 덱을 만들 때, **서로 완전히 다른 20가지 디자인 중 하나를 골라** 타이틀(표지)부터
본문까지 그 스타일로 일관되게 만드는 스킬입니다. 같은 내용이라도 **디자인 번호만 바꾸면 완전히 다른 룩**이
나옵니다.

---

## 1. 설치 (처음 한 번만)

이 폴더(`deck-design-studio`)를 통째로 본인 OneDrive의 아래 위치에 넣어주세요.

```
C:\Users\<사용자명>\OneDrive\문서\Coworker\.claude\skills\deck-design-studio\
```

- 폴더 안의 `SKILL.md`, `designs/`는 **그대로** 두시면 됩니다 (따로 등록할 필요 없음).
- Cowork의 **Skills(스킬) 목록**에 `deck-design-studio`가 보이면 준비 완료.

> 또는 Cowork에 이 ZIP을 주고 *"이 압축 파일로 스킬 추가해줘"* 라고 해도 같은 위치에 설치됩니다.

---

## 2. 사용법

두 가지 방법이 있습니다. `/` 슬래시로 스킬을 직접 참조해도 되고, 평소처럼 말하면 Cowork가 알아서 불러오기도 합니다.

1. 인덱스/카탈로그에서 마음에 드는 design 번호를 고릅니다 (예: 03 Glass Panels).
2. Cowork에 한 줄로 요청합니다.
   > "design 03으로 8장짜리 발표 덱 만들어줘. 제목은 'AI 워크플로우', 발표자는 OOO."
   > 또는 "/deck-design-studio design 03 발표 덱 만들어줘."
3. 타이틀부터 본문까지 그 디자인으로 생성됩니다. 어색한 곳만 한 번 더 다듬으면 끝.

폰트는 지정하면 그대로, 안 하면 맑은 고딕으로 나옵니다.

---

## 3. 회사 템플릿을 새 디자인으로 추가하기

자주 쓰는 회사 템플릿은 1회성 변형 대신 **새 디자인 번호로 추가**해 두면, 이후 번호만 불러 기본 20종처럼
계속 씁니다.

**추가 전 확인**

- 회사 템플릿 파일(`.pptx` 또는 `.potx`)을 **반드시 첨부**합니다. 말로만 설명하면 색·폰트가 정확히 추출되지 않습니다.
- 템플릿의 **슬라이드 마스터·레이아웃**이 정리돼 있어야 테마 색·폰트를 그대로 뽑아낼 수 있습니다.
- 로고는 마스터에 들어 있거나 **별도 이미지 파일**로 같이 첨부합니다. (임의로 만들지 않습니다.)

**권장 프롬프트**

> "첨부한 회사 템플릿(.pptx)을 분석해서 design 21로 추가해줘. 슬라이드 마스터에서 ① 테마 색(강조 1~6) hex,
> ② 제목·본문 폰트, ③ 로고 위치·크기, ④ 표지/본문 레이아웃 여백을 그대로 뽑아내 design-21 파일의
> 팔레트·폰트·모티프·코드 레시피로 고정해줘. hex는 # 없이."

추가 후에는 `design 21로 ... 덱 만들어줘` 처럼 기본 20종과 똑같이 호출합니다.

---

## 4. 기억할 점

| | 내용 |
|---|---|
| 디자인 선택 | design 번호만 바꾸면 같은 내용도 완전히 다른 룩 |
| 일관성 | 각 디자인의 색·폰트·레이아웃이 고정되어 결과가 흔들리지 않음 |
| 커스터마이즈 | 회사 템플릿을 새 디자인 번호(예: design 21)로 추가해 기본 20종처럼 재사용 |
| 재사용 | 스킬은 한 번만 설치, 추가한 디자인도 폴더에 저장되어 계속 사용 |

---

## 5. 디자인 20종

| # | 스타일 | # | 스타일 |
|--|--------|--|--------|
| 01 | Dark Keynote | 11 | Fluent 2 |
| 02 | Carbon Grid | 12 | Spectrum Mesh |
| 03 | Glass Panels | 13 | Data Dashboard |
| 04 | Aurora Gradient | 14 | Swiss Tech |
| 05 | Particle Constellation | 15 | Mono-hue Blue |
| 06 | Teal Systems | 16 | Executive Minimal |
| 07 | Neon Streams | 17 | Isometric Blocks |
| 08 | Rose Quartz | 18 | Split-Feature |
| 09 | Orbit Rings | 19 | Gradient Duotone |
| 10 | Graphite | 20 | Editorial Tech |

**고르기 막막할 땐:** 사내·업무 `11 Fluent 2 · 13 Dashboard` / 키노트 `01 Dark Keynote · 04 Aurora` /
데이터 `02 Carbon · 05 Particle` / 임원 `16 Executive · 20 Editorial` / 프리미엄 `03 Glass · 08 Rose · 19 Duotone`

---

## 6. 폴더 구성

```
deck-design-studio/
├── SKILL.md      ← 스킬 본체 (디자인 철학 + 20 인덱스 + 회사 템플릿 추가 + GPT-5.5 운영 규칙)
├── designs/      ← 20개 디자인 정의 (자동 참조)
└── README.md     ← 이 안내문
```

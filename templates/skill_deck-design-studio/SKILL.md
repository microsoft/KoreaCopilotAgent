---
name: deck-design-studio
description: "서로 완전히 다른 20가지 디자인 스타일로 발표 덱을 만드는 Copilot Cowork 스킬. 사용자가
  'design 03으로 발표 덱 만들어줘', 'Glass Panels 스타일로'처럼 디자인을 지정하면 해당 design 파일을
  읽어 그 팔레트·폰트·모티프·레이아웃을 타이틀(표지)부터 본문까지 정확히 적용한다. 같은 내용도 디자인
  번호만 바꾸면 완전히 다른 룩으로 생성된다. 다크/라이트 다양하게 구성. 회사·행사 템플릿을 새 디자인
  번호로 추가해 재사용할 수 있다. Use when user asks '발표 덱/PPT/슬라이드 만들어줘', 'design NN으로',
  '디자인 골라서 덱 만들어줘', '회사 템플릿을 디자인으로 추가해줘'. Do NOT use for: 단순 텍스트 요약,
  Word(.docx) 문서 작성."
cowork:
  category: writing
  icon: SlideText
---

# Deck Design Studio: 20가지 발표 디자인 스타일

발표 덱을 만들 때 **서로 완전히 다른 20가지 디자인 중 하나를 골라** 타이틀(표지)부터 본문까지 그 스타일로
일관되게 만드는 스킬입니다. 같은 내용이라도 **디자인 번호만 바꾸면 완전히 다른 룩**이 나옵니다.

## 어떻게 쓰나

1. 인덱스(아래)나 카탈로그에서 **마음에 드는 design을 하나 고릅니다** (예: `design-03-glass-panels`).
2. 모델에게: *"design 03으로 N장짜리 발표 덱 만들어줘. 제목은 OOO, 발표자는 OOO."* 라고 요청합니다.
3. 타이틀 슬라이드부터 본문까지 그 디자인 스타일로 생성됩니다.
4. 빌드 후 시각 QA → 실제 결함만 수정 → 정지.

> 빠른 커스터마이즈: *"이 스킬에서 design 03을 우리 회사 톤으로 바꿔줘"* 처럼 1회성으로 바꿀 수도 있지만,
> 자주 쓰는 템플릿이라면 아래 **회사 템플릿을 새 디자인으로 추가하기**를 권장합니다.

## 회사 템플릿을 새 디자인으로 추가하기

자주 쓰는 회사·행사 템플릿은 1회성 변형 대신 **새 디자인 번호로 추가**해 두고 기본 20종처럼 재사용합니다.

**전제 조건 (없으면 사용자에게 요청)**
- 회사 템플릿 파일(`.pptx` 또는 `.potx`)을 **반드시 첨부**받습니다. 말 설명만으로 색·폰트를 지어내지 않습니다.
- 색·폰트·로고는 **슬라이드 마스터/레이아웃**에서 추출합니다. 마스터가 비어 있거나 표지가 이미지 한 장뿐이면 보완을 요청합니다.
- 로고는 마스터에 포함된 것 또는 별도 첨부 파일만 사용합니다. **임의로 만들지 않습니다.**

**추출·추가 절차**
1. 첨부 템플릿의 슬라이드 마스터에서 ① 테마 색(강조 1~6) hex(`#` 없이), ② 제목·본문 폰트, ③ 로고 위치·크기, ④ 표지/본문 레이아웃 여백을 읽어냅니다.
2. 이 값들을 `designs/design-21-<회사명>.md`의 Palette·Fonts·Background·Motif·Layout·코드 레시피로 고정합니다 (기존 20종과 같은 구조).
3. 위 인덱스 표에 한 줄(`21 | <이름> | <계열> | 파일`)을 추가합니다.
4. 이후 *"design 21로 N장짜리 덱 만들어줘"* 로 기본 20종과 똑같이 호출합니다.

> 예시 프롬프트: *"첨부한 회사 템플릿(.pptx)을 분석해서 design 21로 추가해줘. 슬라이드 마스터에서 테마 색
> hex, 제목·본문 폰트, 로고 위치·크기, 레이아웃 여백을 그대로 뽑아내 design-21 파일로 고정해줘. hex는 # 없이."*

## 타이틀(표지) 슬라이드: 이 디자인 스타일로

이 스킬에는 고정 표지가 없습니다. **타이틀(표지) 슬라이드도 본문과 같은 디자인 스타일로** 만듭니다.

- 배경·색·폰트는 아래 본문 디자인의 팔레트를 그대로 사용합니다. (다크 스타일이면 다크 표지, 라이트면 라이트 표지)
- 타이틀 슬라이드에는 **발표 제목 + 부제(또는 발표자/조직)** 정도만 크게 올리고, 본문 모티프를 절제해서 한 번 보여줍니다.
- 회사·행사 로고가 필요하면 사용자가 제공한 파일만 사용합니다. **로고를 임의로 만들어 넣지 않습니다.**
- 표지 텍스트 한글 폰트는 사용자가 지정한 폰트, 없으면 맑은 고딕(Malgun Gothic).

> 예) Dark 계열: 어두운 배경 + 큰 흰색 제목 + 본문 악센트색 1개. Light 계열: 밝은 배경 + 짙은 제목 + 악센트 1개.

-----

## 모든 스타일 공통 규칙 (절대 불변)

core pptx 스킬에서 가져온 규칙이라 어떤 디자인에서도 깨지지 않습니다.

- **hex에 `#` 금지.** `"2E6BE6"` (O), `"#2E6BE6"` (X, .pptx 손상).
- **제목 밑줄 악센트선 금지. 장식용 컬러바·엣지 스트라이프 금지.** (AI 생성물의 #1 신호) 카드는
  fill 틴트나 shadow로 구분. "측면 색 블록"이 필요하면 얇은 띠가 아니라 **풀하이트 실제 레이아웃 블록**으로.
- **한 색이 지배(60~70%)** + 보조 1~2 + 악센트 1. 균등 배분 금지. 둘째 악센트 색 추가 금지.
- **모든 슬라이드에 시각 요소** 하나 이상. 제목+불릿만 있는 슬라이드 금지.
- **본문 좌측 정렬;** 제목만 가운데(스타일이 명시하지 않는 한). 제목 36~44 / 헤더 20~24 / 본문 14~16pt.
- **여백 최소 0.5"**, 간격은 0.3"/0.5"로 일관되게.
- **Aptos 기본값 금지.** 한글은 사용자가 지정한 폰트, 없으면 **맑은 고딕(Malgun Gothic)**. 라틴은 QA-safe 폰트만
  (Arial, Calibri, Cambria, Times New Roman, Courier New, Bookman Old Style, Century Schoolbook).
- pptxgenjs는 옵션 객체를 in-place 변형 → 호출마다 새 객체(`makeShadow()` 팩토리).
- **빌드 후 서브에이전트로 시각 QA** → 실제 결함(오버플로·겹침·누락)만 수정 → 정지.

## 이 스킬의 디자인 철학

- **20개 디자인은 서로 완전히 다른 스타일**입니다. 하나를 고르면 그 디자인의 팔레트·폰트·모티프·레이아웃을
  **그대로** 따릅니다. 임의로 섞거나 다른 팔레트를 지어내지 않습니다.
- **한 덱 안에서는 한 색 계열이 지배**하고, 타이틀 슬라이드부터 마지막까지 같은 스타일로 통일합니다.
- **프리미엄·전문적.** 유치한 클립아트, 뻔한 파란 불릿, AI로 만든 듯한 장식(제목 밑줄·엣지 스트라이프)은 금지.
- 다크/라이트는 디자인마다 다르며, 발표 성격에 맞게 고르면 됩니다.

-----

## 20개 디자인 인덱스

각 파일은 독립적으로 사용합니다 (palette · fonts · background · 단일 motif · layout · code recipe 포함).

| # | 스타일 | 계열 | 파일 |
|--|--------|------|------|
| 01 | Dark Keynote | 다크 | `designs/design-01-dark-keynote.md` |
| 02 | Carbon Grid | 다크 | `designs/design-02-carbon-grid.md` |
| 03 | Glass Panels | 다크 | `designs/design-03-glass-panels.md` |
| 04 | Aurora Gradient | 다크 | `designs/design-04-aurora-gradient.md` |
| 05 | Particle Constellation | 다크 | `designs/design-05-particle-constellation.md` |
| 06 | Teal Systems | 라이트 | `designs/design-06-teal-systems.md` |
| 07 | Neon Streams | 다크 | `designs/design-07-neon-streams.md` |
| 08 | Rose Quartz | 라이트 | `designs/design-08-rose-quartz.md` |
| 09 | Orbit Rings | 다크 | `designs/design-09-orbit-rings.md` |
| 10 | Graphite (Microsoft) | 라이트 | `designs/design-10-graphite-microsoft.md` |
| 11 | Fluent 2 (Microsoft) | 라이트 | `designs/design-11-fluent-2.md` |
| 12 | Spectrum Mesh | 라이트 | `designs/design-12-spectrum-mesh.md` |
| 13 | Data Dashboard | 라이트 | `designs/design-13-data-dashboard.md` |
| 14 | Swiss Tech | 라이트 | `designs/design-14-swiss-tech.md` |
| 15 | Mono-hue Blue | 라이트 | `designs/design-15-mono-hue-blue.md` |
| 16 | Executive Minimal | 라이트 | `designs/design-16-executive-minimal.md` |
| 17 | Isometric Blocks | 라이트 | `designs/design-17-isometric-blocks.md` |
| 18 | Split-Feature | 라이트 | `designs/design-18-split-feature.md` |
| 19 | Gradient Duotone | 라이트 | `designs/design-19-gradient-duotone.md` |
| 20 | Editorial Tech | 라이트 | `designs/design-20-editorial-tech.md` |

-----

## 빠른 선택 (성격별)

- 사내/엔터프라이즈 → **11 Fluent 2**, **13 Data Dashboard**, **10 Graphite**
- 비전/키노트 (다크) → **01 Dark Keynote**, **08 Rose Quartz**, **04 Aurora Gradient**
- 데이터/분석 → **02 Carbon Grid**, **05 Particle Constellation**, **13 Data Dashboard**
- 프로세스/시스템 → **06 Teal Systems**, **17 Isometric Blocks**
- 임원/경영 → **16 Executive Minimal**, **20 Editorial Tech**
- 프리미엄/브랜드 → **03 Glass Panels**, **08 Rose Quartz**, **12 Spectrum Mesh**, **19 Gradient Duotone**

## 데모 흐름

1. **하나의 내용, 스무 가지 디자인.** design 03 / 11 / 19로 같은 내용을 만들어 보여주면 디자인 차이가 한눈에 보입니다.
2. **왜 design 파일이 작동하나:** 모델이 정확한 hex·폰트·모티프·코드 레시피를 받기 때문에 generic blue bullets로 흐를 수 없습니다.
3. **공통 규칙**(엣지 스트라이프 금지, 제목 밑줄 금지, 한 색 지배)이 모든 출력을 "의도된 디자인"으로 보이게 합니다.

-----

# 부록: GPT-5.5 운영 규칙 (사내 GPT-5.5 사용 시)

> 사내에서 **GPT-5.5만** 쓸 수 있는 환경이라면, 이 규칙을 프롬프트에 함께 적용하면 디자인이 `AI 기본값`으로
> 흐르지 않습니다. (별도 파일 없이 이 SKILL.md 하나로 관리합니다.)

## PART A: GPT-5.5가 디자인을 망치지 않게 모는 법

GPT-5.5는 **제약하지 않으면** 기본 습성이 슬라이드 디자인을 조용히 무너뜨립니다. 아래 규칙을 **프롬프트 맨 위**에 두세요.

- **A1. reasoning effort 고정**: 정해진 design으로 덱 1개면 `reasoning.effort: low`(또는 medium). 고정 스펙
  실행은 어려운 추론이 아니며, high effort는 좋은 디자인을 의심하게 만듭니다.
- **A2. "끝"의 정의 + 자가점검 1회**: "design-NN으로 N장. 한 번 렌더하고 실제 결함(오버플로·겹침·누락)만 고친 뒤 STOP."
- **A3. 출력 형태 강제**: "pptxgenjs로 .pptx 하나, 섹션당 슬라이드 1장" + 따라야 할 design 파일의 팔레트/폰트/모티프를 그대로 붙여넣기.
- **A4. 모순 제거**: "미니멀"+"꽉 채워라" 같은 충돌은 축마다 하나만. 고정 스타일이면 "design-NN을 정확히 따르고 즉흥 변경 금지".
- **A5. 코드 전 계획**: "코드 작성 전에 슬라이드별 계획과 사용할 정확한 hex/폰트를 먼저 나열."

### 비협상 디자인 규칙 (어떤 모델이든)
- hex에 `#` 금지. 제목 밑줄·엣지 스트라이프 금지. 한 색 지배(60~70%) + 악센트 1(둘째 악센트 금지).
- 모든 슬라이드에 시각 요소. 본문 좌측 정렬. 호출마다 새 옵션 객체(`makeShadow()` 팩토리).
- Aptos 기본값 금지. 한글은 사용자 지정 폰트(없으면 맑은 고딕), 라틴은 QA-safe 폰트만.

### 복붙용 프롬프트 래퍼 (GPT-5.5)
```
reasoning.effort = low
text.verbosity   = low

너는 pptxgenjs로 PowerPoint를 만든다.
- 타이틀(표지)과 본문 모두 designs/design-{NN}-*.md 스타일을 정확히 따른다.
  · 팔레트(이 hex 그대로, # 없이): {붙여넣기}
  · 폰트: {붙여넣기}
  · 배경 + 모티프: {붙여넣기}
- 보편 규칙: 제목 밑줄 금지, 엣지 스트라이프/컬러바 금지, 한 색 지배, 모든 슬라이드에 시각 요소,
  본문 좌측 정렬, QA-safe 폰트만. 팔레트·폰트·레이아웃을 즉흥적으로 바꾸지 말 것. 둘째 악센트 금지.

코드 전에: 슬라이드별 계획과 사용할 정확한 hex+폰트를 먼저 나열.
그다음 .pptx 하나 작성. 한 번 렌더하고 오버플로/겹침/누락만 고친 뒤 STOP.
완료 정의: N장, 오버플로 없음, design 스펙 일치. 추가 반복 없음.
```

-----

## PART B: 20개 스타일 (압축 스펙)

각 행을 위 래퍼에 붙여넣으세요. **코드 레시피는 각 `designs/design-NN-*.md`에 있습니다.**

|# |Style |계열 |Dominant |Support / Accent |Background |Fonts |Motif |
|--|------|----|---------|-----------------|-----------|------|------|
|01|Dark Keynote|다크|black `0A1020`|텍스트 흰색 `F4F6FA`|`0A1020` 단색|Cambria(제목) + Calibri(본문)|**히어로 하나 + 광활한 여백.** 슬라이드당 단 하나의 초점(큰 단어/숫자/도형)과 그 아래 얇은 1px 라이트 헤어라인.|
|02|Carbon Grid|다크|지배 `161616`|악센트 일렉트릭 블루 `2E6BE6`|`161616`|Arial 전반|**모듈러 데이터 타일 그리드**: `222730` 타일 매트릭스, 그 중 한 타일만 블루로 점등.|
|03|Glass Panels|다크|지배 deep navy `0B1838`|악센트 바이올렛 `7C5CFF`|네이비 그라데이션 `0B1838`→`14224A` + 은은한 컬러 오브.|Calibri|**프로스티드 글래스 패널**: 반투명 흰 fill(~14%) + 얇은 바이올렛 스트로크. 뒤에 컬러 오브가 비침.|
|04|Aurora Gradient|다크|지배 navy `0B1838`|바이올렛 `3A1E6B`|**풀블리드 오로라 그라데이션 wash** + 하나의 희미한 대각 라이트 스트릭.|Calibri|부드러운 오로라 wash; 텍스트는 wash의 차분한(좌측) 영역에 둠.|
|05|Particle Constellation|다크|지배 `0A1230`|악센트 cyan `22D3EE`|`0A1230`|Arial|**연결된 노드-도트 네트워크**: 점 + 얇은 연결선, 핵심 노드는 cyan으로 점등.|
|06|Teal Systems|라이트|지배 teal `0E7C86`|보조 emerald `1FA98F`|흰색|Calibri|**청록 노드 + 연결 플로우**: 흰 배경에 teal 라운드 노드가 얇은 선으로 이어진 프로세스 플로우. 글자와 겹치지 않게 노드는 하단/측면에 배치.|
|07|Neon Streams|다크|지배 `0D0221`|악센트 일렉트릭 블루 `2E6BE6`|`0D0221`|Arial|**네온 글로우 스트릭 라인**: 얇은 선 + 컬러 글로우 섀도. 시선을 이끄는 곡선.|
|08|Rose Quartz|라이트|화이트 `FBF4F8`|보조 rose `E48FB1`|**부드러운 로즈→바이올렛 그라데이션 wash**|Calibri|**라이트 글래스모피즘**: 은은한 로즈-바이올렛 wash 위에 제대로 된 프로스티드 글래스 카드 한 장(반투명 흰 + 얇은 흰 스트로크).|
|09|Orbit Rings|다크|지배 `0B1838`|블루 `7C5CFF`|`0B1838`|Calibri|**동심 궤도 링 + 하나의 초점 노드**: 링이 한 코너에 정박, 콘텐츠는 반대편.|
|10|Graphite (Microsoft)|라이트|지배 graphite `3B3F46`|표면 `F3F4F6`|흰색 + 그래파이트 세그먼트 헤더 밴드.|Calibri(Segoe 대체)|**그래파이트 세그먼트 헤더 + 뉴트럴 카드** (Microsoft 스타일, 회색 기반). 한 카드만 teal 강조.|
|11|Fluent 2 (Microsoft)|라이트|지배 Fluent 블루 `0F6CBD`|보조 light `2899F5`|`FAF9F8`|Calibri(Segoe 대체, QA-safe)|**중립 베이스 위 떠 있는 흰 카드 + 균일한 depth shadow** (Fluent 깊이 언어). 둥근 모서리 ~8px.|
|12|Spectrum Mesh|라이트|보조 indigo `4F46E5`|/violet `8A50D8`|흰색 + 부드럽게 번진 컬러 오브.|Calibri|**흰 카드 뒤로 흐릿한 그라데이션 오브** (표지의 이리데센트를 라이트 버전으로).|
|13|Data Dashboard|라이트|지배 slate `1E293B`|보조 teal `0D9488`|흰색 + 슬레이트 헤더 밴드.|Calibri|**네이티브 편집 가능 차트 + 60~72pt 스탯 콜아웃.**|
|14|Swiss Tech|라이트|잉크 `111111`|악센트 일렉트릭 블루 `1E5BE6`|순백.|Arial 전반|**플러시-레프트 타입 컬럼 + 큰 블루 섹션 숫자.** 모든 텍스트가 같은 x에서 시작.|
|15|Mono-hue Blue|라이트|지배 블루 ramp `0A2A6B`|`9FC3F5`|흰색.|Arial|**밸류 사다리**: 색조 깊이만으로 위계, 하나의 hue만.|
|16|Executive Minimal|라이트|지배 charcoal `222630`|white `F4F6FA`|`F4F6FA`|Cambria(제목) + Calibri|**초대형 숫자 하나 + 헤어라인 룰 하나 + 광활한 여백.**|
|17|Isometric Blocks|라이트|지배 indigo `4F46E5`|보조 violet `8A50D8`|`F5F8FD`|Calibri|**아이소메트릭 3D 스택 블록**: 입체 큐브가 쌓인 일러스트.|
|18|Split-Feature|라이트|지배 네이비 블록 `0B1838`|악센트 앰버 `F2A93B`|흰색 + 좌측 풀하이트 네이비 컬럼.|Calibri|**풀하이트 실제 네이비 사이드 컬럼**(얇은 띠가 아니라 진짜 레이아웃 블록)이 제목을 담음.|
|19|Gradient Duotone|라이트|지배 대각 듀오톤 네이비 `0B1838`|일렉트릭 블루 `2E6BE6`|대각 듀오톤 split.|Arial Black(제목) + Arial|**볼드 대각 2톤 split + 하나의 악센트 도형.**|
|20|Editorial Tech|라이트|지배 잉크 `1A1F2B`|white `FBFBFD`|`FBFBFD`|Cambria(헤더) + Calibri(본문)|**초대형 풀-스탯 + 얇은 컬럼 룰**: 클린 테크 에디토리얼 (옛 세리프 잡지 아님).|

-----

## PART C: GPT-5.5 실패 양상 → 해법

|증상 |원인 |해법|
|-----|-----|----|
|중반부터 generic 블루로 드리프트|열린 재량 + medium effort 탐색|A3+A4: 정확한 hex 붙여넣기, "팔레트 즉흥 금지"|
|제목 아래 컬러바/사이드 스트라이프|학습된 "AI 슬라이드" 필러|매 프롬프트 엣지-스트라이프 금지 반복|
|무한 재렌더|정지 조건 없음 (A2)|하드 "한 번 렌더, 실제 결함만, STOP"|
|경쟁 악센트 2~3색|지배색 미적용|"지배 1 + 악센트 1; 둘째 악센트 금지"|
|텍스트 오버플로|비-safe 폰트 크기 무시|QA-safe 폰트; 컨테이너 +10% 여유; 렌더 검증|
|파일 손상|hex `#`, 옵션 객체 재사용|`#` 금지; `makeShadow()` 팩토리|

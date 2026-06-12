---
name: design-08-rose-quartz
description: "발표 덱 디자인 #08 — Rose Quartz. 타이틀(표지)부터 본문까지 이 스타일의 팔레트·폰트·모티프·레이아웃을 정확히 따른다. 사용자가 'design 08으로', 'Rose Quartz로'처럼 지정하면 이 디자인으로 덱을 만든다. 라이트 — 밝은 배경 기반."
---

# 발표 덱 디자인 #08 — Rose Quartz

한 덱 전체를 이 스타일로 만듭니다 (타이틀 + 본문 모두).

## 타이틀(표지) 슬라이드 — 이 디자인 스타일로

이 스킬에는 고정 표지가 없습니다. **타이틀(표지) 슬라이드도 본문과 같은 디자인 스타일로** 만듭니다.

- 배경·색·폰트는 아래 본문 디자인의 팔레트를 그대로 사용합니다. (다크 스타일이면 다크 표지, 라이트면 라이트 표지)
- 타이틀 슬라이드에는 **발표 제목 + 부제(또는 발표자/조직)** 정도만 크게 올리고, 본문 모티프를 절제해서 한 번 보여줍니다.
- 회사·행사 로고가 필요하면 사용자가 제공한 파일만 사용합니다. **로고를 임의로 만들어 넣지 않습니다.**
- 표지 텍스트 한글 폰트는 사용자가 지정한 폰트, 없으면 맑은 고딕(Malgun Gothic).

> 예) Dark 계열: 어두운 배경 + 큰 흰색 제목 + 본문 악센트색 1개. Light 계열: 밝은 배경 + 짙은 제목 + 악센트 1개.

-----

## 본문 디자인 — Rose Quartz (라이트)

**Mood:** 부드럽고 예쁜, 은은한 로즈-바이올렛, 프리미엄.

**Palette:** 지배 연한 로즈-화이트 `FBF4F8`; 보조 rose `E48FB1`·violet `9B7BE0` 은은한 wash; **악센트 violet `7C5CFF`**; 텍스트 `2A2435`.

**Fonts:** Calibri. 제목 38pt.

**Background:** **부드러운 로즈→바이올렛 그라데이션 wash** (아주 연하게).

**Motif (반복 요소):** **라이트 글래스모피즘** — 은은한 로즈-바이올렛 wash 위에 제대로 된 프로스티드 글래스 카드 한 장(반투명 흰 + 얇은 흰 스트로크).

**Layout:** 소프트 wash + 깨끗한 글래스 카드 하나.

**Do:** 은은한 로즈/바이올렛, 프로스티드 카드, 부드러운 톤.

**Don't:** 쨍한 핑크, 다중 카드 그라데이션, 강한 대비 도형.

```javascript
slide.addShape(pres.shapes.RECTANGLE,{ x:0, y:0, w:13.333, h:7.5, fill:{ type:"gradient", stops:[
  {color:"FBF4F8",position:0},{color:"F3E9FA",position:55},{color:"EAE2FB",position:100}], angle:30 }, line:{type:"none"} });
slide.addShape(pres.shapes.OVAL,{ x:9.4, y:0.6, w:3.4, h:3.4, fill:{ color:"E48FB1", transparency:62 }, line:{type:"none"} });
slide.addShape(pres.shapes.OVAL,{ x:10.4, y:3.6, w:2.6, h:2.6, fill:{ color:"9B7BE0", transparency:60 }, line:{type:"none"} });
slide.addShape(pres.shapes.ROUNDED_RECTANGLE,{ x:0.8, y:1.6, w:8.4, h:4.3, rectRadius:0.06, fill:{ color:"FFFFFF", transparency:30 }, line:{ color:"FFFFFF", width:1 } });
slide.addText("Soft by design", { x:1.2, y:2.0, w:7.6, h:0.9, fontFace:"Calibri", bold:true, fontSize:38, color:"2A2435", margin:0 });
```

-----

## 모든 스타일 공통 규칙 (절대 불변)

core pptx 스킬에서 유래 — 어떤 디자인에서도 깨지지 않습니다.

- **hex에 `#` 금지** — `"2E6BE6"` (O), `"#2E6BE6"` (X, .pptx 손상).
- **제목 밑줄 악센트선 금지. 장식용 컬러바·엣지 스트라이프 금지.** (AI 생성물의 #1 신호) 카드는
  fill 틴트나 shadow로 구분. "측면 색 블록"이 필요하면 얇은 띠가 아니라 **풀하이트 실제 레이아웃 블록**으로.
- **한 색이 지배(60–70%)** + 보조 1–2 + 악센트 1. 균등 배분 금지. 둘째 악센트 색 추가 금지.
- **모든 슬라이드에 시각 요소** 하나 이상. 제목+불릿만 있는 슬라이드 금지.
- **본문 좌측 정렬;** 제목만 가운데(스타일이 명시하지 않는 한). 제목 36–44 / 헤더 20–24 / 본문 14–16pt.
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


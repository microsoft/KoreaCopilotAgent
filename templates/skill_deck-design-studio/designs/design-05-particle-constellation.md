---
name: design-05-particle-constellation
description: "발표 덱 디자인 #05 — Particle Constellation. 타이틀(표지)부터 본문까지 이 스타일의 팔레트·폰트·모티프·레이아웃을 정확히 따른다. 사용자가 'design 05으로', 'Particle Constellation로'처럼 지정하면 이 디자인으로 덱을 만든다. 다크 — 어두운 배경 기반."
---

# 발표 덱 디자인 #05 — Particle Constellation

한 덱 전체를 이 스타일로 만듭니다 (타이틀 + 본문 모두).

## 타이틀(표지) 슬라이드 — 이 디자인 스타일로

이 스킬에는 고정 표지가 없습니다. **타이틀(표지) 슬라이드도 본문과 같은 디자인 스타일로** 만듭니다.

- 배경·색·폰트는 아래 본문 디자인의 팔레트를 그대로 사용합니다. (다크 스타일이면 다크 표지, 라이트면 라이트 표지)
- 타이틀 슬라이드에는 **발표 제목 + 부제(또는 발표자/조직)** 정도만 크게 올리고, 본문 모티프를 절제해서 한 번 보여줍니다.
- 회사·행사 로고가 필요하면 사용자가 제공한 파일만 사용합니다. **로고를 임의로 만들어 넣지 않습니다.**
- 표지 텍스트 한글 폰트는 사용자가 지정한 폰트, 없으면 맑은 고딕(Malgun Gothic).

> 예) Dark 계열: 어두운 배경 + 큰 흰색 제목 + 본문 악센트색 1개. Light 계열: 밝은 배경 + 짙은 제목 + 악센트 1개.

-----

## 본문 디자인 — Particle Constellation (다크)

**Mood:** 네트워크, 데이터, 연결.

**Palette:** 지배 `0A1230`; **악센트 cyan `22D3EE`**; 보조 블루 `2E6BE6`; 텍스트 흰색.

**Fonts:** Arial. 제목 36pt.

**Background:** `0A1230` (표지의 파티클 웨이브 호응).

**Motif (반복 요소):** **연결된 노드-도트 네트워크** — 점 + 얇은 연결선, 핵심 노드는 cyan으로 점등.

**Layout:** 별자리처럼 퍼진 노드, 콘텐츠는 노드에 정착.

**Do:** 점-선 네트워크, 점등 노드, 깊은 네이비.

**Don't:** 두꺼운 도형, 따뜻한 색, 평면 단색 블록.

```javascript
slide.background = { color: "0A1230" };
const nodes=[[2.0,2.2],[4.2,1.6],[3.4,3.6],[5.6,3.0],[1.8,4.4]];
nodes.forEach(([x,y],i)=>{ if(i>0){ const [px,py]=nodes[i-1];
  slide.addShape(pres.shapes.LINE,{ x:Math.min(px,x), y:Math.min(py,y), w:Math.abs(x-px), h:Math.abs(y-py), line:{ color:"2E6BE6", width:0.75, transparency:40 }, flipH:(x<px) }); }});
nodes.forEach(([x,y],i)=> slide.addShape(pres.shapes.OVAL,{ x:x-0.08, y:y-0.08, w:0.16, h:0.16, fill:{ color:i%2?"22D3EE":"2E6BE6" } }));
slide.addText("Everything connects", { x:6.6, y:2.6, w:6, h:1, fontFace:"Arial", bold:true, fontSize:36, color:"FFFFFF", margin:0 });
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


Create a Chinese technical sketchnote infographic in 蒸馏小余知识卡 / Deep Research Sketchnote style.

Output: one landscape knowledge card, aspect ratio about 1080x640 (landscape), PNG.

Topic:
PolyUQuest 系统架构：一张异构图装下网页三层结构，查询先分诊再走三条检索路。

Core message / bottom takeaway strip:
简单问题走便宜通道，复杂问题才动图 —— 成本和 ChunkRAG 持平。

Layout:
多阶段流水线版式，从左到右三大区块，标题居中置顶：「PolyUQuest：先建一张图，查询再分诊」。

Elements:
- 左区块（浅蓝卡，标题「离线：异构图」）：一个手绘小图谱，四类节点用不同 pastel 色小圆：「网页」「证据块」「实体」「话题」。IMPORTANT: 边关系必须严格按下面四条画，不要随意连线或换标签：
  1. 两个「网页」图标之间的连线标「超链接」（超链接只存在于网页与网页之间）
  2. 「网页」到「证据块」的连线标「包含」
  3. 「证据块」到「实体」的连线标「提及」
  4. 「实体」到「话题」的连线标「关联」
  建议画成从上到下的链条：网页↔网页（超链接）→ 证据块（包含）→ 实体（提及）→ 话题（关联），布局清楚胜过花哨
- 中区块（浅黄卡，标题「两层路由器」）：上层小标签「规则层：免 LLM」，下层小标签「LLM 分类器：接长尾」，画一个小分诊台/交通指挥小人
- 右区块（薄荷绿卡，标题「三种检索模式」）：三条并列小通道——
  1. 「A 直接检索」标注「单跳事实」
  2. 「B 导航检索」标注「跨页聚合」
  3. 「C 实体推理」标注「多跳推理」
- 三大区块之间用粗手绘箭头连接，用户问题小气泡从中间进入
- 右下角小标签：「查询 2,968 token ≈ 普通 RAG」

Visual style:
- warm cream paper background (#F6EEDB), not a bright blue/orange poster
- dark navy hand-drawn outlines (#0B1538), rounded sticky-note cards
- pastel accents: pale blue, mint green, soft yellow, soft pink
- centered title, compact knowledge-card density, 3-7 main modules
- clear arrows and readable Chinese labels (2-8 字)
- bottom takeaway strip in a rounded pill
- small friendly robot doodle only as helper
- mobile-readable, clean spacing

Avoid:
- photorealistic, 3D glossy render, dark cyberpunk, corporate PPT
- dense tiny text, real brand logos
- bright blue/orange full background

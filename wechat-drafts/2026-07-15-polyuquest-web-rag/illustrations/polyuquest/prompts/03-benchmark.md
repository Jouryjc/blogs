Create a Chinese technical sketchnote infographic in 蒸馏小余知识卡 / Deep Research Sketchnote style.

Output: one landscape knowledge card, aspect ratio about 1080x640 (landscape), PNG.

Topic:
PolyUQuest 与四个 RAG 基线在港理工官网 300 问上的实测对比。

Core message / bottom takeaway strip:
结构不是玄学：有据率 0.921，token 只花 LightRAG 的 1/10。

Layout:
对比记分卡版式，标题居中置顶：「五个系统同场实测：结构找回来，分数就上来」。

Elements:
- 主体：一张手绘风格的对比卡片表，5 行，每行一个圆角便签条。IMPORTANT: 所有条形和主数字统一表示「有据率 Faithfulness」，不要混入其他指标的数字：
  1. 「ChunkRAG」有据率 0.710，短评「便宜但答不全」
  2. 「HtmlRAG」有据率 0.804，短评「只救页内结构」
  3. 「FastGraphRAG」有据率 0.737，短评「正确性仅 0.295，答案垮了」
  4. 「LightRAG」有据率 0.559，短评「答得顺，查询要 29,825 token」，旁边画一个着火的小钱袋
  5. 「PolyUQuest」一行用高亮浅黄底 + 小皇冠涂鸦：有据率 0.921，附小字「正确性 0.644 / 查询 2,968 token」
- 每行右侧画手绘条形，条形长度严格对应该行的有据率数字（0.710 / 0.804 / 0.737 / 0.559 / 0.921），条形末端标同一个有据率数字
- 左侧列标题用「系统」「有据率」「短评」，不要写「排名」，行首不要放名次序号（避免读者误解为排行榜）
- 右上角小便签：「消融：去掉 DOM 层级，覆盖率 -13.9」
- 底部 takeaway 药丸条

Visual style:
- warm cream paper background (#F6EEDB), not a bright blue/orange poster
- dark navy hand-drawn outlines (#0B1538), rounded sticky-note rows
- pastel accents: pale blue, mint green, soft yellow, soft pink
- centered title, compact knowledge-card density
- readable Chinese labels, numbers large and clear
- mobile-readable, clean spacing

Avoid:
- photorealistic, 3D glossy render, dark cyberpunk, corporate PPT
- dense tiny text, real brand logos
- bright blue/orange full background

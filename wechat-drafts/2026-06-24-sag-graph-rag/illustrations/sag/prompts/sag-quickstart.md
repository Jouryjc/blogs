Create a Chinese technical sketchnote infographic in 蒸馏小余知识卡 / Deep Research Sketchnote style. Horizontal 16:9 knowledge card, mobile-readable.

Topic:
SAG 每个项目自带一个 MCP Server，外部 Agent 复制 mcpServers 配置后即可调用项目级检索工具。

Core message (bottom takeaway strip, exact Chinese):
「不用再传 projectId：每个 SAG 项目天然就是一个检索工具箱」

Important style target:
Match the sibling article images: warm cream paper, hand-drawn rounded cards, dark navy sketch outlines, pastel sticky notes, compact engineering note. This is a MCP architecture explainer, not a quickstart checklist and not a corporate diagram.

Layout:
Use a left-to-right architecture flow with 4 main zones:

1. Left card: SAG 项目
   - small document icons and database icon
   - labels: 文档库 / event + entity / sourceId

2. Center small config card, title exact Chinese: 复制 mcpServers
   - show a tiny JSON-like snippet with exact code-like labels:
     "sag"
     "npm run mcp"
     SAG_MCP_SOURCE_ID

3. Right card: 外部 Agent
   - friendly robot or agent icon
   - label: 不用再传 projectId

4. Bottom tool belt card, title exact Chinese: 四个 MCP 工具
   - four small pill labels, exact text:
     sag_ingest_document
     sag_search
     sag_explain_search
     sag_get_event

Flow:
- A thick hand-drawn arrow from SAG 项目 to 复制 mcpServers.
- A thick hand-drawn arrow from 复制 mcpServers to 外部 Agent.
- A return arrow from 外部 Agent down to 四个 MCP 工具, then back to SAG 项目.
- Add small trace lines labeled: 导入文档 / 检索 / 解释链路 / 查事件

Top title (exact Chinese):
给 Agent 用：每个项目自带 MCP Server

Visual style:
- warm cream paper background (#FAF4E8), not a bright poster
- dark navy hand-drawn outlines (#0B1538), rounded sticky-note cards, light paper texture
- pastel blocks: pale blue, mint green, soft yellow, light peach
- centered title at top, compact knowledge-card density
- bold but soft marker arrows
- small friendly robot / engineer doodle only if useful
- no huge empty margins

Text rule:
- Render ALL Chinese labels exactly as written, large and legible, no garbled glyphs.
- Keep the tool names, JSON-like labels, and env variable exactly as shown.
- No extra random text.
- Do not mention "四步上手", "docker", or ".env" in this image.

Avoid: photorealistic, 3D glossy render, dark cyberpunk, corporate PPT, dense tiny text, real brand logos, bright blue/orange full background, generic quickstart pipeline, giant code block.

Create a Chinese technical sketchnote infographic in 蒸馏小余知识卡 / Deep Research Sketchnote style. Horizontal 16:9 knowledge card, mobile-readable.

Important style target:
Match the sibling article images, especially the warm cream paper card with hand-drawn rounded modules. This should feel like a compact engineering note, not a chart poster. Use lighter outlines, softer shadows, more hand-drawn sticky-note modules, and less glossy / corporate chart styling.

Topic:
SAG 对比 HippoRAG 2 的多跳问答召回提升。

Core message (bottom takeaway strip, exact Chinese):
「Recall@2 越高，Agent 越早命中证据，越省 token 和延迟」

Layout:
Use a compact three-card knowledge layout, not a full-screen chart poster.

Top: centered title on clean cream paper.

Middle: one rounded "Recall@2 对比" card containing a small hand-drawn bar comparison:
- two simple marker-style bars, side by side
- left bar shorter, right bar taller
- keep the chart inside the card, with generous spacing and no heavy axis grid
- use a small curved arrow between the bars

Left small sticky card: benchmark setup.
Right small sticky card: MuSiQue Recall@5 side note.
Bottom: one takeaway strip, same style as the other article images.

Bar labels inside the middle card (exact Chinese labels under each bar):
- left bar shorter, pale gray-blue, label: HippoRAG 2，68.14%
- right bar taller, highlighted mint green with a little up-arrow and sparkle, label: SAG，79.30%
- a curved hand-drawn arrow from left bar to right bar with a tag (exact Chinese): +11.16 个百分点（约 +16.4%）

Top-left small config note card (exact Chinese, small but legible):
统一配置：bge-large-en-v1.5 + qwen3.6-flash
数据集：HotpotQA / 2WikiMultiHop / MuSiQue

Bottom-right small callout sticky (exact Chinese):
MuSiQue Recall@5：65.13% → 80.04%
换 NV-Embed-v2 → 81.71%
增益主要来自结构

Visual style:
- warm cream paper background (#FAF4E8), not a bright poster
- dark navy hand-drawn outlines (#0B1538), but thinner and softer than a poster; no thick black cartoon borders
- rounded sticky-note cards and light paper texture, similar to the other SAG article images
- pastel blocks: pale blue, mint green, soft yellow
- centered title at top (exact Chinese): 平均 Recall@2：从 68% 提到 79%
- small hand-drawn chart, marker-style bars, compact density
- include one tiny friendly robot or engineer doodle only if it does not compete with the data

Text rule:
- Render ALL Chinese characters and the numbers exactly as written, large and legible, no garbled glyphs, no extra random text. Numbers must be exactly: 68.14% / 79.30% / 11.16 / 16.4% / 65.13% / 80.04% / 81.71%.
- Avoid unnecessary spaces around Chinese punctuation.

Avoid: photorealistic, 3D glossy render, dark cyberpunk, corporate PPT, dense tiny text, real brand logos, bright blue/orange full background, giant standalone chart poster, heavy black borders, glossy arrow icons.

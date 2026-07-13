Create a Chinese technical sketchnote infographic in 蒸馏小余知识卡 / Deep Research Sketchnote style. Horizontal 16:9 knowledge card, mobile-readable.

Topic:
SAG 的两种检索模式对比：极速模式与标准模式。

Core message (bottom takeaway strip, exact Chinese):
「两种模式都不是普通向量搜索，都基于事项/实体索引 + SQL 多跳」

Layout: two horizontal pipelines stacked top and bottom, each is a row of 3-4 rounded cards connected by bold arrows.

Top pipeline title (exact Chinese): 极速模式 fast（快、便宜）
Cards left-to-right (exact Chinese, one per card with a tiny icon):
- query 进来
- 实体库 BM25 匹配
- SAG 多跳扩展
- rerank 选 topK
- small note tag (exact Chinese): 不调 LLM 抽实体

Bottom pipeline title (exact Chinese): 标准模式 standard（准、稍慢）
Cards left-to-right (exact Chinese, one per card with a tiny icon):
- query 进来
- LLM 抽 query 实体
- SAG 多路召回
- LLM 精排
- small note tag (exact Chinese): 多两次 LLM 调用，换精度

Visual style:
- warm cream paper background (#FAF4E8), not a bright poster
- dark navy hand-drawn outlines (#0B1538), rounded sticky-note cards
- top pipeline use pale blue cards, bottom pipeline use soft yellow cards
- centered title at top (exact Chinese): 极速还是标准？看你要快还是要准
- bold marker arrows between cards, compact density
- a small lightning doodle near fast lane, a small magnifier doodle near standard lane

Text rule:
- Render ALL Chinese labels exactly as written, large and legible, no garbled glyphs, no random English filler beyond the few terms shown (query / fast / standard / BM25 / LLM / SQL / topK / rerank).

Avoid: photorealistic, 3D glossy render, dark cyberpunk, corporate PPT, dense tiny text, real brand logos, bright blue/orange full background.

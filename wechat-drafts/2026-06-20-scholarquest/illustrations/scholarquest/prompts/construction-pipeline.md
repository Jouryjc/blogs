Create 1 Chinese technical sketchnote infographic.

Exact output:
- one PNG image
- strict horizontal WeChat article body infographic
- exact aspect ratio 2.35:1
- target canvas 1920x817 pixels
- do not generate portrait, square, 4:3, or 16:9
- keep all text large enough for mobile reading

Topic:
ScholarQuest benchmark construction pipeline.

Core message:
先控制 query，再构造答案，再放进统一 ScholarBase 后端评测。

Layout:
Horizontal multi-stage pipeline with 6 connected cards.

Stages:
1. "ACM CCS 主题"
   Small number: "1682"
2. "映射到 arXiv CS"
   Small number: "1638 seeds"
3. "四类意图生成"
   Labels: Method / Setting / Comparison / Scope
4. "过滤去重"
   Small number: "1111 queries"
5. "答案发现"
   Labels: Google / arXiv / Semantic Scholar / citation
6. "ScholarBase 评测"
   Labels: search / inspect / expand

Add a small quality gate icon between stages 4 and 5:
"LLM 相关性 + 人工审计"

Bottom takeaway strip:
可复现评测，要同时固定问题、答案和检索环境。

Visual style:
蒸馏小余知识卡 / Deep Research Sketchnote style, warm cream paper background, dark navy hand-drawn outlines, pastel sticky-note cards, clear arrows, Chinese labels, mobile-readable.

Avoid:
photorealistic, 3D, cyberpunk, corporate PPT, dense tiny text, real company logos, fake math.

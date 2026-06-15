# 正文图提示词：先粗找，再精挑

生成 1 张 16:9 横版中文技术信息图，用于微信公众号正文。

标题：RAG 的第一步是先捞候选

核心信息：Embedding 检索像图书馆先搬出一车可能相关的书。`top_k` 控制先拿多少候选，metadata filter 负责先按时间、权限、栏目做过滤。

布局：
- 左侧：用户问题“退款政策什么时候生效？”。
- 中间横向漏斗流程：
  1. Query Embedding
  2. Vector Search
  3. Metadata Filter
  4. Top-K 候选片段
- 右侧：一只资料篮，里面有 20-40 张文档卡片，其中几张高亮。
- 底部 takeaway：召回阶段宁可多捞一点，但不能把噪音直接塞给模型。

视觉风格：
- 蒸馏小余知识卡 / Deep Research Sketchnote style。
- warm cream paper background。
- dark navy hand-drawn outlines。
- pastel blue / mint / yellow cards。
- clear arrows and mobile-readable Chinese labels。

不要：真实品牌、写实照片、3D、密集小字、水印。

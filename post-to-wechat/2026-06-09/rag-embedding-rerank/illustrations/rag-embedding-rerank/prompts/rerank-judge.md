# 正文图提示词：Rerank 像老师批卷

生成 1 张 16:9 横版中文技术信息图，用于微信公众号正文。

标题：Rerank 像逐份批卷

核心信息：Reranker 会把“用户问题 + 候选片段”成对阅读，给每个候选一个 relevance score，然后重新排序，只把 top_n 交给 LLM。

生活类比：
- 老师改卷：不是看卷子标题像不像，而是逐题对照题目，看是否真正回答了问题。

布局：
- 左侧：一叠候选片段卡片，标注“Top-K 候选”。
- 中间：老师/评审员形象，桌上有问题卡“退款政策何时生效？”。
- 中间下方：三张评分卡：
  - A：0.91 命中答案
  - B：0.63 相关但不完整
  - C：0.22 只是同主题
- 右侧：重新排好的队列“Top-N 证据”。
- 底部 takeaway：相关不等于能回答，Rerank 负责把最像答案的证据排前面。

视觉风格：
- 蒸馏小余知识卡 / Deep Research Sketchnote style。
- warm cream paper background。
- dark navy hand-drawn outlines。
- pastel sticky-note cards。
- readable Chinese labels。
- clear arrows。

不要：真实品牌、写实照片、3D、密集小字、水印。

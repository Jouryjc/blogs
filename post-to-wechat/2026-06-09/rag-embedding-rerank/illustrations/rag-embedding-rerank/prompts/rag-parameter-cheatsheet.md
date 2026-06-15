# 正文图提示词：RAG 参数速查卡

生成 1 张 16:9 横版中文技术信息图，用于微信公众号正文。

标题：RAG 参数是一组取舍

核心信息：chunk_size、overlap、top_k、top_n、score_threshold、hybrid weight 都不是神参；每个参数都在质量、噪音、成本、延迟之间做取舍。

布局：
- 六个旋钮或滑杆卡片：
  1. chunk_size：太小丢上下文，太大不精准
  2. overlap：太低断句，太高重复
  3. top_k：太低漏召回，太高噪音多
  4. top_n：太少证据不足，太多挤上下文
  5. threshold：太低乱进，太高答不上
  6. hybrid：专名多加关键词，语义多加向量
- 底部一条调参顺序：
  切块 -> top_k -> rerank_top_n -> threshold -> eval

视觉风格：
- 蒸馏小余知识卡 / Deep Research Sketchnote style。
- warm cream paper background。
- dark navy hand-drawn outlines。
- pastel sticky-note cards。
- readable Chinese labels。
- clear arrows。

不要：真实品牌、写实照片、3D、密集小字、水印。

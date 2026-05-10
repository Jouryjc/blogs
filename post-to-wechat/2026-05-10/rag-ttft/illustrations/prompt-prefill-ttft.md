生成一张中文技术文章正文配图，比例 16:9。

主题：RAG 把检索内容塞进 prompt，导致输入 token 变多，Prefill 阶段变长，TTFT 变高。

整体风格：
- hand-drawn technical explainer infographic
- sketchnote style
- warm cream paper background
- black hand-drawn lines
- pastel rounded boxes
- clear arrows
- cute engineer doodles
- formula blocks
- takeaway summary

画面结构：
- 上方画一个公式块：TTFT ≈ 检索链路 + Prefill(输入 token)
- 左侧画短 prompt：问题 + 2 个 chunk，计时器短
- 右侧画长 prompt：问题 + 12 个 chunk，计时器明显变长
- 中间画 LLM prefill 机器正在「读完所有输入」
- 底部 takeaway summary：多召回不等于更快，输入 token 会先变成 TTFT

中文标签：
- 短上下文
- 长上下文
- 输入 token
- Prefill
- 首 token 等待
- TTFT ↑
- 总结：少塞、塞准、放对位置

不要出现乱码、伪代码和品牌 logo。

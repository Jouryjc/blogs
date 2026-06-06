生成一张中文技术文章正文配图，比例 16:9。

主题：长上下文 KV Cache 会挤压 batch size 和并发。

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
- 左侧：短上下文请求，KV Cache 小，GPU 里能放很多请求，Batch Size ↑
- 右侧：长上下文请求，KV Cache 大，GPU 显存被占满，Batch Size ↓
- 中间画一个 GPU 显存仪表盘和天平
- 底部 takeaway summary：长上下文不只影响自己，也影响并发

中文标签：
- 短上下文
- 长上下文
- KV Cache
- 显存
- Batch Size
- 并发
- 总结：缓存越大，并发越小

不要出现公司 logo，不要复杂小字。

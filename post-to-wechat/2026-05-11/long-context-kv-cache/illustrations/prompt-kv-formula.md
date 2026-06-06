生成一张中文技术文章正文配图，比例 16:9。

主题：KV Cache 的显存账单公式。

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
- 中间大公式块：KV Cache ≈ 2 × 层数 × KV heads × head_dim × token 数 × bytes
- 左侧画 Key 和 Value 两个缓存盒子
- 右侧画显存条随着 token 数增长而变红
- 下方用小例子：128KB/token × 128K ≈ 16GB
- 底部 takeaway summary：token 越多，缓存线性增长

中文标签：
- Key
- Value
- 层数
- KV heads
- token 数
- 显存
- 总结：上下文越长，显存账单越大

不要出现乱码公式，不要品牌 logo。

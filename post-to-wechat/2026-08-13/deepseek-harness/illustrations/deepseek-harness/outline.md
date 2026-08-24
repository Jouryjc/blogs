# DeepSeek Harness 配图大纲

## 1. 三层定位图

- 文件：`01-three-layers.png`
- 插入位置：解释模型层、Harness 层、产品层之后。
- 结论：同一个模型放进不同 Harness，工作表现也会变化。
- 结构：自下而上的三层工作台，Harness 中间层信息最丰富。

## 2. Cordis 插件架构图

- 文件：`02-cordis-plugin-tree.png`
- 插入位置：解释 Cordis Context、依赖和可逆注册之后。
- 结论：插件既要按依赖装上，也要随生命周期卸干净。
- 结构：中心 Context，周围是 Loop、LLM、工具、会话、Shell、文件、子 Agent 与 UI 插件。

## 3. 收益与治理账单

- 文件：`03-benefit-cost.png`
- 插入位置：插件化治理成本段之后。
- 结论：插件化没有消灭复杂度，而是把复杂度变成一张可治理的依赖图。
- 结构：左右对照，左侧三项收益，右侧四张账单，中间由天平连接。

## 4. 封面

- 文件：`imgs/article-cover.png`
- 标题：`DeepSeek 把 Agent 拆成了插件`
- 副标题：`模型之外，还有一层 Harness`
- 结论：`Loop · 工具 · 会话 · 沙箱 · UI 都能替换`
- 结构：居中模型芯片，外环插件卡片，整体位于正方形安全区。


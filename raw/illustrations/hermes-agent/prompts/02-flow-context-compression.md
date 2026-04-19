---
illustration_id: 02
type: flowchart
style: blueprint
---

Hermes Agent 上下文压缩流程 - Flowchart

Layout: left-to-right process flow with five major steps

STEPS:
1. 长对话历史堆积 - 多轮消息、工具输出越来越长
2. 保留关键上下文 - system prompt、最近消息、关键任务状态
3. 压缩旧工具输出 - 用摘要替代冗长中间结果
4. 生成 handoff summary - 总结 Goals、Progress、Decisions、Files、Next Steps
5. 压缩后继续运行 - 更短上下文继续下一轮推理

CONNECTIONS:
- 用粗箭头连接 1 到 5
- 在第 4 步旁边用 5 个小卡片列出 Goals / Progress / Decisions / Files / Next Steps
- 右上角加一个小标签：不是简单截断，而是保留任务状态机

LABELS:
- 长对话历史
- 保留关键上下文
- 压缩旧工具输出
- handoff summary
- 继续运行
- Goals
- Progress
- Decisions
- Files
- Next Steps

COLORS:
- 背景：暖白
- 过程框：蓝青色渐变块
- summary 卡片：浅黄色 / 浅绿色 / 浅蓝色
- 警示强调：少量橙红色

STYLE:
- Flat vector flowchart with bold arrows and rounded rectangles
- Clean composition with generous white space
- 中文标签大而清楚
- 像技术公众号里的解释型流程图
- 无写实元素，无复杂纹理

TEXT:
- 使用中文
- 标题可写：Hermes 如何压缩上下文

ASPECT: 16:9

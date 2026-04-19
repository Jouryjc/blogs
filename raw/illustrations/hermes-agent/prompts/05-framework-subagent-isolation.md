---
illustration_id: 05
type: framework
style: blueprint
---

Hermes Agent 子代理隔离机制 - Framework Diagram

STRUCTURE: centered parent agent with three isolated child workers around it

NODES:
- 中央：父 Agent 主上下文
- 左侧：子代理 A，局部探索任务
- 右侧：子代理 B，局部执行任务
- 下方：子代理 C，局部分析任务

RELATIONSHIPS:
- 父 Agent 向三个子代理发出委托任务
- 每个子代理只返回结果摘要，不返回全部中间上下文
- 每个子代理旁边用小标签说明：独立预算、独立终端、fresh conversation
- 底部列出禁用项：no memory / no clarify / no delegate / no execute_code

LABELS:
- 父 Agent 主上下文
- 委托任务
- 结果带回
- 独立预算
- 独立终端
- fresh conversation
- 禁 memory
- 禁 clarify
- 禁 delegate
- 保护父上下文

COLORS:
- 父 Agent：深蓝青
- 子代理：浅蓝 / 浅绿 / 浅橙
- 箭头：深灰蓝
- 约束标签：珊瑚红小标签

STYLE:
- Flat vector framework diagram
- Main visual centered, lots of whitespace
- 中文标签清晰
- 像“主上下文保护”解释图
- 不要写实人物，不要 UI 截图

TEXT:
- 使用中文
- 标题可写：子代理为什么要强隔离

ASPECT: 16:9

---
illustration_id: 01
type: framework
style: blueprint
---

Hermes Agent 三层结构总览 - Framework Diagram

STRUCTURE: hierarchical layered architecture with gentle top-down flow

ZONES:
- Zone 1 顶层：入口层，包含 CLI、Messaging Gateway、Batch Runner、ACP / IDE
- Zone 2 中层：Agent 内核层，包含 AIAgent、Conversation Loop、Prompt Builder、Context Compression、Memory、Sessions
- Zone 3 底层：工具与执行层，包含 Tool Registry、Toolsets、Terminal、Browser、Code Execution、MCP、Execution Environments

RELATIONSHIPS:
- 顶层多个入口统一流向 AIAgent
- AIAgent 向下调用工具系统
- 工具系统再连接不同执行环境
- 右侧用简短标签标注“同一内核，多入口复用”

LABELS:
- 入口层
- Agent 内核层
- 工具与执行层
- 对话循环
- 提示词分层
- 上下文压缩
- 记忆与会话
- 工具注册
- 权限边界
- 本地 / Docker / SSH / Modal

COLORS:
- 背景：浅米白 + 很轻的蓝灰渐变
- 顶层：浅青蓝
- 中层：浅靛蓝
- 底层：浅青绿
- 连接线：深蓝灰
- 重点高亮：珊瑚红少量点缀

STYLE:
- Friendly editorial technical explainer
- Flat vector framework diagram with clean black outlines
- Clean composition with generous white space
- Main architecture centered
- 中文标签清晰可读，字大，像公众号技术信息图
- 不是企业 PPT，不要写实，不要复杂背景

TEXT:
- 使用中文
- 标题可写：Hermes Agent 的三层结构
- 其余标签尽量短

ASPECT: 16:9

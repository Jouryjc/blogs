---
illustration_id: 06
type: framework
style: blueprint
---

Hermes Agent 双重角色：在线运行时 + 离线数据工厂 - Framework Diagram

STRUCTURE: split framework with shared core in center

ZONES:
- 左侧：在线 Agent Runtime，包含 CLI、Gateway、ACP / IDE、Tool Use、Sessions
- 中央：Hermes Core，包含 AIAgent、Prompt System、Memory、Tool Registry
- 右侧：离线 Data Factory，包含 Batch Runner、Trajectories、Compression、SFT Data、Analysis

RELATIONSHIPS:
- 左右两侧都连接中央内核
- 从右侧延伸出数据产物箭头：training data / tool stats / reasoning stats
- 顶部短标签：一套内核，两种用途

LABELS:
- 在线运行时
- Hermes Core
- 离线数据工厂
- CLI
- Gateway
- ACP / IDE
- Batch Runner
- Trajectories
- SFT Data
- Analysis
- 一套内核，两种用途

COLORS:
- 左侧：浅蓝青
- 中央内核：深靛蓝
- 右侧：浅绿色和浅黄色
- 数据箭头：橙黄色点缀

STYLE:
- Flat vector framework diagram with clear zones
- Clean composition and strong hierarchy
- 中文标签清晰易读
- 技术编辑插画风格
- 不要复杂背景，不要写实元素

TEXT:
- 使用中文
- 标题可写：Hermes 不只是产品，也是数据工厂

ASPECT: 16:9

---
illustration_id: 04
type: framework
style: blueprint
---

Hermes Agent 记忆冻结快照机制 - Framework Diagram

STRUCTURE: left-to-right conceptual framework with four stages

NODES:
- 本地记忆文件：MEMORY.md / USER.md
- Session 启动快照：system_prompt_snapshot
- 当前推理循环：AIAgent 正在运行
- 下一次 Session：新记忆重新加载生效

RELATIONSHIPS:
- 本地记忆文件在 session 开始时生成快照
- 当前推理循环只读取快照，不直接回读磁盘改动
- 运行中对 memory 的修改通过虚线流向“下一次 Session 生效”
- 右上角加短标签：稳定性优先，不做实时回流

LABELS:
- 本地记忆
- 启动快照
- 当前 Session
- 修改已写盘
- 当前 Prompt 不变
- 下次启动生效
- prefix cache 更稳定
- 避免自我污染

COLORS:
- 背景：暖白
- 左侧记忆文件：浅绿色
- 中间快照：浅蓝色
- 当前 session：浅靛蓝
- 下一次生效：浅橙色

STYLE:
- Flat vector framework diagram with geometric nodes and clean connectors
- Clean composition with generous white space
- 中文标签大而清楚
- 技术公众号解释图风格
- 不要复杂背景，不要写实元素

TEXT:
- 使用中文
- 标题可写：记忆为什么要“冻结快照”

ASPECT: 16:9

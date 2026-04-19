---
illustration_id: 03
type: comparison
style: blueprint
---

Hermes Agent 工具调用与安全审批链路 - Comparison Diagram

LEFT SIDE - 没有安全闸门:
- 模型直接生成命令
- 高风险命令可能直接执行
- 权限边界模糊
- 长会话里更容易积累风险

RIGHT SIDE - Hermes 的安全链路:
- 命令先正规化
- 危险模式检测
- tirith 深度扫描
- 审批作用域：once / session / permanent
- 再进入终端或容器环境执行

DIVIDER:
- 中间用醒目的对比分隔线
- 顶部标题强调“工具调用不是直通执行”

LABELS:
- 没有安全闸门
- Hermes 安全链路
- 命令正规化
- 危险命令检测
- tirith 扫描
- 审批作用域
- once
- session
- permanent
- sandbox / backend

COLORS:
- 左侧使用淡红和灰色，表达风险
- 右侧使用蓝绿和米白，表达稳健
- 分隔线和关键节点使用深蓝灰

STYLE:
- Flat vector comparison with split layout
- Clear visual separation
- 中文标签简短清晰
- 像公众号里的“错误做法 vs 正确链路”示意图
- 保持大量留白

TEXT:
- 使用中文
- 标题可写：工具调用为什么要过安全闸门

ASPECT: 16:9

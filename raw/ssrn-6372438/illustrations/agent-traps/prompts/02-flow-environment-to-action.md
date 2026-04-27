---
illustration_id: 02
type: flowchart
style: editorial
---

恶意环境如何一步步把 Agent 带到错误动作 - Process Flow

Layout: left-to-right flowchart with five major steps, thick arrows, strong causal readability

STEPS:
1. 被污染的环境
   - 恶意网页 / 邮件 / PDF / 通知
   - 隐藏指令、伪装措辞、动态注入
2. 感知解析
   - Agent 读取 HTML、Markdown、图片或通知
   - 人类看不到的内容进入上下文
3. 推理被带偏
   - “像是在帮任务”
   - “像是安全演练”
   - 让 Agent 误判为合理操作
4. 工具与权限执行
   - 读取文件
   - 调用邮箱 / IM / API
   - 拉起子代理
5. 真实损失
   - 数据外泄
   - 未授权操作
   - 错误决策被持续放大

CONNECTIONS:
- each arrow should visually intensify from left to right
- add a red warning branch on the final step showing exfiltration to attacker endpoint
- include one small caption near the arrows: 错误认知 -> 错误计划 -> 错误动作

COLORS:
- cream background
- slate and teal for internal agent steps
- coral/orange/red for malicious or harmful transitions
- use a small attacker endpoint icon on the far right

STYLE:
- flat editorial flowchart with strong information hierarchy
- large, prominent Chinese labels
- simple icons: webpage, eye/parser, brain/reasoning, tool panel, outbound arrow
- avoid clutter; each block should be readable on mobile

ASPECT: 16:9

Clean composition with generous white space. Simple or no background. Main elements centered or positioned by content needs.

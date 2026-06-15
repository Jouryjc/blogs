生成 1 张 16:9 横版中文技术知识卡。

图片标题：GSD 的记忆在 .planning 里

核心信息：
GSD 的连续性不是聊天记录，而是一组可读、可提交、可复盘的 Markdown / JSON 工件。

版式：
- 左侧画一个 `.planning/` 文件树，像手绘文件夹：
  - PROJECT.md：项目说明
  - REQUIREMENTS.md：需求编号
  - ROADMAP.md：阶段路线
  - STATE.md：当前位置
  - phases/01/CONTEXT.md：决策
  - phases/01/RESEARCH.md：研究
  - phases/01/PLAN.md：任务
  - phases/01/UAT.md：验收
- 右侧画三个角色卡：
  - Orchestrator：只负责路由
  - Planner：读决策和研究
  - Executor：按计划改代码
- 用箭头表示所有角色都读写 `.planning/`，不是依赖长聊天。
- 底部 takeaway：把状态写进文件，Agent 才能跨会话继续。

视觉风格：
- 蒸馏小余知识卡 / Deep Research Sketchnote style
- warm cream paper background
- dark navy hand-drawn outlines
- pastel sticky-note rounded cards
- readable Chinese labels
- small file, folder, checklist, arrow doodles

避免：
- 真实 IDE 截图
- 真实品牌 logo
- 复杂不可读文件树

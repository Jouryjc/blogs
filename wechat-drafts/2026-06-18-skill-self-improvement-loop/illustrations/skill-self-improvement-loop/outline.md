# 配图大纲：Agent Skill 自我改进闭环

风格：蒸馏小余知识卡 / Deep Research Sketchnote。暖奶油纸底，深海军蓝手绘线，低饱和便签卡片，中文短标签，手机端可读。

## 图 1：双层 loop，不是一个 while

- 用左右或上下两层结构解释：
  - 内层 loop：新 issue -> 运行 Skill -> 贴标签/评论 -> 记录结果
  - 外层 loop：定时观察 -> 收集反馈 -> 改 Skill -> PR 审核
- 底部 takeaway：执行和改进要分开，否则反馈只会散落在聊天记录里。

## 图 2：反馈如何变成 Skill diff

- 用 6 步横向流水线解释：
  - marker + version
  - 收集反应
  - 对比 relabel
  - 提炼通用 lesson
  - 修改 Skill 文件
  - PR review + merge
- 底部 takeaway：能进入 git diff 的经验，才会影响下一次 Agent 执行。


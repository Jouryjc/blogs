---
title: "Agent Skill 自我改进闭环研究笔记"
source: "https://x.com/zachlloydtweets/status/2066908445425496348"
created_at: "2026-06-18"
tags:
  - type/source
  - topic/agent-skills
  - topic/agent-design
  - topic/agent-memory
moc:
  - "[[agent-skills]]"
  - "[[agent-design]]"
  - "[[agent-memory]]"
related:
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/article]]"
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/raw/source-article]]"
---

# Agent Skill 自我改进闭环研究笔记

## 标题候选

1. 推荐标题：Agent 为什么总学不会？把反馈写回 Skill
2. 稳妥标题：让 Agent 变好的不是循环，而是可审计的 Skill 改动
3. 大众标题：让 AI 助手越用越顺，反馈要回到说明书里
4. 专家标题：Self-improvement Loop 怎么落地：从 Issue Triage 到 Skill PR
5. 反差标题：Agent 改进最大的坑，不在模型，而在反馈怎么回写

最终选题：`Agent 为什么总学不会？把反馈写回 Skill`。

选择理由：从开发者体感切入，避免只讲 self-improvement loop 概念；标题承诺可以在第一屏兑现：问题不是 Agent 没跑起来，而是每次纠错都没有回到 Skill 文件。

## 原始素材要点

- Zach Lloyd 的 X Article 讨论如何为 Skills 搭建 self-improvement loop。
- 核心定义：Agent 可以从外部反馈中持续改进自己的 Skill；示例用人工反馈，也可以替换成自动 grader。
- 示例任务：GitHub issue triage，把新 issue 分成 `ready-to-implement`、`duplicate`、`needs-info`。
- 关键结构：内层 loop 负责应用 Skill；外层 loop 定期观察内层运行记录和反馈，把可泛化经验改写回 Skill。
- 重要边界：Skill 是文件，所以外层 Agent 不应该只“记住经验”，而应该产生 diff；diff 合并后才反馈回下一次执行。

## 一手补充材料

- 示例仓库 [warpdotdev-demos/issue-triage-loop](https://github.com/warpdotdev-demos/issue-triage-loop) 明确把闭环拆成：新 issue -> 内层 Agent triage -> 人工反馈 -> 定时外层 Agent -> Skill improvement PR -> 人工 review/merge。
- README 强调每条 triage comment 里有 marker + version，维护者 relabel 是强训练信号，改进以 PR 形式提交，不直接改 main。
- `triage-issue` Skill 要求评论以 `<!-- oz-triage v:<N> -->` 开头，说明当前分类，并在评论 footer 里请求 👍/👎 或纠正回复。
- `improve-triage-skill` Skill 会查看最近 14 天的 triage 评论、reactions、human replies、label drift 和 duplicate accuracy，只提炼可泛化 lesson；信号弱时不改。
- GitHub Action 在 issue opened 时触发 `warpdotdev/oz-agent-action@v1`，把 issue number、repository、title 传给 `triage-issue` Skill。
- `oz-for-oss` README 把 Oz for OSS 定位为开源自动化平台，能力包括 issue triage、spec 草拟、PR 实现、PR review、评论响应和 slash command 验证。

## 文章主线

1. 开头直接下判断：Agent 总学不会，往往不是模型问题，而是反馈没有沉淀到可执行的 Skill。
2. 解释 loop 不等于 while 循环；工程上要分成执行 loop 和改进 loop。
3. 用 issue triage 举例：内层负责分类，外层负责观察人类如何纠错。
4. 说明反馈需要结构化：marker、version、reaction、relabel、correction reply。
5. 给出可复用模板：记录、归因、提炼、改 Skill、PR 审核、合并回流。
6. 给边界：不是所有反馈都该改，弱信号不改；改的是通用准则，不是单个 issue hack。

## 配图规划

- 封面：问题 -> Skill 文件 -> 反馈闭环 -> PR 合并，强调“把反馈写回 Skill”。
- 正文图 1：内层 loop 和外层 loop 分离。
- 正文图 2：从人类反馈到 Skill diff 的六步流水线。


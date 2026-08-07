---
title: "Agent Design · MOC"
tags:
  - type/moc
  - topic/agent-design
---

# Agent Design(设计空间)

Agent 与 AI 产品的设计方法与取舍:Claude Code 这类工具背后的设计空间,以及一线设计者怎么看待 AI 时代的产品设计与"快慢设计"。

## 文章

- [[post-to-wechat/2026-07-30/backend-context-engineering/backend-context-engineering|Claude Code 越聪明越烧钱？先检查后端有没有让它猜]] · 见 [[context-engineering]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-27/graph-engineering/graph-engineering|多 Agent 别急着画 Graph：先守住这 4 条工程边界]] · 见 [[agent-runtime]] / [[managed-agents]]
- [[post-to-wechat/2026-07-25/nl2dashboard/nl2dashboard|别让 Agent 重写整个页面：NL2Dashboard 用 IR 管住修改边界]] · 见 [[agent-runtime]]
- [[post-to-wechat/2026-07-25/claude-opus-5/article|Opus 5 不是全面替换：先把最难的任务交给它]] · 见 [[claude-code]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/article|微服务别直接塞给 Agent：先补上下文地图和契约测试]] · 见 [[context-engineering]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/article|别硬啃 50 万行源码：先读这本 Claude Code 小书]] · 见 [[claude-code]] / [[agent-runtime]] / [[context-engineering]]
- [[wechat-drafts/2026-06-30-multi-agent-skills-management/article|多 Agent 最大坑不在数量，而在 Skill 边界]]〔草稿〕· 见 [[agent-skills]] / [[managed-agents]]
- [[context-attention-drift|上下文没爆，模型为什么还漏指令？]] · 见 [[context-engineering]] / [[agent-memory]] / [[agent-runtime]]
- [[wechat-drafts/2026-06-20-scholarquest/article|论文 Agent 搜得多还找偏？ScholarQuest 把坑量出来了]]〔草稿〕· 见 [[managed-agents]] / [[rag]]
- [[trellis-agent-workbench|AI 编程总是失忆？Trellis 把规范和任务写回仓库]] · 见 [[agent-runtime]] / [[agent-memory]]
- [[wechat-drafts/2026-06-18-skill-self-improvement-loop/article|Agent 为什么总学不会？把反馈写回 Skill]]〔草稿〕· 见 [[agent-skills]] / [[agent-memory]]
- [[enterprise-plugin-governance|Codex、Claude 插件越装越乱？企业落地先管边界]] · 见 [[claude-code]] / [[agent-skills]]
- [[wechat-drafts/2026-06-13-gsd-build-sdd/article|Agent 长任务总烂尾？GSD 用阶段循环跑到 PR]]〔草稿〕· 见 [[context-engineering]] / [[agent-skills]]
- [[agent-loop-engineering|Agent 不是靠好 Prompt，而是靠循环跑到验收]]
- [[claude-code-workflow-goal|Agent 长任务别乱开:Claude Code workflow 和 goal 怎么选]]
- [[goal-command-claude-code-codex|用 /goal 让 Claude Code 和 Codex 跑到有证据]]
- [[jxnlco-codex-workbench|别只让 Codex 写代码:把它用成工作台]] · 见 [[agent-runtime]]
- [[akshay-agent-harness|别再怪模型了,Agent 真正拼的是 Harness]] · 见 [[agent-runtime]]
- [[multi-agent-team|多 Agent 为什么越跑越乱?从分工、交接到评审讲清楚]] · 见 [[agent-runtime]]

## 原始素材

- [[post-to-wechat/2026-07-27/graph-engineering/research-notes|Graph Engineering 原文与一手资料研究笔记]] · 见 [[agent-runtime]] / [[managed-agents]]
- [[post-to-wechat/2026-07-25/nl2dashboard/research-notes|NL2Dashboard 论文研究笔记]] · 见 [[agent-runtime]]
- [[post-to-wechat/2026-07-25/claude-opus-5/research-notes|Claude Opus 5 官方发布资料]] · 见 [[claude-code]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/source/research-notes|跨微服务 Agent 上下文与契约验证研究笔记]] · 见 [[context-engineering]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/source/dotey-microservice-agent-source|宝玉：跨微服务 Agent 问答源文]] · 见 [[context-engineering]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/research-notes|Claude Code From Scratch 研究笔记]] · 见 [[claude-code]] / [[agent-runtime]] / [[context-engineering]]
- [[post-to-wechat/2026-06-20/context-attention-drift/source/research-notes|上下文没爆，模型为什么还漏指令？研究笔记]] · 见 [[context-engineering]] / [[agent-memory]] / [[agent-runtime]]
- [[wechat-drafts/2026-06-20-scholarquest/research-notes|ScholarQuest 论文编译研究笔记]] · 见 [[managed-agents]] / [[rag]]
- [[raw/arxiv-2606-20235/github-readme|ScholarQuest README]] · 见 [[managed-agents]] / [[rag]]
- [[post-to-wechat/2026-06-20/trellis-agent-workbench/source/research-notes|Trellis 研究笔记]] · 见 [[agent-runtime]] / [[agent-memory]]
- [[wechat-drafts/2026-06-18-skill-self-improvement-loop/research-notes|Agent Skill 自我改进闭环研究笔记]] · 见 [[agent-skills]] / [[agent-memory]]
- [[post-to-wechat/2026-06-12/enterprise-plugin-governance/source/research-notes|Codex 与 Claude 企业级 Plugin 管理研究笔记]] · 见 [[agent-skills]]
- [[wechat-drafts/2026-06-13-gsd-build-sdd/research-notes|GSD Core 与 SDD 对比研究笔记]] · 见 [[context-engineering]] / [[agent-skills]]
- [[post-to-wechat/2026-06-11/agent-loop-engineering/source/research-notes|Agent Loop Engineering 研究笔记]]
- [[post-to-wechat/2026-06-07/claude-code-workflow-goal/source/research-notes|Claude Code workflow / goal 研究笔记]]
- [[claude-code-design-space|Claude Code 的设计空间]]
- [[claude-design-ryan-mather|和 Ryan Mather 聊 Claude 的设计]]
- [[2045162321589252458|Flomerboy:Claude 设计相关推文]]

## 相关主题

[[claude-code]] · [[agent-runtime]] · [[managed-agents]]

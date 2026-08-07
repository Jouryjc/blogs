---
title: "Context Engineering · MOC"
tags:
  - type/moc
  - topic/context-engineering
---

# Context Engineering

上下文工程:Agent 的很多 token 其实浪费在和后端做低效沟通上。怎么把上下文组织好、把 token 花在刀刃上,从而既提速又降本。

## 文章

- [[post-to-wechat/2026-07-30/backend-context-engineering/backend-context-engineering|Claude Code 越聪明越烧钱？先检查后端有没有让它猜]] · 见 [[agent-runtime]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/article|微服务别直接塞给 Agent：先补上下文地图和契约测试]] · 见 [[agent-design]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/article|别硬啃 50 万行源码：先读这本 Claude Code 小书]] · 见 [[claude-code]] / [[agent-runtime]] / [[agent-skills]]
- [[post-to-wechat/2026-06-29/task-specific-knowledge-bases/task-specific-knowledge-bases|别把模型当统一知识库：同一事实，换问法就换参数]] · 见 [[knowledge-base]] / [[agent-memory]]
- [[post-to-wechat/2026-06-25/skill-hidden-configs/article|Skill 老是不听话？先看这 5 个冷门配置]] · 见 [[agent-skills]] / [[agent-runtime]]
- [[context-attention-drift|上下文没爆，模型为什么还漏指令？]] · 见 [[agent-memory]] / [[agent-design]] / [[agent-runtime]]
- [[trellis-agent-workbench|AI 编程总是失忆？Trellis 把规范和任务写回仓库]] · 见 [[agent-runtime]] / [[agent-memory]]
- [[wechat-drafts/2026-06-13-gsd-build-sdd/article|Agent 长任务总烂尾？GSD 用阶段循环跑到 PR]]〔草稿〕 · 见 [[agent-skills]] / [[agent-design]]
- [[rag-embedding-rerank|RAG 总找错资料？Embedding 和 Rerank 讲清楚]] · 见 [[rag]]
- [[claude-prompt-engineering|为什么 Claude 总是不按你想的来?从角色、上下文到约束讲清楚]]
- [[claude-context-deep-dive|Claude Code 上下文管理深度拆解]]

## 原始素材

- [[post-to-wechat/2026-07-30/backend-context-engineering/research-notes|Backend Context Engineering 研究笔记]] · 见 [[agent-runtime]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/source/research-notes|跨微服务 Agent 上下文与契约验证研究笔记]] · 见 [[agent-design]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/source/dotey-microservice-agent-source|宝玉：跨微服务 Agent 问答源文]] · 见 [[agent-design]] / [[agent-runtime]]
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/research-notes|Claude Code From Scratch 研究笔记]] · 见 [[claude-code]] / [[agent-runtime]] / [[agent-skills]]
- [[post-to-wechat/2026-06-29/task-specific-knowledge-bases/research-notes|Task-specific knowledge bases 论文研究笔记]] · 见 [[knowledge-base]] / [[agent-memory]]
- [[post-to-wechat/2026-06-25/skill-hidden-configs/research-notes|Skill 冷门配置研究笔记]] · 见 [[agent-skills]] / [[agent-runtime]]
- [[post-to-wechat/2026-06-20/context-attention-drift/source/research-notes|上下文没爆，模型为什么还漏指令？研究笔记]] · 见 [[agent-memory]] / [[agent-design]] / [[agent-runtime]]
- [[post-to-wechat/2026-06-20/trellis-agent-workbench/source/research-notes|Trellis 研究笔记]] · 见 [[agent-runtime]] / [[agent-memory]]
- [[wechat-drafts/2026-06-13-gsd-build-sdd/research-notes|GSD Core 与 SDD 对比研究笔记]] · 见 [[agent-skills]] / [[agent-design]]
- [[post-to-wechat/2026-06-09/rag-embedding-rerank/source/research-notes|RAG Embedding 和 Rerank 研究笔记]]
- [[post-to-wechat/2026-05-20/khairallah-2057030983044710442/source/original-article|How to Master Claude Prompt Engineering(原文)]]
- [[avi-context-engineering-claude-code|Claude Code 成本怎么降 3 倍?真正该优化的,是后端上下文]]
- [[2046500537584218438|Avi Chawla:用 Karpathy 式上下文把 Claude Code 成本降 3 倍(推文)]]

## 相关主题

[[claude-code]] · [[prompt-caching]] · [[rag]] · [[agent-memory]]

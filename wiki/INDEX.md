---
title: "知识库首页 · INDEX"
tags:
  - type/moc
---

# AI Agent 工程化知识库

这是一个关于 **AI Agent 工程化** 的个人知识库:围绕 Claude Code、Agent Skills、Agent 记忆、上下文工程、RAG、Agent 运行时与安全等方向,把原始素材(论文 / 推文 / 深度笔记)整理成成品文章,并用 wikilink 串成一张可导航的知识网络。

> 用法:从下面的「主题地图」进入任意主题页(MOC),每个主题页汇总该方向的成品文章、原始素材与相关主题。关系图(Graph)按 `type/` 标签着色:MOC / 文章 / 原始素材 / 推文 / 报告·资讯。

## 🗺️ 主题地图

- [[claude-code]] —— Claude Code 用法、配置(AGENTS.md / CLAUDE.md)与底层设计
- [[agent-skills]] —— 把软件工程流程写成 Agent 可执行的「技能」
- [[agent-memory]] —— 让 Agent 拥有长期记忆的架构与工程实践
- [[context-engineering]] —— 上下文工程:把 token 花在刀刃上
- [[prompt-caching]] —— Prompt 缓存如何提速与降本
- [[rag]] —— 检索增强与 TTFT 优化
- [[managed-agents]] —— Agent 基础设施的产品化
- [[agent-runtime]] —— 最小可用的 Agent 运行时与编排循环(Hermes / Ralph)
- [[agent-design]] —— Agent / 产品的设计空间与方法
- [[agent-safety]] —— Agent 时代的新攻击面与陷阱
- [[knowledge-base]] —— 用 AI 把代码 / 资料变成知识库
- [[ai-industry]] —— 行业动态、模型发布、访谈与每日热点

## 🆕 最近文章

- [[post-to-wechat/2026-08-22/codex-harness/codex-harness|别只盯着模型：Codex 难抄的是这套 Harness]] · 2026-08-23
- [[post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache|Agent 上下文越跑越贵，先把 KV Cache 从推理进程里拆出来]] · 2026-08-21
- [[post-to-wechat/2026-08-16/gpu-inference-memory-bandwidth/gpu-inference-memory-bandwidth|LLM 单请求推理慢，不是 GPU 算不动，而是权重搬不动]] · 2026-08-16
- [[post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness|DeepSeek 没做第二个 Claude Code：它把 Agent 拆成了插件]] · 2026-08-13
- [[wechat-drafts/2026-08-10-agent-memory-observations/article|你的 Agent 什么都记得，却什么都不懂：记忆系统缺的不是检索，是模式识别]] · 2026-08-10
- [[post-to-wechat/2026-08-10/context-graph-roadmap/context-graph-roadmap|RAG 找到 Redis，却答不出谁会挂：用 Context Graph 接起依赖链]] · 2026-08-10
- [[post-to-wechat/2026-08-06/one-gpu-5-models/one-gpu-5-models|5 个模型，1 张 GPU：小模型省的钱，别还给 serving]] · 2026-08-06
- [[post-to-wechat/2026-08-02/fde-career-guide/article|AI 项目不缺 Demo，缺能把它送进生产的 FDE]] · 2026-08-02
- [[post-to-wechat/2026-07-30/backend-context-engineering/backend-context-engineering|Claude Code 越聪明越烧钱？先检查后端有没有让它猜]] · 2026-07-30
- [[post-to-wechat/2026-07-27/graph-engineering/graph-engineering|多 Agent 别急着画 Graph：先守住这 4 条工程边界]] · 2026-07-27
- [[post-to-wechat/2026-07-25/nl2dashboard/nl2dashboard|别让 Agent 重写整个页面：NL2Dashboard 用 IR 管住修改边界]] · 2026-07-25
- [[post-to-wechat/2026-07-25/claude-opus-5/article|Opus 5 不是全面替换：先把最难的任务交给它]] · 2026-07-25
- [[post-to-wechat/2026-07-25/guardian-agent-bench/article|Agent 安全别再只改 Prompt：先给工具调用加一道闸]] · 2026-07-25
- [[post-to-wechat/2026-07-01/microservice-agent-context/article|微服务别直接塞给 Agent：先补上下文地图和契约测试]] · 2026-07-01
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/article|别硬啃 50 万行源码：先读这本 Claude Code 小书]] · 2026-07-01
- [[post-to-wechat/2026-06-29/task-specific-knowledge-bases/task-specific-knowledge-bases|别把模型当统一知识库：同一事实，换问法就换参数]] · 2026-06-29
- [[post-to-wechat/2026-06-25/skill-hidden-configs/article|Skill 老是不听话？先看这 5 个冷门配置]] · 2026-06-25
- [[rag-ideablock|RAG 总答偏，先查 chunk]] · 2026-06-22
- [[context-attention-drift|上下文没爆，模型为什么还漏指令？]] · 2026-06-20
- [[trellis-agent-workbench|AI 编程总是失忆？Trellis 把规范和任务写回仓库]] · 2026-06-20
- [[enterprise-plugin-governance|Codex、Claude 插件越装越乱？企业落地先管边界]] · 2026-06-12
- [[agent-loop-engineering|Agent 不是靠好 Prompt，而是靠循环跑到验收]] · 2026-06-11
- [[claude-fable-5-programmers|Claude 5来了，程序员该交出去哪些任务]] · 2026-06-10
- [[rag-embedding-rerank|RAG 总找错资料？Embedding 和 Rerank 讲清楚]] · 2026-06-09
- [[google-agentic-rag|RAG 为什么总漏一跳？Google Agentic RAG 讲清楚]] · 2026-06-08
- [[claude-code-workflow-goal|Agent 长任务别乱开:Claude Code workflow 和 goal 怎么选]] · 2026-06-07

## 📝 在写草稿(wechat-drafts)

- [[wechat-drafts/2026-06-30-multi-agent-skills-management/article|多 Agent 最大坑不在数量，而在 Skill 边界]]
- [[wechat-drafts/2026-06-20-scholarquest/article|论文 Agent 搜得多还找偏？ScholarQuest 把坑量出来了]]
- [[wechat-drafts/2026-06-18-skill-self-improvement-loop/article|Agent 为什么总学不会？把反馈写回 Skill]]
- [[wechat-drafts/2026-06-13-gsd-build-sdd/article|Agent 长任务总烂尾？GSD 用阶段循环跑到 PR]]
- [[wechat-drafts/2026-05-31-claude-dynamic-workflows/article|Claude 大任务为什么烂尾?Workflows 把计划写进脚本]]
- [[wechat-drafts/2026-05-31-ai-second-brain-claude-obsidian/article|别再囤笔记了:让 Claude 读懂你的 Obsidian]]
- [[wechat-drafts/2026-05-26-claude-instruction-conflicts/article|Claude 指令撞车时,谁说了算?]]
- [[wechat-drafts/2026-05-26-custom-claude-plugins/article|Claude 总跑偏?做个 Plugin 固化工作流]]
- [[wechat-drafts/2026-05-25-self-hosted-deep-research/article|Deep Research 最大坑:数据和流程都不在你手里]]

## 📊 报告与资讯

每日 X 热点报告与资讯简报汇总在 [[ai-industry]];最新一期见 [[latest|X 热点日报(最新)]]。

## 📌 说明

- 知识库规范与维护规则见仓库根目录的 [[AGENTS]]。
- 配图 prompt / outline 等生产产物保留在各文章目录内,但**不**纳入本知识网络(已在关系图中过滤)。

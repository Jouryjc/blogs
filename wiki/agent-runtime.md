---
title: "Agent Runtime · MOC"
tags:
  - type/moc
  - topic/agent-runtime
---

# Agent Runtime(运行时与编排)

最小可用的 Agent 运行时与编排循环:Hermes 这类轻量运行时怎么把上下文压缩、工具安全、记忆快照、子 Agent 隔离串起来;Ralph 这类极简循环又如何用"一个 loop"让 Agent 自主跑完复杂任务。

## 文章

- [[post-to-wechat/2026-08-22/codex-harness/codex-harness|别只盯着模型：Codex 难抄的是这套 Harness]] · 见 [[agent-design]] / [[context-engineering]]
- [[post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache|Agent 上下文越跑越贵，先把 KV Cache 从推理进程里拆出来]] · 见 [[context-engineering]] / [[prompt-caching]]
- [[post-to-wechat/2026-08-16/gpu-inference-memory-bandwidth/gpu-inference-memory-bandwidth|LLM 单请求推理慢，不是 GPU 算不动，而是权重搬不动]]
- [[post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness|DeepSeek 没做第二个 Claude Code：它把 Agent 拆成了插件]] · 见 [[agent-design]]
- [[post-to-wechat/2026-08-06/one-gpu-5-models/one-gpu-5-models|5 个模型，1 张 GPU：小模型省的钱，别还给 serving]]
- [[post-to-wechat/2026-08-02/fde-career-guide/article|AI 项目不缺 Demo，缺能把它送进生产的 FDE]] · 见 [[ai-industry]]
- [[post-to-wechat/2026-07-30/backend-context-engineering/backend-context-engineering|Claude Code 越聪明越烧钱？先检查后端有没有让它猜]] · 见 [[context-engineering]] / [[agent-design]]
- [[post-to-wechat/2026-07-27/graph-engineering/graph-engineering|多 Agent 别急着画 Graph：先守住这 4 条工程边界]] · 见 [[agent-design]] / [[managed-agents]]

- [[post-to-wechat/2026-07-25/nl2dashboard/nl2dashboard|别让 Agent 重写整个页面：NL2Dashboard 用 IR 管住修改边界]] · 见 [[agent-design]]
- [[post-to-wechat/2026-07-25/claude-opus-5/article|Opus 5 不是全面替换：先把最难的任务交给它]] · 见 [[claude-code]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/article|微服务别直接塞给 Agent：先补上下文地图和契约测试]] · 见 [[context-engineering]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/article|别硬啃 50 万行源码：先读这本 Claude Code 小书]] · 见 [[claude-code]] / [[context-engineering]] / [[agent-skills]]
- [[post-to-wechat/2026-06-25/skill-hidden-configs/article|Skill 老是不听话？先看这 5 个冷门配置]] · 见 [[agent-skills]] / [[context-engineering]]
- [[context-attention-drift|上下文没爆，模型为什么还漏指令？]] · 见 [[context-engineering]] / [[agent-memory]] / [[agent-design]]
- [[trellis-agent-workbench|AI 编程总是失忆？Trellis 把规范和任务写回仓库]] · 见 [[agent-memory]] / [[context-engineering]]
- [[agent-loop-engineering|Agent 不是靠好 Prompt，而是靠循环跑到验收]]
- [[claude-fable-5-programmers|Claude 5来了，程序员该交出去哪些任务]] · 见 [[ai-industry]]
- [[google-agentic-rag|RAG 为什么总漏一跳？Google Agentic RAG 讲清楚]] · 见 [[rag]]
- [[claude-code-workflow-goal|Agent 长任务别乱开:Claude Code workflow 和 goal 怎么选]]
- [[codex-sdk-python|别只把 Codex 当聊天框:Python SDK 调用本地 Agent]]
- [[goal-command-claude-code-codex|用 /goal 让 Claude Code 和 Codex 跑到有证据]]
- [[jxnlco-codex-workbench|别只让 Codex 写代码:把它用成工作台]]
- [[akshay-agent-harness|别再怪模型了,Agent 真正拼的是 Harness]]
- [[multi-agent-team|多 Agent 为什么越跑越乱?从分工、交接到评审讲清楚]]
- [[codex-remote-control|Codex 支持远程操作:手机接管开发环境]]
- [[outputs/ralph-orchestrator|Ralph Orchestrator:用一个循环让 AI Agent 自主完成复杂任务]]

## 原始素材

- [[post-to-wechat/2026-08-22/codex-harness/source/research-notes|Codex Harness 架构研究笔记]] · 见 [[agent-design]] / [[context-engineering]]
- [[post-to-wechat/2026-08-22/codex-harness/source/official-snapshot|Codex Harness 官方事实快照]] · 见 [[agent-design]] / [[context-engineering]]
- [[post-to-wechat/2026-08-22/codex-harness/source/source-manifest|Codex Harness 一手资料清单]] · 见 [[agent-design]] / [[context-engineering]]
- [[x-to-markdown/akshay_pachaar/2074502882812952666/your-kv-caching-is-broken|Akshay: Your KV Caching Is Broken (X Article)]] · 见 [[context-engineering]] / [[prompt-caching]]
- [[post-to-wechat/2026-08-21/lmcache-kv-cache/source/research-notes|LMCache 与 KV Cache 复用研究笔记]] · 见 [[context-engineering]] / [[prompt-caching]]
- [[x-to-markdown/akshay_pachaar/2087928032904523980/how-a-gpu-actually-works|Akshay: How a GPU Actually Works (X Article)]]
- [[post-to-wechat/2026-08-16/gpu-inference-memory-bandwidth/source/research-notes|GPU 推理性能补充研究]]
- [[post-to-wechat/2026-08-13/deepseek-harness/source/research-notes|DeepSeek Harness 研究笔记]] · 见 [[agent-design]]
- [[post-to-wechat/2026-08-13/deepseek-harness/source/official-snapshot|DeepSeek Harness 一手资料快照]] · 见 [[agent-design]]
- [[akshay-5-models-one-gpu|Akshay: How to serve 5 models on one GPU (X Article)]]
- [[post-to-wechat/2026-08-02/fde-career-guide/research-notes|FDE 岗位与转型研究笔记]] · 见 [[ai-industry]]
- [[post-to-wechat/2026-07-30/backend-context-engineering/research-notes|Backend Context Engineering 研究笔记]] · 见 [[context-engineering]] / [[agent-design]]
- [[post-to-wechat/2026-07-25/nl2dashboard/research-notes|NL2Dashboard 论文研究笔记]] · 见 [[agent-design]]
- [[post-to-wechat/2026-07-25/claude-opus-5/research-notes|Claude Opus 5 官方发布资料]] · 见 [[claude-code]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/source/research-notes|跨微服务 Agent 上下文与契约验证研究笔记]] · 见 [[context-engineering]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/microservice-agent-context/source/dotey-microservice-agent-source|宝玉：跨微服务 Agent 问答源文]] · 见 [[context-engineering]] / [[agent-design]]
- [[post-to-wechat/2026-07-01/claude-code-from-scratch/research-notes|Claude Code From Scratch 研究笔记]] · 见 [[claude-code]] / [[context-engineering]] / [[agent-skills]]
- [[post-to-wechat/2026-06-25/skill-hidden-configs/research-notes|Skill 冷门配置研究笔记]] · 见 [[agent-skills]] / [[context-engineering]]
- [[post-to-wechat/2026-06-20/context-attention-drift/source/research-notes|上下文没爆，模型为什么还漏指令？研究笔记]] · 见 [[context-engineering]] / [[agent-memory]] / [[agent-design]]
- [[post-to-wechat/2026-06-20/trellis-agent-workbench/source/research-notes|Trellis 研究笔记]] · 见 [[agent-memory]] / [[context-engineering]]
- [[post-to-wechat/2026-06-11/agent-loop-engineering/source/research-notes|Agent Loop Engineering 研究笔记]]
- [[post-to-wechat/2026-06-10/claude-fable-5-programmers/source/research-notes|Claude Fable 5 / Mythos 5 研究笔记]] · 见 [[ai-industry]]
- [[post-to-wechat/2026-06-08/google-agentic-rag/source/research-notes|Google Agentic RAG research notes]]
- [[post-to-wechat/2026-06-07/claude-code-workflow-goal/source/research-notes|Claude Code workflow / goal 研究笔记]]
- [[post-to-wechat/2026-05-19/multi-agent-team/source/original-article|How to Build a Team of AI Agents(原文)]]
- [[post-to-wechat/2026-05-15/codex-remote-control/sources|Codex Remote Control 资料笔记]]
- [[raw/ralph-orchestrator|Ralph Orchestrator 笔记]]
- [[ralph|Ralph:一个极简的 Agent 循环]]
- [[hermes-agent|Hermes Agent:一个最小可用的 Agent 运行时]]
- [[hermes-nvidia-minimax-setup|用 NVIDIA + MiniMax 跑通 Hermes Agent]]
- [[2045521315646599471|Pierce Zhang:Hermes + NVIDIA + MiniMax M2 配置(推文)]]

## 相关主题

[[rag]] · [[managed-agents]] · [[agent-design]] · [[agent-memory]] · [[agent-safety]]

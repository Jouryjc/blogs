---
title: "Agent Runtime · MOC"
tags:
  - type/moc
  - topic/agent-runtime
---

# Agent Runtime(运行时与编排)

最小可用的 Agent 运行时与编排循环:Hermes 这类轻量运行时怎么把上下文压缩、工具安全、记忆快照、子 Agent 隔离串起来;Ralph 这类极简循环又如何用"一个 loop"让 Agent 自主跑完复杂任务。

## 文章

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

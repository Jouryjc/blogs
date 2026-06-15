---
title: "Agent Loop Engineering 研究笔记"
source: "https://x.com/sairahul1/status/2064277888216555684"
source_author: "Rahul"
created_at: "2026-06-11"
tags:
  - type/source
  - topic/agent-runtime
  - topic/agent-design
  - topic/agent-skills
  - topic/agent-memory
moc:
  - "[[agent-runtime]]"
  - "[[agent-design]]"
  - "[[agent-skills]]"
  - "[[agent-memory]]"
related:
  - "[[agent-loop-engineering]]"
---

# Agent Loop Engineering 研究笔记

## 原始素材

- 原始链接: https://x.com/sairahul1/status/2064277888216555684
- 作者: Rahul, @sairahul1
- 发布时间: 2026-06-09 09:26:15 UTC
- X 长文标题: Loops: What Every AI Engineer Needs to Know in 2026
- 本地源文件:
  - `source-fxtwitter.json`
  - `source-vxtwitter.json`
  - `source-cover.jpg`

## 标题候选

1. 推荐标题: Agent 不是靠好 Prompt，而是靠循环跑到验收
2. 稳妥标题: Loop Engineering：让 Agent 从提示词走向可验收流程
3. 大众标题: 别再一条条催 AI：让 Agent 自己跑完一轮
4. 专家标题: 从 Prompt 到 Loop：AI Agent 的反馈循环怎么设计
5. 反差标题: 最大坑不在 Prompt，而在没有验收循环

最终选择: `Agent 不是靠好 Prompt，而是靠循环跑到验收`

## 原文主线

Rahul 的长文围绕两句最近传播很广的话展开:

- Peter Steinberger: 不应该再只是提示 coding agent，而应该设计能提示 agent 的循环。
- Boris Cherny: 他不再直接 prompt Claude，而是运行会 prompt Claude 并决定下一步的 loops。

原文的中心判断:

- Prompting 是人工一轮一轮驱动 agent。
- Looping 是人先设计一个反馈循环，让 agent 在其中发现、计划、执行、验证、迭代。
- 最简单的 loop 骨架是 `Goal -> Action -> Check -> Fix -> Repeat until done`。
- 单 Agent loop 适合聚焦任务；fleet loop 用 orchestrator、specialists、subagents 做更大任务。
- Open loop 探索强但烧 token；closed loop 有明确路径、质量闸门和停止条件，更适合普通预算。
- 原文强调 DeepSeek、Kimi、MiniMax 等低成本模型让大规模 agent loop 更经济。

## 一手资料补强

### Loop 不是新名词，关键是反馈和停止条件

OpenAI 的长任务文章把 Codex 的工作循环写成: plan, edit code, run tools, observe results, repair failures, update docs/status, repeat。它强调让 agent 长时间保持稳定的不是一个巨型 prompt，而是 agent loop 里的真实反馈、外部状态和可持续 steering。

来源: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex

### Codex /goal 的关键是 contract

Codex `/goal` 文档强调，重要部分是 contract: agent 开始前必须知道什么叫 done。对迁移任务来说，done 可能是新路径通过 contract tests，旧路径仍有 rollback；对原型来说，done 可能是应用能 build、launch，并匹配参考行为。

来源: https://developers.openai.com/codex/use-cases/follow-goals

### Automations 定义节奏，skills 定义方法

OpenAI Codex best practices 里对 automations 的定位很清楚: 稳定、重复的工作流可以设定项目、prompt、cadence 和执行环境，让 Codex 在后台运行。文档给出的有用规则是: skills define the method, automations define the schedule。

来源: https://developers.openai.com/codex/learn/best-practices

### Worktrees 解决并行 agent 的文件冲突

Codex worktrees 文档说明，worktrees 让 Codex 在同一项目中并行运行多个独立任务，并且不互相干扰。Git 仓库里，automations 会在专用 background worktrees 运行，避免和当前工作冲突。

来源: https://developers.openai.com/codex/app/worktrees

### Skills 是可复用工作流，不只是提示词

Codex Agent Skills 文档说明，一个 skill 会把 task-specific instructions、resources 和 optional scripts 打包起来，让 Codex 更可靠地执行工作流。它不是单句 prompt，而是 workflow authoring format。

来源: https://developers.openai.com/codex/skills

### MCP / connectors 是 loop 进入真实环境的边界

Codex customization 文档把 MCP 定义为连接外部工具和上下文提供者的标准方式，可用于 Linear、GitHub、Figma、浏览器、内部知识服务等。文档还指出 MCP servers 可以暴露 tools、resources、prompts；skills 定义 workflow，MCP 连接外部系统。

来源: https://developers.openai.com/codex/concepts/customization

### Claude Code 的 subagents / hooks / memory 也在补 loop 基础设施

Claude Code subagents 文档显示，subagent 可以有自定义 prompt、工具限制、permission modes、hooks、skills 和独立 memory。Hooks 文档则把 hooks 定义为在 Claude Code 生命周期特定事件上自动执行的命令、HTTP endpoints 或 LLM prompts，可用于格式化、阻断命令、通知、注入上下文等。Memory 文档强调 CLAUDE.md 和项目说明需要具体、可验证，适合放构建命令、测试说明、项目约定。

来源:

- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/memory

### 成本判断需要校准

DeepSeek 官方价格页当前列出 DeepSeek-V4-Flash / Pro，context length 1M，max output 384K，支持 JSON output 和 tool calls；价格表显示 Flash 的 cache-miss input 为 $0.14 / 1M tokens，output 为 $0.28 / 1M tokens，Pro 的 cache-miss input 为 $0.435 / 1M tokens，output 为 $0.87 / 1M tokens，Flash 并发限制为 2500，Pro 为 500。官方页同时提醒价格可能变化，应定期查看。

来源: https://api-docs.deepseek.com/quick_start/pricing

## 写作判断

这篇不应该写成“Loop Engineering 是新潮概念”。更有价值的角度是:

- Prompt 问题的表象是“指令写得不够好”，真实工程问题常常是没有验收循环。
- Loop Engineering 的最小对象不是某个模型，而是一个有触发、上下文、执行、反馈、停止条件的系统。
- 对大多数团队，先做 closed loop。open loop 可以探索，但预算、权限和质量闸门没建立时容易变成贵而乱的自动化。
- 低价模型解决的是可试错成本，不解决验收标准。真正的成本控制来自缩窄路径、外部化状态、拆分权限、记录证据、设置停止条件。

## 文章结构

1. 开头: 先解释读者痛点，为什么“写更好的 Prompt”不是终点。
2. Loop 的定义: 从“一条提示词”变成“有反馈的工作合同”。
3. 先做 closed loop: open loop 很强，但普通团队先要可控。
4. 六个积木: automations, worktrees, skills, MCP/connectors, subagents, memory。
5. 两个落地例子: coding loop 和 research loop。
6. 成本与边界: token burn、低价模型、质量闸门、停止条件。
7. 结尾: 人不是退出工作，而是把判断前移到循环设计。

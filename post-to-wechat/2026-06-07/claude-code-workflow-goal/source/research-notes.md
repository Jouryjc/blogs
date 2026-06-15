---
title: "Claude Code workflow / goal 研究笔记"
tags:
  - type/source
  - topic/claude-code
  - topic/agent-runtime
  - topic/agent-design
moc:
  - "[[claude-code]]"
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[claude-code-workflow-goal]]"
  - "[[goal-command-claude-code-codex]]"
---

# Claude Code workflow / goal 研究笔记

created_at: 2026-06-07

## 标题候选

1. 推荐标题：Agent 长任务别乱开：Claude Code workflow 和 goal 怎么选
2. 稳妥标题：Claude Code workflow 和 goal 的区别：一个管编排，一个管收工
3. 大众标题：Claude Code 两个长任务开关，别再混着用
4. 专家标题：Claude Code Dynamic Workflows vs Goal：编排脚本和完成条件的分界
5. 反差标题：长任务不一定用 /goal：workflow 才是大规模编排入口

最终采用：Agent 长任务别乱开：Claude Code workflow 和 goal 怎么选

## 官方资料要点

### Dynamic workflows

来源：Claude Code Docs - Orchestrate subagents at scale with dynamic workflows
URL: https://code.claude.com/docs/en/workflows

- Dynamic workflows 是 research preview。
- 需要 Claude Code v2.1.154+。
- workflow 是 Claude 为任务写出的 JavaScript 编排脚本，由 runtime 在后台执行。
- 适合 codebase audit、大规模 migration、交叉验证研究、多角度计划评审。
- workflow 的关键差异是 plan 进入 code：脚本保存循环、分支和中间结果，Claude 对话窗口只拿最终结果。
- `/deep-research <question>` 是内置 workflow。
- 自定义 workflow 可通过 `ultracode` 关键字或自然语言 “use a workflow” 触发。
- 保存后的 workflow 会作为 slash command 出现，可保存到 `.claude/workflows/` 或 `~/.claude/workflows/`。
- runtime 限制：workflow 脚本本身不直接访问文件系统或 shell，agent 负责读写和运行命令；最多 16 个并发 agents，单次最多 1000 agents；中途没有常规用户输入，只能通过权限提示暂停。

### Goals

来源：Claude Code Docs - Keep Claude working toward a goal
URL: https://code.claude.com/docs/en/goal

- `/goal` 需要 Claude Code v2.1.139+。
- `/goal <condition>` 设置完成条件，Claude 会跨 turns 继续工作，直到条件满足。
- 每个 turn 结束后，小型快速模型评估条件是否成立；默认评估模型是 Haiku。
- 评估器不调用工具，只能看 Claude 已经展示在对话里的证据。
- 一个 session 只能有一个 active goal；新 goal 会替换旧 goal。
- `/goal` 无参数查看状态；`/goal clear` 清除；`stop/off/reset/none/cancel` 也是 clear 别名。
- condition 最多 4000 字符。
- 可在非交互模式使用：`claude -p "/goal ..."`。
- `/goal` 是 session-scoped prompt-based Stop hook wrapper；auto mode 只自动批准单个 turn 内工具调用，不会启动下一 turn。

## 本机验证

- `claude --version` 输出：`2.1.168 (Claude Code)`。
- 覆盖 dynamic workflows 的 v2.1.154+ 要求，也覆盖 goals 的 v2.1.139+ 要求。

## 本地知识库可复用素材

来源：post-to-wechat/2026-06-04/goal-command-claude-code-codex/goal-command-claude-code-codex.md

可复用判断：

- `/goal` 不是任务描述，而是完成合同。
- 目标必须可验证，证据必须出现在当前会话里。
- 目标写法应该包含 Outcome、Evidence、Constraints、Boundaries、Iteration policy、Blocked stop condition。
- 不建议把模糊任务直接塞进 `/goal`；先 plan，再把 plan 压成可验证 goal。

## 本文判断

- workflow 解决的是“规模化编排”：把 plan 变成可读、可保存、可复跑的脚本，后台调度大量 subagent。
- goal 解决的是“持续收工”：把验收条件挂到当前 session，让 Claude 每轮后根据证据决定继续还是停止。
- 两者不是强弱关系，而是不同层级：workflow 管“谁去做、怎么分治、怎么交叉验证”；goal 管“当前这件事什么时候算完成”。

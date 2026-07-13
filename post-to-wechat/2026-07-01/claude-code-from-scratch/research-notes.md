---
title: "Claude Code From Scratch 研究笔记"
source: "https://diwang.info/claude-code-from-scratch/#/"
source_author: "Windy3f3f3f3f"
tags:
  - type/source
  - topic/claude-code
  - topic/agent-runtime
  - topic/agent-design
  - topic/context-engineering
  - topic/agent-memory
  - topic/agent-skills
moc:
  - "[[claude-code]]"
  - "[[agent-runtime]]"
  - "[[agent-design]]"
  - "[[context-engineering]]"
  - "[[agent-memory]]"
  - "[[agent-skills]]"
---

# Claude Code From Scratch 研究笔记

## 来源

- 在线阅读: https://diwang.info/claude-code-from-scratch/#/
- GitHub 仓库: https://github.com/Windy3f3f3f3f/claude-code-from-scratch
- 本地抓取目录: `raw/`
- 抓取时间: 2026-07-01

## 项目定位

这本书不是 Claude Code 使用教程，而是一份从零构建 Coding Agent 的工程教程。它把 Claude Code 的生产级复杂度拆成一个可运行的最小实现，用 TypeScript 和 Python 两个版本分别复现核心机制。

README 给出的核心事实:

- Claude Code 开源快照约 50 万行 TypeScript。
- 本项目用约 4300 行 TypeScript 和约 3800 行 Python 复现核心架构。
- 课程分为两个阶段: 先构建可用 Coding Agent，再加入记忆、技能、Plan Mode、多 Agent、MCP 等进阶能力。
- 全书 13 章主线，加第 14 章测试指南。

## 可写作主线

### 1. 先把 Claude Code 看成一个受控工具循环

引言和第 1 章反复强调的核心是 Agent Loop: 调用模型，检查 tool_use，执行工具，把结果放回消息历史，再继续调用模型。模型没有继续调用工具时，循环结束。

适合文章里的判断:

- Coding Agent 的心脏不是某个神秘 prompt，而是可观察、可控制的循环。
- 真正从 Copilot / Chat 进入 Agent 的分界线，是模型可以拿到工具反馈并继续修正。

### 2. 工具系统的重点不是数量，而是契约

第 2 章把工具系统拆成工具定义、输入 schema、权限检查、只读/并发/破坏性标记、渲染、结果压缩等完整契约。书中还强调 fail-closed 默认值: 默认不可并发、默认不是只读，避免把危险工具误标成安全工具。

可写作判断:

- 工具不是函数列表，而是 Agent 与真实世界交互的合同。
- 好工具要告诉模型怎么调用，也要告诉运行时怎么授权、并发、渲染和回收输出。

### 3. System Prompt 是工程装配，不是许愿池

第 3 章把 system prompt 拆成身份、系统事实、任务规则、操作风险、工具偏好、输出风格和效率约束。价值不在写得长，而在顺序、边界和反模式接种。

可写作判断:

- Prompt 工程在 Agent 里不是文案，而是运行时装配。
- 项目规则、工具说明、记忆和技能要放在正确位置，才能影响下一步动作。

### 4. 上下文管理决定 Agent 能跑多远

第 7 章是全书最值得优先读的章节之一。它从工具结果持久化、预算裁剪、snip、microcompact 到 auto-compact 逐层压缩。书里也提到 Claude Code 会把稳定系统提示词和动态信息分区，以提高缓存命中。

可写作判断:

- 上下文不是仓库，不能把所有东西塞进去。
- 能长期执行的 Agent，靠的是分层压缩和可回读的外部化结果。

### 5. 记忆和技能是两个不同问题

第 8 章讲记忆只保存不可从当前项目状态推导的信息，分 user、feedback、project、reference 四类，并通过 MEMORY.md 做紧凑索引。第 9 章讲技能是可复用 prompt 模块，有 inline 和 fork 两种执行方式。

可写作判断:

- 记忆解决跨会话认知，技能解决重复工作流。
- 不要把项目当前状态写进记忆，也不要把一次性聊天记录当成技能。

### 6. 多 Agent 和 MCP 是扩展边界

第 11 章的 Sub-Agent 模式强调 fork-return 和上下文隔离。第 12 章 MCP 章节强调 spawn 子进程、JSON-RPC 握手、工具发现、前缀注册、透明路由。

可写作判断:

- 多 Agent 不是人设扩张，而是上下文隔离和任务交接。
- MCP 的价值在于让外部工具变成标准工具池的一部分。

### 7. 这本书最适合的读者

- 想理解 Claude Code 为什么能自动跑任务的开发者。
- 想自己做 Coding Agent / Agent runtime 的工程师。
- 写了很多 prompt，但开始遇到工具、权限、上下文、记忆、技能边界问题的人。
- 不适合只想学 Claude Code 命令用法的人。

## 建议阅读顺序

1. 先读引言和第 1 章，建立 Agent Loop。
2. 再读第 2、3、6 章，理解工具、提示词、权限三角。
3. 接着读第 7 章，上下文管理是分水岭。
4. 想做个人工作流，再读第 8、9、10 章。
5. 想做平台扩展，再读第 11、12、13 章。

## 文章角度

文章定位为荐序，不写成逐章摘要。主标题应抓住读者痛点: 不想硬啃 50 万行源码，但又想真正理解 Claude Code。

可交付资产:

- 一张「先读哪几章」阅读路线表。
- 一组「从这本书带走的 6 个工程判断」。

---
title: "Codex Harness 官方事实快照"
tags:
  - type/source
  - topic/agent-runtime
  - topic/agent-design
  - topic/context-engineering
moc:
  - "[[agent-runtime]]"
  - "[[agent-design]]"
  - "[[context-engineering]]"
related:
  - "[[post-to-wechat/2026-08-22/codex-harness/codex-harness]]"
  - "[[post-to-wechat/2026-08-22/codex-harness/source/research-notes]]"
  - "[[post-to-wechat/2026-08-22/codex-harness/source/source-manifest]]"
---

# Codex Harness 官方事实快照

> 本文件是 2026-08-23 对官方页面与固定提交的压缩记录，不是原文转载。

## 官方当前定义

- Codex App、CLI 与 IDE 等体验由同一套开源 Harness 支撑。
- Harness 位于应用与模型之间，负责收集上下文、推进 Agent Loop、调用工具、应用配置的运行边界、处理审批并把工作延续到后续 Turn。
- 开源的是 Harness 与集成层；模型访问和托管服务是分开的。

来源：`https://learn.chatgpt.com/blog/codex-as-a-platform`

## 三种集成边界

- `codex exec`：适合脚本、CI 或有明确边界的一次性后台任务。
- Codex SDK：适合应用代码启动、恢复或流式读取 Codex 任务。
- App Server：适合 Agent 本身就是产品体验的一部分，需要持久对话、事件流、中断、工具和审批处理。

来源：`https://learn.chatgpt.com/blog/codex-as-a-platform`

## App Server 高层结构

最初的官方架构图把长期运行的 App Server 拆成四块：

1. 输入传输层读取客户端 JSON-RPC 消息。
2. Message Processor 将客户端请求分发成内部操作，并把 Core 事件转成面向 UI 的协议消息。
3. Thread Manager 创建和管理 Core Thread。
4. 每个 Core Thread 承载一个线程的 Agent 运行时。

来源：`https://openai.com/index/unlocking-the-codex-harness/`

## Thread / Turn / Item

- Thread：一段可持续、可恢复的用户与 Codex 会话，包含多个 Turn。
- Turn：一次由用户输入发起的 Agent 工作单元，内部可以有多轮模型推理和工具调用。
- Item：Turn 中可单独展示和持久化的原子输入或输出，例如用户消息、Agent 消息、推理、命令执行、文件修改和审批。

来源：官方 App Server 文档与固定提交 `codex-rs/app-server/README.md`。

## 当前稳定生命周期

1. 连接建立后先发送 `initialize`，随后客户端发出 `initialized` 通知。
2. 使用 `thread/start`、`thread/resume` 或 `thread/fork` 得到 Thread。
3. 使用 `turn/start` 发送输入。
4. 客户端持续接收 `turn/started`、`item/started`、增量事件、`item/completed` 等通知。
5. 完成或中断时收到 `turn/completed`。

固定提交中的协议映射仍包含这些名称：

- `thread/started`
- `turn/started`
- `turn/completed`
- `item/started`
- `item/completed`
- `item/agentMessage/delta`

## 为什么必须双向

App Server 不只是向客户端推送流式文本。命令执行、文件修改或工具补充输入都可能由服务端向客户端发起请求，例如：

- `item/commandExecution/requestApproval`
- `item/fileChange/requestApproval`
- `item/tool/requestUserInput`

客户端回复之前，相关动作或当前 Turn 可以暂停。这是普通单向流式 API 难以完整表达的控制关系。

## 源码交叉验证

- `ThreadManager` 的源码注释明确写明其职责是创建 Thread 并将其维护在内存中；内部映射保存 `ThreadId -> Arc<CodexThread>`，同时持有认证、模型、环境、Skills、Plugins、MCP 和 Thread Store 等共享服务。
- `CodexThread` 的源码注释把它称为组成一个 Thread 的双向消息流通道；它包装 Session、I/O 与 rollout path，并提供提交操作、关闭和等待终止等方法。
- `MessageProcessor` 不是单一 `match`，而是组合初始化、线程、Turn、配置、文件系统、Git、MCP、插件等多个请求处理器；连接状态会记录初始化、实验 API 能力和通知退订。
- `transport.rs` 为连接维护有界发送队列；慢连接队列填满时会断开该连接。README 同时要求客户端将入口过载视为可重试错误并使用带抖动的指数退避。

## 不写入正文的内容

- 当前 experimental API 的完整字段列表：变化太快，会把文章写成版本手册。
- 未统一条件下的“Codex 比其他 Agent 更强”排名。
- 把 Harness 当成安全沙箱：官方 Agent Loop 文章明确指出 Codex 自带沙箱只覆盖 Codex 提供的 Shell；MCP 工具需要自行执行各自的安全边界。

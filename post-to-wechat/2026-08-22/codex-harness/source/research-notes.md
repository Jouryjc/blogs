---
title: "Codex Harness 架构研究笔记"
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
  - "[[post-to-wechat/2026-08-22/codex-harness/source/official-snapshot]]"
  - "[[post-to-wechat/2026-08-22/codex-harness/source/source-manifest]]"
---

# Codex Harness 架构研究笔记

## 研究问题

1. Harness 与 Agent Loop 的边界是什么？
2. Codex Core、App Server 和客户端分别拥有哪一部分状态与控制权？
3. Thread / Turn / Item 为什么是产品协议，而不只是后端数据结构？
4. 一次用户请求如何变成可展示、可暂停、可恢复的事件流？
5. 自建 Coding Agent 时，什么时候应复用 App Server，什么时候只用 SDK 或 `codex exec`？

## 已确认事实

### 1. Harness 比 Agent Loop 多

官方在 2026-08-19 的平台文章中把 Harness 定义为模型周围的执行系统。除推理与工具循环外，它还负责：长期上下文、执行流展示、失败处理、审批、配置边界和跨 Turn 延续。

写作判断：正文使用“Loop 决定下一步做什么，Harness 决定整段工作怎么活下去”作为通俗区分，但标为编辑性概括，不写成官方原话。

### 2. Core 是单 Thread 运行时，App Server 是客户端集成层

最初的 App Server 官方文章把 Codex Core 描述为同时具备库与运行时两种角色：Agent 逻辑在其中，一个实例管理一个 Thread 的 Agent Loop 与持久化。

固定提交的 `codex-rs/core/src/codex_thread.rs` 中，`CodexThread` 包装 `Session`、`SessionIo`、session source 和 rollout path；`codex-rs/core/src/thread_manager.rs` 则维护多个 `CodexThread`。

当前源码显示职责已经扩展：ThreadManager 还共享认证、模型、环境、Skills、Plugins、MCP、线程存储和扩展注册等服务。因此正文应写“高层边界”，不把早期四组件图当成完整类图。

### 3. App Server 使用双向 JSON-RPC

默认传输是 stdio 上的 JSONL；协议采用 JSON-RPC 2.0 结构，但 wire 上省略 `jsonrpc: 2.0` 头。当前文档还列出 Unix socket 与实验性 WebSocket。

双向的直接证据是 Server Request：命令执行审批、文件修改审批、工具补充输入，都由服务端向客户端发起并等待回复。

### 4. Thread / Turn / Item 是三个不同寿命的原语

- Thread 跨多次用户输入存在，可以 start、resume、fork、archive。
- Turn 是一次输入触发的工作单元，可以 in progress、completed、interrupted 或 failed。
- Item 是可增量更新、完成和持久化的细粒度对象。固定提交里的 `ThreadItem` 类型不仅包含消息，还包含命令、文件修改、MCP 调用、动态工具、计划、Web 搜索、图片生成等多种条目。

写作边界：正文举代表性类型，不罗列全部枚举。

### 5. 初始化是能力协商，不只是打招呼

每条连接必须先 `initialize`，再发 `initialized`。当前连接状态保存客户端名、版本、实验 API 开关、通知退订和 MCP 扩展能力。不同客户端可以声明自己理解的能力，同时屏蔽不需要的通知。

工程含义：App Server 让协议可以演进，而不是把所有客户端锁死在内部 Rust 事件形状上。

### 6. App Server 还承担背压

固定提交 README 写明入口、处理和输出之间使用有界队列；过载时新请求会收到 `-32001`，客户端应退避重试。`transport.rs` 还会在慢连接的输出队列填满后断开连接。

写作判断：这说明“流式事件”不只是 UI 动画，还是必须治理的生产数据通道。

### 7. 安全边界是组合出来的

App Server 负责把 sandbox policy、approval policy 等设置带入 Thread / Turn，并把审批暴露给客户端。但官方 Agent Loop 文章明确指出，Codex 的 Shell 沙箱不自动包住 MCP 工具；MCP 工具需要自己的 guardrail。

写作结论：不能把“使用 Codex Harness”写成“所有工具天然进入统一 OS 沙箱”。Harness 统一的是策略接口与控制流，实际隔离仍取决于工具和运行环境。

## 源码证据索引

固定提交：`343074d4207d572809bd8cea15f4be1d09d98e0b`

| 判断 | 路径 | 关键位置 |
|---|---|---|
| ThreadManager 创建并维护 Thread | `codex-rs/core/src/thread_manager.rs` | `ThreadManager` 注释与 `ThreadManagerState.threads` |
| CodexThread 是双向 Thread 通道 | `codex-rs/core/src/codex_thread.rs` | `CodexThread` 与 impl 顶部注释 |
| MessageProcessor 拆分多个请求域 | `codex-rs/app-server/src/message_processor.rs` | `MessageProcessor` 字段与 initialized dispatch |
| 连接能力与通知退订 | `codex-rs/app-server/src/message_processor.rs` | `ConnectionSessionState` |
| 慢连接背压 | `codex-rs/app-server/src/transport.rs` | `send_message_to_connection` |
| Thread / Turn / Item 协议类型 | `codex-rs/app-server-protocol/src/protocol/v2/` | `thread.rs`、`turn.rs`、`item.rs` |
| 核心事件和审批方法 | `codex-rs/app-server-protocol/src/protocol/common.rs` | request / notification 映射 |

## 作者判断

1. **Codex 最难复制的不是 while loop，而是状态与控制面。** Tool call 循环几十行就能搭出来；难的是让它跨客户端保持一致、在动作前停住、断线后恢复、把中间产物稳定地呈现出来。
2. **App Server 的核心价值是隔离变化。** 模型事件、Core 内部结构和产品 UI 都在变，协议层用少量有生命周期的原语建立缓冲带。
3. **深度集成才需要 App Server。** CI 脚本没必要承担长期连接、事件重建与审批 UI；直接用 `codex exec` 或 SDK 更合适。
4. **宿主应用不能把责任外包干净。** 产品仍应拥有业务上下文、MCP 数据与动作、关键写操作审批、最终记录与恢复策略。

## 文章可复用资产：八项检查表

1. Thread 能否恢复、分叉和归档？
2. Turn 能否中断、失败并明确结束？
3. Item 是否有 started / delta / completed 生命周期？
4. 工具执行前后是否留下可观察事件？
5. 高风险动作能否暂停并等待外部审批？
6. 沙箱、网络与 MCP 权限是否分开治理？
7. 协议是否有初始化、能力协商、版本与背压策略？
8. 客户端断线、慢消费或进程重启后，状态如何恢复？

## 排除或降级的说法

- 不写“所有 Codex 产品永远使用完全相同二进制”；官方文章说明本地客户端通常固定经过测试的 App Server 版本，但部署形态可能变化。
- 不写“App Server 就是 Codex Core 的 HTTP API”；默认路径是本地长期进程与 stdio JSONL，当前 WebSocket 仍有实验性边界。
- 不写“Thread 就是聊天记录”；它同时承载运行配置、工具事件、审批和持久状态。
- 不用 ARC-AGI-3 的单项提升作为 Codex 产品性能承诺；如果成稿保留，只能作为 Harness 设计会改变结果的受限例子，并写清任务与条件。为避免主线偏离，正文默认删除该数字。

## 标题候选方向

标题候选另存 `title-candidates.md`，至少覆盖动作提醒、误区纠正、大众入口、专家架构和反差判断五种机制。

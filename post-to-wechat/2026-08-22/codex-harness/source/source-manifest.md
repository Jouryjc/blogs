---
title: "Codex Harness 一手资料清单"
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
  - "[[post-to-wechat/2026-08-22/codex-harness/source/official-snapshot]]"
---

# Codex Harness 一手资料清单

- 检索日期：2026-08-23（Asia/Singapore）
- 官方仓库：`https://github.com/openai/codex`
- 固定提交：`343074d4207d572809bd8cea15f4be1d09d98e0b`
- 提交时间：2026-08-22T05:54:43Z
- 提交说明：`Report runtime MCP connection status (#40068)`
- 许可证：Apache-2.0（以固定提交根目录许可证文件为准）

## 官方网页

1. `https://learn.chatgpt.com/blog/codex-as-a-platform`
   - 2026-08-19 发布。
   - 给出当前官方定义：Codex Harness 负责上下文、工具、运行边界、审批、跨 Turn 工作；并给出 `codex exec`、SDK、App Server 三种集成边界。
2. `https://openai.com/index/unlocking-the-codex-harness/`
   - 解释 App Server 的来源、四个高层组件和 Thread / Turn / Item 三个协议原语。
3. `https://developers.openai.com/codex/app-server`
   - 当前 App Server 协议文档；页面会重定向到 `https://learn.chatgpt.com/docs/app-server`。
   - 核对初始化握手、传输、线程生命周期、事件与审批。
4. `https://openai.com/index/unrolling-the-codex-agent-loop/`
   - 解释一次 Turn 内模型推理、工具调用、结果回填、上下文增长和终止状态。
5. `https://openai.com/index/harness-engineering/`
   - 只用于说明 Harness Engineering 的工程背景与边界，不把内部产能数据推广为通用结果。

## 固定提交重点路径

- `codex-rs/app-server/README.md`
- `codex-rs/app-server/src/main.rs`
- `codex-rs/app-server/src/message_processor.rs`
- `codex-rs/app-server/src/transport.rs`
- `codex-rs/app-server/src/request_processors/thread_processor.rs`
- `codex-rs/app-server/src/request_processors/turn_processor.rs`
- `codex-rs/app-server-protocol/src/protocol/common.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/thread.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/turn.rs`
- `codex-rs/app-server-protocol/src/protocol/v2/item.rs`
- `codex-rs/core/src/thread_manager.rs`
- `codex-rs/core/src/codex_thread.rs`
- `codex-rs/core/src/session/`

## 版本注意

- 当前仓库比最初的 App Server 官方文章更复杂；文章中的“四组件”是用于理解的高层图，不等于当前源码只有四个模块。
- 当前 README 支持 stdio、Unix socket 和实验性 WebSocket 等传输。正文只把 stdio JSONL 作为稳定默认路径；不会把实验性 WebSocket 写成生产承诺。
- `app-server-protocol` 中存在大量 experimental 字段。正文只使用公开文档中的稳定生命周期与事件名作为主线。

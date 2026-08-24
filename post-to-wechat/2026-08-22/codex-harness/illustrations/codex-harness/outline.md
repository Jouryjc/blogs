# Codex Harness 配图大纲

## 1. Harness 四层定位

- 文件：`01-harness-layers.png`
- 位置：解释 Harness 与 Agent Loop 分层之后。
- 结论：Loop 只处理模型与工具往返，Harness 还承载上下文、状态、权限、事件和恢复。

## 2. App Server 架构

- 文件：`02-app-server-architecture.png`
- 位置：解释 App Server 四个高层组件之后。
- 结论：客户端消费稳定 JSON-RPC，App Server 托管多个 Core Thread，并翻译内部事件。

## 3. Thread / Turn / Item 生命周期

- 文件：`03-thread-turn-item.png`
- 位置：三个协议原语解释之后。
- 结论：一次用户输入会展开为多个有身份、有状态、可审批的 Item。

## 4. 公众号封面

- 文件：`imgs/article-cover.png`
- 主标题：`Codex 难抄的是 Harness`
- 副标题：`Core · App Server · 事件与审批`
- 结构：模型内核位于中央，外圈是 Thread、工具、审批、沙箱与多客户端；居中 1:1 裁切信息完整。

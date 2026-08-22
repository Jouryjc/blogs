# Codex Harness 架构深度文章与公众号草稿设计

## 目标

围绕 OpenAI 官方文章《Unlocking the Codex harness: how we built the App Server》与 Codex 开源仓库，写一篇面向 Agent 工程师、AI 编程工具开发者和技术负责人的中文深度文章，并完成公众号草稿发布。

文章不做 Codex 功能清单，也不把 Harness 简化成 Agent Loop。主线是解释：Codex CLI、IDE、桌面端等表面不同的产品，共享的其实是一套负责会话、上下文、工具、权限、扩展和持久化的运行层；App Server 再把这套运行层转译为客户端可依赖的双向协议。

## 事实边界

- 产品与协议事实以 OpenAI 官方文章、OpenAI Developers 文档和 `openai/codex` 官方仓库为准。
- 源码分析固定到发布时的提交哈希，所有代码路径均记录在研究笔记中。
- 明确区分 Codex Harness、Codex Core、App Server 与客户端 UI，不把四者混称。
- 明确区分官方已经公开的行为、根据源码得出的工程推断和作者判断。
- 不把 Harness 写成安全沙箱的同义词：沙箱只是工具执行边界的一部分。
- 不把 App Server 写成普通请求响应 API：它是承载流式事件、审批和客户端回调的双向 JSON-RPC 协议与长期进程。
- 不把 OpenAI 内部 Harness Engineering 项目的产能数据直接推广为任何仓库都能复现的结果。

## 文章定位

### 目标读者

- 已使用 Codex CLI、IDE 或桌面端，希望理解其底层工作方式的开发者
- 正在开发 Coding Agent、代码审查 Agent、SRE Agent 或自定义客户端的工程师
- 需要评估自建 Harness 与复用 Codex App Server 边界的技术负责人

### 核心判断

Codex Harness 真正提供的不是“让模型循环调用工具”，而是一套把不稳定的模型行为收敛为可恢复、可观察、可审批、可扩展产品体验的运行时。Codex Core 管理单个线程的 Agent 逻辑和状态，App Server 管理多个 Core Thread，并把内部事件压缩成稳定、面向 UI 的协议原语。模型决定一次推理能想到什么，Harness 决定整段工作能否继续、能否被看见、能否被用户叫停，以及失败后能否恢复。

### 长度与语气

- 正文约 4,500–5,500 个中文字符
- 蒸馏小余 2.0：结论先行、机制具体、保留明确的工程判断
- 术语首次出现时用具体场景解释，避免源码导读式堆类名
- 结尾提供一份“自建 Coding Agent Harness 的八项检查表”作为可保存资产

## 标题策略

写作前生成五个至少覆盖四种句式的标题候选。推荐方向：

> 别只盯着模型：Codex 真正难抄的是这套 Harness

标题需要兑现两个承诺：解释 Harness 比 Agent Loop 多了什么，以及说明 Codex Core 与 App Server 如何把同一套 Agent 能力带到多个客户端。

## 叙事结构

1. **先纠正一个误区**：同一个模型接上不同 Harness，表现会像两个产品。
2. **Harness 不是 Loop**：拆出模型、Agent Loop、运行时和产品 UI 四层。
3. **Codex Core 管什么**：单线程里的上下文、工具执行、配置、认证、扩展和持久化。
4. **App Server 为何出现**：从 CLI 同进程 TUI 到 IDE、桌面端和第三方客户端需要共享同一运行层。
5. **Thread / Turn / Item 三个原语**：解释 durable session、一次工作单元与带生命周期的原子事件。
6. **一次请求为什么会变成事件流**：从 `initialize` 到输入、工具调用、增量、diff、审批和完成通知。
7. **双向 JSON-RPC 解决什么**：服务端也能向客户端发起审批或用户输入请求，并暂停当前 Turn。
8. **多线程如何托管**：App Server 的 stdio reader、message processor、thread manager 与 core threads 分工。
9. **协议稳定不等于内部不变**：说明 UI-ready 事件层如何隔离内部实现变化，并讨论版本与能力协商。
10. **什么时候该复用，什么时候该自建**：比较 App Server、Codex SDK、CLI 非交互调用和自建 Harness 的适用边界。
11. **八项检查表**：线程恢复、工具策略、审批、沙箱、事件可观察性、扩展接口、协议版本、失败恢复。

## 研究与验证

研究材料写入 `post-to-wechat/2026-08-22/codex-harness/source/`：

- 官方文章快照与引用位置
- OpenAI Developers 的 App Server 文档
- `openai/codex` 固定提交的源码快照或只读 checkout
- `codex-core`、`codex-app-server`、protocol types、thread/session persistence、tool execution、approval 和 sandbox 相关路径
- 一份按“确认事实 / 源码推断 / 作者判断 / 排除项”组织的 `research-notes.md`

关键架构判断至少由官方文章和源码路径双重验证。文章中如包含协议方法或事件名，必须与发布时文档或固定提交一致。

## 配图方案

统一使用蒸馏小余奶油纸底技术手绘知识卡风格，生成一张 2.35:1 封面和三张正文图：

1. **封面**：`Codex 真正难抄的是 Harness`，中央为模型内核，外圈是线程、工具、审批、沙箱和客户端；标题与主视觉位于居中 1:1 安全区。
2. **四层定位图**：模型 → Agent Loop → Codex Core / Harness → CLI、IDE、桌面端，说明 Harness 不等于 Loop。
3. **App Server 架构图**：客户端、双向 stdio JSON-RPC、message processor、thread manager 与多个 core threads。
4. **Thread / Turn / Item 事件图**：一次用户输入如何展开为消息、工具调用、审批、diff 与完成事件。

每张图只表达一个结论，正文不用手机端难读的复杂表格。

## 产物布局

```text
post-to-wechat/2026-08-22/codex-harness/
├── codex-harness.md
├── title-candidates.md
├── research-notes.md
├── article-review.md
├── article-anti-ai.md
├── doocs-wechat-rendered.html
├── mobile-preview-430px.png
├── wechat-dry-run.json
├── publish-result.json
├── draft-readback.json
├── source/
├── imgs/
├── illustrations/codex-harness/
└── cover-image/codex-harness/
```

主文保留；审稿报告和发布稿使用相邻文件。渲染、dry-run 和发布均以 `article-anti-ai.md` 为准。

## 公众号闭环

1. 完成一手资料与固定提交源码核验。
2. 生成五个标题候选并写初稿。
3. 运行 `xiaoyu-wechat-article-reviewer` 与 `article_metrics.py`，输出审稿报告和去 AI 味版本。
4. 生成并检查封面与三张正文图，确认中文、比例与移动端可读性。
5. 使用 `grace` 主题和 `#0F4C81` 品牌色渲染，生成 430px 预览。
6. 执行公众号 API dry-run，要求本地图片全部识别、无 placeholder。
7. 创建真实草稿，保存 `media_id`。
8. 调用 `draft/get` 回读同一 `media_id`，核对单篇文章、标题、封面与正文图片数量。

## 验收标准

- 正确区分 Harness、Core、App Server 与客户端。
- Thread / Turn / Item、双向审批和事件流的说明均可追溯到官方材料或固定提交源码。
- 至少包含三处明确作者判断：Harness 的真正价值、App Server 的边界、自建与复用的选择。
- 不把内部实验产能写成通用能力承诺，不做无依据性能排名。
- `article-anti-ai.md` 的 AI 味命中与 CTA 警告清零或逐项解释。
- 封面和三张正文图存在且通过视觉检查；430px 预览无溢出、断图或过小文字。
- dry-run 成功，真实发布返回 `success: true` 和 `media_id`。
- `draft/get` 远端回读确认标题、封面和三张正文图。
- 主文按知识库规则进入 `agent-runtime`、`agent-design` 与 `claude-code` 相关导航，且不改动已有 raw 正文。

## 失败处理

- 如果官方文档与固定提交存在差异，分别标注“当前文档行为”和“该提交实现”，不强行合并。
- 图片生成失败时保留提示词和完整文章，不用占位图冒充交付。
- 微信 API 因 IP 白名单或账号配置失败时，保存 dry-run 与失败响应，明确标记 API 阻塞。
- 未完成 `draft/get` 回读时，即使上传成功也不宣布草稿交付完成。

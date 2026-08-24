---
title: "DeepSeek Harness 深度文章研究笔记"
source: "https://github.com/deepseek-ai/deepseek-harness"
source_author: "DeepSeek AI"
created_at: "2026-08-13"
tags:
  - type/source
  - topic/agent-runtime
  - topic/agent-design
moc:
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness]]"
  - "[[post-to-wechat/2026-08-13/deepseek-harness/source/official-snapshot]]"
---

# DeepSeek Harness 深度文章研究笔记

## 2026-08-16 源码复核

- 官方仓库 `master` 与 `HEAD` 仍指向固定提交 `47f943859bef60e4160492346772ded9b24f765a`，文章所用源码截面未漂移。
- `packages/core/agent-loop/src/agent.ts`：`followup` 写入 `next-turn` 并唤醒，`steer` 写入 `next-step` 并唤醒，`inject` 写入 `next-step` 但不唤醒；`preStep()` 在每步领取 Inbox、组装提示词并经过 `agent/pre-step` waterfall。
- `packages/core/session/src/index.ts`：`deriveMessages()` 从 Session Surface 投影模型历史，只处理消息节点；chunk 与轮次边界保留在日志但不会喂回模型，surface replace 会触发派生缓存重建。
- `packages/core/agent-loop/src/tool-calls.ts`：工具可按执行模式并行，但结果和 additional context 按模型调用顺序提交。
- `packages/core/tools/src/index.ts`：工具执行依次经过 `tools/pre-execute`、可选审批、单调 Guard、dispatch 与 `tools/post-execute`；Guard 只有拒绝或不表态，后续监听器不能把拒绝重新放行。

## 一句话定位

DeepSeek Harness（`dsh`）是 DeepSeek AI 官方开源的 Agent Harness。它带有可直接运行的 Web UI 和 Headless 模式，但架构重心不是做一个固定 Coding Agent 产品，而是让模型、循环、工具、会话、文件系统、Shell、沙箱、审批、技能、子 Agent、工作流和 UI 都成为可以由配置组装的插件。

## 已确认事实

### 发布状态

- 官方 README 明确标记为 Developer Preview，并以大写警告将出现兼容性破坏。
- MIT 许可证。
- 官方 npm 运行命令：`npx @deepseek-ai/dsh web`，默认 Web UI 地址为 `http://127.0.0.1:3080`。
- 源码运行需要 Node.js、pnpm 安装和构建；固定提交根 manifest 要求 Node `^22.19.0 || >=24.0.0`。
- 固定提交为 `47f943859bef60e4160492346772ded9b24f765a`。核验时 npm 已从仓库 manifest 的 rc.5 推进到 rc.6，说明发布日版本仍在快速滑动。

### 运行形态

- `dsh web` 是 Web profile 的别名。
- `dsh --profile headless "job"` 运行一次性任务，不启动 HTTP Server。
- Profile 是具名装配；bundle 是一层 Cordis 配置与挂载代码。配置从空树开始，依次叠加 bundle、profile patch、home patch 和 `--patch` overlay。
- `dsh --profile web --dump-config` 可以查看机器上最后组装出的配置树。
- Python SDK `deepseek-harness-sdk` 可以启动同一套内置运行时；官方最小示例明确要求隔离 workspace。

### Cordis 插件模型

- Context 是服务容器，能力通过稳定 `ctx.<key>` 被使用，而不是让消费者导入具体实现。
- 插件用 `inject` 声明依赖。依赖没有就绪时插件保持 pending；依赖消失时，消费方也会卸载，依赖恢复后重新加载。
- 插件注册的提示词、工具 schema、适配器和事件监听器是可逆副作用。卸载插件时对应注册被撤销。
- 事件有 `emit`、`waterfall`、`parallel`、`serial` 四种分发模式。其中 waterfall 类似可短路、可包裹的中间件链。
- Cordis 论文把可组合性拆成两维：空间可组合性管理依赖，时间可组合性负责在组件移除时撤销副作用。论文是 2026-08-13 的在修订预印本，不能把形式化结论写成成熟工业标准。

### Agent 主干

- 核心由会话日志、系统提示词、工具注册表、Agent 接口、默认 Agent Loop 和 Scope 原语构成。
- 默认 Agent Loop 是 `ctx.agentLoop` 的具体实现。扩展插件依赖 Agent 接口，不直接依赖 Loop 包，因此 Loop 仍可替换。
- 一个 step 是一次模型请求加工具调用；一个 turn 可以包含多个 step，直到没有工具结果或其他输入要求继续请求。
- 每一步都会重新组装插件注册的提示词片段与工具 schema。

### 事件溯源与长任务控制

- Session 是只追加的类型化事件日志，是会话唯一真源；模型历史通过 `deriveMessages()` 从日志投影，而不是另存一份可变 messages 数组。
- `turn/start`、`step/start`、`user/message`、`assistant/chunk`、`assistant/message`、`tool/call`、`tool/result` 等是持久事件。
- 输入统一进入 Inbox，但语义不同：`followup` 排队下一个普通轮次；`steer` 在最近的 step 边界改变方向并唤醒 idle Agent；`inject` 把上下文放入下个获准请求，但不会单独唤醒 Agent。
- `agent/pre-step` 可改写或拒绝模型即将看到的输入；`agent/request` 和工具前、中、后执行阶段也都有 waterfall 扩展点。
- 文档明确警告：不能把 `followup()` 的返回或一次 idle 状态简单当成某条消息的因果结果，多条 queued work、steering 和 injection 可能共享一个 running 区间。

### 能力 seam

- 一项可替换能力分三类角色：Service Definition、Service Provider、Consumer。
- Shell 的接口、local/sandbox 实现和面向模型的 Bash 工具是分离的。
- 文件系统和进程提供方可以被替换到远端沙箱；使用稳定 seam 的消费者不需要按提供方分叉。
- Subagent 也是可选 seam，不属于 Agent Loop。仓库提供进程内 spawn/fork，以及 ACP、Codex、Claude Code、dsh SDK 等不同 provider。
- Workflow 使用 Worker Thread 执行编排脚本，但官方限制说明“没有注入 Node 全局”不等于安全隔离，逃逸代码仍可能触达 Node；这点适合作为插件化代价的例子。

### 权限与安全默认值

- Base bundle 默认 `workspace-write` + `ask`，并提供 `read-only`、`workspace-write`、`danger-full-access` 三档预设。
- `danger-full-access` 会关闭审批；官方 Python 最小示例正是这一模式，因此文档要求只在可丢弃 checkout 或容器中运行。
- 工具调用先进入 `tools/pre-execute`，然后经过单调 guard 与可选审批，再执行工具，最后由 `tools/post-execute` 处理结果。
- Session telemetry 插件默认 `DISABLED`；只有显式设置环境变量才上传。启用后导出是会话日志的原始捕获副本，文章应提醒先审查内容和 endpoint。
- 动态 Cordis 工具可以让模型注册新的运行时工具，但官方默认组合故意不加载它，因为动态包代码能触达真实运行时。

## 从源码结构得出的推论

以下不是官方口号原句，而是基于文档和固定提交代码结构的工程判断：

1. **Web UI 是这套 Harness 的第一个产品装配，而不是唯一产品形态。** 证据是 Web 与 Headless 都作为 base 之上的 sibling bundle，Python SDK 也能驱动同一运行时。
2. **“Everything is a plugin”首先是在治理变化，不只是方便第三方加工具。** 可替换 Loop、依赖响应、可逆注册和 patch overlay 指向的是运行时拓扑变化。
3. **事件日志比聊天消息数组更适合长任务。** 它能支撑回放、fork、恢复、transcript、遥测和 UI 投影，但代价是事件 schema、迁移、所有权和异步因果都必须严格设计。
4. **插件边界越细，配置与供应链治理越重要。** 固定提交的 `packages/` 下有 49 个组、219 个二级包目录。这个数字只描述拆分粒度，不等价于 219 项用户功能。
5. **DeepSeek Harness 的直接竞争对象不只是 Claude Code 或 Codex CLI，也包括团队自建的 Agent SDK 和运行时层。** 因为它公开了 profile、bundle、service seam、SDK 和 headless 装配。

## 与其他 Coding Agent 的比较边界

- 不能写成“Claude Code / Codex 没有 Harness”。OpenAI 官方也把 Codex 的 Agent Loop 与执行逻辑称为 Harness，并通过 App Server、SDK 支撑多个产品表面。
- 不能根据仓库结构声称 dsh 的 Agent 效果更好。模型、提示词、工具定义、沙箱和任务集都影响结果，没有统一实验就不做性能排行。
- 可比较的是公开架构重心：成熟 Coding Agent 通常先交付一套有主见的产品体验，再开放 SDK、Hook、MCP 或扩展点；dsh 在首次公开时就把“可替换装配”放到架构正中央。
- 这不是非此即彼。产品默认值负责降低使用门槛，插件底座负责适配不同运行环境；好的系统最终都需要两者。

## 标题候选

1. 推荐：DeepSeek 没做第二个 Claude Code：它把 Agent 拆成了插件
2. 稳妥：模型之外，DeepSeek 开源了 Agent 的另一半
3. 大众：同一个模型，为什么换个编程工具就像换了脑子？
4. 专家：Agent Loop 也能替换：DeepSeek Harness 的 Cordis 插件架构
5. 反差：DeepSeek Harness 最值得看的不是 Web UI，而是可替换的 Agent 底座

五个候选覆盖否定判断、对象与结果、问题、技术机制和反差句式。最终选择推荐标题，但第一屏必须承认它确实附带可运行 Web UI，避免把标题读成“没有 Coding Agent 产品”。

## 写作边界

- 不使用第三方同名 Python 项目的 V4 协议怪癖、缓存折扣或试验数据。
- 不使用 GitHub 星数证明架构价值。
- 不把 Cordis 预印本的“时空可组合性”直接写成安全性保证。
- 不把插件化写成免费收益：版本、依赖、权限、供应链、配置和观测都要付成本。
- 不把 telemetry 默认开启；固定提交默认是禁用。
- 不建议在真实主仓库里直接用 `danger-full-access` 试跑。

## 参考资料

- DeepSeek Harness：https://github.com/deepseek-ai/deepseek-harness
- 官方中文 README：https://github.com/deepseek-ai/deepseek-harness/blob/master/README.zh.md
- 架构文档：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.zh.md
- Cordis 入门：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-primer.zh.md
- Agent 生命周期：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/agent-lifecycle.zh.md
- Cordis 论文：https://github.com/cordiverse/paper
- OpenAI Agent Loop：https://openai.com/index/unrolling-the-codex-agent-loop/
- OpenAI App Server：https://openai.com/index/unlocking-the-codex-harness/

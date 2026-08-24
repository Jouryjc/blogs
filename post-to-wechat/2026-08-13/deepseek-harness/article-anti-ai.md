---
title: "DeepSeek 没做第二个 Claude Code：它把 Agent 拆成了插件"
source: "https://github.com/deepseek-ai/deepseek-harness"
source_author: "DeepSeek AI"
author: "蒸馏小余"
written_style: "蒸馏小余 2.0"
created_at: "2026-08-13"
updated_at: "2026-08-16"
source_commit: "47f943859bef60e4160492346772ded9b24f765a"
coverImage: "imgs/article-cover.png"
summary: "DeepSeek Harness 把模型、Loop、工具、会话、沙箱和 UI 都做成插件。拆开它的收益、代价与当前采用边界。"
tags:
  - type/article
  - topic/agent-runtime
  - topic/agent-design
  - platform/wechat
moc:
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[post-to-wechat/2026-08-13/deepseek-harness/source/research-notes]]"
  - "[[post-to-wechat/2026-08-13/deepseek-harness/source/official-snapshot]]"
---

# DeepSeek 没做第二个 Claude Code：它把 Agent 拆成了插件

DeepSeek 做了一个能读代码、改文件、跑命令的 Web Agent。安装 Node.js 后，一条命令就能启动：

```bash
npx @deepseek-ai/dsh web
```

但如果只把 DeepSeek Harness 看成“DeepSeek 版 Claude Code”，就看小了。

这次开源的 `dsh` 更像一盒 Agent 乐高：模型、Agent Loop、工具、会话、文件系统、Shell、沙箱、审批、Subagent、Workflow，连 Web UI 都是插件。官方把它概括为：**Everything is a plugin。**

我的判断是，它要做的不是另一个固定形态的编程助手，而是一套可重新装配的 Agent 底座。自由度更高，配置、依赖、权限和版本治理也会更重。

先提醒一句：官方仍把它标为 Developer Preview，后续会有破坏性变更。现在适合拆解和试验，不适合直接押上关键生产工作流。

## 模型会想，Harness 才让它动手

模型负责推理，Harness 决定它如何行动。

它要选择这一轮的指令和上下文，把工具暴露给模型，在执行前检查权限，失败后决定重试还是停下，还要处理会话恢复、上下文压缩、中途纠偏和子 Agent 收尾。

所以同一个模型放进不同 Coding Agent，体感会明显不同。差异常常不在“脑子”，而在模型周围的工具说明、执行循环、沙箱和反馈信号。

举个最简单的例子。模型说“修改这个函数并运行测试”，Harness 要先把自然语言变成工具调用，确认文件是否位于工作区、命令是否需要审批，再把测试结果写回下一轮上下文。如果测试失败，它还要决定让模型修复、回滚，还是停下来问人。模型给出意图，Harness 承担执行纪律。

可以把 Agent 粗略分成三层：

```text
产品层：Web / CLI / IDE / 企业工作台
Harness 层：Loop / Context / Tools / Memory / Sandbox
模型层：DeepSeek / Claude / GPT / 其他模型
```

DeepSeek Harness 位于中间。Web、Headless 和 Python SDK，只是同一底座的不同装配。

模型层也没有锁死。默认配置选择 DeepSeek，同时提供多 Provider 适配器，可接 Anthropic、OpenAI 或兼容端点。但“能接”不等于“天然兼容”：流式工具参数、思考内容、上下文上限和错误类型，仍要由适配器翻译。

这也是 Harness 值得单独研究的原因：模型可以替换，但工具契约、权限策略和验证闭环不能每换一个模型就重写一遍。

![Agent 产品、Harness 与模型的三层关系](illustrations/deepseek-harness/01-three-layers.png)

## “一切皆插件”到底拆了什么

很多框架的插件只是多装几个工具。`dsh` 更进一步：`agent-loop` 自己也是插件，会话、提示词、模型适配器、文件系统、进程和审批服务都注册到共享 Context。

支撑这套设计的是 Cordis。插件不绑定具体实现，只声明需要什么服务。依赖没准备好，它先不启动；提供服务的插件离开，依赖方会卸载；新实现补上，再重新挂载。

运行时能看到一组稳定的服务键：`ctx.sessions` 管会话日志，`ctx.tools` 管工具，`ctx.agentLoop` 管循环，`ctx.llm` 管模型适配器，`ctx.fs` 与 `ctx.shell` 管执行环境。工具和 UI 面对的是这些接口，而不是某个写死的实现。

这同时处理两种变化：

- 空间上的依赖：文件搜索只依赖 `ctx.fs`，不用关心后面是本地磁盘、E2B 还是远程文件系统。
- 时间上的生命周期：插件注册了工具、提示词和监听器，卸载时这些副作用也要撤销。

Cordis 把它叫“时空可组合性”。翻成人话就是：**不仅要插得进去，还要拔得干净。**

但可逆副作用不等于安全沙箱。它保证插件卸载后不残留旧状态，不保证插件运行时不会读错文件或执行危险代码。生命周期正确和权限正确，仍是两张验收表。

这一区分很重要。插件“拔得干净”解决热替换和测试隔离；文件访问范围、网络出口和命令审批，仍要靠沙箱与权限系统兜底。不能因为架构支持卸载，就把第三方插件当成可信代码。

![Cordis 插件树与可逆生命周期](illustrations/deepseek-harness/02-cordis-plugin-tree.png)

## Profile 和 Seam 决定怎么装

插件负责能力，Profile 负责装配。

`dsh` 从一棵空插件树开始，依次叠加 Base Bundle、Web 或 Headless Bundle、Profile patch、用户级 patch 和临时 overlay。Web Bundle 加入服务器、API 和 UI；Headless 不启动服务，只接收任务并把最终文本写到 stdout。

这里有两个坑。

第一，patch 命中某一行时会替换整份 `config`，不是深度合并。只改一个字段，却没有重写其他字段，可能把默认值一起抹掉。

第二，配置行顺序不决定加载时序，服务依赖才决定。排查时不要只读手写 patch，应该运行：

```bash
dsh --profile web --dump-config
```

把输出当作 Agent 的运行时物料清单。

另一项关键抽象是 Seam。一项能力被拆成 Service Definition、Provider 和 Consumer。例如 Shell 接口是一条接缝，本地 Bash 与沙箱 Bash 是不同 Provider，模型看到的 `bash` 工具是 Consumer。以后从开发机迁到远程容器，只要替换 Provider，上层 Loop 和 UI 不必跟着重写。

Subagent 也是同一思路。默认 Loop 不规定“只能怎样启动子 Agent”，仓库提供进程内 spawn、fork、ACP、Codex、Claude Code 和 dsh SDK 等 Provider。编排层只依赖统一能力，部署时再决定任务交给谁。这比在主循环里塞满不同后端的判断更容易维护。

## 顺着源码跑一轮

文档里的架构词，最后都能在四段源码里对上。

入口在 `packages/core/agent-loop/src/agent.ts`。`followup()` 把消息放进 `next-turn` 并唤醒 Agent；`steer()` 放进 `next-step`，同样会唤醒；`inject()` 也进入 `next-step`，但不会主动唤醒。三种输入共用 Inbox，调度语义却没有混成一个布尔参数。

每个 step 开始前，`preStep()` 先领取 Inbox 消息、重新组装系统提示词，再经过 `agent/pre-step` waterfall。插件可以补上下文，也可以直接拒绝进入模型请求。通过后，Loop 才把 `turn/start`、`step/start` 和 `user/message` 追加到 Session。

随后 `step()` 调用 `session.deriveMessages()` 构造模型历史。`packages/core/session/src/index.ts` 并不是粗暴遍历所有日志，而是只投影带 `surfaceOp` 的消息节点：流式 chunk、轮次边界留在审计日志里，不会重新喂给模型；上下文压缩发生 replace 时，旧节点也会退出派生历史。返回的消息对象还会被深度冻结，避免消费者偷偷改写事实账本。

模型返回工具调用后，`packages/core/agent-loop/src/tool-calls.ts` 会按工具声明决定串行还是并行。即使并行执行，结果仍按模型原始顺序提交，防止完成时间不同把上下文顺序打乱。

最后才进入 `packages/core/tools/src/index.ts`：`tools/pre-execute` 先给策略插件一次 allow、ask 或 deny 的机会；需要时请求人工审批；单调 Guard 再做不可逆的拒绝；通过后才执行工具体，并经 `tools/post-execute` 处理结果。`tool/call` 与 `tool/result` 都写回 Session，下一步继续从同一条事件流出发。

把这条链串起来，`dsh` 的主循环并不神秘：**消息入队 → step 前组装 → 模型请求 → 工具策略 → 执行结果 → 事件回放。** 插件化发生在每个箭头上，而不是只发生在“多装几个工具”上。

## 任务不是消息，是事件流

DeepSeek Harness 没把会话简化成不断追加的 `messages[]`，而是保存只追加的类型化事件：轮次开始、模型输出、工具调用、审批、执行结果和轮次结束。

模型历史、UI、恢复、fork、transcript 和遥测，都从同一条事件流派生。长任务出了问题，团队能追问：模型当时看到了什么，哪个动作真的发生了，拒绝来自权限层还是工具层。

这比只保存最终聊天记录多了一层“事实账本”。一次任务里可能同时出现三个工具调用：一个执行成功，一个被权限策略拒绝，一个等待人工审批。只有保留调用、审批、结果和轮次边界，才能准确回放现场。

工具执行也不是收到函数名就直接跑，而是经过一条流水线：

```text
tool/call 记账
  → pre-execute 策略与 Hook
  → 单调 Guard
  → 必要时审批
  → execute 执行
  → post-execute 处理结果
  → tool/result 写回日志
```

“单调 Guard”很重要：前面的插件一旦拒绝，后面的插件不能重新放行。审批发生在执行之前，用户拒绝后，工具不会先跑一半再补错误记录。

最终 `tool/result` 还要变成可以被 JSON 无损表达的固定结果，让模型历史、页面和审计日志消费同一份事实。否则很容易出现模型看到一版、UI 显示一版、日志又保存另一版的故障。

长任务中的插话也被拆成三种语义：`followup` 排队新轮次，`steer` 在 step 边界改变方向，`inject` 只给下一次模型请求补上下文，不主动唤醒 Agent。

这说明一个容易被 UI 掩盖的问题：**中途插话不是聊天功能，而是调度语义。**

比如用户发来“先别改数据库”，它应该在下一个工具批次前生效，而不是等整轮任务结束；后台检索返回一段补充资料，可能只需注入下一步，不该无条件唤醒 Agent。把这两种输入都当成普通新消息，长任务迟早会失控。

事件流当然有成本：schema 要迁移，异步顺序要讲清楚，不能把 Agent 变 idle 误当成某条消息已经独立完成。但对需要恢复、回放和审计的长任务，这笔复杂度通常值得。

## 插件化的四张账单

“Everything is a plugin”不是免费午餐。我会先算四张账：

1. 配置：多层 patch 让复用更容易，也让最终行为更难靠肉眼推导。
2. 版本：接口能替换，不代表任意版本都能拼。Developer Preview 阶段必须锁 npm 版本或 Git commit。
3. 权限：Shell、文件系统和 Workflow 插件能触达源码、凭据与进程，第三方 Bundle 必须重新做最小权限和来源审计。
4. 可观测性：失败可能跨越模型、Loop、策略、工具和沙箱，必须保留配置快照、事件日志、审批轨迹与工具结果。

官方默认是 `workspace-write + ask`，并未默认装入可动态注册运行时代码的 Cordis 工具，这个取舍是对的。但一旦自行扩展，风险边界也要自己接管。

团队至少应该为每个插件记录来源、版本、所需服务、文件与网络权限，并保存组合后的配置快照。否则一次升级后，即使文章和提示词都没变，也很难解释 Agent 为什么突然多了一个工具，或者为什么原来的审批消失了。

插件化没有消灭复杂度，只是把复杂度从“改一个巨型内核”，换成“治理一张动态依赖图”。

![插件化的收益与治理账单](illustrations/deepseek-harness/03-benefit-cost.png)

## 它不是产品排行榜

不能因为 DeepSeek 强调 Harness，就说 Claude Code 或 Codex 只有产品壳。成熟 Coding Agent 同样有 Loop、Hook、MCP、Skill、沙箱和多 Agent 能力。

差别主要在默认重心：Claude Code、Codex 先提供一套有主见的产品体验，扩展点围绕产品开放；DeepSeek Harness 第一次公开，就把 Profile、Bundle、Service 和 Provider 摆在中央，Web UI 更像 SDK 的第一个客户。

前者降低普通开发者的选择成本，后者给框架作者更大的改造空间。这是默认值与自由度的取舍，不是代码能力排名。没有统一模型、任务和轨迹，也不能从架构图推断谁写代码更强。

## 谁适合现在试

如果你只想要一个稳定的日常编程助手，我建议先等。

如果你在自建 Agent 平台，需要替换模型、沙箱、文件系统或 UI；或者在研究 steering、恢复、fork 与事件回放，`dsh` 已经值得放进隔离环境。

企业团队不该从“能不能启动”开始评估，而应该从“能不能治理”开始。最小权限、版本锁定、故障回放和可回滚配置，比演示里一次成功的代码修改更重要。

第一轮 PoC，我会这样做：

1. 在可丢弃 checkout 或容器里运行，不碰主工作区。
2. 固定 npm 版本或 Git commit，不追 `latest`。
3. 先用 `read-only`，确认需要写入后再切 `workspace-write`。
4. 用 `--dump-config` 保存实际插件树。
5. 只启用一个模型、最少工具和一种文件系统 Provider。
6. 准备真实任务，覆盖修改、测试、失败恢复和中途 steering。
7. 做一次故障注入：审批拒绝、工具超时或 Provider 中断。
8. 用任务成功率、人工接管次数、回滚能力和排障时间验收。

## 竞争正在移到模型之外

DeepSeek Harness 的价值，不是宣布 Agent 工程问题已经解决。它只是把模型外面的 Loop、上下文、工具、权限和调度拆开，让每一层可以替换，也让原本藏在产品内部的工程账单暴露出来。

我会继续观察三个问题：插件卸载能否保持干净，能力替换是否泄漏实现细节，快速迭代后配置与事件能否迁移。三点站得住，`dsh` 才可能从 Developer Preview 长成 Agent 底座。

建议把上面的 PoC 清单收藏下来。真要试，不要先装十个插件；先拿一个真实任务、一套最小权限和一条可回放日志，把闭环跑通。

关注「蒸馏小余」，下一篇继续拆 Harness 中最容易被低估的一层：steering、injection 和 follow-up 为什么不能共用一种消息语义。

## 参考资料

- [DeepSeek Harness 官方仓库](https://github.com/deepseek-ai/deepseek-harness)
- [DeepSeek Harness 架构文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.zh.md)
- [Cordis：A Programming Paradigm for Spatiotemporal Composability](https://github.com/cordiverse/paper)
- [OpenAI：Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)
- [OpenAI：Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)

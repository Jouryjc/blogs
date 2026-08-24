---
title: "别只盯着模型：Codex 真正难抄的是这套 Harness"
source: "https://learn.chatgpt.com/blog/codex-as-a-platform"
source_author: "Nicolas Bonamy、Derrick Choi、Celia Chen"
author: "蒸馏小余"
written_style: "蒸馏小余 2.0"
created_at: "2026-08-23"
coverImage: "imgs/article-cover.png"
summary: "Codex Harness 不只是 Agent Loop。拆开 Codex Core、App Server、Thread / Turn / Item、双向审批与沙箱边界，看同一套 Agent 如何进入 CLI、IDE 和产品。"
tags:
  - type/article
  - topic/agent-runtime
  - topic/agent-design
  - topic/context-engineering
  - platform/wechat
moc:
  - "[[agent-runtime]]"
  - "[[agent-design]]"
  - "[[context-engineering]]"
related:
  - "[[post-to-wechat/2026-08-22/codex-harness/source/research-notes]]"
  - "[[post-to-wechat/2026-08-22/codex-harness/source/official-snapshot]]"
  - "[[post-to-wechat/2026-08-22/codex-harness/source/source-manifest]]"
  - "[[post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness]]"
  - "[[akshay-agent-harness]]"
---

# 别只盯着模型：Codex 真正难抄的是这套 Harness

同一个 GPT 模型，接进一个几十行的 Tool Call 脚本，可能跑两步就迷路；放进 Codex，却能读仓库、改代码、跑测试、等待审批，中断后再接着干。

差别不只在 Prompt。

Tool Call 循环决定模型下一步调用什么，Harness 则要回答另一组更麻烦的问题：上下文从哪里来？命令在哪执行？什么动作必须停下来问人？中间进度怎么显示？客户端断线后怎么恢复？同一个 Agent 又如何同时进入 CLI、IDE 和桌面端？

OpenAI 在 8 月 19 日把 Codex 定位成一套开放的 Agent Harness。我的判断是，Codex 最难复制的并不是中间那段“模型—工具—模型”循环，而是把一次不稳定的模型运行，收敛成可观察、可暂停、可恢复、可嵌入产品的工作系统。

这篇不列功能清单。我们沿着源码和公开协议，把 Codex Core、App Server、Thread / Turn / Item，以及双向审批链逐层拆开。

## Harness 不是多写一个 while 循环

最小 Agent Loop 并不神秘。

用户给出任务，程序把指令、工具定义和输入送给模型。模型要么返回答案，要么要求调用工具。程序执行工具，把结果追加到上下文，再次请求模型。如此反复，直到模型不再发 Tool Call，而是给出最终消息。

这段 Loop 解决的是“下一步做什么”。

生产级 Coding Agent 还要处理四类工作：

**第一类是上下文。** 除了用户消息，还要装入系统指令、项目里的 `AGENTS.md`、当前目录、可用 Skills、工具定义、历史消息和刚刚产生的文件差异。上下文接近窗口上限时，还要压缩，同时尽量不丢任务状态。

**第二类是执行。** Shell 命令、文件修改、MCP 工具不只是 JSON。它们会改变真实环境，需要工作目录、超时、输出截断、权限、网络策略和失败处理。

**第三类是状态。** 一个任务可能持续几分钟甚至几小时。用户会中途追问、改方向、暂停、恢复或从旧节点分叉。Agent 不能只记住最后一条聊天消息。

**第四类是产品交互。** CLI 想看流式日志，IDE 想看 diff，桌面端想同时管理多个任务，业务系统还想把审批放进自己的界面。这些客户端不该各写一遍 Agent Loop。

所以更准确的分层是：

```text
模型层：推理、生成消息或 Tool Call
Agent Loop：执行工具，把结果送回模型
Harness：上下文、状态、权限、持久化、扩展、事件与恢复
产品层：CLI、IDE、桌面端、业务工作台
```

Loop 是 Harness 的心跳，但不是整副身体。

## Codex Core：一个 Thread 的运行时

OpenAI 把 Codex 的 Agent 逻辑放在 Rust 代码库的 `codex-core`。官方把它描述成一套库，也是一套可运行的 Thread Runtime。

这里的 Thread 不等于“聊天记录”。它是一段仍然可以继续工作的会话：有历史、有当前配置、有工具、有审批策略，也有落盘位置。

在我核对的固定提交 `343074d4` 里，`CodexThread` 包着一个 `Session`、双向 `SessionIo`、会话来源和 rollout path。源码给它的注释很直接：这是组成一个 Codex Thread 的双向消息流通道。

再往上一层是 `ThreadManager`。它负责创建 Thread，并把活跃的 `ThreadId` 映射到对应的 `CodexThread`。但它管的远不止一张内存表：共享状态里还有认证、模型目录、执行环境、Skills、Plugins、MCP、扩展注册和 Thread Store。

这套结构透露出一个重要边界：**Thread 是 Agent 的运行单位，ThreadManager 是运行时的资源总管。**

你点击“新任务”时，不只是创建一个对话 ID。Harness 需要解析配置和工作目录，装入项目指令，确定模型与权限，连接工具，准备持久化，然后才让模型看到第一条输入。

恢复也不只是把聊天文本重新塞回去。Harness 还得重建这段历史对应的运行语义：上次在哪个目录、哪些 Item 已经完成、Turn 是否被中断、后续输入应该接在哪里。

这也是为什么“我把历史消息存进数据库了”还不等于支持 Agent 恢复。消息是证据的一部分，运行状态才决定接下来能不能安全继续。

## Core 先组装运行环境，再让模型思考

很多人把 Codex 的输入理解成“用户 Prompt 加仓库代码”。实际送进第一次推理的内容更像一份现场交接包。

官方对 Agent Loop 的拆解把 Responses API 请求归成三块：`instructions`、`tools` 和 `input`。

`instructions` 决定模型要遵守的基础行为。`tools` 描述这一轮可以调用的 Shell、计划工具、托管工具和 MCP 工具。`input` 则不只有用户消息，还会放入权限说明、用户自定义指令、项目 `AGENTS.md`、Skills 元数据、当前目录和 Shell 等环境信息。

顺序很重要。

权限说明要让模型提前知道哪些目录可写、什么时候必须申请升级；项目指令要让它知道这个仓库怎么测试、哪些文件不能碰；环境信息要让它别在错误目录里运行命令。少一块，模型可能依然会写代码，却会在收尾时用错测试命令、漏掉仓库规则，或者提出当前环境根本执行不了的动作。

工具也不是一股脑塞进同一个执行器。Codex 内置的 Shell、Responses API 提供的托管工具、用户配置的 MCP 工具，来源和安全边界不同。Harness 负责把它们整理成模型能理解的工具表，再把 Tool Call 路由到对应执行路径。

一轮里如果连续调用几十次工具，上下文会持续增长。旧消息、命令输出和文件内容不能无限累积，Core 还要在接近上下文窗口时做压缩。压缩不是简单删掉前半段聊天：任务目标、已经完成的动作、关键文件、失败证据和待办状态都要尽量保留，否则“上下文变短”会直接变成“Agent 忘了自己在干什么”。

这里可以看出模型与 Harness 的分工：模型负责在当前上下文里判断下一步，Harness 负责决定它这一刻能看到什么、能调用什么，以及历史以什么形态继续存在。

## App Server：把同一套 Agent 从 TUI 里拆出来

Codex 最初是终端里的 TUI。界面和 Agent Loop 在同一个进程里，TUI 可以直接调用 Rust 类型，开发速度很快。

问题出现在 VS Code 插件。

IDE 需要的不是一问一答。它要一边显示模型输出，一边展示命令进度、文件差异和审批按钮；用户还可能在工具执行期间补充输入。如果为 VS Code 重写一套 Harness，CLI 与 IDE 很快就会出现两种行为。

App Server 就是在这个压力下长出来的。

它是一项协议，也是一段长期运行的进程。客户端启动 App Server，通过默认的 stdio 通道发送一行一条的 JSON 消息；App Server 托管 Codex Core Thread，把内部事件翻译成稳定、适合 UI 消费的 JSON-RPC 消息。

最初的官方架构图把它画成四部分：

1. **输入层**读取客户端消息；
2. **Message Processor**分发请求，转换内部事件；
3. **Thread Manager**创建和管理 Thread；
4. **Core Threads**分别运行各自的 Agent 会话。

当前源码已经比这张图复杂得多。`MessageProcessor` 下面拆出了 Thread、Turn、配置、文件系统、Git、MCP、插件、账号等多个 Request Processor。高层边界却没有变：**客户端说产品语言，Core 说运行时语言，App Server 负责翻译。**

这层翻译很值钱。

Core 可以继续重构内部事件；CLI、IDE、桌面端只要依赖稳定的协议原语，不必追着每个 Rust 枚举一起改。反过来，客户端可以把同一个 Item 渲染成终端日志、IDE diff 或桌面端时间线，而不必干涉 Agent 怎么推理。

## App Server 为什么没有直接沿用 MCP

OpenAI 最初确实试过把 Codex 暴露成 MCP Server，后来放弃了这条路。

原因不是 MCP 不好，而是两套协议在解决不同方向的问题。

MCP 更适合让 Agent 发现和调用外部能力：工具、资源、Prompt 或交互组件。它回答“这个 Agent 能接哪些系统”。App Server 则要让一个产品完整承载 Agent：创建 Thread、开始 Turn、流式展示 Item、发送 diff、处理中断、响应审批，再把历史恢复出来。它回答“产品怎样控制这个 Agent 的一生”。

两者的关系更像纵向与横向：

```text
产品客户端  ↔  App Server  ↔  Codex Core
                              ↕
                         MCP 工具与数据
```

IDE 通过 App Server 控制 Codex；Codex 再通过 MCP 连接外部工具。把 App Server 和 MCP 当成二选一，会把“嵌入 Agent”与“扩展 Agent”混成同一件事。

这种差异在审批上尤其明显。MCP Tool Call 发生在 Agent 内部；但批准按钮、风险解释和用户选择属于宿主产品。App Server 必须允许服务端反过来询问客户端，并把当前 Turn 停在正确位置。普通的“调用一个 MCP Tool，等它返回”表达不了完整的产品控制面。

## 协议稳定，不代表所有字段永远不变

App Server 的公开协议仍在快速扩展。固定提交里既有稳定方法，也有大量 experimental 字段。接入方如果直接对着源码抄 JSON，很容易在升级二进制后踩到变化。

官方提供了两条更稳的路。

第一，使用运行中的 App Server 生成 TypeScript 类型或 JSON Schema。生成物和当前二进制版本一致，避免文档版本、客户端类型和服务端实现各走各的。

第二，本地客户端固定经过验证的 Codex 二进制版本。OpenAI 的 IDE 与桌面端不是每次启动都随便拉一个最新 Core，而是让客户端与经过测试的 App Server 一起发布。协议能向前演进，版本仍然要经过配套验证。

连接初始化也承担一部分兼容工作。客户端会声明名称、版本和能力，服务端根据是否启用实验 API、是否支持扩展、是否退订某类通知来调整输出。未知能力可以被忽略，实验字段也可以被过滤。

所以“有 JSON-RPC”并不自动等于稳定。真正的稳定来自四件事：少量清楚的原语、显式能力协商、与二进制匹配的类型，以及客户端愿意处理未知与失败。

## Thread、Turn、Item：三种不同寿命的状态

App Server 没有把整个过程压成一条巨大的“响应”。它选了三个不同寿命的原语。

**Thread 是容器。**

它包含多次用户输入，可以创建、恢复、分叉和归档。一个 Thread 可以跨越多个 Turn，持久化后，客户端重连仍能重建时间线。

**Turn 是一次工作。**

用户说“跑测试并总结失败”，就启动一个 Turn。这个 Turn 里可能发生十几次模型推理、Shell 命令和文件读取。它最终处于 `completed`、`interrupted`、`failed` 或 `inProgress` 之一。

**Item 是可展示的原子事件。**

用户消息、Agent 消息、命令执行、文件修改、MCP 调用、计划和推理，都可以成为 Item。Item 有自己的 ID 和生命周期，适合被增量更新、单独渲染和持久化。

为什么要拆三层？看一个具体场景就明白了。

你让 Codex 修一个测试。任务还没结束，IDE 已经需要显示：Agent 开始分析、准备执行 `pytest`、命令正在跑、出现两个失败、修改了三个文件、生成一段 diff、等待你批准下一条命令。

如果后端只在最后返回一大段字符串，客户端既不知道现在发生到哪一步，也无法把审批按钮准确挂到那条命令上。

Item 让中间动作有身份，Turn 让一次工作有边界，Thread 让多次工作能续上。

这不是命名洁癖，而是把 Agent 从“文本生成器”变成“可操作产品”的最小状态模型。

## 一次用户输入，为什么会变成事件流

连接建立后，客户端不能立刻发任务。它要先发送 `initialize`，带上客户端名称、版本和能力；然后再发 `initialized` 通知。

这个握手不只是打招呼。当前协议允许客户端声明自己理解哪些扩展、是否启用实验 API、想屏蔽哪些通知。App Server 因此知道该发什么，也知道哪些字段必须过滤。

接下来，客户端用 `thread/start` 创建 Thread，或者用 `thread/resume` 恢复旧 Thread。用户输入则通过 `turn/start` 进入指定 Thread。

从这里开始，一次请求会展开成一串通知：

```text
turn/started
  item/started
  item/agentMessage/delta
  item/completed
  item/started          # 命令执行
  item/completed
  ...
turn/completed
```

`started` 让界面先占住位置，`delta` 让文本或进度持续更新，`completed` 给出终态数据。客户端不需要等整个 Turn 结束，才能知道 Agent 正在做什么。

这里还有一个常被忽略的工程问题：**事件流也会堵车。**

固定提交的 App Server 在输入、请求处理和输出之间使用有界队列。入口过载时，服务端会返回可重试错误；慢客户端把输出队列塞满后，连接可能被断开。

这类代码不会出现在“十分钟搭 Agent”教程里，却直接决定产品能否扛住多个长任务。流式不只是打字机动画，它是一条需要背压、重试和断线策略的数据通道。

## 为什么协议必须双向：Agent 会停下来等你

很多流式 API 只有一个方向：客户端发请求，服务端不断推 token。

Coding Agent 不够用。

模型准备运行一条高风险命令时，Harness 可能需要向客户端发起审批。文件修改、命令执行、MCP 工具补充输入，都可能由服务端主动提出请求。协议里对应的名字很直白：

```text
item/commandExecution/requestApproval
item/fileChange/requestApproval
item/tool/requestUserInput
```

客户端收到请求后，可以弹出对话框、展示命令和原因，再把允许或拒绝返回给 App Server。回复到达之前，相关动作会停住。

而且审批不只是“允许 / 拒绝”两个按钮。固定提交里的命令审批还区分：仅允许这一次、在当前 Session 内允许同类动作、接受一条执行策略修订、拒绝但让 Turn 继续，以及拒绝并立刻中断 Turn。

这些选项对应的产品后果不同。

一次性允许最保守，但重复命令会不断打断用户；Session 级允许降低摩擦，却不能悄悄扩大到以后所有任务；策略修订适合把明确规则沉淀下来；“拒绝后继续”和“拒绝并取消”则决定 Agent 是换一条路，还是立即交还控制权。

如果客户端把它们全部压成一个布尔值，Harness 虽然支持细粒度决策，用户最后看到的仍是粗糙的安全体验。

这条链路把三个角色分开了：

- 模型提出“我想做什么”；
- Harness 判断“是否触发策略”；
- 客户端决定“怎样向用户呈现并收回选择”。

我的判断是，双向协议是 App Server 与普通 SDK 封装最重要的分水岭。它不是把 Codex API 换成 JSON-RPC，而是把“Agent 需要人类参与”的时刻做成了一等公民。

同时要守住安全边界。

Codex 的 sandbox policy 和 approval policy 可以随 Thread 或 Turn 配置，Harness 也能把审批稳定地送到客户端。但这不等于所有工具自动进入同一个操作系统沙箱。

OpenAI 的 Agent Loop 文章明确说明：Codex 提供的 Shell 受它自己的沙箱约束，MCP 工具并不会因此自动被套住，必须执行各自的 guardrail。一个能调用生产数据库的 MCP Server，不能因为前面挂了 App Server 就被当成安全。

Harness 统一的是控制流和策略接口。真正的隔离，仍然要落到每种工具、凭证和运行环境上。

再往前一步，Thread 与 Turn 的权限也不是完全固定。当前协议允许在创建 Thread 时设置工作目录、模型、sandbox 和 approval policy，也允许 `turn/start` 对后续工作覆盖一部分设置。

这带来灵活性，也带来审计要求：同一 Thread 前后两次 Turn 可能处于不同权限配置。客户端不能只在任务开头显示一次“已启用沙箱”，然后默认后面永远不变。权限变化本身应该进入可观察状态，审批还要绑定当时真实生效的策略。

## App Server 不是所有场景的答案

App Server 给了产品团队最大的生命周期控制，也要求接入方承担更多工作：启动和管理长期进程、维护连接、重建事件、处理审批、应对版本和背压。

官方现在给出的选择很清楚。

**脚本、CI、一次性后台任务**，用 `codex exec`。任务有明确入口和终点，拿结构化输出就够了，不必维护长期会话。

**应用代码需要启动、恢复或流式读取任务**，优先看 Codex SDK。SDK 把常见的程序化工作流包得更直接。

**Agent 本身就是产品体验的一部分**，再用 App Server。比如 IDE、SRE 控制台、安全调查台，需要持久 Thread、中间事件、用户中断和审批 UI，这些才是 App Server 的主场。

宿主应用也不能把责任全部交给 Harness。OpenAI 的示例把边界画得很实在：应用拥有业务界面、业务上下文、MCP 数据与动作、关键操作的同意流程；Codex 提供 Agent Loop、会话状态、流式活动和工具交互。

复用 Harness，不等于把产品判断外包。

## 自建 Coding Agent，先过这八道检查

如果你正在搭自己的 Harness，不要只看“模型能不能调用 Shell”。先拿这份清单过一遍。

**1. Thread 能恢复、分叉和归档吗？**

只有一份 messages 数组，不足以恢复目录、配置、中断点和工具状态。

**2. Turn 有明确终态吗？**

完成、中断、失败和仍在运行必须分开。否则客户端无法判断该重试、续跑还是交还用户。

**3. Item 有生命周期吗？**

命令、diff、审批和 Agent 消息需要独立 ID，以及 started、delta、completed 之类的边界。

**4. 工具动作能被观察吗？**

至少要知道调用了什么、输入来自哪里、结果是什么、失败发生在哪一步。

**5. 高风险动作能暂停吗？**

“运行前打印一句日志”不算审批。系统必须真的停住，等待外部决定，并把决定绑定到正确的动作。

**6. 权限是不是分层治理？**

Shell 沙箱、网络访问、MCP 凭证、文件修改和业务写操作不是同一件事。

**7. 协议能演进吗？**

初始化、能力协商、版本、实验字段、背压和重试，至少要有明确策略。

**8. 断线和重启后怎么办？**

客户端慢消费、进程退出、机器重启，都不该让系统凭空猜测任务是否完成。

八项里缺一两项，Demo 依然能跑。缺得多了，长任务越成功，积累的不可控状态反而越多。

## 最后的判断

模型能力还会继续涨，Agent Loop 也会越来越短。但 Thread、工具、权限、审批、事件和恢复不会自动消失。

Codex Harness 值得研究，不是因为它给出了一套必须照抄的唯一架构，而是它把 Coding Agent 最容易被低估的工程层公开了出来：Codex Core 负责让一个 Thread 活着，App Server 负责让不同客户端看懂、控制并继续这段工作。

下次评估一个 Coding Agent，别只问它接了什么模型、榜单多少分。把上面的八项检查表拿出来，看它在任务跑到第 30 分钟、等待审批、客户端断线之后，还剩多少工程确定性。

如果你正在自建 Agent Runtime，建议把这篇先收藏。后面我会继续拆 App Server 的协议接入：从 `initialize` 开始，跑通一个最小客户端，再实测 Thread 恢复、事件流和审批回路。

---

## 官方资料

- [Codex as a platform: build on the open agent harness](https://learn.chatgpt.com/blog/codex-as-a-platform)
- [Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/)
- [Codex App Server documentation](https://developers.openai.com/codex/app-server)
- [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/)
- [openai/codex source repository](https://github.com/openai/codex)

---
title: "Codex 支持远程操作：手机接管开发环境"
author: "蒸馏小余"
created_at: "2026-05-15"
coverImage: "imgs/article-cover.png"
summary: "OpenAI 把 Codex 带进 ChatGPT 手机 App。重点不是手机写代码，而是用手机接管本地或远程环境里的长任务。"
source: "https://openai.com/index/work-with-codex-from-anywhere/"
source_author: "OpenAI"
written_style: "蒸馏小余"
---

# Codex 支持远程操作：手机接管开发环境

OpenAI 这次给 Codex 加的不是一个“手机写代码”功能，而是一个更接近真实工程节奏的能力：人可以离开电脑，但 Codex 继续在你的电脑、Mac mini、devbox 或远程环境里跑。

官方在 2026 年 5 月 14 日发布了「Work with Codex from anywhere」。X 上 OpenAI 和 OpenAI Developers 的说法也一致：你可以在 ChatGPT 手机 App 里开始新任务、看输出、改方向、批准下一步；Codex 仍然运行在宿主机上，文件和项目上下文也留在宿主机。

这对开发者的意义很直接。过去 AI 编程工具最容易卡在一个小节点：它问你要不要跑命令、怎么选方案、是否继续改。你不在电脑前，这个线程就停住。现在手机端变成了一个远程驾驶舱，长任务不必等你回到桌前才继续。

![Codex 远程操作工作流](imgs/codex-remote-flow.png)

## 这次更新到底是什么

按官方文档，Codex 的远程连接有两层。

第一层是手机接管 Codex App 宿主机。你在 Mac 上跑着 Codex App，手机上的 ChatGPT 可以连接这个宿主机，看到线程、项目、审批、插件、浏览器、Computer Use、本地工具和输出状态。

第二层是远程机器。官方说 Remote SSH 已经 generally available，Codex App 可以从 SSH 配置里发现主机，并在远程文件系统和 shell 上创建项目、运行线程。也就是说，项目可以在 devbox 里，Codex 的命令也可以跑在远程主机上。

把这两层合起来看，新的工作流是：

1. 电脑或远程环境负责执行。
2. 手机负责查看、批准、补充上下文和改方向。
3. Codex 负责把长任务继续往前推。

这不是把 IDE 搬到手机上。手机屏幕不适合写复杂代码，也不适合看大 diff。它适合做三件事：判断、批准、补充信息。恰好这三件事正是长时间 agent 工作最容易被人类阻塞的地方。

## 文件和凭证没有跑到手机上

这一点值得单独拆出来，因为它决定了这项功能能不能进团队流程。

OpenAI 官方写得很清楚：文件、凭证、权限和本地配置仍然留在运行 Codex 的机器上。手机端收到的是实时更新，包括截图、终端输出、diff、测试结果和审批请求。

这意味着手机不是新的开发环境。它更像一个远程控制面板，接入的是已经被你信任、已经配置好的宿主环境。

官方还提到，Codex 使用 secure relay layer，让被信任的机器可以跨设备访问，但不直接暴露到公网。开发者文档里对 SSH 也给了安全边界：使用可信密钥、最小权限账号，不要把未认证的 app server listener 暴露在共享网络或公网；如果需要跨网络访问，优先用 VPN 或 Tailscale 这类 mesh networking。

这也是我认为它比“浏览器里开一个远程桌面”更适合 agent 的原因。远程桌面解决的是屏幕控制，Codex 远程操作解决的是线程状态、审批、命令输出、diff 和上下文协作。

## 真正变化的是 agent 的节奏

AI 编程工具已经不只是“补全一段代码”。Codex 现在处理的是更长的线程：查 bug、跑测试、重构、开分支、读文档、改配置、生成 PR 说明。

这类任务不怕跑得久，怕中途没人拍板。

举个常见场景：你早上让 Codex 重构一块鉴权逻辑，出门后它发现两种方案。过去线程会停在“请选择 A 还是 B”。现在你在手机上看它列出的权衡，选一个方向，任务继续跑。等你回到电脑前，它可能已经给出 diff 和测试结果。

OpenAI 在官方博文里也用了类似场景：排队买咖啡时开始调查 bug，通勤途中决定重构方向，会议前让 Codex 汇总最新材料。这里的核心不是“随时随地工作”，而是把开发流程里的等待时间变成可用的决策窗口。

## 适合谁，不适合谁

适合三类人。

第一类是经常跑长任务的开发者。比如迁移、测试修复、批量重构、代码审查、文档整理。这些任务不需要你一直盯着屏幕，但需要你在关键节点给判断。

第二类是有固定远程开发环境的团队。很多公司已经把依赖、凭证、安全策略和算力放在 managed devbox 里。Remote SSH generally available 以后，Codex 可以直接在这些环境里跑，手机只是接管线程。

第三类是需要把 agent 放进工作流的团队。官方同时提到 Hooks、Programmatic access tokens 和 HIPAA-compliant use 的更新。它们不是同一个功能，但方向一致：Codex 正在从一个交互式编码助手，变成能被治理、自动化和远程调度的工程系统。

不适合的人也很明确。

如果你的任务需要长时间肉眼读大段 diff，手机不合适。如果你的团队没有整理好 SSH 权限、凭证边界和命令审批策略，也不建议一上来就把重要仓库接进去。如果你使用的是 Windows 作为被手机连接的 Codex App 宿主机，官方目前写的是支持即将到来，不是已经可用。

## 我会怎么用

我不会把它当“手机上的 Cursor”。

更合理的用法，是把 Codex 远程操作放进四个固定场景：

| 场景 | 让 Codex 做什么 | 人在手机上做什么 |
|---|---|---|
| 通勤前 | 开始 bug 复现、读日志、跑测试 | 看结果，补充线索，批准下一步 |
| 会议间隙 | 整理 issue、PR、文档和客户上下文 | 改摘要重点，决定是否继续 |
| 长重构 | 分析方案、生成 diff、补测试 | 选择方案，批准命令，检查风险 |
| 远程 devbox | 在远程 shell 里读写项目文件 | 控制线程，不搬走凭证和代码 |

我的默认清单会更保守：

1. 只把可信项目接入 Codex。
2. SSH host 用最小权限账号。
3. 重要命令保留审批。
4. 长任务先从测试、文档、重构这类低风险场景开始。
5. 团队 workspace 先确认 Remote Control、RBAC 和审计日志。

这样用，远程操作的价值才会落到工程效率上，而不是变成“手机上也能焦虑工作”。

## 最大的坑：别把远程控制当远程安全

远程控制降低的是协作阻塞，不自动等于安全配置完成。

官方文档已经把边界写出来了：远程访问使用宿主机的项目、线程、文件、凭证、权限、插件、浏览器配置和本地工具。换句话说，你原来宿主机上能碰到什么，远程接入后 Codex 仍然能碰到什么。

这对个人开发者是便利，对企业团队就是治理问题。谁能连宿主机、谁能批准命令、哪些仓库允许远程跑、SSH 主机怎么管、日志怎么留，这些都要在启用前想清楚。

我的判断是：这次更新的产品价值很大，但最好先把它放在“远程协作和长任务续跑”的框架下理解。不要把它包装成万能移动 IDE，也不要把手机端权限开得比桌面端更松。

## 结论

Codex 支持远程操作，真正改变的是 AI 编程 agent 的工作半径。

以前 agent 只能在你盯着电脑时顺畅推进。现在它可以在宿主机或远程环境里继续工作，你在手机上做必要的判断、审批和纠偏。

对开发者来说，这会把很多“等我回电脑再说”的断点变成实时协作。对团队来说，它也会把 Codex 推向更严肃的工程基础设施：远程环境、权限、审计、自动化和安全边界都要一起设计。

如果你要试，先从一个低风险仓库开始：让 Codex 跑测试、修文档、整理 issue 或做小范围重构。等你确认权限、审批和远程主机配置都稳定，再把它放进更重的开发流程。

回复「Codex 远程」我把这篇的远程使用清单和官方资料链接整理成一页，方便团队内部评估。

## 资料来源

- OpenAI 官方发布：《Work with Codex from anywhere》：https://openai.com/index/work-with-codex-from-anywhere/
- OpenAI Developers 文档：《Remote connections》：https://developers.openai.com/codex/remote-connections
- OpenAI Developers 文档：《Codex changelog》：https://developers.openai.com/codex/changelog
- OpenAI Help Center：《Using Codex with your ChatGPT plan》：https://help.openai.com/en/articles/11369540
- OpenAI 在 X 上的发布：借助 ChatGPT 手机 App 开始新任务、查看输出、批准下一步，Codex 继续运行在 laptop、Mac mini 或 devbox：https://x.com/openai/status/2055016850849993072
- OpenAI Developers 在 X 上的发布：手机端访问，文件和项目上下文仍在电脑上：https://x.com/openaidevs/status/2055016926213181608
- OpenAI 在 X 上的补充：iOS 和 Android 预览版开始推出，Windows 宿主机连接支持即将到来：https://x.com/openai/status/2055016852133417389
- Greg Brockman 在 X 上的评论：可以从 ChatGPT App 使用正在运行的 Codex：https://x.com/gdb/status/2055034165968384099


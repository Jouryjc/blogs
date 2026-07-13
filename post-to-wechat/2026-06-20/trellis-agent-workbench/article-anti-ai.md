---
title: "别再反复教 AI 项目规则了：Trellis 把规范和任务写回仓库"
source: "https://github.com/mindfold-ai/Trellis"
source_author: "Mindfold AI"
author: "蒸馏小余"
written_style: "蒸馏小余 2.0"
created_at: "2026-06-20"
coverImage: "imgs/article-cover.png"
summary: "如果 Codex、Claude Code、Cursor 每次都像新同事，Trellis 的价值不是多一个 Agent，而是把 specs、tasks、journal 写回仓库，让下一轮少问废话、少犯旧错。"
---

# 别再反复教 AI 项目规则了：Trellis 把规范和任务写回仓库

你大概率遇到过这种场景。

周一刚告诉 Codex：这个仓库不能碰生产配置，UI 改动要截图，测试先跑 `pnpm test`。它当场答应，改得也还行。周三你开一个新会话，它又像刚入职的同事，重新问项目结构；或者更糟，它不问，直接按通用习惯改代码。

这不是 AI 不会写代码，而是项目记忆没落地。

Trellis 做的事很朴素：把 Agent 需要反复知道的规范、任务和工作日志写回仓库。不是再给你一个聊天窗口，而是给 Codex、Claude Code、Cursor、OpenCode 这类工具一张可以继承的工作台。

![Trellis：给 Coding Agent 一张不会丢的工作台](imgs/article-cover.png)

我对 Trellis 的判断也很简单：如果你只是让 AI 改一次脚本，别上它；如果你已经开始抱怨“每次都要重新教 AI 一遍项目”，它值得试一次。

## 先别换模型，先看记忆放哪了

很多团队现在的 AI 编程上下文，散在三个地方：

- 人的脑子里；
- 上一次聊天记录里；
- 越写越长的 `AGENTS.md`、`CLAUDE.md`、`.cursorrules` 里。

这些文件有用，但很容易变成大杂烩：安装命令、代码风格、业务背景、临时提醒、个人偏好，全塞在一个入口里。Agent 读起来费劲，人 review 起来也费劲。

Trellis 在这些入口之上补了一层结构。它把 AI 编程拆成三类仓库资产：

| 资产 | 放在哪里 | 解决什么问题 |
|---|---|---|
| Specs | `.trellis/spec/` | 稳定规范和项目约定 |
| Tasks | `.trellis/tasks/` | 单个需求的 PRD、实现上下文、检查记录 |
| Workspace journal | `.trellis/workspace/` | 上一次做了什么、学到了什么、下一轮从哪里接 |

![旧方式为什么失忆：规范、任务、复盘散落在对话里](imgs/01-agent-amnesia.png)

这三个目录的好处，是把“我在对话里说过”变成“仓库里有记录”。聊天记录很难 review，也很难跨工具复用；仓库文件可以进版本管理，可以被团队讨论，也可以被不同 Agent 读到。

## Trellis 不是让 Agent 更自由，而是让它先停下来

Trellis 官方 README 里的流程，大致是四段：

1. 用自然语言描述需求。
2. AI 先和你头脑风暴，一次问一个问题，直到 PRD 足够清楚。
3. AI 再进入实现阶段，并按 spec、lint、type-check、tests 做检查。
4. 工作结束后运行 finish workflow，归档任务并更新 journal。

这里我最喜欢的不是“多代理”，也不是“支持多少平台”，而是第一步：先澄清，再动手。

过去很多 AI 编程翻车，都发生在这句话之后：

```text
帮我优化一下登录页。
```

人还没说清楚“优化”是转化率、性能、视觉层级，还是移动端布局，Agent 已经开始改文件。最后你盯着 diff 救火。

Trellis 的 Plan 阶段会让 `trellis-brainstorm` 先追问需求，并写出 `prd.md`。如果任务需要资料调研，可以交给 `trellis-research`。开始实现前，Trellis 会把需要的 specs 和研究材料编进 `implement.jsonl` / `check.jsonl`。

后面才是实现和检查：

- `trellis-implement` 按 PRD 写代码；
- `trellis-check` 对照 diff 和 specs 检查，并运行 lint、type-check、tests；
- `trellis-update-spec` 把本轮新学到的规则沉淀回 `.trellis/spec/`。

![Trellis 四阶段循环：Plan、Implement、Verify、Finish](imgs/02-trellis-loop.png)

有个边界要说清楚：官方 How It Works 里，`/trellis:finish-work` 是提交之后的归档和 journal 记账，不是替你提交功能代码的命令。不同平台入口也不完全一样，有的平台是 slash command，有的平台通过 Trellis skill 或 workflow 触发。

## 第一次别上生产主分支，先跑一个小任务

Trellis 的前置要求不复杂：

- Node.js >= 18
- Python >= 3.9

安装：

```bash
npm install -g @mindfoldhq/trellis@latest
```

进入项目根目录后初始化：

```bash
trellis init -u your-name
```

如果只想生成某些平台的适配文件，可以显式指定平台。README 里给了这个例子：

```bash
trellis init --cursor --opencode --codex -u your-name
```

初始化后先看 `.trellis/`：

```text
.trellis/
├── spec/        # 项目规范和稳定约定
├── tasks/       # 每个任务的 PRD、实现上下文、检查上下文
└── workspace/   # 工作日志和项目记忆
```

我不建议第一次就把它接到大需求上。更稳的做法是：新开实验分支，让它先读项目、生成 specs，然后人工 review。

可以直接这样说：

```text
请先分析这个项目的结构，帮我用 Trellis 建立第一版项目规范。
重点看：技术栈、测试命令、代码风格、危险目录、常见改动流程。
生成后先让我 review，不要直接开始实现需求。
```

这份初稿要认真看。AI 生成的 specs 不应该未经检查就变成团队规范。你要删掉过度推断的规则，补上团队关心的约束：

- 数据库 migration 怎么写；
- 哪些目录不允许自动改；
- 测试必须跑到什么层级；
- UI 改动是否需要截图；
- 生产配置和密钥文件永远不能碰。

## 我会这样接入 Trellis

如果让我把 Trellis 接进一个真实仓库，我会按这个清单来，不会一上来追求全自动。

| 步骤 | 我会做什么 | 不会做什么 |
|---|---|---|
| 1 | 新开实验分支，让 Trellis 读项目 | 直接让它改业务代码 |
| 2 | 人工 review `.trellis/spec/` | 把 AI 猜的规则照单全收 |
| 3 | 选一个低风险任务跑完整流程 | 拿关键模块做第一次实验 |
| 4 | 对照 PRD、检查记录、journal 复盘 | 只看代码能不能跑 |
| 5 | 再决定是否团队共享 specs | 一上来要求所有人切换流程 |

第一轮任务可以很小，比如：

```text
我想给登录页增加“记住我”选项。
请按 Trellis 流程先澄清需求，写 PRD，等我确认后再实现。
实现后运行相关测试，并说明改了哪些文件、怎么验证。
```

如果流程正常，你应该能看到 Trellis 把需求沉淀成任务文件，而不是只在对话里推进。等工作完成、检查通过，并且按团队流程完成提交之后，再运行收尾入口：

```text
/trellis:finish-work
```

如果你所在的平台没有原生 slash command，就按 Trellis 为该平台生成的 finish workflow 或 skill 入口走。

收尾会归档任务、更新工作日志、把有价值的新规则写回 spec。下一次新会话进来，Agent 至少有地方恢复脉络。

![Trellis 第一次使用：安装、初始化、建规范、跑小任务、收尾](imgs/03-first-run.png)

## 哪些团队值得试，哪些先别上

Trellis 最适合三类人。

第一类，是已经在多个 AI 编程工具之间切换的人。你可能在 Codex 里跑长任务，在 Cursor 里做日常编辑，在 Claude Code 里重构，在 OpenCode 里试命令行流程。工具一多，项目规则很容易散。Trellis 的价值是让规则留在仓库里，而不是绑在某个工具里。

第二类，是团队里已经出现“AI 写代码风格不一致”的人。一个人把测试规则写在 `CLAUDE.md`，另一个人写在 Cursor rules，第三个人只靠 Prompt 记忆。短期能跑，长期会乱。Trellis 把 specs、tasks、journal 分开，让团队可以像 review 代码一样 review AI 工作流。

第三类，是经常做长任务的人。长任务最怕上下文快满。Trellis 的 finish workflow 不只是结束当前任务，也是在把工作状态收进仓库。下一轮继续时，Agent 可以从 journal 和 task 里恢复。

但它不适合所有场景。

如果你只是让 AI 改一个一次性脚本，或者仓库很小、没有协作、没有稳定规范，直接写一条清楚的 Prompt 可能更快。Trellis 会引入额外文件和流程，只有当“重复解释项目背景”已经成为成本时，这套结构才划算。

还有一个许可证边界要提前知道：Trellis 是 AGPL-3.0。个人学习、开源项目通常问题不大；公司内部改造、二次分发、商业集成，要让团队自己确认合规边界。

## 下次 Agent 又失忆，先查三件事

我会把 Trellis 当成一种项目记忆实验，而不是银弹。

下次 Agent 又犯同一个错时，先别急着换模型，先查三件事：

1. 这个错误有没有被记录成规则？
2. 这条规则有没有进入仓库，而不是只留在聊天记录里？
3. 下一轮 Agent 开始工作前，能不能读到这条规则？

如果三个答案都是否定的，问题就不只是模型不聪明，而是项目没有给 Agent 留下一条能继承的路。

Trellis 的意义就在这里：它不是让 Agent 更像人，而是让项目开始拥有 AI 时代的工程记忆。

如果你准备试，别从大改造开始。收藏这份清单，先挑一个低风险任务，把 specs、tasks、journal 跑通。跑完再看下一次新会话，Agent 是否少问了废话，少犯了旧错。

能做到这一点，它就不只是又一个工具。

它是你把 AI 编程从“靠聊天续命”，往“靠工程资产协作”挪了一步。

---

参考资料：

- Trellis GitHub：<https://github.com/mindfold-ai/Trellis>
- Trellis 中文 README：<https://github.com/mindfold-ai/Trellis/blob/main/README_CN.md>
- Trellis 官方文档：<https://docs.trytrellis.app/zh>
- Trellis 快速开始：<https://docs.trytrellis.app/zh/start/install-and-first-task>
- Trellis 支持平台：<https://docs.trytrellis.app/zh/advanced/multi-platform>
- npm：<https://www.npmjs.com/package/@mindfoldhq/trellis>

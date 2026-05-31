---
title: "别再只给 AI 写提示词：Agent Skills 把工程流程变成可执行规则"
source: "https://github.com/addyosmani/agent-skills"
source_author: "Addy Osmani / agent-skills contributors"
written_style: "蒸馏小余"
created_at: "2026-04-27"
coverImage: "imgs/agent-skills-engineering-workflow-cover.png"
summary: "如果你发现 AI 编程助手总是跳过测试、猜命令、乱改边界，问题往往不在 prompt 不够长，而在缺少可执行的工程流程。Agent Skills 的价值，是把规格、计划、实现、验证和发布写成 Agent 能稳定遵守的工作契约。"
tags:
  - type/article
  - topic/agent-skills
  - platform/wechat
moc:
  - "[[agent-skills]]"
related:
  - "[[agent-skills-engineering-workflow.optimized]]"
  - "[[agent-skills-deep-dive]]"
---

# 别再只给 AI 写提示词：Agent Skills 把工程流程变成可执行规则

很多人用 Claude Code、Codex 或 Cursor，一开始都会做同一件事：给 AI 写一段更长、更细、更严厉的提示词。

这件事当然有用，但只靠它很快会遇到上限。你会发现，AI 并不是不知道“要写高质量代码”，也不是不知道“测试很重要”，真正的问题在于它经常没有把这些原则稳定地执行完：需求还没问清楚就开始改代码，测试还没跑就汇报完成，遇到报错先猜一个方向，改动范围一大就顺手碰到本来不该动的边界。

所以我现在越来越觉得，AI 编程的下一阶段，不是把 prompt 写成一份更长的入职手册，而是把工程流程拆成 Agent 能触发、能执行、能自查、能留下证据的工作规则。

`addyosmani/agent-skills` 这个项目值得看的地方就在这里。

它不是一个“神奇提示词合集”，而是把资深工程师每天都在做的规格定义、任务拆解、小步实现、测试验证、代码评审和发布准备，整理成一组可以被 AI Agent 读取的 Markdown 技能。

如果只用一句话概括：

**Agent Skills 解决的不是“让 AI 更听话”，而是“让 AI 按工程流程交付”。**

截至 2026 年 4 月 27 日我查看时，GitHub API 显示这个仓库约 24.4k stars、3.0k forks，许可证是 MIT，最新 release 是 2026 年 4 月 10 日发布的 `0.5.0`。

## 真正的问题，不是提示词不够长

普通 prompt 更像建议。

你可以告诉 Agent：

```text
请写高质量代码，注意安全，记得测试。
```

这句话没有错，但在真实项目里，它很容易变成一句口号。模型知道这些词重要，却不一定会在正确的时机停下来做正确的动作；它可能会在实现前不澄清边界，在实现后不跑验证，在测试失败时绕开问题，在汇报时只给一个看起来很完整的总结。

Skill 的思路不一样。

一个 `SKILL.md` 不只是告诉 Agent “你应该重视什么”，而是进一步写清楚：什么时候要触发这个流程，应该按什么顺序推进，哪些偷懒理由不能成立，完成时必须拿出哪些验证证据。

这点很关键。

AI Agent 的很多失败，并不是“不会写代码”，而是“不会坚持工程纪律”。比如你让它做一个用户数据导出功能，如果没有流程约束，它很可能直接找接口、补 UI、拼导出逻辑，看起来推进很快，但权限边界、分页策略、数据量限制、审计日志、错误恢复和测试覆盖都可能被自然跳过。

如果按 Agent Skills 的方式处理，同一个需求会先变成一条更像工程任务的链路：

```text
先写规格 -> 拆小任务 -> 小步实现 -> 补测试 -> 跑验证 -> 做 review -> 准备发布
```

慢的是开头几分钟，省下来的是后面几个小时的返工。

小余判断：prompt 解决的是“你希望 AI 怎么做”，Skill 解决的是“AI 到底会不会按流程把事情做完”。这两者不是同一层能力。

![提示词 vs Agent Skill：从建议变成流程](illustrations/agent-skills-engineering-workflow/01-prompt-vs-skill.png)

## 这个项目的核心，是把开发流程拆成可触发动作

`agent-skills` 的结构很直接，它把软件开发拆成 6 个阶段：

```text
DEFINE -> PLAN -> BUILD -> VERIFY -> REVIEW -> SHIP
```

对应到 Claude Code 里，就是 7 个 slash commands：

| 命令 | 作用 | 核心原则 |
|---|---|---|
| `/spec` | 定义要做什么 | 先规格，后代码 |
| `/plan` | 拆成可执行任务 | 任务要小、可验收 |
| `/build` | 小步实现 | 一次只做一个切片 |
| `/test` | 用测试证明 | 测试是证据 |
| `/review` | 合并前评审 | 先过质量门 |
| `/code-simplify` | 简化代码 | 清晰优于聪明 |
| `/ship` | 准备发布 | 发布要可回滚 |

底层还有 20 个工程技能，覆盖从需求到发布的完整周期。

比如，`spec-driven-development` 负责先写清楚需求、边界和验收标准；`planning-and-task-breakdown` 负责把大任务拆成可检查的小任务；`incremental-implementation` 要求每个改动都保持可构建、可测试、可回滚；`debugging-and-error-recovery` 强调先复现、再定位、再修复；`code-review-and-quality` 则要求从正确性、可读性、架构、安全和性能多个角度做自查。

这套设计最克制的地方，是它没有把所有流程塞进一个巨大 prompt。

`SKILL.md` 只是入口，真正细的检查表放在 `references/` 里，需要时再加载。也就是说，Agent 不需要一开始背下整本工程手册，而是在遇到具体任务时，加载当前真正相关的那一页。

这就是所谓的渐进式上下文。

小余判断：好的 Agent 工作流不是“给它更多上下文”，而是“在正确时机给它正确上下文”。上下文越多不一定越聪明，关键是它是否能改变当前这一步的行为。

![Agent Skills 的工程生命周期](illustrations/agent-skills-engineering-workflow/02-lifecycle.png)

## 最值得借鉴的，是它专门反“偷懒”

我看这个项目时，最喜欢的不是它列了多少技能，而是很多技能里都会写一类东西：`Common Rationalizations`。

翻译成人话，就是 Agent 常见的偷懒理由。

比如：

- “这个改动很小，不用写测试。”
- “我先实现，后面再补验证。”
- “看起来没问题，可以结束。”
- “我已经读了 README，不需要查官方文档。”

这些话是不是很熟？

人类工程师也会这么想。区别在于，人类工程师通常会被 code review、CI、团队规范和线上事故经验拉回来；Agent 如果没有明确门禁，就很容易把这些理由当成合理路径，因为对模型来说，最短路径经常就是最有吸引力的路径。

所以 Agent Skills 把很多“不能跳过的步骤”写得很硬。

`test-driven-development` 要求先写失败测试，再写实现；`debugging-and-error-recovery` 要求先复现问题、缩小范围，再改代码；`code-review-and-quality` 要求从多个维度检查代码，而不是只看能不能跑；`shipping-and-launch` 则要求发布前考虑回滚、监控和风险提示。

这些规则本身不新，老工程师都知道。

真正新的地方在于，它把这些工程纪律写成了 Agent 能稳定读取的流程，而不是停留在“你要注意质量”这种人类友好的提醒里。

小余判断：Agent 真正需要的不是鼓励，而是门禁。没有门禁，它会自动走最短路径；门禁写清楚以后，它才更像一个可以被纳入工程体系的执行者。

## 真要用，先从最痛的 3 个环节开始

我不建议一上来就把 20 个技能全塞给 Agent。

上下文窗口不是无限资源，流程太多也会稀释当前任务重点。更务实的做法，是先从你项目里最容易翻车的环节开始，让 Skill 去补那个缺口。

如果你只是想试水，我建议从这 3 个技能开始：

| 你的问题 | 先用哪个 Skill | 它解决什么 |
|---|---|---|
| 需求经常跑偏 | `spec-driven-development` | 先把目标、边界、验收标准说清楚 |
| 改完没人敢信 | `test-driven-development` | 用测试证明行为变化 |
| 完成后质量不稳 | `code-review-and-quality` | 让 Agent 先做结构化自查 |

如果你的任务经常涉及多文件改动，再加一个 `incremental-implementation`。它的价值不是让 Agent 写得更快，而是强制它把大改动拆成小切片，每个切片都保持可构建、可测试、可回滚。

在 Claude Code 里，可以直接通过插件市场安装：

```text
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

如果你用 Cursor，可以把常用的 `SKILL.md` 复制到 `.cursor/rules/`；如果你用 Gemini CLI，也可以通过 skills 安装命令把 `skills/` 目录装进去。其他 Agent 工具同样可以复用这套思路，因为这些技能的本质就是 Markdown 文件。

通用做法也很简单：

```bash
git clone https://github.com/addyosmani/agent-skills.git
```

然后把你真正需要的 `skills/<name>/SKILL.md`，放进对应工具的规则系统里。

小余判断：不要一开始追求完整体系。先解决一个最痛的环节，再根据真实使用中的失败案例往里补规则，这比一次性装满 20 个技能更可靠。

## 它应该和 AGENTS.md / CLAUDE.md 配合用

很多团队已经在项目里写了 `AGENTS.md`、`CLAUDE.md`、`.cursorrules` 或 Copilot instructions。

Agent Skills 不是替代这些文件，而是补上它们最容易失效的一层：任务流程。

项目级规则通常回答的是：

- 这个仓库用什么技术栈
- 测试命令是什么
- 哪些目录不能动
- 提交信息怎么写
- 完成前必须跑哪些验证

Skill 回答的是另一个问题：

- 需求不清时怎么澄清
- 多文件改动怎么切片
- 修 bug 时怎么先复现
- review 时从哪些维度检查
- 发布前要拿出哪些证据

一个是“本项目的规矩”，一个是“做这类事的步骤”。

它们应该叠在一起用。

比如你的 `AGENTS.md` 可以写：

```md
本项目使用 pnpm。
测试命令是 pnpm test。
不要修改 generated/ 目录。
```

而 `test-driven-development` 技能会要求 Agent：

```md
先写一个会失败的测试。
确认测试真的失败。
写最小实现让测试通过。
重构后再次运行测试。
```

前者告诉 Agent “在这个仓库怎么做”，后者告诉 Agent “这类任务应该按什么顺序做”。如果只写前者，Agent 可能知道命令却不知道什么时候必须跑；如果只写后者，Agent 可能知道流程却猜错项目里的真实命令。

![AGENTS.md / CLAUDE.md 与 Skill.md 如何配合](illustrations/agent-skills-engineering-workflow/03-agents-plus-skill.png)

## 可以直接拿走的落地清单

如果你想把这套思路放到自己的项目里，我建议不要从“整理一套完整 Skill 体系”开始，而是先做一个很小的工作流改造。

这张清单可以直接用：

```text
1. 选一个最常翻车的任务类型：需求、bug、测试、review 或发布。
2. 给它找一个对应 Skill，不要一次装太多。
3. 在 AGENTS.md / CLAUDE.md 里写清楚本项目命令和边界。
4. 跑一个真实小任务，观察 Agent 有没有按 Skill 留下验证证据。
5. 如果它重复犯错，把纠正沉淀成一条短规则。
6. 每隔一段时间删掉不会改变行为的规则，避免长期文件变成噪音。
```

我会优先把它用在三类任务上。

第一类是需求不清的功能开发，因为这类任务如果一开始没写清楚验收标准，后面越写越像猜谜。第二类是 bug 修复，因为 Agent 很容易在没有稳定复现的情况下直接改代码。第三类是多文件重构，因为这种任务最容易在“顺手修一下”的过程中扩大边界。

相反，如果只是改一个错别字、补一个明显的文案、调整一个无风险配置，就没必要把完整流程拉起来。Skill 是工程门禁，不是每个小动作都要经过的审批表。

小余判断：Skill 的价值不在于让工作看起来更正规，而在于让高风险任务少走弯路。真正应该流程化的是那些一旦出错就会返工、误判或影响线上质量的环节。

## 最后：不要把 Agent 当成更快的打字员

Agent Skills 不是魔法。

它不能保证模型永远理解需求，也不能替代工程师判断。如果项目本身没有测试、没有构建命令、没有清晰边界，Skill 写得再好，Agent 仍然缺少验证依据。

但它提醒了一个很重要的方向：AI 编程助手要进入真实工程，不只是模型能力要变强，工作方式也要变得可约束、可验证、可复盘。

过去大家优化 AI 编程助手，最常见的动作是继续写更长的提示词；现在更值得做的，是把团队里那些“老工程师默认知道的流程”，压缩成 Agent 能执行的规则。

什么时候应该停下来问问题，什么时候必须写测试，什么时候必须查官方文档，什么时候不能继续猜，什么时候应该把改动拆小。

这些东西不神秘，却决定了 AI Agent 能不能真正进入生产环境。

不要把 Agent 当成一个更快的打字员。

更好的方向是：让它按你的工程流程工作。

我把这篇文章里的「3 个起步 Skill + AGENTS.md 配合方式 + 验证清单」整理成了可复制版本。

关注「蒸馏小余」，回复 `SKILL` 获取。

下一篇我会拆：怎么把一个团队的 code review 经验，写成 Agent 能稳定执行的 `code-review-and-quality` Skill。

## 参考资料

- GitHub 仓库：<https://github.com/addyosmani/agent-skills>
- Getting Started：<https://github.com/addyosmani/agent-skills/blob/main/docs/getting-started.md>
- Skill Anatomy：<https://github.com/addyosmani/agent-skills/blob/main/docs/skill-anatomy.md>
- 0.5.0 Release：<https://github.com/addyosmani/agent-skills/releases/tag/0.5.0>

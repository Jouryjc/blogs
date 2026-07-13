---
title: "Agent 为什么总学不会？把反馈写回 Skill"
source: "https://x.com/zachlloydtweets/status/2066908445425496348"
source_author: "Zach Lloyd"
written_style: "蒸馏小余 2.0 anti-ai-edit"
created_at: "2026-06-20"
coverImage: "imgs/article-cover.png"
summary: "Agent 反复犯同一个错，很多时候不是没有记忆，而是你的纠错没有变成它下次会读取的 Skill diff。"
tags:
  - type/article
  - topic/agent-skills
  - topic/agent-design
  - topic/agent-memory
  - platform/wechat
moc:
  - "[[agent-skills]]"
  - "[[agent-design]]"
  - "[[agent-memory]]"
related:
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/research-notes]]"
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/raw/source-article]]"
  - "[[agent-loop-engineering]]"
---

# Agent 为什么总学不会？把反馈写回 Skill

你应该见过这种场景。

Agent 给 issue 贴错了标签，你在评论里纠正它：这个不是 `ready-to-implement`，还缺复现步骤。它当场认错，回复得也很礼貌。

两天后，新 issue 进来，它又按同一套旧规则判断，错得很像上次。

这时候别急着给 Agent 加“长期记忆”。更常见的问题是：你的纠错只留在评论区，没有变成它下一次会读取的 Skill 文件。

Zach Lloyd 最近写的 [How to build a self-improvement loop for your Skills](https://x.com/zachlloydtweets/status/2066908445425496348)，我觉得最值得拿出来讲的就是这一点：让 Agent 变好，不是让它在心里记住“我错了”，而是把反馈改成一个能 review、能合并、能回滚的 `SKILL.md` diff。

![双层 Agent loop：执行和改进分开](illustrations/skill-self-improvement-loop/inner-outer-loop.png)

## 先拆开：一条线干活，一条线改说明书

很多人说 Agent loop，脑子里会浮现一个模型自己反复规划、执行、检查的循环。

Zach 讲的不是这种单次任务循环。他讲的是一个能力怎么越用越稳。

他的例子是 issue triage。内层 Agent 做日常工作：新 issue 创建后，读取内容，判断它属于 `ready-to-implement`、`duplicate` 还是 `needs-info`，然后贴标签、发评论、留下记录。

外层 Agent 不抢它的活。外层只定期回看：哪些判断被维护者改了？哪些评论被点了 👎？哪些“duplicate”后来被证明不是重复？这些反馈够不够强，能不能沉淀成一条新规则？

我会把这两条线分得很死：

- 内层 loop 负责产出。
- 外层 loop 负责复盘。
- 人类负责审核改动能不能进入主分支。

混在一起，Agent 很容易当场道歉、下次照旧。拆开以后，错误才有机会变成规则。

## Skill 是文件，所以能进 PR

这套方法能跑起来，有个前提很朴素：Skill 是文件。

文件和聊天记录最大的区别，不是格式，而是工程待遇。

文件能进 git。能看 diff。能 review。能回滚。能追到“这条规则是谁在什么时候改进去的”。

示例仓库 [warpdotdev-demos/issue-triage-loop](https://github.com/warpdotdev-demos/issue-triage-loop) 里的 `triage-issue` Skill，就没有写成一段含糊的“帮我判断 issue”。它把动作拆成了几步：

1. 读取 issue。
2. 搜索可能重复的问题。
3. 只能选一个桶：`ready-to-implement`、`needs-info`、`duplicate`。
4. 确保标签存在。
5. 贴上唯一标签。
6. 发一条带反馈入口的 triage 评论。

评论开头还会埋一个隐藏标记：`<!-- oz-triage v:<N> -->`。

这个版本号很关键。没有它，外层 Agent 只能猜：这次错是旧规则导致的，还是新规则改了但还不够。猜出来的“经验”，很容易变成新的噪音。

## 反馈不能只是一句“你错了”

自我改进最怕的不是不改，而是乱改。

一个用户说“不对”，Agent 就把 Skill 改掉；一个维护者随手换了标签，Agent 就写进永久规则。这种改进看起来勤奋，实际是在污染说明书。

所以反馈要先变成信号。

在这个例子里，可用信号很具体：

- triage 评论上的 👍 / 👎；
- 人类回复里的纠正理由；
- 维护者把 `ready-to-implement` 改成 `needs-info`；
- duplicate 判断后来被保留，还是被否定；
- 当前 issue 标签和当时 Agent 判断是否发生漂移。

这些信号里，我最看重两类：维护者明确 relabel，以及带原因的纠正回复。它们比一个表情反应更重，因为它们说明人类已经用自己的工作流成本投票了。

![反馈如何变成 Skill diff](illustrations/skill-self-improvement-loop/feedback-to-diff.png)

## 外层 Agent 只改强证据

外层 Agent 不应该像热心实习生一样，看到一句反馈就立刻改规则。

它更像一个周报编辑：看最近一批 triage 记录，找重复出现的错误，再把能泛化的经验写进 Skill。

比如某类 crash issue 连续两次被 Agent 判成 `ready-to-implement`，但维护者都改成了 `needs-info`，理由都是缺少 OS 和版本信息。那就可以写成一条新规则：

> 崩溃类 issue 如果缺少操作系统、版本号或复现步骤，优先标记为 `needs-info`，不要直接进入实现队列。

这条规则有用，因为它不是在修某一个 issue。它在修一类判断。

如果反馈很弱，或者几条信号互相打架，我宁愿不改。Agent Skill 的坏规则很难被发现，因为它会悄悄影响后面很多次执行。

## 我愿意让 Agent 提 PR，但不会让它直接改 main

这套方案最打动我的地方，是外层 Agent 最终提交的是 PR。

PR 里要说明：

- 它看了哪些 issue；
- 哪些反馈说明原规则不够好；
- 新增了哪几条 lesson；
- `SKILL.md` 的 diff 是什么；
- 版本号怎么变化。

人类 review 之后，合并才生效。

这一步听起来慢，其实是把 Agent 自我改进拉回普通软件工程。只要进入 PR，团队就能讨论、能反驳、能回滚。否则所谓“越用越聪明”，最后很可能只是越用越不可解释。

## 可复制的落地清单

如果我现在要在团队里试这套方法，会先挑一个低风险、高频、反馈清楚的 Skill。

issue triage 很适合。文档初审、PR 摘要、客服问题分类、运行日志归因，也可以。

第一版我会只做六件事：

1. 每次运行写入版本号和运行 ID。
2. 把 Agent 输出放到可查询的位置，比如 issue comment、review comment、trace 文件或数据库。
3. 给人类一个轻量反馈入口，不要一开始就做复杂评分表。
4. 定期收集强信号：relabel、纠正回复、测试失败、被 revert。
5. 只提炼能覆盖一类问题的 lesson。
6. 所有 Skill 改动走 PR，不直接改主分支。

这六步跑通之前，不建议急着上自动 grader、复杂指标和多 Agent 复盘。闭环本身不难，难的是别让低质量反馈进入执行规则。

## 什么时候不该用这套

不是所有 Skill 都值得做自我改进 loop。

如果任务低频，反馈模糊，或者错误代价很高，我会先停在人工 review。比如安全策略、发布审批、财务相关判断，这类 Skill 可以记录反馈，但不要让外层 Agent 自动改规则。

还有一种情况也不适合：团队连“正确结果”都没共识。人类自己都不知道某类 issue 该怎么分桶，Agent 收集再多反馈也只是把分歧写进文件。

所以这套方法最适合的起点，是那些已经有基本规则、每天都在跑、维护者愿意纠正的工作流。

下次 Agent 又犯同一个错时，可以先别问“它为什么记不住”。去看三件事：

- 这次错误有没有被记录？
- 纠正有没有变成可泛化 lesson？
- lesson 有没有进 `SKILL.md` 的 PR？

如果答案都是没有，那它不是学不会，是你还没给它一条能学习的路。

我建议先收藏上面的六步清单。后面如果继续拆，我会把这套 “反馈 -> lesson -> Skill diff -> PR” 做成一个可复制模板，用来检查自己的 Agent Skill 有没有真的闭环。

---

参考材料：

- [Zach Lloyd 的 X Article：How to build a self-improvement loop for your Skills](https://x.com/zachlloydtweets/status/2066908445425496348)
- [示例仓库：warpdotdev-demos/issue-triage-loop](https://github.com/warpdotdev-demos/issue-triage-loop)
- [Oz Agent Action README](https://github.com/warpdotdev/oz-agent-action)
- [Oz for OSS README](https://github.com/warpdotdev/oz-for-oss)


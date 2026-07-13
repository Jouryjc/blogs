# Research Notes — Skill Distillation（技能蒸馏）

调研时间：2026-07-12

## 来源 1：Iwo Szapar 实测文章（本篇主来源）

URL: https://www.iwoszapar.com/p/claude-code-skills-written-by-a-smarter-model
（WebFetch 抓取于 2026-07-12）

- **起源**：2026 年 7 月 1 日，一个 Reddit 帖子（大意为 "Have Fable 5 write skills for Opus 4.8 to use"）获得**数百条评论**；"skill distillation" 这个词是评论区创造的。
- **定义**：用更强大的模型编写 agent 技能，供廉价日常模型使用。原文表述："强大的模型写下来，你的日常模型保持它（The powerful model writes it down. Your everyday model keeps it.）"
- **时间窗口**：Fable 5 附赠（免费）额度到 **2026 年 7 月 7 日**截止；之后按 **$10 / 百万输入 token、$50 / 百万输出 token** 计费。
- **作者实测**：
  - 让 Fable 5 写了 **6 个技能**；
  - 盲测在 **Opus 4.8** 上执行（作者声明性能数字仅来自 Opus 4.8 的盲测）；
  - 结果：**12 胜、0 负、2 平**（共 14 次盲测评估）；
  - 坦承：初版中**有 2 个技能输掉了盲测，改写后才修正**；
  - 成本：加载技能后每个任务约增加 **7% 的 token 成本**。
- **SKILL.md 结构**："包含 name、description 和简明指令的 markdown 文件"；放在 `~/.claude/skills/<name>/SKILL.md`；"无权重、无微调、无 API（No weights, no fine-tuning, no API）"。
- **跨工具通用**：建立在 Agent Skills 开放标准上。文件路径对照：
  - Claude Code：`~/.claude/skills/<name>/SKILL.md`
  - Codex CLI：`~/.agents/skills/<name>/SKILL.md`
  - Gemini CLI：`~/.gemini/skills/` 或 `~/.agents/skills/` 别名
  - 原文："同一个文件夹、同样的 frontmatter、同样的 markdown 正文。"

## 来源 2：benjaminard/fable-skills 仓库

URL: https://github.com/benjaminard/fable-skills
（WebFetch + GitHub API 查询于 2026-07-12）

- 仓库描述："A skill library that teaches Claude Opus the working disciplines of Claude Fable 5. Move the checkpoints, not the capacity."（把 Fable 5 的工作纪律教给 Opus；移动的是检查点，不是能力上限。）
- 创建于 2026-07-02（Reddit 热帖次日）；**26 stars、5 forks**（GitHub API，2026-07-12）。
- 包含 **9 个技能**：verified-done、root-cause-first、minimal-diff、delegate-and-verify、finish-the-turn、lessons-ledger、outcome-first-writing、plain-handoff、evidence-audited-analysis。
- README 核心论点："你没法用一个 markdown 文件给模型更多能力（capacity），但你可以移动它的检查点（checkpoints）"——技能编码的是模型在输出前停下来验证的决策点。
- 技能内容源于 Anthropic 官方的 "Prompting Claude Fable 5" 指南中记录的模型行为；README 引 Anthropic 测试称 claim-auditing 指令在 Fable 上"几乎消除了捏造的状态汇报"，并称这类改进可迁移到 Opus。该仓库本身**没有发布对比基准数据**，只有定性描述。
- 安装方式：把 SKILL.md 复制进 Claude Code 的 `.claude/skills/` 目录即可，每个技能独立可装。

## 来源 3：alirezarezvani/claude-skills 仓库

URL: https://github.com/alirezarezvani/claude-skills
（WebFetch + GitHub API 查询于 2026-07-12）

- **GitHub API 实测（2026-07-12）：22,300 stars、3,115 forks**。
  - 注意：周报（reports/x-hot-ai-agent-engineering/2026-07-12.md）写的 "5.2k+ stars" 与 API 实测不符，**文章采用 API 实测的 22.3k**。
- 仓库描述（GitHub API 原文）："345 Claude Code skills & agent skills & plugins (30+ Agents, 70+ custom commands, 330+ skills, ...) for Claude Code, Codex, Gemini CLI, Cursor, and 8 more coding agents" —— 即 **345 个技能包、30+ agents、70+ 自定义命令，兼容 12 种编码智能体**（4 个点名 + 8 more）。
  - README 页面（WebFetch）另有 "355 skills / 13 platforms" 的更新口径；文章采用仓库描述的保守口径 **345 / 12 种**。
- 覆盖 18 个领域：工程、产品、营销、研究、合规、C-Level 顾问、财务、商业运营等。
- 安装：`/plugin marketplace add alirezarezvani/claude-skills`；多工具转换脚本 `./scripts/convert.sh --tool all` 可把技能转成各平台原生格式。

## 来源 4：Google agents-cli

主要 URL:
- TechTimes 报道（2026-07-01）: https://www.techtimes.com/articles/319412/20260701/google-agents-cli-one-command-adds-ai-agent-lifecycle-skills-claude-code-codex.htm（WebFetch 403，经 WebSearch 摘要交叉验证）
- Google 官方仓库: https://github.com/google/agents-cli
- Google Developers Blog: https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/

关键事实（WebSearch 交叉验证，2026-07-12）：

- Google 于 4 月 22 日发布 "Agents CLI in Agent Platform"，定位是 Google Cloud 上 Agent 开发生命周期的统一 CLI。
- 一条命令 `uvx google-agents-cli setup` 会把 **7 个结构化 Markdown 技能文件**装进编码助手的技能目录。
- 这些技能文件遵循 **SKILL.md 开放规范**——该规范由 **Anthropic 于 2025 年 12 月发布**，目前已有 **32 种编码工具支持**（TechTimes 数据）。
- GitHub 仓库明确列出支持 Antigravity CLI、Claude Code、Codex，且兼容任何支持 SKILL.md 标准的编码智能体。
- 技能覆盖：项目脚手架、评估管线搭建、部署（Cloud Run / GKE / Agent Runtime）、Gemini Enterprise 注册、可观测性配置。

## 来源 5：周报聚合（仓库内部）

路径: /Users/yjcjour/Documents/code/2026/4/blogs/reports/x-hot-ai-agent-engineering/2026-07-12.md

- "Reddit 数百评论热帖；一天内出圈"（skill distillation 传播速度描述）。
- 选题确认：本篇与 wechat-drafts/2026-06-18-skill-self-improvement-loop（《Agent 为什么总学不会？把反馈写回 Skill》）构成系列。
- 周报中 claude-skills "5.2k+ stars" 的数据已被 GitHub API 实测（22.3k）取代，文章不使用 5.2k。

## 文章中使用的数字对照表（事实纪律自查）

| 文章中的说法 | 出处 |
|---|---|
| Reddit 帖 7 月 1 日发出、数百条评论、"skill distillation" 出自评论区 | 来源 1 |
| 一天出圈 | 来源 5（周报） |
| Fable 5 附赠额度 7 月 7 日到期；$10/M 输入、$50/M 输出 | 来源 1 |
| 6 个技能、盲测 12 胜 0 负 2 平、仅测 Opus 4.8 | 来源 1 |
| 2 个技能初版盲测失败、改写后通过 | 来源 1 |
| 每任务 +7% token 成本 | 来源 1 |
| SKILL.md = name + description + 指令；无权重无微调无 API | 来源 1 |
| Claude Code / Codex CLI / Gemini CLI 路径对照 | 来源 1 |
| fable-skills 9 个技能、"移动检查点不是能力" | 来源 2 |
| claude-skills 345 技能、22.3k stars、12 种智能体、18 领域 | 来源 3 |
| agents-cli 一条命令装 7 个技能文件 | 来源 4 |
| SKILL.md 规范 Anthropic 2025 年 12 月发布、32 种工具支持 | 来源 4（TechTimes） |

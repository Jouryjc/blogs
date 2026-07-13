---
title: "Trellis 研究笔记"
source: "https://github.com/mindfold-ai/Trellis"
source_author: "Mindfold AI"
created_at: "2026-06-20"
tags:
  - type/source
  - topic/agent-runtime
  - topic/agent-memory
  - topic/context-engineering
  - topic/agent-design
moc:
  - "[[agent-runtime]]"
  - "[[agent-memory]]"
  - "[[context-engineering]]"
  - "[[agent-design]]"
related:
  - "[[trellis-agent-workbench]]"
---

# Trellis 研究笔记

## 一手来源

- GitHub: https://github.com/mindfold-ai/Trellis
- 中文 README: https://github.com/mindfold-ai/Trellis/blob/main/README_CN.md
- 官方文档: https://docs.trytrellis.app/zh
- 快速开始: https://docs.trytrellis.app/zh/start/install-and-first-task
- 支持平台: https://docs.trytrellis.app/zh/advanced/multi-platform
- npm: https://www.npmjs.com/package/@mindfoldhq/trellis

## 当前事实核验

- 写稿时间: 2026-06-20。
- GitHub API 返回仓库: `mindfold-ai/Trellis`。
- 仓库描述: `The best agent harness.`
- Star: 10,785。
- Fork: 611。
- 默认分支: `main`。
- 最近 push: 2026-06-18T14:29:55Z。
- 许可证: AGPL-3.0。
- npm latest: `0.6.3`。
- npm package: `@mindfoldhq/trellis`。
- npm license: AGPL-3.0-only。

## README 给出的定位

Trellis 是一个开箱即用的 AI 编码工程化框架。它解决的不是模型能不能写代码，而是 AI coding agent 每次会话都容易从零开始的问题: 记不住项目规范、团队需求和上一次工作脉络。

Trellis 的做法是把规范、任务和记忆沉淀进仓库，让不同 coding agent 都能按照同一套工程标准工作。

## 关键能力

README 列出的 5 个能力:

1. 自动注入规范: 规范写在 `.trellis/spec/`，Trellis 按当前任务注入相关上下文。
2. 任务驱动工作流: PRD、实现上下文、审查上下文、任务状态放在 `.trellis/tasks/`。
3. 项目记忆: `.trellis/workspace/` 中的 journal 保存上一次会话脉络。
4. 团队共享标准: Spec 随仓库版本化，让个人经验变成团队基础设施。
5. 多平台复用: 同一套 Trellis 结构覆盖 16 个 AI coding 平台。

## 基本安装和初始化

前置要求:

- Node.js >= 18
- Python >= 3.9

README 给出的命令:

```bash
npm install -g @mindfoldhq/trellis@latest
trellis init -u your-name
trellis init --cursor --opencode --codex -u your-name
```

其中第三条用于只初始化实际使用的平台。

## 使用流程

README 描述的使用流程:

1. 用自然语言描述需求。
2. 与 AI 一起头脑风暴，一次回答一个问题，直到 PRD 足够清晰，再开始实现。
3. 交由 AI 推进实现，AI 会调用 `trellis-implement`，并依据 Spec、lint、type-check、tests 做检查。
4. 工作完成或上下文快满时，输入 `/trellis:finish-work`，Trellis 归档任务并更新工作日志。

官方 How It Works 对 `finish-work` 有一个更精确的边界: 只有工作 commit 已经存在后，才应该运行 `/trellis:finish-work`。它做的是归档和 journal 记账，不是提交功能代码的命令。

## 工作原理

Trellis 内部是 4 阶段循环:

1. Plan: `trellis-brainstorm` 逐题澄清需求并写 `prd.md`；研究任务可交给 `trellis-research` 子代理。相关上下文由 `implement.jsonl` / `check.jsonl` 编排。
2. Implement: `trellis-implement` 子代理按 PRD 写代码，上下文按 `implement.jsonl` 自动注入，不执行 git commit。
3. Verify: `trellis-check` 子代理根据 diff 对照 Spec 检查，并运行 lint、type-check、tests，能修则修。
4. Finish: 运行最终检查，`trellis-update-spec` 把本轮新增认知沉淀回 `.trellis/spec/`。

官方 How It Works 还说明: 下一次 AI 会话会重新读取仓库状态，不需要上一段聊天记录，也能知道任务是什么、哪些 spec 适用、下一步应该执行哪个 workflow step。

## 多平台边界

官方多平台文档说明 Trellis 支持 16 个平台: Claude Code、Cursor、OpenCode、Codex、Kiro、Kilo、Gemini CLI、Antigravity、Devin、Qoder、CodeBuddy、GitHub Copilot、Droid、Pi Agent、Reasonix、ZCode，以及读取 `.agents/skills/` 规范的其他 AI coding agent。

需要注意: 不同平台交付方式不同。Claude Code / Cursor / OpenCode 等平台有更完整的 SessionStart、hook、sub-agent 上下文注入；Codex 使用 `AGENTS.md` 加 `UserPromptSubmit` hook，部分 workflow 入口以 skill 形式交付，不一定是原生 slash command。

## 与 CLAUDE.md / AGENTS.md 的差异

README FAQ 的判断: `CLAUDE.md`、`AGENTS.md`、`.cursorrules` 是有用入口，但容易变成单体长文档。Trellis 在它们上面补充:

- scoped specs
- task PRDs
- workflow gates
- workspace memory
- platform-aware generated files

文章里可以解释为: AGENTS.md 更像项目说明书，Trellis 更像一套把说明书、任务单、验收记录和复盘记忆组织起来的工作台。

## 标题候选

1. 推荐标题: AI 编程总是失忆？Trellis 把规范和任务写回仓库
2. 稳妥标题: Trellis：把 AI 编程流程做成仓库里的工程记忆
3. 大众标题: 别再每次重新教 AI 写代码，试试 Trellis
4. 专家标题: Trellis 如何用 Specs、Tasks 和 Journal 管住 Coding Agent
5. 反差标题: AI 写代码最大坑不在模型，而在项目记忆散了

最终选择推荐标题。理由: 先命中 AI 编程反复解释项目背景的体感问题，再给出 Trellis 的技术路径。

## 文章主线

- 开头先判断: Trellis 解决的是 coding agent 失忆和标准散落问题，不是替代 Claude Code / Codex / Cursor。
- 第一部分解释痛点: 每次开新会话，规范、任务上下文、验收标准、历史决策都要重新解释。
- 第二部分解释 Trellis 放了哪三类东西: spec、task、workspace journal。
- 第三部分讲安装和第一次使用。
- 第四部分讲 4 阶段循环。
- 第五部分讲适合谁、不适合谁和注意事项。

## 需要谨慎表达的边界

- Trellis 不能保证 AI 一定写对代码，它提供的是工程化上下文和流程约束。
- 生成的 specs 需要人工 review，不能把 AI 生成规则直接当团队规范。
- AGPL-3.0 对商业/内部改造场景有合规影响，需要团队自己确认。
- 多平台支持来自官方 README，但不同平台的命令和触发体验可能有差异。
- 第一次接入最好用实验分支或小仓库，不要直接在生产主分支上跑大任务。

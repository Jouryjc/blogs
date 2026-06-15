---
title: "GSD Core 与 SDD 工作流研究笔记"
tags:
  - type/source
  - topic/context-engineering
  - topic/agent-skills
  - topic/agent-design
moc:
  - "[[context-engineering]]"
  - "[[agent-skills]]"
related:
  - "[[wechat-drafts/2026-06-13-gsd-build-sdd/article]]"
---

# GSD Core 与 SDD 工作流研究笔记

Created: 2026-06-13

## 来源入口

- 用户给定仓库：`gsd-build/get-shit-done`
  - URL: https://github.com/gsd-build/get-shit-done
  - 当前状态：README 已标明该仓库不再是活跃开发位置，项目已迁移到 `open-gsd/gsd-core`。

## 一手来源与关键信息

- GSD Core README
  - URL: https://github.com/open-gsd/gsd-core
  - Key facts:
    - GSD Core 自称是轻量级 meta-prompting、context engineering 与 spec-driven development 系统。
    - 支持 Claude Code、OpenCode、Gemini CLI、Kimi CLI、Kilo、Codex、Copilot、Cursor、Windsurf 等运行时。
    - 解决的问题是 context rot：随着上下文窗口填满，输出质量悄悄下降。
    - 主要方法是把研究、规划、执行等重工作交给 fresh-context subagents，主会话保持轻量。
    - 每个 milestone 重复 Discuss、Plan、Execute、Verify、Ship 五步循环。
    - 安装入口是 `npx @opengsd/gsd-core@latest`。
    - 旧仓库不要直接复制 `agents/` 或 `commands/`，应使用 installer 做跨运行时转换。

- GSD Core: Install on your runtime
  - URL: https://github.com/open-gsd/gsd-core/blob/main/docs/how-to/install-on-your-runtime.md
  - Key facts:
    - 需要 Node.js 18+ 和 npm/npx。
    - installer 会根据不同运行时转换 schema、目录布局和命令语法。
    - Claude Code 常见安装：`npx @opengsd/gsd-core@latest --claude --global`。
    - 不同运行时命令形态不同：Claude/OpenCode 等使用 `/gsd-*`，Gemini 使用 `/gsd:*`，Codex 使用 `$gsd-*`。
    - GSD 会安装 hooks 用于 session orientation、context monitoring、prompt/read/workflow guard、commit validation 等。

- GSD Core: Your first project
  - URL: https://github.com/open-gsd/gsd-core/blob/main/docs/tutorials/your-first-project.md
  - Key facts:
    - 首次项目从 `/gsd-new-project` 开始，生成 `.planning/PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md`、`STATE.md`、`config.json`。
    - `/gsd-discuss-phase 1` 会把实现偏好和决策写入 `CONTEXT.md`。
    - `/gsd-plan-phase 1` 会生成 `RESEARCH.md` 和多个原子 `PLAN.md`。
    - `/gsd-execute-phase 1` 会按 wave 并行执行计划，并为每个 task 原子提交。
    - `/gsd-verify-work 1` 走用户验收，并在失败时诊断和生成 fix plan。
    - `/gsd-ship 1` 创建 PR，PR body 包含 Summary、Changes、Requirements Addressed、Verification 和 Key Decisions。

- GSD Core: The phase loop
  - URL: https://github.com/open-gsd/gsd-core/blob/main/docs/explanation/the-phase-loop.md
  - Key facts:
    - 核心循环是 Discuss -> optional UI design -> Plan -> Execute -> Verify -> Ship。
    - Discuss 解决怎么做的问题，输出 `CONTEXT.md`。
    - Plan 负责研究、拆解和计划验证，输出 `RESEARCH.md` 与 `PLAN.md`。
    - Execute 让每个 executor 在干净 200k-token context 中只读取任务所需材料。
    - Verify 不只是测试，还检查 requirement coverage、decision coverage 和 phase goal alignment。
    - Ship 负责创建 PR 并归档 phase artefacts。
    - `.planning/` 让工作跨 session、跨 context reset 存续。

- GSD Core: Context engineering
  - URL: https://github.com/open-gsd/gsd-core/blob/main/docs/explanation/context-engineering.md
  - Key facts:
    - Context rot 表现为违背早期决策、风格漂移、遗漏要求、幻觉文件名或函数签名。
    - `/clear` 可以重启上下文，但会丢连续性。
    - GSD 的答案是主会话只做 orchestrator，重工作由 fresh-context subagents 完成。
    - Spec-driven artefacts 保证每个 fresh agent 读到正确目标，而不只是读到一个干净窗口。
    - `.planning/STATE.md` 是系统脊柱，记录当前 milestone、phase、plan 进度和 blocker。
    - GSD 明确承认 trade-off：phase loop 对小改动有额外开销，小任务应该使用 `/gsd-quick` 或 `/gsd-fast`。

- Superpowers README
  - URL: https://github.com/obra/superpowers
  - Key facts:
    - Superpowers 是一个给 coding agents 使用的完整软件开发方法论，建立在可组合 skills 和初始指令上。
    - 它会在发现用户要构建东西时先追问目标，而不是直接写代码。
    - 基本 workflow：brainstorming、using-git-worktrees、writing-plans、subagent-driven-development 或 executing-plans、test-driven-development、requesting-code-review、finishing-a-development-branch。
    - 强调 RED-GREEN-REFACTOR、YAGNI、DRY、系统化 debugging、verification-before-completion。
    - 关键定位不是 spec 仓库，而是让 agent 自动触发正确工程技能。

- OpenSpec README
  - URL: https://github.com/Fission-AI/OpenSpec
  - Key facts:
    - OpenSpec 是 AI coding assistants 的轻量 SDD 框架。
    - 哲学：fluid not rigid、iterative not waterfall、easy not complex、built for brownfield not just greenfield。
    - 默认 quick path：`/opsx:propose` -> `/opsx:apply` -> `/opsx:sync` -> `/opsx:archive`。
    - 每个 change 目录包含 proposal、specs、design、tasks。
    - `openspec/specs/` 是当前系统行为的 source of truth，change 完成后 delta specs merge 回主 specs。
    - OpenSpec 支持 20+ 或 25+ AI 工具，具体支持列表随版本变化。

- OpenSpec: Getting Started / OPSX
  - URL: https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
  - URL: https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md
  - Key facts:
    - `openspec init` 后会生成 `openspec/specs/`、`openspec/changes/` 和可选 `config.yaml`。
    - `proposal.md` 捕获 why/what，`specs/` 表示变更 delta，`design.md` 捕获 how，`tasks.md` 是 checklist。
    - Delta spec 使用 ADDED、MODIFIED、REMOVED 表达相对当前 spec 的变化。
    - OPSX 强调 actions not phases，dependencies are enablers。
    - 如果实现中发现设计不对，可以改 artifact 后继续。

## 5 个标题候选

1. 推荐标题：Agent 长任务总烂尾？GSD 用阶段循环跑到 PR
2. 稳妥标题：GSD Core 怎么用：从需求到 PR 的 Agent 阶段循环
3. 大众标题：别只让 AI 写代码，先把任务拆到能验收
4. 专家标题：GSD、Superpowers、OpenSpec：三种 SDD 工作流怎么选
5. 反差标题：SDD 不是多写文档，而是让 Agent 少跑偏

Chosen: Agent 长任务总烂尾？GSD 用阶段循环跑到 PR

## 文章承诺

把 GSD Core 讲成一个真实可用的 AI 编程工作流：它解决什么问题、怎么安装、一次需求如何从 `/gsd-new-project` 走到 `/gsd-ship`，以及它和 Superpowers、OpenSpec 这两类 SDD 的差别。

## 配图规划

1. `imgs/article-cover.png`：标题封面，问题 -> GSD 阶段循环 -> PR。
2. `imgs/phase-loop.png`：Discuss -> Plan -> Execute -> Verify -> Ship。
3. `imgs/planning-artifacts.png`：`.planning/` 工件地图。
4. `imgs/sdd-comparison.png`：GSD / Superpowers / OpenSpec 三列对比。
5. `imgs/when-to-use-gsd.png`：什么时候用 GSD，什么时候不要用。

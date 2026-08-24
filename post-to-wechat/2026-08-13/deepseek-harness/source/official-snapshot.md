---
title: "DeepSeek Harness 一手资料快照"
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
  - "[[post-to-wechat/2026-08-13/deepseek-harness/source/research-notes]]"
  - "[[post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness]]"
---

# DeepSeek Harness 一手资料快照

## 核验截面

- 核验时间：2026-08-13 23:13（Asia/Singapore）
- 官方仓库：https://github.com/deepseek-ai/deepseek-harness
- 本地研究检出提交：`47f943859bef60e4160492346772ded9b24f765a`
- 提交时间：2026-08-13 19:38:46 +08:00
- 提交标题：`Merge pull request #2519 from deepseek-harness/feat/npm-public`
- 默认分支：`master`
- 许可证：MIT
- 固定提交根 `package.json`：`0.1.0-rc.5`
- 核验时 npm `@deepseek-ai/dsh`：`0.1.0-rc.6`
- 核验时 GitHub API：27,011 stars、1,976 forks

仓库在文章写作期间仍快速变化。正文不以星数或 RC 版本作为价值论据；上述数字只用于说明核验截面。

## 官方发布入口

- 官方 README：https://github.com/deepseek-ai/deepseek-harness/blob/master/README.zh.md
- 官方发布帖：https://x.com/deepseek_ai/status/2087887408440164663
- npm：https://www.npmjs.com/package/@deepseek-ai/dsh
- Cordis 设计预印本：https://github.com/cordiverse/paper

## 本次重点核验文件

- `README.zh.md`
- `docs/architecture.zh.md`
- `docs/cordis-primer.zh.md`
- `docs/agent-lifecycle.zh.md`
- `docs/tool-execution-pipeline.zh.md`
- `docs/capability-seams.zh.md`
- `docs/subsystems/core.zh.md`
- `docs/subsystems/subagent.zh.md`
- `docs/subsystems/workflow.zh.md`
- `docs/subsystems/approval.zh.md`
- `docs/subsystems/sandbox.zh.md`
- `docs/user/guide/index.zh.md`
- `docs/user/guide/python-sdk.zh.md`
- `packages/README.zh.md`
- `packages/bundle/base/cordis.patch.yml`
- `packages/bundle/base/README.zh.md`
- `packages/bundle/web-app/README.zh.md`
- `packages/bundle/headless/README.zh.md`
- `apps/cli/README.zh.md`
- `package.json`
- `pnpm-workspace.yaml`
- `vendor/README.md`

## 同名项目排除

本文介绍的是 DeepSeek AI 官方 GitHub 组织下的 TypeScript monorepo `deepseek-ai/deepseek-harness`，npm 入口为 `@deepseek-ai/dsh`。

不把第三方项目 `HenryZ838978/deepseek-harness`、PyPI 包 `deepseek-harness`，或其他“支持 DeepSeek 模型的 Harness”写成官方产品能力。

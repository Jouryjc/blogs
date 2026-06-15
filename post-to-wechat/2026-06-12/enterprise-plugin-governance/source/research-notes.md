---
title: "Codex 与 Claude 企业级 Plugin 管理研究笔记"
source: "https://developers.openai.com/codex/plugins"
source_author: "OpenAI Developers / Anthropic Claude Code Docs"
tags:
  - type/source
  - topic/claude-code
  - topic/agent-skills
  - topic/agent-design
  - topic/agent-safety
moc:
  - "[[claude-code]]"
  - "[[agent-skills]]"
  - "[[agent-design]]"
  - "[[agent-safety]]"
related:
  - "[[post-to-wechat/2026-06-12/enterprise-plugin-governance/enterprise-plugin-governance]]"
  - "[[wechat-drafts/2026-05-26-custom-claude-plugins/article]]"
---

# Codex 与 Claude 企业级 Plugin 管理研究笔记

Created: 2026-06-12

## 5 个标题候选

1. 推荐标题：Codex、Claude 插件越装越乱？企业落地先管边界
2. 稳妥标题：企业如何管理 Codex 和 Claude 插件
3. 大众标题：团队用 AI 编程工具，先别急着装插件
4. 专家标题：Codex 与 Claude Code Plugin 治理：分发、权限和审计
5. 反差标题：插件不是能力越多越好，最大坑是边界失控

Chosen: Codex、Claude 插件越装越乱？企业落地先管边界

## 文章承诺

把 Codex 和 Claude Code 的 plugin / skill / MCP / hook / managed settings 放进同一套企业治理框架里，给出可落地的分发、权限、版本、审计和 rollout 清单。

## 官方资料要点

### OpenAI Codex

- Codex Plugins: https://developers.openai.com/codex/plugins
  - Plugin 是可安装的能力包，可包含 skills、app integrations、MCP servers。
  - Plugin 安装后仍受现有 approval settings 约束；外部 app 仍受自己的认证、隐私和数据政策约束。
  - 插件可以通过 curated directory、workspace sharing、marketplace 等方式分发。

- Codex Build plugins: https://developers.openai.com/codex/plugins/build
  - 本地迭代阶段用 skill；当要跨团队共享、绑定 app/MCP、打包 lifecycle hooks、发布稳定包时再做 plugin。
  - Manifest 路径是 `.codex-plugin/plugin.json`。
  - Repo marketplace 可放在 `$REPO_ROOT/.agents/plugins/marketplace.json`，个人 marketplace 可放在 `~/.agents/plugins/marketplace.json`。
  - 可用 `codex plugin marketplace add` 管理 marketplace，并用 `--ref` pin Git ref。
  - 可在 Codex app 内将本地 plugin 分享给 workspace 成员或 group。

- Codex Skills: https://developers.openai.com/codex/skills
  - Skill 是可复用工作流的 authoring format，Plugin 是可安装分发单元。
  - Skill 使用 progressive disclosure：初始上下文只放名称、描述和路径；完整 `SKILL.md` 只在触发时加载。
  - Skill 描述需要清晰，否则安装过多时初始列表会被压缩或省略。
  - Codex 可从 repo/user/admin/system 多个位置读取 skills。

- Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
  - Codex 在工作前读取 `AGENTS.md`，按 global -> project -> current directory 叠加。
  - 更靠近当前目录的规则覆盖更早规则。
  - 默认项目说明合并上限是 32 KiB，可通过配置调整。

- Codex MCP: https://developers.openai.com/codex/mcp
  - MCP 配置位于 `config.toml`；支持 STDIO 和 streamable HTTP。
  - 可配置 enabled tools、disabled tools、默认 approval mode 和 per-tool approval。
  - Plugin-provided MCP servers 由插件 manifest 提供，用户仍可在 config 中控制 enabled 和 tool policy。

- Codex Managed configuration: https://developers.openai.com/codex/enterprise/managed-configuration
  - 企业管理员可用 requirements 和 managed defaults 管控本地 Codex 行为。
  - Requirements 可约束 approval policy、sandbox、permission profiles、MCP allowlist、web search、network domains、hooks、feature flags 等。
  - Cloud-managed requirements 优先于 MDM 和系统文件。

- Codex Hooks: https://developers.openai.com/codex/hooks
  - Hooks 允许在 agent loop 中注入脚本，用于 prompt 扫描、日志、校验、记忆、目录定制等。
  - Non-managed hooks 需要被 review/trust；managed hooks 由策略信任且不能被用户禁用。

- Codex Governance: https://developers.openai.com/codex/enterprise/governance
  - 企业可用 Analytics Dashboard/API 和 Compliance API 做使用量、adoption、Code Review、activity logs 和审计。

### Anthropic Claude Code

- Claude Code Plugins: https://code.claude.com/docs/en/plugins
  - Standalone `.claude/` 适合个人、项目内、实验性配置；Plugin 适合团队共享、跨项目复用、版本更新和 marketplace 分发。
  - Claude plugin 可包含 skills、agents、hooks、MCP servers、LSP servers、monitors、settings。
  - 本地测试用 `claude --plugin-dir ./my-plugin`，修改后可用 `/reload-plugins`。
  - Plugin skills 使用命名空间，例如 `/my-plugin:hello`。

- Claude Plugins reference: https://code.claude.com/docs/en/plugins-reference
  - Manifest 路径是 `.claude-plugin/plugin.json`。
  - CLI 支持 `claude plugin init/install/uninstall/prune/enable/disable/update/list/details/tag`。
  - `plugin install --scope user|project|local` 控制安装范围；project scope 写入 `.claude/settings.json`，可被团队共享。
  - `defaultEnabled: false` 可让高成本或高权限 plugin 默认安装后不启用。

- Claude settings: https://code.claude.com/docs/en/settings
  - Scopes: managed、user、project、local。Managed 适合组织级不可绕过策略；project 适合 repo 团队共享；local 适合个人且 gitignored。
  - `extraKnownMarketplaces` 可添加 marketplace；`strictKnownMarketplaces` 是 managed-only allowlist，可限制用户只能安装批准来源。
  - `enabledPlugins` 控制插件启用状态。

- Claude hooks: https://code.claude.com/docs/en/hooks-guide
  - Hooks 是用户定义 shell commands，在 Claude Code 生命周期事件中执行，用于格式化、通知、阻止受保护文件、审计配置变更等。
  - Hook 用于确定性控制；判断型决策可用 prompt-based 或 agent-based hooks。

- Claude MCP: https://code.claude.com/docs/en/mcp
  - 可通过 `oauth.scopes` pin MCP OAuth scopes，把授权范围限制在安全团队批准的子集。
  - `headersHelper` 可为 Kerberos、短期 token、内部 SSO 等自定义认证动态生成 headers。

- Claude Security / IAM:
  - https://code.claude.com/docs/en/security
  - https://code.claude.com/docs/en/iam
  - 官方建议敏感代码仓库使用 project-specific permission settings，定期用 `/permissions` 审计，团队层面使用 managed settings、版本化 permission configuration、OpenTelemetry metrics、ConfigChange hooks。
  - Claude for Enterprise 增加 SSO、domain capture、role-based permissions、Compliance API、managed policy settings。

## 文章判断

- 企业治理重点不是“允许不允许插件”，而是把 plugin 当作软件供应链的一部分：来源、版本、权限、数据、验证、回滚、审计都要有 owner。
- Skill 解决“方法复用”；Plugin 解决“安装分发”；MCP 解决“工具连接”；Hook 解决“必须执行的约束”；Managed settings / requirements 解决“组织不可绕过的边界”。
- 初期不要建大平台。先用 repo marketplace / workspace sharing / project settings 做一条可控分发链，再逐步接入 managed settings 和 analytics。

## 配图计划

1. 封面：企业插件治理，不是装得越多越好。
2. 正文图 1：AI 编程工具的能力栈。
3. 正文图 2：Codex 与 Claude 的插件管理地图。
4. 正文图 3：Plugin Bill of Materials。
5. 正文图 4：权限闸门：marketplace、MCP、hooks、sandbox、audit。
6. 正文图 5：五步 rollout loop。

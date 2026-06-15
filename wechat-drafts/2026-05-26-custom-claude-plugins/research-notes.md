---
title: "Claude 自定义 Plugin 研究笔记"
tags:
  - type/source
  - topic/claude-code
  - topic/agent-skills
moc:
  - "[[claude-code]]"
related:
  - "[[wechat-drafts/2026-05-26-custom-claude-plugins/article]]"
---

# Research Notes: Custom Claude Plugins

Created: 2026-05-26

## Sources

- Claude Code docs: Create plugins
  - URL: https://code.claude.com/docs/en/plugins
  - Key facts:
    - Plugins extend Claude Code with skills, agents, hooks, and MCP servers.
    - Use standalone `.claude/` for personal or project-only customization.
    - Use plugins when functionality should be shared across projects, teams, or marketplaces.
    - A plugin directory contains `.claude-plugin/plugin.json`.
    - Other component directories live at the plugin root, not inside `.claude-plugin/`.
    - Test local plugins with `claude --plugin-dir ./my-first-plugin`.
    - Plugin skills are namespaced, for example `/my-first-plugin:hello`.
    - `$ARGUMENTS` captures text after the skill name.
    - Share by adding README, version strategy, marketplace, and testing with teammates.
    - Run `claude plugin validate` before submitting a community plugin.

- Claude Code docs: Plugins reference
  - URL: https://code.claude.com/docs/en/plugins-reference
  - Key facts:
    - Plugin components include skills, agents, hooks, MCP servers, LSP servers, monitors, output styles, themes, executables, and settings.
    - Manifest path: `.claude-plugin/plugin.json`.
    - Skills default location: `skills/<name>/SKILL.md`.
    - Commands are legacy / flat markdown; use `skills/` for new plugins.
    - Agents default location: `agents/`.
    - Hooks default location: `hooks/hooks.json`.
    - MCP server definitions default location: `.mcp.json`.
    - LSP server definitions default location: `.lsp.json`.
    - Monitors default location: `monitors/monitors.json`.
    - `bin/` executables are added to Bash PATH while plugin is enabled.
    - A plugin-root `CLAUDE.md` is not loaded as project context; ship loadable instructions as skills.

- Claude.ai docs: Plugins overview
  - URL: https://claude.com/docs/plugins/overview
  - Key facts:
    - Plugins are reusable capability packages that bundle MCP connectors, skills, slash commands, and sub-agents.
    - Claude Code has full plugin support.
    - Claude Cowork also supports plugins in research preview for paid users.
    - Official docs position plugins as role/team/company specialization packages.

- Claude Code docs: Discover plugins
  - URL: https://code.claude.com/docs/en/discover-plugins
  - Key facts:
    - Marketplaces can be added from GitHub repos, Git URLs, local paths, and remote `marketplace.json` URLs.
    - Demo marketplace: `anthropics/claude-code`.

- Claude Code docs: Plugin marketplaces
  - URL: https://code.claude.com/docs/en/plugin-marketplaces
  - Key facts:
    - Marketplace manifest requires `name`, `owner`, and `plugins`.
    - Plugin entries require `name` and `source`.
    - Third-party marketplaces cannot use reserved official-looking names.

## 5 Title Candidates

1. 推荐标题：Claude 总跑偏？做个 Plugin 固化工作流
2. 稳妥标题：从目录开始，做一个自定义 Claude Plugin
3. 大众标题：把 Claude 调成顺手工具，从一个插件开始
4. 专家标题：Claude Code Plugin 入门：Skill、Agent、Hook 和 MCP 怎么打包
5. 反差标题：Claude 插件不是魔法，真正有用的是工作流封装

Chosen: Claude 总跑偏？做个 Plugin 固化工作流

## Article Promise

Teach a first-time reader how to build a minimal custom Claude Code plugin by hand, understand when a plugin is better than `.claude/`, and know how to expand from one Skill to agents, hooks, MCP, and marketplaces.

## Practical Asset

- Minimal directory template.
- Minimal `plugin.json`.
- Minimal `SKILL.md`.
- Local test commands.
- Decision checklist for when to add Skill / Agent / Hook / MCP / Marketplace.


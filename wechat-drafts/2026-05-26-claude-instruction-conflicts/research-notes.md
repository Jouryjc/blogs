# Research Notes: Claude .claude vs Global Plugins Conflicts

Created: 2026-05-26

## Sources

- Claude Code docs: Slash commands
  - URL: https://code.claude.com/docs/en/slash-commands
  - Key facts:
    - Custom slash commands can live in project commands under `.claude/commands/`.
    - Personal commands can live in `~/.claude/commands/`.
    - Markdown file names map to command names.
    - `$ARGUMENTS` can pass user input to commands.
    - Custom commands have been merged into skills; `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`.
    - Skill locations include enterprise, personal, project, and plugin.
    - When skills share names across levels, enterprise overrides personal, and personal overrides project.
    - Plugin skills use `plugin-name:skill-name` namespace, so they cannot conflict with other levels.
    - If a skill and a command share the same name, the skill takes precedence.

- Claude Code docs: Create plugins
  - URL: https://code.claude.com/docs/en/plugins
  - Key facts:
    - Plugins package reusable Claude Code functionality.
    - Plugin components can include skills, agents, hooks, and MCP servers.
    - Local plugins can be tested with `claude --plugin-dir ./my-first-plugin`.
    - Plugin skills are namespaced in command form, for example `/my-first-plugin:hello`.
    - Use `.claude/` for personal/project-only customizations and plugins for reusable/team-shared functionality.

- Claude Code docs: Plugins reference
  - URL: https://code.claude.com/docs/en/plugins-reference
  - Key facts:
    - Plugin components include skills, agents, hooks, MCP servers, LSP servers, monitors, output styles, themes, executables, and settings.
    - Manifest path is `.claude-plugin/plugin.json`.
    - Skills default path is `skills/<name>/SKILL.md`.
    - Commands are legacy; new plugins should generally use skills.
    - Plugin root `CLAUDE.md` is not loaded as project context; plugin instructions should be shipped through loadable components such as skills.

- Claude Code docs: Settings
  - URL: https://code.claude.com/docs/en/settings
  - Key facts:
    - Settings precedence is enterprise managed policy, command line arguments, local project settings, shared project settings, then user settings.
    - MCP server precedence by name is local, project, then user.
    - Permission rules are merged with deny rules taking precedence over allow rules.

- Claude Code docs: Subagents
  - URL: https://code.claude.com/docs/en/sub-agents
  - Key facts:
    - Project subagents live in `.claude/agents/`.
    - User subagents live in `~/.claude/agents/`.
    - When names conflict, project-level agents take precedence over user-level agents.

## 5 Title Candidates

1. 推荐标题：Claude 指令撞车时，谁说了算？
2. 稳妥标题：项目 .claude 和全局 Plugin 冲突时会发生什么
3. 大众标题：Claude 为什么有时不听你项目里的规则？
4. 专家标题：Claude Code 指令解析：.claude、Plugin、Skill、Agent 的优先级
5. 反差标题：不是项目一定优先：Claude 指令冲突的真实规则

Chosen: Claude 指令撞车时，谁说了算？

## Article Promise

Explain, from the loading and dispatch model, what happens when project `.claude` customizations and globally installed plugins appear to define the same instruction or behavior.

## Practical Asset

- Conflict decision table.
- Local reproduction checklist.
- Rule-of-thumb for choosing `.claude`, user-level customization, plugin, hook, MCP.
- Concrete example: global Plugin `review` Skill vs project `.claude/commands/review.md`, plus personal `~/.claude/skills/review` caveat.

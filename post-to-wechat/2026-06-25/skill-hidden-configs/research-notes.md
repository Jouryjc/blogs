---
title: "Skill hidden configuration research notes"
created_at: "2026-06-25"
tags:
  - type/source
  - topic/agent-skills
  - topic/agent-runtime
moc:
  - "[[agent-skills]]"
  - "[[agent-runtime]]"
related:
  - "[[post-to-wechat/2026-06-25/skill-hidden-configs/article]]"
---

# Skill Hidden Configuration Research Notes

## Writing Goal

Write a 蒸馏小余 style WeChat article about five lesser-known configuration surfaces around Agent Skills / Claude Code Skills / Codex Skills.

Reader promise: help developers avoid writing everything into `SKILL.md`, and understand which knob controls runtime compatibility, permissions, invocation, agent delegation, context isolation, and runtime integration.

## Title Candidates

1. 推荐标题：`Skill 老是不听话？先看这 5 个冷门配置`
2. 稳妥标题：`5 个容易被忽略的 Agent Skill 配置`
3. 大众标题：`给 AI 写 Skill，别只会写说明书`
4. 专家标题：`从 allowed-tools 到 context: fork：Skill 控制面拆解`
5. 反差标题：`Skill 最大的坑，不在内容，而在配置放错地方`

Chosen: `Skill 老是不听话？先看这 5 个冷门配置`

## Source Notes

- Agent Skills spec:
  - `SKILL.md` requires YAML frontmatter plus Markdown body.
  - Required fields: `name`, `description`.
  - Optional fields include `license`, `compatibility`, `metadata`, `allowed-tools`.
  - `allowed-tools` is experimental and support may vary between implementations.
  - Progressive disclosure: startup loads only metadata; full `SKILL.md` loads on activation; resources load on demand.
  - Source: https://agentskills.io/specification.md
- Claude Code skills/subagents:
  - Claude Code skills follow the Agent Skills standard and extend it with invocation control, subagent execution, and dynamic context injection.
  - Subagents have isolated context windows, custom prompts, specific tool access, and independent permissions.
  - Built-in subagents include Explore, Plan, and general-purpose.
  - Skill frontmatter supports `context` and `agent`: `context: fork` runs the skill in a forked subagent context; `agent` selects the subagent type when `context: fork` is set.
  - For Skill frontmatter, `context: fork` means the skill content becomes the subagent task; do not conflate it with the `/fork` command that forks the current conversation.
  - The `/fork` current-conversation feature inherits the parent conversation instead of starting fresh.
  - Fork mode can be controlled with `CLAUDE_CODE_FORK_SUBAGENT`.
  - Sources: https://code.claude.com/docs/en/skills.md and https://code.claude.com/docs/en/sub-agents.md
- Codex/OpenAI local skill examples:
  - `agents/openai.yaml` is present in installed skills and carries `display_name`, `short_description`, `default_prompt`, icon metadata, and tool dependencies in some cases.
  - Example: `/Users/yjcjour/.codex/skills/.system/openai-docs/agents/openai.yaml` declares an OpenAI Developer Docs MCP dependency.
  - Example: `/Users/yjcjour/.codex/skills/codex-image-gen/agents/openai.yaml` declares a default prompt and interface copy.
- Local skill corpus:
  - Most installed skills only use `name` and `description` in frontmatter.
  - Some skills use `metadata` for plugin-specific requirements.
  - `allowed-tools` appears in `agent-browser`.
  - `disable-model-invocation` appears in local health/memory guidance as a recommended low-frequency skill behavior, but it is not part of the portable Agent Skills spec.

## Five Configs To Explain

1. `compatibility`:
   - Standard optional Agent Skills field for environment requirements.
   - Use for runtime/tool/workspace assumptions instead of burying them in body text.
2. `allowed-tools`:
   - Pre-approve or constrain tool use for a skill.
   - Useful for repeatable scripts, but support differs.
   - Do not treat it as a security boundary unless the runtime enforces it.
3. `disable-model-invocation` / auto-trigger control:
   - Useful for rare or high-cost skills that should only run when explicitly called.
   - Non-standard extension; mention runtime-specific support.
4. `agent` + `context`:
   - `context: fork` runs the skill content in a subagent context.
   - `agent` selects the subagent type, e.g. `Explore`, `Plan`, `general-purpose`, or custom agents.
   - Distinguish this from `/fork`, which forks the current conversation.
5. `metadata` / `agents/openai.yaml`:
   - Safe place for client-specific metadata, dependencies, ownership, versions, and packaging hints.
   - Best used with namespaced keys to avoid collisions.
   - Runtime adapter files can carry default prompt, display text, icons, and dependency declarations.

## Editorial Judgment

The article should not teach readers to copy random frontmatter fields. The stronger point is:

> Skill is no longer only a prompt file. A mature skill has a control plane: environment, permission, invocation, agent routing, context, and UI/runtime integration.

The practical asset should be a decision table:

| Need | Put it in |
|---|---|
| Environment assumptions | `compatibility` |
| Can this skill run shell/tools | `allowed-tools` or runtime permissions |
| Should this run only manually | invocation policy / runtime extension |
| Which worker should execute it | `agent` |
| Does it need isolated execution context | `context: fork` |
| Does it need UI/default prompt/dependencies | runtime adapter such as `agents/openai.yaml` |

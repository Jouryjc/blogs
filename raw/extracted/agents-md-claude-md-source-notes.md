# AGENTS.md / CLAUDE.md source notes

Created: 2026-04-25

## Source spine

User request: write a WeChat article explaining how to initialize Codex `AGENTS.md` or Claude Code `CLAUDE.md`, with emphasis on continuously optimizing important prompts into these files, based on online practices and in the "码农小余" style.

## High-signal facts

1. OpenAI Codex official docs

- Source: https://developers.openai.com/codex/guides/agents-md
- Codex reads `AGENTS.md` before work and layers global, project, and directory-specific guidance.
- Global guidance lives under `~/.codex/AGENTS.md`; project guidance lives in repo `AGENTS.md`.
- Files closer to the current directory appear later and override broader guidance.
- Default combined project instruction limit is `project_doc_max_bytes = 32 KiB`.
- Official verification prompt: `codex --ask-for-approval never "Summarize the current instructions."`
- Useful framing: do not trust that the file loaded; ask the agent to summarize loaded instruction sources.

2. Anthropic Claude Code memory docs

- Source: https://code.claude.com/docs/en/memory
- `/init` generates a starting `CLAUDE.md`; if one exists, it suggests improvements instead of overwriting.
- Claude can load `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, and `CLAUDE.local.md`.
- `.claude/rules/` supports modular and path-specific rules.
- Task-specific instructions should be skills instead of always-loaded memory.

3. Anthropic Claude Code best practices

- Source: https://code.claude.com/docs/en/best-practices
- Include commands, non-default style rules, testing instructions, repo etiquette, architecture decisions, environment quirks, and common gotchas.
- Exclude what Claude can infer from code, generic language conventions, detailed API docs, volatile information, long tutorials, and file-by-file descriptions.
- Treat `CLAUDE.md` like code: review it when behavior goes wrong, prune regularly, and test whether behavior changes.
- `CLAUDE.md` can import additional files via `@path/to/import`.

4. Claude Help Center guide

- Source: https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts
- `CLAUDE.md` is automatically read at the beginning of a session in that directory.
- Most teams only need a project-root file checked into git.
- Aim for short and signal-dense, roughly under 200 lines.
- Update after `/init`, when Claude gets something wrong twice, when conventions change, and during periodic pruning.

5. Claude power user tips

- Source: https://support.claude.com/en/articles/14554000-claude-code-power-user-tips
- Key practice: anytime Claude does something incorrectly, add it to `CLAUDE.md` so it knows not to repeat the mistake.
- In review feedback, write instructions like: add this to `CLAUDE.md`.
- Verification is the top quality lever: give Claude a way to verify its work.

6. AGENTS.md official site

- Source: https://agents.md/
- `AGENTS.md` is a README for agents, with setup commands, test commands, code style, security considerations, and project-specific rules.
- It is standard Markdown with no required fields.
- Large monorepos can use nested files; closest file wins.
- Treat it as living documentation.

7. GitHub blog analysis

- Source: https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
- GitHub analyzed 2,500+ `agents.md` files.
- Successful files put executable commands early, prefer real examples over abstract explanations, set clear boundaries, specify stack versions, and cover six core areas: commands, testing, project structure, code style, git workflow, boundaries.
- Start minimal and add detail when the agent makes mistakes.

8. Efficiency paper

- Source: https://arxiv.org/abs/2601.20404
- 10 repos / 124 PRs.
- Presence of AGENTS.md associated with lower median runtime by 28.64% and reduced output token consumption by 16.58%.
- Caveat: efficiency result does not prove every context file improves success; content quality matters.

9. Evaluation paper

- Source: https://arxiv.org/abs/2602.11988
- Across multiple agents and LLMs, context files tended to reduce task success rates and increase inference cost by over 20%.
- Authors conclude unnecessary requirements make tasks harder, and human-written files should describe only minimal requirements.
- Important article tension: instruction files are powerful, but bloated files can hurt.

10. Agent Experience article

- Source: https://marmelab.com/blog/2026/01/21/agent-experience
- Agent productivity depends on codebase being agent-friendly, not only prompt quality.
- Dedicated instruction files should briefly explain domain concepts, personas, design principles.
- Agent-friendly repositories expose domain knowledge, improve findability, have testability and guardrails.

11. Software Skeptic article

- Source: https://blog.smallbit.dev/2025/11/27/agents-md-how-to-guide-your-coding-agents/
- Useful mental model: current prompt describes what to do now; AGENTS.md describes how work should be done in this repo.
- Common pitfalls: too much detail, conflicting rules, stale content, assuming every tool auto-loads the file.
- Verify by asking the agent what it learned from AGENTS.md.

## Article thesis

`/init` is not the real work. The real work is building an agent operating manual that compounds: every time the agent guesses wrong, fails to verify, touches the wrong file, uses the wrong command, or violates team style, convert that correction into a short, testable, project-specific rule.

But the file is not a trash can. It should be:

- short enough to actually be used
- specific enough to change behavior
- reviewed like code
- split when scope differs
- linked to deeper docs instead of copying them
- verified through observable agent behavior

## Recommended structure

1. Start with `/init`, but immediately review the generated file.
2. Keep a minimum template:
   - project mental model
   - setup / dev / test / lint commands
   - architecture boundaries
   - style differences from defaults
   - verification requirements
   - hard stops
   - update rules
3. Use a prompt-to-memory loop:
   - correction happens
   - ask whether it is recurring and project-specific
   - add one concise rule
   - run a small future task to verify behavior changes
   - prune quarterly or when stack changes
4. Use split files:
   - Codex nested `AGENTS.md` or `AGENTS.override.md`
   - Claude `.claude/rules/` and `@imports`
   - local/private rules in ignored files
5. Avoid anti-patterns:
   - "write clean code"
   - full API docs pasted in
   - stale commands
   - conflicting old/new rules
   - personal secrets
   - one huge file for every module

## Revision notes

2026-04-25 writing pass:

- Main issue: the first draft used too many isolated short paragraphs, which made the reading rhythm choppy and weakened logical transitions.
- Fix: merge related short sentences into medium-length paragraphs with explicit cause/effect and contrast.
- Added a clearer initialization flow: generate/write file, prune, ask the agent to summarize loaded rules, run a small task, then convert observed drift into rules.
- Strengthened the article logic from "init is not enough" to "init -> verification -> prompt-to-rule loop -> pruning -> layered memory".
- Updated `create-wechat-article/references/xiaoyu-style.md` so future articles avoid mechanical one-sentence paragraphing.

2026-04-25 cover pass:

- Replaced the earlier blue/orange poster-like cover with a cover matching the inline “码农小余知识图解” visual system.
- New cover local path: `outputs/imgs/agents-md-claude-md-cover-knowledge-v2.png`.
- Style rule added to `create-wechat-article`: when inline illustrations use the warm cream/dark navy rounded-card knowledge-graphic style, the cover should reuse the same visual system instead of switching to a separate poster style.

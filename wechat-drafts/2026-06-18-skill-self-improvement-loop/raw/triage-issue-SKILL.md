---
name: triage-issue
description: Triage a newly opened GitHub issue into one of three buckets (ready-to-implement, needs-info, duplicate), apply the matching label, and post a triage comment requesting feedback. Use when a new issue needs triage.
version: 1
tags:
  - type/source
  - topic/agent-skills
  - topic/agent-design
moc:
  - "[[agent-skills]]"
  - "[[agent-design]]"
related:
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/article]]"
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/research-notes]]"
---

# Triage Issue

You are triaging a single GitHub issue. You will be given the repository and issue number. Use the `gh` CLI for all GitHub interactions.

## Skill version

This skill is at **version 1**. Always embed the current version number in the triage comment marker (see below). This version is bumped automatically by the `improve-triage-skill` agent when it revises this skill.

## Steps

1. **Read the issue.**
   ```sh
   gh issue view <number> --repo <owner>/<repo> --json title,body,author,labels,createdAt
   ```

2. **Search for duplicates.** Search open and recently closed issues for similar titles, error messages, or feature requests:
   ```sh
   gh search issues --repo <owner>/<repo> "<key terms from the issue>" --limit 10
   ```
   Compare candidates carefully: a duplicate must describe the same underlying problem or request, not just share keywords.

3. **Classify into exactly one bucket:**
   - `ready-to-implement` — The issue is actionable as written. For bugs: it has reproduction steps (or an obvious cause), expected vs. actual behavior, and enough environment detail to start work. For feature requests: the problem and desired behavior are clear and well scoped.
   - `needs-info` — Required information is missing: no reproduction steps, no environment details, vague description, or unclear scope. The issue cannot be acted on without follow-up from the author.
   - `duplicate` — An existing issue (open or closed) already covers the same problem or request.

4. **Ensure labels exist** (idempotent — ignore "already exists" errors):
   ```sh
   gh label create ready-to-implement --repo <owner>/<repo> --color 0E8A16 --description "Triaged: actionable as written" || true
   gh label create needs-info --repo <owner>/<repo> --color FBCA04 --description "Triaged: waiting on more information" || true
   gh label create duplicate --repo <owner>/<repo> --color CFD3D7 --description "Triaged: duplicate of an existing issue" || true
   ```

5. **Apply exactly one bucket label:**
   ```sh
   gh issue edit <number> --repo <owner>/<repo> --add-label <bucket>
   ```

6. **Post a single triage comment.** The comment MUST:
   - Start with the hidden marker `<!-- oz-triage v:<version> -->` on its own first line, where `<version>` is this skill's version number from the frontmatter.
   - State the chosen bucket and a short, concrete justification (1-3 sentences).
   - For `duplicate`: link the original issue (e.g. `#12`) and explain the match.
   - For `needs-info`: ask 2-4 specific follow-up questions (not generic "please provide more info").
   - End with the feedback footer shown in the template below.

   Comment template:
   ```markdown
   <!-- oz-triage v:1 -->
   ## Triage: `<bucket>`

   <Short justification. For duplicates, link the original issue. For needs-info, list specific questions.>

   ---
   *I'm an automated triage agent. Was this triage correct? React with 👍 or 👎, or reply with a correction — your feedback is used to improve future triage.*
   ```

   Post it with:
   ```sh
   gh issue comment <number> --repo <owner>/<repo> --body-file <tempfile>
   ```

## Rules

- Post exactly one triage comment per issue. If a comment containing `<!-- oz-triage` already exists on the issue, do nothing and stop.
- Apply exactly one of the three bucket labels. Never apply more than one bucket label.
- Do not close issues, even duplicates — leave closing decisions to maintainers.
- Do not edit the issue title or body.
- When genuinely uncertain between `ready-to-implement` and `needs-info`, prefer `needs-info` and ask questions.

## Learned guidelines

<!-- The improve-triage-skill agent appends generalizable lessons here, learned from maintainer feedback. Do not remove this section. -->

(None yet.)

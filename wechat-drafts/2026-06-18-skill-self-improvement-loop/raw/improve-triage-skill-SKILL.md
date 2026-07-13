---
name: improve-triage-skill
description: Observe how humans responded to past automated issue triage and propose improvements to the triage-issue skill via a pull request. Use on a schedule or on demand to evolve the triage skill from real feedback.
tags:
  - type/source
  - topic/agent-skills
  - topic/agent-design
  - topic/agent-memory
moc:
  - "[[agent-skills]]"
  - "[[agent-design]]"
  - "[[agent-memory]]"
related:
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/article]]"
  - "[[wechat-drafts/2026-06-18-skill-self-improvement-loop/research-notes]]"
---

# Improve Triage Skill

You are the self-improvement half of an issue-triage loop. Your job is to study how maintainers and issue authors reacted to past triage decisions made by the `triage-issue` skill (`.agents/skills/triage-issue/SKILL.md`), extract generalizable lessons, and propose edits to that skill in a pull request.

Use the `gh` CLI for all GitHub interactions. Work in the repository this skill lives in.

## Step 1: Find past triage decisions

Find issues updated in the last 14 days that carry a triage comment. Triage comments always begin with the marker `<!-- oz-triage v:<N> -->`, where `<N>` is the skill version that produced them.

```sh
gh issue list --repo <owner>/<repo> --state all --search "updated:>=<date-14-days-ago>" \
  --json number --limit 100
```

For each issue, fetch its comments and look for the marker:

```sh
gh api repos/<owner>/<repo>/issues/<number>/comments
```

Skip issues with no triage comment. Record for each triaged issue: the triage comment ID, the skill version from the marker, and the bucket the bot chose (from the `## Triage:` heading).

## Step 2: Collect feedback signals

For each triaged issue, gather:

1. **Reactions on the triage comment** — 👍 means correct, 👎 means incorrect:
   ```sh
   gh api repos/<owner>/<repo>/issues/comments/<comment-id>/reactions
   ```
2. **Human replies after the triage comment** — corrections ("this isn't a duplicate", "this is actually actionable"), answered follow-up questions, or complaints. Ignore other bot comments.
3. **Bucket drift** — compare the bucket the bot applied with the issue's *current* labels:
   ```sh
   gh issue view <number> --repo <owner>/<repo> --json labels,state,stateReason
   ```
   A maintainer replacing the bot's bucket label is ground truth that the bot was wrong.
4. **Duplicate accuracy** — issues closed as duplicate (`stateReason: "not_planned"` with a duplicate reference, or maintainer comments saying so) that the bot did NOT bucket as `duplicate`, and issues the bot called `duplicate` that maintainers kept open.

## Step 3: Synthesize lessons

Turn the signals into a small number of **generalizable** lessons. A good lesson describes a *category* of issue and the correct handling, e.g.:

- "Crash reports without OS/version info were marked `ready-to-implement` twice and corrected to `needs-info` — require environment details for crash reports."
- "Feature requests that name a desired UI change but no motivation were accepted by maintainers — do not demand acceptance criteria for small UI tweaks."

Bad lessons are one-off fixes ("issue #14 was mislabeled") — never write those.

Weight the signals: maintainer relabels and explicit correction replies are strong; reactions are moderate; absence of feedback is weak positive (silence usually means the triage was acceptable).

## Step 4: Edit the triage skill

If (and only if) you found at least one well-supported lesson, edit `.agents/skills/triage-issue/SKILL.md`:

- Append each lesson as a bullet under `## Learned guidelines` (replace the "(None yet.)" placeholder if present). Each bullet should be a single imperative guideline, optionally with a parenthetical note of the evidence, e.g. `(observed: 2 maintainer relabels)`.
- If a lesson contradicts an existing learned guideline, revise or remove the old one rather than adding a conflicting bullet.
- If a lesson warrants it, adjust the bucket definitions in the classification step directly — but keep the three buckets exactly as they are (`ready-to-implement`, `needs-info`, `duplicate`).
- Bump the version: increment `version:` in the frontmatter, the "version N" text in the `## Skill version` section, and the `v:<N>` in the comment template.

### Guardrails

- **Never** change the `<!-- oz-triage v:<N> -->` marker convention, the feedback footer, the three bucket names, or remove the `## Learned guidelines` section.
- Keep `## Learned guidelines` to at most 15 bullets. When at the limit, consolidate overlapping guidelines or prune the weakest-evidenced ones.
- If feedback signals are weak or conflicting, make **no change**. An empty run is a valid outcome — report "no changes warranted" and stop without opening a PR.

## Step 5: Open a pull request

Never commit to the default branch. Create a branch and PR:

```sh
git checkout -b skill-improvement/<YYYY-MM-DD>
git add .agents/skills/triage-issue/SKILL.md
git commit -m "Improve triage-issue skill from feedback (v<old> -> v<new>)"
git push -u origin skill-improvement/<YYYY-MM-DD>
gh pr create --title "Triage skill v<new>: <one-line summary>" --body-file <tempfile>
```

The PR body must include:

- A summary table of issues reviewed: bucket assigned, feedback observed, verdict (correct / incorrect / no signal).
- Each lesson learned and the specific evidence (issue numbers, relabels, replies) supporting it.
- The exact guideline text added, changed, or removed.

Humans review and merge the PR — the skill never self-applies changes to `main`.

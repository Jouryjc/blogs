# DeepSeek Harness WeChat Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Research DeepSeek's official Harness, produce a reviewed and illustrated Chinese deep-dive, publish it to the WeChat draft box, and verify the remote draft.

**Architecture:** Treat the official repository at a pinned commit as the source of truth, with compact research notes connecting claims to files and URLs. Preserve the first draft, generate a sibling reviewer report and anti-AI publication draft, then use the existing Markdown-first WeChat API path for dry-run, publication, and `draft/get` verification.

**Tech Stack:** Git/GitHub, Markdown/YAML, Python reviewer metrics, Codex image generation, Bun/TypeScript WeChat API tooling, repository knowledge-base scripts.

---

### Task 1: Capture and pin primary sources

**Files:**
- Create: `post-to-wechat/2026-08-13/deepseek-harness/research-notes.md`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/raw/source-manifest.md`

**Step 1: Clone the official repository into a temporary directory**

Run: `git clone --depth 1 https://github.com/deepseek-ai/DeepSeek-Harness.git <temporary-dir>/DeepSeek-Harness`

Expected: the checkout succeeds and `git remote get-url origin` points to the `deepseek-ai` organization.

**Step 2: Record the commit and live repository metadata**

Run: `git -C <temporary-dir>/DeepSeek-Harness rev-parse HEAD` and query GitHub's official repository API.

Expected: a 40-character commit hash plus current repository metadata.

**Step 3: Read architecture evidence**

Inspect the README files, `docs/`, workspace manifests, `packages/core/`, capability packages, Cordis code, licenses, and official release post. Record claim-to-source mappings, not just a source list.

**Step 4: Write the compact source snapshot manifest and research notes**

The manifest must include retrieval date, canonical URLs, commit hash, and selected source-file paths. The research notes must separate confirmed facts, code-derived inferences, author judgments, and facts intentionally excluded.

**Step 5: Verify source hygiene**

Run: `rg -n "third-party Python|Developer Preview|commit|Cordis|plugin" post-to-wechat/2026-08-13/deepseek-harness/{research-notes.md,raw/source-manifest.md}`

Expected: the notes distinguish the official project from the third-party homonym and pin the preview state.

### Task 2: Write the traceable first draft

**Files:**
- Create: `post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness.md`

**Step 1: Generate five title candidates**

Use five distinct sentence patterns and record the candidates in `research-notes.md`; select the title whose first screen can be fulfilled immediately.

**Step 2: Write frontmatter without unstable promotional claims**

Include `title`, `source`, `source_author`, `written_style`, `created_at`, `coverImage`, `summary`, `tags`, `moc`, and `related`.

**Step 3: Draft the article**

Write 4,500–5,500 Chinese characters covering Harness fundamentals, the product/Harness/model layers, Cordis composition, plugin boundaries, long-task control, costs, comparisons, adoption timing, and an actionable checklist.

**Step 4: Check the title promise and evidence boundary**

Run the metrics script and inspect every number, project-state claim, comparison, and inferred mechanism against `research-notes.md`.

Expected: the first 200–300 Chinese characters answer why this is not merely another Claude Code; no unsupported performance ranking appears.

### Task 3: Review and remove AI-smell

**Files:**
- Create: `post-to-wechat/2026-08-13/deepseek-harness/article-review.md`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/article-anti-ai.md`

**Step 1: Run deterministic article metrics**

Run: `python3 .agents/skills/xiaoyu-wechat-article-reviewer/scripts/article_metrics.py post-to-wechat/2026-08-13/deepseek-harness/deepseek-harness.md`

Expected: JSON metrics for title, headings, length, AI-smell hits, reusable assets, judgment, and CTA.

**Step 2: Write the reviewer diagnosis**

Score title promise, first screen, structure, mobile rhythm, technical depth, author judgment, reusable asset, AI-smell, and closing.

**Step 3: Write the optimized sibling draft**

Apply concrete editorial changes while preserving technical claims and the original draft.

**Step 4: Re-run metrics and manually inspect the ending**

Expected: zero unexplained AI-smell hits, explicit author judgment, a useful checklist, and a non-hollow save/follow reason.

### Task 4: Generate and verify four illustrations

**Files:**
- Create: `post-to-wechat/2026-08-13/deepseek-harness/gen-image.md`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/illustrations/deepseek-harness/outline.md`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/illustrations/deepseek-harness/prompts/*.md`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/illustrations/deepseek-harness/*.png`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/imgs/article-cover.png`
- Modify: `post-to-wechat/2026-08-13/deepseek-harness/article-anti-ai.md`

**Step 1: Write the shared visual system and per-image prompts**

Use warm cream paper, navy hand-drawn lines, low-saturation cards, short Chinese labels, and one conclusion per image. Keep the cover's subject and title inside a centered 1:1 safe crop.

**Step 2: Generate images with the Codex image backend**

Run the Codex image generation script once per prompt; require real image files, not successful-looking logs.

**Step 3: Inspect every image**

Check dimensions, aspect ratio, Chinese spelling, hierarchy, technical correctness, thumbnail readability, and cover crop safety. Regenerate only failed images.

**Step 4: Insert image references into the optimized draft**

Expected: one cover in frontmatter and exactly three inline illustration references in the body.

### Task 5: Run WeChat preflight and publish

**Files:**
- Create: `post-to-wechat/2026-08-13/deepseek-harness/publish-dry-run.json`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/publish-result.json`
- Create: `post-to-wechat/2026-08-13/deepseek-harness/draft-readback.json`

**Step 1: Dry-run the optimized Markdown**

Run `wechat-api.ts` with `article-anti-ai.md`, `--dry-run`, `--theme grace`, `--color '#0F4C81'`, and the explicit cover path.

Expected: successful title/summary extraction, correct image count, and zero placeholder images.

**Step 2: Publish the first draft**

Run the same command without `--dry-run` and store the full response.

Expected: `success: true` and a new `media_id`.

**Step 3: Read back the remote draft**

Use the API's draft retrieval path for the new `media_id`.

Expected: one article with the intended title, cover, and three inline images.

### Task 6: Integrate the article into the knowledge base

**Files:**
- Modify: `_kb_build/manifest.json`
- Modify: `wiki/agent-runtime.md`
- Modify: `wiki/agent-design.md`
- Modify: `wiki/INDEX.md`

**Step 1: Add the article manifest entry**

Add only the new first-class article; keep reviewer notes, prompts, images, research notes, and source manifest as production attachments.

**Step 2: Apply tags idempotently**

Run: `python3 _kb_build/apply_tags.py`

Expected: only missing frontmatter relations are added; existing keys remain unchanged.

**Step 3: Add wiki links**

Link the unique article basename from the two topic MOCs and the recent-articles section of `wiki/INDEX.md`.

**Step 4: Verify inventory and links**

Run: `python3 _kb_build/inventory.py` and `python3 _kb_build/link_check.py`.

Expected: the new article is classified and introduces no new dead link; any historical unrelated failures are reported separately.

**Step 5: Review the scoped diff**

Run: `git diff --check` plus a path-scoped status/diff review.

Expected: no whitespace errors, no source-body mutation, no secrets, and no accidental changes to pre-existing user work.

# Codex Harness Architecture WeChat Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Produce a source-traceable, reviewed, illustrated deep dive into the Codex Harness architecture, publish it to the WeChat draft box, and verify the remote draft.

**Architecture:** Use OpenAI's official Harness and App Server materials plus a pinned `openai/codex` source checkout. Preserve the initial draft, reviewer report, and publication version separately; generate all final visuals through Codex image generation; treat mobile preview, API dry-run, and `draft/get` readback as release gates.

**Tech Stack:** OpenAI official documentation, Git/Rust source inspection, Markdown/YAML, Python reviewer metrics, Codex image generation, Bun/TypeScript WeChat API tooling, repository knowledge-base scripts.

---

### Task 1: Capture official sources and pin the code

**Files:**
- Create: `post-to-wechat/2026-08-22/codex-harness/source/source-manifest.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/source/official-snapshot.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/research-notes.md`

**Steps:**

1. Open the official App Server article and linked OpenAI Developers pages; record retrieval date and canonical URLs.
2. Clone `https://github.com/openai/codex.git` into a temporary directory, record `HEAD`, remote URL and relevant source paths.
3. Trace `codex-core`, `codex-app-server`, protocol types, thread/session persistence, tool execution, approval and sandbox boundaries.
4. Write notes under confirmed facts, code-derived inferences, author judgments and excluded claims.
5. Verify each retained protocol name and architecture claim against the official article or pinned source.

Expected: every mechanism used in the article has a direct URL, source path, or clearly labelled inference.

### Task 2: Draft the architecture article

**Files:**
- Create: `post-to-wechat/2026-08-22/codex-harness/title-candidates.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/codex-harness.md`

**Steps:**

1. Generate five title candidates using at least four sentence patterns and select the architecture-first title.
2. Write frontmatter with source, author, date, cover, summary, tags, MOC and related links without changing existing notes.
3. Write 4,500–5,500 Chinese characters following the approved Core → App Server → primitives → event flow → integration-boundary structure.
4. Add an eight-item Harness evaluation checklist and at least three explicit author judgments.
5. Cross-check every named method, event and product boundary against `research-notes.md`.

Expected: the first 200–300 Chinese characters explain why Harness is more than an Agent Loop; no unsupported benchmark or generalization appears.

### Task 3: Run the 蒸馏小余 review gate

**Files:**
- Create: `post-to-wechat/2026-08-22/codex-harness/article-review.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/article-anti-ai.md`

**Steps:**

1. Run `article_metrics.py` on the initial draft and capture the output.
2. Score title promise, first screen, technical depth, paragraph rhythm, author judgment, reusable asset, AI smell and CTA.
3. Write the optimized sibling draft without overwriting the initial article.
4. Re-run metrics and resolve every unexplained AI-smell or CTA warning.

Expected: publication draft remains technically deep, `ai_smell_hits` is empty or documented, and the ending points to the reusable checklist.

### Task 4: Generate and verify four visuals

**Files:**
- Create: `post-to-wechat/2026-08-22/codex-harness/gen-image.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/illustrations/codex-harness/outline.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/illustrations/codex-harness/prompts/*.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/cover-image/codex-harness/cover-prompt.md`
- Create: `post-to-wechat/2026-08-22/codex-harness/imgs/article-cover.png`
- Create: `post-to-wechat/2026-08-22/codex-harness/imgs/01-harness-layers.png`
- Create: `post-to-wechat/2026-08-22/codex-harness/imgs/02-app-server-architecture.png`
- Create: `post-to-wechat/2026-08-22/codex-harness/imgs/03-thread-turn-item.png`

**Steps:**

1. Write the shared cream-paper, navy-outline knowledge-card visual specification.
2. Write one prompt per visual from the optimized article, keeping the cover inside the centered 1:1 safe crop.
3. Generate all four images with the Codex image backend.
4. Inspect dimensions, Chinese text, hierarchy, architecture correctness and mobile readability; regenerate failures only.
5. Insert the three inline images into `article-anti-ai.md`.

Expected: a 2.35:1 cover plus three phone-readable inline diagrams, with no placeholder assets.

### Task 5: Render, preview and publish

**Files:**
- Create: `post-to-wechat/2026-08-22/codex-harness/doocs-wechat-rendered.html`
- Create: `post-to-wechat/2026-08-22/codex-harness/mobile-preview-430px.png`
- Create: `post-to-wechat/2026-08-22/codex-harness/wechat-dry-run.json`
- Create: `post-to-wechat/2026-08-22/codex-harness/publish-result.json`
- Create: `post-to-wechat/2026-08-22/codex-harness/draft-readback.json`

**Steps:**

1. Render `article-anti-ai.md` with Doocs `grace` and classic blue `#0F4C81`.
2. Produce and inspect a 430px preview for image overflow, heading rhythm, list markers, code blocks and color drift.
3. Run `wechat-api.ts --dry-run` with the explicit cover and save the response.
4. Publish a new draft and require `success: true` plus a `media_id`.
5. Call `draft/get` for that `media_id` and verify one article, intended title, cover and three inline images.

Expected: remote readback, not upload logs alone, proves delivery.

### Task 6: Integrate and verify the knowledge base

**Files:**
- Modify: `_kb_build/manifest.json`
- Modify: `wiki/agent-runtime.md`
- Modify: `wiki/agent-design.md`
- Modify: `wiki/claude-code.md`
- Modify: `wiki/INDEX.md`

**Steps:**

1. Add only the main article as a first-class note in the manifest; leave review, prompt and source artifacts outside the knowledge network.
2. Run `python3 _kb_build/apply_tags.py` and confirm existing frontmatter values are preserved.
3. Add the article link to the relevant MOCs and recent articles index without overwriting concurrent user edits.
4. Run inventory, link check, `git diff --check`, and a path-scoped diff review.

Expected: the new article is classified, introduces no new broken links, and unrelated dirty work remains untouched.

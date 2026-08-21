# LMCache / KV Cache WeChat Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn Akshay Pachaar's X Article about KV cache management into a fact-checked, de-AI-smelled 蒸馏小余 article with original Chinese illustrations and a verified WeChat draft.

**Architecture:** Preserve the source capture, build a first-party evidence notebook, and keep the initial article, review report, and publication draft as separate files. Generate all final visuals through Codex image generation, publish the optimized Markdown through the WeChat API, and treat `draft/get` readback as the final delivery proof.

**Tech Stack:** Bun/TypeScript ingestion and WeChat scripts, Markdown/YAML, Python article metrics and preview helpers, Codex image generation, WeChat Official Account Draft API.

---

### Task 1: Capture and verify the X source

**Files:**
- Create: `x-to-markdown/akshay_pachaar/2074502882812952666/your-kv-caching-is-broken.md`
- Create: `x-to-markdown/akshay_pachaar/2074502882812952666/imgs/*`

**Step 1: Confirm authorization and preferences**

Run:

```bash
test -f "$HOME/Library/Application Support/baoyu-skills/x-to-markdown/consent.json"
test -f "$HOME/.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md"
```

Expected: both commands exit `0`; consent is version `1.0` and `download_media: 1` is configured.

**Step 2: Convert the article and download media**

Run:

```bash
npx -y bun .agents/skills/baoyu-danger-x-to-markdown/scripts/main.ts \
  'https://x.com/akshay_pachaar/status/2074502882812952666' \
  --download-media
```

Expected: the command reports a saved Markdown file and local media files under the tweet ID directory.

**Step 3: Verify the capture**

Run:

```bash
rg -n 'Your KV Caching Is Broken|LMCache|CacheBlend' \
  x-to-markdown/akshay_pachaar/2074502882812952666
find x-to-markdown/akshay_pachaar/2074502882812952666/imgs -type f | sort
```

Expected: all three topics are present and downloaded media is non-empty.

**Step 4: Commit the source capture**

```bash
git add x-to-markdown/akshay_pachaar/2074502882812952666
git commit -m "content: capture LMCache X article"
```

### Task 2: Build the first-party evidence notebook

**Files:**
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/research-notes.md`

**Step 1: Create the article workspace**

Run:

```bash
mkdir -p post-to-wechat/2026-08-21/lmcache-kv-cache
```

Expected: workspace exists without modifying any prior article.

**Step 2: Inspect first-party sources**

Check these primary sources and record the access date:

- LMCache GitHub repository and official documentation.
- LMCache architecture, storage backends, observability, integrations, and failure behavior.
- CacheBlend paper and EuroSys 2025 program or proceedings.
- Official Prompt Caching documentation from Anthropic or another provider used as an example.
- Original benchmark pages for any retained `14x`, `4x`, break-even, or cost-saving claim.

Expected: each retained quantitative claim has a URL, workload, hardware/model context, comparison baseline, and limitation.

**Step 3: Write the evidence notebook**

Organize `research-notes.md` into:

```markdown
# Research Notes
## Source spine
## Verified concepts
## Verified benchmark conditions
## Claims removed or downgraded
## Article judgments
## Primary sources
```

Expected: Uber budget, Gartner cancellation rate, Stanford `62%`, and economic claims are either supported by first-party evidence or explicitly marked for removal.

**Step 4: Run an evidence-boundary check**

Run:

```bash
rg -n '62%|14x|4x|2900|29M|Uber|Gartner|15 TB|1%' \
  post-to-wechat/2026-08-21/lmcache-kv-cache/research-notes.md
```

Expected: every match includes a direct source and boundary note; unsupported claims are listed under removal.

**Step 5: Commit the research notebook**

```bash
git add post-to-wechat/2026-08-21/lmcache-kv-cache/research-notes.md
git commit -m "docs: research LMCache KV cache article"
```

### Task 3: Draft the 5-minute distillation

**Files:**
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/title-candidates.md`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache.md`

**Step 1: Write five title candidates**

Create recommended, safe, broad-audience, expert, and contrast candidates. Use at least four sentence patterns and at most one `为什么` title.

Expected: the recommended title leads with Agent context cost and introduces KV Cache as the explanation path.

**Step 2: Write the initial article**

Use this structure:

```markdown
# Agent 上下文越跑越贵，先把 KV Cache 从推理进程里拆出来
## Agent 在为重复上下文付费
## KV Cache 缓存的到底是什么
## Prefix Cache 为何不够
## 进程内缓存也有性能税
## LMCache 把缓存变成独立基础设施
## CacheBlend 处理多文档组合
## 先用这份清单判断值不值得上
```

Expected: 2,500-3,000 Chinese characters, first screen fulfills the title, and the final section provides a collectible decision checklist.

**Step 3: Check factual traceability**

Run:

```bash
rg -n '62%|14x|4x|2900|29M|Uber|Gartner|15 TB|1%' \
  post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache.md
```

Expected: no unsupported claim remains; any benchmark number includes its test conditions.

**Step 4: Commit the initial article**

```bash
git add \
  post-to-wechat/2026-08-21/lmcache-kv-cache/title-candidates.md \
  post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache.md
git commit -m "content: draft LMCache WeChat article"
```

### Task 4: Run the 蒸馏小余 review gate

**Files:**
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/article-review.md`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/article-anti-ai.md`

**Step 1: Measure the initial draft**

Run:

```bash
python3 .agents/skills/xiaoyu-wechat-article-reviewer/scripts/article_metrics.py \
  post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache.md
```

Expected: capture Chinese characters, paragraph count, heading count, image count, AI-smell hits, CTA hits, and warnings.

**Step 2: Write the diagnosis**

Use `@xiaoyu-wechat-article-reviewer` and include:

```markdown
## 总评
## 指标
## 评分
## 具体 AI 味位置
## 优先修改
## 改写目标
```

Expected: the review identifies exact phrases and preserves evidence boundaries.

**Step 3: Produce the optimized sibling draft**

Rewrite title, first screen, headings, author judgment, checklist, and CTA into `article-anti-ai.md`; do not overwrite `lmcache-kv-cache.md`.

**Step 4: Re-run metrics**

Run:

```bash
python3 .agents/skills/xiaoyu-wechat-article-reviewer/scripts/article_metrics.py \
  post-to-wechat/2026-08-21/lmcache-kv-cache/article-anti-ai.md
```

Expected: `ai_smell_hits: []`, `warnings: []`, CTA is tied to the decision checklist, and Chinese character count remains near 2,500-3,000.

**Step 5: Commit the reviewed article**

```bash
git add \
  post-to-wechat/2026-08-21/lmcache-kv-cache/article-review.md \
  post-to-wechat/2026-08-21/lmcache-kv-cache/article-anti-ai.md
git commit -m "content: review LMCache WeChat article"
```

### Task 5: Generate the cover and three Chinese illustrations

**Files:**
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/gen-image.md`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/illustrations/lmcache-kv-cache/outline.md`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/illustrations/lmcache-kv-cache/prompts/*.md`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/cover-image/lmcache-kv-cache/cover-prompt.md`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/article-cover.png`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/01-agent-prefill.png`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/02-prefix-cache-boundary.png`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/03-lmcache-architecture.png`

**Step 1: Write the shared visual specification and prompt files**

Use warm cream paper, dark navy hand-drawn lines, low-saturation note colors, classic blue `#0F4C81`, short Chinese labels, and one conclusion per image. Keep all cover text and the focal workflow inside the centered `1:1` safe area.

**Step 2: Generate each image with Codex**

Run the four prompts:

```bash
node /Users/yjcjour/.codex/skills/codex-image-gen/scripts/generate-image-with-codex.mjs \
  --prompt-file post-to-wechat/2026-08-21/lmcache-kv-cache/cover-image/lmcache-kv-cache/cover-prompt.md \
  --out-dir post-to-wechat/2026-08-21/lmcache-kv-cache/imgs \
  --prefix article-cover \
  --timeout-ms 900000

node /Users/yjcjour/.codex/skills/codex-image-gen/scripts/generate-image-with-codex.mjs \
  --prompt-file post-to-wechat/2026-08-21/lmcache-kv-cache/illustrations/lmcache-kv-cache/prompts/01-agent-prefill.md \
  --out-dir post-to-wechat/2026-08-21/lmcache-kv-cache/imgs \
  --prefix 01-agent-prefill \
  --timeout-ms 900000

node /Users/yjcjour/.codex/skills/codex-image-gen/scripts/generate-image-with-codex.mjs \
  --prompt-file post-to-wechat/2026-08-21/lmcache-kv-cache/illustrations/lmcache-kv-cache/prompts/02-prefix-cache-boundary.md \
  --out-dir post-to-wechat/2026-08-21/lmcache-kv-cache/imgs \
  --prefix 02-prefix-cache-boundary \
  --timeout-ms 900000

node /Users/yjcjour/.codex/skills/codex-image-gen/scripts/generate-image-with-codex.mjs \
  --prompt-file post-to-wechat/2026-08-21/lmcache-kv-cache/illustrations/lmcache-kv-cache/prompts/03-lmcache-architecture.md \
  --out-dir post-to-wechat/2026-08-21/lmcache-kv-cache/imgs \
  --prefix 03-lmcache-architecture \
  --timeout-ms 900000
```

Expected: each call reports `success: true` and at least one real image path; no placeholder fallback is allowed.

**Step 3: Normalize names and inspect dimensions**

Run:

```bash
sips -g pixelWidth -g pixelHeight \
  post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/*.png
```

Expected: cover is approximately `2.35:1`; inline images are approximately `16:9`.

**Step 4: Insert the three inline images**

Add relative `![](imgs/...)` references to `article-anti-ai.md` at the matching conceptual sections.

**Step 5: Commit the final visual assets**

```bash
git add post-to-wechat/2026-08-21/lmcache-kv-cache
git commit -m "assets: illustrate LMCache WeChat article"
```

### Task 6: Render and verify the mobile article

**Files:**
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/doocs-wechat-rendered.html`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/mobile-preview-430px.png`

**Step 1: Dry-render the optimized Markdown**

Run:

```bash
npx -y bun /Users/yjcjour/.agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts \
  post-to-wechat/2026-08-21/lmcache-kv-cache/article-anti-ai.md \
  --theme grace \
  --color '#0F4C81' \
  --cover post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/article-cover.png \
  --dry-run
```

Expected: conversion succeeds, the cover and three local body images are detected, and no unresolved image placeholder remains.

**Step 2: Save or extract the rendered HTML**

Persist the exact dry-run HTML to `doocs-wechat-rendered.html` using the script-supported output path or the returned dry-run artifact; do not hand-edit article content in the HTML.

**Step 3: Verify the theme**

Run:

```bash
rg -n '#92617E' post-to-wechat/2026-08-21/lmcache-kv-cache/doocs-wechat-rendered.html
rg -n '#0F4C81' post-to-wechat/2026-08-21/lmcache-kv-cache/doocs-wechat-rendered.html
```

Expected: no `#92617E` match and at least one `#0F4C81` match.

**Step 4: Capture a 430px preview**

Open the local HTML in a Chromium-based browser at a `430px` viewport and save a full-page screenshot to `mobile-preview-430px.png`.

Expected: no horizontal overflow, broken image, clipped heading, unreadable label, missing ordered-list number, or double bullet.

**Step 5: Commit verified render artifacts**

```bash
git add \
  post-to-wechat/2026-08-21/lmcache-kv-cache/doocs-wechat-rendered.html \
  post-to-wechat/2026-08-21/lmcache-kv-cache/mobile-preview-430px.png
git commit -m "docs: verify LMCache WeChat mobile render"
```

### Task 7: Publish and read back the WeChat draft

**Files:**
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/wechat-dry-run.json`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/publish-result.json`
- Create: `post-to-wechat/2026-08-21/lmcache-kv-cache/draft-readback.json`

**Step 1: Save a clean dry-run result**

Run the API command from Task 6 and save its machine-readable result to `wechat-dry-run.json`.

Expected: success is true, input is `article-anti-ai.md`, cover is present, and body image count is three.

**Step 2: Publish a new draft**

Run:

```bash
npx -y bun /Users/yjcjour/.agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts \
  post-to-wechat/2026-08-21/lmcache-kv-cache/article-anti-ai.md \
  --theme grace \
  --color '#0F4C81' \
  --cover post-to-wechat/2026-08-21/lmcache-kv-cache/imgs/article-cover.png
```

Expected: `success: true`, `updated: false`, and a non-empty `media_id`; save the response to `publish-result.json`.

**Step 3: Read back the exact draft**

Resolve the same configured WeChat credentials without printing them, fetch an access token, read the published `media_id`, and call `draft/get`:

```bash
set -a
source "$HOME/.baoyu-skills/.env"
set +a
WECHAT_ACCESS_TOKEN=$(curl -sS \
  "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${WECHAT_APP_ID}&secret=${WECHAT_APP_SECRET}" \
  | jq -r '.access_token')
PUBLISHED_MEDIA_ID=$(jq -r '.media_id' \
  post-to-wechat/2026-08-21/lmcache-kv-cache/publish-result.json)
jq -n --arg media_id "$PUBLISHED_MEDIA_ID" '{media_id:$media_id}' \
  | curl -sS -X POST \
      -H 'Content-Type: application/json' \
      --data-binary @- \
      "https://api.weixin.qq.com/cgi-bin/draft/get?access_token=${WECHAT_ACCESS_TOKEN}" \
  > post-to-wechat/2026-08-21/lmcache-kv-cache/draft-readback.json
unset WECHAT_ACCESS_TOKEN WECHAT_APP_ID WECHAT_APP_SECRET PUBLISHED_MEDIA_ID
```

Save the response to `draft-readback.json` without storing credentials.

Expected: one article, exact title, non-empty cover URL, three inline WeChat CDN image URLs, and matching summary.

**Step 4: Verify remote image reachability**

Issue HTTP HEAD/GET checks for the read-back cover and inline image URLs.

Expected: every remote asset returns HTTP `200`.

**Step 5: Commit delivery evidence**

```bash
git add \
  post-to-wechat/2026-08-21/lmcache-kv-cache/wechat-dry-run.json \
  post-to-wechat/2026-08-21/lmcache-kv-cache/publish-result.json \
  post-to-wechat/2026-08-21/lmcache-kv-cache/draft-readback.json
git commit -m "docs: record LMCache WeChat draft delivery"
```

### Task 8: Integrate the article into the knowledge base

**Files:**
- Modify: `_kb_build/manifest.json`
- Modify: `wiki/agent-runtime.md`
- Modify: `wiki/context-engineering.md`
- Modify: `wiki/INDEX.md`
- Modify: `post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache.md`

**Step 1: Add the manifest entry**

Register the main article with:

```yaml
tags:
  - type/article
  - topic/agent-runtime
  - topic/context-engineering
  - platform/wechat
moc:
  - "[[agent-runtime]]"
  - "[[context-engineering]]"
related:
  - "[[your-kv-caching-is-broken]]"
  - "[[post-to-wechat/2026-08-21/lmcache-kv-cache/research-notes]]"
```

Expected: existing manifest content and ordering are preserved outside the new entry.

**Step 2: Apply frontmatter tags**

Run:

```bash
python3 _kb_build/apply_tags.py
```

Expected: only allowed frontmatter additions are made; raw source body content remains unchanged.

**Step 3: Update the two topic MOCs and index**

Add the article wikilink to `wiki/agent-runtime.md`, `wiki/context-engineering.md`, and the recent-article section in `wiki/INDEX.md`.

**Step 4: Run knowledge-base validation**

Run:

```bash
python3 _kb_build/inventory.py
python3 _kb_build/link_check.py
git diff --check
```

Expected: the new first-class note is classified and creates no new dead link; report any pre-existing repository warning separately.

**Step 5: Commit the knowledge-base integration**

```bash
git add \
  _kb_build/manifest.json \
  wiki/agent-runtime.md \
  wiki/context-engineering.md \
  wiki/INDEX.md \
  post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache.md
git commit -m "content: index LMCache WeChat article"
```

### Task 9: Final evidence audit

**Files:**
- Verify: `post-to-wechat/2026-08-21/lmcache-kv-cache/*`

**Step 1: Verify all required artifacts**

Run:

```bash
find post-to-wechat/2026-08-21/lmcache-kv-cache -maxdepth 3 -type f | sort
```

Expected: source-linked research, original article, review, optimized article, four images, HTML, mobile preview, dry-run, publish response, and readback are present.

**Step 2: Re-run the final metrics gate**

Run:

```bash
python3 .agents/skills/xiaoyu-wechat-article-reviewer/scripts/article_metrics.py \
  post-to-wechat/2026-08-21/lmcache-kv-cache/article-anti-ai.md
```

Expected: no AI-smell hit or warning remains.

**Step 3: Verify git scope**

Run:

```bash
git status --short
git log --oneline -10
```

Expected: task commits contain only LMCache article assets and intentionally updated knowledge-base files; unrelated user changes remain untouched.

**Step 4: Report completion**

Report the source path, optimized Markdown, review report, illustration directory, cover, rendered HTML, mobile preview, `media_id`, readback checks, metrics, and any residual factual or repository-wide warning.

---
name: xiaoyu-wechat-article-reviewer
description: Review, score, and de-AI Chinese WeChat Official Account drafts for 蒸馏小余 or 码农小余, especially AI Agent engineering articles. Use when asked to 检测 AI 味, 去 AI 味, 优化公众号文章, 检查标题/开头/结构/CTA, 改成蒸馏小余风格, or turn a technical draft into a reader-friendly WeChat article. Not for generic copywriting unrelated to technical WeChat content.
---

# Xiaoyu WeChat Article Reviewer

## Purpose

Turn a technically correct draft into a WeChat article that sounds like a human technical editor for “蒸馏小余”: concrete, opinionated, useful, and not template-like.

Protect this positioning:

> 蒸馏小余：把 AI Agent、AI 编程和工程知识库的前沿内容，蒸馏成开发者能直接用的工作流。

## Inputs

Accept:

- Markdown file path
- pasted draft
- title and outline
- source link plus notes
- optional backend data: sent users, opens, read completion, shares, saves, likes, follows, unfollows

If a Markdown file path is provided, run:

```bash
python3 <skill-dir>/scripts/article_metrics.py <markdown_file>
```

Use metrics as evidence, not as the whole judgment.

## Workflow

1. Classify article type with `references/review-scorecard.md`.
2. Scan for AI smell with `references/anti-ai-smell.md`.
3. Score the draft and identify the top 3 highest-leverage fixes.
4. Rewrite in this order: title, first screen, section headings, practical asset, author judgment, CTA.
5. For direct edits, create an optimized sibling file by default. In this vault, prefer `article-anti-ai.md` for article variants so it stays a production artifact instead of a first-class note. Edit in place only when the user explicitly asks.

## Non-Negotiable Checks

- Title names a reader pain, benefit, conflict, or practitioner scenario.
- First 200-300 Chinese chars show a concrete developer scene, the stakes, the conclusion, and reader fit.
- Every main section advances a specific judgment instead of repeating the abstract thesis.
- The draft contains one reusable object: checklist, template, prompt, table, command block, migration plan, or rubric.
- Personal judgment is visible before the final third: what I would use, avoid, test, or watch.
- CTA is tied to the article asset, not a generic “欢迎关注”.
- Accuracy beats punch. Do not invent benchmarks, official claims, source intent, or author identity.

## Output Contract

For review-only:

```markdown
## 总评
## 指标
## 评分
## 具体 AI 味位置
## 优先修改
## 改写目标
```

For optimization:

- Write a short diagnosis file when useful.
- Write the optimized Markdown file.
- Report paths, metric deltas, and the remaining risks.

## References

- Anti-AI smell patterns: `references/anti-ai-smell.md`
- Review scorecard: `references/review-scorecard.md`


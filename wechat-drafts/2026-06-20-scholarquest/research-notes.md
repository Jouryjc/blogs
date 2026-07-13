---
title: "ScholarQuest 论文编译研究笔记"
source: "https://arxiv.org/html/2606.20235v1"
source_author: "Tingyue Pan, Mingyue Cheng, Daoyu Wang, Yitong Zhou, Jie Ouyang, Qi Liu, Enhong Chen"
created_at: "2026-06-20"
tags:
  - type/source
  - topic/managed-agents
  - topic/agent-design
  - topic/rag
moc:
  - "[[managed-agents]]"
  - "[[agent-design]]"
  - "[[rag]]"
related:
  - "[[wechat-drafts/2026-06-20-scholarquest/article]]"
  - "[[raw/arxiv-2606-20235/github-readme]]"
---

# ScholarQuest 论文编译研究笔记

## Source Capture

- arXiv HTML: https://arxiv.org/html/2606.20235v1
- arXiv PDF: https://arxiv.org/pdf/2606.20235v1
- GitHub: https://github.com/pty12345/ScholarQuest
- Local source HTML: `source.html`
- Local extracted text: `paper-extracted.txt`
- Canonical README capture: `raw/arxiv-2606-20235/github-readme.md`
- Dataset capture: `ScholarQuest.jsonl`, 1111 lines
- Metadata capture: `query_metadata.jsonl`, 13097 lines

## Title Candidates

- 推荐标题：论文 Agent 搜得多还找偏？ScholarQuest 把坑量出来了
- 稳妥标题：ScholarQuest：评测学术搜索 Agent 的新基准
- 大众标题：AI 帮你找论文，为什么还会找偏？
- 专家标题：ScholarQuest 如何评测 Agentic Paper Search
- 反差标题：论文 Agent 的坑，不是没搜索，而是搜偏了

Final choice: 推荐标题。它先抓住读者体感问题，再引出 ScholarQuest。

## One-Screen Thesis

ScholarQuest 的价值不是证明学术搜索 Agent 已经很强，而是把“搜得多但搜偏”的问题量化出来。论文把学术搜索改成多轮任务，提供 1111 条 benchmark 查询、四类研究意图、自动构造答案集和统一 ScholarBase 后端。结果显示 Agentic 方法强于单轮检索，但最好的 PaperScout 整体 Recall@100 也只有 0.314，说明开放文献环境里的论文搜索 Agent 还远没有稳。

## Core Facts

- Paper date/version: arXiv:2606.20235v1, 18 Jun 2026.
- Task: agentic academic paper search in open literature environments.
- Benchmark: ScholarQuest.
- Shared backend: ScholarBase.
- Topic construction:
  - Main paper says over 1000 computer science topics.
  - Appendix gives precise construction: 1682 ACM CCS topics mapped to arXiv CS categories, 1638 retained CS topic seeds, 1111 final high-quality queries after deduplication and filtering.
- Query intent types:
  - method-oriented / method_capability
  - setting-anchored / setting_anchor
  - comparison-based / claim_comparison
  - scope-controlled / scope_control
- Main query distribution in paper:
  - method-oriented: 27.2%
  - setting-anchored: 29.0%
  - scope-controlled: 28.5%
  - comparison-based: 15.3%
- Metadata pool from repo:
  - `query_metadata.jsonl`: 13097 generated and deduplicated records.
  - category counts from local capture: claim_comparison 4052, setting_anchor 3127, method_capability 3056, scope_control 2862.
- Final dataset from repo:
  - `ScholarQuest.jsonl`: 1111 benchmark queries.
  - Released queries keep 5 to 200 final answers.
- GitHub README says Lewen API local deployment covers roughly 3M arXiv papers.

## Benchmark Construction

1. Topic seeds come from ACM CCS and are mapped into arXiv CS categories with Qwen3-Max.
2. Each retained topic seed generates four controlled query types.
3. Queries are deduplicated and filtered for ambiguity, over-breadth, over-narrowness, duplicates, and judgment difficulty.
4. Answer discovery uses 10 rewritten search queries per benchmark query.
5. Retrieval sources include Google Search, arXiv, and Semantic Scholar.
6. Candidate papers are matched to arXiv records, normalized by arXiv ID, and deduplicated.
7. Candidate answers go through recall-oriented prefiltering, LLM-based relevance adjudication, citation expansion, and quality verification.
8. Citation expansion retrieves up to 30 citing papers and all available references per high-confidence seed, with up to 2 hops.
9. Human audit samples 450 query-paper pairs, stratified by automatic relevance score.

## Evaluation Setup

Compared methods:

- ScholarBase retrieval baselines: Dense Retrieval, Hybrid Retrieval.
- External academic search systems: Google Search, Google Scholar, Semantic Scholar, DeepXiv.
- Agentic paper search systems: PaSa, SPAR, PaperScout.

Metrics:

- Recall@25
- Recall@100
- Recall@All
- Tool-use process metrics: rounds, search calls, expansion calls, observed candidates, Recall@100 per 100 candidates.

## Main Numbers

Overall Recall@100:

- Dense Retrieval: 0.208
- Hybrid Retrieval: 0.214
- PaSa: 0.281
- SPAR: 0.270
- PaperScout: 0.314

Overall Recall@All:

- PaSa: 0.310
- SPAR: 0.291
- PaperScout: 0.355

The paper highlights that the best agentic method improves R@100 from 0.214 to 0.314 over the strongest non-agentic baseline, a relative gain of 46.7%.

Intent-level finding:

- Agentic methods work better on method-oriented, setting-anchored, and comparison-based queries.
- Scope-controlled is the hardest category.
- Scope-controlled R@100:
  - Google Search: 0.006
  - Google Scholar: 0.010
  - PaSa: 0.193
  - SPAR: 0.188
  - PaperScout: 0.182

Efficiency:

- PaSa: 60.1 tool calls, 55.1 expansions, 744 observed candidates, 0.051 Recall@100 per 100 candidates.
- SPAR: 47.1 tool calls, 39.1 expansions, 515 observed candidates, 0.064 efficiency.
- PaperScout: 15.3 search calls, 19.0 expansions, 9.2 rounds, 408 observed candidates, 0.120 efficiency.

Common zero-recall failures:

- 20 out of 1111 complete agentic queries, 1.80%.
- Average candidates in common failures:
  - PaSa: 894.6
  - SPAR: 612.9
  - PaperScout: 408.0
- Interpretation: failures are not caused by lack of effort; they are off-target exploration.

Human audit:

- 450 query-paper pairs.
- Pearson correlation 0.867, Spearman 0.867, quadratic weighted Cohen kappa 0.866.
- Score-2 final positives: 86.0% strict precision, 98.7% relaxed precision.

## Reader-Facing Interpretation

- ScholarQuest is not just another retrieval leaderboard. It evaluates whether an academic search agent can keep intent, constraints, and evidence trajectory stable during multi-turn search.
- The benchmark matters for Deep Research-style systems because academic search quality often fails before writing starts: the agent may produce a fluent report from a biased candidate pool.
- The most useful engineering lesson is to record and score process behavior, not only final answer quality.
- Scope-control queries expose a hard failure mode: agents must preserve negative constraints and boundaries, not only chase semantically related papers.
- More tool calls can make errors worse when the initial neighborhood is wrong.

## Article Boundaries

- This is a Chinese compiled explainer, not a full literal translation.
- The article should not claim ScholarQuest covers all disciplines; it is CS/arXiv-grounded.
- Relevance judgment is title/abstract/metadata based, not full-text based.
- Automatically built answers may miss relevant papers.
- GitHub repo currently has no declared license in GitHub API metadata.

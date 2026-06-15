---
title: "Self-hosted Deep Research 研究笔记"
tags:
  - type/source
  - topic/rag
  - topic/knowledge-base
moc:
  - "[[rag]]"
related:
  - "[[wechat-drafts/2026-05-25-self-hosted-deep-research/article]]"
---

# Research Notes

## Title Candidates

1. 推荐标题：Deep Research 最大坑：数据和流程都不在你手里
2. 稳妥标题：Onyx、CrewAI、Voxtral 这套开源 Deep Research 栈怎么判断
3. 大众标题：AI 帮你做研究前，先想清楚资料放在哪里
4. 专家标题：从 Onyx 到 CrewAI：自托管 Deep Research 的三层架构
5. 反差标题：Deep Research 的问题不在模型，而在引用链和权限边界

## Factual Notes

- Original article is an X Article by Akshay Pachaar, published on 2026-04-23, attached to `https://x.com/akshay_pachaar/status/2047395420935229724`.
- Original stack: Onyx for retrieval, CrewAI for orchestration, Voxtral for voice/report narration.
- Onyx GitHub README positions Onyx as an open-source, self-hostable AI platform with RAG, Web Search, code execution, file creation, Deep Research, MCP, custom agents, and 50+ connectors.
- Onyx GitHub README says Deep Research was top of its linked leaderboard as of Feb 2026.
- DeepResearch Bench project page says the benchmark contains 100 PhD-level research tasks across 22 fields and evaluates report quality plus citation effectiveness/accuracy.
- Hugging Face leaderboard captured on 2026-05-25 shows Onyx overall score 54.54, above OpenAI DeepResearch 46.45, Gemini 2.5 Pro DeepResearch 49.71, and Perplexity Research 40.46, but not current overall #1.
- CrewAI homepage describes CrewAI OSS as an open-source orchestration framework for complex agent-driven workflows.
- Hugging Face model card for `mistralai/Voxtral-4B-TTS-2603` identifies it as a Text-to-Speech model, 9 languages, CC BY-NC 4.0 license. Treat it as report narration/TTS unless separate STT tooling is verified.

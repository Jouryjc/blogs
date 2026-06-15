---
title: "Google Agentic RAG research notes"
source: "https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/"
source_author: "Google Research"
created_at: "2026-06-08"
tags:
  - type/source
  - topic/rag
  - topic/managed-agents
  - topic/agent-runtime
related:
  - "[[google-agentic-rag]]"
---

# Google Agentic RAG research notes

## 标题候选

1. 推荐标题：RAG 为什么总漏一跳？Google Agentic RAG 讲清楚
2. 稳妥标题：Google Agentic RAG：从上手到原理
3. 大众标题：让 RAG 自己补证据，Google 新方案怎么做
4. 专家标题：从 Cross-Corpus Retrieval 看 Google Agentic RAG
5. 反差标题：RAG 的问题不在不会答，而在不知道证据不够

最终选择：推荐标题。原因：先抓开发者体感里的“漏一跳”，再引出 Google Agentic RAG，能同时覆盖使用和原理。

## 一手来源

- Google Research：Unlocking dependable responses with Gemini Enterprise Agent Platform's Agentic RAG  
  https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/
- Google Cloud Docs：RAG Engine on Gemini Enterprise Agent Platform overview  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview
- Google Cloud Docs：RAG Engine Cross Corpus Retrieval  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/cross-corpus-retrieval
- Google Cloud Docs：RAG quickstart  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-quickstart
- Google Cloud Docs：Use data ingestion with RAG Engine  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/use-data-ingestion
- Google Cloud Docs：Reranking for RAG Engine  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/retrieval-and-ranking
- Google Cloud Docs：Use the LLM parser  
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/llm-parser
- Google Research：Deeper insights into RAG: the role of sufficient context  
  https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/
- OpenReview：Sufficient Context: A New Lens on Retrieval Augmented Generation Systems  
  https://openreview.net/forum?id=Jjr2Odj8DJ

## 关键事实

- Google Research 在 2026-06-05 发布 Agentic RAG 说明，定位为 Google Research 与 Google Cloud 合作的多 Agent RAG 工作流。
- 公开产品入口是 Gemini Enterprise Agent Platform 上的 Cross-Corpus Retrieval，当前文档称其由后端 Agentic Retrieval 驱动。
- 标准 RAG 的弱点不是完全不会检索，而是面对多源、多跳问题时，第一轮检索可能只找到中间证据，无法继续顺着线索找缺口。
- Google 描述的 Agentic RAG 角色包括 Orchestrator、Planner Agent、Query Rewriter、Search Fanout / RAG Agent、Sufficient Context Agent、Synthesis Agent。
- Sufficient Context 的判断重点不是“片段是否相关”，而是“这些片段是否足够回答原始问题”。这能把“相关但不够”的证据和“足够回答”的证据区分开。
- Google Research 称，与标准 RAG 相比，该框架在 factuality datasets 上准确率最高提升 34%。
- 在 FramesQA 实验里，Cross-corpus 设置加入 4 个候选语料库，Planner 需要选对检索目标。Google 报告 cross-corpus 正确率为 90.1%，与 single-corpus 延迟平均差异在 3% 内。
- RAG Engine 基础流程仍然是数据摄取、转换、embedding、索引、检索、生成。Agentic RAG 是在检索阶段外面增加计划、路由、重写、充分性检查和迭代。
- RAG Engine 支持的输入包括本地单文件上传、Cloud Storage、Google Drive、Slack、Jira、SharePoint 等；Google Drive 等数据源需要给 RAG Data Service Agent 赋权。
- Cross Corpus Retrieval 文档强调创建 corpus 时要写好 `description`，因为系统会依赖这些描述选择合适的 corpus。
- Cross Corpus Retrieval 文档列出两个 API：`AsyncRetrieveContexts` 和 `AskContexts`。文档同时说明该能力当前仅在 `us-central1` 可用。
- RAG quickstart 仍展示单 corpus 的基础用法：创建 corpus、导入文件、设置 chunk size / overlap、用 `retrieval_query` 检索，或者用 `Tool.from_retrieval` 把 RAG corpus 接到 Gemini。
- Reranking 文档区分了低延迟 ranking API 和 LLM reranker。LLM parser 文档说明可用自定义 prompt 让解析更贴合专门文档。

## 写作判断

- 文章不要写成“Google 又发布一个 RAG”。更有价值的角度是：RAG 工程里最烦人的失败，是检索结果看起来相关，但证据链缺一段，模型还会自信写答案。
- 使用部分要明确普通 RAG 与 Agentic RAG 的入口差异：先跑通 corpus 和普通 retrieval，再考虑 cross-corpus / agentic retrieval。
- 原理部分用“证据够不够”而不是“Agent 很聪明”来解释，避免把多 Agent 包装成玄学。
- 边界要写清：小规模、单 corpus、单跳 FAQ 不一定需要 Agentic RAG；跨系统、跨团队、多跳查询才更适合。

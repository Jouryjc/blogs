---
title: "RAG Embedding 和 Rerank 研究笔记"
source: "https://platform.openai.com/docs/api-reference/embeddings"
source_author: "OpenAI / Cohere / Pinecone / Qdrant"
created_at: "2026-06-09"
tags:
  - type/source
  - topic/rag
  - topic/context-engineering
moc:
  - "[[rag]]"
  - "[[context-engineering]]"
---

# RAG Embedding 和 Rerank 研究笔记

## 标题候选

1. 推荐标题：RAG 总找错资料？Embedding 和 Rerank 讲清楚
2. 稳妥标题：RAG 里的 Embedding 和 Rerank 怎么用
3. 大众标题：让 AI 会翻资料：先找一篮子，再挑最靠谱
4. 专家标题：Embedding 召回、Rerank 精排与 RAG 参数配置
5. 反差标题：RAG 的坑不在模型太笨，而在资料没排好队

最终选择：`RAG 总找错资料？Embedding 和 Rerank 讲清楚`

## 一手资料要点

- OpenAI Embeddings API：embedding 是输入内容的向量表示，返回的是 float 数组；向量长度取决于模型。
- OpenAI File Search 默认设置里能看到一套可参考的 RAG 参数：chunk size 800 tokens，chunk overlap 400 tokens，embedding model `text-embedding-3-large` 256 dimensions，最多加入上下文 20 个 chunks，ranker `auto`，score threshold 0。
- OpenAI File Search 的 `chunking_strategy` 有边界：`max_chunk_size_tokens` 在 100 到 4096 之间，`chunk_overlap_tokens` 不能超过 chunk size 的一半。
- OpenAI File Search 的 ranking options 包括 `ranker`、`score_threshold` 和 `hybrid_search.embedding_weight`。score threshold 越高，使用的 chunk 越严格，但可能漏掉相关证据；embedding weight 越高，越偏向语义相似。
- Cohere Rerank：输入 query 和 documents，输出按语义相关性排序的结果；`top_n` 控制返回多少条，结果包含 `relevance_score`。
- Cohere Rerank 4.0/3.5 是单一多语言模型，适合中英文混合知识库。
- Pinecone rerank docs：rerank 是两阶段检索的一部分，先从索引取回一批候选，再用 rerank 模型按 query 与结果的语义相关性重新排序。示例里先取 `top_k: 4`，再 rerank 成 `top_n: 2`。
- Qdrant hybrid reranking：rerank 不应该跑全库，而应该作用在更快方法先取回的一小批候选上；hybrid search 可以先用 dense/sparse 多路召回，再用 late interaction 或 rerank 模型精排。

## 写作主线

- Embedding 不是“理解所有资料”，而是把问题和资料放到同一张语义地图里。
- 向量检索的优点是快，适合先把可能相关的一篮子资料找出来。
- 向量检索的问题是只看“像不像”，不等于“能不能回答原问题”。
- Rerank 是第二道工序：把用户问题和每个候选片段放在一起细读，重新排队。
- 工程上不要把 top_k 调大当万能药。top_k 大能提高召回，但会带来噪音、延迟和上下文成本。
- 更稳的路径是：切块质量 -> embedding 召回 -> hybrid 补关键词 -> rerank 精排 -> score threshold 拒绝低质量证据 -> eval 迭代。

## 参数建议边界

- 没有通用神参。参数要根据文档类型、问题类型、延迟预算和评测集调。
- 初始配置建议：
  - FAQ/短文档：chunk 300-500 tokens，overlap 30-80，top_k 8-15，无 rerank 时传 3-5 条。
  - 技术文档/知识库：chunk 600-900 tokens，overlap 80-160，top_k 20-40，rerank_top_n 4-8。
  - 法务/制度/PDF：chunk 800-1200 tokens，按章节优先，overlap 120-250，hybrid search + rerank，rerank_top_n 5-10。
- 如果正确片段经常在 top 20 里但不在 top 5，应该上 rerank。
- 如果正确片段根本进不了 top 50，先别怪 rerank，应该检查切块、query rewrite、hybrid search 和 embedding model。
- score threshold 不能跨模型照搬；应先记录真实查询分数分布，再用评测集找阈值。

## 参考资料

- OpenAI Embeddings API Reference: https://platform.openai.com/docs/api-reference/embeddings
- OpenAI Assistants File Search: https://platform.openai.com/docs/assistants/tools/file-search
- Cohere Rerank Overview: https://docs.cohere.com/docs/rerank-overview
- Pinecone Rerank Results: https://docs.pinecone.io/guides/search/rerank-results
- Qdrant Hybrid Search with Reranking: https://qdrant.tech/documentation/advanced-tutorials/reranking-hybrid-search/

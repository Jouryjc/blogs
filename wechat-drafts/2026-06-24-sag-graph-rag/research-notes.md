---
title: "SAG 研究笔记"
source: "https://github.com/Zleap-AI/SAG"
created_at: "2026-06-25"
---

# SAG 研究笔记

## 一手来源

- GitHub 仓库：https://github.com/Zleap-AI/SAG
- Benchmark 仓库：https://github.com/Zleap-AI/SAG-Benchmark
- 论文：https://arxiv.org/abs/2606.15971

## 已核对事实

- GitHub API 于 2026-06-25 查询：Zleap-AI/SAG 为 MIT 协议，默认分支 `main`，`stargazers_count=1618`，最近 push 为 `2026-06-18T09:56:30Z`。
- README 定位：SAG 是一个开箱即用的文档检索工作台，上传 Markdown / TXT 后自动处理 chunking、vectorization、event extraction、entity extraction 和 relation organization。
- README 核心结构：`chunk -> event`、`chunk -> entities`、`event <-> entities`。
- README benchmark：HotpotQA / 2WikiMultiHop / MuSiQue 下，平均 Recall@2 从 HippoRAG 2 的 68.14% 到 SAG 的 79.30%；MuSiQue Recall@5 从 65.13% 到 80.04%，换 NV-Embed-v2 后到 81.71%。
- 论文题名：SAG: SQL-Retrieval Augmented Generation with Query-Time Dynamic Hyperedges。
- 论文抽象核心：SAG 不预建全局静态图，而是把每个 chunk 转成 semantically complete event 和 indexing entities，再用 SQL join 在查询时把共享实体的 event 动态连成局部 hyperedges。
- 上手依赖：Node.js 20+、npm、PostgreSQL、pgvector；`docker compose up -d`、`npm install`、`npm run db:setup`、`npm run dev`。
- 默认开发地址：WebUI `http://localhost:5173`，API `http://localhost:4173`。
- 默认模型配置示例：`text-embedding-3-large`、`qwen3.6-flash`、`qwen3-rerank`、`DEFAULT_SEARCH_MODE=fast`。
- MCP 工具：`sag_ingest_document`、`sag_search`、`sag_explain_search`、`sag_get_event`。

## 5 个标题候选

1. 推荐标题：RAG 别再硬塞 chunk：SAG 用「事项+实体」接证据链
2. 稳妥标题：SAG：用 SQL 和轻量图结构做多跳 RAG
3. 大众标题：别再给 RAG 硬塞 chunk，SAG 换了一种找证据的方法
4. 专家标题：SAG 的 Query-Time Dynamic Hyperedges 怎么跑
5. 反差标题：多跳 RAG 的坑不在模型，而在证据怎么连起来

## 写作判断

- 文章入口应该从开发者体感问题切入：多跳问题时 topK 越调越大、上下文越塞越乱。
- 不把 SAG 写成通用 GraphRAG 替代品，而是写成介于普通向量 RAG 和重型知识图谱之间的轻量方案。
- benchmark 必须标注为项目/论文自测，建议读者用自己的语料重测 Recall、延迟和成本。
- 适合强调 Agent 场景，因为高频检索下 Recall@2、上下文噪声和 trace 可观测性都更重要。

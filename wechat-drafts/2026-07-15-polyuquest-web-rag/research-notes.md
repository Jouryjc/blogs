# Research Notes — PolyUQuest: Verifiable Structure-Aware Web RAG over Heterogeneous Graphs

## 源信息

- 论文：PolyUQuest: Verifiable Structure-Aware Web RAG over Heterogeneous Graphs
- arXiv: https://arxiv.org/abs/2607.08269 (cs.AI)
- 提交日期：2026-07-09
- 作者：Ying Liu, Yi Ye, Quanyu Feng, Mingxi Ye, Mingtao Zhang, Haoyang Li, Chen Jason Zhang, Qing Li
- 机构：香港理工大学（PolyU，从系统名与评估站点推断，页面未列出机构）

## 核心问题

现有 RAG 把网页当"扁平文本"（flat text）处理，丢掉了 Web 内容的三层互补结构：

1. **超链接拓扑**（页面之间）— hyperlink topology
2. **DOM 层级**（页面内部）— DOM hierarchy / heading path
3. **跨页实体**（named entities 在多个页面反复出现）

结果：跨页聚合类问题（"哪些教授在做 X 方向"）答不全；保留页内结构的系统（HtmlRAG）又忽略页面间超链接。

## 系统设计

### 异构图（离线构建）

节点四类：𝒱 = 𝒱_P（网页）∪ 𝒱_B（证据块 31,086）∪ 𝒱_E（实体 29,119）∪ 𝒱_T（话题）

边四类：
1. 页面-页面：超链接
2. 页面-块：包含
3. 块-实体：提及
4. 实体-实体/话题：语义关联

块属性：源页面 p(b)、标题路径 h(b)、嵌入 x_b、长度 ℓ(b)、提及实体集 𝒱_E(b)

### 两层路由器（在线）

- 第一层：轻量规则捕获明确结构信号（"which professors" → 模式 C；"admission requirements for" → 模式 B）
- 第二层：LLM 分类器处理长尾查询，输出三种模式置信度

### 三种检索模式

| 模式 | 名称 | 场景 | 机制 |
|------|------|------|------|
| A | Direct Block Retrieval | 单跳事实 | 密集向量 + BM25，交叉编码器重排 |
| B | Navigation Retrieval | 跨页聚合比较 | 查询分解 → 页面检索 → 邻近页扩展 → 全局重排 |
| C | Entity Reasoning | 多跳实体推理 | 提取实体 → 沿关系扩展 → 回溯源块综合评分 |

### 可验证引用（verifiable citation）

每个引用块携带：源页面 + 标题路径（可点击回跳）+ 实体链接；Graph 视图可视化支撑答案的页面/块/实体/话题节点，可扩展相邻节点。

> "Every cited block carries its source page, heading path, and entity links so that users can trace any claim back to its structural evidence."

## 实验

数据集：PolyU 官网，4,240 页面 / 31,086 块 / 29,119 实体 / 37,680 关系，300 个问题。

| 系统 | Corr. | Cov. | Faith. | Q.Token | B.Token |
|-----|-------|-------|--------|---------|---------|
| ChunkRAG | 0.532 | 0.479 | 0.710 | 2,947 | — |
| HtmlRAG | 0.453 | 0.448 | 0.804 | 4,009 | — |
| FastGraphRAG | 0.295 | 0.469 | 0.737 | 4,484 | 28.1M |
| LightRAG | 0.610 | 0.612 | 0.559 | 29,825 | 37.4M |
| **PolyUQuest** | **0.644** | **0.649** | **0.921** | **2,968** | **17.5M** |

要点：
- Faithfulness 0.921，比有据率次佳的 HtmlRAG（0.804）高约 12 个百分点；比正确性最强的基线 LightRAG（0.559）高约 36 个百分点
- Query token 2,968 ≈ ChunkRAG 水平，约为 LightRAG 的 1/10
- Build token 17.5M ≈ LightRAG（37.4M）的 47%
- 消融：去掉 DOM 块 → Corr. -8.1 / Cov. -13.9；去掉跨页导航 → Corr. -2.0 / Cov. -1.6

## 局限

- 最适合"组织型网站"：大学、政府、医院、企业官网（知识分布在链接页面 + 层级章节 + 复现实体中）
- 迁移到新域需重新爬取 + 域特定实体 schema（索引/路由/检索/可验证机制可复用）
- 依赖高质量 HTML 结构与链接拓扑；实体抽取消歧质量影响模式 C
- 仅在 PolyU 单站点评估，泛化未充分验证

## 补充背景（第二轮研究）

- GraphRAG 生态：微软 GraphRAG 开创 LLM 抽实体建图路线；LightRAG（HKU）与 FastGraphRAG 是轻量化后继，但建图/查询 token 成本仍高 —— 论文数据佐证（LightRAG 建图 37.4M token）
- HtmlRAG（2024）：保留页面内 HTML/DOM 结构进 LLM，代表"页内结构"路线，但不处理页面间超链接
- NodeRAG（arXiv 2504.11544）：同样使用异构节点图做 RAG，但面向通用文档，不是 Web 三层结构；说明"异构图 RAG"是当前活跃方向
- 相关资源：Awesome-GraphRAG（github.com/DEEP-PolyU/Awesome-GraphRAG，同为 PolyU 团队维护）

## 标题候选（蒸馏小余 2.0）

1. 推荐：RAG 一问官网就翻车？坑不在模型，而在网页被拍平成纯文本
2. 稳妥：网页不是纯文本：PolyUQuest 用一张异构图让 RAG 的每句话可溯源
3. 大众：为什么 AI 问答一到官网就胡说？这篇论文把网页结构找回来了
4. 专家：超链接 + DOM + 实体三层合一：PolyUQuest 的结构感知 Web RAG 拆解
5. 反差：GraphRAG 不是太弱，是太贵：PolyUQuest 用 1/10 token 拿到更高有据率

最终选择：候选 1（推荐）。

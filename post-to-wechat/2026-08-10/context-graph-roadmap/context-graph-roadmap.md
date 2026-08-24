---
title: "RAG 找到 Redis，却答不出谁会挂：用 Context Graph 接起依赖链"
source: "https://x.com/0xMorlex/status/2086754640968732729"
source_author: "Morlex (@0xMorlex)"
written_style: "蒸馏小余 2.0"
created_at: "2026-08-10"
coverImage: "imgs/article-cover.png"
summary: "RAG 能找到提到 Redis 的片段，却不一定能接起跨文档依赖链。用 9 步搭一张可遍历、可引用的 Context Graph。"
tags:
  - type/article
  - topic/rag
  - topic/context-engineering
  - topic/knowledge-base
  - platform/wechat
moc:
  - "[[rag]]"
  - "[[context-engineering]]"
  - "[[knowledge-base]]"
related:
  - "[[post-to-wechat/2026-08-10/context-graph-roadmap/research-notes]]"
  - "[[x-to-markdown/0xMorlex/2086754640968732729/from-rag-to-context-graphs-the-9-step-roadmap]]"
---

# RAG 找到 Redis，却答不出谁会挂：用 Context Graph 接起依赖链

你问知识库：“Redis 挂了，会影响哪些系统？”

普通 RAG 很可能给你一段“Token Cache 由 Redis 提供后端”的文档。检索没错，答案却没出来。真正要找的是另一条跨文档的依赖链：

```text
登录流程 -> 认证服务 -> Token Cache -> Redis
```

这类问题的难点不在“有没有搜到 Redis”，而在“能不能沿着关系继续走”。如果答案散在四份互不引用的文档里，再大的 embedding 模型也不会凭空补出中间三跳。

Morlex 把解决路线压成了 9 步：不再只召回 passage，而是把实体做成节点、关系做成边、答案做成一条带来源的路径。

先给结论：**单跳事实查询继续用 RAG；跨文档依赖、影响分析和因果链，再考虑 Context Graph。**

![](imgs/source-rag-vs-graph.jpg)

## 先别建图，先找出 RAG 答不出的那类问题

Context Graph 的第一步不是选图库，也不是让 LLM 扫完整个知识库，而是收集失败查询。

“Redis 的默认端口是多少”是单跳查找。只要相关片段被召回，模型就能回答。

“Redis 挂了，哪些业务会受影响”则是多跳问题。它实际上在问：谁依赖某个服务，那个服务又依赖谁，链条最终是否落到 Redis。

可以用一个很朴素的判断：

- 最难的问题是找一个事实：继续优化 chunk、metadata 和 reranker。
- 最难的问题是沿依赖链找影响范围：图结构开始有价值。
- 两类问题都存在：保留向量检索，用图补关系，不要二选一。

Microsoft GraphRAG 的 Local Search 也不是丢掉原始文本，而是把知识图谱中的实体关系与原始 text chunks 一起送进检索上下文。工程上更常见的是混合方案，而不是“RAG 已死”。

## 第一层：Extract，把文本变成能连接的三元组

### 1. 用失败查询定义关系

先写出你要支持的问题，再反推最小关系集合。

如果目标是故障影响分析，第一版可能只需要：

- `depends_on`：A 依赖 B
- `backed_by`：A 的后端是 B
- `runs_on`：A 运行在 B 上
- `owned_by`：A 由 B 团队负责

关系越多，抽取和评估越难。第一版只选一个关系类型，反而更容易验证价值。

### 2. 抽取实体和关系，不急着做 embedding

原文用确定性正则演示三元组抽取：

```python
PATTERNS = [
    (r"(.+?) depends on (.+)", "depends_on"),
    (r"(.+?) is backed by (.+)", "backed_by"),
]

# 每条边都带 source_chunk_id，后面才能引用原文
Triple(subject, relation, object, source_chunk_id)
```

生产环境通常会用 LLM 或信息抽取模型，但输出契约不变：主语、关系、宾语、来源。`source_chunk_id` 不能等到最后再补，因为它决定每一跳能否回到原始证据。

### 3. 做实体归一化，否则图会碎掉

`The Auth Service`、`auth service` 和 `AuthService` 对人类是同一个服务，对图数据库却可能是三个节点。

一旦别名没有合并，边都在，路径还是断的。最小实现至少需要：

- 大小写与空白归一化
- 冠词、标点清洗
- 显式 alias 表
- 无法自动确认的实体进入人工复核队列

这一步看起来不性感，却常常决定图检索到底能不能返回结果。

![](imgs/source-extract.jpg)

## 第二层：Connect，让每条边都带“收据”

### 4. 同时构建正向边和反向边

“A 依赖什么”要沿正向边查，“什么依赖 A”要沿反向边查。

可以分别维护两张邻接表：

```python
forward[subject].append((relation, object, source))
reverse[object].append((relation, subject, source))
```

存两份方向会增加一点内存，但能避免每次影响分析都全图扫描。对依赖图来说，这笔交换通常值得。

### 5. 多个来源支持同一条边，就提高权重

两份独立文档都说“认证服务依赖 Token Cache”，这条边比单一来源更可信。

最简单的做法，是把相同的 `subject + relation + object` 合并，并记录来源集合。权重可以先等于独立来源数，后续再叠加文档可信度、更新时间和抽取置信度。

但要注意：十份互相复制的文档不是十个独立证据。来源去重比单纯计数更重要。

### 6. provenance 必须挂在边上

Context Graph 最有用的产物不是一张漂亮关系图，而是一条能核对的路径：

```text
登录流程 -depends_on-> 认证服务    [c1]
认证服务 -depends_on-> Token Cache [c2, c8]
Token Cache -backed_by-> Redis     [c3]
```

模型得到的不再是一堆“可能相关”的片段，而是三条关系、三组出处和一条明确链路。

**没有 provenance 的图，只是把未经核对的断言换了一个包装。**

![](imgs/source-connect.jpg)

## 第三层：Traverse，检索路径而不是段落

### 7. 从实体出发，取 k-hop 邻域

问题里提到 Redis，就从 Redis 节点开始走。`k=1` 找直接依赖者，`k=2` 再找上游，直到达到跳数、节点数或置信度上限。

这里必须设预算。没有边界的图遍历会迅速把无关节点塞回上下文，最后又变成另一种“长文本墙”。

### 8. 排路径，不排 passage

故障影响分析可以从 Redis 沿反向边做 BFS：

```python
queue = [("redis", ["redis"])]

while queue:
    node, path = queue.pop(0)
    for upstream in reverse[node]:
        queue.append((upstream, path + [upstream]))
```

候选答案不再是 Top-K 文档，而是一组路径。排序时至少考虑：

- 路径是否完整
- 每条边的来源数量与可信度
- 跳数是否过长
- 关系类型是否符合问题
- 路径上的证据是否过期或冲突

### 9. 只把相关子图交给模型

最终上下文应该包含三样东西：路径上的节点、连接节点的边、每条边对应的原始片段。

LLM 的任务因此被缩小了：它不再负责从一堆 chunk 里猜哪些事实能连接，只负责读取已经连好的证据链，解释“谁会受影响、为什么、证据在哪里”。

![](imgs/source-traverse.jpg)

## 一张 9 步落地清单

如果要在团队里做 PoC，我会按下面顺序推进：

1. 收集 20-50 个当前 RAG 失败的真实问题。
2. 标注哪些是单跳、哪些是多跳。
3. 只选一个高价值关系，例如 `depends_on`。
4. 定义三元组 Schema 和来源字段。
5. 建实体 alias 表，并记录人工合并率。
6. 同时写入正向边和反向边。
7. 给每条边保留来源、时间和置信度。
8. 先实现一个有跳数预算的 BFS / k-hop 查询。
9. 用路径正确率、引用完整率和无答案拒答率评估，而不是只看回答是否顺口。

这套 PoC 的验收标准也应该提前写清楚：普通 RAG 的单跳准确率不能明显退化；多跳问题要能返回完整路径；每一跳都能打开原始证据；图中没有路径时，系统必须敢于说不知道。

## Context Graph 不是所有知识库的下一站

图索引有明确成本：LLM 抽取、实体消歧、关系更新、冲突处理、图存储和评估都要付账。Microsoft GraphRAG 官方仓库也提醒，索引可能昂贵，应该从小规模开始。

我暂时不建议三类团队直接上图：

- 知识库主要回答 FAQ 和单文档事实；
- 实体命名极不稳定，又没人维护 alias；
- 还没有一组真实失败查询，只是因为“GraphRAG 很火”想重构检索。

相反，如果你的高价值问题集中在服务依赖、组织责任、合规追踪、事件影响、跨文档调查，图会把“模型猜关系”变成“系统查路径”。

原文用八个单事实 chunk 做了一个演示：普通检索找到了 Redis 那句话，图遍历则返回登录链路和每一跳引用。这是一个说明结构差异的最小实验，不是通用 benchmark。

最稳妥的路线不是推翻 RAG，而是让两种检索各做擅长的事：**向量检索负责找相关文本，Context Graph 负责接起关系链。**

![](imgs/source-takeaway.jpg)

如果你正在做企业知识库或 Agent 记忆，建议先把文中的 9 步清单收藏下来，再拿最近 20 个失败问题做一次“点还是链”的标注。这个结果会比任何框架选型更早告诉你，团队到底需不需要一张图。

关注「蒸馏小余」，下一篇我会继续拆：Context Graph 的评估集应该怎么做，才能避免图看起来很满、答案仍然不可靠。

## 参考资料

- [Morlex：From RAG to Context Graphs](https://x.com/0xMorlex/status/2086754640968732729)
- [Microsoft GraphRAG Query Engine](https://microsoft.github.io/graphrag/query/overview/)
- [Microsoft GraphRAG Repository](https://github.com/microsoft/graphrag)
- [GraphRAG paper](https://arxiv.org/abs/2404.16130)

---
title: "论文 Agent 搜得多还找偏？ScholarQuest 把坑量出来了"
source: "https://arxiv.org/html/2606.20235v1"
source_author: "Tingyue Pan, Mingyue Cheng, Daoyu Wang, Yitong Zhou, Jie Ouyang, Qi Liu, Enhong Chen"
author: "蒸馏小余"
written_style: "蒸馏小余 2.0"
created_at: "2026-06-20"
coverImage: "imgs/article-cover.png"
summary: "ScholarQuest 把学术论文搜索 Agent 放进开放文献环境里评测：1111 个查询、四类研究意图、统一 ScholarBase 后端，结论是 Agent 确实更强，但最大坑是搜偏。"
tags:
  - type/article
  - topic/managed-agents
  - topic/agent-design
  - topic/rag
  - platform/wechat
moc:
  - "[[managed-agents]]"
  - "[[agent-design]]"
  - "[[rag]]"
related:
  - "[[wechat-drafts/2026-06-20-scholarquest/research-notes]]"
  - "[[raw/arxiv-2606-20235/github-readme]]"
---

# 论文 Agent 搜得多还找偏？ScholarQuest 把坑量出来了

先说结论：ScholarQuest 不是在证明学术搜索 Agent 已经可以替代 Google Scholar，而是在提醒我们，当前 Agent 最大的问题不是“不搜索”，而是“很努力地搜偏”。

这篇 2026 年 6 月 18 日提交到 arXiv 的论文，把学术论文搜索做成了一个更接近真实研究流程的 benchmark：给 Agent 一个研究问题，让它多轮搜索、检查、扩展候选论文，最后交出一组相关论文。

结果很有意思。Agentic 方法确实强于单轮检索，最好的 PaperScout 整体 Recall@100 从最强非 Agent baseline 的 0.214 提到 0.314。但 0.314 也意味着，在开放文献环境里，论文搜索 Agent 还远远谈不上稳。

更值得看的不是排行榜，而是失败原因：论文里共同零召回的失败案例只有 20 个，占 1111 个查询的 1.80%，但这些案例非常刺眼。PaSa、SPAR、PaperScout 都看了不少候选论文，最后还是一个金标准答案都没捞到。问题不在于工具调用太少，而在于初始方向错了，后面的检索和引用扩展只是在错误邻域里越走越远。

![论文 Agent 搜得多还找偏？ScholarQuest 把坑量出来了](imgs/article-cover.png)

## 真正要评测的，不是第一屏列表

传统学术搜索更像一次性排序：输入 query，系统返回一个 ranked list。BM25、embedding 检索、混合检索都属于这类路径。它们可以很快，也适合关键词明确的问题，但遇到细粒度研究意图时会变脆。

比如：

- 哪些论文研究了“基于 microservices 的 IT architecture”？
- 哪些论文在“医疗行业语境”下评估 IT architecture？
- 哪些论文声称 microservices 架构优于 monolithic designs？
- 我想找 IT architecture 论文，但排除 legacy systems 范围。

这四个问题看起来都和 IT architecture 有关，但搜索动作完全不同。第一个偏方法，第二个偏场景，第三个偏比较结论，第四个偏范围约束。

Agentic paper search 的目标，是让模型不只返回第一屏结果，而是能自己决定：什么时候改写 query，什么时候检查一篇论文，什么时候沿着引用关系扩展，什么时候停止。

![从一次性检索到多轮论文搜索](imgs/search-eval-shift.png)

所以 ScholarQuest 评测的不是“哪个搜索框更像 Google”，而是“一个论文搜索 Agent 能不能在多轮探索里保住研究意图”。

这对 Deep Research 类产品很关键。报告写得流畅不代表研究链路可靠。如果前面的候选论文池已经偏了，后面的总结、引用和分析都会在一个看似合理但错误的邻域里打转。

## ScholarQuest 先把问题控制住

ScholarQuest 的设计思路很朴素：要评测 Agent，先别让 query 本身乱飞。

论文从 ACM Computing Classification System 里收集主题，再把主题映射到 arXiv 的 CS 分类。正文里说覆盖 1000+ 计算机主题，附录给了更精确的构造数字：从 1682 个 ACM CCS topic 出发，保留 1638 个 CS topic seed，最后经过去重和质量过滤，得到 1111 个高质量查询。

每个主题会生成四类研究意图：

| 意图类型 | 读者可以理解成 | 典型搜索难点 |
|---|---|---|
| Method-oriented | 找使用某种方法的论文 | 方法名可能有同义表达 |
| Setting-anchored | 找特定场景下的论文 | 场景词容易被弱化 |
| Comparison-based | 找支持某个比较结论的论文 | 要识别 claim，而不只是主题相似 |
| Scope-controlled | 找满足范围限制的论文 | 要保留排除条件和边界 |

![四类研究意图不是四种问法，而是四种约束](imgs/four-intents.png)

这个设计比“随机找一些人类问题”更可控。因为评测者知道每个 query 本来想考什么，也能观察 Agent 是在哪一类意图上失守。

GitHub 仓库里也放出了数据：`ScholarQuest.jsonl` 有 1111 条最终 benchmark 查询，`query_metadata.jsonl` 有 13097 条生成和去重后的 query metadata。README 里还写明，最终数据集保留的是有 5 到 200 个相关答案的查询。

这点很重要。论文搜索不是问答题。很多研究问题天然对应一组论文，而不是一个唯一答案。只看 top-1 或单篇命中，很难判断 Agent 有没有真的覆盖研究空间。

## ScholarBase 让所有方法在同一个考场里跑

Agent benchmark 最怕比较条件不一致。

一个系统接 Google Scholar，另一个系统接私有索引，第三个系统还能用额外 citation API，最后分数差异就很难解释：到底是 Agent 好，还是工具更强？

ScholarQuest 这篇论文把环境也一起做了。它提供 ScholarBase 作为统一检索后端，基于 S2 PaperData 快照保留 arXiv 论文、摘要、元数据和引用关系。仓库 README 里提到，构造时使用的 Lewen API 本地部署大约覆盖 300 万篇 arXiv 论文。

ScholarBase 支持几类动作：

- sparse retrieval：基于 SQLite FTS5 的 BM25。
- dense retrieval：基于 BGE-M3 的标题-摘要 embedding。
- hybrid retrieval：用 RRF 合并 sparse 和 dense 排名。
- paper inspection：查论文元数据和详情。
- citation/reference traversal：沿引用和参考文献扩展。

![ScholarQuest 的构造流水线](imgs/construction-pipeline.png)

这样 PaSa、SPAR、PaperScout 这些 Agentic 方法，以及 Dense、Hybrid、Google Search、Google Scholar、Semantic Scholar、DeepXiv 等 baseline，至少是在同一组答案和相近检索目标下比较。

这也是 ScholarQuest 比普通论文检索评测更有价值的地方：它不仅看最后召回了哪些论文，还看 Agent 怎么搜、调用了多少工具、观察了多少候选、每 100 个候选换来多少 Recall@100。

## 结果：Agent 更强，但离可靠还很远

主表里最关键的一组数字，是整体 Recall@100。

| 方法 | Overall Recall@100 |
|---|---:|
| Dense Retrieval | 0.208 |
| Hybrid Retrieval | 0.214 |
| PaSa | 0.281 |
| SPAR | 0.270 |
| PaperScout | 0.314 |

如果只看相对提升，PaperScout 很漂亮。论文也明确说，最好的 Agentic 方法把 R@100 从 0.214 提到 0.314，相对提升 46.7%。

但换个角度看，0.314 也很克制。它说明多轮搜索、引用扩展、自主工具调用确实有帮助，但还没有把开放文献搜索变成稳定能力。

更有信息量的是效率分析。

PaSa 平均 60.1 次工具调用，其中 55.1 次是 expansion，观察 744 个候选，Recall@100 per 100 candidates 只有 0.051。SPAR 平均 47.1 次工具调用，观察 515 个候选，效率是 0.064。

PaperScout 的模式不一样。它平均有 9.2 轮交互，15.3 次 search call，19.0 次 expansion，观察 408 个候选，效率达到 0.120。

这个结果说明，Agent 搜索不是工具调用越多越好。更强的路线不是盲目扩展候选池，而是让每一次 search 和 expansion 都服务于当前研究意图。

## 最大坑在 scope-control

四类意图里，scope-controlled 最难。

它要求 Agent 一边找相关主题，一边保住排除条件、范围限制、细粒度边界。人类读起来不复杂，但对多轮搜索 Agent 来说很容易失真。

论文里的 scope-controlled R@100 很直观：

| 方法 | Scope-controlled R@100 |
|---|---:|
| Google Search | 0.006 |
| Google Scholar | 0.010 |
| PaSa | 0.193 |
| SPAR | 0.188 |
| PaperScout | 0.182 |

Agent 比传统搜索好很多，但这仍然是所有类别里最弱的一档。

原因不难理解。正向线索容易追，负向边界难保留。

“找使用强化学习做视频摘要的论文”是一类任务。“找某类论文，但排除某个范围、不要某类方法、只保留某个语境”是另一类任务。后一类需要 Agent 持续记住约束，并在每次 query rewrite、citation expansion、candidate filtering 时重新检查。

如果没有显式的 constraint ledger，负约束很容易在多轮工具调用中被磨掉。

## 搜偏之后，努力会放大错误

论文最有价值的一段，是 failure analysis。

共同零召回失败只有 20 个查询，但它们揭示了一个很工程化的问题：Agent 不是没干活，而是干了很多无效活。

这些失败查询里，PaSa 平均观察 894.6 个候选，SPAR 是 612.9，PaperScout 是 408.0。结果三个 Agent 都没有召回任何金标准答案。

![搜偏以后，引用扩展会放大错误邻域](imgs/off-target-exploration.png)

这就是开放文献搜索里很危险的局部最优。

一开始的 query rewrite 如果偏向了一个语义上相似、但约束上错误的方向，后续检索会返回一批看起来相关的论文。Agent 再沿着这些论文的引用关系扩展，就会得到更多同一邻域里的论文。候选池变大了，证据看起来变多了，但离正确答案没有更近。

对用户来说，最麻烦的是这种失败很难被肉眼发现。报告可能有引用、有表格、有流畅叙述，只是底层证据空间从一开始就偏了。

## 对研究 Agent 的工程启发

如果要把 ScholarQuest 的结论用到自己的 Deep Research 或论文搜索 Agent 里，我会先改五件事。

第一，把用户意图拆成显式字段。

不要只存一句自然语言 query。至少拆成 topic、method、setting、comparison claim、scope boundary、negative constraints。Agent 每次改写搜索词之前，都要重新看这些字段。

第二，把负约束当一等公民。

scope-control 的失败说明，排除条件不是附属信息。它应该进入候选过滤、引用扩展和最终报告检查，而不是只在第一轮 prompt 里出现一次。

第三，记录搜索轨迹，而不是只记录结果。

ScholarQuest 之所以有诊断价值，是因为它看 tool calls、rounds、observed candidates、per-candidate recall efficiency。自己的 Agent 也应该记录：每次 search 为什么发生，query 从哪来，扩展 seed 为什么被选中。

第四，给“搜偏”设置早停信号。

如果候选池越来越大，但新增候选都来自同一个主题邻域，或者和原始约束的重合度越来越低，Agent 应该暂停，而不是继续扩展。更好的动作可能是回到意图字段，重新生成一组覆盖不同角度的 query。

第五，把答案构造和报告写作分开。

先让一个阶段负责找全候选、去重、按约束过滤，再让另一个阶段负责写报告。不要让写作 Agent 一边找一边写，否则它会很自然地把早期错误当成文章主线。

这也是我看完 ScholarQuest 后最想带走的结论：论文搜索 Agent 的瓶颈，不只是模型聪不聪明，而是有没有把“研究意图保持”做成可检查的工程对象。

## 这篇论文的边界也要看清

ScholarQuest 做得很扎实，但它不是最终答案。

第一，它主要覆盖计算机科学主题，并且是 arXiv-grounded 的开放文献环境。医学、法律、社科、专利、工业报告这类资料形态不在同一个分布里。

第二，相关性判断主要基于标题、摘要和元数据，而不是全文证据。这样可以规模化，但遇到只在正文里出现的细粒度 claim，仍然可能漏掉。

第三，答案集是自动构造加人工审计，不是穷尽式人工标注。论文的人工审计质量不错：最终高置信正例有 86.0% strict precision 和 98.7% relaxed precision。但开放文献环境里，漏标风险永远存在。

所以更合理的用法，是把 ScholarQuest 看成一个诊断台，而不是终局排行榜。

它告诉我们：Agentic paper search 确实比单轮检索更有潜力，但真正难的是在多轮搜索里保住意图、约束和证据方向。

如果你的 Agent 只是“多搜几次、多扩展几篇引用”，它可能会变得更忙，而不是更准。

原论文：https://arxiv.org/html/2606.20235v1

代码与数据：https://github.com/pty12345/ScholarQuest

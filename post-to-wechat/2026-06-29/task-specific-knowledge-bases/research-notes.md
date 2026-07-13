---
title: "Task-specific knowledge bases 论文研究笔记"
source: "https://arxiv.org/abs/2606.27237"
source_author: "Amit Elhelo, Amir Globerson, Mor Geva"
created_at: "2026-06-29"
tags:
  - type/source
  - topic/knowledge-base
  - topic/agent-memory
  - topic/context-engineering
moc:
  - "[[knowledge-base]]"
  - "[[agent-memory]]"
  - "[[context-engineering]]"
related:
  - "[[post-to-wechat/2026-06-29/task-specific-knowledge-bases/task-specific-knowledge-bases]]"
---

# Task-specific knowledge bases 论文研究笔记

## 一手来源

- arXiv abstract: https://arxiv.org/abs/2606.27237
- arXiv PDF: https://arxiv.org/pdf/2606.27237
- 官方代码仓库: https://github.com/amitelhelo/TaskInvariance

说明: 论文正文写了会 release code and data，但截至 2026-06-29，本地访问到的 GitHub README 仍是 "coming soon!"。

## 论文信息

- 标题: LMs as Task-Specific Knowledge Bases: An Interpretability Analysis
- 作者: Amit Elhelo, Amir Globerson, Mor Geva
- 机构: Tel Aviv University, Google Research
- arXiv v1: 2026-06-25
- 核心问题: 大模型参数是否像传统知识库一样，对同一个事实提供单一事实源，还是会按任务格式存成不同参数编码。

## 标题候选

1. 推荐标题: 别把模型当统一知识库：同一事实，换问法就换参数
2. 稳妥标题: 大模型的事实知识，可能按任务格式分开存
3. 大众标题: 模型答对一次，不代表它真的稳定记住了
4. 专家标题: Task-invariance 被破坏：LM factual knowledge 的任务特异参数编码
5. 反差标题: 知识编辑漏网，问题可能不在编辑，而在事实分散存储

Chosen: `别把模型当统一知识库：同一事实，换问法就换参数`

## 文章主线

这篇论文挑战的是 "LMs as knowledge bases" 的常见比喻。传统知识库应该有 single source of truth: 问 "What is the capital of France?"、选择题、判断题，都应该从同一事实源返回 Paris。

论文发现，大模型更像按任务格式维护了多个局部知识库:

- 行为层面: 一个事实在一种任务上学会了，不会稳定同步到其他任务。
- 参数层面: 同一个事实在不同任务上的表现，可以被定位到不同 attention heads / MLP neurons 子集。
- 推理层面: CoT 有时能恢复直接回答拿不到的知识，原因之一是它会动用评估任务之外的任务特异编码。

## 关键事实

- 行为实验使用 OLMo-3-7B IT 的 105 个训练检查点。
- 数据来自 5 类关系，每类下采样到 46 个事实，共 230 个事实。
- 6 种任务: COMPLETION, FITB, OPENQA, MCQA, NEGMCQA, VERIFICATION。
- Co-emergence 假设: 如果一个事实已经在某任务上出现，且目标任务本身已经 competent，那么这个事实应当也在目标任务上出现。
- 结果: 1,031 个可测试 fact-task pair 里，47.9% 没有按预期 co-emerge。阈值换成 0.4 / 0.8 时结果仍接近，分别为 50.9% / 49.2%。
- 统计检验: fact-task interaction 在每个 checkpoint 都显著，最终模型中解释 23% 方差。
- 机制实验模型: OLMo-2-7B IT, OLMo-2-13B IT, Gemma-2-9B IT。
- 机制实验通过 binary mask 定位 attention heads 和 MLP neurons，要求 mask 对目标 fact-task pair 同时满足 necessary, sufficient, specific。
- 代表性结果: 在 official language 数据集 + OLMo-2-7B IT 上，目标任务 diagonal drop 为 29%-89%，同事实其他任务和同任务其他事实基本保持，off-diagonal / bottom row 均 ≤8%。
- Sufficiency: 对同一组合，patch 局部组件激活后，目标 pair 恢复率 69%-102%。
- 纠缠度: 判别任务 MCQA / VERIFICATION / NEGMCQA 的平均 Enttask 为 0.21，生成任务 OPENQA / FITB / MULTI-HOP 为 0.11。
- Co-emergence 来源差异: 判别任务作为来源时，对非 VERIFICATION 目标的 co-emergence rate 只有 3%-42%；生成任务作为来源时为 40%-90%。
- CoT 消融: 消融目标任务自己的编码时，direct accuracy 下降 20%-72%，CoT 只下降 12%-30%；消融其他任务编码时，direct 最多下降 8%，CoT 下降 11%-31%。

## 可写作判断

1. 对 Agent 工程来说，最重要的不是 "模型有没有知识"，而是 "同一个事实在生产会遇到的问法里是否一致"。
2. 单一格式评测会高估事实可靠性。只测 OpenQA、只测选择题、只测判断题，都可能漏掉另一个任务格式下的存储路径。
3. Knowledge editing / unlearning 不能只验证一个 prompt family。单一任务格式被改掉，不代表其他格式也被改掉。
4. CoT 不是单纯 "更聪明"，它可能是在绕路访问其他任务特异编码。直接回答失败时，CoT 有机会救回来；但这也说明知识访问并不干净。
5. 外部知识库、RAG、Agent memory 的工程价值仍然存在: 它们提供显式 single source of truth，而不是把事实一致性赌在参数空间里。

## 原论文图片

- `imgs/figure-1-task-invariance.png`: Figure 1, 传统知识库与语言模型的 task-invariance 对比。
- `imgs/figure-4-localization-heatmap.png`: Figure 4, 参数定位必要性与特异性热力图。
- `imgs/figure-5-cot-ablation.png`: Figure 5, CoT 与直接回答在同任务 / 跨任务消融下的表现。

图片均从原论文 PDF 渲染裁切，未重绘数据。

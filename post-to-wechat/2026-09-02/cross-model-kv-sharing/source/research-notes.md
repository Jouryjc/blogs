---
title: "跨模型 KV 共享工程解读研究笔记"
source: "https://arxiv.org/abs/2608.30963v1"
source_author: "Yi Li、Dongming Jiang、Yi Zhao、Bingzhe Li"
created_at: "2026-09-02"
tags:
  - type/source
  - topic/prompt-caching
  - topic/agent-runtime
  - topic/context-engineering
moc:
  - "[[prompt-caching]]"
  - "[[agent-runtime]]"
  - "[[context-engineering]]"
related:
  - "[[post-to-wechat/2026-09-02/cross-model-kv-sharing/cross-model-kv-sharing]]"
  - "[[post-to-wechat/2026-09-02/cross-model-kv-sharing/source/paper-source]]"
  - "[[post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache]]"
  - "[[post-to-wechat/2026-08-30/llm-cache-four-layers/llm-cache-four-layers]]"
---

# 跨模型 KV 共享工程解读研究笔记

## 研究问题

同一段系统提示、对话历史、检索证据或工具输出，在模型路由、升级、校验和多 Agent 协作中常被多个模型反复读取。现有 prefix cache 通常只能让同一个模型复用自己的 KV；模型一换，目标模型仍要从 token 开始做 prefill。

论文提出的系统判断是：如果多个模型处理同一上下文，理解这段上下文的计算不一定要由每个模型各做一遍。

## 方法主线

传统路径：

`共享上下文 → 模型 A prefill → A 的 KV`，切换模型后再执行 `同一上下文 → 模型 B prefill → B 的 KV → decode`。

论文路径：

`共享上下文 → 模型 A prefill → A 的 KV → T(A→B) 翻译 → B 可消费的 KV → 模型 B decode`。

翻译不是 tensor reshape。模型可能在层数、hidden representation、attention 配置、KV head、tokenizer 和模型家族上都不同。目标也不是逐元素复刻原生 `KV_B(C)`，而是生成一个足以让 B 继续推理、且质量可接受的兼容状态。

论文用 learned transport module 描述实际实验路径，目标模型保持冻结。正文给出两类可能的目标：最小化 translated KV 与 native target KV 的表示距离，或直接优化下游输出、attention、logits、任务准确率。但论文没有公开实际 transport module 的网络结构、训练超参数、训练步数、loss 组合、训练数据规模和模型对扩展方式。

## 三组实验及准确口径

### 同家族：Qwen2.5-7B → Qwen2.5-1.5B

- transport module 用 NoLiMa prompts 训练。
- 在 116 个计分 LongBench2 样本上，用 A/B/C/D log-probability scoring 评估。
- Qwen2.5-7B 原生：45.69%。
- Qwen2.5-1.5B 原生：27.59%。
- 7B → 1.5B handoff：34.48%。
- handoff 比原生 1.5B 高 6.89 个百分点，回收了 1.5B 与 7B 准确率差距的 38.1%，但仍低于 7B 原生。
- 8K–16K：27 个样本，handoff 准确率 40.74%；16K–32K：89 个样本，32.58%。长区间下降 8.16 个百分点。
- 8K–16K：1.5B 原生 prefill 158.7 ms，handoff 34.5 ms；16K–32K：288.3 ms 对 53.8 ms。
- 每个长度区间的 latency 只测了 3 个样本。
- 翻译、peer copy、assembly 三个可归因组件合计分别为 14.8 ms 和 20.3 ms，低于 handoff 总耗时 34.5 ms 和 53.8 ms；论文承认 runtime integration、同步及其他开销仍未被完整归因。

### 跨家族、相近规模：Qwen2.5-1.5B → Gemma-2-2B

- 输入来自 FineWeb-Edu，prompt 长度覆盖 128、1K、4K。
- 128 tokens：Gemma prefill 5.492 ms，handoff 3.007 ms，减少 45.25%。
- 1K：40.105 ms 对 16.081 ms，减少 59.90%。
- 4K：181.706 ms 对 59.897 ms，减少 67.04%。
- 论文摘要写 67.05%，表 5 与正文写 67.04%；写作采用表格值并不放大差异。
- perplexity 并非每个 horizon 都更优。H=1、32、128 时 handoff 略好于 Gemma native；H=16、512 时更差。H=512 为 14.037 对 13.574。
- 这组实验支持“翻译后的跨家族状态可用”，不支持“跨家族完全无质量损失”。

### 跨家族、10 倍规模差：Llama3.1-70B → Qwen2.5-7B

- Llama 原生：准确率 44.0%，latency 7,328 ms。
- Qwen 原生：准确率 45.7%，latency 899 ms。
- Llama → Qwen handoff：准确率 44.0%，latency 138 ms。
- handoff 相对目标原生快约 6.5 倍，同时低 1.7 个百分点；论文换算为保留目标原生准确率的 96.3%。
- 138 ms 只计算复用“已经存在的”Llama KV 后的 handoff，不包含 70B 模型最初的 7,328 ms prefill。
- 论文没有在实验设置中清楚列出这组 multiple-choice accuracy 的数据集名称、样本数、硬件与重复次数。

## 最重要的工程边界

1. **不是免费生成 KV。** 只有源 KV 本来就因业务流程存在，handoff 延迟比较才有意义。为了转给目标模型而先跑一次昂贵源 prefill，可能得不偿失。
2. **不是一个万能 translator。** 论文使用 `T(A→B)` 与具体模型对实验，没有证明任意模型自动兼容。模型数上升后可能出现模型对管理、训练与版本升级成本。
3. **不是只看平均质量。** 长上下文准确率下降、不同 decoding horizon 的 perplexity 波动，都要求按任务和长度设置质量闸门，并保留 native prefill fallback。
4. **不是端到端生产 benchmark。** 论文未完整披露硬件、吞吐、并发、batching、缓存命中率、网络拓扑、存储成本、translator memory footprint 与多租户隔离。
5. **KV 是高敏感运行时状态。** 跨模型、跨 worker、跨环境搬运 KV 会带来权限、租户隔离、加密、失效与版本绑定问题；这是从生产系统推导出的工程风险，论文没有评估安全性。

## 小余工程判断（不是论文已验证结论）

优先试点场景：固定少量模型对、共享长上下文、模型切换频繁，而且源 KV 本来就存在，例如小模型路由后升级、大模型生成后小模型校验、固定模型组合的多 Agent 流水线。

暂不适合直接上生产的场景：短 prompt、模型对经常变化、跨供应商黑盒 API、严格数据隔离、多版本频繁滚动，或无法容忍质量波动的关键任务。

落地评审应至少回答五问：

1. 源 KV 是否本来就存在，真实命中率是多少？
2. 每个模型对是否需要独立 translator，升级后如何失效与重训？
3. 质量闸门看 accuracy、perplexity 还是业务成功率？
4. 端到端账单是否包含 source prefill、translation、copy、assembly、调度和存储？
5. 哪些情况立即 fallback 到 target native prefill？

## 写作红线

- 不写“所有模型都能共享同一份 KV”。
- 不把 `Universal` 写成已经完成的任意模型即插即用。
- 不写“延迟降低 85%”而省略“源 KV 已存在”的前提。
- 不把 138 ms 与 899 ms 写成完整请求端到端耗时。
- 不写“零质量损失”；必须同时给出 44.0% 对 45.7% 以及长上下文下降。
- 不把 116 个计分样本或每桶 3 个 latency 样本推广成生产定论。
- 不虚构 transport module 结构、训练配方、硬件或开源代码。

---
title: "跨模型 KV 共享论文事实快照"
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
  - "[[post-to-wechat/2026-09-02/cross-model-kv-sharing/source/research-notes]]"
---

# 跨模型 KV 共享论文事实快照

## 元信息

- 论文：A Universal Context-Reuse Layer for Cross-Model KV Sharing
- 作者：Yi Li、Dongming Jiang、Yi Zhao、Bingzhe Li
- 机构：University of Texas at Dallas
- arXiv：2608.30963v1
- 首次提交：2026-08-31 15:28:17 UTC
- 分类：cs.LG、cs.AI
- 许可：CC BY 4.0
- 摘要页：https://arxiv.org/abs/2608.30963v1
- PDF：https://arxiv.org/pdf/2608.30963v1
- 论文列出的演示：https://youtu.be/0TiOdUK0qB8
- 本地 PDF：`arxiv-2608.30963.pdf`
- 本地 arXiv 页面：`arxiv-2608.30963.html`
- 本地 arXiv 源码包：`arxiv-2608.30963-source.tar`

## 摘要性事实

论文研究跨模型 KV sharing：源模型已经对一段上下文完成 prefill 后，用一个 learned transport module 把源 KV 状态翻译到目标模型的表示空间，让冻结的目标模型直接从翻译后的状态开始 decode，不再独立重算整段目标侧 prefill。

实验覆盖一组同家族迁移和两组跨家族迁移：Qwen2.5-7B-Instruct → Qwen2.5-1.5B-Instruct、Qwen2.5-1.5B-Instruct → Gemma-2-2B-IT，以及 Llama3.1-70B → Qwen2.5-7B。

论文将这一方向概括为 `context mobility`：KV 不只是一份绑定单模型的临时缓存，也可能成为可存储、传输、翻译并由另一模型消费的计算状态。

## 必须保留的口径

- 所有 handoff latency 都是“源 KV 已经存在”之后的增量成本，不包含源模型为了传输而做的 prefill。
- `899 ms → 138 ms` 只属于 Llama3.1-70B → Qwen2.5-7B 的论文实验设置；准确率是 `45.7% → 44.0%`，不是零损失。
- Qwen2.5-7B → Qwen2.5-1.5B 的 LongBench2 结果基于 116 个计分样本；1.5B 原生为 27.59%，handoff 为 34.48%，7B 原生为 45.69%。
- Qwen2.5-1.5B → Gemma-2-2B 的 `67.04%` 来自 4K prompt 下 181.706 ms 对 59.897 ms 的增量延迟比较。摘要写 67.05%，正文表 5 写 67.04%，公众号稿采用表格的 67.04%，并说明四舍五入口径差异。
- 论文标题里的 `Universal` 更适合解读为通用的 serving abstraction。论文没有证明一个 translator 可以在任意模型对之间即插即用。

## 取证时间

本快照依据 2026-09-02（Asia/Singapore）访问的 arXiv v1 摘要页、PDF 与官方源码包整理。公众号稿只对该版本负责。

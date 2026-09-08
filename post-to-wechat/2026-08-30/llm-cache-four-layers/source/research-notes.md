---
title: "LLM 四层缓存：原文校正与一手资料核验"
source: "https://x.com/_avichawla/status/2093265776266637739"
source_author: "Avi Chawla"
author: "蒸馏小余"
created_at: "2026-08-30"
tags:
  - type/source
  - topic/prompt-caching
  - topic/agent-runtime
  - topic/context-engineering
  - topic/rag
moc:
  - "[[prompt-caching]]"
  - "[[agent-runtime]]"
  - "[[context-engineering]]"
  - "[[rag]]"
related:
  - "[[kv-prefix-prompt-and-semantic-caching-in-llms-clearly-exp]]"
  - "[[post-to-wechat/2026-08-30/llm-cache-four-layers/llm-cache-four-layers]]"
  - "[[post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache]]"
---

# LLM 四层缓存：原文校正与一手资料核验

## 选题判断

Avi Chawla 的原文把 KV Cache、Prefix Cache、Prompt Cache 和 Semantic Cache 放在同一张地图里，最有价值的不是又解释一次“缓存能省钱”，而是说明四种同名机制优化的并不是同一笔账。

更准确的分类是：前三层都在不同作用域复用 KV 状态，Semantic Cache 则绕过模型、复用已经生成的回答。前三层精确复用失败，通常损失的是 prefill 时间和输入费用；Semantic Cache 错误命中，会把旧答案直接交给当前用户。

这篇文章与 2026-08-21 的 LMCache 文章区分开：旧文讨论跨进程、多层存储和 CacheBlend；本篇讨论四层缓存对象、作用域、命中条件、失败后果，以及上线前如何排查。

## 可采用的一手事实

### Transformers v5 KV Cache

- Transformers v5 把缓存暴露为可传递的 `Cache` 对象，常见策略包括 `DynamicCache`、`StaticCache` 与 `QuantizedCache`，也支持显式通过 `past_key_values` 复用。
- KV Cache 避免重复计算历史 token 的 K/V，但新 token 仍需读取并关注已有 K/V；不能写成“每步计算变成 O(1)”。
- `DynamicCache` 是通用文档里的常见策略，但 v5 允许模型定义自己的默认缓存；需要确定行为时应显式配置。
- KV 量化可能影响数值结果，并不属于“完全正确性中性”的精确复用。

来源：

- https://huggingface.co/docs/transformers/v5.15.1/kv_cache
- https://huggingface.co/docs/transformers/v5.15.1/cache_explanation
- https://github.com/huggingface/transformers/blob/v5.15.1/MIGRATION_GUIDE_V5.md

### vLLM Prefix Caching

- vLLM 当前 stable 配置中的默认 block size 为 16，但模型、后端与 `prefix_match_unit` 都可能改变物理块或匹配粒度，正文只能写“当前默认配置为 16”。
- 前缀键由父块哈希、当前 token IDs 与额外身份信息组成；额外信息可能包括 LoRA、多模态输入和租户级 `cache_salt`。
- Prefix Cache 主要减少 prefill 和 TTFT，不直接减少新 token 的 decode。
- 多租户部署应使用不可预测、租户范围稳定的 salt，避免共享前缀缓存形成时序侧信道。

来源：

- https://docs.vllm.ai/en/stable/api/vllm/config/cache/
- https://docs.vllm.ai/en/stable/design/prefix_caching/
- https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/
- https://docs.vllm.ai/en/latest/usage/security/

### Anthropic Prompt Caching

- 默认 5 分钟缓存写入按基础输入价的 1.25 倍计费，1 小时写入按 2 倍计费，缓存命中及刷新按 0.1 倍计费。
- 折扣只覆盖命中的输入前缀；变化后缀、普通输入和输出 token 仍按各自价格计算。
- 命中要求缓存边界前的内容 100% 相同，顺序是 `tools → system → messages`。
- 每个断点最多回看 20 个 API 内容块，最多可定义 4 个断点；这里的“内容块”不是 vLLM 的 16-token block。
- 缓存存在模型相关的最短 token 门槛；不足时请求仍成功，但不会产生缓存命中。

来源：

- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching

### Semantic Cache

- 通用流程是：查询 embedding → 向量 Top-K → 相似度或重排门槛 → 命中后直接返回旧回答；未命中才调用模型并写回缓存。
- 相似不等于答案可复用。否定词、数字、权限、版本、套餐、日期和多轮上下文变化都可能造成错误命中。
- 阈值没有跨模型、跨业务的通用值；生产指标应关注错误命中率和“有效命中率”，而不只是 hit rate。
- 缓存命名空间至少要覆盖租户、模型、Prompt 版本、知识版本与安全策略；动态数据还需要 TTL 和主动失效。
- NDSS 2026 已展示针对语义缓存的投毒攻击，Agent、代码生成与 SQL 场景需要额外防护。

来源：

- https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/semantic-caching-overview.html
- https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/semantic-caching-best-practices.html
- https://github.com/zilliztech/GPTCache
- https://aclanthology.org/2023.nlposs-1.24/
- https://learn.microsoft.com/en-us/azure/cosmos-db/gen-ai/semantic-cache
- https://www.ndss-symposium.org/wp-content/uploads/2026-f200-paper.pdf

## 原文需要校正的表达

1. “四种缓存存四种对象”改为“三种 KV 状态复用范围，加一条响应复用旁路”。
2. “vLLM 固定使用 16-token block”改为“当前默认配置为 16，实际取决于版本、模型与后端”。
3. “Prompt Cache 命中后整次请求只花 10%”改为“命中的输入前缀按 0.1 倍计费”。
4. “截断工具输出能保持前缀一致”改为“任何历史改写都会从修改点起使后续前缀失效”。
5. “RAG 文档换序后完全没有复用”改为“复用在第一处顺序分歧停止，之前稳定部分仍可能命中”。
6. “Semantic Cache 阈值可以照抄”改为“阈值必须结合流量、风险与错误命中评测确定”。
7. CacheBlend 的 2.2–3.3 倍 TTFT 改善属于限定模型与数据集的论文结果，不写成通用 SLA。

## 最终写作边界

- 不把局部输入折扣写成总成本折扣。
- 不把 Prefix Cache 命中写成 Decode 加速。
- 不把精确 KV 复用与近似 KV 量化混为一谈。
- 不宣传单一命中率或通用相似度阈值。
- 不重复介绍 LMCache 架构，只在 related 中保留溯源关系。

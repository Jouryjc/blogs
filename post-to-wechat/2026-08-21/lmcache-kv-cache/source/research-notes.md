---
title: "LMCache 与 KV Cache 复用：一手资料核验"
source: "https://x.com/akshay_pachaar/status/2074502882812952666"
author: "蒸馏小余"
created_at: "2026-08-21"
tags:
  - type/source
  - topic/agent-runtime
  - topic/context-engineering
  - topic/prompt-caching
moc:
  - "[[agent-runtime]]"
  - "[[context-engineering]]"
  - "[[prompt-caching]]"
related:
  - "[[x-to-markdown/akshay_pachaar/2074502882812952666/your-kv-caching-is-broken]]"
  - "[[post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache]]"
---

# LMCache 与 KV Cache 复用：一手资料核验

## 选题判断

原始 X Article 抓住了一个值得写的工程问题：Agent 在多轮执行中会反复提交系统提示词、工具定义、历史消息与检索材料，重复 prefill 会拉高首 token 等待时间。可写方向不应是“KV Cache 能省 90% 成本”的营销承诺，而应回答三个更实用的问题：

1. Provider 的 Prompt Cache 已经能解决什么；
2. 为什么自托管、多进程、长上下文服务仍会遇到复用边界；
3. 什么负载值得引入 LMCache，什么负载先别引入。

## 可采用的一手事实

### Anthropic Prompt Caching

- 官方定价页当前给出的倍数：5 分钟缓存写入为基础输入价的 1.25 倍，1 小时写入为 2 倍，缓存读取为 0.1 倍。按价格计算，5 分钟缓存命中一次即可抵消额外写入成本，1 小时缓存需要两次命中。
- 官方 Prompt Caching 文档要求可复用段完全一致，并按 `tools → system → messages` 的层级组成前缀。前方内容变化，会让后续缓存失效。
- 缓存只改变输入处理，模型输出生成本身不受影响。

来源：

- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context

### LMCache 当前架构

- 官方文档把 LMCache 定义为独立于推理引擎生命周期的 KV Cache 层，可在 CPU、SSD 与远端存储之间分层保存和复用 KV。
- MP 模式以独立服务运行，多个 vLLM 进程向同一服务注册，共享主机内存中的缓存池。它处理的是进程内缓存分片、工作集超出 HBM 后无法共享的问题。
- 官方列出的能力还包括异步写入/预取、可插拔存储与传输、PD 分离，以及通过 CacheBlend 做非前缀复用。
- 2026-04 官方基准：8×H100、Qwen3-235B-A22B、8 路数据并行、多轮会话负载下，LMCache MP 相比进程内 offload 的平均 TTFT 为 0.29 秒对 3.98 秒，p99 为 1.30 秒对 13.55 秒，平均解码速度为 37.47 对 9.81 token/s。只能作为该配置下的结果，不能外推成通用“14 倍”。
- 2026-05 官方 MI300X 基准给了重要反例：8 用户、32K 上下文的低负载阶段，HBM Prefix Cache 完成 52 个请求，LMCache 完成 25 个；工作集能放进 HBM 时，L2 搬运的开销可能不划算。在 32 用户、100K 上下文的压力阶段，LMCache 才明显占优。

来源：

- https://docs.lmcache.ai/
- https://docs.lmcache.ai/v0.3.7/developer_guide/architecture.html
- https://docs.lmcache.ai/mp/architecture.html
- https://blog.lmcache.ai/en/2026/04/03/lmcaches-new-architecture-boosts-moe-inference-performance-by-10x/
- https://blog.lmcache.ai/en/2026/05/12/benchmarking-lmcache-for-multi-turn-agentic-workloads-on-amd-mi300x/
- https://github.com/LMCache/LMCache

### CacheBlend

- EuroSys 2025 论文指出，简单拼接分别缓存的多个文档 KV，会丢失跨文档注意力；从头重算质量稳定，但 TTFT 代价高。
- CacheBlend 只重算一小部分受影响 token，再把它们与已缓存 KV 混合。论文报告的经验值是重算少于 15% 的 token 往往能保持接近完整重算的质量，这不是所有模型和任务的保证。
- 在论文测试的 3 个开源模型与 3 组数据集上，CacheBlend 相比完整重算和 Prefix Cache 基线，TTFT 改善 2.2–3.3 倍，吞吐提高 2.8–5 倍。文章须同时写明测试边界。

来源：

- https://www.microsoft.com/en-us/research/uploads/prod/2024/09/eurosys25-final999.pdf
- DOI: 10.1145/3689031.3696098

## 不采用或降级表达的原文说法

以下说法未在可核验的一手资料中找到匹配证据，正文不使用：

- “Stanford 研究发现 62% Agent 输入是重复内容”；
- “Uber 四个月花完 2026 年 AI 预算”；
- “Gartner 预计 40% Agent 项目只因成本超支取消”；
- “单张 MI300X 每天产生 15TB KV Cache”；
- “1% 命中率即可回本”与“某公司一年省 2900 万美元”；
- “TurboQuant 3-bit 零精度损失，但拖慢推理 20%”；
- 不带硬件、模型、并发和基线的“LMCache 普遍提速 14 倍”。

## 写作边界

- 不把 KV Cache 命中等同于总 Token 消失。它跳过一段重复输入的 prefill；新增输入与输出 token 仍需处理。
- 不把 Prefix Cache 写成“只要历史增长就失效”。增长发生在稳定前缀之后时，前缀仍可命中；问题主要出在前缀变化、文档顺序变化与非前缀片段组合。
- 不把独立缓存服务写成免费加速。必须讨论搬运、序列化、网络、容量、淘汰、哈希一致性、降级与可观测性成本。
- 不给统一命中率阈值。建议先记录 p50/p95 TTFT、复用 token 占比、命中率、缓存读取耗时、prefill 耗时、存储与网络开销，再决定是否引入。

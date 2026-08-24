---
title: "GPU 推理性能补充研究"
source: "https://x.com/akshay_pachaar/status/2087928032904523980"
tags:
  - type/source
  - topic/agent-runtime
moc:
  - "[[agent-runtime]]"
related:
  - "[[how-a-gpu-actually-works]]"
  - "[[gpu-inference-memory-bandwidth]]"
---

# GPU 推理性能补充研究

## 写作切口

把原文从“GPU 硬件入门”重组为 LLM 工程师的性能诊断框架：小批量 Decode 为什么经常受 HBM 带宽限制，以及 batching、量化、融合、FlashAttention 为什么都在减少数据搬运或提高权重复用。

## 标题候选

1. 推荐：LLM 单请求推理慢，不是 GPU 算不动，而是权重搬不动
2. 稳妥：别只盯 TFLOPS：LLM 推理速度先看内存带宽
3. 大众：租了昂贵 GPU，却只跑出几十 token/s，钱花错了吗？
4. 专家：从 Roofline 到 FlashAttention：LLM 推理的 GPU 性能直觉
5. 反差：GPU 利用率 100%，不等于计算单元吃满了

最终采用候选 1。它先写开发者体感，再给出技术判断；第一屏必须立刻补上“小批量 Decode”边界。

## 一手核对

- Akshay Pachaar 原帖《How a GPU Actually Works》：文章主线、车间/走廊比喻、算术强度、Roofline、Decode/Prefill 区别与优化分类。
- NVIDIA H100 官方规格：H100 SXM 为 80GB HBM、3.35TB/s；官方列出的 Tensor Core 峰值带 `with sparsity` 注记。文章用约 989 TFLOPS 的 dense BF16 等效值与 3.35TB/s 估算约 295 FLOP/byte，只作为 Roofline 教学近似。
- NVIDIA CUDA Programming Guide：warp 为 32 个线程；warp 上下文驻留片上，调度器可在就绪 warp 间切换，以隐藏访存延迟。
- FlashAttention 原论文：通过 tiling 减少 HBM 与片上 SRAM 之间的读写；优化目标是 IO，而不是改变 attention 的数学定义。
- NVIDIA H200 官方技术资料：141GB HBM3e、4.8TB/s，用于说明仅增加容量和带宽也能改善受内存限制的负载。

## 对原文示例的修正

原文用“70B、BF16、140GB 权重、单张 H100 3.35TB/s”推导约 24 token/s，但 140GB 权重无法放入 80GB H100 SXM。成稿改用能放进 80GB H100 的 30B BF16 教学示例：

```text
模型权重约 30B × 2 byte = 60GB
理想带宽上限约 3.35TB/s ÷ 60GB ≈ 56 次整模型读取/秒
因此小批量 Decode 的理想上限约为 56 token/s
```

这是忽略 KV Cache、激活、调度、通信和 kernel 开销的物理上限，不是实测成绩。

## 成文边界

- “Decode 受带宽限制”主要指小批量、自回归生成，不把所有推理阶段一概而论。
- Prefill 常更偏计算受限；长上下文还会引入 attention 和 KV Cache 的额外读写。
- 量化的收益不是无条件翻倍，要计算量化/反量化 kernel、精度和硬件支持。
- batching 优先提升吞吐，不保证单请求延迟；持续批处理需要在 TTFT、ITL 与吞吐之间取舍。
- `GPU-Util` 不能单独证明算力吃满，必须同时观察 HBM 带宽、SM 吞吐和 kernel/CPU 时间线。

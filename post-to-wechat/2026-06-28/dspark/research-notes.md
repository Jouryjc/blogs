---
title: "DSpark 论文研究笔记"
source: "https://github.com/deepseek-ai/DeepSpec/blob/main/DSpark_paper.pdf"
source_author: "DeepSeek-AI"
created_at: "2026-06-28"
tags:
  - type/source
  - topic/agent-runtime
  - topic/ai-industry
---

# DSpark 论文研究笔记

## 一手来源

- 论文 PDF: https://github.com/deepseek-ai/DeepSpec/blob/main/DSpark_paper.pdf
- DeepSpec 仓库 README: https://raw.githubusercontent.com/deepseek-ai/DeepSpec/main/README.md
- Hugging Face 模型卡: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark

## 标题候选

1. 推荐标题: 大模型变快，不是只靠更小模型：DSpark 的草稿验证法
2. 稳妥标题: DSpark 把 speculative decoding 做成了一套生产调度系统
3. 大众标题: DeepSeek 这篇新论文，讲的是大模型怎么少跑冤枉路
4. 专家标题: DSpark：半自回归草稿 + 置信度调度的推理加速方案
5. 反差标题: 推理加速最大坑不在草稿少，而在验证太浪费

## 文章主线

DSpark 不是新模型，而是 DeepSeek V4 上的 speculative decoding 模块。它解决两类浪费:

- 草稿质量浪费: 并行草稿可以一次猜很多 token，但 token 之间缺少依赖，后缀容易被拒。
- 验证算力浪费: 草稿猜得多不等于都值得让大模型验证。高并发时，低置信后缀会占用目标模型 batch 容量。

DSpark 的两刀:

- 半自回归生成: 重计算仍由 parallel backbone 做，轻量 sequential head 给草稿 token 加入前后依赖。
- 置信度调度验证: confidence head 估计每个位置的 prefix survival probability，hardware-aware scheduler 根据当前引擎吞吐曲线决定每个请求验证多长。

## 关键事实

- Speculative decoding 的基本流程: draft model 先提出一段候选 token，target model 用一次 forward pass 并行验证，接受与目标分布一致的最长 prefix，并额外生成一个 bonus token。
- 论文强调 lossless 加速: 验证规则保持 target model 分布，不靠降低输出质量换速度。
- 离线结果: Qwen3-4B/8B/14B 上，DSpark 相比 Eagle3 的 macro-average accepted length 提升 30.9%、26.7%、30.0%；相比 DFlash 提升 16.3%、18.4%、18.3%。
- 线上 DeepSeek-V4 结果: 在匹配吞吐水平下，V4-Flash 每用户生成速度提升 60%-85%，V4-Pro 提升 57%-78%。
- 边界: 这类数字来自 DeepSeek 自己的 V4 serving 系统，不应泛化为任意模型和任意推理框架的固定收益。
- 线上 DSpark-5 最大 draft length 为 gamma = 5，使用 Markov head。
- Limitations: DSpark 仍要先付出生成整段 draft block 的固定成本。复杂查询如果低接受率，这部分草稿成本收不回来。

## 原论文图片

- `imgs/figure-1-dspark-architecture.png`: Figure 1, DSpark architecture and decoding cycle。
- `imgs/figure-4-proposal-length-latency.png`: Figure 4, proposal length and latency overhead。
- `imgs/figure-7-throughput-vs-tps.png`: Figure 7, production throughput vs TPS。
- `imgs/figure-8-load-adaptive-budget.png`: Figure 8, load-adaptive throughput and verification budgets。

图片均从原论文 PDF 渲染裁切，未重绘数据。


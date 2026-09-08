---
title: "AgentJudgeBench 论文事实快照"
source: "https://arxiv.org/abs/2608.26623v1"
source_author: "Abhigya Verma、Amit Kumar Saha、Seganrasan Subramanian、Sai Harshitha Aluru"
created_at: "2026-08-30"
tags:
  - type/source
  - topic/agent-design
  - topic/agent-runtime
moc:
  - "[[agent-design]]"
  - "[[agent-runtime]]"
related:
  - "[[post-to-wechat/2026-08-30/agentjudgebench-llm-judge/agentjudgebench-llm-judge]]"
  - "[[post-to-wechat/2026-08-30/agentjudgebench-llm-judge/source/research-notes]]"
---

# AgentJudgeBench 论文事实快照

## 元信息

- 论文：AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling
- 作者：Abhigya Verma、Amit Kumar Saha、Seganrasan Subramanian、Sai Harshitha Aluru
- 机构：ServiceNow AI，Hyderabad, India
- arXiv：2608.26623v1
- 首次提交：2026-08-27
- 分类：cs.AI
- 许可：CC BY 4.0
- arXiv 备注：EMNLP 2026 Main Conference
- HTML：https://arxiv.org/html/2608.26623v1
- PDF：https://arxiv.org/pdf/2608.26623v1
- 代码：https://github.com/ServiceNow/SyGra/tree/scratch/agent_judge_bench/tasks/agentic_bfcl_judge_eval
- 数据：https://huggingface.co/datasets/ServiceNow-AI/AgentJudgeBench

## 摘要性事实

论文研究的不是“哪个 Agent 最会调用工具”，而是 LLM Judge 在结构化、多步骤工具调用任务上能否可靠地复现程序评分器的判断。

基准包含 3,808 条基础记录。每条记录改写为 easy、medium、hard 三种问法，因此完整数据集是 11,424 个问题变体，覆盖六种 DAG 拓扑。五个 Generator 产生工具调用序列，六个主 Judge 分别在能看见参考轨迹和看不见参考轨迹的条件下，对工具选择、参数结构、调用顺序、查询覆盖四个维度打分。

论文报告：Judge 与程序评分器的一致度会随任务难度上升而下降；without-GT 的下降约为 with-GT 的 1.5 倍。hard、without-GT 条件下，不同 Judge 在同一 Generator 面前的差距被压缩，论文将这一现象概括为约 77%–82% 的窄区间，但并非所有 Generator 与实验格都严格落在这个范围。

给 Judge 参考轨迹也不总是有利。论文内部命名的 GPT-5.4 与 Gemini-2.5-Pro 分别出现 -1.5pp 与 -3.9pp 的 GT lift；结果与过度锚定解释一致，并通过 corrupted-GT 控制实验为 Gemini 的锚定行为提供了更直接的证据。

测试时思考链和温度调整在论文覆盖的有限配对中影响很小。with-GT 的结构化、逐指标评分 rubric 在一组 Judge–Generator 配对上提升 4.8–6.5pp，但在第二组 hard 任务上出现 -0.8pp 反转，因此不能推广为普遍有效的提示技巧。

## 口径说明

- `alignment` 是 LLM Judge 与论文程序评分器的一致程度，不是现实任务成功率。
- 程序评分器没有执行真实工具；参数结构只比较 key，调用顺序只比较一条参考轨迹。
- Ground Truth 是参考轨迹，不保证是唯一正确解。
- 数据是合成、单轮、无状态任务，不直接等于生产环境的多轮 Agent。
- 论文的 `GPT-5.4` 是作者对 2026 年 4 月 Azure preview 快照的内部命名，不是可公开复现的正式模型版本字符串。

## 取证时间

本快照依据 2026-08-30（Asia/Singapore）访问的 arXiv 官方 abs、HTML 与论文正文整理。公众号稿只对 v1 内容负责。

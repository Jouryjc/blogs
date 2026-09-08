---
title: "AgentJudgeBench 工程解读研究笔记"
source: "https://arxiv.org/html/2608.26623v1"
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
  - "[[post-to-wechat/2026-08-30/agentjudgebench-llm-judge/source/paper-source]]"
---

# AgentJudgeBench 工程解读研究笔记

## 研究问题

AgentJudgeBench 把“裁判是否可靠”从 Agent 能力评测中单独拆出来。它不研究开放文本偏好，而是研究一个更结构化的问题：面对带 JSON Schema、工具依赖和多步骤 DAG 的调用轨迹，LLM Judge 能否复现确定性评分器的判断。

## 数据与生成流程

- 3,808 条基础记录，每条改写为 easy、medium、hard，得到 11,424 个问题变体。
- 覆盖 15 个企业领域、六种 DAG：linear、fan-out、fan-in、diamond、optional enrichment、loop-like。
- 每条记录提供 8–19 个候选工具，平均 12.9 个；参考轨迹实际调用 2–5 个工具，平均 3.3 个。
- 难度通过增加自然语言歧义实现，底层工具图与参考轨迹保持不变。
- 在 198 组抽样难度三元组中，medium→hard 被三个 meta-judge 一致认定变难的比例是 93.9%；easy→medium 只有 58.1%。另一个独立口径是 hard 改写“保持同一 GT”的全票比例为 76.8%。因此 medium 适合作为鲁棒性检查，主难度结论应依赖 medium→hard，且不能把 93.9% 误写成 GT 保持率。

## 评分对象

程序评分器和 LLM Judge 都在四个指标上给 `0 / 0.5 / 1`：

1. 工具选择：工具集合是否匹配。
2. 参数结构：参数 key 是否完整，是否多传或漏传。
3. 调用顺序：生成轨迹与参考轨迹逐位置是否一致。
4. 查询覆盖：参考轨迹中的预期工具被命中了多少。

论文的 alignment 计算 LLM Judge 分数与程序评分器分数的接近程度。程序评分器可复现，但不是现实语义的绝对金标准：它不执行工具、不验证参数值语义，也不能识别所有功能等价路径。

## 实验矩阵

### Generator

- Llama-3.3-70B-Instruct
- Qwen3-32B
- Llama-3.1-8B-Instruct
- SmolLM3-3B
- GPT-5.4（论文内部命名的 Azure preview 快照）

### 主 Judge

- QwQ-32B
- GPT-OSS-20B
- GPT-OSS-120B
- Claude Sonnet 4.5
- Gemini-2.5-Pro
- GPT-5.4

Prometheus-2 是额外的 judge-specialised baseline，不计入“六个 Judge”的主统计。

### 两种条件

- with-GT：Judge 能看到参考工具调用轨迹。
- without-GT：Judge 只能看到问题、工具 Schema 与 Generator 输出。

53,608 条有效 Generator 输出乘以六个 Judge，得到 321,648 个唯一 Judge 评测元组；每个元组再分别在两个条件下评测，对应 643,296 个 condition-specific evaluation instances。

## 主要发现

### 难度让 Judge 自身退化

30 个 Generator × Judge 组合在两种 GT 条件下都出现 easy→hard 单调下降。without-GT 的下降约为 with-GT 的 1.5 倍；with-GT 的 medium→hard 通常下降约 5–7pp。

这说明 Judge 不是静态测量仪。问题歧义、依赖结构和 Generator 输出质量变化时，测量工具本身也在变。

### hard/no-GT 的区分力收缩

论文摘要把六个 Judge 在 hard/no-GT 下的集中现象概括为 77%–82%。准确口径是：同一个 Generator 面前，不同 Judge 的差距被压扁；不同 Generator 的绝对水平仍有差异。例如 SmolLM3-3B 单元可落到约 69%–73%，Llama-3.3-70B 可在约 83%–85%。

六 Judge 软集成约 79.5%，最好单 Judge 约 79.8%，差距不超过 0.4pp。多个 Judge 不是独立噪声，而是在同类结构问题上共同失灵，因此简单投票没有带来收益。

### Judge 更一致，不代表更正确

- with-GT：Judge 间平均一致率 79.1%，Cohen's κ≈0.419。
- without-GT：一致率反而升到 92.6%，κ≈0.559。

without-GT prompt 在不确定时偏向给 1.0，导致分数压缩。六个裁判异口同声，可能不是共同看懂了任务，而是共同选择了安全的乐观分数。

### 参考轨迹可能造成锚定

- GPT-5.4：GT lift -1.5pp。
- Gemini-2.5-Pro：GT lift -3.9pp。
- QwQ-32B 与 GPT-OSS-120B 从 GT 中受益。

corrupted-GT 控制实验给 Judge 一条来自其他样本的错误参考轨迹。Gemini-2.5-Pro 在错误 GT 与标准 GT 下的 alignment 相差 0–1.8pp；QwQ-32B 在错误 GT 条件下接近 without-GT，差距不超过 0.2pp。Gemini 的锚定机制有更直接证据；GPT-5.4 的负 lift 与锚定一致，但没有同强度案例验证。

### 最佳 Judge 取决于评测目标

- with-GT、以程序评分器为参照：QwQ-32B 总体最好。
- 120 条 hard 样本的人工验证：GPT-OSS-120B 对人工判断的一致度最高。
- QwQ-32B 对程序为 82.9%、对人工为 74.3%；GPT-OSS-120B 对程序为 82.2%、对人工为 79.4%。
- 两套 Judge 排序的 Spearman ρ 只有 0.26。

人工验证边界：120 条 hard 样本，每条只有一名标注者，共 480 个 metric-level verdict；没有 inter-annotator agreement。人工—程序总体一致 92.7%，但参数结构只有 82.5%。

## 消融与配置杠杆

### CoT

QwQ-32B 开关 thinking，在四个开源 Generator、三档难度、两种 GT 条件上比较：平均 GT 差异 +0.11pp，单格最大不超过 0.3pp。不能推广为“所有推理模型的 CoT 都没用”。

### Temperature

第一组配对最大差异不超过 0.6pp；第二组最大 0.25pp。温度只复验了两个 Judge–Generator 配对，结论限定在本论文设置。

### Structured rubric

with-GT 的 Qwen3-32B Judge × Llama-3.3-70B Generator 中，保留逐指标定义和评分 rubric 的结构化 prompt 比 free-form prompt 高 4.8–6.5pp。第二组 with-GT 的 QwQ-32B × SmolLM3-3B 中，easy +3.9、medium +2.4、hard -0.8。它是论文测到的最大配置杠杆，但效果依赖 Judge、Generator 与难度。

### 默认分消融

将 without-GT 不确定时的默认分从 1.0 改为 0.5，对较强 Generator 只提升 +0.4、+1.0、+0.5pp；对 Llama-3.1-8B 与 SmolLM3-3B 分别提升 +4.1、+5.6pp。强 Generator 的天花板主要由任务难度驱动，弱 Generator 的天花板高度还明显受 prompt 影响。

## 拓扑结果

with-GT 的拓扑分析中，六 Judge 均值里 fan-out 约 92.8%，fan-in 约 84.1%，相差约 8.7pp。fan-out 的并行分支可以独立检查；fan-in 与 loop-like 需要追踪跨分支依赖。只写成该合成基准中的稳定难度信号，不推广为所有生产流程的定律。

## 论文明确局限

- 全部是合成数据；只测单轮、无状态规划。
- 不执行真实工具，不包含多轮恢复与环境状态。
- 程序评分器对语义等价和替代路径不敏感。
- 人工验证是单标注者、小样本。
- easy→medium 难度校准较弱。
- Prompt、温度和 CoT 消融没有覆盖完整全矩阵。
- GPT-5.4 快照不可复现，同时担任 Generator、LLM Judge 与难度改写验证的 meta-judge。
- 论文没有验证 Judge 问题是否会污染 RLHF、DPO 或 reward training。

## 小余工程判断（不是论文已验证结论）

### 四层评测防线

1. **确定性结构检查**：Schema、必填参数、依赖、执行结果、权限和副作用先用程序验证。
2. **LLM 语义复核**：让 LLM 处理意图覆盖、语义等价、解释与无法完全结构化的质量判断。
3. **差异与争议复核**：保留程序分、盲审分、参考轨迹复核分；差异大时不直接汇总成一个分数。
4. **人工抽检**：按难度、拓扑、Generator 和分歧类型分层抽样，不只检查随机 easy 样本。

### 可验证建议

- 可以实验“先不看 GT 独立判断，再展示 GT 做差异复核”，以观察锚定；论文没有测试这一路径。
- Ensemble 要混合规则执行器、Schema 验证器、LLM 语义 Judge 和人工，而不是只堆多个相似 LLM。
- 不把 Judge 间一致率直接当置信度；without-GT 的高一致可能来自共同乐观。

## 写作红线

- 不写“LLM Judge 准确率只有 77%–82%”。
- 不写“标准答案会让所有 Judge 变差”。
- 不写“CoT、温度永远没用”。
- 不写“结构化 Prompt 普遍提升 6.5pp”。
- 不把程序评分器称为绝对真相。
- 不把论文内部命名的 GPT-5.4 当成可公开复现型号。
- 不把四层评测防线写成论文已经跑过的系统。

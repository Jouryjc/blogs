---
title: "GuardianAgentBench 研究笔记"
source: "https://arxiv.org/abs/2607.20982"
source_author: "Vishal Ishwar Naik 等"
created_at: "2026-07-25"
tags:
  - type/source
  - topic/agent-safety
  - topic/agent-runtime
  - topic/agent-design
moc:
  - "[[agent-safety]]"
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[post-to-wechat/2026-07-25/guardian-agent-bench/article]]"
---

# GuardianAgentBench 研究笔记

## 论文

- 标题：GuardianAgentBench: Where Agents Fail and How to Guard Them
- arXiv：2607.20982v1
- 提交日期：2026-07-23
- 作者：Vishal Ishwar Naik、Chenyu Xu、Donna Dong、Hussein Hassan、Abhishek Pradhan、Ofer Mendelevitch、Tallat Shafat、Humayun Irshad

## Benchmark 设计

- 580 个场景，6 个领域，81 个工具，1,177 个顺序 turn。
- 领域：Customer Service 118、Email 117、Calendar 105、Financial 99、Business Intelligence 77、Internal Knowledge 64。
- 398 个普通场景，182 个对抗场景。
- 5 种对抗改造：Massive Data、Error Conditions、Multiple Matches、Prompt Injection、Partial Data。
- 工具数 1–7，平均约 2.76；顺序 turn 平均约 2.05。
- 三个生产框架：LlamaIndex、LangChain、Vectara。
- 六个模型：Claude Opus 4.5、GPT-5.2 Pro、Gemini-3-Pro、DeepSeek-V3.2、Qwen3-Max、GPT-OSS-120B。
- 自动评分同时检查 response correctness 与 action correctness；60 个样本上与人工标注一致率 93.3%（56/60）。

## 关键结果

1. 最佳组合 Claude Opus 4.5 + Vectara，Overall 74.8，约每四个任务失败一个。
2. Calendar 最难，没有模型超过 62.0。
3. 同一模型在三个框架上的差距通常不超过 2–3 分，论文判断失败更多由模型而非框架驱动。
4. 强模型的主要失败是 Missing Required Tool Call；例如 GPT-5.2 Pro 为 56.7%–57.2%，Gemini-3-Pro 为 52.1%–54.7%。
5. DeepSeek-V3.2、Qwen3-Max 更常出现选错工具或重复调用。
6. 工具顺序错误 ITO 只占 0.6%–4.4%，但顺序 turn 变长仍会显著拉低总任务成功率。两者不矛盾：单个已执行调用的排列错误很少，不代表模型能长期维持完整计划、覆盖所有必要调用。
7. Claude Opus 4.5 的平均 Overall 随工具数从 1 个时的 78.2 降至 7 个时的 62.3；随 turn 从 1 层时的 82.3 降至 7 层时的 51.2。长链依赖比工具数量更伤。
8. system prompt 安全说明对强模型几乎无效：Gemini-3-Pro +0.3、Claude Opus 4.5 +0.4、GPT-5.2 Pro -0.3。
9. 执行时 guardrail 对六个模型均有提升，+2.8 至 +7.7。
10. 在 Claude Opus 4.5 + LlamaIndex 上，guardrail 修复 151 个原失败场景中的 30 个（19.9%）；429 个原成功场景中误伤 2 个（0.5%）。

## 三个 Guardrail

- Argument Validation：检查参数是否符合 schema，以及上下文里是否真的有需要的字段。
- Tool Coverage Check：检查必要工具是否被跳过。
- Relevance and Cost Check：拦截无关、重复、徒增成本的调用。

判定为 Pass、Corrective Feedback 或 Block。纠错最多重试两轮，仍失败则阻断并升级给人。

## 文章主判断

Agent 安全不能只写在 prompt 里。生产系统需要把工具调用当成待审批的执行计划，在副作用发生前做参数、覆盖、成本和权限检查。

## 证据边界

- guardrail 只在 LlamaIndex 上实现和评测，不应写成三个框架都验证了防护效果。
- 三个 guardrail 本身由 Claude Sonnet 4.5 驱动，不是纯规则系统；会增加推理成本与延迟，论文没有给出完整成本数据。
- 场景要求唯一 ground-truth 路径，真实任务往往有多条合理路径，因此 74.8 不能外推成“所有生产 Agent 的成功率”。
- 论文的“工具顺序已解决”和“长链规划是瓶颈”需要拆开解释，避免照抄成自相矛盾的结论。

## 补充一手资料

- LangChain 官方文档提供 middleware、`wrap_tool_call` 与 Human-in-the-Loop，可在工具调用前后做验证、阻断、修改和人工审批。
- 官方文档还提供 tool-call limit、PII 检测、重试和 early termination 等中间件，说明“执行层治理”已有工程入口，不只是论文概念。


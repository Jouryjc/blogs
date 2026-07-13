# 调研笔记：Harness Engineering for Self-Improvement

日期：2026-07-12
用途：为公众号文章《AI 自我进化的第一步》提供事实出处。正文所有数字与事实均应能在此文件找到来源。

## 来源清单

1. Lilian Weng 博客原文：https://lilianweng.github.io/posts/2026-07-04-harness/ （下称「Weng 博客」）
2. Latent Space AINews 报道：https://www.latent.space/p/ainews-lilian-weng-summarizes-35 （下称「AINews」）
3. 论文《Stop Comparing LLM Agents Without Disclosing the Harness》：https://arxiv.org/abs/2605.23950 / https://arxiv.org/pdf/2605.23950 （下称「Harness 披露论文」）
4. Developers Digest 解读：https://www.developersdigest.tech/blog/harness-engineering-self-improvement （下称「DD 解读」）
5. 本仓库周报：reports/x-hot-ai-agent-engineering/2026-07-12.md （下称「周报」）

## 一、Weng 博客核心事实

### 发布与热度
- 发布日期 2026-07-04（周报、Weng 博客 URL）。
- 综述约 35 篇论文（AINews 标题「summarizes 35」；周报 Rank 1 同述）。
- 社区反响：Sakana AI 官号日文长文转发；DeepSeek 研究员公开背书；AINews 7/8 做成头条（周报 data；Sakana 转发帖 https://x.com/SakanaAILabs/status/2074489949529776308 ）。
- AINews 补充：Sakana AI 把该文与 The AI Scientist、ShinkaEvolve、Darwin Gödel Machine 关联（AINews）。

### harness 定义（原文引语）
> "A harness is the system surrounding a base model that orchestrates execution and decides how the model thinks and plans, calls tools and acts, perceives and manages context, stores artifacts, and evaluates results."（Weng 博客）

组成：工作流编排、工具调用、上下文管理、工件存储、结果评估，另含权限控制与持久状态管理（Weng 博客）。

OS 类比原文：
> "Similar to an OS, a harness should encapsulate complicated logic while keeping the interface simple. Configs, tool interfaces and other protocols may gradually become standardized."（Weng 博客）

### RSI 判断（原文引语）
> "The near-term path of RSI is unlikely to start as a model directly rewriting its weights."（Weng 博客）

> "The layer between the raw model and the real-world context seems to be as important as the model's raw intelligence."（Weng 博客）

代码即可优化空间：
> "Code is a universal language for defining programs and systems. If an LLM can optimize the code that executes agents, it can access a much larger design space than hand-written prompts."（Weng 博客）

### 三大 harness 设计模式（Weng 博客；DD 解读同述）
1. 目标导向循环：plan → execute → observe → improve
2. 文件系统作持久记忆（管理长程任务工件，替代只靠上下文窗口）
3. 显式子代理与后台任务

### 优化目标演进主线（原文引语）
> "The progression in optimization targets is roughly: prompts → structured context → workflow → harness code → optimizer code."（Weng 博客）

代表论文链（Weng 博客梳理）：
- 上下文工程：ACE（Agentic Context Engineering，Zhang et al. 2025，Generator-Reflector-Curator 结构化上下文）→ MCE（Ye et al. 2026，双层优化）→ Meta-Harness（Lee et al. 2026，把 harness 代码本身当优化目标）。ACE arXiv: 2510.04618；Meta-Harness arXiv: 2603.28052（AINews 给出链接）。
- 工作流搜索：ADAS（Hu et al. 2025，元代理搜索 agent 设计）、AFlow（Zhang et al. 2025，MCTS 优化工作流图）。
- 自我改进 harness：STOP（Zelikman et al. 2023）、Darwin Gödel Machine（Zhang et al. 2025）、Self-Harness（Zhang et al. 2026）、Hyperagents（Zhang et al. 2026）。
- 进化搜索：Promptbreeder、GEPA、AlphaEvolve、ThetaEvolve、ShinkaEvolve。
- 科研代理：AI Scientist（Lu et al. 2026）、ScientistOne、Autodata。
- 联合优化 harness+权重：SIA（Hebbar et al. 2026）。

### 关键数字（均出自 Weng 博客对相应论文的引用）
- Darwin Gödel Machine 进化自身代码库：SWE-bench Verified 从 20.0% 提升到 50.0%；Polyglot 从 14.2% 提升到 30.7%（Weng 博客引 DGM，Zhang et al. 2025）。
- STOP 警示：递归改进 scaffolding 在 GPT-4 上提升平均下游表现，但在 GPT-3.5、Mixtral 等较弱模型上反而退化——递归结构本身不够，基础模型必须足够强（Weng 博客引 STOP）。
- PaperBench：复现 20 篇 ICML 2024 论文，Claude 3.5 Sonnet 最高约 21% 成功率，低于 ML PhD 水平（Weng 博客）。
- MLE-bench：75 个 Kaggle 竞赛，o1-preview 在 16.9% 的竞赛中达到铜牌线（Weng 博客）。
- RE-Bench：7 个环境，人类专家 82% 成功率（Weng 博客；正文未必使用）。

### 七大瓶颈（Weng 博客）
1. 弱评估器与模糊评估（weak and fuzzy evaluators）
2. 上下文与记忆生命周期
3. 负结果（LLM 不擅长放弃假设/报告失败，训练数据成功案例偏多）
4. 多样性崩溃（进化/RL 循环收敛到同一解的变体）
5. 奖励黑客（优化单测就过拟合单测；优化 judge 就学会骗 judge；优化 benchmark 就利用 benchmark 缺陷）
6. 长期成功（编码代理完成眼前任务，但可维护性、所有权边界、迁移成本、向后兼容、未来调试负担等长期健康度不清楚）
7. 人类角色

fuzzy evaluators 原文：
> "Many research claims do not have a fast and precise verifier. Current self-improvement loops work best when evaluation metrics are measurable and objective, similar to how RL works. Research taste, novelty, and long-term scientific value are much harder to measure."（Weng 博客）

reward hacking 原文：
> "A self-improvement loop optimizes whatever signal it is given. If reward comes from unit tests, the agent may overfit to tests; if from a judge model, it may learn reward hacking tricks specific to this judge; if from benchmark scores, it may exploit benchmark artifacts."（Weng 博客）

人类角色原文：
> "Humans should move up the stack, not be removed from the loop."（Weng 博客）

### takeaway（AINews 转述 Weng）
- 即使许多 harness 改进最终被吸收进核心模型，"the need to specify goals and context will not disappear"（指定目标和上下文的需求不会消失）（AINews）。

## 二、Harness 披露论文（arXiv 2605.23950）

- 标题：Stop Comparing LLM Agents Without Disclosing the Harness
- 作者：Yunbei Zhang, Janet Wang, Yingqiang Ge, Weijie Xu, Jihun Hamm, Chandan K. Reddy（arXiv abs 页）
- 提交日期：2026-05-07（arXiv abs 页）；本周随 Weng 博客走热（周报 Rank 8）
- 类型：position paper（abstract 自述）

核心论点（abstract 原文）：
> "…the agent execution harness, namely the infrastructure layer that governs context construction, tool interaction, orchestration, and verification around a language model, is often a stronger determinant of agent performance than the model it wraps."

Binding Constraint Thesis（约束绑定论题，abstract）：
> "…performance variance is governed more by harness configuration than by model choice, and current evaluation protocols therefore systematically misattribute harness-level gains to model improvements."

三条论证线（abstract）：
1. 控制论形式化：harness 是闭环动力系统的控制器，LLM 是被控的随机策略；解释为什么小的 harness 改动能带来超过换模型的性能变化。
2. 已发表 benchmark、工业部署与受控方差分解显示：harness 引入的方差可以显著超过模型引入的方差，"including cases of model ranking reversal"（包括模型排名反转的案例）。
3. 提出 harness-aware 评测框架：披露标准（disclosure standard）+ 方差分解协议（variance decomposition protocol）。

正文其他表述（WebFetch 摘录，来自 PDF）：
> "The evaluation harness itself becomes a confounding variable."
> "Without transparency regarding harness specifications, we cannot definitively attribute performance differences to model capability versus infrastructure variation."

披露清单涵盖：工具规格与可用性、环境配置与约束、agent-harness 交互协议、超时与终止条件、验证与打分方法、可复现工件（PDF）。

## 三、DD 解读的工程建议（正文选用性引用）

- 与其死磕 prompt，不如投资 harness 设计。
- "leave receipts"：留下持久日志、diff、轨迹记录。
- 评估器保持外置（held-out tests），防止被优化循环钻空子。
- 上下文作为去重、带 ID 的工件来管理。
- 引语："The harness is code an agent can already read and rewrite, and its behavior can be validated empirically."（DD 解读）

## 四、写作注意

- 周报提到的 DeepSeek 背书者具体人名无法二次核实，正文只写「DeepSeek 研究员公开背书」或省略人名。
- DGM 数字采用「从 20.0% 到 50.0%」的区间表述，与 Weng 博客引用一致。
- 「35 篇论文」以 AINews 标题与周报为准，Weng 原文未自报总数，正文表述为「约 35 篇」。

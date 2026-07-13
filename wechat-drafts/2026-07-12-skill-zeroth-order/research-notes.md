# Research Notes — SkillOpt-Lite（技能零阶优化）

调研日期：2026-07-12

## 论文定位（已找到原文）

- **标题**：SkillOpt-Lite: Better and Faster Agent Self-evolution via One Line of Vibe
- **作者**：Yifei Shen, Bo Li, Xinjie Zhang
  - 来源：https://arxiv.org/abs/2607.03451
  - 机构信息（来自 HF 论文页抓取，以论文原文为准）：LMMs-Lab / NTU MMLab / Microsoft
    - 来源：https://huggingface.co/papers/2607.03451
- **arXiv**：https://arxiv.org/abs/2607.03451 （HTML 全文：https://arxiv.org/html/2607.03451）
- **提交日期**：2026-07-03（来源：arXiv abs 页）
- **HF Papers 页**：https://huggingface.co/papers/2607.03451，本周登上 HF Papers trending
  - 佐证：本仓库周报 /reports/x-hot-ai-agent-engineering/2026-07-12.md Rank 9（"HF Papers trending（本周）"）
- **代码**：https://github.com/EvolvingLMMs-Lab/SkillOpt-Lite（arXiv abs 页给出的官方仓库；2026-07-13 抓取：85 stars、4 forks、MIT License、Python 90%）
  - 落地形式：`.github/prompts/*.prompt.md` 提示文件（不是独立扩展），可接入 VS Code Copilot Chat、Claude Code 等编码代理（来源：GitHub README）
  - 两条 slash 命令（来源：论文 3.2 节 + GitHub README）：
    - `/skillopt-loop rounds=10 batchsize=40 target=gpt5.4-nano [custom_requirements]` —— 只优化技能层（编辑 skill.md）
    - `/harnessopt-loop rounds=2 batchsize=40 target=gpt5.4-nano skill=best_skill_nano.md` —— 联合优化技能与 agent 代码
- **前作**：SkillOpt: Executive Strategy for Self-Evolving Agent Skills，https://arxiv.org/abs/2605.23904（Microsoft Research，2026-05）；2026-07-13 抓取 HF Papers trending 页显示其 254 upvotes（来源：https://huggingface.co/papers/trending）；SkillOpt-Lite 自身 upvote 数未抓到，文章中不写

## 零阶优化形式化（来源：https://arxiv.org/html/2607.03451）

- 目标函数：f(s) = E_{z~D}[ R( H(M, z, s) ) ]
  - s ∈ S_text：文本形式的技能 artifact（markdown 文件，如 best_skill.md，含领域启发式与声明式提示文本）
  - M：冻结的 LLM 骨干（不改权重）
  - z：任务实例；H：执行 harness；R：奖励函数
- 为什么是零阶（Zeroth-Order）：梯度 ∇_s f 在离散文本空间中解析不可行（"analytically intractable due to the discrete nature of S_text"），LLM 与执行环境的组合不可微 → 只能靠黑盒评估反馈
- 经典 ZO 概念与 skill 优化的映射（论文表 1）：
  - 单轨迹反思 → 1 点梯度估计器
  - 对比诊断 → 中心差分近似
  - 故障隔离编辑 → 沿基向量的坐标下降
  - 编辑预算 → 信任域半径（trust region）
- 与经典 ZO 的差异：经典 ZO 是盲目数值扰动，而 skill 轨迹是可解释的调试反馈（来源：WebSearch 摘要 + arXiv HTML）

## 三原则（来源：https://arxiv.org/html/2607.03451）

1. **文件系统轨迹探索（file-system-based trajectory exploration）**
   - "everything is a file"：每条执行轨迹存为独立文本文件，优化器模型用 ls/grep 等原始 shell / 文件系统工具直接翻原始日志
   - 论文论据（bitter lesson 式）：随着基座 LLM 变强，"直接检查原始日志文件"持续优于重度工程化的基线；预定义的复杂拓扑（层级树归并等）反而成为阻碍
2. **共识属性挖掘（consensus attribute mining）**
   - 跨任务提取不变特性（invariant attributes），而不是从单条轨迹得出结论
   - 理由：过拟合单个试验的异常会增大稳定性系数 β_exp（泛化界中的项）
3. **独立验证门控（independent validation gating）**
   - PAC 学习论证：泛化误差界 ϵ(S) ≤ ϵ̂_D(S) + O(β_exp + √(ln(1/δ)/N))；使用严格不相交的独立验证集可移除 β_exp 项
   - 点名现有方法违反验证协议：Reflexion 跳过独立验证；SkillCAT 用训练失败的子采样当验证（克隆训练分布）

## 最小可行管线（4 步循环）（来源：https://arxiv.org/html/2607.03451）

1. **轨迹落盘**：每条原始执行轨迹存为独立文本文件
2. **轨迹探索**：优化器模型通过文件系统工具（ls、grep 等）导航、聚类共性失败
3. **共识挖掘 + 最小编辑**：识别跨任务不变量，生成紧凑的 diff/patch（Minimal Update Principle，满足 trust-region 约束）
   - 归属更正（2026-07-13 三次抓取确认）：编辑预算衰减 L_t: 4→2 是**前作 full SkillOpt** 的机制（表 1："SkillOpt: Edit Budget decay (L_t=4→2)"），Lite 没有衰减调度，只用每个补丁的 Minimal Update Principle；原文（3.2 节）："Once these patterns are identified, and to satisfy the trust-region constraint of bounded text updates, the system follows a Minimal Update Principle by generating a compact code diff or patch to address the diagnosed errors."
4. **验证门控**：候选技能在独立验证集上评估，有改进才接受；超过历史最佳才覆写 best_skill.md
- IDE 集成一行命令触发（"one line of vibe" 的含义）：
  `/skillopt-loop rounds=10 batchsize=40 target=gpt5.4-nano`
- 论文结论提到扩展到 HarnessOpt 并做了 VSCode 集成；WebSearch 摘要称"integrated into production coding agents like VSCode Copilot"

## 去冗余：相对 full SkillOpt 删掉的组件（来源：https://arxiv.org/html/2607.03451）

- 前作 full SkillOpt：Yang et al. (2026) "SkillOpt: executive strategy for self-evolving agent skills"（论文引用 [27]），使用 mini-batch tree merging、textual learning-rate schedules、rejected-edit buffers
- SkillOpt-Lite 删除：
  1. mini-batch 反思池（平均多个文本更新 → 造成"梯度"模糊化）
  2. 慢更新阻尼（epoch 级）→ 拖慢早期探索
  3. 拒绝编辑缓冲（rejected-edit buffer）
  4. 层级树归并（并行 LLM 合并）→ 用文件系统工具替代

## 实验数字（来源：https://arxiv.org/html/2607.03451，交叉验证 arXiv abs 页摘要）

- 基准（6 个）：SearchQA、SpreadsheetBench、ALFWorld、LiveMath、DocVQA、OfficeQA
- 模型：GPT-4o、GPT-5.4-nano、GPT-5.4-mini、GPT-5.4、GPT-5.5
- baseline：初始技能（Init skill）、full SkillOpt（最多 4 epochs 或 10 batches）
- SkillOpt-Lite vs full SkillOpt（表 2）：
  - LiveMath, GPT-4o：31.2 → 58.8（+27.6）
  - LiveMath, GPT-5.5：64.8 → 73.6（+8.8）（abstract 亦确认 +8.8）
  - LiveMath, GPT-5.4-nano：30.3 → 55.7（+25.4）（abstract 亦确认 +25.4）
  - ALFWorld, GPT-5.4-nano：71.8 → 81.3（+9.5）
  - （注意：Spreadsheet 上两次抓取数字不一致——一次 61.5→79.4/+17.9(GPT-5.4)，一次 69.7 vs 57.1/+12.6，可能对应不同模型行，文章中不使用该组数字）
- 2026-07-13 二次抓取 HTML 全文交叉验证（含初始分数列）：
  - LiveMath, GPT-5.5：初始 36.6 → SkillOpt 64.8 → SkillOpt-Lite 73.6（与首次抓取一致）
  - LiveMath, GPT-5.4-nano：初始 26.4 → 30.3 → 55.7（一致）
  - ALFWorld, GPT-5.4-nano：初始 34.3 → 71.8 → 81.3（一致）
  - Spreadsheet, GPT-5.4：初始 39.9 → 61.5 → 79.4（与首次抓取的 61.5→79.4 一致，可谨慎使用）
- Figure 2 佐证（2026-07-13 抓取）：单批、无验证门控的文件系统轨迹探索，在 LiveMath 和 DocVQA 上即超过 SkillOpt 跑满 4 个 epoch 的结果
- 共识挖掘原文引用（2026-07-13 抓取）："The optimization algorithm must discard single-sample eccentricities and extract the common attributes across heterogeneous rollouts"；"If the refinement process overfits to a specific sample anomaly...the stability coefficient β_exp increases, leading to generalization collapse"
- 验证门控原文引用（2026-07-13 抓取）：候选技能库在独立验证集上评估获得无偏分数，"若超过 historical best score 则覆盖 best_skill.md"；批评 Reflexion、SkillCat、SkillAdapter、Trace2Skill "compromise the validation bound by executing their gates either on direct clones of the source training failure instances or on sub-sampled training subsets"
- 与经典 ZO 的差异原文（2026-07-13 抓取）："Classical ZO relies on blind numerical perturbations, whereas agentic skill optimization functions as language-mediated program compilation where rollout trajectories serve as interpretable debugging feedback."
- token 成本：论文未显式给出 token 数字，只有 "significantly reduced computational overhead" 等定性表述；文章不得编造具体 token 数

## 防冗余 / 防膨胀机制（来源：https://arxiv.org/html/2607.03451，2026-07-13 抓取）

- **Minimal Update Principle**："the system follows a Minimal Update Principle by generating a compact code diff or patch to address the diagnosed errors" —— 每次只写紧凑 diff，不重写整份技能
- HarnessOpt 的三道保险（5.1 节）：
  - Allowlist 约束：只允许修改框架脚手架脚本，任务技能与内部配置列为只读 denylist，防止漂移
  - 可回滚：所有代码编辑可经 git reset 回滚，重大修改包在环境变量 feature toggle 后面
  - Dead band filtering：改进低于死区阈值的补丁，除非在连续型次要软指标上有非平凡进步才接受，否则回滚，"prevent codebase inflation with non-functional artifacts"
- 论文未量化膨胀率，文章中避免给具体百分比
- HarnessOpt on SpreadsheetBench（表 3）：GPT-5.4-nano 从 0.2989 → 0.7758，超过 SkillOpt 设置下 GPT-5.5 的 0.7620（即优化后的小模型超过未充分优化的旗舰模型）
- 收敛行为（图 4）：SkillOpt-Lite 在前 2-3 步就取得主要收益；full SkillOpt 因 mini-batch 切分与慢更新阻尼在早期表现欠佳
- 超参/数据：SkillOpt-Lite 严格限制 10 个 batch；数据分割由 2:1:7 调整为 2:2:6（训练:验证:测试）以缓解高方差；LiveMath 和 OfficeQA 验证集仅 10-20 个实例

## 结论三贡献（来源：https://arxiv.org/html/2607.03451）

1. 把 skill 训练映射到 ZO 优化 + PAC 学习框架
2. 提出极简管线（删除 pooling、damping、rejection buffers）
3. 扩展到 HarnessOpt，并通过 VSCode 集成实现"one-line evolution"；轻量模型（GPT-5.4-nano）优化后可超越 frontier 模型

## 相关背景（用于"闭环三段"一节）

- Skill Distillation（强模型写 SKILL.md 给弱模型执行）：实测 6 个技能盲测 12 胜 0 负 2 平
  - 来源：https://www.iwoszapar.com/p/claude-code-skills-written-by-a-smarter-model （经周报 /reports/x-hot-ai-agent-engineering/2026-07-12.md Rank 2 收录）
- Skills 生态：claude-skills 仓库 5.2k+ stars、345 个 skills/agents/commands，兼容 12 种编码智能体
  - 来源：https://github.com/alirezarezvani/claude-skills （经周报 Rank 6 收录）
- Claude Code / Codex 的技能目录约定：`.claude/skills/<name>/SKILL.md`、`$CODEX_HOME/skills`（通用工程常识，文中仅作举例，不引数字）

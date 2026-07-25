# Research Notes — Controlling Reasoning Effort in LLMs

## 主来源

- **文章**: Controlling Reasoning Effort in LLMs — How LLMs Learn Low-, Medium-, and High-Effort Reasoning Modes
- **作者**: Sebastian Raschka, PhD（Ahead of AI / Substack）
- **发布日期**: 2026-07-18
- **URL**: https://magazine.sebastianraschka.com/p/controlling-reasoning-effort-in-llms

## 文章核心论点

reasoning effort（低/中/高档位）不是推理时的简单截断，而主要是**训练出来的行为**。
所有已公开配方共享一个三步框架：

1. **SFT 引入模式**：用带档位标记的样本 / chat template 教模型认识不同模式
2. **模式条件化 RL**：按档位调整上下文窗口和长度惩罚
3. **预算鲁棒性技巧**：随机截断、交替 RL、续写训练，让模型被硬截断时也能收尾

## 关键事实（已核实）

### RLVR 基础
- DeepSeek-R1 开创 RLVR（Reinforcement Learning with Verifiable Rewards）
- 可验证领域：数学（SymPy/WolframAlpha 校验）、代码（编译器/单元测试）
- 奖励是二元的（0/1），**中间推理轨迹在训练中被忽略**，只看最终答案+格式
- R1 试过 process reward model，"发现对训练没有帮助"
- "aha moment"：模型在 RLVR 中自发学会反思、回溯、自我纠错

### `<think>` 标签
- 纯粹是"化妆品"：方便训练管线切分和 UI 折叠
- 通过格式奖励引入：R_total = R_accuracy + R_format
- 换成别的分隔符也一样

### 开关（on/off）
- Qwen3 "Thinking Mode Fusion"：SFT 混合 `/think`（带推理）和 `/no_think`（空 `<think></think>`）样本
- soft switch = SFT 学出来的；hard switch = tokenizer 直接塞空 think 块

### 档位（low/medium/high）
- gpt-oss：系统提示一句 "Reasoning: low/medium/high"（模型卡确认，llama.cpp 讨论确认）
- 档位 → 输出长度 → 准确率，高档位收益饱和（GPT-5.6 Sol 曲线；"继续加推理预算在某个点之后不经济"）
- 两条实现路径（可叠加，gpt-oss / GPT-5.6 疑似两者都用）：
  - RL：按系统提示施加不同长度惩罚（low 罚重，high 罚轻/不罚）
  - SFT：RLVR 之后再做一轮带档位标注的监督微调

### 六个模型的公开配方

| 模型 | SFT 引入 | RL 条件化 | 预算鲁棒性 | 推理时控制 |
|---|---|---|---|---|
| DeepSeek V4 | 多专家（non-think / think high / think max） | 每模式单独上下文窗口+长度惩罚 | 靠分开的专家 | 系统提示 |
| Nemotron 3 Ultra | gpt-oss-120b 当老师生成 medium 档 SFT 数据 | 长度奖励调整（medium RLVR 提示仅 ~2.5%） | 随机截断轨迹 + mask `</think>` | chat template + 外部预算 |
| Kimi K2.5 | 混合 thinking/non-thinking | Toggle：预算约束阶段⇄不限长阶段交替 | 交替 RL 本身 | 学出来的；另有 thinking/instant 二元模式 |
| GLM-5 | interleaved / turn-level 模式样本 | 多阶段 RL（reasoning→agentic→general→蒸馏） | 未明确披露 | 模板 prefill `<think>` 或 `</think>` |
| Qwen3 | Thinking Mode Fusion | General RL 巩固两种模式 | 部分推理能力是涌现的 | tokenizer 硬预算（到点插 stop-thinking 指令） |
| Inkling | 少量初始 SFT | 连续 effort 值 + 动态 per-token 成本 | 连续条件化 | 系统消息里的 effort 浮点值 |

### 数字
- Kimi K2.5 Toggle：省 25–30% 生成 token，基准性能几乎不变
- Nemotron 3 Ultra：medium 档位 RLVR 提示只占 ~2.5%
- Inkling：effort 连续值 0.2–0.99（API 语义 0.0 ≤ e < 1.0）；异步 RL 超 3000 万 rollouts；推理性能全程 log-linear 提升
- Inkling 奖励：R(e) = R_task − λ(e)·N_tokens，effort 越低 per-token 成本越高

### 两个旋钮 + 未来方向
- 模型大小（训练缩放）× reasoning effort（推理缩放）两个旋钮，非线性交互
- 小模型高 effort 可接近大模型低 effort，取舍看准确率/成本/延迟
- 自动选档是"圣杯"：GPT-5 Auto 模式试过，后来从 UI 撤掉
- Raschka 预测：agent harness 或内部 router 按任务状态、工具状态、剩余预算自动选档，用户可覆盖

## 补充核实来源

- Inkling 官方发布（2026-07-16，Thinking Machines Lab 首个开源权重模型）:
  https://thinkingmachines.ai/news/introducing-inkling/
- Inkling thinking-effort 文档（Tinker docs）:
  https://tinker-docs.thinkingmachines.ai/cookbook/inkling/thinking-effort/
  - effort 是 [0.0, 1.0) 浮点值；更大值鼓励更多推理，但不保证每条样本更长/更准
  - RL 中同时改系统消息指令和 per-token 成本
  - 涌现现象：训练奖励效率后，隐藏推理轨迹变得更短、更"电报体"
- gpt-oss 模型卡（arXiv 2508.10925）：三档推理，系统提示关键词 "Reasoning: low" 等
- VentureBeat / The Register 对 Inkling 发布的报道（背景：Mira Murati 团队）

## 改写注意

- GPT-5.6（Luna/Terra/Sol/Ultra 变体命名）、DeepSeek V4、Nemotron 3 Ultra、GLM-5、Kimi K2.5 的配方细节均转述自 Raschka 原文，不添加原文以外的猜测
- 原文明确区分"已确认的实现"和"合理推测"（如 gpt-oss 内部训练法是推测），改写时保留这种谨慎

# Research Notes: Eval Engineering / Agent 合并门禁

## 源材料

- 主来源：@hanakoxbt 的 X Article 长文（2026-08-01），见 `source-capture.md`
- 互动快照：❤️ 413 · 🔖 846 · 👁 156.7k —— 收藏/赞比 ≈ 2:1，典型"先存后用"的工程向长文

## 交叉验证结果（grok-research，2026-08-03）

| 帖内引用 | 核验结果 |
|---|---|
| Zheng 等 / UC Berkeley 2023，GPT-4 裁判与人类一致率 >80% | ✅ 方向可核：对应 *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*（arXiv:2306.05685），2023 年 LLM-as-judge 的奠基性工作，">80% 一致率、接近人类互评水平"是该论文被广泛引用的结论 |
| Huang 等 / DeepMind, ICLR 2024，intrinsic self-correction 不可靠 | ✅ 可核：*Large Language Models Cannot Self-Correct Reasoning Yet*（arXiv:2310.01798），无外部 grounding 的自我修正经常让结果更差 |
| 2026 benchmark：GPT-5.2 / Gemini 3.1 Pro 给自家族 75–84% 胜率；Claude Opus 4.7 反向低估 10.6–41.2%；ArenaHard 偏差 -38% ~ +90%；同一份输出两个裁判 93.3% vs 39.5% | ⚠️ 未能核到公开原始榜单，按"帖内主张"处理，改写时保留为"原帖引用的测试数据"，不写成行业定论 |
| "至少 500 cases 再信聚合分" | ⚠️ 属作者给的工程经验值，无公开出处，保留为作者建议 |

## 改写判断

1. **原文骨架很好，不做结构重组**：六步本身就是"判断 → 原因 → 方法"的推进链，符合蒸馏小余 2.0。
2. **文章主线**：agent 自动合并的前提不是信任模型，而是有一道读证据的 gate。这个主线与今天 X 热点（Qwen3.8-Max 长程自主 coding 叙事）正好呼应——能力越强，门禁越值钱。开头可以用这个呼应做场景切入。
3. **数字处理**：裁判偏见数据保留原文数字但标注为原帖引用的测试；Zheng/Huang 两个学术引用可以坐实，补上论文名。
4. **可复用对象**：第六步的三条泳道（可逆且小 / 可逆但广 / 不可逆）+ 证据优先级排序（确定性检查 > 轨迹评测 > 历史回滚率 > 模型自评）是天然的表格/知识卡素材。
5. **作者判断**：适合已经在跑 coding agent 的团队；最大坑是"套件全绿 ≠ 产品没问题"（测试收敛于测试本身）。

## 标题候选（5 个）

1. **推荐**：Agent 写的代码你敢不 review 吗？先修好这六道门禁
2. 稳妥：让 Agent 自动合并代码的前提：一套读证据的 Eval 门禁
3. 大众：AI 写完代码直接上线？差的不止是胆子
4. 专家：Eval Engineering：从 LLM 裁判偏见到按爆炸半径开闸的六步实践
5. 反差：Agent 交付能不能自动合并，关键不在模型多强，而在门禁多硬

## 术语约定

- gate → 门禁（保留英文 gate 首次出现）
- judge → 裁判模型
- trajectory → 轨迹
- blast radius → 爆炸半径
- shadow mode → 影子模式
- faithfulness → 忠实度
- thermometer vs thermostat → 温度计 vs 恒温器（保留这个比喻，原文最佳意象）

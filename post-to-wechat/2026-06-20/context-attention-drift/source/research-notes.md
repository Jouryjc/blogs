---
title: "上下文没爆，模型为什么还漏指令？研究笔记"
source: "multi-source web research"
source_author: "Google, Stanford, NVIDIA, THUDM, OpenAI, Anthropic, arXiv papers"
created_at: "2026-06-20"
tags:
  - type/source
  - topic/context-engineering
  - topic/agent-memory
  - topic/agent-design
  - topic/agent-runtime
moc:
  - "[[context-engineering]]"
  - "[[agent-memory]]"
  - "[[agent-design]]"
  - "[[agent-runtime]]"
related:
  - "[[post-to-wechat/2026-06-20/context-attention-drift/context-attention-drift]]"
  - "[[agent-memory-never-forget]]"
  - "[[agent-loop-engineering]]"
  - "[[trellis-agent-workbench]]"
---

# 上下文没爆，模型为什么还漏指令？研究笔记

## 文章判断

上下文窗口没有超限，只说明模型“还能读到这些 token”，不等于模型会稳定、均匀、按优先级地使用每条信息。关键指令被遗漏，通常来自六类因素：

1. 长上下文里的位置偏差：开头和结尾更容易被用到，中间更容易丢。
2. 注意力竞争：每个 token 都在和其他 token 争夺模型下一步生成时的权重。
3. 噪声和硬负例：无关但相似的材料会制造“看起来也重要”的路标。
4. 长对话状态漂移：多轮对话会让早期约束变成背景，后续目标和局部修复会抢占注意力。
5. 指令层级和可执行性不足：关键规则只是“写在里面”，没有变成任务前检查、工具前检查、输出前检查。
6. 有效上下文长度小于标称窗口：窗口大小是容量上限，不是稳定推理质量的保票。

## 标题候选

1. 推荐标题：上下文没爆，模型为什么还漏指令？
2. 稳妥标题：长上下文不是可靠记忆：模型漏指令的原因
3. 大众标题：东西都在聊天里，AI 为什么还是忘？
4. 专家标题：从 Lost in the Middle 看长上下文指令遗漏
5. 反差标题：问题不在窗口太小，而在注意力太散

最终选择推荐标题，因为它从读者真实体感出发：明明规则还在聊天里，模型却像没看见。

## 关键资料

### 1. Attention Is All You Need

来源：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)

可用信息：

- Transformer 的自注意力机制不是“把上下文一次性放进脑子里”，而是为当前位置的生成计算 query 与 key 的匹配，并对 value 做加权组合。
- 对普通读者可以解释成：模型不是拿着荧光笔逐字复习，而是在每一步生成时，对上下文里的许多片段重新打分。
- 文章可用类比：会议桌上有很多便签，主持人每次回答问题时都快速扫一遍，哪些便签被看见取决于当前问题和便签之间的匹配程度。

### 2. Lost in the Middle

来源：[Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) / [ACL Anthology](https://aclanthology.org/2024.tacl-1.9/)

可用信息：

- 论文评估多文档问答和 key-value 检索，发现相关信息在上下文开头或结尾时表现更好，放在中间时表现显著下降。
- 这说明“上下文还在窗口内”不等于“模型会像数据库一样定位到它”。
- 文章可用类比：一摞资料最上面和最后一张容易被想起，中间夹着的票据最容易被忘。

### 3. LongBench

来源：[LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding](https://arxiv.org/abs/2308.14508)

可用信息：

- LongBench 覆盖问答、摘要、少样本学习、代码补全等多类长上下文任务。
- 重点不是单个数字，而是说明长上下文能力需要跨任务评估；“能放长文本”不代表各种任务都会稳。
- 文章可用：长上下文就像仓库变大了，但拣货、核对、打包仍然是不同能力。

### 4. RULER

来源：[RULER: What's the Real Context Size of Your Long-Context Language Models?](https://arxiv.org/abs/2404.06654)

可用信息：

- RULER 专门评估长上下文模型的有效上下文大小，并指出真实可用上下文可能小于模型声明窗口。
- 多跳追踪、聚合、变量追踪等任务比简单 needle retrieval 更接近真实工作流。
- 文章可用：标称窗口像房间面积，有效窗口像你能在房间里快速找到东西的能力。

### 5. Attention Sinks

来源：[Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453)

可用信息：

- 流式长文本中，模型会给初始 token 较多注意力；某些 token 即使语义不重要，也会像“注意力水槽”一样吸走权重。
- 这可以解释为什么位置本身会影响使用效果，而不是纯粹由语义重要性决定。
- 文章可用类比：会议桌最前排的人不一定最懂业务，但更容易被主持人看到。

### 6. NoLiMa

来源：[NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/abs/2502.05167)

可用信息：

- 许多长上下文评测依赖字面匹配，NoLiMa 刻意移除问题和上下文之间的词面重叠，更考验模型语义推理。
- 这提醒读者：模型在长上下文里“搜到相同词”相对容易，真正难的是把隐含关系和指令约束连起来。
- 文章可用：找同款包装容易，认出换了包装的同一种药更难。

### 7. Context Length Alone Hurts LLM Performance Despite Perfect Retrieval

来源：[Context Length Alone Hurts LLM Performance Despite Perfect Retrieval](https://arxiv.org/abs/2510.05381)

可用信息：

- 论文提出即使相关证据已经被完美检索并放进上下文，单纯增加上下文长度也会降低问答表现。
- 这和读者体感高度一致：不是资料没给，而是多余资料让模型更难稳定执行。
- 文章可用：把正确钥匙放在桌上不够，如果桌上还有 100 把相似钥匙，拿错概率会上升。

### 8. Contextual Distraction Curse

来源：[Breaking Focus: Contextual Distraction Curse in Large Language Models](https://arxiv.org/abs/2502.01609)

可用信息：

- 论文研究语义连贯但任务无关的上下文干扰，指出上下文里的干扰项会显著影响模型表现。
- 这支持“噪声越像答案越危险”的判断。
- 文章可用：真正影响专注的不是窗外噪音，而是旁边有人讲一个看似相关的八卦。

### 9. LLMs Get Lost In Multi-Turn Conversation

来源：[LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)

可用信息：

- 论文构造 Sharded Simulation，把一次性任务拆成多轮对话，发现多轮对话会显著降低模型完成任务的能力。
- 论文把现象称为“lostness”，和用户在 Agent 长会话里看到的跑偏、漏规则、忘记前提很接近。
- 文章可用：会议开了太久，后面所有人都在解决刚刚那个小问题，最初的目标反而模糊了。

### 10. OpenAI GPT-4.1 prompting guide

来源：[OpenAI Cookbook: GPT-4.1 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)

可用信息：

- OpenAI 官方提示工程建议强调长上下文和复杂任务中，提示要清楚写出角色、工具调用、规划、输出格式、持久性等。
- 可用于工程建议：把关键约束变成固定块、最终检查、输出格式，而不是散落在自然语言段落里。

### 11. Anthropic Long Context Prompting Tips

来源：[Anthropic Docs: Long context prompting tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

可用信息：

- Anthropic 建议把长文档和输入放在问题之前，并用 XML 标签组织材料；还建议让模型先引用相关片段再回答。
- 可用于工程建议：结构化上下文、先定位证据、再执行指令。

### 12. EXACT: Teaching Long Context Language Models to Reason in Parallel

来源：[EXACT: Teaching Long Context Language Models to Reason in Parallel](https://arxiv.org/abs/2605.07098)

可用信息：

- 2026 预印本把长上下文能力问题指向训练和推理方式：不是只扩窗口就够，还要让模型学会在长上下文中并行分解和推理。
- 文章中谨慎引用为“新近研究方向”，不把它写成行业定论。

## 可写进文章的生活比拟

- 上下文窗口像会议室容量：能坐下 100 人，不等于主持人能记住每个人说过什么。
- 长上下文像冰箱：东西没丢，但如果没有分区和标签，想找“昨天那盒药”会越来越难。
- 关键指令像外卖备注：写在备注栏里还不够，店员出餐前要看到，骑手取餐前也要看到。
- Agent 长会话像装修沟通：最早说“不要动承重墙”，后面讨论瓷砖、灯带、柜门太久，施工队如果没有施工红线清单，就可能忘掉最危险的约束。

## 文章配图规划

1. 封面：上下文没爆，为什么还漏指令？
2. 正文图 1：装得下 vs 用得好。
3. 正文图 2：注意力不是聚光灯，是加权投票。
4. 正文图 3：Lost in the Middle 的 U 型位置偏差。
5. 正文图 4：噪声越像答案越危险。
6. 正文图 5：长对话让旧规则变成背景音。
7. 正文图 6：关键指令被盖住的七种方式。
8. 正文图 7：把关键指令做成工程护栏。
9. 正文图 8：可复用 Prompt 骨架。

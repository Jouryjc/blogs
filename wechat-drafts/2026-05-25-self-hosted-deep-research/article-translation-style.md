---
title: "如何构建一个 Deep Researcher"
source: "https://x.com/akshay_pachaar/status/2047395420935229724"
source_author: "Akshay Pachaar"
author: "蒸馏小余"
written_style: "忠实译写"
created_at: "2026-05-26"
coverImage: "imgs/article-cover.png"
summary: "一个开源、可自托管的 Deep Research 技术栈：用 Onyx 做检索，用 CrewAI 做编排，用 Voxtral 做语音层，把研究流程从闭源云服务搬回自己的基础设施。"
---

# 如何构建一个 Deep Researcher

一个 100% 开源、可自托管的 Deep Research 技术栈。

如果你今天需要 AI 帮你做研究，大概率会使用 ChatGPT Deep Research、Claude、Gemini 或 Perplexity。

它们都很强，也都很方便。但它们也有一个共同点：它们是闭源 SaaS，运行在别人的云上。

你提交的每一个研究问题，以及你连接进去的每一份内部文档，都在供应商的服务器上处理。

对很多团队来说，过去的选择只有两个：接受这个交换，或者不把 AI 用在严肃研究里。

这篇文章介绍第三种选择：一套完全开源、可以跑在自己基础设施上的 Deep Research 栈。

它由三个工具组成：

- **Onyx**：检索层。
- **CrewAI**：编排层。
- **Voxtral**：语音层。

这套系统可以从语音提问开始，检索公开网页和内部资料，再生成带引用的研究报告，并把报告朗读出来。

![原文封面：100% Open-Source Deep Researcher](source-media/2047394888136929280.jpg)

图中要点：Onyx、CrewAI、Voxtral 被放进同一套 Deep Research 工作流里。原文强调的是“可自托管”，也就是查询、索引、数据和执行流程都可以放在自己的基础设施内。

![完整 Demo 界面：Agentic Deep Researcher](source-media/2047309825919582208.jpg)

图中要点：界面左侧支持上传文档和语音输入，中间是 Agentic Deep Researcher 主窗口，底部可以输入研究问题。这个 Demo 展示的是端到端流程，而不是单独的聊天框。

## 为什么自托管重要

主流 AI 研究工具基本都是闭源云服务。这会带来几个直接后果。

**第一，研究问题会发送到供应商服务器。**

你问的问题本身就会暴露你正在做什么。一次看似普通的研究请求，可能包含产品方向、客户情况、交易线索、内部故障、合规风险或工程路线。

**第二，连接的数据会在供应商基础设施里被索引。**

很多 Deep Research 产品都支持连接企业数据源。连接很方便，但索引的位置决定了信任边界。索引在谁那里，谁就控制了数据处理、访问和留存方式。

**第三，留存、日志和审计规则由供应商决定。**

企业套餐可以缓解这个问题，但不会让它消失。对于受监管行业、敏感 IP 团队、数据驻留要求严格的组织，这不是理论风险。

**第四，配额和价格会按供应商节奏变化。**

你今天依赖的功能，明天可能被重新定价、限流，或者变成更高套餐的一部分。

这就是很多团队一直犹豫的原因。AI 研究很有用，但当研究材料变成内部文档、客户资料、代码库、工单、会议记录和战略信息时，闭源云服务会让人不放心。

除非整套系统都能自己运行。

![供应商云 vs 自有基础设施](source-media/2047376961442635776.jpg)

图中要点：左侧是供应商云，查询会离开你的网络，数据和索引放在 ChatGPT、Claude、Perplexity 这类服务侧；右侧是自有基础设施，查询留在自己的环境里，Onyx 自托管，索引、权限同步和连接数据都由你控制。底部强调：索引位置就是信任边界。

## 现有研究工具为什么容易失效

大多数研究工具只做一轮流程。

它们先搜索，拿到结果，然后把内容交给 LLM 写成报告。

对浅层问题，这样可以工作。

但一旦问题需要跨来源综合、识别矛盾、做多跳推理，或者同时使用公开资料和内部资料，这种流程就会断裂。

典型失败方式有三种。

第一种，Agent 找到一个来源，又找到另一个相反来源，但它只选择其中一个继续写，矛盾没有被呈现。

第二种，两个来源其实来自同一条原始证据，只是换了说法，但报告把它们当成两份独立证据。

第三种，关键事实藏在没被召回的文档里。关键词匹配无法理解“cloud migration”和“把 PostgreSQL 集群迁到 AWS”之间的关系，于是多跳连接丢失。

这些不是边缘情况，而是现实研究问题的常见形状。

根本原因是：研究不是一个任务。

![One-Pass Agent 的问题](source-media/2047378310955724801.jpg)

图中要点：一轮式 Agent 把收集、分析、写作压成连续流程，噪音会一路向后传。最终报告可能读起来流畅，但矛盾被抹平、重复来源被误当成独立证据、多跳连接也可能被漏掉。

## 好的 Deep Research 需要什么

不管使用什么工具，好的 Deep Research 至少需要五件事。

**1. 阶段分离。**

收集、分析、写作之间需要明确边界。每个阶段只接收上一阶段整理后的输出，而不是直接共享同一个上下文窗口。

**2. 会推理的检索。**

关键词搜索很脆。向量相似度在多跳问题上也会失败。系统需要并行生成查询变体，把结果重新组合，再让 LLM 在合成前筛选相关材料。跳过这个筛选环节，幻觉就会进入报告。

**3. 循环中的反思。**

静态计划碰到真实发现后经常不够用。系统应该在出现新线索时调整方向，同时记录原计划中哪些内容已经覆盖、哪些仍然缺失。

**4. 统一搜索公开资料和内部资料。**

研究层需要同时搜索 Web 和内部知识库，并且按文档权限控制可见范围。索引在自己基础设施里，还是在供应商云里，决定了谁真正拥有数据。

**5. 语音层。**

对复杂研究问题来说，说出来往往比打字更自然。对长报告来说，听一遍有时比一直盯着屏幕读更容易吸收。语音层不是底座，但它会让工具更容易使用。

![好的 Deep Research 五层能力](source-media/2047377686033756160.jpg)

图中要点：底层是阶段分离，然后是会推理的检索、循环反思、公开资料和内部资料统一搜索，最上面才是语音层。图中强调：阶段分离是基础，语音层是最后一块砖。

## Onyx：开源检索层

Onyx 是这个系统里的检索层。

它是一个开源 AI 平台，可以给任意模型提供 RAG、Web Search、代码执行、Deep Research、自定义 Agent 等能力。

更重要的是，它可以自托管。

这意味着你的数据不必离开自己的基础设施。

Onyx 参加过 DeepResearch Bench。这个 benchmark 覆盖 100 个博士级研究任务，横跨 22 个领域，用报告质量和引用准确性等指标评估 Deep Research Agent。

原文发布时，Onyx 在榜单上的表现高于 OpenAI Deep Research、Gemini 2.5 Pro 和 Perplexity Deep Research。

我在 2026 年 5 月 25 日重新核对榜单时，Onyx 仍然高于这三个闭源 Deep Research 产品，但已经不是总榜第一。所以这里更准确的说法是：Onyx 的表现已经进入可以和主流闭源 Deep Research 产品比较的区间。

Onyx 团队分享过一条核心思路：宁愿研究得足够彻底，也不要急着显得有帮助。

这个思路体现在它的架构上。

## 三个阶段，而不是一个循环

Onyx 的研究流程分成三个阶段。

**阶段一：澄清。**

当查询太短或太模糊时，系统最多会提出 5 个定向问题。如果用户已经给出足够详细的需求，这一步会自动跳过。

**阶段二：规划。**

系统会把查询拆成最多 6 个探索方向。这里有一个关键设计：规划器没有工具访问权限。它只能产生计划，不能直接搜索，也不能提前回答。

**阶段三：迭代执行。**

编排器和研究 Agent 交替工作，最多进行 8 个循环。每个循环最多可以并行派发 3 个研究 Agent。

![Onyx 三阶段架构](source-media/2047378785163726849.jpg)

图中要点：第一阶段最多问 5 个澄清问题；第二阶段生成最多 6 个探索方向，规划器没有工具权限；第三阶段最多执行 8 轮，每轮最多 3 个 Agent 并行。底部两个约束很关键：编排器不直接搜索，研究 Agent 看不到完整查询和完整计划。

这两个分离不是限制，而是特性。

编排器不直接搜索，可以避免全局计划被局部检索结果污染。

研究 Agent 看不到完整问题和完整计划，可以迫使每个任务说明都足够自洽。每个 Agent 只完成自己那部分研究，不把无关上下文带进去。

## 自适应策略

Onyx 不会机械执行最初计划。

每次派发研究 Agent 之后，它都会运行一次反思步骤，输出结构化结果：

- 已经覆盖了什么？
- 还缺什么？
- 出现了哪些新的方向？
- 继续搜索是否还能带来新信息？

这个步骤每轮都会执行。

因此，系统的行为更像研究员，而不是一次性检索引擎。

## 六阶段检索流水线

在 LLM 合成答案之前，每个研究 Agent 都会先跑一条六阶段检索流水线。

**第一阶段：查询生成。**

系统并行生成多种查询，包括语义改写、关键词变体、更宽泛的搜索。如果用户问题包含多个子问题，也会自动拆分。

**第二阶段：搜索和重组。**

Onyx 使用混合索引，也就是向量检索加 BM25。结果会通过 Reciprocal Rank Fusion 合并排序，相邻 chunk 也会被合并，避免上下文被切得太碎。

**第三阶段：LLM 选择。**

LLM 会查看所有候选 chunk，只保留相关材料。原文特别强调：如果跳过这一步，幻觉就会进入系统。

**第四阶段：上下文扩展。**

对每个被选中的文档，LLM 会读取周围 chunk，决定需要扩展多少上下文。这个步骤可以按文档并行。

**第五阶段：构建 Prompt。**

系统把选中的片段、引用和聊天历史组装到 prompt 中。

**第六阶段：合成答案。**

LLM 生成有来源支撑的回答，并把引用链接回具体来源。

![Onyx 六段式检索流水线](source-media/2047381972503408640.jpg)

图中要点：流程从查询生成开始，经过搜索融合、LLM 筛选、上下文扩展、Prompt 构建，最后才进入答案合成。图中把第三阶段标成“幻觉闸门”，意思是材料筛选是质量控制点，不是可有可无的优化。

## 引用完整性

研究报告的引用不应该在最后才补。

Onyx 的做法是：Agent 写中间报告时就加入 inline citation。

当多个并行 Agent 产生引用后，系统会把引用合并，并重新编号成统一集合。

最终报告里的每个关键结论，都能追溯到具体来源文档。

这对严肃研究非常重要。

因为你不仅要知道答案是什么，还要知道这句话从哪里来、是否有权限查看、来源是否可靠、以后能否复核。

## 内部资料要在自己的基础设施里索引

Onyx 可以连接很多企业数据源，包括 Slack、Confluence、Jira、GitHub、Salesforce、Google Drive、SharePoint、Notion、Zendesk、HubSpot、Gong 等。

![企业连接器示例](source-media/2047382681403723776.jpg)

图中要点：这里展示的是企业连接器生态，包括 Slack、Gmail、Salesforce、GitHub、Discord、Teams、Google Drive、HubSpot、GitLab、Dropbox、Zendesk、Notion、SharePoint 等。Deep Research 不应该只搜索网页，也应该搜索组织内部已经积累的知识。

和闭源工具相比，区别不在于是否能连接这些数据源。

区别在于索引发生在哪里。

Onyx 会在你的基础设施中持续预索引这些内容，同步内容、元数据和权限。

这会带来几个结果：

- 一个查询可以同时覆盖公开 Web 和所有内部来源。
- 用户只能看到自己有权限访问的文档。
- 权限会从源系统自动同步。
- 内部数据不会离开你的网络去供应商侧建索引或存储。

![Onyx 连接器管理界面](source-media/2047382937096908801.jpg)

图中要点：这是 Onyx 的连接器管理界面。File、Notion、Slack 等连接器会显示最近索引时间、状态、权限访问范围和文档数量。它强调的是持续索引和权限同步，而不是一次性上传文件。

## CrewAI：编排层

Onyx 负责检索，CrewAI 负责协调。

很多开发者第一反应会写一个 Agent，然后让它顺序执行三个任务：收集、分析、写作。

这种模式的问题是，上下文会越积越多。

Writer 可能在 Analyst 完成之前就开始依赖不完整材料。原始搜索噪音会进入最终报告。来源材料也会在多个阶段被重新解释。

CrewAI 用三个能力解决这个问题。

**第一，Flows。**

Flows 可以把彼此独立的 Crews 连接起来。每个 Crew 只接收上一个阶段的干净输出，不继承整个上下文。

**第二，Skills。**

Skills 可以在运行时把领域特定说明注入 Agent prompt。例如报告结构、证据标准、语气要求和格式规则。

**第三，MCP 集成。**

MCP Server 可以直接挂到 Agent 上，不需要额外 adapter，也不需要手动维护复杂的上下文管理器。

把 Onyx 接进 Researcher Agent，只需要一个声明：

```python
from crewai import Agent

researcher_agent = Agent(
    role="Senior Research Analyst",
    goal="Gather information on research query with source URLs",
    backstory="You are a disciplined analyst. Record every source URL.",
    mcps=[
        f"{ONYX_MCP_URL}?token={ONYX_TOKEN}"
    ]
)
```

这样 Researcher Agent 立刻获得三个工具：

- 搜索知识库。
- 搜索 Web。
- 抓取任意 URL 的完整页面内容。

不需要手动接工具，不需要重复写 schema。连接按需建立，服务器不可达时也可以优雅失败。

## Voxtral：语音层

每个研究工作流都有一个摩擦点：键盘。

AI 工具里的语音能力通常只是外接功能：输入用一个转录模型，输出用一个 TTS，中间没有统一设计。

原文里的 Voxtral 用来解决语音输入和报告朗读。

它带来两个体验变化。

**第一，语音输入。**

用户可以直接说出问题，而不是手动输入。转录文本会进入研究流水线。

**第二，报告朗读。**

最终 Markdown 报告可以被朗读出来。对长报告来说，听一遍有时比一直读屏幕更容易。

![Voxtral 输入输出示意](source-media/2047385500152193024.jpg)

图中要点：左边是音频输入转文本输出，右边是文本输入转音频输出。它的作用不是替代检索层或编排层，而是让研究工具更容易被使用。

## 完整系统如何工作

完整流程可以这样理解。

用户输入文本、说一段语音，或者上传 PDF 作为研究问题。

Researcher Agent 通过 Onyx MCP 搜索 Web 和内部文档。

Analyst Agent 对研究发现去重、标记矛盾，并按主题整理。

Report Writer Agent 输出结构化、带引用的 Markdown 报告。

用户点击 Play Report，就可以用 Voxtral TTS 听报告。

![Multi-Agent Deep Researcher Workflow](source-media/2047385969649999872.jpg)

图中要点：左侧是用户输入，可以来自语音或 PDF；Researcher Agent 调用 Onyx MCP Tools 产生 Research Findings；Analyst Agent 做分析并生成 Analytical Summary；Writer Agent 写出 Final Markdown Report；最后 Voxtral TTS 朗读报告。整个流程由 CrewAI 编排。

## 三个 mini-crews，而不是一个 Crew

最自然的设计是一个 Crew，里面放三个顺序任务。

不要这样做。

共享上下文会降低事实质量。Onyx 团队把这种现象叫作“deep frying”：事实被重新解释，矛盾被抹平，原始材料到 Writer 手里时已经不像原材料。

这套系统使用 Flow，把流程拆成三个独立 Crew。每个 Crew 只接收上一个阶段的干净输出。

![三个 mini-crews 的边界](source-media/2047386259732201472.jpg)

图中要点：Researcher Crew 只在第一阶段运行，并拥有搜索 Web、打开 URL、搜索索引文档等 MCP 工具；Analyst Crew 没有工具，只读取研究发现并分析；Writer Crew 也没有工具，只读取分析摘要并生成最终报告。图里特别标出 Analyst 不能碰 collected_urls，强调工具权限和材料边界。

**Researcher Agent** 连接 Onyx，执行 Web 搜索、完整 URL 阅读、上传 PDF 搜索和内部文档搜索。每条发现都带引用。

**Analyst Agent** 接收原始发现，然后：

- 去除重复事实。
- 合并不同来源中表达相同含义的内容。
- 标记明确矛盾。
- 按主题组织材料。

它输出的是结构化摘要，而不是一堆搜索结果。

**Report Writer Agent** 把结构化摘要写成带引用的 Markdown 报告。

为了让输出稳定，Writer 配备一个 CrewAI Skill。这个 Skill 在生成时注入报告结构、证据标准和格式规则。

目录大概是这样：

```plaintext
deep-research-report/
├── SKILL.md       # 报告格式、证据标准、结构规则
├── scripts/       # 可选
└── references/    # 可选
```

`SKILL.md` 使用 YAML front matter 和 Markdown 正文：

```markdown
---
name: deep-research-report
description: >
  Guidelines for writing high-quality, publication-ready deep research reports.
  Covers structure, tone, evidence standards, and formatting rules.
metadata:
  author: deep-research-agent
  version: "1.0"
---

Instructions for the agent go here.
This markdown is injected into the agent's prompt when the skill is activated.
```

这让报告质量不完全依赖模型临场发挥，而是变成一个可复用的写作约束。

![执行成功截图](source-media/2047386667263434752.jpg)

图中要点：截图显示 Flow Execution Completed，并给出 ResearchFlow ID。下方提示 tracing 目前关闭，如果要开启，可以设置 `tracing=True`、配置 `CREWAI_TRACING_ENABLED=true`，或运行 `crewai traces enable`。

## 代码和模板

原文给出的代码入口在 Lightning AI Studio。

可以从这个模板开始：

<https://lightning.ai/lightning-ai/templates/multi-agent-deep-researcher-powered-by-gemma-4?utm_campaign=akshay&utm_medium=twitter>

Onyx 的开源仓库：

<https://github.com/onyx-dot-app/onyx>

## 构建这套系统能得到什么

这篇文章的重点不是说开源工具终于追上了闭源产品。

重点是：Onyx 可以让 Deep Research 跑在你能检查、能自托管、能修改的基础设施上。

再加上 CrewAI 的阶段分离和 Voxtral 的语音层，最终得到的是一个同时具备能力、控制和透明度的研究栈。

**能力。**

它能提供有竞争力的研究质量，并且保留完整引用链。

**控制。**

查询、索引和内部数据都可以留在自己的基础设施中。

**透明。**

代码可以阅读、审计和扩展。

![能力、控制、透明的交集](source-media/2047387722575405056.jpg)

图中要点：这张图把 Capability、Control、Transparency 画成三个圆。Onyx + CrewAI + Voxtral 位于交集处。能力来自 benchmark 表现和引用完整性；控制来自自有基础设施和权限审计；透明来自开源代码和可扩展性。

最后真正值得问的问题是：

如果数据主权不再是限制，你的团队会怎样设计自己的研究工作流？

可以从这里开始。

---

参考资料：

- 原文：<https://x.com/akshay_pachaar/status/2047395420935229724>
- Onyx GitHub：<https://github.com/onyx-dot-app/onyx>
- Onyx 官网：<https://onyx.app/>
- DeepResearch Bench：<https://deepresearch-bench.github.io/>
- DeepResearch Bench Leaderboard：<https://huggingface.co/spaces/muset-ai/DeepResearch-Bench-Leaderboard>
- CrewAI：<https://crewai.com/>
- Voxtral-4B-TTS-2603：<https://huggingface.co/mistralai/Voxtral-4B-TTS-2603>

---
title: "跨微服务 Agent 上下文与契约验证：研究笔记"
source: "https://x.com/dotey/status/2071961238528012358"
source_author: "宝玉（@dotey）"
created_at: "2026-07-01"
tags:
  - type/source
  - topic/context-engineering
  - topic/agent-design
  - topic/agent-runtime
moc:
  - "[[context-engineering]]"
  - "[[agent-design]]"
  - "[[agent-runtime]]"
related:
  - "[[post-to-wechat/2026-07-01/microservice-agent-context/article]]"
  - "[[dotey-microservice-agent-source]]"
---

# 跨微服务 Agent 上下文与契约验证：研究笔记

## 原始问题

一家公司有十几个微服务，希望让开发使用 AI Agent 做系统设计和编码。难点是一个 user story 经常跨多个服务，Agent 需要理解服务职责边界、业务概念、API 协议和验证方式。团队考虑把所有服务放进同一个 workspace，每个服务配自己的文档。

## 原文核心判断

- 放进一个 workspace / monorepo / virtual monorepo 是合理起点，但不能等同于“把代码都扔给 AI”。
- Agent 需要一张根索引：有哪些服务、各自职责、相关文档在哪、改哪个服务要先读什么。
- 每个服务目录需要局部说明，尤其是职责边界、领域概念和服务协议。
- 能从代码或规格生成的文档不要手写；OpenAPI、schema、Pact 契约文件、contract test 比普通文字文档更可靠。
- 跨微服务验证不能依赖完整端到端环境，应该用 mock server、OpenAPI spec、contract test 形成“写代码 -> 跑测试 -> 自我修正”的闭环。

## 补充资料

1. Anthropic《Effective context engineering for AI agents》
   - Context engineering 的重点不是写更漂亮的 prompt，而是在每一轮推理前决定哪些信息应该进入有限上下文。
   - 文章强调 context 是有限资源，信息越多并不必然越好；高信号、按需加载更重要。
   - 适合折回本文：微服务 workspace 的价值不是“全量塞进去”，而是提供可导航的上下文结构。

2. Anthropic《Effective harnesses for long-running agents》
   - 长任务里 Agent 常见失败是一次做太多、跨上下文窗口丢失进度、没有验证就宣称完成。
   - Anthropic 的示例强调 feature list、progress file、git history、初始化脚本和明确测试工具。
   - 适合折回本文：跨服务需求应该先拆成一项项可验证的服务改动，不要让 Agent 一口气改完整条链路。

3. AGENTS.md 官方站
   - AGENTS.md 被定位成给编码 Agent 的 README，适合放 setup、测试、代码风格、安全事项等。
   - 大型 monorepo 推荐在子项目里放嵌套 AGENTS.md，让最近的文件提供局部规则。
   - 适合折回本文：根目录做服务地图，服务目录做局部边界和命令。

4. OpenAPI Specification
   - OAS 定义了语言无关的 HTTP API 标准接口，让人和计算机在不看源代码、不抓包的情况下理解服务能力。
   - OAD 可以被文档生成、代码生成、服务端/客户端生成和测试工具使用。
   - 适合折回本文：OpenAPI 是“活文档 + mock + 测试入口”，不是附属文档。

5. Pact Docs
   - Pact 把 contract tests 定义为验证应用间消息是否符合共同契约的测试。
   - Pact 文档明确说契约测试在多服务环境里尤其适用，可以降低昂贵、脆弱的集成测试依赖。
   - 适合折回本文：把契约测试作为 Agent 的本地验证闸门，而不是只在 CI 里给人看。

## 标题候选

1. 推荐标题：微服务别直接塞给 Agent：先补上下文地图和契约测试
2. 稳妥标题：跨微服务用 Agent，先搭三层上下文和验证闭环
3. 大众标题：十几个服务交给 AI 写代码前，先做这张工程地图
4. 专家标题：虚拟 Monorepo + 契约测试：Agent 才能改跨服务需求
5. 反差标题：Agent 改微服务，最大坑不在代码多，而在协议没闭环

最终选择：`微服务别直接塞给 Agent：先补上下文地图和契约测试`

理由：标题先命中工程误区，再给出两个具体抓手；比“跨微服务 Agent 实践”更适合推荐流，也没有夸大到“解决所有微服务协作”。

## 文章结构

1. 先给判断：一个 workspace 是起点，不是答案。
2. 拆三层：
   - 全局视图：monorepo / virtual monorepo + 根 AGENTS.md。
   - 精准上下文：服务级 AGENTS.md、bounded context、OpenAPI、schema、contract test。
   - 验证闭环：mock server、contract test、局部 CI、Agent 自我修正。
3. 给落地清单：根索引、服务卡片、接口规格、契约测试、mock、完成定义。
4. 给作者判断：适合谁、不适合谁、最大坑。
5. CTA：收藏三层清单；回复关键词“微服务”可继续拆一份目录模板。

## 资料来源

- X 原文：https://x.com/dotey/status/2071961238528012358
- Anthropic Effective context engineering for AI agents：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic Effective harnesses for long-running agents：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- AGENTS.md：https://agents.md/
- OpenAPI Specification：https://spec.openapis.org/oas/latest.html
- Pact Docs：https://docs.pact.io/

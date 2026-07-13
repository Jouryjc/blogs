---
title: "宝玉：跨微服务场景下如何让 AI Agent 做系统设计和编码"
source: "https://x.com/dotey/status/2071961238528012358"
source_author: "宝玉（@dotey）"
captured_at: "2026-07-01"
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
  - "[[post-to-wechat/2026-07-01/microservice-agent-context/source/research-notes]]"
---

Q：我们公司有十几个微服务，现在想让开发用 AI Agent 来做系统设计和编码。问题是一个 user story 经常需要多个微服务协作，Agent 必须了解每个服务的职责边界和业务概念才能做出合理的设计。我们打算把所有微服务放到一个 workspace 下，每个服务配上自己的文档，让 AI 自己去处理。这种方式合理吗？有没有更好的实践？

A：用好 Agent 的关键是两点：上下文的质量，和验证的闭环。

先说上下文质量。

放在一个 workspace 下是目前社区比较推荐的做法。

monorepo 天然适合和 AI 配合，因为 Agent 可以在一个地方同时看到 schema 定义、API 协议、各个服务的实现代码。如果因为历史原因确实不方便合成 monorepo，有个折中方案叫虚拟 monorepo，就是把多个仓库 clone 到同一个本地目录下。

除了放在一起，文档也是很好的让Agent获取上下文的方式，最好给 Agent 一张地图，加上按需加载：
1. 根目录放一份总的 AGENTS.md(或 CLAUDE.md)当索引用，列清楚有哪些服务、各自负责什么、要改某个服务就去读它目录下的文档。
2. 每个微服务自己目录里再放一份,写清自己的职责边界和业务概念,这其实就是 DDD 里的 bounded context。
3. 让 Agent 先看根索引，定位到相关的那几个服务，再去加载它们的细节。

不过要注意文档要及时更新，尤其是微服务协议变更了，一定要及时更新文档，否则会误导。

能从代码或规格自动生成的，就别手写。手写文档迟早会和代码对不上，而像 OpenAPI 这种机器可读的接口规格，一份东西既是文档，又能拿去生成 mock 和测试。

除了文档，还有一个很多人忽略的上下文来源：协议测试代码。高质量的 contract test 本身就是最准确的活文档，它精确地描述了服务之间实际的交互协议，比人写的文档更不容易过时，因为错了测试就无法通过。你如果已经有 OpenAPI spec 或者 Pact 契约文件，这些对 Agent 理解服务边界非常有价值。

再说验证。微服务场景下验证是最麻烦的部分，因为一个 user story 可能涉及好几个服务协作，你不可能让 Agent 每改一行代码就把整个系统跑起来做端到端测试。

一个实用的思路是：每个微服务提供 mock server 或者基于 OpenAPI spec 自动生成的模拟服务。Agent 写完代码后可以在本地跑 contract test 验证自己的改动有没有破坏和其他服务的协议约定，不需要依赖线上真实的 API 或者完整的集成环境。这样 Agent 就能形成一个“写代码→跑测试→自我修正”的闭环，不需要人在过程中频繁干预。

想再进一步,建议了解一下契约测试(consumer-driven contract testing，常用工具是 Pact)。思路是调用方把自己实际用到的接口形状记下来，生成一个契约文件，被调方再去验证自己能不能满足这个契约。

简单说：workspace 统一提供全局视图，分层文档 + 协议测试提供精准上下文，mock server + contract test 提供验证闭环。这三层搭好，Agent 处理跨微服务的系统设计就比较靠谱了。

一些参考资料

1. Anthropic 的 Effective context engineering for AI agents，讲怎么把上下文当稀缺资源来经营、按需加载:
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

2. Anthropic 的 Effective harnesses for long-running agents，讲长任务里怎么给 Agent 搭脚手架(比如用进度文件加 git 记录跨上下文窗口接力)：
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

3. 怎么在 monorepo 里组织 AGENTS.md 给 Agent 用,可以看 http://dev.to 上这篇 Steering AI Agents in Monorepos with AGENTS.md：
https://dev.to/datadog-frontend-dev/steering-ai-agents-in-monorepos-with-agentsmd-13g0

契约测试入门，搜 Pact 加 consumer-driven contract testing 的指南就行。

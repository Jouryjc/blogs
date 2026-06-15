---
title: "Claude Fable 5 / Mythos 5 研究笔记"
source: "https://www.anthropic.com/news/claude-fable-5-mythos-5"
source_author: "Anthropic"
created_at: "2026-06-10"
tags:
  - type/source
  - topic/ai-industry
  - topic/claude-code
  - topic/agent-runtime
moc:
  - "[[ai-industry]]"
  - "[[claude-code]]"
  - "[[agent-runtime]]"
related:
  - "[[claude-fable-5-programmers]]"
---

# Claude Fable 5 / Mythos 5 研究笔记

## 标题候选

1. 推荐标题：Claude 5来了，程序员该交出去哪些任务
2. 稳妥标题：Claude Fable 5 对程序员真正有用的变化
3. 大众标题：Claude 5 不只是更聪明：它更会干活了
4. 专家标题：从 Fable 5 到 Mythos 5：长任务编程能力怎么变
5. 反差标题：Claude 5 的重点不是聊天，而是接住长任务

最终选择：`Claude 5来了，程序员该交出去哪些任务`

## 官方发布要点

- Anthropic 在 2026-06-09 发布 Claude Fable 5 和 Claude Mythos 5。
- Fable 5 是面向普通用户和开发者开放的 Mythos-class 模型；Mythos 5 是同一能力层级但解除部分安全限制的版本，只面向 Project Glasswing 等受限访问场景。
- Fable 5 的官方定位是 Anthropic 已广泛开放模型中能力最高的一档，尤其适合 demanding reasoning 和 long-horizon agentic work。
- 官方发布文强调：任务越长、越复杂，Fable 5 相比旧模型的领先越明显。
- 软件工程方面，官方给出的早期案例包括 Stripe 在 5000 万行 Ruby 代码库里让模型一天完成一次大范围迁移，原本需要一个团队手工两个月以上。
- 官方基准图显示，Claude Fable 5 在 SWE-Bench Pro 为 80.3%，FrontierCode Diamond 为 29.3%，Terminal-Bench 2.1 为 88.0%。
- Fable 5 的视觉能力提升明显，官方示例包括从复杂截图重建 Web App 源码。
- Fable 5 在长上下文、长任务和持久文件记忆场景中更强，官方提到它能跨数百万 tokens 保持专注，并利用自己的笔记改进输出。

## API 与接入要点

- API model ID：`claude-fable-5`；Mythos 5 的 ID 是 `claude-mythos-5`，但受限访问。
- Fable 5 在 Claude API、Claude Platform on AWS、Amazon Bedrock、Vertex AI、Microsoft Foundry 上从 2026-06-09 起可用。
- 默认支持 1M token context window，单次请求最大 128k output tokens。
- 价格：10 美元 / 百万输入 token，50 美元 / 百万输出 token。
- Adaptive thinking 常开，`thinking: {"type": "disabled"}` 不支持；应使用 `effort` 控制智能、延迟和成本。
- 原始 chain-of-thought 不返回；可用 summarized thinking。
- Fable 5 有安全分类器。被拒绝时 Messages API 返回 HTTP 200，但 `stop_reason` 为 `refusal`，不是普通异常。
- 可使用 `fallbacks` 参数或 SDK middleware，把被拒绝请求重试到其他模型；拒绝发生在输出前时不计费。
- Fable 5 使用 Opus 4.7 引入的新 tokenizer，相比更早模型，同样文本大约多 30% tokens，应重新用 token counting API 测量上下文和成本。
- Fable 5 和 Mythos 5 要求 30 天数据保留，不支持 Zero Data Retention。对企业代码、客户数据和受监管数据要提前确认合规边界。

## Claude Code 相关

- Claude Code CHANGELOG 2.1.170 写明：更新到 2.1.170 可访问 Claude Fable 5。
- Claude Code 2.1.154 已引入 dynamic workflows 和 Opus 4.8 高 effort 相关能力；Fable 5 更适合把这类长任务、多 agent、长运行工作流跑得更稳。
- Fable 5 prompting 文档强调它适合 hours/days/weeks 级任务，不应用只测简单任务来低估能力。
- 文档建议：长任务要调整超时、流式输出、进度提示和异步检查机制；高 effort 可能会过度计划或做额外重构，需要在 prompt 中明确边界。

## 写作主线

- 这次“Claude 5”对程序员的意义，不是代码补全更快，而是能把任务粒度从“帮我写函数”推到“帮我完成迁移、审查、排查、验证”。
- 最值得关注的是长任务自治、长上下文、视觉理解、代码审查和 debugging recall。
- Fable 5 不是所有任务都该默认使用：价格更高、长任务延迟更高、数据保留要求更严格、安全分类器可能误伤部分安全研究请求。
- 实用建议：日常小修小补继续用便宜快的模型；跨仓库迁移、疑难 bug、重构验证、截图转实现、长链路 agent 任务再上 Fable 5。
- API 迁移不是只改 model 字符串，还要补 `effort`、`refusal`、fallback、token 预算、数据保留检查。

## 参考资料

- Anthropic 官方发布：https://www.anthropic.com/news/claude-fable-5-mythos-5
- Claude API Docs - Introducing Claude Fable 5 and Claude Mythos 5：https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
- Claude API Docs - Context windows：https://platform.claude.com/docs/en/build-with-claude/context-windows
- Claude API Docs - Effort：https://platform.claude.com/docs/en/build-with-claude/effort
- Claude API Docs - Prompting Claude Fable 5：https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5
- Claude API Docs - API and data retention：https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
- Claude Code CHANGELOG：https://github.com/anthropics/claude-code/raw/refs/heads/main/CHANGELOG.md

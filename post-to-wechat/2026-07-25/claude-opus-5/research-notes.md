---
title: "Claude Opus 5 官方发布资料"
source: "https://www.anthropic.com/news/claude-opus-5"
tags:
  - type/source
  - topic/claude-code
  - topic/agent-runtime
  - topic/agent-design
moc:
  - "[[claude-code]]"
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[post-to-wechat/2026-07-25/claude-opus-5/article]]"
---

# Claude Opus 5 官方发布资料

核验日期：2026-07-25（Asia/Singapore）

## 一手来源

- Anthropic 发布公告：https://www.anthropic.com/news/claude-opus-5
- Opus 产品页：https://www.anthropic.com/claude/opus
- 模型文档：https://platform.claude.com/docs/en/about-claude/models/overview
- System Card：https://www.anthropic.com/news/claude-opus-5 （公告内链接）

## 已核验事实

- 发布时间：2026-07-24。
- API model ID：`claude-opus-5`。
- 定价：每百万输入 token 5 美元、输出 token 25 美元，与 Opus 4.8 相同。
- Fast mode：官方称约为默认速度的 2.5 倍，价格为基础价格的 2 倍。
- 定位：接近 Fable 5 的前沿能力，但成本约为后者一半；Claude Max 的默认模型、Claude Pro 可用的最强模型。
- 可用范围：Claude.ai、Claude Code、Claude Cowork、Claude Platform，以及 AWS、Google Cloud、Microsoft Foundry。
- effort settings：可按任务在智能上限、token 消耗、延迟和成本之间取舍。
- 新 beta：会话中途修改工具而不破坏 prompt cache；安全分类器触发时可自动回退。
- 安全回退：在 Claude.ai、Claude Code、Claude Cowork 中，部分被安全分类器拦截的请求默认回退到 Opus 4.8；API 可选择启用自动回退。
- 官方边界：Opus 5 在网络安全能力上仍落后 Mythos 5；在长时程自主生物研究任务上仍有重要限制。

## 可用于文章的官方评测

- Frontier-Bench v0.1：官方称 Opus 5 超过其他模型，并以更低的单任务成本把 Opus 4.8 的表现提高到两倍以上。
- CursorBench 3.2：max effort 下与 Fable 5 峰值相差 0.5%，单任务成本约一半。
- ARC-AGI 3：官方称得分约为次优模型的 3 倍。
- Zapier AutomationBench：相同单任务成本下，通过率约为次优模型的 1.5 倍。
- OSWorld 2.0：官方称以略高于 Fable 5 三分之一的成本超过其最佳结果。

以上均来自 Anthropic 发布材料，不能写成独立第三方结论。具体图表和 harness 条件应以官方公告脚注及 System Card 为准。

## 文章判断

- Opus 5 的工程价值不只是峰值分数，而是把“高难任务的能力、验证倾向、可控 effort、可用价格”放进同一个日常模型。
- 不建议无差别替换所有任务。分类、抽取、简单改写等稳定任务仍可留在更便宜的模型；跨文件重构、根因分析、长链工具任务、专业研究更值得 A/B。
- effort 应当按任务价值分档，而不是全局拉满。
- 自动回退会改变审计语义。生产系统应记录实际执行模型，避免把 Opus 4.8 的结果误记为 Opus 5。


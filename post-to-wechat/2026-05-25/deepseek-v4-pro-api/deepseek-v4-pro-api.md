---
title: 炸裂！DeepSeek 1M接入
author: 蒸馏小余
summary: DeepSeek-V4-Pro 支持 1M 上下文，官方文档给出 Claude Code 接入方式；价格页当前显示折扣到 5 月 31 日。
cover: imgs/01-deepseek-v4-pro-1m.png
source_url: https://x.com/deepseek_ai/status/2048062777357750316
docs_pricing_url: https://api-docs.deepseek.com/quick_start/pricing
docs_claude_code_url: https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code
---

![](imgs/01-deepseek-v4-pro-1m.png)

这条 DeepSeek 官方更新，最值得看的不是促销，而是 V4-Pro 的 1M 上下文已经能接进 Claude Code。

价格以官方 pricing 页为准：我在 2026-05-25 核对时，DeepSeek-V4-Pro 仍显示 75% off 到 2026-05-31 15:59 UTC，也就是北京时间 5 月 31 日 23:59。

怎么试：先拿 DeepSeek API Key；再把 Claude Code 的 `ANTHROPIC_BASE_URL` 指到 DeepSeek Anthropic API，把 `ANTHROPIC_MODEL` 设成 `deepseek-v4-pro[1m]`；最后进项目跑 `claude`。

OpenCode 记得升到 v1.14.24+，OpenClaw 升到 v2026.4.24+。适合大仓库读代码、长上下文排查、批量改动前先吃完整背景。

来源：DeepSeek 官方 X 与 API Docs（2026-05-25 访问）

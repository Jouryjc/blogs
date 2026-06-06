---
title: DeepSeek 1M接入
author: 蒸馏小余
summary: DeepSeek 官方文档给出了 V4-Pro 在 Claude Code 中的接入方式，核心是 Anthropic API 格式和 deepseek-v4-pro[1m] 模型名。
cover: imgs/01-deepseek-v4-pro-1m.png
---

![](imgs/01-deepseek-v4-pro-1m.png)

DeepSeek 官方文档给出了 V4-Pro 在 Claude Code 中的接入方式。

核心配置很简单：Base URL 走 DeepSeek 的 Anthropic API 格式，模型名设为 `deepseek-v4-pro[1m]`。

适合大仓库读代码、长上下文排查、批量改动前先补全项目背景。

来源：DeepSeek 官方 X 与 API Docs（2026-05-25 访问）

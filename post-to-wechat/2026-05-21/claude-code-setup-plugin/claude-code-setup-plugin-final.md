---
title: 项目自动化配置
author: 蒸馏小余
summary: 先读项目结构和依赖，再推荐适合当前仓库的自动化配置。
cover: imgs/01-claude-code-setup.png
---

![](imgs/01-claude-code-setup.png)

Claude Code Setup 的价值，不是“又多一个插件”，而是把配置前的诊断流程标准化。

它先看仓库结构、依赖和代码模式，再推荐适合当前项目的自动化配置。

可以把它理解成 5 类建议：

- MCP servers：接外部工具和数据源
- Skills：沉淀可复用流程
- Hooks：在关键节点自动检查
- Subagents：把专项任务分出去
- Slash commands：把常用动作变成命令

小余判断：这类工具最适合三种场景：

1. 新项目接手，不知道先配什么。
2. 老项目补 AI 工程化，不想凭感觉加配置。
3. 团队要统一 Claude Code 工作流。

别一开始追求全套。先让它读项目，再挑最值钱的 1-2 个自动化建议落地。

来源：Anthropic Claude Code Setup 插件页（2026-05-21 访问）

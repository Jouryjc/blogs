---
title: 炸裂！claude-code-setup
author: 蒸馏小余
summary: 一个命令让 Claude 先读懂你的仓库，再告诉你最该配置哪些 MCP、Skills、Hooks、Subagents 和 slash commands。
cover: imgs/01-claude-code-setup.png
---

![](imgs/01-claude-code-setup.png)

这个插件最狠的地方，不是“又多了一个配置项”。

而是它把 Claude Code 新手最痛的一步自动化了：

**先读懂你的仓库，再告诉你该装什么。**

安装命令很直接：

`claude plugin install claude-code-setup@claude-plugins-official`

装好之后，在项目里问：

`recommend automations for this project`

它会只读分析你的项目结构、依赖、语言文件和代码模式，然后给出 5 类建议：

- MCP：该接哪些外部工具
- Skills：哪些流程值得沉淀
- Hooks：哪些节点该自动检查
- Subagents：哪些专项任务该分出去
- Slash commands：哪些常用动作该变命令

真正好用的点是：它不是甩给你一堆大而全清单，而是每类先挑 1-2 个最值得做的。

比如 React 项目，可能先推荐 Playwright MCP；如果发现认证相关代码，可能建议安全审查类 subagent。

我的用法会很简单：

1. 新项目接手，先跑一遍。
2. 只选最痛的 1-2 个建议落地。
3. 验证有效后，再写进团队规则文件。

小余判断：这东西适合所有还在手配 Claude Code 的项目。别再凭感觉堆配置了，先让它扫一遍仓库，你会更快知道第一刀该切哪里。

来源：Anthropic Claude Code Setup 插件页（2026-05-21 访问）

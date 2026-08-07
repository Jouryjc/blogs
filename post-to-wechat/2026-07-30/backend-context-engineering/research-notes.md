---
title: "Backend Context Engineering research notes"
source: "https://x.com/_avichawla/status/2063548691353629040"
source_author: "Avi Chawla"
tags:
  - type/source
  - topic/context-engineering
  - topic/agent-runtime
  - topic/agent-design
moc:
  - "[[context-engineering]]"
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[post-to-wechat/2026-07-30/backend-context-engineering/backend-context-engineering]]"
---

# 素材核验

## 原始 X Article

- 标题：How to cut Claude Code costs by 2.5x (using Karpathy's context engineering principles)
- 作者：Avi Chawla（@_avichawla）
- 发布时间：2026-06-07
- 主张：同一套 DocuRAG 功能、同一生成与嵌入模型，在作者的两次 Claude Code 构建中，Firebase 路线消耗 15.7M tokens、$12.95；InsForge 路线消耗 6.3M tokens、$4.87。
- 原文归因：Firebase 路线需要更碎片化的状态发现、更多人工介入、更多文件返工；InsForge 用 Skills 承载静态知识、CLI 执行操作、结构化 metadata 暴露实时状态。
- 重要边界：这是作者的一次对照项目，不是通用 benchmark；两套后端能力边界、默认组件与成熟度并不完全等价。

## 一手资料核验

- Firebase 官方 MCP 文档确认：MCP server 同时暴露 prompts、tools 和 documentation resources，并支持 `--only` 限制启用的 feature groups。
- Firebase 官方文档也建议 MCP 与 Agent Skills 配合，以更低成本完成复杂任务。
- InsForge GitHub 将项目定位为面向 agentic coding 的开源后端，仓库采用 Apache-2.0 许可证。
- MCPMark 论文用于说明真实 MCP 任务通常需要多轮执行与多次工具调用；原帖引用的 Sonnet 4.5/4.6 具体 token 数来自作者转述，本文不把它当作本文对照实验的独立结论。

## 写作判断

1. 不写成 Firebase 对 InsForge 的产品站队。
2. 把 2.5 倍差距视为一个诊断信号：Agent 在“补上下文”上花了多少成本。
3. 给读者一份可复用的后端 Agent-ready 检查表。
4. 给出低成本改造顺序：先裁工具面，再聚合状态，再结构化错误，最后才换平台。

## 来源

- https://x.com/_avichawla/status/2063548691353629040
- https://github.com/InsForge/InsForge
- https://firebase.google.com/docs/ai-assistance/mcp-server
- https://firebase.google.com/docs/cli
- https://arxiv.org/abs/2509.24002

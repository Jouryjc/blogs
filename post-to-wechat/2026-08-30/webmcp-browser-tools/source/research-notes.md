---
title: "WebMCP 一手资料核查与写作边界"
source: "https://x.com/akshay_pachaar/status/2093452397402317239"
tags:
  - type/source
  - topic/agent-runtime
  - topic/agent-design
moc:
  - "[[agent-runtime]]"
  - "[[agent-design]]"
related:
  - "[[webmcp-clearly-explained]]"
  - "[[post-to-wechat/2026-08-30/webmcp-browser-tools/webmcp-browser-tools]]"
---

# WebMCP 一手资料核查与写作边界

## 五个标题候选

1. 推荐标题：别再让 Agent 猜按钮：WebMCP 把网页能力变成工具
2. 稳妥标题：WebMCP 不是网页里的 MCP：它给浏览器 Agent 一份工具清单
3. 大众标题：网页一改版，Agent 就失灵？浏览器开始给它操作说明
4. 专家标题：从 DOM 猜测到结构化调用：WebMCP 的前端工具层
5. 反差标题：Agent 逛网页，最大问题不在模型，而在页面没说自己会什么

最终采用推荐标题。五个候选覆盖动作提醒、概念辨析、问句、技术路径、反差判断五种句式。

## 已确认事实

- WebMCP 是仍在讨论中的 proposed web standard，不应写成已经普及的稳定标准。
- Chrome 官方文档将其放在 origin trial，并提供本地 flag；官方页面当前写的是从 Chrome 149 加入 origin trial。
- Microsoft Edge 的 Web 平台发布说明也已列出 WebMCP origin trial，但发布节奏和 API 仍可能变化。
- 当前 API 使用 `document.modelContext.registerTool()`；工具包括名称、描述、JSON Schema 和执行函数。
- Declarative API 可通过 `toolname`、`tooldescription` 等 HTML 属性把表单转成工具。
- WebMCP 主要服务于有浏览器 UI、有人在环的本地工作流；不是无头、全自动 Agent 的默认方案。
- WebMCP 与 MCP 互补：前者暴露页面内前端能力，后者更适合后端数据、工具与跨平台工作流。
- WebMCP 可以复用当前页面的状态与会话，但不等于自动授权。服务端鉴权、权限校验、确认步骤仍必须保留。
- 官方安全指南明确提醒间接提示注入风险，并建议使用 `readOnlyHint`、`untrustedContentHint`、可信 origin 白名单和短输出。
- 页面未覆盖的任务仍需回退到 DOM、可访问性树或计算机操作；WebMCP 不会消灭浏览器自动化。

## 原文需要降调的说法

- “Google 和 Microsoft 正在一起构建同一个东西”：改成 Chrome 与 Edge 都把 WebMCP 放进试验轨道，不推断组织层面的共同承诺。
- “nothing to configure”：限定为用户不必为每个站点单独配置后端 MCP；站点仍需开发工具，浏览器与 Agent 也要支持。
- “Login comes for free”：改成页面工具能在当前登录会话中运行，但授权与高风险确认不会自动消失。
- “Any model can use it”：改成任何兼容 WebMCP 的 Agent 都可能使用，实际仍取决于浏览器与客户端支持。
- “cost of trying is close to nothing”：简单表单的原型成本低，复杂状态机、支付和权限流程仍需工程改造与评测。

## 一手来源

- [Chrome WebMCP 概览](https://developer.chrome.com/docs/ai/webmcp)
- [Chrome WebMCP Imperative API](https://developer.chrome.com/docs/ai/webmcp/imperative-api)
- [Chrome WebMCP Declarative API](https://developer.chrome.com/docs/ai/webmcp/declarative-api)
- [Chrome WebMCP 安全指南](https://developer.chrome.com/docs/ai/webmcp/secure-tools)
- [Chrome：WebMCP 与 MCP 的边界](https://developer.chrome.com/docs/ai/webmcp/compare-mcp)
- [Web Machine Learning Community Group 的 WebMCP explainer](https://github.com/webmachinelearning/webmcp)
- [Microsoft Edge Web 平台发布说明](https://learn.microsoft.com/en-us/microsoft-edge/web-platform/release-notes/153)


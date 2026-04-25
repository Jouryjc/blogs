Create a technical architecture diagram showing Ralph Orchestrator's hub-and-spoke design.

Layout (16:9 landscape), three horizontal tiers connected by vertical arrows:

TOP TIER - "用户接口层" (User Interface Layer):
5 rounded rectangle boxes arranged horizontally, each with a small icon:
- CLI (terminal icon)
- TUI (monitor icon)
- Web Dashboard (browser icon)
- MCP Server (plug icon)
- Telegram Bot (chat bubble icon)

All 5 boxes have dotted lines connecting to a sidebar element on the right labeled ".ralph/ 共享状态" (Shared State) with a folder icon - emphasizing all interfaces share the same state directory.

MIDDLE TIER - The central hub, visually prominent and larger:
A rounded rectangle with a gear/brain icon: "ralph-core 核心编排引擎" (Core Orchestration Engine)
Below it, a thinner bar: "ralph-adapters 后端抽象层" (Backend Abstraction Layer)

BOTTOM TIER - "AI 后端" (AI Backends):
7 small boxes arranged horizontally with provider logos/icons:
Claude, Kiro, Gemini, Codex, Amp, Copilot, OpenCode

Arrows flow: Top tier → Middle hub → Bottom tier (bidirectional)

The visual emphasis should be on the center hub and the shared state concept. Use varying shades of blue for the tiers, with the center hub being the most prominent.

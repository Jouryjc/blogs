# Research Notes: MCP vs Skills 之争与混合架构共识

调研日期：2026-07-12
选题来源：`reports/x-hot-ai-agent-engineering/2026-07-12.md` Rank 3

## 来源清单

1. Frank's World（Frank La Vigne，2026-07-07，基于 IBM Technology 视频）
   https://www.franksworld.com/2026/07/07/navigating-ai-agent-extensions-mcp-vs-skills/
2. BrightCoding（2026-07-08，介绍 Muratcan Koylan 的 Agent Skills for Context Engineering 项目）
   https://www.blog.brightcoding.dev/2026/07/08/agent-skills-the-context-engineering-revolution
3. InfoWorld《The role of MCP in context engineering》
   https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html
4. Firecrawl《MCP vs CLI for AI Agents》（35% 数字的出处）
   https://www.firecrawl.dev/blog/mcp-vs-cli
5. Analytics Vidhya《MCP vs. Agent Skills: Why You Need Both for AI Agents》（"神经系统 / 行动手册"比喻出处）
   https://www.analyticsvidhya.com/blog/2026/04/mcp-vs-agent-skills/

---

## 事实与数字（均注明出处）

### 争论背景 / 唱衰 MCP

- Peter Steinberger（OpenClaw 作者）2026 年 1 月发文："mcp were a mistake. bash is better"。他谈的是 ergonomics（易用性）而非能力上限；随后他做了把 MCP 转成 CLI 的工具 MCPorter，后被 OpenAI 聘用。
  来源：https://www.firecrawl.dev/blog/mcp-vs-cli
- 2026-07-07 ~ 07-08 一周内 Frank's World、BrightCoding、InfoWorld 等多篇博客同周讨论 MCP vs Skills。
  来源：reports/x-hot-ai-agent-engineering/2026-07-12.md

### MCP 使用量增长数据

- "Firecrawl's own MCP usage grew roughly 35% in a single month"（2026 上半年，Firecrawl 单一产品数据）；原文补充 "One product in a sea of many, but that kind of growth is hard to dismiss as noise"。
  来源：https://www.firecrawl.dev/blog/mcp-vs-cli
  ⚠️ 注意：35% 是 Firecrawl 自家产品的 MCP 使用量月增，不是全生态数字，正文表述必须带出处限定。
- Bloomberry 对 1,400 个 MCP 服务器的分析：2025 年 8 月至 2026 年 2 月增长 232%；工具读操作与写操作比例约 2:1。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html （引 Bloomberry：https://bloomberry.com/blog/we-analyzed-1400-mcp-servers-heres-what-we-learned/）
- Zuplo《MCP 状态报告》（2026 年初）：63% 的 MCP 用户用 MCP 服务器访问文档、知识库等数据源；"提供更好的 AI 上下文"是 MCP 最常见的价值主张。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html

### MCP 是什么 / 擅长什么

- MCP 是标准化 AI 模型与外部数据源交互的中间层，"将 AI 模型请求转化为可执行的 POST 或 GET 命令"，负责身份验证与数据隐私。
  来源：https://www.franksworld.com/2026/07/07/navigating-ai-agent-extensions-mcp-vs-skills/
- MCP 解决 N×M 集成问题：5 个 agent × 5 个后端 = 25 个定制集成，MCP 统一成一个协议层；独立进程 + JSON-RPC 严格类型参数；支持工具链（Tool A 输出接 Tool B 输入）。
  来源：https://www.analyticsvidhya.com/blog/2026/04/mcp-vs-agent-skills/
- MCP 适合实时数据访问 + 严格权限控制的场景（CRM 查询、虚拟机监控等）；适合高频低延迟操作（GitHub、PostgreSQL、Stripe、Slack）。
  来源：https://www.franksworld.com/2026/07/07/navigating-ai-agent-extensions-mcp-vs-skills/ ；https://www.analyticsvidhya.com/blog/2026/04/mcp-vs-agent-skills/
- 企业治理：Merge 联合创始人兼 CTO 表示 MCP"实施得当的话，能够强制执行策略驱动的访问控制"，例如防止低级别工程师通过 agent 访问自己无权限的日志。企业最佳实践：建立内部审查过的 MCP 注册表。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html
- 对比传统 RAG：Sonar 产品经理指出预索引快照"在快速变化的环境中很快过时"，MCP 提供实时检索。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html
- InfoWorld 展望：MCP 式抽象将像早期的 REST 一样成为标准基础设施，充当 AI 系统与数据之间的"控制平面"；"context is king"。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html

### Skills 是什么 / 擅长什么

- Skills 是领域知识的封装：markdown 文件（SKILL.md）+ 元数据，"自包含、可复用的单元"；本地文件夹结构（SKILL.md + scripts/ + examples/），通过 shell（bash/python）执行，无需额外基础设施。
  来源：https://www.franksworld.com/2026/07/07/navigating-ai-agent-extensions-mcp-vs-skills/ ；https://www.analyticsvidhya.com/blog/2026/04/mcp-vs-agent-skills/
- Skills 适合重复性预定义任务：代码调试、数据分析、合规检查，以及保证输出格式一致性（例：销售团队要求统一数据格式）。
  来源：https://www.franksworld.com/2026/07/07/navigating-ai-agent-extensions-mcp-vs-skills/
- Progressive disclosure（渐进式披露）：启动时只加载技能名称和描述（<200 tokens，对比传统提示库 2000+ tokens），触发关键词后才加载完整技能内容（2000+ tokens 的专业知识）。
  来源：https://www.blog.brightcoding.dev/2026/07/08/agent-skills-the-context-engineering-revolution
- Token 效率：生产用户报告 compression + filesystem 技能组合带来 60-80% token 使用量减少；一个生产客服机器人案例：70% token 节省、零 lost-in-the-middle 故障。
  来源：https://www.blog.brightcoding.dev/2026/07/08/agent-skills-the-context-engineering-revolution
- 跨工具复用：平台无关设计，支持 Claude Code、Cursor 及任何自定义指令平台。
  来源：https://www.blog.brightcoding.dev/2026/07/08/agent-skills-the-context-engineering-revolution
- BrightCoding 介绍的项目本身包含 13 个技能、5 大类别（Muratcan Koylan 的 Agent-Skills-for-Context-Engineering）。
  来源：https://www.blog.brightcoding.dev/2026/07/08/agent-skills-the-context-engineering-revolution

### 失败模式相关数据

- MCP 的 token 成本（Scalekit 基准测试，经 Firecrawl 引用）：CLI 约 200 tokens/命令，MCP 约 32,000–82,000 tokens/操作；月 1 万次操作成本 CLI 约 $3.20 vs MCP 约 $55.20；一个 800-token 的技能文件可替代 28,000 tokens 的 MCP 架构；可靠性对比 CLI 100% 成功率 vs 原始 MCP 实现 72%。
  来源：https://www.firecrawl.dev/blog/mcp-vs-cli
- 挂太多 MCP 服务器会显著增加 LLM 输入；Claude Code 的工具搜索功能可将工具定义 token 从 51k 降到 8.5k；Spacelift 解决方案架构师："MCP 工具仅靠确保使用正确的内容就能节省数千 token"。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html
- 信任背景：Sonar 2026《开发者代码状态调查》：96% 的开发者不完全信任 AI 编码输出；2025 年底 StackOverflow 调查：近 50% 开发者对"几乎正确但不完全正确"的 AI 方案感到沮丧。
  来源：https://www.infoworld.com/article/4175336/the-role-of-mcp-in-context-engineering.html

### 互补共识 / 比喻

- Analytics Vidhya 结论："MCP scales your systems. Agent Skills scale your agent's behavior."；"If you aren't using both, you're building half an agent."
  比喻措辞：MCP 提供 "standardized nervous system"（标准化神经系统，连接世界），Skills 提供 "mental playbooks"（行动手册，指导行为）。
  来源：https://www.analyticsvidhya.com/blog/2026/04/mcp-vs-agent-skills/
- Frank's World 结论：两者都是"强大的 LLM 扩展"，按项目特性混合运用——MCP 主导数据密集 / 权限敏感环境，Skills 保证领域输出一致性。
  来源：https://www.franksworld.com/2026/07/07/navigating-ai-agent-extensions-mcp-vs-skills/
- Firecrawl 结论：混合模式胜出——"内循环"（本地开发、高频日常操作）用 CLI/轻量方式，"外循环"（企业多租户集成、OAuth、审计）用 MCP。
  来源：https://www.firecrawl.dev/blog/mcp-vs-cli
- BrightCoding：Skills 与 MCP 互补而非取代，tool-design 技能本身就实现 MCP 标准——框架级工具连接归 MCP，agent 级上下文策略归 Skills。
  来源：https://www.blog.brightcoding.dev/2026/07/08/agent-skills-the-context-engineering-revolution

## 表述纪律备忘

- "35%" 只能表述为：Firecrawl 披露自家 MCP 使用量单月增长约 35%（并可引 "hard to dismiss as noise"）。
- 生态级增长数据用 Bloomberry 232%（2025.8–2026.2，1400 个服务器样本）。
- "神经系统 / 行动手册" 比喻出处是 Analytics Vidhya（nervous system / mental playbooks），周报将其概括为社区共识。
- 60-80% token 节省是 BrightCoding 报道的该技能库生产用户数据，不是所有 Skills 的普适数字。

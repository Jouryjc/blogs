# Research Notes: OpenAI 7/9 发布 — ChatGPT Work agent + GPT-5.6 + Codex 并入桌面端

调研日期：2026-07-12 ~ 2026-07-13
本篇文章：wechat-drafts/2026-07-12-openai-work-agent/article.md

## 来源清单

1. 9to5Mac 发布会报道：https://9to5mac.com/2026/07/09/openai-announcing-the-next-chapter-for-chatgpt-today-watch-here/
2. Codex 官方 changelog（developers.openai.com/codex/changelog 已 308 跳转至）：https://learn.chatgpt.com/docs/changelog
3. TechCrunch Claude Cowork 报道（7/7）：https://techcrunch.com/2026/07/07/the-coding-agent-wars-are-spilling-into-the-rest-of-the-office-claude-cowork/
4. OpenAI 官方博客《Codex is becoming a productivity tool for everyone》：https://openai.com/index/codex-for-knowledge-work/ （直接抓取 403，数据经下述二手来源交叉核实）
5. Constellation Research 对官方数据的报道：https://www.constellationr.com/insights/news/openai-touts-broadening-codex-usage-5-million-weekly-active-users
6. Releasebot 汇总的 Codex 更新（rollout budget / delegation 原文）：https://releasebot.io/updates/openai/codex
7. Codex rollout budget 实现 PR：https://github.com/openai/codex/pull/28494
8. 本仓库周报：reports/x-hot-ai-agent-engineering/2026-07-12.md（Rank 4、Rank 5 条目）

## 一、7 月 9 日发布会（来源 1：9to5Mac）

- **ChatGPT Work agent**：新 AI 代理，覆盖网页、移动、桌面三端；OpenAI 描述为"为最雄心勃勃工作而打造的 ChatGPT"（"ChatGPT built for your most ambitious work"意译）。
- **GPT-5.6 三个模型**：
  - Sol：旗舰模型
  - Terra：日常工作平衡模型
  - Luna：快速且经济模型
  - 命名规则（OpenAI 表述）："数字标识模型代际，而 Sol、Terra 和 Luna 标识可独立发展的能力层级"。
- **API 定价**（每百万 token，输入/输出）：
  - Sol：$5 / $30
  - Terra：$2.50 / $15
  - Luna：$1 / $6
- **可用性**：
  - Chat 应用：Plus、Pro、Business、Enterprise 用户可用 GPT-5.6 Sol（中等及更高难度设置）。
  - ChatGPT Work 和 Codex：免费及 Go 用户可用 Terra；Pro 和 Enterprise 用户可选 Sol/Terra/Luna 并设置难度级别。
  - "ultra" 加速模式：仅 Pro 和 Enterprise 用户在 ChatGPT Work 中可用。
- **Codex 并入 ChatGPT 桌面端**（macOS/Windows）：现有 Codex 用户保留项目、设置和工作流；新增 Markdown 编辑、GitHub PR 审查、跨仓库项目工作。
- **GPT-5.4 将于 7 月 23 日停用**。

## 二、Codex 用量数据（来源 4/5，OpenAI 官方数据，2026-06-02 公布）

- Codex 周活用户**超过 500 万**（"more than 5 million weekly active users"）。
- **知识工作者约占 20%**，即约 100 万非开发者用户；该群体增速快于开发者（Constellation 转述：增长迅速；另有多来源称约为开发者增速 3 倍，本文只采信"约 20%、增长更快"的保守表述）。
- 使用场景（OpenAI 原话，Constellation 转引）："知识工作者主要使用 Codex 创建报告、电子表格、演示文稿、合同及其他工作产品。他们还越来越多地将其用于研究、数据分析、工作流自动化和构建轻量级工具。"
- 注意：**500 万周活数据的官方公布日期是 6 月 2 日**，早于 7/9 发布会约五周；文章表述为"6 月初官方公布"，不绑定在发布会当天。
- 周报（来源 8）将"周活超 500 万、100 万+ 非编程用户"记为官方数据，与上述一致（100 万 = 500 万 × 20% 推算，文中写"约 100 万"）。

## 三、Codex changelog 工程化更新（来源 2/6/7）

### v0.144.0（2026-07-09）
- Codex 并入 ChatGPT 桌面端："Codex is now part of the ChatGPT desktop app on macOS and Windows"。
- Computer Use 提速："Made Computer Use faster with GPT-5.6"。
- 多代理并发成本警告："Selecting Ultra reasoning now warns when high multi-agent concurrency could increase usage quickly"。
- usage-limit reset credits："Usage-limit reset credits now show their type and expiration"，并支持选择兑换哪一笔额度。
- MCP 工具可交互式请求认证，无需实验性标志。
- GitHub PR 侧边栏审查："Review GitHub pull requests in the sidebar... without leaving the app"。
- token budget 相关内部改动："core: raise token budget message limits"（#29970）、"core: wrap token budget window context"（#29494）。

### v0.143.0（2026-07-08）
- 远程插件默认启用："Remote plugins are now enabled by default, with richer catalog rows, npm marketplace sources, and visible remote/local versions"。
- 委派授权入口："allow AGENTS.md and skills to authorize delegation"（#30274）。
- Amazon Bedrock 上线 GPT-5.6 Sol/Terra/Luna，"first-class support for max reasoning effort"。
- MCP 工具默认使用 tool search。
- 系统代理支持（macOS/Windows，PAC/WPAD）。

### v0.142.x（2026-06-22 / 06-25）
- **rollout token budgets**（v0.142.0，2026-06-22，来源 6）："Configurable rollout token budgets track usage across agent threads, provide remaining-budget reminders, and abort turns when exhausted."（可配置的 rollout token 预算：跨 agent 线程追踪用量、剩余预算提醒、耗尽时中止本轮）相关 PR：#28746、#28494、#28707、#29423。配置项含 limit_tokens、reminder_interval_tokens、sampling_token_weight、prefill_token_weight，提醒间隔默认为预算上限的 10%（来源：WebSearch 对 changelog/PR 的摘要；配置项细节在 releasebot 页面未复核，文中不写具体参数名，仅写机制）。
- **多智能体委派控制**（v0.142.0，2026-06-22，来源 6）："App-server clients can configure multi-agent delegation as disabled, explicit-request-only, or proactive at the thread and turn level."（委派可配置为禁用 / 仅显式请求 / 主动，粒度到 thread 和 turn 级）
- **插件浏览器改进**（v0.142.0，来源 6）："/plugins now organizes remote plugins into OpenAI Curated, Workspace, and Shared with me sections, while eligible turns can recommend and install relevant plugins."
- **Codex Remote GA + DigitalOcean 插件**（v0.142.2，2026-06-25，来源 2/6）："The new DigitalOcean plugin lets Codex provision a DigitalOcean Droplet, configure SSH access, and connect it to the Codex App as a remote workspace."；Codex Remote 正式可用，iOS/Android 管理 Mac/Windows 主机，QR 一对一配对认证。

> 时间线注意：rollout token 预算、委派三档控制、DigitalOcean 插件均在 6 月下旬版本先行落地，7/8-7/9 的 0.143/0.144 继续加码（AGENTS.md/skills 授权委派、并发成本警告、reset credits）。文中表述为"过去三周的连续更新"，不把 6 月功能说成 7/9 当天发布。

## 四、Anthropic 对照（来源 3，TechCrunch，2026-07-07）

- Claude Cowork 自 7 月 7 日（周二）起向 **Max 订阅用户**开放网页端和移动端（原文："starting Tuesday it is available on web and mobile for Max subscribers"）。
- 跨设备接力（原文）："start a task from their desk, get status updates on their phone, and pick up the finished output later"。桌面应用保留深度能力（本地文件与浏览器访问）。
- 官方用量数据：来自 **60 万+ 组织**的 **120 万条**匿名聚合会话（采样期为 5 月最后两周）：
  - 业务流程运营 33.4%（报告整合、清单构建、电子表格协调）
  - 内容创作与文案 16.4%（草稿、幻灯片、社交帖子、提案）
  - 软件开发 8.7%
- TechCrunch 对 Codex 的描述："began as a software development tool but is increasingly being used by non-developers for reports, spreadsheets, presentations, research, data analysis"。
- Anthropic 表述："the use of AI for everyday business work is on the rise"；Cowork 定位为处理"工作周围的工作"的管理助手。

## 五、文中每个数字的出处对照

| 文中事实/数字 | 出处 |
|---|---|
| 7/9 发布会三件事（Work agent / GPT-5.6 / Codex 并入桌面端） | 来源 1 |
| GPT-5.6 Sol/Terra/Luna 命名与定价（$5/$30、$2.5/$15、$1/$6） | 来源 1 |
| GPT-5.4 于 7 月 23 日停用 | 来源 1 |
| ultra 加速模式限 Pro/Enterprise（ChatGPT Work） | 来源 1 |
| Codex 周活超 500 万；知识工作者约 20%（约 100 万） | 来源 4/5（官方数据，6/2 公布） |
| 知识工作者场景：报告/表格/PPT/合同/研究/数据分析/工作流自动化/轻量工具 | 来源 5（转引官方） |
| "Made Computer Use faster with GPT-5.6" | 来源 2（v0.144.0） |
| rollout token 预算机制（追踪/提醒/中止） | 来源 6（v0.142.0）、来源 7 |
| 委派三档：disabled / explicit-request-only / proactive，thread+turn 级 | 来源 6（v0.142.0） |
| AGENTS.md 和 skills 可授权委派 | 来源 2（v0.143.0，#30274） |
| Ultra reasoning 高并发用量警告 | 来源 2（v0.144.0） |
| reset credits 显示类型/过期、可选择兑换 | 来源 2（v0.144.0） |
| DigitalOcean 插件（Droplet+SSH+远程工作区） | 来源 2/6（v0.142.2，6/25） |
| /plugins 三分区（OpenAI Curated / Workspace / Shared with me） | 来源 6（v0.142.0） |
| MCP 工具默认 tool search、交互式认证 | 来源 2（v0.143.0 / v0.144.0） |
| Cowork：7/7 上线网页/移动端，Max 订阅 | 来源 3 |
| Cowork 数据：60 万+ 组织、120 万会话、33.4%/16.4%/8.7% | 来源 3 |

## 六、谨慎处理 / 不写入文章的内容

- "增长 6x since February desktop app launch"、"知识工作者增速 3x"：出现在部分二手来源，Constellation 明确说未提及，**不写入正文**。
- "6 million active users by mid-July"：仅个别聚合站提及，无法核实，**不写**。
- rollout budget 的具体配置参数名（limit_tokens 等）：来自搜索摘要，未在权威页面逐字复核，正文只写机制不写参数名。
- 500 万周活是 6 月 2 日公布的数据，正文明确写"6 月初"，不说成发布会当天公布。

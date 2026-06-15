为同一篇微信公众号技术文章生成 5 张正文信息图。请一次性生成 5 个独立 raster 图片文件，并保存到指定输出目录。不要生成封面图。

统一视觉风格：
- 蒸馏小余知识卡 / Deep Research Sketchnote / hand-drawn technical explainer infographic。
- 暖米白 / 奶油纸底，深海军蓝手绘描边，低饱和 pastel 便签卡片。
- 中文短标签，手机端可读。
- 不要真实公司 Logo，不要复制 OpenAI 或 Anthropic 标志；可以使用文字标签「Codex」「Claude」。
- 不要企业 PPT，不要写实，不要 3D，不要暗色赛博风，不要复杂小字。
- 每张图都要有底部 takeaway summary。
- 每张图只出一版，不要反复重生成；如果视觉方向满足提示，就直接保存。

输出文件要求：
1. `01-capability-stack.png`
2. `02-codex-claude-map.png`
3. `03-plugin-bom.png`
4. `04-permission-gates.png`
5. `05-rollout-loop.png`

图片 1：`01-capability-stack.png`
主题：AI 编程工具能力栈：从规则到分发。
结构：自下而上 6 层堆叠：
1. Prompt：临时约束
2. AGENTS.md / CLAUDE.md：项目规则
3. Skill：可复用工作流
4. Plugin：安装与分发
5. MCP / Hook：外部工具与强制检查
6. Managed Policy：组织边界
右侧箭头：「越往上，越需要治理」
底部 takeaway：「先分层，再装能力」

图片 2：`02-codex-claude-map.png`
主题：Codex 与 Claude 的插件管理地图。
结构：左右两栏对照。
左栏「Codex」：`.agents/skills`、`.codex-plugin/plugin.json`、repo marketplace、requirements / permissions、MCP in config.toml。
右栏「Claude Code」：`.claude/skills`、`.claude-plugin/plugin.json`、enabledPlugins、strictKnownMarketplaces、OAuth scopes / hooks。
中间结论卡片：「Skill 是方法，Plugin 是分发」
底部 takeaway：「文件名不同，治理问题相同」

图片 3：`03-plugin-bom.png`
主题：Plugin BOM：企业共享前必须补齐的字段。
结构：中央手绘表格，标题「Plugin BOM」。
三组字段：
- 责任：Owner、Scope、Source、Version
- 风险：Components、Permissions、Data
- 交付：Test prompts、Rollback、Audit
右上角放放大镜和复选框。
底部 takeaway：「说不清 BOM，就不要进共享范围」

图片 4：`04-permission-gates.png`
主题：权限闸门：从来源到审计逐层收口。
结构：从左到右 5 道闸门：
1. Marketplace 来源
2. 安装范围
3. MCP 工具与 scopes
4. Hook 强制检查
5. Analytics / Audit
上方是「Plugin 能力包」穿过五道闸门进入「团队可用能力」。
底部 takeaway：「权限前置，事故才不会后补」

图片 5：`05-rollout-loop.png`
主题：企业插件落地五步：从试点到治理闭环。
结构：闭环流程，5 个节点：
1. 盘点重复工作
2. 项目级试点
3. 封装成 Plugin
4. 受控分发
5. 治理与清理
每个节点下面加短动作词：「找高频」「测触发」「补 BOM」「控来源」「看指标」
中央图标：内部插件市场 + 工程师 + 审计表。
底部 takeaway：「发布不是终点，维护才是插件治理」

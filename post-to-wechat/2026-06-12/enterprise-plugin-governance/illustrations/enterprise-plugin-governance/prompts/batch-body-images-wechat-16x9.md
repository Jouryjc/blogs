为同一篇微信公众号技术文章重新生成 5 张正文信息图。请一次性生成 5 个独立 raster PNG 图片文件，并保存到指定输出目录。不要生成封面图。

硬性尺寸要求：
- 每张图必须是横版 16:9 信息图，目标画布 1600x900。
- 不要竖版、不要长图、不要 1:1、不要 4:5、不要海报比例。
- 适合微信公众号正文手机阅读：主体内容居中，左右和上下都留 80px 安全边距。
- 中文文字必须大而少，每张图最多 8 个短标签；禁止密集小字。
- 每张图底部只保留一句短 takeaway，不要长段落。

统一视觉风格：
- 蒸馏小余知识卡 / Deep Research Sketchnote / hand-drawn technical explainer infographic。
- 暖米白 / 奶油纸底，深海军蓝手绘描边，低饱和 pastel 便签卡片。
- 中文短标签，手机端可读。
- 不要真实公司 Logo，不要复制 OpenAI 或 Anthropic 标志；可以使用文字标签「Codex」「Claude」。
- 不要企业 PPT，不要写实，不要 3D，不要暗色赛博风，不要复杂小字。
- 每张图只出一版，不要反复重生成；如果视觉方向满足提示，就直接保存。

输出文件要求：
1. `01-capability-stack.png`
2. `02-codex-claude-map.png`
3. `03-plugin-bom.png`
4. `04-permission-gates.png`
5. `05-rollout-loop.png`

图片 1：`01-capability-stack.png`
主题：AI 编程工具能力栈：从规则到分发。
结构：横版三段式。左侧是「个人提示」，中间是 4 层能力阶梯，右侧是「组织治理」。
阶梯标签从下到上：
1. Prompt
2. AGENTS / CLAUDE
3. Skill
4. Plugin
顶部横条：MCP / Hook / Policy
右侧箭头：「越共享，越要治理」
底部 takeaway：「先分层，再装能力」

图片 2：`02-codex-claude-map.png`
主题：Codex 与 Claude 的插件管理地图。
结构：横版左右两栏对照，中间放结论卡片。
左栏「Codex」只放 4 个短标签：Skills、Plugin、Marketplace、Requirements。
右栏「Claude」只放 4 个短标签：Skills、Plugin、enabledPlugins、Hooks。
中间结论卡片：「Skill 是方法，Plugin 是分发」
底部 takeaway：「文件名不同，治理问题相同」

图片 3：`03-plugin-bom.png`
主题：Plugin BOM：企业共享前必须补齐的字段。
结构：横版中央大表格，3 列 3 行。
三列标题：
- 责任：Owner / Scope / Version
- 风险：Components / Permissions / Data
- 交付：Tests / Rollback / Audit
右上角放放大镜和复选框。
底部 takeaway：「说不清 BOM，就不要共享」

图片 4：`04-permission-gates.png`
主题：权限闸门：从来源到审计逐层收口。
结构：横版从左到右 5 道闸门，闸门要宽而清晰。
五道闸门：
1. 来源
2. 范围
3. 工具
4. 检查
5. 审计
左侧输入：「Plugin 能力包」
右侧输出：「团队可用能力」
底部 takeaway：「权限前置，事故才不会后补」

图片 5：`05-rollout-loop.png`
主题：企业插件落地五步：从试点到治理闭环。
结构：横版闭环流程，但不要做成竖向环。用宽屏五节点环形或 S 形路线。
5 个节点：
1. 盘点
2. 试点
3. 封装
4. 分发
5. 清理
每个节点下面只放 2-3 个字动作词：找高频、测触发、补 BOM、控来源、看指标。
中央图标：内部插件市场 + 审计表。
底部 takeaway：「发布不是终点，维护才是治理」

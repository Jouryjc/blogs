---
title: "Anthropic《Introducing Claude Opus 4.7》提取笔记"
source: "https://www.anthropic.com/news/claude-opus-4-7"
source_author: "Anthropic"
captured_at: "2026-04-16"
captured_by: "agent-browser"
tags:
  - type/source
  - topic/ai-industry
  - topic/claude-code
moc:
  - "[[ai-industry]]"
related:
  - "[[claude-opus-4-7]]"
---

# 页面基本信息

- 标题：Introducing Claude Opus 4.7
- 页面类型：Anthropic Product / Announcements
- 发布时间：2026-04-16
- 原始链接：https://www.anthropic.com/news/claude-opus-4-7

# 官方主结论

- Claude Opus 4.7 已经正式可用。
- 相比 Opus 4.6，重点提升在高级软件工程，尤其是更难、更长链路的任务。
- 官方强调，用户现在可以把过去必须密切盯着的难任务，更放心地交给 Opus 4.7。
- 模型在长时间任务中更严谨、更一致，也更会按照指令做事，并且会主动验证输出。

# 这次升级的核心点

## 1. 编程与 Agent 能力更强

- 高难软件工程任务提升明显。
- 更适合复杂、长时间运行的编码工作流。
- 更强的指令遵循能力，会更“按字面执行”。
- 对工具调用、规划、验证这类 agent 场景更友好。

## 2. 视觉能力更强

- 支持更高分辨率图片。
- 官方给出的上限是长边 `2576` 像素，约 `3.75MP`。
- 这比此前 Claude 模型高出 3 倍以上。
- 适合密集截图阅读、复杂图表提取、精细视觉参考等任务。

## 3. 专业产出更“像能交付的东西”

- 官方称它在界面、幻灯片、文档等专业任务上更有审美，也更有创意。
- 重点不是“会不会生成”，而是生成结果更接近可直接交付。

## 4. 记忆能力更实用

- 更善于使用基于文件系统的记忆。
- 能跨多轮、多会话记住重要笔记，减少重复上下文输入。

# 可用范围与价格

- 当天已在所有 Claude 产品中上线。
- 同步覆盖 API、Amazon Bedrock、Google Cloud Vertex AI、Microsoft Foundry。
- API 模型名：`claude-opus-4-7`
- 价格与 Opus 4.6 相同：
- 输入：`$5 / 1M tokens`
- 输出：`$25 / 1M tokens`

# 官方强调的风险控制

- Anthropic 前一周刚发布 Project Glasswing，讨论更强模型在网络安全上的收益与风险。
- Opus 4.7 被定位成先行落地、先做安全验证的模型。
- 官方称它会自动检测并拦截高风险或被禁止的网络安全请求。
- 合规安全研究人员可申请加入 Cyber Verification Program。

# 早期测试里最值得记的几个信号

- Cursor：CursorBench 从 Opus 4.6 的 `58%` 提升到 Opus 4.7 的 `70%`。
- Rakuten：在 Rakuten-SWE-Bench 上，官方引用的合作方说 Opus 4.7 解决的生产任务数是 Opus 4.6 的 `3x`。
- XBOW：视觉敏锐度基准从 `54.5%` 提升到 `98.5%`。
- CodeRabbit：代码审查召回率提升 `10%+`，并称在复杂 PR 上能找到更难发现的问题。
- 多家合作方重复提到同一件事：更少中途停下，更少工具报错，更会自我校验，更适合长链路任务。

# 官方列出的四个“使用层面”提醒

- 指令遵循显著增强，老 prompt 可能会因为模型现在更字面理解指令而产生意外结果。
- 多模态支持提升，尤其是高分辨率图像输入。
- 在金融等高价值知识工作上，结果更严谨、整合度更高。
- 更会利用文件系统记忆，适合长周期 agent 任务。

# 同日发布的额外更新

- 新 effort 等级：`xhigh`
- 位置：介于 `high` 和 `max` 之间
- Claude Code 默认 effort 提高到 `xhigh`
- Anthropic 建议：编码和 agent 场景先从 `high` 或 `xhigh` 开始试
- Claude Platform 增加 task budgets 公测
- Claude Code 上线 `/ultrareview`
- Pro 和 Max 用户可免费试用 3 次 ultrareview
- auto mode 扩展给 Max 用户

# 迁移到 Opus 4.7 时需要注意

- 使用了更新 tokenizer。
- 相同输入可能会映射到更多 tokens，官方给出的范围是 `1.0x - 1.35x`，取决于内容类型。
- 更高 effort 下，尤其是 agent 场景后续轮次，模型会“想得更多”，输出 token 也会更多。
- 官方建议不要只看公告，要在真实流量上测 token 与效果。

# 安全与对齐结论

- 整体安全画像与 Opus 4.6 接近。
- 在诚实性、抗 prompt injection 上有提升。
- 在某些 harm-reduction 场景下略弱。
- Anthropic 仍然认为 Mythos Preview 是对齐表现最好的模型。

# 用于重写时应保留的主线

- 这不是一次“普通提分”发布，而是一次更接近“可以放手交任务”的升级。
- 最重要的不是单个 benchmark，而是模型在长链路、复杂、需要验证的真实工作流里更靠谱。
- 对开发者来说，真正要改的不只是模型版本号，还包括 prompt、effort 配置、token 预算和评测方式。

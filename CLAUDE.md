# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在本仓库中工作时提供指引。

## 语言要求

**后续所有思考过程（thinking）和回复都必须使用中文。**

## 这个仓库是什么

这**不是一个软件工程项目**，而是一个内容生产工作区，用于产出关于 AI Agent 工程化的中文
**微信公众号**文章，以作者人设 **蒸馏小余**（科普 / 讲解口吻）和 **码农小余**（工程师口吻）
发布。工作流程是：收集源材料（X/Twitter 推文串、论文、仓库、网页），改写成中文文章，配上
生成的图卡，渲染成微信可用的 HTML，最后提交为草稿。

这里没有 build、lint 或测试套件。"干活"指的是运行**技能（skills）**和临时的**渲染脚本**，
而不是编译代码。

## 技能（Skills）是首要工具

大多数任务对应一个技能，而不是手写代码。优先使用这些：

- **create-webchat-article** —— 完整流水线：把一个来源（X 链接、仓库、网页、笔记）变成排版
  精美的微信草稿，包含中文改写、配图、2.35:1 封面、本地 Doocs 风格渲染、以及 API 草稿提交。
- **wechat-sticker-post** —— 从链接 / 截图 / 笔记生成短篇贴图 / 图文帖子。
- **xiaoyu-wechat-article-reviewer** —— 以 蒸馏小余 / 码农小余 的风格对草稿打分并优化
  （标题、开头、结构、CTA）。文章在定稿前应先跑一遍这个。
- **baoyu-image-gen** —— 生成封面和插图（批量时建议 ~4 个并发）。
- **dashen-x-battle-plan** —— 生成 X 内容作战计划 PDF 报告。

`reports/x-hot-ai-agent-engineering/` 下的每日热点日报是选题来源：从 TOP10 / 选题建议
部分挑出文章主题，再用上面的技能去写稿。

## 目录约定

仓库里因为不同时期 / 不同技能积累了多条并行的输出目录，它们的重叠是有意为之的。新增内容时，
请沿用你所添加的那条目录树的约定，而不要另立一套新的。

- `raw/` —— 未处理的源材料（论文、推文串、图片）。**绝不要修改这些文件。**
- `x-to-markdown/<author>/<slug>/` —— 转成 markdown 的 X/Twitter 推文串，附下载好的 `imgs/`。
- `reports/x-hot-ai-agent-engineering/` —— 按日期命名的每日 X 热点日报（`YYYY-MM-DD.md`）；
  `latest.md` 镜像最新一天。用于决定写什么。
- `wechat-drafts/<YYYY-MM-DD>-<slug>/` 和 `post-to-wechat/<YYYY-MM-DD>/<slug>/` —— 当前
  每篇文章的工作目录。标准结构为：
  - `article.md` —— 带 YAML frontmatter 的文章（见下文）
  - `research-notes.md` —— 来源与佐证笔记
  - `imgs/` —— 封面（`article-cover.png`）+ 内文插图；`prompts/` 存放配图生成提示词
  - `doocs-wechat-rendered.html` —— 微信可用的渲染结果（Doocs 风格）
  - `render-card.mjs` / `render-card.py` —— 该文章的图卡生成脚本
- `outputs/`、`output/` —— 更早 / 备选的成稿与幻灯片（小红书）目录树。
- `wiki/` —— 整理好的知识 wiki（由 AI 维护；见 `AGETNS.md`）。

`AGETNS.md`（注意：拼写有误，本意是 AGENTS.md）是一份知识库 schema：raw 只读，wiki 完全由
AI 维护并用 `[[topic-name]]` 互链、配 `INDEX.md`，outputs 存放生成的分析。

## 文章 frontmatter

`article.md` 以渲染 / 技能依赖的 YAML frontmatter 开头：

```yaml
---
title: "..."
source: "<原始 URL>"
source_author: "..."
author: "蒸馏小余"            # 或 码农小余
written_style: "蒸馏小余 2.0"
created_at: "YYYY-MM-DD"
coverImage: "imgs/article-cover.png"
summary: "..."
---
```

## 默认配图风格

除非用户明确指定其他风格，所有公众号封面和正文配图默认使用 **Sketchnote / 蒸馏小余知识图解**
风格。不要再让用户重复说明这个偏好。

默认视觉要求：

- Deep Research Sketchnote / hand-drawn technical explainer infographic，优先贴近蒸馏小余文章
  `https://mp.weixin.qq.com/s/GaEdNZRgPV4ofNXvJsJQjQ` 的知识卡风格。
- 暖米白 / 奶油纸底为主，低饱和蓝、绿、黄、粉作为便签色块；深海军蓝细描边。
- 标题居中、信息密度适中偏高、少量角落涂鸦；正文图优先做 1080×602 左右的横版知识卡。
- 低饱和 pastel 圆角卡片、手绘箭头、便签式小标签、流程关系和工程抽象图。
- 适合中文技术公众号手机端扫读：中文短标签、底部 takeaway、信息分组清晰。
- 只有用户明确指定参考图时才用参考图覆盖默认风格；不要因为 `raw/640.jpeg` 存在就自动切到蓝橙海报风。
- 使用参考图时只借鉴视觉语言，不复制原图文案和构图。
- 避免默认生成干净 PPT、企业宣传海报、写实摄影、3D、赛博霓虹、纯扁平流程图风格。
- 避免大面积高饱和蓝橙背景、过多云朵 / 齿轮装饰、过松的信息排布。

生成图片前先检查当前文章目录是否有 `gen-image.md`；若没有，使用仓库根目录 `gen-image.md`
作为默认提示词。

## 渲染脚本

图卡和封面由每篇文章各自的、自包含的脚本临时生成（没有 `package.json`，也没有共享依赖文件
—— 直接用系统运行时）：

- **Node**（`render-card.mjs`、`generate-assets.mjs`）：用 **Playwright** + 系统 Chromium 把
  内联 HTML/CSS 卡片光栅化为 PNG。运行 `node render-card.mjs`。
  Chrome 路径硬编码为 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`。
- **Python**（`render-card.py`、`render-cover.py`）：用 **Pillow**（`PIL`）直接绘制卡片。
  运行 `python render-card.py`。

输出尺寸遵循微信约定：封面为 2.35:1，且在 1:1 居中裁剪后仍需可读（技能会强制这一点）；图卡
为竖版（如 1080×1350、896×1200）。

## 环境说明

- `agent-browser.json` 配置 agent-browser 技能（headed Chrome、自动连接）。
- `.claude/settings.json` 预先放行了对技能目录的读取以及拉取源推文串所用的特定 `WebFetch`
  域名（threadreaderapp、dailydoseofds、github）。
- 内容中的日期使用真实发布日期；当天日期由会话上下文提供。

# DeepSeek Harness 深度文章与公众号草稿设计

## 目标

围绕 DeepSeek AI 于 2026 年 8 月 13 日开放 Developer Preview 的官方项目 DeepSeek Harness（`dsh`），写一篇面向 AI Agent 工程师、技术负责人和关注 Coding Agent 的开发者的中文深度文章，并完成公众号草稿发布。

文章不做新闻通稿式功能罗列，也不把 `dsh` 简化成“DeepSeek 版 Claude Code”。主线是解释：模型只是 Agent 的推理内核，决定长任务是否可靠的另一半是 Harness；DeepSeek 选择把这一层做成可替换、可组合的插件系统，意味着它更接近 Agent SDK 和运行时底座，而不只是一个终端编程助手。

## 事实边界

- 核心材料只使用 DeepSeek 官方仓库、仓库内文档与代码、官方发布信息、Cordis 项目和其设计论文。
- GitHub 星数、提交数、包版本和 Developer Preview 状态在发布前实时复核，并标注核实日期。
- 社区讨论只用于捕捉问题，不作为架构事实来源。
- 不把尚未稳定的接口写成长期承诺；明确说明官方警告会出现兼容性破坏。
- 不把 DeepSeek Harness 与第三方同名 Python 包 `deepseek-harness` 混为一谈。

## 文章定位

### 目标读者

- 正在使用 Claude Code、Codex、OpenCode 等 Coding Agent 的开发者
- 正在自建 Agent Loop、工具系统、沙箱、记忆或多 Agent 编排的工程团队
- 想判断 DeepSeek Harness 是否值得试用、集成或二次开发的技术负责人

### 核心判断

DeepSeek Harness 最值得关注的不是“DeepSeek 也有 Coding Agent 了”，而是它把 Agent 的循环、模型、工具、权限、状态、UI 与编排都降为插件。这样做提高了可替换性和组合能力，也把依赖图、生命周期、冲突处理、版本兼容和安全边界暴露成必须认真治理的工程问题。

### 预期长度与语气

- 正文约 4,500–5,500 个中文字符
- 蒸馏小余 2.0：先给结论，再拆机制，保留明确的作者判断
- 少用“颠覆”“重新定义”等发布稿措辞
- 结尾提供可保存的试用检查表，而不是空泛 CTA

## 标题策略

正式写作前生成五个不同句式的标题候选。首选方向：

> DeepSeek 没做第二个 Claude Code：它把 Agent 拆成了插件

标题需要同时兑现两个承诺：解释 `dsh` 与成品 Coding Agent 的区别，以及说明“Everything is a plugin”带来的工程收益和成本。

## 叙事结构

1. **先下判断**：DeepSeek 开源的不是单一聊天壳，而是一套可组装 Agent 的 Harness。
2. **Harness 到底是什么**：用“模型是大脑，Harness 是神经、手脚、工作台和安全制度”的具象例子解释 Agent Loop、上下文、工具、状态与验证。
3. **为什么不是再做一个 Claude Code**：区分产品层、Harness 层与模型层，说明 Web UI 是 SDK 的一个消费者。
4. **Everything is a plugin 如何落地**：从 Cordis Context、服务注册、事件和配置组装切入，拆解核心包和能力包。
5. **三个关键工程机制**：
   - 接口、实现与模型工具分层，如何替换本地 Shell、远程容器或文件系统；
   - 生命周期与依赖如何让插件按需出现和消失；
   - steering、context injection、receipt、subagent/workflow 如何服务长任务控制。
6. **插件化不是免费的**：分析配置复杂度、依赖冲突、供应链安全、权限边界、遥测与兼容性风险。
7. **与 Claude Code、Codex 等路线的比较**：只比较架构重心，不做未经统一基准支持的性能排名。
8. **谁该现在试，谁该等**：给出个人开发者、框架作者和企业团队的三档判断。
9. **试用检查表**：安装隔离、权限最小化、沙箱、日志、可回滚性、版本锁定、真实任务 A/B。

## 研究与验证

将官方仓库浅克隆到文章目录的 `raw/deepseek-harness/`，重点阅读：

- `README.md` / `README.zh.md`
- `docs/` 中的 architecture、development、Web UI 与 plugin 文档
- `packages/core/` 以及模型、Shell、文件系统、LSP、Skill、Subagent、Workflow、Approval、Context Compaction 等包
- 根目录 `package.json`、workspace 配置、许可证和第三方声明
- vendored Cordis 代码及其公开论文

研究笔记写入 `research-notes.md`，每个重要判断记录来源文件或官方 URL。对仓库 README 的宏观描述至少做一次代码结构交叉验证。

## 配图方案

生成一张 2.35:1 封面和三张 16:9 正文图，统一使用蒸馏小余奶油纸底技术手绘风：

1. **封面**：`模型之外，Agent 还有一半`；中央是模型内核，外围是 Loop、工具、记忆、权限和 UI 插件。
2. **三层定位图**：模型层 → Harness 层 → 产品层，解释 `dsh` 的位置。
3. **插件架构图**：Cordis Context 位于中央，核心循环和能力插件围绕注册，配置将其组装成具体 Agent。
4. **收益与代价图**：左侧是可替换、可组合、可测试，右侧是依赖、权限、供应链和兼容性成本。

每张图只承载一个结论，复杂比较不用公众号小字号表格。封面标题和主体需位于中央正方形安全区。

## 产物布局

```text
post-to-wechat/2026-08-13/deepseek-harness/
├── deepseek-harness.md
├── article-review.md
├── article-anti-ai.md
├── research-notes.md
├── publish-dry-run.json
├── publish-result.json
├── draft-readback.json
├── imgs/article-cover.png
├── illustrations/deepseek-harness/
└── raw/deepseek-harness/
```

主文 `deepseek-harness.md` 保留不覆盖；审稿结果和发布版使用相邻文件，后续渲染和发布均以 `article-anti-ai.md` 为准。

## 公众号闭环

1. 写完初稿后运行 `xiaoyu-wechat-article-reviewer` 和 `article_metrics.py`。
2. 检查第一屏承诺、AI 味词组、段落节奏、作者判断、可保存资产和 CTA。
3. 生成并逐张检查图片尺寸、中文和移动端可读性。
4. 以 Markdown 直接调用 `wechat-api.ts --dry-run`，主题为 `grace`，品牌色为 `#0F4C81`，确认封面与本地图片均被识别且没有 placeholder。
5. 首次发布时创建一份新草稿，保存返回的 `media_id`；不误用第三方同名项目已有草稿。
6. 调用公众号 `draft/get` 回读同一 `media_id`，核对标题、文章数、封面和正文图片后再宣布完成。

## 验收标准

- 文章能用清晰例子解释 Harness，而不依赖读者预先理解 Cordis。
- 对插件机制的描述同时有官方文档和仓库结构证据。
- 至少包含三个作者判断：项目定位、插件化代价、当前采用时机。
- 不声称 Developer Preview 已达到生产稳定性，不做无依据的性能比较。
- 审稿文件与优化稿存在，`ai_smell_hits` 已清空或逐项说明。
- 四张图片实际存在、比例正确、中文可读，Markdown 引用无误。
- dry-run 成功且本地图片 placeholder 为零。
- 真实发布返回 `success: true` 和 `media_id`。
- `draft/get` 回读确认远程草稿状态与本地成稿一致。
- 按知识库流程给主文补齐 `type/article`、`topic/agent-runtime`、`topic/agent-design`、`platform/wechat`，更新 manifest 与相关 wiki，并如实报告全库既有死链。

## 失败处理

- 若官方仓库持续快速变化，以发布时固定提交哈希为准，并在研究笔记记录。
- 若图片生成失败，保留提示词和完整成稿，但不拿占位图冒充完成。
- 若微信 API 因 IP 白名单失败，保留 dry-run 和失败响应，明确标记为“API 阻塞”，不宣称已进入草稿箱。
- 若 `draft/get` 不能确认远程状态，即使上传日志成功，也不宣称发布闭环完成。

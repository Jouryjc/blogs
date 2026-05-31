# Spec: 把 blogs 仓库转成 Obsidian 知识库

- **Date:** 2026-05-31
- **Status:** Approved (design)
- **Topic:** blogs-to-obsidian

## 1. 目标 (Goal)

把当前 `blogs/` 仓库**原地**改造成一个可用的 Obsidian 知识库(vault):在不破坏现有目录结构、不改动文章正文、不影响公众号发布流水线的前提下,叠加一层"知识库能力"——一致的 frontmatter 标签体系、笔记之间的 wikilink 关联、按主题组织的 MOC(内容地图)页面、以及一个首页索引,让 Obsidian 的关系图(graph)与反向链接(backlinks)变得有意义、好导航。

## 2. 已确认的关键决策 (Locked decisions)

1. **改造野心 = 链接型知识库,保持现有布局(非破坏性)。** 所有文件留在原地,只叠加 `.obsidian/` 配置 + `wiki/` 知识层 + frontmatter 标签/链接。
2. **笔记类型划分 = 文章是一级笔记,配图 prompt 是附件。** 成品文章、raw 原始素材、报告、资讯、推文串 → 一级笔记;封面/插图的 prompt、outline、system-prompt 等生产产物 → 保留为附件,**不进入**关系图/索引/标签体系。
3. **raw/ 处理 = 给 raw 原始素材文章补 tags。** 允许给实质性的 raw 源文章新增一行 `tags:`(必要时补 `title`/`source`),但**绝不动正文**,也**绝不动** prompt/outline 类文件。`AGETNS.md` 的"never modify raw"规则相应放宽并在 `AGENTS.md` 中记录。

## 3. 非目标 / 范围边界 (Non-goals)

绝不改动:
- 任何文章/raw 文件的**正文文本**(只动 frontmatter,且只增不改)。
- 配图 prompt / outline / system-prompt 文件(`illustrations/**`、`cover-image/**`、`imgs/prompts/**`、`**/prompts/**`、`outline.md`、`prompt-*.md`、`cover*.md`)。
- 已渲染的 HTML 产物(`doocs-wechat-rendered*.html` 等)。
- 任何实际图片(`.png/.jpg/.jpeg/.svg`)。

其他:
- **不引入社区插件**(对版本控制不友好、与用户环境强相关),只启用 Obsidian 核心插件。
- 不重命名/移动任何现有文章文件(`AGETNS.md → AGENTS.md` 除外)。

## 4. Vault 形态

- **Vault 根 = 仓库根。** 在根目录加 `.obsidian/`(纳入版本控制)。
- **`wiki/` = 知识层**(沿用 `AGETNS.md` 既有约定):放首页索引 `INDEX.md` 与每个主题一个 MOC 页面。
- 现有目录(`raw/`、`outputs/`、`post-to-wechat/`、`reports/`、`x-to-markdown/`、`output/`)原样保留。

## 5. 一级笔记的选取规则 (Selection rules)

一个 `.md` 文件是**一级笔记**当且仅当它**不**位于附件目录、**不**是附件文件名,且属于下列之一:

**附件(排除)判定** —— 路径包含任一段 `illustrations/`、`cover-image/`、`imgs/`、`prompts/`,或文件名匹配 `outline.md`、`system-prompt.md`、`prompt-*.md`、`cover*.md`、`*-prompt*.md`。

**一级笔记类别:**
| 类别 | 选取范围 | `type/` 标签 |
|---|---|---|
| 成品文章 | `outputs/*.md`(顶层)、`outputs/arxiv-*/*.md`(草稿正文)、`post-to-wechat/**/<slug>.md`、`output/xiaohongshu/**/caption.md` | `type/article` |
| raw 原始素材 | `raw/*.md`(顶层)、各 `raw/<source>/<主文档>.md`、`raw/extracted/*.md`、`raw/ssrn-6372438/abstract-page.md` | `type/source` |
| 热点报告 | `reports/**/*.md` | `type/report` |
| 资讯简报 | `raw/news/*.md` | `type/news` |
| 推文串 | `**/x-to-markdown/**/*.md` | `type/thread` |
| MOC/索引 | `wiki/INDEX.md`、`wiki/<topic>.md`(本次新建) | `type/moc` |

> `wiki/xiaoyu-2.0-rewrite-prompt.md` 是一个改写 prompt 工具文件,**保持原样**,不纳入 MOC、不打主题标签。

## 6. 标签体系 (Tag taxonomy)

每个一级笔记的 `tags` 至少含 **1 个 `type/*`** 与 **1+ 个 `topic/*`**;成品/发布类可加 `platform/*`。

**`type/*`:** `type/article`、`type/source`、`type/report`、`type/news`、`type/thread`、`type/moc`

**`topic/*`(12 个,实现时按正文确认):**
`topic/claude-code`、`topic/agent-skills`、`topic/agent-memory`、`topic/context-engineering`、`topic/prompt-caching`、`topic/rag`、`topic/managed-agents`、`topic/agent-runtime`、`topic/agent-design`、`topic/agent-safety`、`topic/knowledge-base`、`topic/ai-industry`

**`platform/*`(可选):** `platform/wechat`、`platform/xiaohongshu`

**初步主题归类(实现时读正文确认/微调):**
- `topic/claude-code`: `outputs/agents-md-claude-md.md`、`outputs/claude-code-boris-cherny.md`、`post-to-wechat/2026-05-09/.../claude-code-html-effectiveness.md`、`raw/Claude_Code_Boris_Cherny_深度总结.md`、`raw/extracted/agents-md-claude-md-source-notes.md`、`output/xiaohongshu/agents-md-claude-md/caption.md`
- `topic/agent-skills`: `outputs/agent-skills-tips.md`、`outputs/agent-skills-engineering-workflow.optimized.md`、`outputs/agent-skills-engineering-workflow.xiaoyu.md`、`post-to-wechat/2026-04-26/.../agent-skills-deep-dive.md`
- `topic/agent-memory`: `outputs/agent-memory-never-forget.md`、`outputs/arxiv-2604-01707/memory-in-llm-era-wechat-draft.md`、`...optimized.md`、(+ `outputs/agents-md-claude-md.md` 次要主题)
- `topic/context-engineering`: `post-to-wechat/2026-04-23/.../claude-context-deep-dive.md`、`raw/avi-context-engineering-claude-code/...md`、`x-to-markdown/avichawla/how-to-cut-claude-code-costs-by-3x-.../*.md`
- `topic/prompt-caching`: `post-to-wechat/2026-05-10/rag-ttft/rag-ttft.md`(次要)、`raw/avi-prompt-caching-claude-code/...md`、`x-to-markdown/avichawla/prompt-caching-in-llms-clearly-explained/*.md`
- `topic/rag`: `post-to-wechat/2026-05-10/rag-ttft/rag-ttft.md`、`post-to-wechat/2026-04-28/.../gitnexus-code-intelligence.md`、`post-to-wechat/2026-04-23/.../claude-context-deep-dive.md`(次要)
- `topic/managed-agents`: `raw/claude-managed-agents/claude-managed-agents-deep-dive.md`、`raw/claude-managed-agents/x-to-markdown/RLanceMartin/.../*.md`
- `topic/agent-runtime`: `outputs/ralph-orchestrator.md`、`raw/ralph.md`、`raw/ralph-orchestrator.md`、`raw/hermes-agent.md`、`raw/pierce-zhang-*/hermes-nvidia-minimax-setup.md`、对应推文串
- `topic/agent-design`: `raw/claude-design-ryan-mather/claude-design-ryan-mather.md`、`raw/arxiv-2604-14228/claude-code-design-space.md`、对应推文串
- `topic/agent-safety`: `raw/ssrn-6372438/ai-agent-traps-xiaoyu.md`、`raw/ssrn-6372438/abstract-page.md`
- `topic/knowledge-base`: `outputs/code-to-business-knowledge-base.md`
- `topic/ai-industry`: `outputs/luo-fuli-agent-era-wechat.md`、`outputs/claude-opus-4-7.md`、`raw/extracted/claude-opus-4-7-source-notes.md`、`raw/extracted/luo-fuli-interview-source-notes.md`、`reports/**`、`raw/news/**` → 报告/资讯统一 `topic/ai-news`(并入 `ai-industry` 主题页展示)

> 注:`raw/news/*.md` 已有扁平 `tags`(如 `ai`、`news`),实现时**追加** `type/news`、`topic/ai-news`,保留原有项,沿用其列表写法。

## 7. Frontmatter 规则(只增不改)

- **绝不**重命名、删除、调整顺序或改写任何已有 frontmatter 键的值。
- **已有 frontmatter 的笔记:** 新增 `tags`(若已有则合并去重);可选新增 `moc`、`related`(见 §8)。
- **无 frontmatter 的笔记:** 在文件最顶部插入最小 YAML 块:`title`(取自首个 H1,无则取文件名)+ `tags`。
- **raw 源文章:** 仅新增 `tags`;若缺 `title`/`source` 可补,正文不动。
- YAML 用双引号包裹含特殊字符的值;保持与现有文件一致的风格(2 空格缩进、列表用 `- `)。

## 8. 链接策略(关联写进 frontmatter + wiki,绝不写进正文)

为避免链接杂质泄漏到公众号 HTML:
- **不**往文章正文追加可见的"相关阅读"段落。
- 在一级笔记 frontmatter 用 Obsidian 链接属性表达关联:
  - `moc:` —— 指向所属主题页,如 `moc: ["[[agent-memory]]"]`
  - `related:` —— 溯源链(原始素材→草稿→成品)与姊妹篇,如 `related: ["[[claude-managed-agents-deep-dive]]"]`
  - 这些 frontmatter 内的 `[[...]]` 会进入关系图与反向链接面板。
- **wiki MOC 页面**承载人类可读的 `[[链接]]` 正文结构(每页:一段摘要 + 分组的 `[[文章]]`/`[[原始素材]]` 链接 + 相关主题)。
- wikilink 解析靠唯一 basename;主文章 basename 已唯一。若遇重名,用带路径的 `[[folder/name]]`。
- **图片不改:** 现有 `![](imgs/xxx.png)` 相对链接在 Obsidian 中本就能渲染。

## 9. wiki/ 内容产出

- **`wiki/INDEX.md`**(首页 / `type/moc`):
  - 顶部一段话说明这是什么知识库。
  - "主题地图"区:列出全部 12 个 `[[<topic>]]` MOC 链接 + 一句话简介。
  - "最近文章""报告与资讯""推文串原始素材"等分区入口。
- **`wiki/<topic>.md` × 12**(每个 `type/moc`):
  - 开头一段话主题摘要(遵循 schema 规则)。
  - `## 文章`:该主题的成品文章 `[[链接]]`。
  - `## 原始素材`:相关 raw 源 / 推文串 `[[链接]]`。
  - `## 相关主题`:其它 `[[topic]]` 链接。

## 10. .obsidian/ 配置

- `app.json`: `useMarkdownLinks: false`(新链接用 wikilink)、`newLinkFormat: "shortest"`、`alwaysUpdateLinks: true`。
- `core-plugins.json`: 启用 graph、backlink、outgoing-link、tag-pane、properties、file-explorer、search、global-search、switcher、page-preview、outline、bookmarks、command-palette、file-recovery。
- `graph.json`: 默认过滤查询隐藏附件,如:
  `-path:prompts -path:illustrations -path:cover-image -path:imgs/prompts -file:outline -file:system-prompt`
- `appearance.json`: 最小默认(`baseFontSize` 等),不强制主题。
- (可选)在 `app.json` 配置以 `wiki/INDEX.md` 为默认首页。

## 11. 杂项收尾

- **`AGETNS.md` → `AGENTS.md`:** 新建正确命名的文件,修正拼写,并把 Obsidian 约定写入(wiki MOC 结构、`type/`+`topic/` 标签体系、frontmatter 链接属性、放宽后的"raw 可加 tags 行"规则、附件定义);随后删除 `AGETNS.md`。
- **`.gitignore`:** 追加 `.obsidian/workspace.json`、`.obsidian/workspace-mobile.json`、`.obsidian/cache`(界面/缓存状态不入库,配置入库)。

## 12. 可选 / 范围外

- 修复 frontmatter 中陈旧的绝对路径(`/Users/jouryjc/.../2026.04/blogs/...` → 现用户/路径)。默认**不做**,除非另行确认。
- 给主文章补 `aliases`(英文短名)以优化链接手感。默认**不做**。

## 13. 验收标准 (Verification)

1. 仓库根存在 `.obsidian/`,Obsidian 可直接"Open folder as vault"打开且无报错。
2. `wiki/INDEX.md` + 12 个 `wiki/<topic>.md` 存在,链接可点击、无死链(basename 能解析)。
3. 所有一级笔记含合法 `tags`(`type/*` + `topic/*`);附件文件未被改动(`git diff` 不含它们)。
4. 关系图过滤后只显示一级笔记 + MOC,附件节点被隐藏。
5. 成品文章正文逐字未变(`git diff` 仅显示 frontmatter 增量)。
6. `AGENTS.md` 存在且内容更新;`AGETNS.md` 已删除;`.gitignore` 已更新。

# Knowledge Base Schema

## What This Is

一个关于 **AI Agent 工程化** 的个人知识库,同时也是一个 **Obsidian vault**(仓库根目录即 vault 根目录,直接用 Obsidian "Open folder as vault" 打开)。

内容覆盖:Claude Code、Agent Skills、Agent 记忆、上下文工程、Prompt 缓存、RAG、托管 Agent、Agent 运行时 / 设计 / 安全,以及行业资讯。

## How It's Organized

- `raw/` —— 原始素材(论文、推文、深度笔记)。**正文永不修改**;唯一允许的改动是给"源文章"补一行 `tags:`(及缺失的 `title`/`source`),见下。
- `outputs/` —— 成品文章(公众号草稿、优化版、HTML 渲染等)。
- `post-to-wechat/<日期>/<slug>/` —— 按日期组织的公众号成品(主文 `<slug>/<slug>.md`)。
- `output/xiaohongshu/` —— 小红书文案。
- `reports/` —— 每日 X 热点报告。
- `x-to-markdown/` —— 转成 Markdown 的推文串。
- `wiki/` —— **知识层(AI 维护)**:首页 `INDEX.md` + 每个主题一个 MOC 页面。
- `.obsidian/` —— vault 配置(纳入版本控制;UI/缓存状态见 `.gitignore`)。
- `_kb_build/` —— 维护脚本(分类、打标签、查死链)。详见文末。

## 一级笔记 vs 附件

**一级笔记(first-class notes)** = 进入知识网络(打标签、被 wiki 链接、出现在关系图)的内容:成品文章、raw 源文章、报告、资讯、推文串。

**附件(attachments)** = 生产产物,保留在原处但**不**进入知识网络。判定规则(满足任一即为附件):
- 路径中包含目录段:`illustrations/`、`cover-image/`、`imgs/`、`prompts/`;或
- 文件名匹配:`outline.md`、`system-prompt.md`、`prompt-*.md`、`cover*.md`。

> 注意:文件名"中间"含 `prompt` 的真实文章(如 `avi-prompt-caching-claude-code.md`)**不是**附件——只按上面的前缀/精确名判定,不要用 `*-prompt*` 这种宽松匹配。

## 标签体系(Tag Taxonomy)

每个一级笔记的 `tags` 至少含 1 个 `type/*` + 1 个及以上 `topic/*`;成品/发布类可加 `platform/*`。

- **`type/*`**:`type/article`(可发布成品)、`type/source`(raw 源)、`type/report`、`type/news`、`type/thread`、`type/moc`(wiki 页面)
- **`topic/*`**:`claude-code`、`agent-skills`、`agent-memory`、`context-engineering`、`prompt-caching`、`rag`、`managed-agents`、`agent-runtime`、`agent-design`、`agent-safety`、`knowledge-base`、`ai-industry`(报告/资讯另用 `topic/ai-news`)
- **`platform/*`**:`platform/wechat`、`platform/xiaohongshu`

## Frontmatter 规则(只增不改)

- **绝不**重命名 / 删除 / 调整顺序 / 改写任何已有 frontmatter 键的值(公众号流水线依赖它们)。
- 已有 frontmatter 的笔记:新增 `tags`(已有则合并去重),可选新增 `moc` / `related`。
- 无 frontmatter 的笔记:在文件最顶部插入最小 YAML 块(`title` 取自首个 H1)+ `tags`。
- raw 源文章:仅新增 `tags`(必要时补 `title`/`source`),正文不动;附件文件完全不动。

## 链接策略(关联写进 frontmatter + wiki,绝不写进正文)

为避免链接杂质泄漏到公众号 HTML,**不**往文章正文追加"相关阅读"段落。关联只存在于两处:

1. **笔记 frontmatter** 的链接属性(会进入关系图 / 反向链接):
   - `moc: ["[[<topic>]]"]` —— 指向所属主题页
   - `related: ["[[...]]"]` —— 溯源链(原始素材 → 草稿 → 成品)与姊妹篇
2. **wiki MOC 页面** 的正文 `[[链接]]`(人类可读的导航结构)。

约定:
- wikilink 默认用唯一 basename;若 basename 冲突(目前仅 `ralph-orchestrator`:`outputs/` vs `raw/`),用带路径的 `[[outputs/ralph-orchestrator]]` / `[[raw/ralph-orchestrator]]`。
- 推文串文件名是数字 ID,链接时务必加可读别名:`[[2044670188998803855|Avi: Prompt caching]]`。
- 图片不改:现有 `![](imgs/xxx.png)` 相对链接在 Obsidian 中本就能渲染。

## Wiki Rules

- 每个主题一个 `wiki/<topic>.md`,文件名 = `topic/` 标签去掉前缀。
- 每个 wiki 页面以一段话摘要开头。
- 用 `[[topic-name]]` 链接相关主题;用 `[[note]]` 链接文章 / 源。
- 维护 `wiki/INDEX.md` 作为首页(主题地图 + 最近文章 + 报告资讯入口)。
- 新的 raw 源到达时,更新相关 wiki 页面与受影响笔记的 `related`。

## 加一篇新文章时(维护流程)

1. 把成品放进 `outputs/` 或 `post-to-wechat/<日期>/<slug>/`,原始素材放进 `raw/`。
2. 在 `_kb_build/manifest.json` 给新笔记加一条(`tags` / `moc` / `related`)。
3. 跑 `python3 _kb_build/apply_tags.py`(幂等,只动新文件的 frontmatter)。
4. 跑 `python3 _kb_build/inventory.py` 确认没有 `unclassified` 漏网,跑 `python3 _kb_build/link_check.py` 确认无死链。
5. 把新笔记 `[[链接]]` 加到对应的 `wiki/<topic>.md` 与 `wiki/INDEX.md`。

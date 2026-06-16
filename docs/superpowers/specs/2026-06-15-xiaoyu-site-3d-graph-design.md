# 蒸馏小余个人站点 · 3D 知识图谱首页 设计方案

- 日期：2026-06-15
- 状态：已通过 brainstorming，待用户 review spec
- 目标分支：`feat/xiaoyu-site`

## 1. 目标与范围

基于本仓库现有的博客资源，开发一个「蒸馏小余」个人站点：

- **首页**：把仓库内容组成的知识图谱渲染成酷炫的 **3D 深色星系风** 力导向图。
- **内容**：展示当前**全部成品博客文章**（站内全文阅读），不含草稿、source、小红书、报告。
- **形态**：纯静态站点（Vite + 原生 JS + 3d-force-graph/Three.js），构建脚本从仓库数据生成 JSON。
- **部署**：**Cloudflare Pages**（Git 集成，根路径部署）。

非目标（YAGNI）：服务端、搜索后端、评论、登录、草稿/报告节点、SSR、SEO 深度优化。

## 2. 目录结构

站点独立放在仓库 `site/` 子目录，不污染现有内容目录：

```
site/
├── build/
│   └── generate-data.mjs       # 扫描仓库 → graph.json + articles.json + 复制配图
├── public/
│   ├── data/                   # 构建产物（gitignore）：graph.json / articles.json
│   ├── article-assets/<slug>/  # 构建产物（gitignore）：复制的文章配图
│   └── _redirects              # CF Pages SPA fallback: /* /index.html 200
├── src/
│   ├── main.js                 # 入口 + history 路由
│   ├── router.js               # 极简 history 路由
│   ├── graph/
│   │   └── graph3d.js          # 3d-force-graph 星系首页 + Bloom 辉光
│   ├── pages/
│   │   ├── home.js             # 首页（3D 图谱 + HUD）
│   │   ├── list.js             # 文章列表（卡片网格 + 主题筛选）
│   │   └── article.js          # 文章详情（站内全文）
│   ├── styles/
│   │   ├── base.css
│   │   ├── home.css
│   │   ├── list.css
│   │   └── article.css
│   └── data.js                 # 运行时加载 data/*.json 的封装
├── index.html
├── vite.config.js              # base: '/'
├── package.json
└── .gitignore                  # 忽略 public/data、public/article-assets、dist、node_modules
```

## 3. 数据生成（build/generate-data.mjs）

Node 脚本（ESM），在 `vite build` 前运行（`prebuild` 钩子），也可单独 `npm run gen`。

### 3.1 主题节点（topic，预期 12 个）

- 扫描 `wiki/*.md`，排除 `INDEX.md` 与 `xiaoyu-2.0-rewrite-prompt.md`。
- 文件名（去 `.md`）即节点 `id`（如 `claude-code`）；标题取 frontmatter `title` 或正文首个 `#`。
- 节点字段：`{ id, type:'topic', title, slug, summary?, val:<较大>, color:<按主题分配> }`。

### 3.2 文章节点（article，预期 ~27 个）

- 数据源目录：`post-to-wechat/*/*/` 与 `output/*/`。
- 每个文章目录取**主文件**：优先与目录同名的 `<slug>.md`，否则 `article.md`。
- 解析 frontmatter（`gray-matter`）：`title / summary / author / source / created_at / coverImage / tags / moc`。
- **纳入规则**：必须有 `title` 且 `tags` 含 `type/article`。排除：
  - 草稿目录 `wechat-drafts/**`
  - `source/**`、`raw/**`、小红书 `xiaohongshu/**`、`image-cards/**`、attachments
  - 没有有效 frontmatter 的支撑文件
- 用 `_kb_build/inventory.json` 的 `first_class`（`type=='article'`）做**交叉校验**：脚本最终打印「纳入文章数 / 跳过清单」，便于人工核对。若某成品文章被规则误杀，在脚本里维护一份显式 `INCLUDE`/`EXCLUDE` 兜底列表。
- `slug`：取文章目录名（保证唯一；冲突时加日期前缀）。
- 节点字段：`{ id:slug, type:'article', title, slug, summary, topic:<主 moc>, tags, date, val:<较小>, color:<继承主题色> }`。

### 3.3 边（links）

- **article → topic（kind: 'moc'）**：来自 frontmatter `moc`（形如 `[[claude-code]]`，解析出 `claude-code`）与 `tags` 里的 `topic/<x>`。一篇文章可连多个主题。
- **article → article（kind: 'related'）**：来自 `_kb_build/manifest.json` 对应条目的 `related`，以及正文 wikilink `[[slug|...]]`（仅当目标也是已纳入的 article 时建边，去重、无向去重）。
- 丢弃指向不存在节点的边。

### 3.4 正文与配图

- markdown → HTML：`markdown-it`（开启 `html`, `linkify`, `typographer`）。
- 图片路径重写：把正文里相对路径（`imgs/xxx.png`、`./imgs/...`）改写为 `/article-assets/<slug>/imgs/xxx.png`。
- 复制每篇文章目录的 `imgs/`（含子目录）到 `public/article-assets/<slug>/imgs/`；封面 `coverImage` 一并复制并在 articles.json 记录重写后的路径。
- 去掉正文里的 frontmatter；去掉文末可能存在的微信发布残留无需特殊处理（保留原文即可）。

### 3.5 产物

- `public/data/graph.json`：`{ nodes:[...], links:[...] }`。
- `public/data/articles.json`：`{ [slug]: { title, summary, author, date, topic, tags, cover, related:[slug...], html } }`。
  - 注意：不含 `source` 外链字段的展示（详情页不放微信原文链接）。

## 4. 首页 3D 知识图谱（深色星系风）

- 库：`3d-force-graph`（底层 Three.js），后处理 `UnrealBloomPass` 做整体辉光。
- 背景：深空近黑（`#05060f` 一类）+ 远景粒子星点。
- 节点：
  - **主题 = 大亮星**：12 主题各一种低饱和但发光的颜色，`val` 较大，标签常显。
  - **文章 = 小卫星**：继承所属主题色（取主 moc），`val` 较小，hover 才显标签。
- 连线：发光细线；`moc` 边亮于 `related` 边。
- 交互：
  - 旋转/缩放/拖拽（库内置）；缓慢自转。
  - hover 节点：放大 + tooltip（标题 / 类型 / 摘要首句）。
  - 点击 **主题星**：高亮其直接邻居（下属文章），其余淡化；再点一次进入 `/articles?topic=<id>`。
  - 点击 **文章星**：进入 `/article/<slug>`。
- HUD 叠层（DOM 覆盖在 canvas 上）：
  - 左上：品牌「蒸馏小余 · AI Agent 工程化知识库」+ 一句副标题。
  - 右上：12 主题色图例（点击 = 聚焦该主题）。
  - 顶部中：搜索框，按标题/主题实时过滤并把相机聚焦到匹配节点。
  - 右下：「进入文章列表 →」入口。
- 性能：节点规模 ~40，无压力；移动端降级（减少粒子、关闭/弱化 Bloom）。

## 5. 页面与路由

极简 history 路由（`router.js`），三条路由：

- `/` 首页：全屏 3D 图谱 + HUD。
- `/articles`（可带 `?topic=<id>`）列表：响应式封面卡片网格；顶部主题 tab 过滤；卡片含封面、标题、摘要、主题色条、日期。
- `/article/<slug>` 详情：封面图 + 标题 + 作者/日期 meta + **站内全文 HTML** + 配图 + 「相关文章」卡片（同 moc / related）。**不放微信原文外链。**

视觉：首页深色星系；列表/详情用深色基底（暗色阅读主题）配星系点缀，正文排版保证长文可读（合适行宽、字号、对比度、代码块/引用样式）。

## 6. 部署（Cloudflare Pages）

- Git 集成：CF Pages 连接 GitHub 仓库。
  - Build command：`cd site && npm ci && npm run build`
  - Build output directory：`site/dist`
  - Root 目录可留空（命令里已 `cd site`）。
- `vite.config.js` `base: '/'`（根路径部署）。
- `public/_redirects` 内容：`/*    /index.html   200`（SPA history 路由 fallback）。
- 自定义域名后续在 CF 面板绑定，无需改代码。
- `npm run build` = `npm run gen && vite build`；`gen` 失败则 build 失败（数据缺失早暴露）。

## 7. 测试与验证

无单测框架；以**可运行 + 数据正确性**为验收：

1. `npm run gen` 后检查：`graph.json` 节点数（12 主题 + 实际成品文章数，与脚本打印的纳入清单一致）、无悬空边、`articles.json` 每篇有 html 且图片路径已重写、`article-assets` 下图片确实存在。
2. `npm run dev` 本地：首页 3D 图谱可旋转、节点可点、主题高亮正确；列表筛选正确；随机抽 3 篇详情页全文与配图正常显示，相关文章可跳转。
3. `npm run build` 成功产出 `site/dist`，`npm run preview` 验证生产构建（含 `_redirects` 行为用 `vite preview` 近似验证，最终以 CF 为准）。
4. 移动端窄屏快速过一遍（图谱降级、列表单列、正文可读）。

## 8. 风险与取舍

- **成品文章口径**：`post-to-wechat` 与 `output(s)` 目录约定不一，靠 frontmatter + inventory 交叉校验 + 兜底列表控制；脚本打印纳入清单供人工确认是关键防线。
- **图片体积**：复制全部 `imgs/` 可能较大；首版全量复制，后续可按需压缩（已有 `compressing-images` 技能）。
- **Bloom 性能**：低端机可能掉帧，做移动端降级开关。
- **wikilink 解析**：仅在目标为已纳入 article 时建边，避免脏边。

## 9. 实现顺序（供 writing-plans 展开）

1. 脚手架：`site/` + Vite + 依赖 + `.gitignore` + `index.html` + 路由骨架。
2. `generate-data.mjs`：节点/边/正文/配图 + 纳入校验打印。
3. 首页 3D 图谱 + HUD + 交互。
4. 列表页 + 主题筛选。
5. 详情页 + 正文排版 + 相关文章。
6. 移动端降级 + 视觉打磨。
7. CF Pages 部署配置（`_redirects`、`base`、构建命令文档）。

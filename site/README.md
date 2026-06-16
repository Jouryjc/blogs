# 蒸馏小余 · 3D 知识图谱站点

基于本仓库博客资源构建的纯静态站点：**3D 深色星系风知识图谱首页** + 全部成品文章的站内全文阅读。
技术栈：Vite + 原生 JS + [`3d-force-graph`](https://github.com/vasturiano/3d-force-graph)（Three.js + UnrealBloom）。

## 本地开发

```bash
cd site
npm install
npm run dev      # 先跑 generate-data 生成数据，再启动 Vite dev server
```

打开终端提示的地址（默认 `http://localhost:5173`）即可。三条路由：

- `/` —— 全屏 3D 知识图谱 + HUD（品牌 / 搜索 / 12 主题图例 / 进入列表）
- `/articles`（可带 `?topic=<id>`）—— 文章卡片网格 + 主题筛选
- `/article/<slug>` —— 站内全文 + 配图 + 相关文章

## 数据来源与生成

数据由构建脚本从仓库内容**构建期生成**（产物已 gitignore，不入库）：

```bash
npm run gen          # 生成 public/data/*.json 并复制配图到 public/article-assets/
node build/verify-data.mjs   # 断言：主题=12、文章≥10、无悬空边、颜色合法、related 一致
```

- 数据驱动来源：`_kb_build/manifest.json`（成品文章的 `tags`/`moc`/`related` 元数据，按路径为 key）。
- 纳入口径：manifest 中 `type/article` 且 `platform/wechat` 的条目，跨 `outputs/`、`output/`、`post-to-wechat/`。
  - 自动排除小红书文案（`platform/xiaohongshu`）。
  - 同一篇文章的多个变体（`.optimized` / `.xiaoyu`）归一化后去重，优先 `.optimized`。
- 主题节点来自 `wiki/*.md`（排除 `INDEX.md`、`xiaoyu-2.0-rewrite-prompt.md`），共 12 个。
- 当前产出：**12 主题 + 16 篇文章**。改动源内容后重跑 `npm run gen` 即可刷新。

## 生产构建

```bash
npm run build    # = npm run gen（prebuild）+ vite build，产出 site/dist
npm run preview  # 本地预览 dist
```

`dist/` 含 `index.html`、`assets/`、`data/*.json`、`article-assets/**`。

## Cloudflare 部署

本仓库用 **Cloudflare Workers 静态资源**（assets-only Worker）托管，配置见 `site/wrangler.jsonc`。

Workers Builds（Git 集成）按以下设置：

- **构建命令（Build command）**：`cd site && npm ci && npm run build`
- **部署命令（Deploy command）**：`cd site && npx wrangler deploy`
- **根目录**：留空（命令里已 `cd site`）。
- **Node 版本**：≥ 18。

`site/wrangler.jsonc` 关键字段：

- `assets.directory: "./dist"` —— 只发布构建产物（不含 `node_modules`）。
- `assets.not_found_handling: "single-page-application"` —— SPA 路由 fallback，
  未命中路径回退 `index.html`；真实 `/assets/*.js`、`*.css` 仍按正确 MIME 返回。
  **不要**用 Pages 的 `_redirects`（`/* /index.html 200`），Workers 会判定为无限循环而拒绝部署。
- `name` 必须与 CF 上的 Worker 名称一致，否则会新建 Worker。

> 注：部署命令必须 `cd site`，让 wrangler 读到 `site/wrangler.jsonc`（指向 `./dist`）。
> 若从仓库根运行，会误把整个 `site/`（含 `node_modules`）当资源上传。
> Cloudflare 的 workers-autoconfig 可能在仓库根自动生成一份 `wrangler.jsonc`（assets 指向 `site`）——
> 因部署命令已 `cd site`，那份配置不会被使用；如出现可直接删除。

## 已知事项 / 后续优化（不在当前范围）

- **配图体积**：首版全量复制文章引用的原始 PNG（部分知识卡单图 ~7MB，`dist` 约 70MB）。
  后续可用仓库 `compressing-images` 技能压缩 / 转 WebP 降体积。
- `three` 必须 ≥ 0.179（`3d-force-graph@1.80` 要求），与库去重为单实例，否则
  UnrealBloomPass 与库内 renderer 接口不一致会导致首页**整屏黑**。当前锁定 `three@^0.184.0`。
- 其他可选：节点聚类布局、暗/亮色切换、RSS。

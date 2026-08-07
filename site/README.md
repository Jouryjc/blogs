# 蒸馏小余 · 个人网站(简历型)

基于本仓库博客资源构建的纯静态站点:**简历型个人主页**(Hero / 研究方向 / 近期写作 / 关于我 / 签名页脚)+ 全部成品文章的站内全文阅读。
技术栈:Vite + 原生 JS。设计:编辑排版风——衬线中文大标题 + 等宽元数据、左侧粘性栏目签的非对称栅格、单一蓝色强调 + 蓝色签名页脚。

## 本地开发

```bash
cd site
npm install
npm run dev      # 先跑 generate-data 生成数据,再启动 Vite dev server
```

打开终端提示的地址(默认 `http://localhost:5173`)即可。三条路由:

- `/` —— 简历型首页:Hero(定位 + 数据概览)、01 研究方向(12 主题 + 篇数)、02 近期写作、03 关于我、蓝色签名页脚
- `/articles`(可带 `?topic=<id>`)—— 全部文章编号存档 + 主题筛选
- `/article/<slug>` —— 站内全文 + 配图 + 相关文章

## 数据来源与生成

数据由构建脚本从仓库内容**构建期生成**(产物已 gitignore,不入库):

```bash
npm run gen          # 生成 public/data/{graph.json,articles.json}
node build/verify-data.mjs   # 断言:主题=12、文章≥10、无悬空边、颜色合法、related 一致
```

- 数据驱动来源:`_kb_build/manifest.json`(成品文章的 `tags`/`moc`/`related` 元数据,按路径为 key)。
- 纳入口径:manifest 中 `type/article` 且 `platform/wechat` 的条目,跨 `outputs/`、`output/`、`post-to-wechat/`。
  - 自动排除小红书文案(`platform/xiaohongshu`)。
  - 同一篇文章的多个变体(`.optimized` / `.xiaoyu`)归一化后去重,优先 `.optimized`。
- 主题节点来自 `wiki/*.md`(排除 `INDEX.md`、`xiaoyu-2.0-rewrite-prompt.md`),共 12 个。
- 主题的中文名与一句话简介维护在 `src/topics.js`(摘自 `wiki/` MOC 页面首段)。
- **配图走 GitHub 图床**:正文 `imgs/...` 与封面在构建期重写为
  `https://cdn.jsdelivr.net/gh/Jouryjc/blogs@main/<文章目录>/<图片路径>`,
  不复制进产物(dist 从 ~307MB 降到 <1MB)。前提:图片必须先提交并推送到 main;
  jsDelivr 回源有 CDN 缓存,新推送的图片最长可能数小时后才生效。
- 改动源内容后重跑 `npm run gen` 即可刷新。

## 生产构建

```bash
npm run build    # = npm run gen(prebuild)+ vite build,产出 site/dist
npm run preview  # 本地预览 dist
```

`dist/` 含 `index.html`、`assets/`、`data/*.json`、`article-assets/**`。

## Cloudflare 部署

本仓库用 **Cloudflare Workers 静态资源**(assets-only Worker)托管,配置见 `site/wrangler.jsonc`。

Workers Builds(Git 集成)按以下设置:

- **构建命令(Build command)**:`cd site && npm ci && npm run build`
- **部署命令(Deploy command)**:`cd site && npx wrangler deploy`
- **根目录**:留空(命令里已 `cd site`)。
- **Node 版本**:≥ 18。

`site/wrangler.jsonc` 关键字段:

- `assets.directory: "./dist"` —— 只发布构建产物(不含 `node_modules`)。
- `assets.not_found_handling: "single-page-application"` —— SPA 路由 fallback,
  未命中路径回退 `index.html`;真实 `/assets/*.js`、`*.css` 仍按正确 MIME 返回。
  **不要**用 Pages 的 `_redirects`(`/* /index.html 200`),Workers 会判定为无限循环而拒绝部署。
- `name` 必须与 CF 上的 Worker 名称一致,否则会新建 Worker。

> 注:部署命令必须 `cd site`,让 wrangler 读到 `site/wrangler.jsonc`(指向 `./dist`)。
> 若从仓库根运行,会误把整个 `site/`(含 `node_modules`)当资源上传。

## 已知事项 / 后续优化(不在当前范围)

- **图片 CDN 缓存**:jsDelivr 对 `@main` 分支有缓存,新推送的配图可能延迟生效;
  如需立即可见可改用具象 commit hash  pinning。
- 其他可选:暗/亮色切换、RSS、个人经历时间线(待补充真实经历数据)。

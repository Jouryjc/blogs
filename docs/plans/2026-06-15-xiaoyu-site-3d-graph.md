# 蒸馏小余个人站点 · 3D 知识图谱 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 基于本仓库博客资源，构建一个纯静态站点：3D 深色星系风知识图谱首页 + 全部成品文章的站内全文阅读，部署到 Cloudflare Pages。

**Architecture:** 仓库 `site/` 子目录。构建期 `generate-data.mjs` 扫描 `wiki/` + `post-to-wechat`/`output` + `_kb_build/manifest.json`，产出 `graph.json`/`articles.json` 并复制配图；前端用 Vite + 原生 JS + `3d-force-graph`（Three.js + UnrealBloom）渲染首页图谱，配 history 路由的列表页与详情页。

**Tech Stack:** Node(ESM) 构建脚本、`gray-matter`、`markdown-it`、Vite、`3d-force-graph`、`three`。

**参考 spec：** `docs/superpowers/specs/2026-06-15-xiaoyu-site-3d-graph-design.md`

**测试说明：** 本仓库无单测框架，本项目以「脚本断言 + 可运行 + 数据正确性」为验收。数据层用 Node 断言脚本验证；前端用 `npm run dev` 目视验收。每个 Task 末尾 commit。

---

## Task 1: 脚手架与依赖

**Files:**
- Create: `site/package.json`
- Create: `site/vite.config.js`
- Create: `site/.gitignore`
- Create: `site/index.html`
- Create: `site/public/_redirects`
- Create: `site/src/main.js`（占位）

**Step 1: 初始化目录与 package.json**

`site/package.json`：
```json
{
  "name": "xiaoyu-site",
  "private": true,
  "type": "module",
  "scripts": {
    "gen": "node build/generate-data.mjs",
    "dev": "npm run gen && vite",
    "prebuild": "npm run gen",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.4.0"
  },
  "dependencies": {
    "3d-force-graph": "^1.73.0",
    "three": "^0.160.0",
    "gray-matter": "^4.0.3",
    "markdown-it": "^14.1.0"
  }
}
```

`site/vite.config.js`：
```js
import { defineConfig } from 'vite'
export default defineConfig({ base: '/', build: { outDir: 'dist' } })
```

`site/.gitignore`：
```
node_modules/
dist/
public/data/
public/article-assets/
```

`site/public/_redirects`：
```
/*    /index.html   200
```

`site/index.html`：
```html
<!doctype html>
<html lang="zh">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
    <title>蒸馏小余 · AI Agent 工程化知识库</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

`site/src/main.js`（占位，后续替换）：
```js
document.getElementById('app').textContent = 'scaffold ok'
```

**Step 2: 安装依赖**

Run: `cd site && npm install`
Expected: 安装成功，生成 `node_modules` 与 `package-lock.json`。

**Step 3: 启动确认脚手架可运行**

Run: `cd site && npx vite --port 5180` （手动开浏览器看到 "scaffold ok" 后 Ctrl-C）
Expected: 页面显示 scaffold ok。

**Step 4: Commit**

```bash
git add site/package.json site/package-lock.json site/vite.config.js site/.gitignore site/index.html site/public/_redirects site/src/main.js
git commit -m "feat(site): 脚手架与依赖"
```

---

## Task 2: 数据生成脚本 generate-data.mjs

**Files:**
- Create: `site/build/generate-data.mjs`
- Create: `site/build/verify-data.mjs`（一次性断言脚本，可保留）

**Step 1: 写 generate-data.mjs**

核心逻辑（完整实现）：
```js
// site/build/generate-data.mjs
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import matter from 'gray-matter'
import MarkdownIt from 'markdown-it'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const REPO = path.resolve(__dirname, '../..')       // 仓库根
const SITE = path.resolve(__dirname, '..')
const DATA_DIR = path.join(SITE, 'public/data')
const ASSET_DIR = path.join(SITE, 'public/article-assets')

const md = new MarkdownIt({ html: true, linkify: true, typographer: true })

// 12 主题色（低饱和但发光）
const TOPIC_COLORS = {
  'claude-code':'#6db1ff','agent-skills':'#8fe3a6','agent-memory':'#ffd479',
  'context-engineering':'#ff9ec4','prompt-caching':'#b39 dff','rag':'#7ad0d6',
  'managed-agents':'#f6a96b','agent-runtime':'#9fd356','agent-design':'#c9a7ff',
  'agent-safety':'#ff8a8a','knowledge-base':'#74c0fc','ai-industry':'#ffe08a'
}

function read(p){ return fs.readFileSync(p,'utf8') }
function exists(p){ return fs.existsSync(p) }

// --- 1. 主题节点 ---
function buildTopics(){
  const dir = path.join(REPO,'wiki')
  const skip = new Set(['INDEX.md','xiaoyu-2.0-rewrite-prompt.md'])
  const nodes = []
  for(const f of fs.readdirSync(dir)){
    if(!f.endsWith('.md') || skip.has(f)) continue
    const id = f.replace(/\.md$/,'')
    const g = matter(read(path.join(dir,f)))
    const title = (g.data.title||id).replace(/ ·.*$/,'').trim()
    nodes.push({ id, type:'topic', title, slug:id,
      color: TOPIC_COLORS[id]||'#9db4ff', val: 14 })
  }
  return nodes
}

// --- 2. 成品文章发现 ---
function articleDirs(){
  const out = []
  for(const base of ['post-to-wechat','output']){
    const root = path.join(REPO, base)
    if(!exists(root)) continue
    walkArticleDirs(root, out)
  }
  return out
}
function walkArticleDirs(root, out){
  // post-to-wechat/<date>/<slug>/  与 output/<slug>/
  const stack = [root]
  while(stack.length){
    const d = stack.pop()
    const entries = fs.readdirSync(d,{withFileTypes:true})
    const slug = path.basename(d)
    const main = pickMain(d, slug)
    if(main){ out.push({ dir:d, slug, main }) ; continue }
    for(const e of entries){
      if(e.isDirectory() && !['source','imgs','illustrations','cover-image','prompts','raw'].includes(e.name))
        stack.push(path.join(d,e.name))
    }
  }
}
function pickMain(dir, slug){
  const cands = [`${slug}.md`, 'article.md']
  for(const c of cands){
    const p = path.join(dir,c)
    if(exists(p)){
      const g = matter(read(p))
      const tags = g.data.tags||[]
      if(g.data.title && tags.some(t=>String(t).includes('type/article'))) return c
    }
  }
  return null
}

// --- 3. moc/related 解析辅助 ---
function parseMoc(data){
  const out = new Set()
  for(const m of (data.moc||[])){
    const mm = String(m).match(/\[\[([^\]|]+)/); if(mm) out.add(mm[1].trim())
  }
  for(const t of (data.tags||[])){
    const tt = String(t).match(/^topic\/(.+)$/); if(tt) out.add(tt[1].trim())
  }
  return [...out]
}

function main(){
  fs.rmSync(DATA_DIR,{recursive:true,force:true})
  fs.rmSync(ASSET_DIR,{recursive:true,force:true})
  fs.mkdirSync(DATA_DIR,{recursive:true})
  fs.mkdirSync(ASSET_DIR,{recursive:true})

  const manifest = JSON.parse(read(path.join(REPO,'_kb_build/manifest.json')))
  const topics = buildTopics()
  const topicIds = new Set(topics.map(t=>t.id))

  const found = articleDirs()
  const articles = {}        // slug -> meta
  const nodes = [...topics]
  const links = []
  const skipped = []

  for(const {dir, slug, main} of found){
    const p = path.join(dir, main)
    const g = matter(read(p))
    const d = g.data
    const mocs = parseMoc(d).filter(x=>topicIds.has(x))
    const primary = mocs[0] || 'ai-industry'

    // 配图复制
    copyImgs(dir, slug)
    const htmlRaw = md.render(g.content)
    const html = rewriteImgs(htmlRaw, slug)
    const cover = d.coverImage ? `/article-assets/${slug}/${d.coverImage}` : null

    nodes.push({ id:slug, type:'article', title:d.title, slug,
      topic:primary, color: TOPIC_COLORS[primary]||'#9db4ff', val:5,
      summary: d.summary||'' })
    for(const m of mocs) links.push({ source:slug, target:m, kind:'moc' })

    articles[slug] = {
      title:d.title, summary:d.summary||'', author:d.author||'蒸馏小余',
      date:d.created_at||'', topic:primary, tags:d.tags||[],
      cover, related:[], html
    }
  }

  // related 边（来自 manifest，目标必须是已纳入文章）
  const slugSet = new Set(Object.keys(articles))
  for(const [p, m] of Object.entries(manifest)){
    const src = path.basename(path.dirname(p))
    if(!slugSet.has(src)) continue
    for(const r of (m.related||[])){
      if(slugSet.has(r) && r!==src){
        links.push({ source:src, target:r, kind:'related' })
        articles[src].related.push(r)
      }
    }
  }

  // 丢弃悬空边
  const ids = new Set(nodes.map(n=>n.id))
  const clean = links.filter(l=>ids.has(l.source)&&ids.has(l.target))

  fs.writeFileSync(path.join(DATA_DIR,'graph.json'),
    JSON.stringify({nodes, links:clean}))
  fs.writeFileSync(path.join(DATA_DIR,'articles.json'),
    JSON.stringify(articles))

  console.log(`主题节点: ${topics.length}`)
  console.log(`文章节点: ${Object.keys(articles).length}`)
  console.log(`边: ${clean.length} (moc+related)`)
  console.log('纳入文章:'); for(const s of Object.keys(articles)) console.log('  +', s)
}

function copyImgs(dir, slug){
  const src = path.join(dir,'imgs')
  if(!exists(src)) return
  const dst = path.join(ASSET_DIR, slug, 'imgs')
  fs.mkdirSync(dst,{recursive:true})
  copyDir(src,dst)
}
function copyDir(s,d){
  for(const e of fs.readdirSync(s,{withFileTypes:true})){
    const sp=path.join(s,e.name), dp=path.join(d,e.name)
    if(e.isDirectory()){ fs.mkdirSync(dp,{recursive:true}); copyDir(sp,dp) }
    else if(/\.(png|jpe?g|gif|webp|svg)$/i.test(e.name)) fs.copyFileSync(sp,dp)
  }
}
function rewriteImgs(html, slug){
  return html.replace(/(src=")(\.\/)?(imgs\/[^"]+)(")/g,
    (_,a,_b,p,z)=>`${a}/article-assets/${slug}/${p}${z}`)
}

main()
```

注：`TOPIC_COLORS` 里 `'#b39 dff'` 是占位错字，实现时写成合法 6 位 hex（如 `#b39dff`）。所有颜色都要是合法 hex。

**Step 2: 运行并核对纳入清单**

Run: `cd site && node build/generate-data.mjs`
Expected: 打印「主题节点: 12」、文章节点数（与 `_kb_build/inventory.json` 的 first_class article 数量大致吻合），并逐条列出纳入文章 slug。人工扫一眼有无误纳入草稿/source、或漏掉成品。

**Step 3: 写 verify-data.mjs 断言**

```js
// site/build/verify-data.mjs
import fs from 'node:fs'
const g = JSON.parse(fs.readFileSync('public/data/graph.json'))
const a = JSON.parse(fs.readFileSync('public/data/articles.json'))
const ids = new Set(g.nodes.map(n=>n.id))
const dangling = g.links.filter(l=>!ids.has(l.source)||!ids.has(l.target))
const topics = g.nodes.filter(n=>n.type==='topic')
const arts = g.nodes.filter(n=>n.type==='article')
let bad=0
if(topics.length!==12){ console.error('主题数≠12:',topics.length); bad++ }
if(arts.length<10){ console.error('文章数过少:',arts.length); bad++ }
if(dangling.length){ console.error('悬空边:',dangling.length); bad++ }
for(const n of arts){ if(!a[n.id]||!a[n.id].html){ console.error('缺正文:',n.id); bad++ } }
// 颜色合法性
for(const n of g.nodes){ if(!/^#[0-9a-f]{6}$/i.test(n.color)){ console.error('非法色:',n.id,n.color); bad++ } }
console.log(bad? `FAIL(${bad})` : `OK 主题${topics.length} 文章${arts.length} 边${g.links.length}`)
process.exit(bad?1:0)
```

**Step 4: 运行断言**

Run: `cd site && node build/verify-data.mjs`
Expected: 输出 `OK 主题12 文章N 边M`，退出码 0。若失败按提示修 generate-data.mjs（含颜色 hex）。

**Step 5: Commit**

```bash
git add site/build/generate-data.mjs site/build/verify-data.mjs
git commit -m "feat(site): 数据生成脚本与校验"
```

---

## Task 3: 路由与运行时数据加载

**Files:**
- Create: `site/src/router.js`
- Create: `site/src/data.js`
- Create: `site/src/styles/base.css`
- Modify: `site/src/main.js`（替换占位）

**Step 1: data.js — 加载并缓存 JSON**

```js
// site/src/data.js
let _graph, _articles
export async function getGraph(){ return _graph ??= await (await fetch('/data/graph.json')).json() }
export async function getArticles(){ return _articles ??= await (await fetch('/data/articles.json')).json() }
```

**Step 2: router.js — 极简 history 路由**

```js
// site/src/router.js
const routes = []
export function route(pattern, handler){ routes.push({pattern, handler}) }
export function navigate(to){ history.pushState({}, '', to); render() }
export async function render(){
  const url = new URL(location.href)
  const pathn = url.pathname
  for(const {pattern, handler} of routes){
    const m = pattern.exec(pathn)
    if(m){ await handler({ params:m.groups||{}, query:url.searchParams }); return }
  }
  routes[0]?.handler({ params:{}, query:url.searchParams })
}
window.addEventListener('popstate', render)
document.addEventListener('click', e=>{
  const a = e.target.closest('a[data-link]')
  if(a){ e.preventDefault(); navigate(a.getAttribute('href')) }
})
```

**Step 3: main.js — 注册路由**

```js
// site/src/main.js
import './styles/base.css'
import { route, render } from './router.js'
import { renderHome } from './pages/home.js'
import { renderList } from './pages/list.js'
import { renderArticle } from './pages/article.js'

const app = document.getElementById('app')
route(/^\/$/, ()=>renderHome(app))
route(/^\/articles$/, (ctx)=>renderList(app, ctx))
route(/^\/article\/(?<slug>[^/]+)$/, (ctx)=>renderArticle(app, ctx))
render()
```

**Step 4: base.css — 全局深色基底**

```css
:root{ --bg:#05060f; --panel:#0d1020; --fg:#e8ecf6; --muted:#9aa3bd; --line:#1d2340; }
*{ box-sizing:border-box }
html,body{ margin:0; height:100%; background:var(--bg); color:var(--fg);
  font-family:-apple-system,"PingFang SC","Microsoft YaHei",system-ui,sans-serif; }
a{ color:#8fb6ff; text-decoration:none }
#app{ min-height:100% }
```

为避免 import 报错，先建空的三个 page 文件占位（导出空函数），下一 Task 实现。

```bash
mkdir -p site/src/pages
printf "export function renderHome(app){app.textContent='home'}\n" > site/src/pages/home.js
printf "export function renderList(app){app.textContent='list'}\n" > site/src/pages/list.js
printf "export function renderArticle(app){app.textContent='article'}\n" > site/src/pages/article.js
```

**Step 5: 验证路由可切换**

Run: `cd site && npm run dev`（浏览器手动访问 `/`, `/articles`, `/article/x`，分别看到 home/list/article）
Expected: 三条路由文本正确切换；刷新 `/articles` 不 404（dev server 下 Vite history fallback）。

**Step 6: Commit**

```bash
git add site/src/router.js site/src/data.js site/src/main.js site/src/styles/base.css site/src/pages/
git commit -m "feat(site): 路由、数据加载与全局样式"
```

---

## Task 4: 首页 3D 知识图谱（星系风 + HUD）

**Files:**
- Create: `site/src/graph/graph3d.js`
- Modify: `site/src/pages/home.js`
- Create: `site/src/styles/home.css`

**Step 1: graph3d.js — 封装 3d-force-graph + Bloom**

要点（实现）：
```js
// site/src/graph/graph3d.js
import ForceGraph3D from '3d-force-graph'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { navigate } from '../router.js'

export function createGraph(el, data, { onTopicFocus } = {}){
  const isMobile = matchMedia('(max-width:768px)').matches
  const Graph = ForceGraph3D()(el)
    .backgroundColor('#05060f')
    .graphData(data)
    .nodeLabel(n=> n.type==='topic'
      ? `<b>${n.title}</b>` : `${n.title}<br><i>${n.summary||''}</i>`)
    .nodeVal(n=>n.val)
    .nodeColor(n=>n.color)
    .nodeOpacity(0.92)
    .nodeResolution(isMobile?8:16)
    .linkColor(l=> l.kind==='moc' ? 'rgba(150,180,255,0.55)' : 'rgba(120,130,170,0.25)')
    .linkWidth(l=> l.kind==='moc'?0.6:0.25)
    .linkDirectionalParticles(isMobile?0:1)
    .onNodeClick(n=>{
      if(n.type==='article') navigate(`/article/${n.slug}`)
      else onTopicFocus?.(n)
    })
  if(!isMobile){
    const bloom = new UnrealBloomPass()
    bloom.strength = 1.6; bloom.radius = 0.8; bloom.threshold = 0.1
    Graph.postProcessingComposer().addPass(bloom)
  }
  // 缓慢自转
  let angle = 0; const dist = 320
  Graph.cameraPosition({ z: dist })
  const timer = setInterval(()=>{
    if(Graph.__paused) return
    angle += Math.PI/1500
    Graph.cameraPosition({ x: dist*Math.sin(angle), z: dist*Math.cos(angle) })
  }, 30)
  el.addEventListener('mousedown', ()=>Graph.__paused=true)
  Graph.__timer = timer
  return Graph
}
```

**Step 2: home.css — HUD 叠层**

```css
.home{ position:fixed; inset:0 }
.home .graph{ position:absolute; inset:0 }
.hud{ position:absolute; pointer-events:none; z-index:2 }
.hud-brand{ top:24px; left:28px }
.hud-brand h1{ margin:0; font-size:20px; letter-spacing:.5px }
.hud-brand p{ margin:4px 0 0; color:var(--muted); font-size:13px }
.hud-legend{ top:24px; right:24px; display:flex; flex-direction:column; gap:6px;
  pointer-events:auto; max-height:70vh; overflow:auto }
.hud-legend button{ display:flex; align-items:center; gap:8px; background:none;
  border:0; color:var(--fg); font-size:12px; cursor:pointer; opacity:.8 }
.hud-legend .dot{ width:10px; height:10px; border-radius:50% }
.hud-search{ top:22px; left:50%; transform:translateX(-50%); pointer-events:auto }
.hud-search input{ width:260px; padding:8px 14px; border-radius:20px;
  border:1px solid var(--line); background:rgba(13,16,32,.8); color:var(--fg) }
.hud-enter{ bottom:28px; right:28px; pointer-events:auto;
  padding:10px 18px; border-radius:22px; border:1px solid var(--line);
  background:rgba(13,16,32,.8); color:var(--fg) }
@media(max-width:768px){ .hud-legend{ display:none } .hud-search input{ width:180px } }
```

**Step 3: home.js — 组装图谱 + HUD + 交互**

实现：构造 `.home` 容器、`.graph` 挂载点、HUD（brand / legend / search / enter）。
- 加载 `getGraph()`，调 `createGraph`。
- legend：遍历 graph 中 `type==='topic'` 节点生成色点按钮，点击 = 聚焦该主题相机 + 高亮邻居（其余 link 节点变暗）。
- search：输入实时过滤，匹配则 `Graph.cameraPosition` 聚焦第一个匹配节点。
- `onTopicFocus(n)`：第一次点高亮，连续点同一主题 → `navigate('/articles?topic='+n.id)`。
- enter 按钮：`navigate('/articles')`。
- 离开首页时 `clearInterval(Graph.__timer)`（在 home 返回的 cleanup 里；可用模块级变量保存当前 Graph，路由切换前销毁）。

```js
// site/src/pages/home.js
import './../styles/home.css'
import { getGraph } from '../data.js'
import { createGraph } from '../graph/graph3d.js'
import { navigate } from '../router.js'

let current
export async function renderHome(app){
  if(current){ clearInterval(current.__timer); current._destructor?.(); current=null }
  const data = await getGraph()
  app.innerHTML = `
    <div class="home">
      <div class="graph"></div>
      <div class="hud hud-brand"><h1>蒸馏小余 · AI Agent 工程化知识库</h1>
        <p>把论文 / 推文 / 笔记，蒸馏成一张可漫游的知识星图</p></div>
      <div class="hud hud-search"><input placeholder="搜索文章 / 主题…" /></div>
      <div class="hud hud-legend"></div>
      <button class="hud hud-enter">进入文章列表 →</button>
    </div>`
  const el = app.querySelector('.graph')
  let lastTopic
  const Graph = createGraph(el, data, {
    onTopicFocus(n){
      focusNode(Graph, n)
      if(lastTopic===n.id) navigate('/articles?topic='+n.id)
      lastTopic = n.id
    }
  })
  current = Graph
  // legend
  const legend = app.querySelector('.hud-legend')
  legend.innerHTML = data.nodes.filter(n=>n.type==='topic')
    .map(n=>`<button data-id="${n.id}"><span class="dot" style="background:${n.color}"></span>${n.title}</button>`).join('')
  legend.addEventListener('click',e=>{ const b=e.target.closest('button'); if(!b)return
    const n=data.nodes.find(x=>x.id===b.dataset.id); focusNode(Graph,n) })
  // search
  app.querySelector('.hud-search input').addEventListener('input',e=>{
    const q=e.target.value.trim(); if(!q)return
    const n=data.nodes.find(x=>x.title.includes(q)); if(n) focusNode(Graph,n) })
  app.querySelector('.hud-enter').addEventListener('click',()=>navigate('/articles'))
}
function focusNode(Graph, n){
  if(!n||n.x==null){ return }
  const d=120, r=1+d/Math.hypot(n.x,n.y,n.z||1)
  Graph.cameraPosition({x:n.x*r,y:n.y*r,z:(n.z||1)*r},{x:n.x,y:n.y,z:n.z},1000)
}
```

**Step 4: 验证首页**

Run: `cd site && npm run dev`
Expected: 看到深色星空、发光节点（主题大、文章小）、连线；可旋转/缩放；hover 出 tooltip；点击主题聚焦、再点进列表；点击文章进详情；legend 与搜索可聚焦；移动端窄屏图谱降级且 legend 隐藏。

**Step 5: Commit**

```bash
git add site/src/graph/ site/src/pages/home.js site/src/styles/home.css
git commit -m "feat(site): 3D 星系知识图谱首页与 HUD"
```

---

## Task 5: 文章列表页（主题筛选）

**Files:**
- Modify: `site/src/pages/list.js`
- Create: `site/src/styles/list.css`

**Step 1: list.js**

实现：加载 `getGraph()`（取 topic 列表）+ `getArticles()`。
- 顶部返回首页链接 + 主题 tab（「全部」+ 12 主题，含色点）。
- `?topic=<id>` 决定初始选中；点 tab 用 `navigate('/articles?topic=...')`。
- 卡片网格：每篇封面图（`cover`，无则纯色占位用主题色渐变）、标题、摘要、日期、主题色左边条；点击 `navigate('/article/'+slug)`。
- 按 `date` 倒序。

```js
// site/src/pages/list.js
import './../styles/list.css'
import { getArticles, getGraph } from '../data.js'
import { navigate } from '../router.js'

export async function renderList(app, ctx){
  const [articles, graph] = await Promise.all([getArticles(), getGraph()])
  const topics = graph.nodes.filter(n=>n.type==='topic')
  const tColor = Object.fromEntries(topics.map(t=>[t.id,t.color]))
  const sel = ctx.query.get('topic') || 'all'
  const items = Object.entries(articles)
    .map(([slug,a])=>({slug,...a}))
    .filter(a=> sel==='all' || a.topic===sel || (a.tags||[]).includes('topic/'+sel))
    .sort((x,y)=> (y.date||'').localeCompare(x.date||''))
  const tabs = [{id:'all',title:'全部',color:'#9db4ff'},...topics]
  app.innerHTML = `
    <div class="list-wrap">
      <header class="list-top">
        <a href="/" data-link class="back">← 星图首页</a>
        <h2>全部文章 · ${items.length}</h2>
        <nav class="tabs">${tabs.map(t=>`
          <a data-link href="/articles${t.id==='all'?'':'?topic='+t.id}"
             class="tab ${t.id===sel?'on':''}">
             <span class="dot" style="background:${t.color}"></span>${t.title}</a>`).join('')}</nav>
      </header>
      <div class="grid">${items.map(a=>card(a,tColor)).join('')}</div>
    </div>`
  app.querySelectorAll('.card').forEach(c=>c.addEventListener('click',
    ()=>navigate('/article/'+c.dataset.slug)))
}
function card(a, tColor){
  const c = tColor[a.topic]||'#9db4ff'
  const cover = a.cover
    ? `<img loading="lazy" src="${a.cover}" alt="">`
    : `<div class="ph" style="background:linear-gradient(135deg,${c}33,${c}11)"></div>`
  return `<article class="card" data-slug="${a.slug}" style="--c:${c}">
    <div class="cover">${cover}</div>
    <div class="body"><h3>${a.title}</h3><p>${a.summary||''}</p>
      <span class="meta">${a.date||''}</span></div></article>`
}
```

**Step 2: list.css**

实现：`.list-wrap` 居中容器（max-width ~1100px）；`.tabs` 横向可滚动；`.grid` 用 `grid-template-columns:repeat(auto-fill,minmax(260px,1fr))`；卡片深色面板、左侧 `--c` 色条、hover 上浮发光；封面 16:9 裁剪。窄屏单列。

**Step 3: 验证**

Run: `cd site && npm run dev` → 访问 `/articles`
Expected: 卡片网格正确、封面显示、tab 筛选切换 URL 与内容、点击进详情、移动端单列。

**Step 4: Commit**

```bash
git add site/src/pages/list.js site/src/styles/list.css
git commit -m "feat(site): 文章列表页与主题筛选"
```

---

## Task 6: 文章详情页（站内全文 + 相关文章）

**Files:**
- Modify: `site/src/pages/article.js`
- Create: `site/src/styles/article.css`

**Step 1: article.js**

实现：按 `slug` 取 `articles[slug]`。
- 不存在 → 显示「文章不存在」+ 返回链接。
- 渲染：返回首页/列表链接、封面（有则显示）、标题、作者+日期 meta、主题色标签、`.prose` 注入 `a.html`（已是安全的自产 HTML）。
- 「相关文章」：`a.related` 映射成小卡片，点击跳转；无则不显示该区块。
- **不渲染任何微信原文外链。**
- 注入后把页面滚动置顶。

```js
// site/src/pages/article.js
import './../styles/article.css'
import { getArticles } from '../data.js'
import { navigate } from '../router.js'

export async function renderArticle(app, ctx){
  const slug = ctx.params.slug
  const articles = await getArticles()
  const a = articles[slug]
  if(!a){ app.innerHTML = `<div class="article-wrap"><p>文章不存在。</p>
    <a href="/articles" data-link>← 返回列表</a></div>`; return }
  const related = (a.related||[]).map(s=>({slug:s,...articles[s]})).filter(x=>x.title)
  app.innerHTML = `
    <div class="article-wrap">
      <div class="nav"><a href="/" data-link>← 星图</a>
        <a href="/articles" data-link>全部文章</a></div>
      ${a.cover?`<img class="hero" src="${a.cover}" alt="">`:''}
      <h1>${a.title}</h1>
      <div class="meta">${a.author||'蒸馏小余'} · ${a.date||''}</div>
      <article class="prose">${a.html}</article>
      ${related.length?`<section class="related"><h3>相关文章</h3>
        <div class="rel-grid">${related.map(r=>`
          <a class="rel" data-link href="/article/${r.slug}">
            <span>${r.title}</span><small>${r.summary||''}</small></a>`).join('')}</div>
      </section>`:''}
    </div>`
  scrollTo(0,0)
}
```

**Step 2: article.css**

实现：`.article-wrap` 居中（max-width ~760px，行宽舒适）；`.hero` 2.35:1 圆角；`.prose` 排版：行高 1.8、段距、`h2/h3` 间距、`img` 圆角自适应宽度居中、`pre/code` 深色块、`blockquote` 左色条、`a` 高亮色、`ul/ol` 缩进；`.related` 小卡片网格。整体深色阅读主题，正文 `--fg` 高对比。

**Step 3: 验证**

Run: `cd site && npm run dev` → 从列表点进 3 篇不同文章
Expected: 封面 + 标题 + meta + 全文 + 内文配图（路径 `/article-assets/...` 正常加载）显示正确；相关文章可跳转；无微信外链；窄屏可读。

**Step 4: Commit**

```bash
git add site/src/pages/article.js site/src/styles/article.css
git commit -m "feat(site): 文章详情页与站内全文阅读"
```

---

## Task 7: 生产构建、部署配置与文档

**Files:**
- Create: `site/README.md`
- 确认：`site/public/_redirects`、`site/vite.config.js`

**Step 1: 生产构建验证**

Run: `cd site && npm run build`
Expected: `prebuild` 跑 gen 成功 → `vite build` 产出 `site/dist`，含 `dist/data/*.json`、`dist/article-assets/**`、`dist/_redirects`。

**Step 2: 预览生产包**

Run: `cd site && npm run preview`（手动访问 `/`、`/articles`、`/article/<slug>` 并刷新）
Expected: 三页正常；直接刷新子路由由 `_redirects`（preview 下 Vite 近似）返回应用。

**Step 3: 写 README（CF Pages 部署说明）**

`site/README.md` 内容覆盖：
- 本地：`npm install` → `npm run dev`。
- 数据来源与 `npm run gen` 说明（产物为构建期生成、已 gitignore）。
- **Cloudflare Pages 部署**：
  - 连接 GitHub 仓库。
  - Build command：`cd site && npm ci && npm run build`
  - Build output directory：`site/dist`
  - 框架预设：None；Node 版本 ≥ 18。
  - `_redirects` 已处理 SPA history 路由 fallback。
  - 自定义域名在 CF 面板绑定。

**Step 4: Commit**

```bash
git add site/README.md
git commit -m "docs(site): 生产构建与 Cloudflare Pages 部署说明"
```

---

## 完成后

- 全部 7 个 Task 完成后，`feat/xiaoyu-site` 分支包含完整站点。
- 用 superpowers:finishing-a-development-branch 决定合并/PR。
- 后续可选优化（YAGNI，不在本计划内）：配图压缩、节点聚类布局、暗色/亮色切换、RSS。

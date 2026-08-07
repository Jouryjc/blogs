// site/build/generate-data.mjs
// manifest 驱动的数据生成：扫描 _kb_build/manifest.json 的成品文章,
// 产出 public/data/{graph.json,articles.json}。
// 配图不入产物:直接引用 GitHub 图床(jsDelivr 回源 Jouryjc/blogs 仓库内的 imgs/)。
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import matter from 'gray-matter'
import MarkdownIt from 'markdown-it'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const REPO = path.resolve(__dirname, '../..') // 仓库根
const SITE = path.resolve(__dirname, '..')
const DATA_DIR = path.join(SITE, 'public/data')

// GitHub 图床:jsDelivr 回源 main 分支(新增图片推送后可能有最长数小时 CDN 缓存延迟)
const CDN_BASE = 'https://cdn.jsdelivr.net/gh/Jouryjc/blogs@main'

const md = new MarkdownIt({ html: true, linkify: true, typographer: true })

// 12 主题色（低饱和但发光）
const TOPIC_COLORS = {
  'claude-code': '#6db1ff', 'agent-skills': '#8fe3a6', 'agent-memory': '#ffd479',
  'context-engineering': '#ff9ec4', 'prompt-caching': '#b39dff', 'rag': '#7ad0d6',
  'managed-agents': '#f6a96b', 'agent-runtime': '#9fd356', 'agent-design': '#c9a7ff',
  'agent-safety': '#ff8a8a', 'knowledge-base': '#74c0fc', 'ai-industry': '#ffe08a',
}
const DEFAULT_COLOR = '#9db4ff'

const read = (p) => fs.readFileSync(p, 'utf8')
const exists = (p) => fs.existsSync(p)

// slug：去扩展名 + 去 .optimized/.xiaoyu 变体后缀；通用主文件名用父目录名
function normSlug(s) { return String(s).replace(/\.(optimized|xiaoyu)$/, '') }
function slugFromPath(p) {
  let b = path.basename(p).replace(/\.md$/, '')
  if (b === 'article' || b === 'index') b = path.basename(path.dirname(p))
  return normSlug(b)
}

// --- 1. 主题节点（wiki/*.md，预期 12） ---
function buildTopics() {
  const dir = path.join(REPO, 'wiki')
  const skip = new Set(['INDEX.md', 'xiaoyu-2.0-rewrite-prompt.md'])
  const nodes = []
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith('.md') || skip.has(f)) continue
    const id = f.replace(/\.md$/, '')
    const g = matter(read(path.join(dir, f)))
    const title = (g.data.title || id).replace(/ ·.*$/, '').trim()
    nodes.push({ id, type: 'topic', title, slug: id, color: TOPIC_COLORS[id] || DEFAULT_COLOR, val: 14 })
  }
  return nodes
}

// frontmatter moc 兜底解析（manifest 缺 moc 时用）
function parseMocFrontmatter(data) {
  const out = new Set()
  for (const m of (data.moc || [])) {
    const mm = String(m).match(/\[\[([^\]|]+)/)
    out.add((mm ? mm[1] : String(m)).trim())
  }
  return [...out]
}

function main() {
  fs.rmSync(DATA_DIR, { recursive: true, force: true })
  fs.mkdirSync(DATA_DIR, { recursive: true })

  const manifest = JSON.parse(read(path.join(REPO, '_kb_build/manifest.json')))
  const topics = buildTopics()
  const topicIds = new Set(topics.map((t) => t.id))

  // 候选：manifest 中 type/article 且 platform/wechat（排除小红书等），且文件存在
  const candidates = Object.entries(manifest)
    .filter(([, v]) => (v.tags || []).includes('type/article') && (v.tags || []).includes('platform/wechat'))
    .map(([p, v]) => ({
      p, v,
      slug: slugFromPath(p),
      optimized: /\.optimized$/.test(path.basename(p).replace(/\.md$/, '')),
    }))
    .filter((c) => exists(path.join(REPO, c.p)))

  // 去重：同 slug 取 .optimized 优先，否则 post-to-wechat > outputs > output
  const rank = (c) => (c.optimized ? 0 : c.p.startsWith('post-to-wechat') ? 1 : c.p.startsWith('outputs') ? 2 : 3)
  const bySlug = new Map()
  for (const c of candidates) {
    const cur = bySlug.get(c.slug)
    if (!cur || rank(c) < rank(cur)) bySlug.set(c.slug, c)
  }
  const chosen = [...bySlug.values()].sort((a, b) => a.slug.localeCompare(b.slug))
  const slugSet = new Set(chosen.map((c) => c.slug))

  const articles = {}
  const nodes = [...topics]
  const links = []

  for (const c of chosen) {
    const full = path.join(REPO, c.p)
    const g = matter(read(full))
    const d = g.data
    const slug = c.slug
    const dir = path.dirname(full)

    // moc：manifest 优先，回退 frontmatter；过滤为合法主题
    const mocRaw = (c.v.moc && c.v.moc.length) ? c.v.moc.map(String) : parseMocFrontmatter(d)
    const mocs = [...new Set(mocRaw.map((x) => x.trim()))].filter((x) => topicIds.has(x))
    const primary = mocs[0] || 'ai-industry'

    // 正文渲染（去掉与标题重复的正文首个 H1，详情页另行渲染标题）
    const body = g.content.replace(/^\s*#\s+.*(\r?\n)+/, '')
    const htmlRaw = md.render(body)

    // 配图:不复制进产物,直接指到 GitHub 图床(jsDelivr 回源仓库内原始路径)
    const dirRel = path.dirname(c.p).split(path.sep).join('/')
    const coverRel = (d.coverImage || d.cover || '').replace(/^\.\//, '')

    const html = rewriteImgs(htmlRaw, dirRel)
    const cover = coverRel && exists(path.join(dir, coverRel)) ? `${CDN_BASE}/${dirRel}/${coverRel}` : null

    nodes.push({
      id: slug, type: 'article', title: d.title, slug,
      topic: primary, color: TOPIC_COLORS[primary] || DEFAULT_COLOR, val: 5,
      summary: d.summary || '',
    })
    for (const mtopic of mocs) links.push({ source: slug, target: mtopic, kind: 'moc' })

    articles[slug] = {
      title: d.title, summary: d.summary || '', author: d.author || '蒸馏小余',
      date: d.created_at || '', topic: primary, tags: c.v.tags || [],
      cover, related: [], html,
    }
  }

  // related 边（manifest）：归一化 + 仅指向已纳入文章；无向去重；双向写入 related 便于详情页
  const seen = new Set()
  for (const c of chosen) {
    const src = c.slug
    for (const r of (c.v.related || [])) {
      const tgt = normSlug(String(r).trim())
      if (tgt === src || !slugSet.has(tgt)) continue
      const key = [src, tgt].sort().join('::')
      if (seen.has(key)) continue
      seen.add(key)
      links.push({ source: src, target: tgt, kind: 'related' })
      articles[src].related.push(tgt)
      articles[tgt].related.push(src)
    }
  }

  // 丢弃悬空边
  const ids = new Set(nodes.map((n) => n.id))
  const clean = links.filter((l) => ids.has(l.source) && ids.has(l.target))

  fs.writeFileSync(path.join(DATA_DIR, 'graph.json'), JSON.stringify({ nodes, links: clean }))
  fs.writeFileSync(path.join(DATA_DIR, 'articles.json'), JSON.stringify(articles))

  const mocN = clean.filter((l) => l.kind === 'moc').length
  const relN = clean.filter((l) => l.kind === 'related').length
  console.log(`主题节点: ${topics.length}`)
  console.log(`文章节点: ${Object.keys(articles).length}`)
  console.log(`边: ${clean.length} (moc ${mocN} + related ${relN})`)
  console.log('纳入文章:')
  for (const c of chosen) console.log(`  + ${c.slug}  [${c.p}]`)
}

function rewriteImgs(html, dirRel) {
  // 所有相对路径图片(imgs/、illustrations/、raw/ 等)统一改指 GitHub 图床
  return html.replace(/(src=")(?!https?:|data:|\/)(?:\.\/)?([^"]+)(")/g, (_, a, p, z) => `${a}${CDN_BASE}/${dirRel}/${p}${z}`)
}

main()

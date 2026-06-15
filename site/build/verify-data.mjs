// site/build/verify-data.mjs —— 数据正确性断言（在 site/ 下运行）
import fs from 'node:fs'
const g = JSON.parse(fs.readFileSync('public/data/graph.json'))
const a = JSON.parse(fs.readFileSync('public/data/articles.json'))
const ids = new Set(g.nodes.map((n) => n.id))
const dangling = g.links.filter((l) => !ids.has(l.source) || !ids.has(l.target))
const topics = g.nodes.filter((n) => n.type === 'topic')
const arts = g.nodes.filter((n) => n.type === 'article')
let bad = 0
if (topics.length !== 12) { console.error('主题数≠12:', topics.length); bad++ }
if (arts.length < 10) { console.error('文章数过少:', arts.length); bad++ }
if (dangling.length) { console.error('悬空边:', dangling.length); bad++ }
for (const n of arts) { if (!a[n.id] || !a[n.id].html) { console.error('缺正文:', n.id); bad++ } }
// 颜色合法性
for (const n of g.nodes) { if (!/^#[0-9a-f]{6}$/i.test(n.color)) { console.error('非法色:', n.id, n.color); bad++ } }
// related 一致性：article.related 必须指向已纳入文章
for (const [slug, art] of Object.entries(a)) {
  for (const r of (art.related || [])) { if (!a[r]) { console.error('related 悬空:', slug, '->', r); bad++ } }
}
console.log(bad ? `FAIL(${bad})` : `OK 主题${topics.length} 文章${arts.length} 边${g.links.length}`)
process.exit(bad ? 1 : 0)

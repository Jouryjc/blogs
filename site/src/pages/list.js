// site/src/pages/list.js —— 文章存档:主题筛选 + 编号列表
import { getArticles } from '../data.js'
import { TOPICS } from '../topics.js'
import { siteHead, signoff, esc } from '../ui.js'

export async function renderList(app, ctx) {
  const articles = (await getArticles()).filter((a) => a.date)
  const total = articles.length
  const counts = {}
  for (const a of articles) counts[a.topic] = (counts[a.topic] || 0) + 1
  const topics = Object.entries(TOPICS)
    .map(([id, t]) => ({ id, zh: t.zh, n: counts[id] || 0 }))
    .filter((t) => t.n > 0)

  let active = ctx.query.get('topic') || 'all'
  if (active !== 'all' && !counts[active]) active = 'all'

  app.innerHTML = `
    ${siteHead('archive')}
    <section class="archive-head">
      <p class="kicker">Archive · ${total} Articles</p>
      <h1>文章存档</h1>
      <p class="sub">${total} 篇深度长文,按时间倒序。每一篇都指向一个工程问题:不是"是什么",而是"怎么做才成立"。</p>
    </section>
    <div class="filters" id="filters">
      <button data-t="all" class="${active === 'all' ? 'on' : ''}">全部<span class="n">${total}</span></button>
      ${topics
        .map(
          (t) =>
            `<button data-t="${t.id}" class="${active === t.id ? 'on' : ''}">${t.zh}<span class="n">${t.n}</span></button>`,
        )
        .join('')}
    </div>
    <section class="archive" id="archive"></section>
    ${signoff()}
  `

  const archive = document.getElementById('archive')
  const draw = () => {
    const rows = articles.filter((a) => active === 'all' || a.topic === active)
    archive.innerHTML = rows.length
      ? rows
          .map(
            (a) => `
        <a class="entry" href="/article/${a.slug}" data-link>
          <span class="idx">${String(total - articles.indexOf(a)).padStart(3, '0')}</span>
          <span class="date">${a.date}</span>
          <span class="ttl">${esc(a.title)}</span>
          <span class="pill">${TOPICS[a.topic]?.zh || a.topic}</span>
        </a>`,
          )
          .join('')
      : '<p class="empty">// 这个方向还没有文章</p>'
  }
  draw()

  document.getElementById('filters').addEventListener('click', (e) => {
    const btn = e.target.closest('button[data-t]')
    if (!btn) return
    active = btn.dataset.t
    document.querySelectorAll('#filters button').forEach((b) => b.classList.toggle('on', b === btn))
    history.replaceState({}, '', active === 'all' ? '/articles' : `/articles?topic=${active}`)
    draw()
  })
}

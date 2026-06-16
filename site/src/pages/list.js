// site/src/pages/list.js —— 文章列表：卡片网格 + 主题筛选
import './../styles/list.css'
import { getArticles, getGraph } from '../data.js'
import { navigate } from '../router.js'

export async function renderList(app, ctx) {
  const [articles, graph] = await Promise.all([getArticles(), getGraph()])
  const topics = graph.nodes.filter((n) => n.type === 'topic')
  const tColor = Object.fromEntries(topics.map((t) => [t.id, t.color]))
  const sel = ctx.query.get('topic') || 'all'
  const items = Object.entries(articles)
    .map(([slug, a]) => ({ slug, ...a }))
    .filter((a) => sel === 'all' || a.topic === sel || (a.tags || []).includes('topic/' + sel))
    .sort((x, y) => (y.date || '').localeCompare(x.date || ''))
  const tabs = [{ id: 'all', title: '全部', color: '#9db4ff' }, ...topics]
  app.innerHTML = `
    <div class="list-wrap">
      <header class="list-top">
        <a href="/" data-link class="back">← 星图首页</a>
        <h2>全部文章 · ${items.length}</h2>
        <nav class="tabs">${tabs.map((t) => `
          <a data-link href="/articles${t.id === 'all' ? '' : '?topic=' + t.id}"
             class="tab ${t.id === sel ? 'on' : ''}">
             <span class="dot" style="background:${t.color}"></span>${t.title}</a>`).join('')}</nav>
      </header>
      <div class="grid">${items.map((a) => card(a, tColor)).join('')}</div>
    </div>`
  app.querySelectorAll('.card').forEach((c) => c.addEventListener('click', () => navigate('/article/' + c.dataset.slug)))
}

function card(a, tColor) {
  const c = tColor[a.topic] || '#9db4ff'
  const cover = a.cover
    ? `<img loading="lazy" src="${a.cover}" alt="">`
    : `<div class="ph" style="background:linear-gradient(135deg,${c}33,${c}11)"></div>`
  return `<article class="card" data-slug="${a.slug}" style="--c:${c}">
    <div class="cover">${cover}</div>
    <div class="body"><h3>${a.title}</h3><p>${a.summary || ''}</p>
      <span class="meta">${a.date || ''}</span></div></article>`
}

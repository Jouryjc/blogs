// site/src/pages/article.js —— 站内全文阅读
import { getArticles } from '../data.js'
import { TOPICS } from '../topics.js'
import { siteHead, signoff, esc } from '../ui.js'

export async function renderArticle(app, ctx) {
  const articles = await getArticles()
  const a = articles.find((x) => x.slug === ctx.params.slug)
  if (!a) {
    app.innerHTML = `${siteHead('archive')}
      <section class="read-head"><h1>文章不存在</h1>
      <p class="summary">这篇内容可能已被移除。<a class="read-back" href="/articles" data-link>回到文章存档</a></p></section>
      ${signoff()}`
    return
  }
  document.title = `${a.title} · 蒸馏小余`

  const related = (a.related || [])
    .map((r) => articles.find((x) => x.slug === r || x.slug.endsWith(r)))
    .filter(Boolean)
    .slice(0, 3)

  app.innerHTML = `
    ${siteHead('archive')}
    <section class="read-head">
      <div class="meta">
        <span>${a.date || ''}</span>
        <span class="dot"></span>
        <span class="pill">${TOPICS[a.topic]?.zh || a.topic}</span>
        <span class="dot"></span>
        <span>蒸馏小余</span>
      </div>
      <h1>${esc(a.title)}</h1>
      ${a.summary ? `<p class="summary">${esc(a.summary)}</p>` : ''}
    </section>
    <article class="prose">${a.html || ''}</article>
    ${
      related.length
        ? `<section class="read-tail">
            <p class="k">Related · 相关阅读</p>
            ${related
              .map(
                (r) => `
              <a class="entry" href="/article/${r.slug}" data-link>
                <span class="idx"></span>
                <span class="date">${r.date || ''}</span>
                <span class="ttl">${esc(r.title)}</span>
                <span class="pill">${TOPICS[r.topic]?.zh || r.topic}</span>
              </a>`,
              )
              .join('')}
          </section>`
        : ''
    }
    <section class="read-tail"><a class="read-back" href="/articles" data-link>回到文章存档</a></section>
    ${signoff()}
  `
  window.scrollTo(0, 0)
}

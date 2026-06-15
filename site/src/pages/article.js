// site/src/pages/article.js —— 文章详情：站内全文 + 配图 + 相关文章（无微信外链）
import './../styles/article.css'
import { getArticles } from '../data.js'
import { navigate } from '../router.js'

export async function renderArticle(app, ctx) {
  const slug = ctx.params.slug
  const articles = await getArticles()
  const a = articles[slug]
  if (!a) {
    app.innerHTML = `<div class="article-wrap"><p>文章不存在。</p>
      <a href="/articles" data-link>← 返回列表</a></div>`
    return
  }
  const related = (a.related || []).map((s) => ({ slug: s, ...articles[s] })).filter((x) => x.title)
  app.innerHTML = `
    <div class="article-wrap">
      <div class="nav"><a href="/" data-link>← 星图</a>
        <a href="/articles" data-link>全部文章</a></div>
      ${a.cover ? `<img class="hero" src="${a.cover}" alt="">` : ''}
      <h1>${a.title}</h1>
      <div class="meta">${a.author || '蒸馏小余'} · ${a.date || ''}</div>
      <article class="prose">${a.html}</article>
      ${related.length ? `<section class="related"><h3>相关文章</h3>
        <div class="rel-grid">${related.map((r) => `
          <a class="rel" data-link href="/article/${r.slug}">
            <span>${r.title}</span><small>${r.summary || ''}</small></a>`).join('')}</div>
      </section>` : ''}
    </div>`
  scrollTo(0, 0)
}

// site/src/pages/home.js —— 简历型首页:Hero / 研究方向 / 写作 / 关于 / 签名页脚
import { getArticles } from '../data.js'
import { TOPICS } from '../topics.js'
import { siteHead, signoff, esc } from '../ui.js'

export async function renderHome(app) {
  const articles = await getArticles()
  const dated = articles.filter((a) => a.date)
  const total = dated.length
  const firstDate = dated[dated.length - 1]?.date?.slice(0, 7) || ''
  const lastDate = dated[0]?.date || ''

  // 每个方向的实际文章数
  const counts = {}
  for (const a of articles) if (a.topic) counts[a.topic] = (counts[a.topic] || 0) + 1
  const topics = Object.entries(TOPICS)
    .map(([id, t]) => ({ id, ...t, n: counts[id] || 0 }))
    .filter((t) => t.n > 0)

  const recent = dated.slice(0, 8)

  app.innerHTML = `
    ${siteHead('home')}
    <section class="hero">
      <p class="kicker">AI Agent Engineering · Writing / Research / Building</p>
      <h1>蒸馏小余<br /><span class="latin">AI Agent</span> 工程化<br />写作者</h1>
      <p class="lede">
        我把散落在论文、源码与一线访谈里的 Agent 知识,<em>蒸馏</em>成可执行的工程判断——
        从 Agent 运行时、上下文工程、记忆与 RAG,到 Claude Code 的真实用法。
        这个站点是我的公开档案:每一篇长文,都是一次把"看起来会了"变成"工程上成立"的记录。
      </p>
      <div class="stats">
        <div class="stat"><div class="n">${total}<sup>篇</sup></div><div class="t">深度长文</div></div>
        <div class="stat"><div class="n">${topics.length}<sup>个</sup></div><div class="t">研究方向</div></div>
        <div class="stat"><div class="n">${firstDate.replace('-', '.')}<sup>始</sup></div><div class="t">持续写作</div></div>
        <div class="stat"><div class="n">${lastDate.slice(5).replace('-', '.')}<sup>新</sup></div><div class="t">最近更新</div></div>
      </div>
    </section>

    <section class="sec" id="focus">
      <div class="sec-label"><div class="sec-label-inner">
        <span class="no">01</span>
        <span class="zh">研究方向</span>
        <span class="en">Focus Areas</span>
      </div></div>
      <div class="sec-body">
        ${topics
          .map(
            (t, i) => `
          <a class="topic-row" href="/articles?topic=${t.id}" data-link>
            <span class="idx">${String(i + 1).padStart(2, '0')}</span>
            <span class="name"><span class="zh">${t.zh}</span><span class="en">${t.en}</span></span>
            <span class="desc">${t.desc}</span>
            <span class="count">${t.n} 篇</span>
          </a>`,
          )
          .join('')}
      </div>
    </section>

    <section class="sec" id="writing">
      <div class="sec-label"><div class="sec-label-inner">
        <span class="no">02</span>
        <span class="zh">近期写作</span>
        <span class="en">Selected Writing</span>
      </div></div>
      <div class="sec-body">
        ${recent
          .map(
            (a, i) => `
          <a class="entry" href="/article/${a.slug}" data-link>
            <span class="idx">${String(total - i).padStart(3, '0')}</span>
            <span class="date">${a.date}</span>
            <span class="ttl">${esc(a.title)}</span>
            <span class="pill">${TOPICS[a.topic]?.zh || a.topic}</span>
          </a>`,
          )
          .join('')}
        <a class="sec-more" href="/articles" data-link>全部 ${total} 篇文章存档</a>
      </div>
    </section>

    <section class="sec" id="about">
      <div class="sec-label"><div class="sec-label-inner">
        <span class="no">03</span>
        <span class="zh">关于我</span>
        <span class="en">About</span>
      </div></div>
      <div class="sec-body">
        <div class="about-grid">
          <div>
            <p>
              我相信一件事:Agent 的瓶颈不在模型,而在工程。模型每隔几个月就换一代,
              但上下文怎么组织、记忆怎么写入召回、工具怎么约束、任务怎么验收——
              这些决定 Agent 能不能在真实工作里站住。
            </p>
            <p>
              所以我系统性地追踪这个领域的一线实践:读论文、读源码、读访谈,
              然后写成不掺水的长文。这个站点背后的知识库本身也是一件作品:
              一个 Obsidian vault,用 manifest 驱动、构建期生成数据的静态站点。
            </p>
          </div>
          <ul class="about-facts">
            <li><span class="k">笔名</span><span class="v">蒸馏小余</span></li>
            <li><span class="k">领域</span><span class="v">AI Agent 工程化</span></li>
            <li><span class="k">阵地</span><span class="v">微信公众号「蒸馏小余」</span></li>
            <li><span class="k">方法</span><span class="v">论文 / 源码 / 访谈 → 工程判断</span></li>
          </ul>
        </div>
      </div>
    </section>

    ${signoff()}
  `
}

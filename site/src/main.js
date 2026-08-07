// site/src/main.js —— 入口 + 路由注册
import './styles/base.css'
import './styles/home.css'
import './styles/list.css'
import './styles/article.css'
import { route, render } from './router.js'
import { renderHome } from './pages/home.js'
import { renderList } from './pages/list.js'
import { renderArticle } from './pages/article.js'

const app = document.getElementById('app')
route(/^\/$/, async () => {
  document.title = '蒸馏小余 · AI Agent 工程化写作者'
  await renderHome(app)
  if (location.hash) {
    requestAnimationFrame(() => document.querySelector(location.hash)?.scrollIntoView({ behavior: 'smooth' }))
  } else {
    window.scrollTo(0, 0)
  }
})
route(/^\/articles$/, async (ctx) => {
  document.title = '文章存档 · 蒸馏小余'
  await renderList(app, ctx)
  window.scrollTo(0, 0)
})
route(/^\/article\/(?<slug>[^/]+)$/, (ctx) => renderArticle(app, ctx))
render()

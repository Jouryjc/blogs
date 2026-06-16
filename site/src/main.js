// site/src/main.js —— 入口 + 路由注册
import './styles/base.css'
import { route, render } from './router.js'
import { renderHome } from './pages/home.js'
import { renderList } from './pages/list.js'
import { renderArticle } from './pages/article.js'

const app = document.getElementById('app')
route(/^\/$/, () => renderHome(app))
route(/^\/articles$/, (ctx) => renderList(app, ctx))
route(/^\/article\/(?<slug>[^/]+)$/, (ctx) => renderArticle(app, ctx))
render()

// site/src/pages/home.js —— 首页：3D 图谱 + HUD（品牌 / 图例 / 搜索 / 入口）
import './../styles/home.css'
import { getGraph } from '../data.js'
import { createGraph } from '../graph/graph3d.js'
import { navigate } from '../router.js'

let current
export async function renderHome(app) {
  if (current) { clearInterval(current.__timer); current.pauseAnimation?.(); current._destructor?.(); current = null }
  const data = await getGraph()
  app.innerHTML = `
    <div class="home">
      <div class="graph"></div>
      <div class="hud hud-brand">
        <h1>蒸馏小余 · AI Agent 工程化知识库</h1>
        <p>把论文 / 推文 / 笔记，蒸馏成一张可漫游的知识星图</p>
      </div>
      <div class="hud hud-search"><input placeholder="搜索文章 / 主题…" /></div>
      <div class="hud hud-legend"></div>
      <button class="hud hud-enter">进入文章列表 →</button>
    </div>`
  const el = app.querySelector('.graph')
  let lastTopic
  const Graph = createGraph(el, data, {
    onTopicFocus(n) {
      focusNode(Graph, n)
      if (lastTopic === n.id) navigate('/articles?topic=' + n.id)
      lastTopic = n.id
    },
  })
  current = Graph

  // 图例：12 主题色点，点击聚焦相机
  const legend = app.querySelector('.hud-legend')
  legend.innerHTML = data.nodes.filter((n) => n.type === 'topic')
    .map((n) => `<button data-id="${n.id}"><span class="dot" style="color:${n.color};background:${n.color}"></span>${n.title}</button>`)
    .join('')
  legend.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return
    const n = data.nodes.find((x) => x.id === b.dataset.id); focusNode(Graph, n)
  })

  // 搜索：按标题实时聚焦第一个匹配
  app.querySelector('.hud-search input').addEventListener('input', (e) => {
    const q = e.target.value.trim(); if (!q) return
    const n = data.nodes.find((x) => x.title && x.title.includes(q)); if (n) focusNode(Graph, n)
  })

  app.querySelector('.hud-enter').addEventListener('click', () => navigate('/articles'))
}

function focusNode(Graph, n) {
  if (!n || n.x == null) return
  const d = 120
  const r = 1 + d / Math.hypot(n.x, n.y, n.z || 1)
  Graph.cameraPosition({ x: n.x * r, y: n.y * r, z: (n.z || 1) * r }, { x: n.x, y: n.y, z: n.z }, 1000)
}

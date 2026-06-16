// site/src/graph/graph3d.js —— 3d-force-graph 星系首页 + UnrealBloom 辉光
import ForceGraph3D from '3d-force-graph'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js'
import { navigate } from '../router.js'

export function createGraph(el, data, { onTopicFocus } = {}) {
  const isMobile = matchMedia('(max-width:768px)').matches
  const Graph = ForceGraph3D()(el)
    .backgroundColor('#05060f')
    .graphData(data)
    .nodeLabel((n) => (n.type === 'topic'
      ? `<b>${n.title}</b>`
      : `${n.title}${n.summary ? `<br><i>${n.summary}</i>` : ''}`))
    .nodeVal((n) => n.val)
    .nodeColor((n) => n.color)
    .nodeOpacity(0.92)
    .nodeResolution(isMobile ? 8 : 16)
    .linkColor((l) => (l.kind === 'moc' ? 'rgba(150,180,255,0.55)' : 'rgba(120,130,170,0.25)'))
    .linkWidth((l) => (l.kind === 'moc' ? 0.6 : 0.25))
    .linkDirectionalParticles(isMobile ? 0 : 1)
    .onNodeClick((n) => {
      if (n.type === 'article') navigate(`/article/${n.slug}`)
      else onTopicFocus?.(n)
    })

  if (!isMobile) {
    // three r152+ 的 EffectComposer 在线性色彩空间渲染，bloom 后必须接 OutputPass
    // 做 sRGB/色调映射输出，否则整屏黑
    const composer = Graph.postProcessingComposer()
    const bloom = new UnrealBloomPass()
    bloom.strength = 1.2
    bloom.radius = 0.6
    bloom.threshold = 0.15
    composer.addPass(bloom)
    composer.addPass(new OutputPass())
  }

  // 缓慢自转；首页被路由替换（el 脱离 DOM）后自动停转并暂停动画，避免泄漏
  let angle = 0
  const dist = 320
  Graph.cameraPosition({ z: dist })
  const timer = setInterval(() => {
    if (!el.isConnected) {
      clearInterval(timer)
      Graph.pauseAnimation?.()
      return
    }
    if (Graph.__paused) return
    angle += Math.PI / 1500
    Graph.cameraPosition({ x: dist * Math.sin(angle), z: dist * Math.cos(angle) })
  }, 30)
  el.addEventListener('mousedown', () => { Graph.__paused = true })
  Graph.__timer = timer
  return Graph
}

// site/src/graph/graph3d.js —— 3d-force-graph 星系首页 + 柔和 UnrealBloom + 主题常显标签
import ForceGraph3D from '3d-force-graph'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js'
import { CSS2DRenderer, CSS2DObject } from 'three/examples/jsm/renderers/CSS2DRenderer.js'
import { navigate } from '../router.js'

export function createGraph(el, data, { onTopicFocus } = {}) {
  const isMobile = matchMedia('(max-width:768px)').matches

  // CSS2D 渲染器：主题标签用 HTML 叠层渲染，不进 WebGL，故不受 bloom 影响、永远清晰
  const labelRenderer = new CSS2DRenderer()
  labelRenderer.domElement.style.pointerEvents = 'none' // 不拦截图谱的旋转/点击

  const Graph = ForceGraph3D({ extraRenderers: [labelRenderer] })(el)
    .backgroundColor('#05060f')
    .graphData(data)
    .nodeLabel((n) => (n.type === 'topic'
      ? `<b>${n.title}</b>`
      : `${n.title}${n.summary ? `<br><i>${n.summary}</i>` : ''}`))
    .nodeVal((n) => n.val)
    .nodeColor((n) => n.color)
    .nodeOpacity(0.95)
    .nodeResolution(isMobile ? 8 : 16)
    // 主题节点叠加常显标签；文章节点不加（避免 16 条长标题糊屏），仍有 hover 提示
    .nodeThreeObjectExtend(true)
    .nodeThreeObject((n) => {
      if (n.type !== 'topic') return null
      const div = document.createElement('div')
      div.className = 'graph-label'
      div.textContent = n.title
      const obj = new CSS2DObject(div)
      obj.position.set(0, Math.cbrt(n.val) * 4 + 6, 0) // 浮在球体上方
      return obj
    })
    .linkColor((l) => (l.kind === 'moc' ? 'rgba(150,180,255,0.45)' : 'rgba(120,130,170,0.2)'))
    .linkWidth((l) => (l.kind === 'moc' ? 0.6 : 0.25))
    .linkDirectionalParticles(isMobile ? 0 : 1)
    .onNodeClick((n) => {
      if (n.type === 'article') navigate(`/article/${n.slug}`)
      else onTopicFocus?.(n)
    })

  if (!isMobile) {
    // three r152+ 的 EffectComposer 在线性色彩空间渲染，bloom 后必须接 OutputPass 做 sRGB 输出。
    // 强度调低、阈值调高：只给较亮处一层淡光晕，避免球体过曝成白色、丢失颜色与轮廓。
    const composer = Graph.postProcessingComposer()
    const bloom = new UnrealBloomPass()
    bloom.strength = 0.45
    bloom.radius = 0.4
    bloom.threshold = 0.35
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

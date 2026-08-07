// site/src/ui.js —— 共享 UI 片段:顶部导航、签名页脚、转义
export function esc(s = '') {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
}

export function siteHead(active = '') {
  const item = (href, label, key, hot = false) =>
    `<a href="${href}" data-link class="${active === key ? 'hot' : hot ? 'hot' : ''}">${label}</a>`
  return `
  <header class="site-head">
    <a class="brand" href="/" data-link>蒸馏小余</a>
    <nav>
      ${item('/#focus', '研究方向', 'focus')}
      ${item('/#writing', '写作', 'writing')}
      ${item('/#about', '关于', 'about')}
      ${item('/articles', '文章存档', 'archive', active !== 'home' && active !== 'archive')}
    </nav>
  </header>`
}

export function signoff() {
  return `
  <footer class="signoff">
    <div class="signoff-inner">
      <p class="big">模型会换代,<br /><em>工程判断</em>会留下来。</p>
      <div class="row">
        <div><span class="k">公众号</span><span class="v">蒸馏小余</span></div>
        <div><span class="k">写作主题</span><span class="v">AI Agent 工程化</span></div>
        <div><span class="k">入口</span><a class="v" href="/articles" data-link>全部文章存档</a></div>
      </div>
      <p class="fine">© 蒸馏小余 · Built with an Obsidian vault, a manifest, and a static pipeline.</p>
    </div>
  </footer>`
}

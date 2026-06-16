// site/src/router.js —— 极简 history 路由
const routes = []
export function route(pattern, handler) { routes.push({ pattern, handler }) }
export function navigate(to) { history.pushState({}, '', to); render() }
export async function render() {
  const url = new URL(location.href)
  const pathn = url.pathname
  for (const { pattern, handler } of routes) {
    const m = pattern.exec(pathn)
    if (m) { await handler({ params: m.groups || {}, query: url.searchParams }); return }
  }
  routes[0]?.handler({ params: {}, query: url.searchParams })
}
window.addEventListener('popstate', render)
document.addEventListener('click', (e) => {
  const a = e.target.closest('a[data-link]')
  if (a) { e.preventDefault(); navigate(a.getAttribute('href')) }
})

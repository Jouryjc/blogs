// site/src/data.js —— 运行时加载并缓存构建产物 JSON
let _articles, _topics
export async function getArticles() {
  if (!_articles) {
    const map = await (await fetch('/data/articles.json')).json()
    // 转成按日期倒序的数组,补上 slug
    _articles = Object.entries(map)
      .map(([slug, a]) => ({ slug, ...a }))
      .sort((a, b) => (b.date || '').localeCompare(a.date || ''))
  }
  return _articles
}
export async function getTopics() {
  if (!_topics) {
    const g = await (await fetch('/data/graph.json')).json()
    _topics = g.nodes.filter((n) => n.type === 'topic')
  }
  return _topics
}
export function topicName(id) {
  return id
}

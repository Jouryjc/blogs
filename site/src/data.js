// site/src/data.js —— 运行时加载并缓存构建产物 JSON
let _graph, _articles
export async function getGraph() { return (_graph ??= await (await fetch('/data/graph.json')).json()) }
export async function getArticles() { return (_articles ??= await (await fetch('/data/articles.json')).json()) }

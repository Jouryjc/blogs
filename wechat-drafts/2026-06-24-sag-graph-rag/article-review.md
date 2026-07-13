# SAG 公众号稿发布前 Review

## 总评

这篇适合作为「5 分钟蒸馏」类型发布。入口从 RAG 多跳检索的真实痛点切入，主线不是项目摘要，而是围绕「普通向量 RAG、重型知识图谱、SAG 轻结构」三者的工程取舍展开。基本使用、检索模式、MCP 接入和适用边界都覆盖到了。

## 指标

```json
{
  "chinese_chars_excluding_code": 2681,
  "paragraph_count": 56,
  "heading_count_h2_to_h4": 7,
  "link_count": 16,
  "image_count": 4,
  "code_block_count": 5,
  "cta_keyword_hits": ["关键词", "收藏"],
  "ai_smell_hits": [],
  "warnings": []
}
```

## 评分

综合评分：90 / 100。

- 定位匹配：10 / 10，SAG 与 RAG / Agent 检索工作流高度相关。
- 标题转化：14 / 15，痛点明确，技术名词有解释路径。
- 第一屏：14 / 15，能快速兑现「多跳检索越塞越乱」的标题承诺。
- 结构密度：14 / 15，原理、使用、MCP、边界完整。
- 可复用资产：14 / 15，提供了上手命令、MCP 配置、适用判断。
- 作者判断：9 / 10，有适合谁、不适合谁、最大坑。
- 微信可读性：8 / 10，技术信息较密，但 4 张图能分担解释压力。
- 增长机制：7 / 10，结尾已补收藏清单，后续可继续拆「自己怎么测 Recall」。

## 已修改

- 将 `核心思路` 改为更自然的 `做法可以压成一句话`。
- 将 `本质是"一跳"检索` 改为 `更像"一跳"检索`。
- 将小标题 `核心原理` 改为 `原理拆开看`。
- 增加结尾三项判断清单，强化收藏动机。

## 发布建议

使用 `article-anti-ai.md` 作为最终发布稿，配 1 张封面图和 4 张正文信息图。发布前继续用 `wechat-api.ts --dry-run` 检查 Markdown 渲染、图片上传占位和主题色。

## 二次去 AI 味复检（2026-06-25）

按新的默认流程，对 `article-anti-ai.md` 做了二次去 AI 味处理：把几处泛泛过渡句改成更具体的作者判断句，保留 `article.md` 作为初稿溯源。

复检指标：

```json
{
  "chinese_chars_excluding_code": 2727,
  "paragraph_count": 56,
  "heading_count_h2_to_h4": 7,
  "link_count": 16,
  "image_count": 4,
  "code_block_count": 5,
  "cta_keyword_hits": ["关键词", "收藏"],
  "ai_smell_hits": [],
  "warnings": []
}
```

人工风险词扫查未命中高频模板表达。dry-run 通过：标题、作者、摘要正常，正文占位图 4 张。已用原 `media_id` 更新公众号草稿：

```json
{
  "success": true,
  "media_id": "GHixSPLvYVluGTAOLz6Fea9aKmBZbfDhCe6NfnuqDegTpOsEDK1tyEhJEpzUXiUv",
  "updated": true,
  "index": 0
}
```

## 标题句式优化（2026-06-25）

用户要求不要把 `为什么？xxx` 固化成默认标题模板。结合公众号标题资料，当前标题策略改为：先按文章内容判断标题机制，再选句式；技术文优先把读者痛点、反差、结果或可执行对象放到前半句，问句只在问题本身确实是读者入口时使用。

这篇 SAG 的标题从：

```text
RAG 多跳检索为什么越塞越乱？SAG 用「事项+实体」重做了一遍
```

改为：

```text
RAG 别再硬塞 chunk：SAG 用「事项+实体」接证据链
```

选择原因：

- 不再依赖固定问句，而是用“别再硬塞 chunk”直接命中 RAG 多跳场景里的错误动作。
- “接证据链”比“重做了一遍”更贴近 SAG 的 event / entity 多跳检索机制。
- 前半句给读者体感问题，后半句给方法和技术对象，和文章第一屏承诺一致。

本地复检指标：正文图片 4 张，代码块 5 个，`ai_smell_hits: []`。发布前 dry-run 通过，已用原 `media_id` 更新公众号草稿标题：

```json
{
  "success": true,
  "media_id": "GHixSPLvYVluGTAOLz6Fea9aKmBZbfDhCe6NfnuqDegTpOsEDK1tyEhJEpzUXiUv",
  "title": "RAG 别再硬塞 chunk：SAG 用「事项+实体」接证据链",
  "articleType": "news",
  "updated": true,
  "index": 0
}
```

## MCP Server 配图重生成（2026-06-25）

用户反馈「给 Agent 用：每个项目自带一个 MCP Server」章节配图不对。原图偏向“四步上手流程”，与本节主旨不匹配。已重写 prompt，将图改成项目级 MCP Server 架构图：

- 左侧：`SAG 项目`，标出 `文档库 / event + entity / sourceId`
- 中间：`复制 mcpServers` 配置卡，保留 `"sag"`、`"npm run mcp"`、`SAG_MCP_SOURCE_ID`
- 右侧：`外部 Agent`，强调不用再传 `projectId`
- 底部：四个 MCP 工具 `sag_ingest_document` / `sag_search` / `sag_explain_search` / `sag_get_event`

本地文件已替换：

- 新图源文件：`illustrations/sag/sag-quickstart-redo.png`
- 文章引用文件：`imgs/sag-quickstart.png`
- 尺寸：`1672x941`

发布前 dry-run 已通过：标题、作者、摘要正常，正文占位图 4 张。已用原 `media_id` 更新公众号草稿成功：

```json
{
  "success": true,
  "media_id": "GHixSPLvYVluGTAOLz6Fea9aKmBZbfDhCe6NfnuqDegTpOsEDK1tyEhJEpzUXiUv",
  "updated": true,
  "index": 0
}
```

## 平均 Recall 配图重生成（2026-06-25）

用户反馈平均 Recall 图风格不符合正文其它配图。已重写 prompt，弱化图表海报感，改为奶油纸底、手绘卡片、轻描边的蒸馏小余知识卡风格。

本地文件已替换：

- 新图源文件：`illustrations/sag/sag-benchmark-redo.png`
- 文章引用文件：`imgs/sag-benchmark.png`
- 尺寸：`1672x941`

发布前 dry-run 已通过：标题、作者、摘要正常，正文占位图 4 张。第一次走本地代理时，微信图片上传接口连续返回 `SSL_ERROR_SYSCALL`；随后用增强重试的临时 curl 包装器继续走代理出口，已用原 `media_id` 更新公众号草稿成功。

```json
{
  "success": true,
  "media_id": "GHixSPLvYVluGTAOLz6Fea9aKmBZbfDhCe6NfnuqDegTpOsEDK1tyEhJEpzUXiUv",
  "updated": true,
  "index": 0
}
```

# LMCache / KV Cache 公众号文章设计

## 目标

围绕 Akshay Pachaar 的 X Article《Your KV Caching Is Broken》，为“蒸馏小余”写一篇约 2,500–3,000 个中文字符的「5 分钟蒸馏」，并完成微信公众号草稿发布。

文章不做原文逐段翻译，也不把 LMCache 写成通用的“14 倍加速器”。主线是解释：Agent 成本高，不只是 token 单价问题；大量重复上下文在每一步重新 Prefill。Prefix Cache 只能复用稳定前缀，LMCache 则尝试把 KV Cache 管理从推理引擎中拆出，变成可独立扩展的基础设施。

## 读者与成功标准

目标读者是正在自托管大模型、搭建 RAG 或运行 Agent 工作流的开发者和平台团队。

成功标准：

- 不预设读者理解 KV Cache，第一屏即交代重复上下文的工程后果。
- 分清 Prompt Caching / Prefix Caching、KV Cache 卸载、LMCache 解耦和 CacheBlend 多文档复用的不同问题。
- 对性能数字保留测试条件，不把单一 benchmark 写成普遍承诺。
- 给出可保存的采用判断清单，帮助读者决定是否需要引入独立 KV Cache 层。
- 完成去 AI 味审稿、430px 移动端预览、微信 API dry-run、真实发布和 `draft/get` 远端回读。

## 事实边界

一手材料优先级如下：

1. LMCache 官方仓库、官方文档和官方 benchmark 说明。
2. CacheBlend 论文与 EuroSys 公开材料。
3. vLLM、SGLang、TensorRT-LLM 等集成项目的官方文档。
4. Anthropic 等模型服务商对 Prompt Caching 的官方说明。

原 X Article 是叙事主干，不是唯一事实依据。下列内容必须逐项复核：

- “62% 请求内容是重复内容”的研究对象和测量口径。
- “14x TTFT”“4x decoding”和启动时间数据的模型、GPU、并发数和对照组。
- “1% 命中率即回本”与“三年节省 2,900 万美元”的假设。
- Uber 预算、Gartner 项目取消比例、单 GPU 每日 KV Cache 产生量等引人注目的数字。

无法从一手材料确认的说法不写入成稿；官方 benchmark 只按其测试条件表述。

## 标题与第一屏

写作前生成五个至少覆盖四种句式的标题候选。推荐方向是：

> Agent 上下文越跑越贵，先把 KV Cache 从推理进程里拆出来

第一屏用 Agent Loop 的具体场景开篇：系统提示词、工具定义、文档和对话历史在每一步再次进入 Prefill。立即给出判断：如果重复前缀稳定，先做 Prompt Caching；如果有跨请求、跨 GPU、多存储层和多文档复用需求，才需要评估 LMCache 这类独立缓存层。

## 叙事结构

1. **Agent 在为重复上下文付费**：用一次 Agent 执行里的多轮模型调用解释 Prefill 重复。
2. **KV Cache 缓存的到底是什么**：用“读完教材后保留笔记”的类比解释 Key / Value 状态复用，同时避免把注意力复杂度简化成不准确的定律。
3. **Prefix Cache 为何不够**：拆解稳定前缀、文档顺序、多文档组合与对话增长的边界。
4. **进程内缓存的性能税**：说明缓存 I/O 和 GPU 推理争用资源的场景，不做“一定串行”的过度概括。
5. **LMCache 的解耦架构**：解释独立进程、多级存储、跨 GPU 复用、并行加载和故障降级。
6. **CacheBlend 处理多文档组合**：说明独立缓存文档之间缺失交叉关系，以及选择性重算的思路。
7. **是否引入 LMCache 的判断清单**：以缓存命中率、TTFT、跨请求重复度、多 GPU 规模、存储成本、降级路径和运维复杂度作为决策条件。

## 作者判断

成稿至少明确表达三个工程判断：

- 有稳定系统提示词和工具定义时，先把服务商 Prompt Caching 用对，不需要为了“架构先进”提前引入 LMCache。
- 对长上下文 RAG、重复文档、多 GPU 推理和明显 TTFT 压力，KV Cache 已经是需要单独管理的数据资产。
- 是否采用 LMCache 要看端到端 p50/p95 TTFT、命中率、存储与网络开销，不看脱离自身 workload 的单一倍数。

## 配图设计

生成一张 2.35:1 封面和三张 16:9 正文图，统一使用蒸馏小余奶油纸底知识卡风格：深海军蓝手绘线、低饱和便签色块、经典蓝 `#0F4C81` 强调、简短中文标签。

1. **封面**：`Agent 上下文越跑越贵`，中央是推理引擎与独立 KV Cache 层，标题和主视觉位于居中 1:1 安全区。
2. **重复 Prefill 流程图**：Agent 每一步重发系统提示词、工具、文档和历史，对比命中缓存后只计算新增部分。
3. **Prefix Cache 边界图**：稳定前缀可复用，文档顺序变化、多文档组合和历史增长会造成失配。
4. **LMCache 多级缓存图**：推理引擎与缓存管理解耦，后者并行管理 GPU、CPU RAM、SSD 和远程存储。

每张图只表达一个结论，不使用手机端字号过小的复杂表格。原 X Article 图片作为证据与构图参考，正文使用重新绘制的中文图。

## 产物布局

```text
post-to-wechat/2026-08-21/lmcache-kv-cache/
├── lmcache-kv-cache.md
├── article-review.md
├── article-anti-ai.md
├── title-candidates.md
├── research-notes.md
├── doocs-wechat-rendered.html
├── mobile-preview-430px.png
├── wechat-dry-run.json
├── publish-result.json
├── draft-readback.json
├── imgs/
│   ├── article-cover.png
│   ├── 01-agent-prefill.png
│   ├── 02-prefix-cache-boundary.png
│   └── 03-lmcache-architecture.png
├── illustrations/lmcache-kv-cache/
└── cover-image/lmcache-kv-cache/
```

X 原始素材由 X 转 Markdown 工具存入 `x-to-markdown/akshay_pachaar/2074502882812952666/`，并自动下载媒体。主文保留；审稿报告和发布稿作为相邻文件，不覆盖原始成文。

## 执行与验收

1. 使用已授权的 X 转 Markdown 工具下载原文与媒体。
2. 复核官方仓库、文档、论文和 Prompt Caching 官方说明，把证据写入 `research-notes.md`。
3. 生成五个标题候选后完成初稿。
4. 运行 `xiaoyu-wechat-article-reviewer` 和 `article_metrics.py`，生成 `article-review.md` 与 `article-anti-ai.md`。
5. 仅使用 `codex-image-gen` 生成三张正文图和封面，检查尺寸、中文和居中 1:1 裁剪区。
6. 生成 430px 预览，确认无图片溢出、断图、过小标签、列表标记错乱或紫色主色残留。
7. 以 `article-anti-ai.md` 执行微信 API dry-run，使用 `grace` 主题和 `#0F4C81` 主色，确认封面与四张本地图片均被识别。
8. 首次发布时创建新草稿，保存返回的 `media_id`。
9. 调用 `draft/get` 回读同一 `media_id`，确认单篇文章、标题、封面和正文图片数量后才宣布交付完成。
10. 按知识库规则为主文增加 `type/article`、`topic/agent-runtime`、`topic/context-engineering`、`platform/wechat`，更新 manifest、相关 wiki 与 `wiki/INDEX.md`，运行 inventory 和 link check。

## 失败处理

- X 转换器失败时，保留已获取的只读源内容，但不把未完整落盘称为原文归档完成。
- 无法验证的数字直接删除，不使用二手转述填补证据缺口。
- 图片生成失败时，保留提示词和完整成稿，不使用占位图冒充交付。
- 微信 API 因 IP 白名单或账号配置失败时，保留 dry-run 与失败证据，明确标记“API 受阻”，不声称已进入草稿箱。
- 未完成 `draft/get` 回读时，即使上传日志成功，也不宣布发布闭环完成。

# AgentJudgeBench 工程决策版文章与公众号草稿设计

## 目标

以 arXiv:2608.26623v1《AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling》为唯一论文主证据，写一篇面向 Agent 工程师、评测平台开发者和技术负责人的蒸馏小余文章，并完成公众号草稿发布与远端回读。

文章不做逐节翻译，也不把榜单第一当作结论。主线是：当 LLM 被用来给 Agent 的工具调用判卷时，任务难度、参考轨迹和评分提示会共同改变裁判可靠性；工程上不能把 LLM Judge 当成唯一真相层。

## 文章定位

- 类型：`5 分钟蒸馏 + 工程清单`
- 目标长度：3,500–4,200 个中文字符
- 写作风格：蒸馏小余 2.0，先下判断，再解释机制与边界
- 可保存资产：一份“Agent 评测四层防线”清单
- 推荐标题方向：`给 Agent 判卷，AI 裁判先撞上了结构性天花板`

## 核心叙事

1. 用反常识结果开场：给参考轨迹并不总能提升 Judge 与程序评分器的一致度，Gemini-2.5-Pro 与论文内部命名的 GPT-5.4 分别出现 -3.9pp 与 -1.5pp 的 GT lift。
2. 解释论文测的不是 Agent 能力，而是 Judge 与程序评分器在四项结构指标上的一致程度。
3. 交代基准规模与方法：3,808 条基础记录、11,424 个三档难度问题、5 个 Generator、6 个主 Judge、with-GT / without-GT 成对条件。
4. 展开主要发现：难度上升时 alignment 单调下降；without-GT 下降约快 1.5 倍；hard/no-GT 下同一 Generator 面前的 Judge 差距被压缩；更高的 Judge 间一致不代表更正确。
5. 解释三类配置杠杆：CoT 和温度影响很小，结构化 rubric 在一组实验中提升 4.8–6.5pp，但在第二组 hard 任务中反转为 -0.8pp。
6. 给出小余的工程判断：能确定性验证的结构问题交给程序，语义等价与意图覆盖交给 LLM，争议样本做差异复核和人工抽检。

## 事实边界

- `alignment` 是 LLM Judge 与论文程序评分器的一致度，不是现实任务成功率或真实准确率。
- 3,808 是唯一基础记录数；三档改写后的数据集为 11,424 行。
- 321,648 是 paired with-GT/without-GT 评测单元；若把两个条件分别计数是 643,296 个 verdict。
- 77%–82% 是论文对 hard/no-GT 聚集现象的概括，不写成每个 Generator、Judge、指标都严格落入该区间。
- Ground Truth 是参考工具调用轨迹，不保证是唯一正确轨迹。
- 论文程序评分器只看工具集合、参数 key、单条参考顺序和覆盖率，没有执行真实工具，也不完整理解语义等价。
- 论文数据是合成、单轮、无状态的工具调用任务，不直接代表线上多轮 Agent。
- easy→medium 的难度校准较弱；主要难度证据落在 medium→hard。
- 论文的 `GPT-5.4` 是作者对 2026 年 4 月 Azure preview 快照的内部命名，不写成可公开复现的正式版本。
- “四层评测防线”“先盲审再看 GT”等内容明确标为作者判断或待验证建议。

## 配图方案

统一使用蒸馏小余奶油纸底知识卡视觉，生成一张 2.35:1 封面和四张 16:9 正文图：

1. 基准流水线：基础记录 → 三档改写 → Generator → 程序评分器与 LLM Judge → 四项 alignment。
2. 难度退化：with-GT / without-GT 两条曲线，突出 without-GT 下降约快 1.5 倍；据论文 Figure 8 重绘。
3. 参考答案锚定：参考轨迹与功能等价替代轨迹对照，保留 -1.5pp 与 -3.9pp 的条件说明。
4. 配置杠杆：温度、CoT、结构化 rubric 三张卡，并保留 rubric 不稳定泛化的限定。

封面标题、中心裁判图形与“任务难度 / 参考轨迹 / 评分规则”三个标签均放进居中 1:1 安全区。所有重绘图在正文图注中标注 `据 Verma 等《AgentJudgeBench》重绘，CC BY 4.0`。

## 产物布局

```text
post-to-wechat/2026-08-30/agentjudgebench-llm-judge/
├── agentjudgebench-llm-judge.md
├── article-review.md
├── article-anti-ai.md
├── article-metrics.json
├── title-candidates.md
├── gen-image.md
├── source/
│   ├── paper-source.md
│   └── research-notes.md
├── illustrations/agentjudgebench-llm-judge/
│   ├── outline.md
│   ├── prompts/
│   └── 01-*.png ... 04-*.png
├── cover-image/agentjudgebench-llm-judge/cover-prompt.md
├── imgs/article-cover.png
├── doocs-wechat-rendered.html
├── mobile-preview-430.png
├── wechat-dry-run.json
├── wechat-publish.json
├── wechat-draft-readback-summary.json
└── wechat-asset-reachability.json
```

## 知识库接入

- 主文标签：`type/article`、`topic/agent-design`、`topic/agent-runtime`、`topic/agent-safety`、`platform/wechat`。
- 论文来源笔记标签：`type/source` 与相同三个 topic 标签。
- 只在 frontmatter 和 wiki 中写关联，不向公众号正文追加 Obsidian 相关阅读。
- 更新 `_kb_build/manifest.json`、`wiki/agent-design.md`、`wiki/agent-runtime.md`、`wiki/agent-safety.md` 与 `wiki/INDEX.md`。
- 不改动任何既有 raw 正文和当前未跟踪的其他文章目录。

## 发布与验收

1. 保留原稿，Reviewer 输出独立的 `article-review.md` 与 `article-anti-ai.md`。
2. `article_metrics.py` 要求 `ai_smell_hits=[]`、`warnings=[]`；如有保留项必须在审稿报告解释。
3. 图片必须真实生成、尺寸正确、中文可读；不使用占位图冒充完成。
4. 使用 Doocs `grace` 与 `#0F4C81`，最终 HTML 不含 `#92617E`。
5. 430px 预览要求 `scrollWidth == viewportWidth == 430`、断图为 0。
6. dry-run 直接传 `article-anti-ai.md`，正文图片占位数等于 4。
7. 首次发布返回 `success: true`、`updated: false` 和非空 `media_id`。
8. `draft/get` 必须回读同一 `media_id`，确认单篇文章、标题、作者、摘要、封面和四张正文图。
9. 封面与四张微信 CDN 图片均执行 GET，保存 HTTP 200 证据。

## 失败处理

- 图片生成失败时保留 prompt 和完整文章，报告具体失败图，不切换到其他图片后端。
- 微信 API 因 IP 白名单或账号配置失败时保留 dry-run 与错误证据，不把上传日志当作交付完成。
- 未完成同 `media_id` 的 `draft/get` 时，不宣布草稿已交付。
- 论文证据与作者工程判断冲突时，以论文可追溯事实为准，并在正文降低断言强度。

# AgentJudgeBench 公众号文章执行计划

## 交付目标

完成论文一手资料归档、蒸馏小余工程决策版文章、Reviewer 优化、五张知识图、移动端预览、微信 API 首次发布和同 `media_id` 远端回读。

## 执行步骤

1. **建立受控工作区**
   - 创建 `post-to-wechat/2026-08-30/agentjudgebench-llm-judge/` 的 source、illustrations、cover-image、imgs 目录。
   - 只修改本任务目录、对应 manifest/wiki 和本计划文档；避开现有未跟踪目录。

2. **归档论文证据**
   - 保存 arXiv 标题、作者、提交时间、摘要、代码与数据链接。
   - 按方法、数据规模、实验配置、主要发现、消融、人工验证、局限、工程推断整理 `research-notes.md`。
   - 对所有关键数字记录适用条件，尤其是 alignment、77%–82%、GT lift、CoT、温度和 rubric。

3. **写标题与原稿**
   - 生成五个至少覆盖四种句式的标题候选。
   - 写 3,500–4,200 中文字符的原稿。
   - 第一屏兑现“AI 裁判也会失灵”的标题承诺；中段解释机制；末段交付四层评测清单。

4. **Reviewer 与指标门禁**
   - 对原稿运行 `article_metrics.py`。
   - 写 `article-review.md`，按标题、第一屏、结构、可保存资产、作者判断和 CTA 评分。
   - 写独立的 `article-anti-ai.md`，再次跑指标并保存 `article-metrics.json`。

5. **图片规划与生成**
   - 写统一的 `gen-image.md`、插图 outline、四个插图 prompt 和封面 prompt。
   - 仅用 `codex-image-gen` 生成一张封面和四张正文图。
   - 检查文件存在、尺寸、比例、中文可读性和视觉一致性；将图片插入优化稿。

6. **知识库接入与检查**
   - 增加 manifest 条目并运行 `_kb_build/apply_tags.py`。
   - 更新 agent-design、agent-runtime、agent-safety 三个 MOC 和 wiki 首页。
   - 运行 inventory 与 link_check，只将既有基线告警与本次回归区分开。

7. **渲染与移动端 QA**
   - 对最终 Markdown 执行 WeChat dry-run，保存 JSON 和本地 HTML。
   - 生成 430px 全页预览，验证无横向溢出、断图、双黑点、列表 marker 或旧主题色。

8. **发布与远端验收**
   - 使用相同参数去掉 `--dry-run` 首次发布。
   - 保存 `wechat-publish.json` 并提取 `media_id`。
   - 通过 Bun 调用 `draft/get` 回读同一 `media_id`，核对标题、作者、摘要、封面、正文图数量和关键短语。
   - 对微信 CDN 图片执行 GET，保存可达性摘要。

9. **最终报告**
   - 报告最终标题、字符数、Reviewer 结论、图片与预览结果、发布 `media_id`、远端回读证据以及所有关键文件路径。

## 验收命令摘要

```bash
python3 .agents/skills/xiaoyu-wechat-article-reviewer/scripts/article_metrics.py <article-anti-ai.md>
python3 _kb_build/apply_tags.py
python3 _kb_build/inventory.py
python3 _kb_build/link_check.py
npx -y bun /Users/yjcjour/.agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts <article-anti-ai.md> --theme grace --color '#0F4C81' --author '蒸馏小余' --cover <article-cover.png> --dry-run
```

发布命令与 dry-run 相同，仅移除 `--dry-run`。完成标准以真实 API 返回和同 `media_id` 的 `draft/get` 为准。

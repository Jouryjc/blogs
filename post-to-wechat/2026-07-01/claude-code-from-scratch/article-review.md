# 蒸馏小余审稿记录

## 总评

这篇稿件选题契合蒸馏小余定位：它不是介绍一本普通书，而是借《Claude Code From Scratch》把 Coding Agent 的运行时骨架讲给开发者。标题有明确痛点，第一屏能兑现「不啃 50 万行源码」的承诺。

需要修的地方有三处：AI 味指标命中少量高风险词，正文没有视觉锚点，结尾 CTA 偏弱。

## 指标

```json
{
  "title": "别硬啃 50 万行源码：先读这本 Claude Code 小书",
  "chinese_chars_excluding_code": 3004,
  "paragraph_count": 89,
  "heading_count_h2_to_h4": 10,
  "link_count": 2,
  "image_count": 0,
  "code_block_count": 0,
  "cta_keyword_hits": ["关键词"],
  "ai_smell_hits": ["核心", "真正", "这件事"],
  "warnings": [
    "CTA/follow-conversion signals are weak.",
    "No images found; WeChat technical articles often need at least one visual anchor."
  ]
}
```

## 评分

| 维度 | 分数 | 说明 |
|---|---:|---|
| 定位契合 | 10/10 | Claude Code、Agent runtime、上下文工程都贴合账号。 |
| 标题转化 | 14/15 | 痛点明确，数字来自原书信息，边界清楚。 |
| 第一屏 | 14/15 | 开头直接给判断，读者收益清楚。 |
| 结构密度 | 14/15 | 6 个精髓 + 阅读路线，适合荐序。 |
| 可复用资产 | 13/15 | 有阅读路线表和检查表，优化稿需强化收藏理由。 |
| 作者判断 | 9/10 | 有「我会先读第 7 章」等取舍。 |
| 微信可读性 | 8/10 | 需要至少一张运行时骨架图。 |
| 增长机制 | 7/10 | 需要把 CTA 绑定到阅读路线表和后续拆解。 |

总分：89/100。优化后可发布。

## 具体 AI 味位置

- frontmatter summary 和正文第 36 行附近使用「核心机制」，替换为「关键机制」。
- 正文第 36 行「做的就是这件事」像总结器过渡，改成「走的就是这条路径」。
- 正文第 114、126 行有「真正」，改成更直接的工程判断。

## 优先修改

1. 在第一屏后加入一张「Claude Code 运行时骨架」正文信息图，作为视觉锚点。
2. 清理 `核心 / 真正 / 这件事` 三个命中词。
3. 结尾加「收藏阅读路线表」和「后续拆 Agent Loop / 上下文 / Skill」的关注理由。

## 改写目标

保留荐序口吻和原有结构，不改事实边界。优化稿写入 `article-anti-ai.md`，发布链路使用优化稿。

## 复核结果

优化稿 `article-anti-ai.md` 复跑指标：

```json
{
  "chinese_chars_excluding_code": 3064,
  "paragraph_count": 91,
  "heading_count_h2_to_h4": 10,
  "link_count": 3,
  "image_count": 1,
  "cta_keyword_hits": ["下一篇", "关注", "关键词", "收藏"],
  "ai_smell_hits": [],
  "warnings": []
}
```

# GSD Core 公众号配图大纲

Style: 蒸馏小余知识卡 / Deep Research Sketchnote。

## 1. Cover

- File: `imgs/article-cover.png`
- Message: Agent 长任务烂尾的解法不是更长 Prompt，而是 GSD 的阶段循环。
- Layout: 问题 -> GSD loop -> PR, title inside centered 1:1 safe crop.

## 2. Phase Loop

- File: `imgs/phase-loop.png`
- Message: GSD 把一个需求拆成 Discuss、Plan、Execute、Verify、Ship 五个可验收步骤。
- Layout: 横向流程图，五个便签卡片，每步下面一个短说明。

## 3. Planning Artifacts

- File: `imgs/planning-artifacts.png`
- Message: GSD 的记忆不在聊天里，而在 `.planning/` 文件里。
- Layout: 文件树 + 数据流箭头。

## 4. SDD Comparison

- File: `imgs/sdd-comparison.png`
- Message: GSD、Superpowers、OpenSpec 都在反对 vibe coding，但控制对象不同。
- Layout: 三列对比。

## 5. When To Use GSD

- File: `imgs/when-to-use-gsd.png`
- Message: 复杂跨文件任务用 phase loop，小改动不要上完整流程。
- Layout: 左右对比，适合用 / 不适合用。

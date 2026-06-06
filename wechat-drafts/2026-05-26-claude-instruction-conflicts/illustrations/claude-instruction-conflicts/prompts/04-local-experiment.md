Create a Chinese technical sketchnote infographic in Deep Research Sketchnote style.

Image title:
亲手复现：两个 review 到底谁生效

Core message:
用一个项目 Skill 和一个本地 Plugin Skill，就能看懂命名空间和加载时机。

Layout:
Four-step experiment flow with arrows.

Steps:
1. 项目建 Skill
   label: `.claude/skills/review`
2. 插件建 Skill
   label: `plugins/demo/skills/review`
3. 本地加载 Plugin
   label: `--plugin-dir`
4. 分别调用
   labels: `/review` and `/demo:review`

Small result card:
- `/review` 走项目入口
- `/demo:review` 走插件入口
- 冲突要看实际触发入口

Bottom takeaway strip:
不要靠猜优先级，做一个 5 分钟实验最可靠。

Visual style:
- Warm cream paper background.
- Dark navy hand-drawn outlines.
- Pastel rounded cards.
- Terminal window and folder icons.
- Mobile-readable Chinese labels.


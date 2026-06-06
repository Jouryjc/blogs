Create a Chinese technical sketchnote infographic in Deep Research Sketchnote style.

Image title:
最小 Plugin：三份东西先跑通

Core message:
一个可测试的 Claude Code Plugin，先从 manifest + Skill + 本地加载命令开始。

Layout:
File tree on the left, runtime flow on the right.

Left file tree card:
my-first-plugin/
  .claude-plugin/
    plugin.json
  skills/
    hello/
      SKILL.md

Right flow:
1. 写 plugin.json
2. 写 SKILL.md
3. `claude --plugin-dir ./my-first-plugin`
4. `/my-first-plugin:hello`

Small annotation:
- `.claude-plugin/` 只放 manifest
- `skills/` 放到插件根目录
- `$ARGUMENTS` 接收用户输入

Bottom takeaway strip:
不要先追求大而全，先让一个 Skill 真正可调用。

Visual style:
- Warm cream paper background.
- Dark navy hand-drawn outlines.
- Pastel rounded cards.
- Terminal window and folder icons.
- Mobile-readable Chinese labels.
- Avoid unreadable fake code; keep tree text large and clear.


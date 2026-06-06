# Illustration Outline

## Cover

Title: Claude 指令撞车时，谁说了算？
Core message: .claude 和 Plugin 不是一条优先级链，要按组件类型判断。
Layout: centered title + project folder and plugin toolbox feeding into a dispatcher.

## 01: 四条管线

Core message: CLAUDE.md、Skill、Agent、Hook/MCP 走不同加载通道。
Layout: layered routing diagram.

## 02: 同名不一定撞名

Core message: Plugin Skill 默认带命名空间，`/review` 和 `/plugin:review` 是两个入口。
Layout: side-by-side command cards.

## 03: 冲突判断表

Core message: Skill、Agent、MCP、Hook 的冲突规则不同。
Layout: decision table / matrix.

## 04: 本地复现实验

Core message: 用一个项目 Skill 和一个本地 Plugin Skill，亲手看命名空间和加载差异。
Layout: four-step experiment flow.


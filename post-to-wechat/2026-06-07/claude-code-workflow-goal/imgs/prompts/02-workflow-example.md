# 图片提示词：workflow 用法图

生成 1 张横版中文技术知识卡，比例 16:9，建议 1080x608。

主题：Claude Code dynamic workflow 用法。

画面结构：

- 顶部标题：workflow：把编排写成脚本
- 左侧输入区：
  - `/deep-research <question>`
  - `ultracode: audit src/routes`
- 中间流程：
  - Claude 写 JS workflow
  - 用户批准计划
  - 后台 runtime 执行
  - 多个 subagent 并行工作
  - reviewer 交叉检查
  - 汇总报告
- 右侧复用区：
  - 保存到 `.claude/workflows/`
  - 以后变成 slash command
- 底部提示：适合审计、迁移、研究、重复流程

视觉风格：

- 蒸馏小余知识卡 / Deep Research Sketchnote。
- 暖奶油纸底，深海军蓝手绘描边。
- 使用低饱和蓝色表示脚本，绿色表示 subagent，黄色表示 review，粉色表示报告。
- 中文短标签，代码片段必须清晰但不要太长。
- 不要真实品牌 logo。

输出 PNG。

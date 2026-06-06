# Claude Dynamic Workflows 研究笔记

生成日期：2026-05-31

## 主题校准

用户原文写的是 `clude workflows`。检索结果显示最匹配的新主题是 Anthropic 在 2026-05-28 发布的 Claude Code `Dynamic workflows`，官方路径包括产品博客、Claude Code 文档 `/workflows` 和 changelog。本文按 `Claude Code Dynamic workflows` 写，中文统一称为 `Claude Workflows` 或 `Dynamic workflows`。

## 标题候选

1. 推荐标题：Claude 大任务为什么烂尾？Workflows 把计划写进脚本
2. 稳妥标题：Claude Code Workflows 入门：把多代理协作写成脚本
3. 大众标题：Claude 不只会聊天了，它开始自己写工作流
4. 专家标题：从子代理到 workflow.js：Claude Code Dynamic Workflows 入门
5. 反差标题：Claude Workflows 不是新按钮，而是可执行计划

最终采用：Claude 大任务为什么烂尾？Workflows 把计划写进脚本

## 关键事实

- Anthropic 在 2026-05-28 发布 Dynamic workflows，定位是让 Claude Code 为复杂任务生成并执行一个 `workflow.js` 脚本。
- 工作流入口可以从 Claude Code 的 `/workflows` 开始，也可以在自然语言里描述任务，由 Claude 选择是否生成工作流。
- 工作流脚本不是普通顺序清单。它可以用 JavaScript 控制流表达条件分支、并行任务、循环、状态保存和错误处理。
- 官方强调脚本本身不能直接访问文件系统或 shell。它只能通过调度子代理完成实际工作，子代理再按用户授予的工具权限行动。
- 工作流的运行状态和任务成功不是一回事。官方文档提醒：如果 workflow 完成但实际任务没完成，说明 workflow 本身设计不足。
- 发布博客拿 Bun 从 Zig 迁移 Rust 的 PR 作为压力测试案例：约 75 万行代码，达到 99.8% 测试通过率。这个例子适合说明上限，不应写成所有大型迁移都能自动成功。
- Dynamic workflows 与已有能力的边界：
  - subagents 解决“把任务分给谁做”。
  - slash commands / skills 解决“如何复用一段操作说明”。
  - hooks 解决“某个事件发生时强制跑什么检查”。
  - GitHub Actions / CI 解决“在远端事件里自动触发”。
  - SDK 解决“把 Claude 嵌进自己的应用或脚本”。
  - Dynamic workflows 更偏“让 Claude 自己为一次复杂任务写编排脚本”。

## 写作主线

1. 开头从开发者痛点进：让 Claude 连续做几十个步骤，容易中途跑偏、忘记目标、检查不全。
2. 结论：Workflows 的价值不是“更自动”，而是把大任务从聊天窗口搬到可执行计划里。
3. 入门解释：`workflow.js` 是 Claude 写出来的临时编排器，负责拆任务、调子代理、保存状态、做检查。
4. 边界解释：不是 cron，不是 CI，不是万能脚本，也不是绕过权限的后门。
5. 给出上手清单：从小任务试，要求 Claude 先展示计划，检查 workflow，限制权限，使用 git worktree，最后验收输出。
6. 给出 prompt 模板和适用/不适用场景。

## 高质量资料清单

- Anthropic 官方发布博客：Introducing dynamic workflows in Claude Code  
  https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
- Claude Code 官方文档：Dynamic workflows  
  https://code.claude.com/docs/en/workflows
- Claude Code 官方 changelog  
  https://code.claude.com/docs/en/changelog
- Claude Code 官方文档索引  
  https://code.claude.com/docs/llms.txt
- Claude Code：Agents  
  https://code.claude.com/docs/en/agents
- Claude Code：Subagents  
  https://code.claude.com/docs/en/sub-agents
- Claude Code：Routines  
  https://code.claude.com/docs/en/routines
- Claude Code：Hooks guide  
  https://code.claude.com/docs/en/hooks-guide
- Claude Code：Slash commands  
  https://code.claude.com/docs/en/slash-commands
- Claude Code：Memory / CLAUDE.md  
  https://code.claude.com/docs/en/memory
- Claude Code：SDK overview  
  https://code.claude.com/docs/en/sdk
- Claude Code：Headless mode  
  https://code.claude.com/docs/en/sdk/sdk-headless
- Claude Code：TypeScript SDK  
  https://code.claude.com/docs/en/sdk/sdk-typescript
- Claude Code：Python SDK  
  https://code.claude.com/docs/en/sdk/sdk-python
- Claude Code：GitHub Actions  
  https://code.claude.com/docs/en/github-actions
- Claude Code：CI/CD  
  https://code.claude.com/docs/en/ci-cd
- Claude Code：Permissions  
  https://code.claude.com/docs/en/permissions
- Claude Code：Security  
  https://code.claude.com/docs/en/security
- Claude Code：Costs  
  https://code.claude.com/docs/en/costs
- Claude Code：Settings  
  https://code.claude.com/docs/en/settings
- Claude Code：Troubleshooting  
  https://code.claude.com/docs/en/troubleshooting
- Bun 迁移 Rust PR：Rewrite Bun in Rust  
  https://github.com/oven-sh/bun/pull/30412
- Bun 迁移说明：PORTING.md  
  https://raw.githubusercontent.com/oven-sh/bun/3157cb14b5970b69532a47800504a28ef5963e22/docs/PORTING.md

## 不采用或谨慎使用的信息

- Reddit、Hacker News、聚合资讯类文章可以帮助判断社区关注点，但正文不把它们作为事实依据。
- Bun 迁移案例使用官方博客和 GitHub PR 作为依据，避免转述二手报道里的夸张标题。
- `workflow.js` 的内部 API 还可能变化，正文只写官方文档明确展示的概念，不写未验证的隐藏能力。

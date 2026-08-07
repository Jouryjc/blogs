// site/src/topics.js —— 12 个研究方向的静态元数据(中文名 + 一句话简介,摘自 wiki/ MOC 页面)
export const TOPICS = {
  'claude-code': {
    zh: 'Claude Code',
    en: 'Claude Code',
    desc: '怎么用好 Claude Code:用 AGENTS.md / CLAUDE.md 把它从"每次像新员工"养成长期协作者,以及它背后的设计取舍与版本演进。',
  },
  'agent-skills': {
    zh: 'Agent Skills',
    en: 'Agent Skills',
    desc: '把软件工程流程(规格、计划、实现、测试、评审、发布)写成可被 Agent 读取执行的 Markdown 技能,让 AI 按工程纪律参与真实工程。',
  },
  'agent-memory': {
    zh: 'Agent 记忆',
    en: 'Agent Memory',
    desc: '让 Agent 拥有"永不遗忘"的长期记忆:记忆的分层架构、写入与召回机制,以及大模型时代记忆系统的工程化落地。',
  },
  'context-engineering': {
    zh: '上下文工程',
    en: 'Context Engineering',
    desc: 'Agent 的很多 token 浪费在和后端的低效沟通上。把上下文组织好、把 token 花在刀刃上,既提速又降本。',
  },
  'prompt-caching': {
    zh: 'Prompt 缓存',
    en: 'Prompt Caching',
    desc: 'Prompt 缓存如何让 LLM 提速降本:以 ~92% 缓存命中率为例,讲清 KV cache、前缀复用与 TTFT 的关系。',
  },
  'rag': {
    zh: 'RAG',
    en: 'RAG',
    desc: '检索增强生成的工程实践:从把整个代码仓库变成可对话的知识图谱,到 RAG 系统 TTFT 的来源与优化。',
  },
  'managed-agents': {
    zh: '托管 Agent',
    en: 'Managed Agents',
    desc: 'Agent 从"一段提示词 + 一层脚本"变成托管运行时:长期运行、安全边界与上下文管理正在成为基础设施。',
  },
  'agent-runtime': {
    zh: 'Agent 运行时',
    en: 'Agent Runtime',
    desc: '最小可用的 Agent 运行时与编排循环:上下文压缩、工具安全、记忆快照、子 Agent 隔离,以及"一个 loop"跑完复杂任务。',
  },
  'agent-design': {
    zh: 'Agent 设计',
    en: 'Agent Design',
    desc: 'Agent 与 AI 产品的设计方法与取舍:Claude Code 这类工具背后的设计空间,以及一线设计者如何看待 AI 时代的产品设计。',
  },
  'agent-safety': {
    zh: 'Agent 安全',
    en: 'Agent Safety',
    desc: 'Agent 时代的新攻击面:要防的不只是提示词注入,而是整个外部环境都可能在给 Agent "下套"。',
  },
  'knowledge-base': {
    zh: '知识库',
    en: 'Knowledge Base',
    desc: '用 AI 把散落的代码与资料变成可检索、可对话的知识库:从代码仓库到业务知识,从代码智能到知识图谱。',
  },
  'ai-industry': {
    zh: '行业观察',
    en: 'AI Industry',
    desc: '行业动态、模型发布与从业者访谈:Agent 时代的换挡时刻,以及每天值得关注的信号。',
  },
}

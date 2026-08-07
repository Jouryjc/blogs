---
title: "FDE 岗位与转型研究笔记"
created_at: "2026-08-02"
tags:
  - type/source
  - topic/ai-industry
  - topic/agent-runtime
moc:
  - "[[ai-industry]]"
  - "[[agent-runtime]]"
related:
  - "[[post-to-wechat/2026-08-02/fde-career-guide/article]]"
---

# FDE 岗位与转型研究笔记

核验时间：2026-08-02（Asia/Singapore）。岗位数量、地点、薪资与出差要求会变化，文章只把它们当作当前岗位样本，不当作整个行业的统一标准。

## 可写入文章的主要判断

- FDE 不是 2026 年才出现的新职位。Palantir 长期使用 Forward Deployed Software Engineer / Delta 这一角色，并明确把它描述成一种对客户结果负责、深入客户环境、端到端交付的工程模式。
- AI 让 FDE 从少数公司的交付方法，扩张成模型公司、云厂商和合作伙伴体系的组织能力。原因不是模型不会生成代码，而是企业 AI 的难点已经转向数据、权限、工作流、评测、可靠性、治理与组织采用。
- 2026 年的强信号包括：OpenAI 成立 Deployment Company；AWS 宣布 10 亿美元投入 Forward Deployed Engineering；Microsoft 宣布向 Frontier Company 投入 25 亿美元并调集 6,000 名行业专家与工程师；Anthropic 与 DXC 的联盟计划培训大量 Claude 认证 FDE。
- FDE 的共通工作链路是：问题发现、技术界定、架构设计、动手开发、生产部署、采用与效果度量、把现场经验反馈给产品/研究团队。
- FDE 不是一个标准化到可以只看岗位名判断的职位。OpenAI 当前把相邻职责拆成 FDE、Forward Deployed Software Engineer、Technical Deployment Lead 和 Platform Engineer；别的公司可能把相似工作叫 Applied AI Engineer、Customer Engineer、Solutions Architect 或 Implementation Engineer。
- 年限不是统一门槛。OpenAI 当前 FDE 样本要求 5 年以上相关经验，FDSWE 样本要求 7 年以上全栈经验；Palantir 同时开放 New Grad FDSE。因此，开发者应按岗位的交付范围、技术深度和客户责任判断级别，而不是只记一个年限。
- 转型作品集不能只放聊天机器人 Demo。更有效的证据是一份端到端交付包：业务问题、成功指标、架构、生产代码、评测集、观测与安全设计、上线及交接文档。

## 一手资料

1. [Palantir：Forward Deployed Software Engineer, New Grad](https://jobs.lever.co/palantir/2e6b0ac8-83e9-4be5-a3aa-cf319f751728)
   - 将 Forward Deployed Engineering 描述为对结果的激进承诺；工作包括架构决策、大规模数据、定制应用、LLM 工作流、生产方案和多层级利益相关者沟通。
   - 当前样本明确接受 New Grad，同时注明不同团队可能需要 25%–50% 出差。

2. [OpenAI：Forward Deployed Engineer](https://openai.com/careers/forward-deployed-engineer-%28fde%29-seattle-seattle/)
   - 定位在客户交付与核心平台开发的交叉点。
   - 覆盖 discovery、technical scoping、system design、build、production rollout；以生产采用、工作流影响和 eval 驱动的产品反馈衡量成功。
   - 当前样本要求 5 年以上工程或技术部署经验、全栈生产代码、生成式 AI 经验与客户沟通能力；出差最高可到 50%。

3. [OpenAI：Forward Deployed Software Engineer](https://openai.com/careers/forward-deployed-software-engineer-sf-san-francisco/)
   - 更强调在客户基础设施上并肩编码、构建全栈方案，以及把一次性方案抽象为跨项目可复用能力。
   - 当前样本要求 7 年以上全栈工程经验，客户侧经验加分。

4. [OpenAI：成立 Deployment Company](https://openai.com/index/openai-launches-the-deployment-company/)
   - 2026-05-11 发布。通过收购 Tomoro，计划从约 150 名有经验的 FDE 与 Deployment Specialists 起步；强调将模型连接到客户的数据、工具、控制系统和业务流程。

5. [AWS：Forward Deployed Engineering for Partners](https://aws.amazon.com/blogs/apn/introducing-forward-deployed-engineering-for-partners-winning-the-future-of-enterprise-ai/)
   - 2026-06-30 发布。宣布 10 亿美元投入，计划让数千名工程师直接与客户共建 Agentic AI，并把方法扩展给合作伙伴。
   - 官方判断是企业 AI 已经超出纯咨询模式，客户需要在真实治理与真实数据条件下运行的生产系统。

6. [Microsoft：Microsoft Frontier Company](https://blogs.microsoft.com/blog/2026/07/02/microsoft-frontier-company-ai-engineering-that-amplifies-and-protects-your-intelligence/)
   - 2026-07-02 发布。宣布 25 亿美元投入和 6,000 名行业专家、工程师，直接与客户共同设计、部署和持续改进 AI 系统。
   - Microsoft 称其模式不止于通常所说的 FDE，因此文章将其视为相邻趋势信号，不把 6,000 人全部称为 FDE。

7. [Anthropic 与 DXC 联盟](https://www.anthropic.com/news/dxc-anthropic-alliance?pubDate=20260602)
   - 2026-06 发布。DXC 将培训大量 Claude 认证 FDE，把 Claude 引入银行、航空、保险、制造和政府等客户环境。

8. [Anthropic：当前职位列表](https://www.anthropic.com/careers/jobs)
   - 核验时列有多个地区的 Forward Deployed Engineer, Applied AI，以及相关的 Applied AI、Technical Deployment 与 Solutions Architecture 岗位。

9. [Anthropic：Applied AI Engineer, Beneficial Deployments](https://job-boards.greenhouse.io/anthropic/jobs/5343697008)
   - 相邻岗位样本覆盖 eval、agent architecture、context engineering、成本优化、结对编程、原型和代码贡献，以及把现场问题反馈给产品与研究。

## 写作边界

- 不写“FDE 是 2026 年最火岗位”之类无法从官方数据证明的判断。
- 不把 Microsoft Frontier Company 的全部 6,000 人直接称为 FDE；官方明确说该组织的能力范围超出通常的 FDE。
- 不用单家公司薪资推导行业薪资。
- 不把 FDE 等同于必须长期驻场。出差和现场比例取决于公司、客户与地区。
- 不把 FDE 写成纯 AI 岗位。角色早于生成式 AI，今天仍存在数据、基础设施、政府、国防等多种方向。

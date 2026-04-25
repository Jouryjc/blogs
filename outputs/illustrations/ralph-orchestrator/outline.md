# Ralph Orchestrator 文章配图方案

## 配图清单

### 图 1：核心循环机制
- 位置：插入在"破局思路：五行伪代码"章节后
- 类型：flowchart
- 内容：展示 Ralph 的核心循环——新上下文 → 执行 → 验收 → 成功则退出/失败则重置上下文继续，突出三个"外接大脑"文件的角色
- 风格：友好技术图解，中文标注

### 图 2：架构总览
- 位置：插入在"架构：中心辐射式设计"章节
- 类型：architecture diagram
- 内容：展示 hub-and-spoke 架构，用户接口层 → ralph-core → ralph-adapters → 各 AI 后端，强调共享状态
- 风格：友好技术图解，中文标注

### 图 3：Hat 系统事件流
- 位置：插入在"Hat 系统"章节
- 类型：sequence/flow diagram
- 内容：展示四角色流水线的事件流转：planner → builder → reviewer → finalizer，用帽子图标表示不同角色
- 风格：友好技术图解，中文标注

### 图 4：Prompt 九层叠加
- 位置：插入在"Prompt 构建：九层叠加"章节
- 类型：layered infographic
- 内容：展示九层 prompt 的叠加结构，从底部 Memories 到顶部 Objective，用不同颜色区分层级
- 风格：友好技术图解，中文标注

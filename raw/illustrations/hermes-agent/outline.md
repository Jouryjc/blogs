---
topic: hermes-agent
type: mixed
density: balanced
style: editorial-technical-blueprint
image_count: 6
source_article: /Users/jouryjc/Documents/code/2026.04/blogs/raw/hermes-agent.md
---

## Illustration 1
**Position**: 标题后，介绍三层架构的位置  
**Purpose**: 帮读者快速建立对 Hermes Agent 全局结构的第一印象  
**Visual Content**: 三层结构图，展示入口层、Agent 内核层、工具与执行层，以及它们之间的数据流与复用关系  
**Filename**: 01-framework-hermes-runtime.png

## Illustration 2
**Position**: “上下文压缩”一节  
**Purpose**: 解释 Hermes 为什么不是简单截断上下文，而是保留任务状态机  
**Visual Content**: 从长对话历史到摘要交接的流程图，突出 goals、progress、decisions、files、next steps 五个保留槽位  
**Filename**: 02-flow-context-compression.png

## Illustration 3
**Position**: “安全系统”一节  
**Purpose**: 解释工具调用不是直通执行，而是经过检查、正规化、扫描、审批的链路  
**Visual Content**: 工具调用到最终执行的安全闸门流程图，体现 dangerous pattern、tirith、approval scope、sandbox/backend  
**Filename**: 03-comparison-tool-security.png

## Illustration 4
**Position**: “记忆系统”一节  
**Purpose**: 解释记忆修改后为什么不会立刻回流进当前 session 的 system prompt  
**Visual Content**: 一张“磁盘记忆 -> session snapshot -> 当前推理 -> 下次 session 生效”的框架图，突出 frozen snapshot 和 delayed effect  
**Filename**: 04-framework-memory-snapshot.png

## Illustration 5
**Position**: “子代理”一节  
**Purpose**: 展示父 Agent 为什么要把中间探索隔离到独立 worker 中  
**Visual Content**: 父 Agent 在中间，左右延伸出 2 到 3 个隔离子代理，标注独立预算、独立终端、禁 memory / clarify / delegate 等约束  
**Filename**: 05-framework-subagent-isolation.png

## Illustration 6
**Position**: “BatchRunner”一节  
**Purpose**: 展示 Hermes 同时作为在线运行时和离线数据工厂的双重角色  
**Visual Content**: 左边是在线 Agent runtime，右边是 batch runner / trajectories / SFT data / analysis，二者共享同一个内核  
**Filename**: 06-framework-runtime-data-factory.png

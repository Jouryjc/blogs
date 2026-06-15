# Google Agentic RAG illustration outline

## Image 1: rag-loop

Purpose: Explain why normal RAG misses multi-hop evidence and how Agentic RAG loops back with feedback.

Layout: left-right comparison.

Left: 普通 RAG
- 用户问题
- 一次检索
- 相关片段
- 答案缺一跳

Right: Agentic RAG
- Planner
- Query Rewriter
- Cross-corpus retrieval
- Sufficient Context Agent
- Feedback loop
- Synthesis

Bottom takeaway: 不是多搜几次，而是知道缺哪块证据。

## Image 2: usage-checklist

Purpose: Give developers a practical adoption checklist.

Layout: multi-stage pipeline.

Stages:
1. 建 corpus
2. 写 description
3. 导入数据
4. 先测单库 RAG
5. 再开跨库检索
6. 加 rerank / parser
7. 记录缺口与引用

Bottom takeaway: 数据边界和 corpus 描述，决定 Agent 能不能选对路。


---
title: "Prompt Caching · MOC"
tags:
  - type/moc
  - topic/prompt-caching
---

# Prompt Caching

Prompt 缓存如何让 LLM 提速与降本:以 Claude 达到 ~92% 缓存命中率为例,讲清楚 KV cache、前缀复用与 TTFT 之间的关系。

## 文章

- [[post-to-wechat/2026-09-02/cross-model-kv-sharing/cross-model-kv-sharing|模型切换别再重算长上下文：KV Cache 开始跨模型接力]] · 见 [[agent-runtime]] / [[context-engineering]]
- [[post-to-wechat/2026-08-30/llm-cache-four-layers/llm-cache-four-layers|同样叫 Cache：前三层失效会变贵，最后一层命中却可能答错]] · 见 [[agent-runtime]] / [[context-engineering]] / [[rag]]
- [[post-to-wechat/2026-08-21/lmcache-kv-cache/lmcache-kv-cache|Agent 上下文越跑越贵，先把 KV Cache 从推理进程里拆出来]] · 见 [[agent-runtime]] / [[context-engineering]]
- [[long-context-kv-cache|长上下文和 KV Cache:为什么上下文不是免费的]]
- [[rag-ttft|RAG 系统的 TTFT 优化:从原理到工程实践]] · 见 [[rag]]

## 原始素材

- [[post-to-wechat/2026-09-02/cross-model-kv-sharing/source/paper-source|跨模型 KV 共享论文事实快照]] · 见 [[agent-runtime]] / [[context-engineering]]
- [[post-to-wechat/2026-09-02/cross-model-kv-sharing/source/research-notes|跨模型 KV 共享工程解读研究笔记]] · 见 [[agent-runtime]] / [[context-engineering]]
- [[x-to-markdown/avichawla/2093265776266637739/kv-prefix-prompt-and-semantic-caching-in-llms-clearly-exp|Avi：KV、Prefix、Prompt 与 Semantic Cache（X Article）]] · 见 [[agent-runtime]] / [[context-engineering]] / [[rag]]
- [[post-to-wechat/2026-08-30/llm-cache-four-layers/source/research-notes|LLM 四层缓存研究笔记]] · 见 [[agent-runtime]] / [[context-engineering]] / [[rag]]
- [[x-to-markdown/akshay_pachaar/2074502882812952666/your-kv-caching-is-broken|Akshay: Your KV Caching Is Broken (X Article)]] · 见 [[agent-runtime]] / [[context-engineering]]
- [[post-to-wechat/2026-08-21/lmcache-kv-cache/source/research-notes|LMCache 与 KV Cache 复用研究笔记]] · 见 [[agent-runtime]] / [[context-engineering]]
- [[post-to-wechat/2026-05-20/akshay-2031021906254766128/source/original-article|Prompt caching, clearly explained(原文)]]
- [[avi-prompt-caching-claude-code|Prompt Caching 是怎么让 Claude 提速的]]
- [[2044670188998803855|Avi Chawla:Prompt caching in LLMs, clearly explained(推文)]]

## 相关主题

[[rag]] · [[context-engineering]] · [[claude-code]]

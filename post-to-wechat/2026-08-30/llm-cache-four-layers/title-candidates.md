# 标题候选

1. 推荐标题：同样叫 Cache：前三层失效会变贵，最后一层命中却可能答错
2. 稳妥标题：KV、Prefix、Prompt、Semantic Cache：四层缓存分别省什么
3. 大众标题：大模型缓存没省到钱，可能是四层 Cache 混在了一起
4. 专家标题：从 KV Cache 到 Semantic Cache：四种复用的收益与正确性边界
5. 反差标题：缓存命中不一定是好事：Semantic Cache 可能直接复用错答案

最终选择第 1 个。它先给出工程后果，再解释四层缓存的差异；同时与已有 LMCache 文章的“跨进程 KV 复用”主线保持区分。

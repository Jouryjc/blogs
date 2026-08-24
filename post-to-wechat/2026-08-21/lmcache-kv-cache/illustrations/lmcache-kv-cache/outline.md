# LMCache 与 KV Cache 配图大纲

## 1. Agent 重复 Prefill

- 文件：`01-agent-loop.png`
- 位置：第一屏判断之后。
- 结论：Agent 每轮只新增一点内容，却可能反复处理整段上下文。
- 结构：左侧 1–20 轮递增上下文，右侧缓存命中后只处理新增尾部。

## 2. Prefix Cache 边界

- 文件：`02-prefix-boundary.png`
- 位置：Prompt Cache 规则之后。
- 结论：尾部增长可以复用，前缀变化和多文档换序才容易失效。
- 结构：上方命中，下方两种未命中/需要重组场景。

## 3. LMCache 分层架构

- 文件：`03-lmcache-layers.png`
- 位置：LMCache 独立服务与数据路径之后。
- 结论：先查共享缓存，缺失部分才做 Prefill；故障时退回正常计算。
- 结构：推理进程、独立 LMCache、HBM/CPU/SSD 三层与回退路径。

## 4. 公众号封面

- 文件：`imgs/article-cover.png`
- 主标题：`Agent 上下文越跑越贵`
- 副标题：`把 KV Cache 拆成独立服务`
- 底部标签：`Prompt Cache · LMCache · CacheBlend`
- 结构：Agent 循环把重复上下文交给共享缓存层，中央 1:1 裁切信息完整。


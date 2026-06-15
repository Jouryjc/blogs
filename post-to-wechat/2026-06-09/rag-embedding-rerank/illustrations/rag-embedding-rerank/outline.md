# RAG Embedding 和 Rerank 配图计划

目标：共 5 张图，包含 1 张封面和 4 张正文信息图。统一使用蒸馏小余知识卡 / Deep Research Sketchnote 风格，奶油纸底、深海军蓝手绘线、低饱和便签卡片、中文短标签。

## 1. article-cover.png

位置：文章开头。

主题：RAG 不是让模型硬背资料，而是先找一篮子，再挑最靠谱。

结构：左侧“问题”，中间“Embedding 找候选”，右侧“Rerank 重新排队”，底部 takeaway。

## 2. embedding-menu-map.png

位置：解释 embedding 的小节。

主题：Embedding 像把资料放进语义地图。

结构：外卖/超市场景类比，不同食物/问题在地图上靠近；相似意思靠近，字面相同不一定靠近。

## 3. retrieval-funnel.png

位置：解释 RAG 检索流程的小节。

主题：先粗找，再精挑。

结构：用户问题 -> query embedding -> vector search top_k -> metadata filter -> candidate chunks。

## 4. rerank-judge.png

位置：解释 rerank 的小节。

主题：Rerank 像老师批卷，逐份对题。

结构：一叠候选片段交给 reranker，reranker 逐个和问题配对评分，输出 top_n。

## 5. rag-parameter-cheatsheet.png

位置：参数配置小节。

主题：RAG 参数不是神秘旋钮，而是一组取舍。

结构：chunk_size、overlap、top_k、top_n、score_threshold、hybrid weight 六个旋钮，旁边写“调大/调小的后果”。

# AgentJudgeBench 正文配图规划

## 01 基准流水线

- 位置：解释论文方法之后
- 判断：这篇论文不是测 Agent，而是测给 Agent 打分的 Judge
- 结构：基础记录 → 三档改写 → Generator → 两类裁判 → 四项 alignment
- 来源：据论文 Figure 1、Figure 2 重绘

## 02 难度退化

- 位置：难题让 Judge 尺子变形一节
- 判断：without-GT 的 alignment 随难度下降约快 1.5 倍
- 结构：easy / medium / hard 双折线 + hard/no-GT 收缩带
- 来源：据论文 Figure 8 重绘

## 03 参考轨迹锚定

- 位置：参考答案可能带偏 Judge 一节
- 判断：参考轨迹能帮助部分 Judge，也可能让部分 Judge 过度锚定
- 结构：参考路径与功能等价替代路径 → Judge → 两个负 GT lift
- 来源：据论文 Figure 3、Table 1 与 corrupted-GT 控制实验重绘

## 04 配置杠杆

- 位置：CoT、温度与 Rubric 一节
- 判断：本论文设置下，CoT 和温度变化很小，结构化 Rubric 更值得先试，但不稳定泛化
- 结构：三个旋钮卡 + 一条限定提示
- 来源：据论文 Figure 4、Figure 5 与 Table 5 重绘

## 图注统一格式

`据 Verma 等《AgentJudgeBench》相关图表重绘，CC BY 4.0。`

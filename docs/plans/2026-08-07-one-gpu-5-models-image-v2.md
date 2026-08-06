# 《5 个模型，1 张 GPU》配图 V2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 按已确认的蒸馏小余视觉规范重构六张配图，替换优化稿中的图片引用，并更新同一个微信公众号草稿。

**Architecture:** 使用内置图片生成能力逐张创建独立 PNG，保存为版本化的 `-v2` 文件；先做文件和视觉验收，再通过最小 Markdown 修改切换引用。发布阶段先运行微信 API 预检，再用既有 `media_id` 和 `index 0` 原位更新，最后回读结果确认没有创建重复草稿。

**Tech Stack:** Codex built-in image generation、PNG、Markdown、ImageMagick/Pillow 图像检查、Bun、baoyu-post-to-wechat API 脚本

---

### Task 1: 固定输入与发布配置

**Files:**
- Read: `docs/superpowers/specs/2026-08-06-one-gpu-5-models-image-v2-design.md`
- Read: `post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md`
- Read: `~/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md`

**Step 1: 核对文章图片槽位**

Run:

```bash
rg -n '^!\[|^coverImage:' post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md
```

Expected: 一处封面字段和六处正文图片引用，均指向现有 `-zh.jpg` 文件。

**Step 2: 核对发布偏好与凭据位置**

Run:

```bash
test -f "$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md"
test -f "$HOME/.baoyu-skills/.env"
```

Expected: 两个检查均返回成功；只确认文件存在，不输出密钥。

**Step 3: 锁定原草稿目标**

使用既有草稿：

```text
media_id = GHixSPLvYVluGTAOLz6FeQulE51gAh7JA7dBYCczmQXYrMTxcP_HcMFmKvLZ52_d
index = 0
theme = grace
color = #0F4C81
```

Expected: 后续不调用新建草稿路径。

### Task 2: 生成六张版本化图片

**Files:**
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/00-cover-v2.png`
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/01-pipeline-v2.png`
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/02-idle-gpu-v2.png`
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/04-one-server-v2.png`
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/05-sie-pool-v2.png`
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/06-decision-checklist-v2.png`

**Step 1: 生成封面**

使用内置图片生成能力创建 2.35:1 横图。逐字使用：

```text
5 个模型，1 张 GPU
小模型省钱，先让硬件共享起来
```

Expected: 五个模型卡片汇入一张 GPU，中央方形裁切仍保留标题和共享关系。

**Step 2: 生成理赔流水线图**

逐字使用：

```text
一单理赔，要走过 5 个模型
解析文档
抽取实体
重排条款
检查照片
生成结论
模型更小，不代表基础设施更省
```

Expected: 五阶段流程和五个独立部署单元均可辨认。

**Step 3: 生成 GPU 账单图**

逐字使用：

```text
GPU 账单按占用时间算
付费时间
真正计算
等待
卡在等待，钱也在烧
```

Expected: 连续付费时间与稀疏计算脉冲形成清楚对比。

**Step 4: 生成统一 Serving 图**

逐字使用：

```text
五套服务，合成一个入口
Agent
一个 API
统一 Serving
五类模型
共享硬件之前，先共享调度
```

Expected: 上方重复部署、下方统一入口，迁移关系清楚。

**Step 5: 生成共享资源池图**

逐字使用：

```text
共享资源池如何省 GPU
按需加载
LRU 驱逐
共享队列
按成本组批
弹性扩缩
显存跟着流量走
```

Expected: 五种机制与中央 GPU 池有真实箭头关系。

**Step 6: 生成决策清单图**

逐字使用：

```text
什么时候值得换 Serving
3 个以上模型
显存长期固定占用
各模型峰值错开
新模型就要新 Server
看不到等待时间
用真实流量做 PoC
先保留 vLLM / TEI
先测一周真实流量，再决定迁移
```

Expected: 问题信号和两条决策出口清楚，不出现仿 README 界面。

### Task 3: 检查并修复图片质量

**Files:**
- Verify: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/*-v2.png`

**Step 1: 验证文件和尺寸**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
from PIL import Image

root = Path('post-to-wechat/2026-08-06/one-gpu-5-models/imgs')
names = [
    '00-cover-v2.png',
    '01-pipeline-v2.png',
    '02-idle-gpu-v2.png',
    '04-one-server-v2.png',
    '05-sie-pool-v2.png',
    '06-decision-checklist-v2.png',
]
for name in names:
    path = root / name
    assert path.exists() and path.stat().st_size > 100_000, name
    with Image.open(path) as image:
        print(name, image.size)
PY
```

Expected: 六个文件均存在且非空；封面接近 2.35:1，正文图接近 16:9。

**Step 2: 逐张视觉检查**

检查清单：

- 奶油纸底、深蓝手绘线、低饱和卡片属于同一套风格。
- 所有中文无乱码、错字、缺字和多余英文。
- 手机缩放后标题、技术关系和底部结论可读。
- GPU、队列、等待、调度和资源池关系符合设计规范。
- 封面中央正方形裁切可用。

Expected: 六张图全部通过；未通过的图片只做一次针对性重生成，并重新检查。

### Task 4: 切换文章到 V2 图片

**Files:**
- Modify: `post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md`

**Step 1: 修改六处正文引用和封面字段**

映射：

```text
00-cover-zh.jpg      -> 00-cover-v2.png
01-pipeline-zh.jpg   -> 01-pipeline-v2.png
02-idle-gpu-zh.jpg   -> 02-idle-gpu-v2.png
04-one-server-zh.jpg -> 04-one-server-v2.png
05-sie-pool-zh.jpg   -> 05-sie-pool-v2.png
06-sie-readme-zh.jpg -> 06-decision-checklist-v2.png
```

**Step 2: 验证只发生预期修改**

Run:

```bash
rg -n 'v2\.png' post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md
rg -n -- '-zh\.jpg' post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md
git diff --check -- post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md
```

Expected: V2 引用共七处（封面字段一次、正文六次），旧中文引用为零，没有空白错误。

### Task 5: 预检并更新原微信草稿

**Files:**
- Read: `post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md`
- Read/Write: 微信草稿 `GHixSPLvYVluGTAOLz6FeQulE51gAh7JA7dBYCczmQXYrMTxcP_HcMFmKvLZ52_d`

**Step 1: 运行 API 预检**

Run:

```bash
bun /Users/yjcjour/.agents/skills/baoyu-post-to-wechat/scripts/wechat-api.ts \
  post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md \
  --theme grace \
  --color '#0F4C81' \
  --cover post-to-wechat/2026-08-06/one-gpu-5-models/imgs/00-cover-v2.png \
  --update-media-id GHixSPLvYVluGTAOLz6FeQulE51gAh7JA7dBYCczmQXYrMTxcP_HcMFmKvLZ52_d \
  --index 0 \
  --dry-run
```

Expected: 预检成功，识别六张正文图片和指定封面，不提交远程变更。

**Step 2: 原位更新草稿**

移除 `--dry-run`，其余参数保持不变。

Expected: 返回 `success: true`、`updated: true`、`index: 0`，并复用相同 `media_id`。

**Step 3: 回读更新结果**

使用脚本支持的草稿读取能力或微信 API 回读既有草稿。

Expected: 标题不变，正文包含六张图片，封面为 V2，草稿 `media_id` 不变。

### Task 6: 保存本地结果

**Files:**
- Create: `post-to-wechat/2026-08-06/one-gpu-5-models/imgs/*-v2.png`
- Modify: `post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md`

**Step 1: 检查变更边界**

Run:

```bash
git status --short -- docs/plans/2026-08-07-one-gpu-5-models-image-v2.md post-to-wechat/2026-08-06/one-gpu-5-models
git diff --check -- post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md
```

Expected: 本次新增计划、六张图片和一处 Markdown 修改；不纳入其他已有脏文件。

**Step 2: 提交本次结果**

```bash
git add \
  docs/plans/2026-08-07-one-gpu-5-models-image-v2.md \
  post-to-wechat/2026-08-06/one-gpu-5-models/article-anti-ai.md \
  post-to-wechat/2026-08-06/one-gpu-5-models/imgs/00-cover-v2.png \
  post-to-wechat/2026-08-06/one-gpu-5-models/imgs/01-pipeline-v2.png \
  post-to-wechat/2026-08-06/one-gpu-5-models/imgs/02-idle-gpu-v2.png \
  post-to-wechat/2026-08-06/one-gpu-5-models/imgs/04-one-server-v2.png \
  post-to-wechat/2026-08-06/one-gpu-5-models/imgs/05-sie-pool-v2.png \
  post-to-wechat/2026-08-06/one-gpu-5-models/imgs/06-decision-checklist-v2.png
git diff --cached --check
git commit -m "content: rebuild one GPU article illustrations"
```

Expected: 提交仅包含计划、六张新图和优化稿图片引用。

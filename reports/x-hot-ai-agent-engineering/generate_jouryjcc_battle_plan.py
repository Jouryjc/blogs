#!/usr/bin/env python3
from __future__ import annotations

import base64
import html
import json
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "outputs"
SKILL_ROOT = Path("/Users/yjcjour/.codex/skills/dashen-x-battle-plan")
LOGO_PATH = SKILL_ROOT / "assets" / "logo.svg"

TODAY = date(2026, 4, 26)
START = date(2026, 4, 27)
END = START + timedelta(days=29)

HANDLE = "@Jouryjcc"
HANDLE_SLUG = "Jouryjcc"
NICKNAME = "Joury"
BIO = "AI Agent / 编程实战 / 个人知识库 / 从代码到业务"
DIRECTIONS = ["AI Agent 实战", "编程与自动化", "个人知识管理", "从代码到业务"]


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def logo_uri() -> str:
    if LOGO_PATH.exists():
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
        return f"data:image/svg+xml;base64,{b64}"
    return ""


def fmt_day(d: date) -> str:
    return f"{d.month}月{d.day}日"


def weekdays(d: date) -> str:
    return ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()]


MILESTONES = [
    ("D1-D3", "完成账号包装、置顶挑战帖、首批 3 篇重型长帖", "30 粉", "验证定位是否有人愿意关注"),
    ("D4-D7", "每天 1 长帖 + 6 短推 + 40 条高质量回复", "150 粉", "找到 2 个互动率最高的内容角度"),
    ("D8-D14", "做 2 个可下载模板，开始互推/连麦/引用合作", "500 粉", "至少 1 条帖文破 2 万曝光"),
    ("D15-D21", "把已验证角度系列化，集中打 3 个大号评论区", "1,200 粉", "稳定每天 50-100 新粉"),
    ("D22-D30", "发布 2 篇旗舰复盘，放大结果和方法论", "2,000 粉", "把关注理由从热闹变成信任"),
]


STREAMS = [
    {
        "name": "AI Agent 实战",
        "job": "让开发者看到你不是搬运工具新闻，而是在把 Agent 真正用进工作流。",
        "proof": "截图、命令、失败记录、前后对比、可复用模板。",
        "cadence": "长帖每周 3 篇，短推每天 2 条。",
        "topics": [
            "Codex/Claude Code 真实任务拆解",
            "Agent 失败案例和修复方法",
            "技能、MCP、工作流模板",
            "AI 写作、发文、配图自动化",
            "一人公司如何用 Agent 替代重复劳动",
        ],
    },
    {
        "name": "编程与自动化",
        "job": "给工程师一个明确关注理由：跟着你能把工具链搭起来。",
        "proof": "仓库结构、脚本片段、终端输出、前后耗时对比。",
        "cadence": "长帖每周 2 篇，短推每天 1-2 条。",
        "topics": [
            "从需求到 PR 的 Agent 协作流程",
            "自动生成报告、PPT、公众号草稿",
            "个人知识库维护规范",
            "调试、测试、验收清单",
            "把一次性脚本产品化",
        ],
    },
    {
        "name": "从代码到业务",
        "job": "突破纯技术圈层，吸引创作者、独立开发者和小团队老板。",
        "proof": "业务场景、成本节省、变现路径、真实限制。",
        "cadence": "长帖每周 1-2 篇，短推每天 1 条。",
        "topics": [
            "AI 不是效率玩具，是低成本交付系统",
            "个人 IP 的内容资产怎么沉淀",
            "小团队如何用 Agent 做客服、销售、运营",
            "开源项目怎么讲成商业故事",
            "免费工具如何导向付费咨询或产品",
        ],
    },
    {
        "name": "公开挑战与复盘",
        "job": "空号起盘需要戏剧张力。30 天 0 到 2000 粉本身就是连续剧。",
        "proof": "每日数据、失败原因、下一步调整。",
        "cadence": "每天 1 条固定格式，周日 1 篇复盘。",
        "topics": [
            "今日新增粉丝/曝光/主页访问",
            "哪条内容有效，哪条没有用",
            "今天回复了哪些大号，结果如何",
            "明天要测试的 1 个假设",
            "7 天、14 天、21 天阶段复盘",
        ],
    },
]


THREAD_TOPICS = [
    "我准备用 30 天把这个空号做到 2000 粉：方法、数据和失败都会公开",
    "AI Agent 新手最容易犯的 7 个错：我会先避开这些坑",
    "我用 Codex 管一个博客仓库：从素材到成稿的完整流程",
    "提示词不是护城河，工作流才是：一个可复制的 Agent 系统长什么样",
    "从 0 搭一个 AI 写作流水线：素材、检索、大纲、配图、排版、发布",
    "Claude Code 和 Codex 哪些任务该交给 Agent，哪些必须自己把关",
    "第 1 周复盘：空号起盘，最难的不是写内容，是找到别人为什么关注你",
    "我设计了一个个人知识库规则：让 AI 不再每次从零理解我",
    "把一篇英文技术长文变成公众号草稿：我会保留哪些，删掉哪些",
    "AI Agent 做内容的 5 个真实限制：别把自动化当魔法",
    "一个人如何同时维护 X、公众号和知识库：我的最小发布系统",
    "我会关注的 30 个 AI/开发者账号，以及我怎么在评论区建立存在感",
    "如果只能给 Agent 一个上下文文件，我会这样写 AGENTS.md",
    "第 2 周复盘：哪些内容带粉，哪些内容只是自嗨",
    "我把 10 个重复任务交给 Agent，最后只有 4 个值得自动化",
    "从代码到业务：为什么技术人做内容不能只晒工具",
    "如何写一条让大号愿意回复的技术评论：5 个可复制结构",
    "我准备做一个 Agent 工作流模板包：需求、结构和第一版目录",
    "AI 编程最危险的瞬间：代码能跑，但需求已经偏了",
    "一个开发者的内容飞轮：项目、笔记、教程、案例、产品",
    "第 3 周复盘：如果还没到 900 粉，我会立刻改变打法",
    "我用公开挑战逼自己输出：这件事为什么比内容日历更重要",
    "把爆款拆成工程问题：钩子、证据、结构、分发、转化",
    "用 Agent 做研究报告：我会怎样避免一本正经地胡说八道",
    "小团队最该优先自动化的 8 类工作，不包括写朋友圈文案",
    "为什么我不建议新人一上来追热点：空号最缺的是信任资产",
    "30 天 2000 粉倒计时 5 天：最后一波我要怎么冲",
    "我会怎样把 X 粉丝导向长期资产：知识库、邮件、社群或产品",
    "这 30 天里最有效的 10 条内容原则：有数据才算数",
    "终局复盘：这个空号有没有做到 2000 粉，以及下一阶段怎么打",
]


SHORT_TEMPLATES = [
    ("反差钩子", "大多数人做 AI 内容，输在太像新闻。\n更好的写法是：我遇到一个具体问题，试了 3 种方法，最后只有第 2 种能跑。"),
    ("公开挑战", "第 [N] 天，空号冲 2000 粉。\n今天测试一个假设：[假设]。\n如果失败，我明天公开复盘原因。"),
    ("技术拆解", "一个 Agent 工作流不要先问“怎么自动化”。\n先问：输入是什么、验收标准是什么、人在哪一步必须介入。"),
    ("踩坑复盘", "今天踩了一个坑：[坑]。\n表面原因是 [A]，真正原因是 [B]。\n下次我会把 [规则] 写进工作流。"),
    ("观点短刀", "提示词会贬值，流程会复利。\n你真正该沉淀的不是一句 prompt，而是一套能被重复调用的上下文。"),
    ("案例开头", "我刚把 [任务] 从 [原耗时] 压到 [新耗时]。\n不是因为模型更强，而是因为我补了 3 个很土的工程约束。"),
    ("互动提问", "你现在最想交给 AI Agent 的重复任务是什么？\n我挑 3 个，用长帖拆成可执行工作流。"),
    ("清单型", "新人做 AI Agent，先别追炫技。\n先准备 4 个文件：目标、输入样例、验收标准、失败案例。"),
    ("引用大号", "这条说到关键点了。\n我补一个工程视角：真正决定 Agent 是否可用的不是模型回答，而是错误能不能被发现。"),
    ("复盘 CTA", "今天这条没有跑起来。\n原因我猜不是选题，而是关注理由不够强。\n明天改成：[新标题]。"),
    ("业务转译", "技术内容想破圈，要把“我用了什么工具”改成“我帮谁减少了什么成本”。"),
    ("系列预告", "接下来 7 天我只做一件事：\n把 AI Agent 工作流从玩具拆成生产系统。\n每天交付一个可复制模板。"),
]


DAILY_RHYTHM = [
    ("08:30", "公开挑战短推", "昨日新增粉丝、曝光、主页访问、今天要测试的假设"),
    ("10:30", "主长帖", "当天唯一重型内容，主题来自 30 天日历"),
    ("12:20", "高质量回复 1", "进入 10 个目标账号评论区，每条回复必须补充信息或案例"),
    ("15:00", "工具/截图短推", "展示一个真实流程、命令、失败截图或模板片段"),
    ("18:30", "观点短推", "用一句强判断制造转发和评论"),
    ("21:30", "高质量回复 2", "复盘当天热点，引用 2 条相关大号内容"),
    ("23:00", "收口短推", "今天学到什么，明天改什么"),
]


def build_calendar() -> list[dict[str, str]]:
    rows = []
    for idx, topic in enumerate(THREAD_TOPICS):
        d = START + timedelta(days=idx)
        if idx % 7 in (0, 3):
            primary = "AI Agent 实战"
            ratio = "AI Agent 3 / 编程 2 / 业务 1 / 复盘 1"
        elif idx % 7 in (1, 4):
            primary = "编程与自动化"
            ratio = "编程 3 / AI Agent 2 / 业务 1 / 复盘 1"
        elif idx % 7 == 2:
            primary = "从代码到业务"
            ratio = "业务 3 / AI Agent 2 / 编程 1 / 复盘 1"
        elif idx % 7 == 5:
            primary = "互动增长"
            ratio = "回复 40 条 / 原创 5 条 / 引用 2 条"
        else:
            primary = "周复盘"
            ratio = "复盘 3 / 公开数据 2 / 下周预告 2"
        rows.append(
            {
                "day": f"D{idx + 1}",
                "date": fmt_day(d),
                "weekday": weekdays(d),
                "topic": topic,
                "primary": primary,
                "ratio": ratio,
            }
        )
    return rows


def table(headers: list[str], rows: list[list[object]], cls: str = "") -> str:
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{e(cell)}</td>" for cell in row) + "</tr>")
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def render_html() -> str:
    logo = logo_uri()
    calendar = build_calendar()
    milestone_rows = [[*row] for row in MILESTONES]
    rhythm_rows = [[time, action, standard] for time, action, standard in DAILY_RHYTHM]
    calendar_rows = [[r["day"], r["date"], r["weekday"], r["primary"], r["topic"], r["ratio"]] for r in calendar]
    template_rows = [[name, text] for name, text in SHORT_TEMPLATES]

    stream_cards = []
    for s in STREAMS:
        topics = "".join(f"<li>{e(t)}</li>" for t in s["topics"])
        stream_cards.append(
            f"""
            <section class="stream">
              <h3>{e(s["name"])}</h3>
              <p><strong>任务：</strong>{e(s["job"])}</p>
              <p><strong>证据：</strong>{e(s["proof"])}</p>
              <p><strong>节奏：</strong>{e(s["cadence"])}</p>
              <ul>{topics}</ul>
            </section>
            """
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{e(HANDLE_SLUG)} X 内容作战计划</title>
<style>
@page {{ size: A4; margin: 15mm 15mm 17mm; }}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: "Songti SC", "STSong", "SimSun", "Times New Roman", serif;
  color: #141414;
  font-size: 12px;
  line-height: 1.62;
  background: #fff;
}}
.page {{ page-break-after: always; }}
.page:last-child {{ page-break-after: auto; }}
.cover {{
  min-height: 266mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 8mm 0 4mm;
}}
.logo {{ width: 210px; height: auto; margin-bottom: 18mm; }}
.text-logo {{ font-size: 22px; font-weight: 800; letter-spacing: 0; }}
.eyebrow {{ font-size: 11px; color: #666; letter-spacing: 2px; text-transform: uppercase; }}
h1 {{
  margin: 4mm 0 3mm;
  font-size: 32px;
  line-height: 1.12;
  letter-spacing: 0;
}}
.subtitle {{ font-size: 16px; color: #333; margin: 0 0 8mm; }}
.cover-line {{ border-top: 3px solid #111; padding-top: 5mm; }}
.meta-grid, .kpi-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid #111;
}}
.meta-grid div, .kpi-grid div {{ padding: 11px 12px; border-right: 1px solid #d8d8d8; }}
.meta-grid div:last-child, .kpi-grid div:last-child {{ border-right: 0; }}
.label {{ color: #777; font-size: 10px; letter-spacing: 1px; }}
.value {{ font-weight: 800; font-size: 20px; line-height: 1.2; margin-top: 3px; }}
.note {{
  border-left: 4px solid #111;
  padding: 10px 14px;
  background: #f7f7f7;
  color: #333;
}}
.footer {{
  position: fixed;
  left: 15mm;
  right: 15mm;
  bottom: 6mm;
  display: flex;
  justify-content: space-between;
  color: #999;
  font-size: 10px;
  border-top: 1px solid #e5e5e5;
  padding-top: 4px;
}}
.section {{ padding-top: 2mm; }}
.part {{ color: #777; letter-spacing: 2px; font-size: 10px; margin-bottom: 2mm; }}
h2 {{
  font-size: 23px;
  margin: 0 0 5mm;
  padding-bottom: 2mm;
  border-bottom: 2px solid #111;
  line-height: 1.2;
}}
h3 {{ font-size: 15px; margin: 5mm 0 2mm; }}
p {{ margin: 0 0 2.5mm; }}
table {{
  width: 100%;
  border-collapse: collapse;
  margin: 3mm 0 5mm;
  font-size: 11px;
}}
th {{
  background: #111;
  color: #fff;
  text-align: left;
  padding: 7px 8px;
  font-weight: 700;
}}
td {{
  border-bottom: 1px solid #e7e7e7;
  padding: 7px 8px;
  vertical-align: top;
}}
tr:nth-child(even) td {{ background: #f8f8f8; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.three {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
.box {{ border: 1px solid #ddd; padding: 11px 12px; break-inside: avoid; }}
.box strong {{ display: block; margin-bottom: 4px; }}
.stream {{ border: 1px solid #ddd; padding: 12px 14px; margin-bottom: 10px; break-inside: avoid; }}
.stream h3 {{ margin-top: 0; border-bottom: 1px solid #ddd; padding-bottom: 6px; }}
ul {{ margin: 2mm 0 0 0; padding-left: 16px; }}
li {{ margin-bottom: 1mm; }}
.danger {{ border-left-color: #111; background: #f4f4f4; }}
.quote {{
  font-size: 15px;
  line-height: 1.7;
  border-top: 2px solid #111;
  border-bottom: 1px solid #bbb;
  padding: 12px 0;
  margin: 6mm 0;
}}
.small {{ color: #666; font-size: 10.5px; }}
.calendar td:nth-child(5) {{ font-weight: 650; }}
.templates td:first-child {{ width: 20%; font-weight: 700; }}
.templates td:last-child {{ white-space: pre-line; }}
.brand-end {{ text-align: center; margin-top: 18mm; color: #777; }}
.brand-end img {{ width: 180px; opacity: .72; }}
</style>
</head>
<body>
<div class="footer"><span>AI最严厉的父亲 · dashen.wang</span><span>{e(HANDLE)} 内容作战计划</span></div>

<section class="cover page">
  <div>
    {"<img class='logo' src='" + logo + "' alt='dashen.wang'>" if logo else "<div class='text-logo'>AI最严厉的父亲 · dashen.wang</div>"}
    <div class="cover-line">
      <div class="eyebrow">X CONTENT BATTLE PLAN · FIRST TIME BASELINE</div>
      <h1>{e(HANDLE_SLUG)}<br>30 天 X 作战计划</h1>
      <p class="subtitle">空号起盘，目标从 0 内容做到 2,000 粉丝</p>
      <p class="small">生成日期：{TODAY.isoformat()} ｜ 计划周期：{START.isoformat()} 至 {END.isoformat()} ｜ 模式：首次分析，无历史 CSV</p>
    </div>
  </div>
  <div>
    <div class="kpi-grid">
      <div><div class="label">当前内容</div><div class="value">0</div></div>
      <div><div class="label">30 天目标</div><div class="value">2,000 粉</div></div>
      <div><div class="label">日均新增要求</div><div class="value">67 粉</div></div>
      <div><div class="label">执行强度</div><div class="value">高压</div></div>
    </div>
    <div class="note danger" style="margin-top: 8mm;">
      刺耳但必要：空号 30 天到 2,000 粉，不是靠“每天随便发几条”完成的。你需要一个公开挑战、每天一篇重型长帖、持续进入目标大号评论区、至少两次外部协作放大。每天低于 2.5 小时投入，目标应下调到 300-800 粉。
    </div>
  </div>
  <div class="small">by AI最严厉的父亲 · dashen.wang</div>
</section>

<section class="section page">
  <div class="part">PART 1</div>
  <h2>基准判断</h2>
  <p>这个计划按你提供的信息生成：账号 {e(HANDLE)} 当前没有输出内容，目标是在 30 天内做到 2,000 粉。因无法读取历史 CSV，也未能从公开索引可靠验证账号数据，本报告把当前账号视为“空号起盘”。</p>
  {table(["项目", "判断", "行动含义"], [
      ["账号阶段", "0 内容冷启动", "不要先追求完美人设，先让市场用数据告诉你哪个角度有关注价值"],
      ["核心定位", BIO, "用 AI Agent 实战切入，避免泛泛聊 AI 新闻"],
      ["目标难度", "极高", "必须有公开实验、可复制模板、评论区分发和协作放大"],
      ["第一关注理由", "跟着 Joury 看一个开发者如何用 Agent 做内容和业务系统", "关注理由必须写进 Bio、置顶帖和每日复盘"],
      ["最大风险", "只发原创，不做分发", "空号没有初始信任，评论区和引用帖是前 14 天的主要曝光入口"],
  ])}
  <div class="quote">一句话战略：把“30 天从空号到 2,000 粉”做成公开实验，用 AI Agent 实战内容证明你值得关注，用高质量回复借别人的流量池完成冷启动。</div>
  <h3>开局前 30 分钟必须改完</h3>
  <div class="two">
    <div class="box"><strong>昵称</strong>Joury｜AI Agent 实战<br><span class="small">不要只写英文名。空号需要让陌生人一眼知道你解决什么问题。</span></div>
    <div class="box"><strong>Bio</strong>用 AI Agent / Codex / Claude Code 做可复用工作流。30 天公开实验：空号冲 2,000 粉，每天交付一个真实案例或模板。</div>
    <div class="box"><strong>头像与 Banner</strong>头像清晰、真人或强识别符号。Banner 写一句话：AI Agent 工作流公开实验：0 → 2,000。</div>
    <div class="box"><strong>置顶帖</strong>第 1 天长帖必须置顶。标题就是公开挑战，不要用抽象价值观开头。</div>
  </div>
</section>

<section class="section page">
  <div class="part">PART 2</div>
  <h2>增长目标拆解</h2>
  {table(["阶段", "主动作", "粉丝目标", "判断标准"], milestone_rows)}
  <h3>过程 KPI</h3>
  {table(["指标", "30 天目标", "每日最低线", "失败信号"], [
      ["新增粉丝", "2,000", "67", "第 7 天低于 80，说明定位或分发有问题"],
      ["原创长帖", "30 篇", "1 篇", "连续 2 天断更，公开挑战会失去可信度"],
      ["原创短推", "180-240 条", "6-8 条", "只有长帖没有短推，主页缺少密度"],
      ["高质量回复", "1,200 条", "40 条", "回复只是夸赞或抢沙发，无法带粉"],
      ["引用/合作", "20 次", "每 2 天至少 1 次", "没有大号互动，空号曝光会卡死"],
      ["模板资产", "2 个", "第 10 天前做出第 1 个", "没有可领取资产，关注转化偏低"],
  ])}
  <div class="note">判断目标是否还成立：第 14 天低于 350 粉，需要把目标改成 1,000 粉或引入外部渠道；第 21 天低于 900 粉，除非出现大号转发，否则 2,000 粉基本不可控。</div>
</section>

<section class="section page">
  <div class="part">PART 3</div>
  <h2>内容战略</h2>
  {"".join(stream_cards)}
</section>

<section class="section page">
  <div class="part">PART 4</div>
  <h2>每日执行框架</h2>
  {table(["时间", "动作", "合格标准"], rhythm_rows)}
  <h3>回复打法</h3>
  <div class="three">
    <div class="box"><strong>目标账号</strong>每天固定 30 个 AI、开发者、独立产品、内容增长账号。只盯同一批人，连续出现。</div>
    <div class="box"><strong>回复质量</strong>每条回复必须提供补充案例、反例、框架、数据或可执行步骤。不要“说得对”。</div>
    <div class="box"><strong>时间窗口</strong>大号发帖后 10 分钟内优先回复。晚了就改做引用帖，不要在沉底评论区浪费精力。</div>
  </div>
  <h3>置顶帖草稿</h3>
  <div class="quote">我准备做一个公开实验：用 30 天把这个空号做到 2,000 粉。<br><br>方向只做一件事：AI Agent 如何真正进入开发者、创作者和小团队的工作流。<br><br>每天我会公开：发了什么、数据如何、哪里失败、明天怎么改。<br><br>如果你也在用 Codex、Claude Code、Agent 工作流做内容或产品，可以跟着看。</div>
</section>

<section class="section page">
  <div class="part">PART 5</div>
  <h2>30 天创作日历</h2>
  {table(["天数", "日期", "星期", "主方向", "长帖题目", "短推配比"], calendar_rows, "calendar")}
</section>

<section class="section page">
  <div class="part">PART 6</div>
  <h2>短推模板库</h2>
  {table(["模板", "可直接改写的句式"], template_rows, "templates")}
  <h3>长帖结构</h3>
  {table(["段落", "写什么", "标准"], [
      ["1. 钩子", "冲突、数字、失败或公开挑战", "第一屏必须让陌生人知道为什么要点开"],
      ["2. 背景", "你遇到的具体问题", "不要从宏大趋势开始"],
      ["3. 过程", "你做了哪 3-5 步", "每一步有截图、命令、清单或判断标准"],
      ["4. 结果", "节省时间、减少错误、产出质量、粉丝数据", "没有数据就用前后对比"],
      ["5. 坑", "哪一步失败、为什么", "失败比正确更容易建立信任"],
      ["6. CTA", "让读者评论一个关键词或问题", "CTA 要和后续资产绑定，不要泛泛求关注"],
  ])}
</section>

<section class="section page">
  <div class="part">PART 7</div>
  <h2>执行清单与复盘规则</h2>
  <div class="two">
    <div class="box"><strong>每天收盘记录</strong>粉丝数、主页访问、最高曝光帖、最高带粉帖、回复数量、今天最有效的一句话。</div>
    <div class="box"><strong>每 7 天复盘</strong>按内容类型统计：长帖、短推、回复、引用、模板资产。只保留带粉或带互动的角度。</div>
    <div class="box"><strong>第 10 天交付资产</strong>做一个《AI Agent 工作流模板包》或《X 空号起盘记录表》，让评论关键词的人有明确领取理由。</div>
    <div class="box"><strong>第 15 天开始协作</strong>找 5 个同方向账号，做互评、共同 Space、互相拆工作流或模板交换。</div>
  </div>
  <h3>禁止事项</h3>
  {table(["不要做", "原因", "替代动作"], [
      ["搬运 AI 新闻", "空号没有信息差，新闻号竞争极强", "写你亲手测试后的结论"],
      ["大量空泛金句", "容易有赞但不带粉", "每条观点后面补案例或操作步骤"],
      ["只发中文技术术语", "非工程师看不懂，破圈困难", "每篇长帖都写清业务场景"],
      ["追十个方向", "算法和读者都无法识别你", "前 14 天只围绕 AI Agent 工作流"],
      ["把回复当灌水", "低质量回复可能被折叠，也不会形成信任", "回复要比原帖多一个信息增量"],
  ])}
  <h3>可参考的平台机制</h3>
  <p class="small">X 官方说明中，公开帖子默认可被任何人查看；回复的展示会考虑相关性、可信度、安全性、作者互动和订阅状态等因素；账号推荐会参考用户活动、互动、关注、转发和引用等信号。因此本计划把“公开账号、原创资产、高质量回复、引用互动”作为冷启动核心动作。</p>
</section>

<section class="section">
  <div class="part">FINAL</div>
  <h2>最后的硬话</h2>
  <p>这不是一个“灵感来了就发”的计划。你要做的是连续 30 天把自己变成一个可观察的案例：每天有产出，每周有复盘，每个失败都有下一步调整。</p>
  <p>最重要的一件事：不要等账号有粉丝才开始做资产。第一天就把自己当成 2,000 粉账号来写，区别只是分发要靠评论区和协作。</p>
  <div class="brand-end">
    {"<img src='" + logo + "' alt='dashen.wang'>" if logo else ""}
    <p>本报告由 <strong>AI最严厉的父亲</strong> 内容作战系统生成</p>
    <p class="small">dashen.wang · 内容作战计划 · 数据驱动创作</p>
  </div>
</section>
</body>
</html>"""


def build_passport() -> dict:
    now = datetime(2026, 4, 26, 13, 30).isoformat()
    analysis_id = TODAY.isoformat()
    return {
        "version": "2.0",
        "handle": HANDLE,
        "nickname": NICKNAME,
        "bio": BIO,
        "directions": DIRECTIONS,
        "created_at": now,
        "last_analysis_date": now,
        "total_analyses": 1,
        "baseline": {
            "date": TODAY.isoformat(),
            "followers": 0,
            "followers_estimated": True,
            "avg_imp": 0,
            "monthly_new_follows": 0,
            "reply_ratio": 0,
            "top_content_type": "暂无历史数据",
            "top_content_avg_imp": 0,
            "viral_formula": "公开挑战 + 真实案例 + 可复用模板 + 高频分发",
        },
        "analyses": [
            {
                "id": analysis_id,
                "date": analysis_id,
                "mode": "FIRST_TIME",
                "data_period": "无历史CSV，按空号起盘",
                "followers_at_time": 0,
                "stats": {
                    "total_posts": 0,
                    "total_imp": 0,
                    "avg_imp": 0,
                    "max_imp": 0,
                    "new_follows_period": 0,
                    "reply_ratio": 0,
                    "type_breakdown": {},
                    "top_viral_posts": [],
                    "best_month": None,
                },
                "plan": {
                    "start_date": START.isoformat(),
                    "end_date": END.isoformat(),
                    "kpi_targets": {
                        "new_followers_30d": 2000,
                        "target_followers_by_day_7": 150,
                        "target_followers_by_day_14": 500,
                        "target_followers_by_day_21": 1200,
                        "long_articles_per_day": 1,
                        "short_tweets_per_day": 6,
                        "strategic_replies_per_day": 40,
                        "quote_or_collab_posts_30d": 20,
                        "lead_magnets_30d": 2,
                    },
                    "daily_ratio": {
                        "AI Agent 实战": 0.4,
                        "编程与自动化": 0.25,
                        "从代码到业务": 0.2,
                        "公开挑战与复盘": 0.15,
                    },
                    "top3_article_topics": THREAD_TOPICS[:3],
                    "calendar": build_calendar(),
                },
                "self_reported_execution": None,
                "execution_score": None,
            }
        ],
        "execution_history": [],
        "viral_patterns": {
            "confirmed_formulas": [
                {
                    "formula": "公开挑战 + 真实案例 + 可复用模板 + 高频分发",
                    "first_seen": TODAY.isoformat(),
                    "examples_count": 0,
                    "avg_imp": 0,
                    "still_working": None,
                }
            ],
            "fatigue_signals": [],
            "emerging_patterns": [],
        },
        "growth_milestones": [
            {"date": TODAY.isoformat(), "followers": 0, "note": "首次分析基准：空号起盘，粉丝数按0估算"}
        ],
        "notes": [
            "用户提供账号链接：https://x.com/Jouryjcc",
            "用户说明当前账号没有输出内容。",
            "未提供CSV和历史数据，本报告按AI Agent/开发者实战定位生成。",
            "7天后建议带最新X数据CSV和本passport做执行复盘。",
        ],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUT_DIR / f"{HANDLE_SLUG}_作战计划_{TODAY.isoformat()}.html"
    pdf_path = OUT_DIR / f"{HANDLE_SLUG}_作战计划_{TODAY.isoformat()}.pdf"
    passport_path = OUT_DIR / f"{HANDLE_SLUG}_passport.json"

    html_path.write_text(render_html(), encoding="utf-8")
    passport_path.write_text(json.dumps(build_passport(), ensure_ascii=False, indent=2), encoding="utf-8")

    chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    if not chrome.exists():
        raise SystemExit("Google Chrome not found; HTML and passport were generated but PDF was not rendered.")
    subprocess.run(
        [
            str(chrome),
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--print-to-pdf={pdf_path}",
            "--no-pdf-header-footer",
            html_path.as_uri(),
        ],
        check=True,
    )

    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")
    print(f"Passport: {passport_path}")


if __name__ == "__main__":
    main()

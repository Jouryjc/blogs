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
BIO = "AI Agent / Codex / Claude Code / 自动化工作流"


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def logo_uri() -> str:
    if LOGO_PATH.exists():
        b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
        return f"data:image/svg+xml;base64,{b64}"
    return ""


def table(headers: list[str], rows: list[list[object]], cls: str = "") -> str:
    head = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{cell if isinstance(cell, Raw) else e(cell)}</td>" for cell in row) + "</tr>")
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


class Raw(str):
    pass


OFFER_ROWS = [
    [
        "主报价",
        "AI Agent 工作流急诊",
        "$50 / 24小时交付",
        "客户给一个重复任务；你交付一份可执行流程、一个提示词/AGENTS.md片段、一个验收清单。",
    ],
    [
        "升级报价",
        "Codex/Claude Code 小工作流搭建",
        "$100-$150 / 48小时交付",
        "帮客户把一个具体任务跑通：资料整理、文章草稿、报告生成、仓库规则、测试清单。",
    ],
    [
        "低价资产",
        "AI Agent 工作流模板包",
        "$9-$19",
        "用于吸引犹豫用户，不作为第一目标。先靠服务拿现金和案例。",
    ],
]

POSTS = [
    [
        "置顶帖",
        "我把目标改了：不追粉丝数，先从 X 上赚到第一个 $100。\n\n方法很简单：卖 2 个 $50 的 AI Agent 工作流急诊名额。\n\n你给我一个重复任务，我在 24 小时内交付：流程拆解、可复制提示词、验收清单。\n\n我会公开记录：曝光、私信、成交、失败原因。",
    ],
    [
        "案例帖",
        "一个适合 AI Agent 改造的任务，通常有 3 个特征：\n1. 每周重复发生\n2. 输入材料相似\n3. 结果可以被验收\n\n不满足这 3 条，先别自动化，容易把时间浪费在花活上。",
    ],
    [
        "销售帖",
        "我开 2 个 beta 名额：AI Agent 工作流急诊，$50。\n\n适合：开发者、内容创作者、小团队老板。\n不适合：想要万能 AI、没有具体任务、只想聊概念。\n\n评论或私信我一个重复任务，我先判断值不值得做。",
    ],
    [
        "信任帖",
        "我不会承诺“AI 替你赚钱”。\n\n我只做一件具体的事：把一个重复任务拆成能被 Agent 执行、能被人验收、失败后能修正的流程。\n\n如果 24 小时内我判断做不了，不收钱。",
    ],
]

DM_ROWS = [
    [
        "冷启动回复后私信",
        "刚看了你说的 [具体任务]，这类任务我会先看 3 件事：输入是否固定、结果能否验收、失败成本多高。你愿意的话，把一个真实样例发我，我免费判断它值不值得用 Agent 做。",
    ],
    [
        "报价",
        "这个任务可以做成一个小工作流。我现在开 beta：$50，24 小时交付一份流程拆解、提示词/规则文件、验收清单。做不了我提前说，不收钱。",
    ],
    [
        "催单",
        "我今天还剩 1 个 beta 位置。你这个任务如果本周还会重复发生，建议直接做；如果只是一次性任务，就没必要花钱。",
    ],
    [
        "成交后收集素材",
        "发我 3 个东西：1. 你现在怎么做这个任务；2. 一个真实输入样例；3. 你认为合格输出长什么样。我收到后开始拆。",
    ],
]

DAILY_PLAN = [
    ["D1", "改 Bio、发置顶帖、明确 $50 急诊报价", "不发泛内容，只发“从 X 赚 $100”公开实验", "$0"],
    ["D2", "发 2 条案例帖，回复 30 个目标账号", "每条回复都指出一个可自动化任务", "$0"],
    ["D3", "做 5 个免费迷你诊断，公开 1 个匿名拆解", "目标拿到 2 个强痛点私信", "$0-$50"],
    ["D4", "发销售帖，推 2 个 beta 名额", "不谈粉丝，只谈交付和时限", "$50"],
    ["D5", "交付第 1 个客户，截图做结果帖", "必须拿到一句可公开反馈", "$50"],
    ["D6", "继续 30 条高质量回复，引用 3 个大号任务痛点", "把反馈帖置顶 24 小时", "$50-$100"],
    ["D7", "成交第 2 个客户或发布复盘", "如果没成交，降价到 $25 做 4 单，不再纠结体面", "$100"],
    ["D8-D14", "把成交案例变成长帖和模板包", "目标：再成交 2 单 $100 服务", "$300+"],
    ["D15-D21", "从手工服务提炼成可重复产品", "目标：模板包 10 单或服务 3 单", "$500+"],
    ["D22-D30", "筛选高客单方向，决定是否做订阅/课程/顾问包", "目标：现金优先，粉丝只是副产品", "$1,000+"],
]

TARGET_ACCOUNTS = [
    "正在发 AI 工具测评但缺流程落地的人",
    "有公众号/博客/Newsletter，但更新成本高的人",
    "独立开发者、小团队创始人、咨询顾问",
    "公开说自己在用 Codex / Claude Code / Cursor 的人",
    "发过“想自动化”“效率低”“资料太多”的人",
]

REPLY_FORMULAS = [
    "我会先问：这个任务多久重复一次？如果低于每周一次，自动化 ROI 不一定成立。",
    "这里真正难的不是 prompt，是验收标准。没有验收标准，Agent 做出来的东西看起来对，实际不可用。",
    "这个可以拆成 3 步：输入标准化、Agent 初稿、人类验收。最先自动化的应该是第 1 步。",
    "如果你愿意给一个匿名样例，我可以帮你判断这个任务值不值得做成 Agent 工作流。",
    "不要先买工具。先把当前手工流程写下来，能写清楚的部分才适合交给 Agent。",
]


def render_html() -> str:
    logo = logo_uri()
    target_list = "".join(f"<li>{e(item)}</li>" for item in TARGET_ACCOUNTS)
    reply_list = "".join(f"<li>{e(item)}</li>" for item in REPLY_FORMULAS)
    post_rows = [[kind, Raw("<pre>" + e(text) + "</pre>")] for kind, text in POSTS]
    dm_rows = [[kind, Raw("<pre>" + e(text) + "</pre>")] for kind, text in DM_ROWS]

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{HANDLE_SLUG} 从0赚100美元作战计划</title>
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
.cover {{
  min-height: 266mm;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 8mm 0 4mm;
}}
.logo {{ width: 210px; height: auto; margin-bottom: 18mm; }}
.cover-line {{ border-top: 3px solid #111; padding-top: 5mm; }}
.eyebrow {{ font-size: 11px; color: #666; letter-spacing: 2px; text-transform: uppercase; }}
h1 {{ margin: 4mm 0 3mm; font-size: 32px; line-height: 1.12; letter-spacing: 0; }}
.subtitle {{ font-size: 16px; color: #333; margin: 0 0 8mm; }}
.small {{ color: #666; font-size: 10.5px; }}
.kpi-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid #111;
}}
.kpi-grid div {{ padding: 11px 12px; border-right: 1px solid #d8d8d8; }}
.kpi-grid div:last-child {{ border-right: 0; }}
.label {{ color: #777; font-size: 10px; letter-spacing: 1px; }}
.value {{ font-weight: 800; font-size: 20px; line-height: 1.2; margin-top: 3px; }}
.note {{
  border-left: 4px solid #111;
  padding: 10px 14px;
  background: #f7f7f7;
  color: #333;
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
th {{ background: #111; color: #fff; text-align: left; padding: 7px 8px; font-weight: 700; }}
td {{ border-bottom: 1px solid #e7e7e7; padding: 7px 8px; vertical-align: top; }}
tr:nth-child(even) td {{ background: #f8f8f8; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.box {{ border: 1px solid #ddd; padding: 11px 12px; break-inside: avoid; }}
.box strong {{ display: block; margin-bottom: 4px; }}
pre {{
  white-space: pre-wrap;
  font-family: "Songti SC", "STSong", "SimSun", serif;
  margin: 0;
  line-height: 1.58;
}}
.quote {{
  font-size: 15px;
  line-height: 1.7;
  border-top: 2px solid #111;
  border-bottom: 1px solid #bbb;
  padding: 12px 0;
  margin: 6mm 0;
}}
ul {{ margin: 2mm 0 0 0; padding-left: 16px; }}
li {{ margin-bottom: 1mm; }}
.brand-end {{ text-align: center; margin-top: 18mm; color: #777; }}
.brand-end img {{ width: 180px; opacity: .72; }}
</style>
</head>
<body>
<div class="footer"><span>AI最严厉的父亲 · dashen.wang</span><span>{e(HANDLE)} 现金流作战计划</span></div>

<section class="cover page">
  <div>
    {"<img class='logo' src='" + logo + "' alt='dashen.wang'>" if logo else ""}
    <div class="cover-line">
      <div class="eyebrow">X CASHFLOW BATTLE PLAN · FROM ZERO TO FIRST $100</div>
      <h1>{e(HANDLE_SLUG)}<br>从 0 赚到第一个 $100</h1>
      <p class="subtitle">不追粉丝数，先验证现金流</p>
      <p class="small">生成日期：{TODAY.isoformat()} ｜ 计划周期：{START.isoformat()} 至 {END.isoformat()} ｜ 模式：目标修订，现金流优先</p>
    </div>
  </div>
  <div>
    <div class="kpi-grid">
      <div><div class="label">第一目标</div><div class="value">$100</div></div>
      <div><div class="label">最快路径</div><div class="value">2 单</div></div>
      <div><div class="label">首单期限</div><div class="value">7 天</div></div>
      <div><div class="label">粉丝 KPI</div><div class="value">取消</div></div>
    </div>
    <div class="note" style="margin-top: 8mm;">结论：如果你说的“马斯克的 100 刀”是 X 官方广告分成，那从 0 账号短期不现实。真正可控的第一笔钱，是用 X 找到 2 个有痛点的人，各卖一个 $50 的 AI Agent 工作流急诊。</div>
  </div>
  <div class="small">by AI最严厉的父亲 · dashen.wang</div>
</section>

<section class="section page">
  <div class="part">PART 1</div>
  <h2>先把幻想砍掉</h2>
  <p>X 官方 Creator Revenue Sharing 当前要求包括：Premium 订阅、近 3 个月 500 万自然曝光、至少 500 个 verified followers、支持国家、遵守 X 用户协议；通过后还要连接 Stripe 和身份验证，广告分成最低 payout 当前是 $30。订阅功能要求更高：至少 2,000 verified followers 和近 3 个月 500 万自然曝光，订阅最低 payout 是 $50。</p>
  <div class="quote">所以，第一笔 $100 不应该等平台打钱。你要用 X 做获客，用服务或数字资产收钱。粉丝不是目标，成交对话才是目标。</div>
  {table(["路径", "从0可控性", "预计时间", "判断"], [
      ["X 官方广告分成", "低", "90天以上且不保证", "需要 500 verified followers + 500万曝光，先不作为第一目标"],
      ["X 订阅", "低", "90天以上且不保证", "需要 2,000 verified followers + 500万曝光，不适合冷启动"],
      ["卖 $50 微服务", "高", "7-14天", "最直接，先用手工交付换现金和案例"],
      ["卖 $9-$19 模板包", "中", "14-30天", "需要信任和流量，可作为第二阶段"],
  ])}
</section>

<section class="section page">
  <div class="part">PART 2</div>
  <h2>你的第一款报价</h2>
  {table(["层级", "名称", "价格", "交付"], OFFER_ROWS)}
  <h3>为什么先卖服务，不先卖课或模板</h3>
  <div class="two">
    <div class="box"><strong>你现在没有信任资产</strong>模板包需要别人相信你知道他们的问题。服务可以先从一个具体任务切入。</div>
    <div class="box"><strong>服务能反向生成内容</strong>每一单都能变成匿名案例帖、复盘帖、模板素材。</div>
    <div class="box"><strong>$50 心理门槛低</strong>客户不用开会审批，你也能用 24 小时交付控制风险。</div>
    <div class="box"><strong>目标不是规模化</strong>第一阶段目标只有一个：证明陌生人愿意为你的判断和执行付钱。</div>
  </div>
  <h3>合格客户画像</h3>
  <ul>{target_list}</ul>
</section>

<section class="section page">
  <div class="part">PART 3</div>
  <h2>7 天成交剧本</h2>
  {table(["日期", "主任务", "执行重点", "现金目标"], DAILY_PLAN)}
  <div class="note">第 7 天如果没有成交，不要怪粉丝少。只检查三件事：你有没有每天 30 条高质量回复；你有没有明确报价；你有没有让别人发真实样例给你。</div>
</section>

<section class="section page">
  <div class="part">PART 4</div>
  <h2>公开内容</h2>
  {table(["类型", "可直接发布的文本"], post_rows)}
</section>

<section class="section page">
  <div class="part">PART 5</div>
  <h2>回复与私信</h2>
  <h3>回复公式</h3>
  <ul>{reply_list}</ul>
  <h3>私信脚本</h3>
  {table(["场景", "文本"], dm_rows)}
</section>

<section class="section page">
  <div class="part">PART 6</div>
  <h2>交付模板</h2>
  {table(["模块", "内容", "验收标准"], [
      ["任务定义", "客户当前怎么做、多久做一次、输入材料是什么", "一句话能说清楚任务边界"],
      ["Agent流程", "拆成输入清洗、上下文注入、生成、检查、人工确认", "客户能照着跑第一遍"],
      ["提示词/规则文件", "给出一段可复制 prompt 或 AGENTS.md/CLAUDE.md 片段", "不是泛泛建议，必须能粘贴使用"],
      ["验收清单", "合格输出、常见失败、人工检查点", "客户知道什么时候该信，什么时候该停"],
      ["下一步报价", "如果客户想继续，给 $100-$150 搭建报价", "不是硬推，而是基于下一处瓶颈"],
  ])}
  <h3>收款和边界</h3>
  <div class="two">
    <div class="box"><strong>先收款再交付</strong>$50 beta 也要先收款。可以用 Stripe Payment Link、PayPal 或其他你可用的收款方式。</div>
    <div class="box"><strong>不承诺收益</strong>只承诺工作流交付，不承诺客户通过 AI 赚钱。</div>
    <div class="box"><strong>不接模糊需求</strong>没有真实样例、没有验收标准、只想“做个万能 Agent”的，不接。</div>
    <div class="box"><strong>保留匿名案例权</strong>成交前说明：会去除敏感信息后公开复盘，用来做内容资产。</div>
  </div>
</section>

<section class="section">
  <div class="part">PART 7</div>
  <h2>30 天之后怎么接回 X 官方分成</h2>
  <p>当你已经靠服务赚到第一笔钱，再考虑马斯克真正打给你的钱。那时 X 官方分成是副线：持续发布高质量内容，积累 verified followers 和 verified Home Timeline impressions。不要反过来等广告分成救你。</p>
  {table(["阶段", "现金目标", "平台目标", "动作"], [
      ["0-7天", "$100", "不看粉丝", "卖 2 个 $50 急诊"],
      ["8-30天", "$500-$1,000", "形成案例和主页信任", "把服务复盘成公开内容和模板"],
      ["31-90天", "$2,000+", "冲 X 官方分成门槛", "规模化内容，同时积累 verified followers 和曝光"],
  ])}
  <h3>资料来源</h3>
  <p class="small">X Creator Revenue Sharing: https://help.x.com/en/using-x/creator-revenue-sharing<br> X Creator Monetization Standards: https://help.x.com/en/rules-and-policies/content-monetization-standards<br> X Creator Subscriptions: https://help.x.com/en/using-x/subscriptions-creator</p>
  <div class="brand-end">
    {"<img src='" + logo + "' alt='dashen.wang'>" if logo else ""}
    <p>本报告由 <strong>AI最严厉的父亲</strong> 内容作战系统生成</p>
    <p class="small">dashen.wang · 内容作战计划 · 数据驱动创作</p>
  </div>
</section>
</body>
</html>"""


def build_passport() -> dict:
    old_path = OUT_DIR / f"{HANDLE_SLUG}_passport.json"
    if old_path.exists():
        passport = json.loads(old_path.read_text(encoding="utf-8"))
    else:
        passport = {
            "version": "2.0",
            "handle": HANDLE,
            "nickname": NICKNAME,
            "bio": BIO,
            "directions": ["AI Agent", "编程自动化", "从代码到业务"],
            "created_at": datetime.combine(TODAY, datetime.min.time()).isoformat(),
            "analyses": [],
            "execution_history": [],
            "viral_patterns": {"confirmed_formulas": [], "fatigue_signals": [], "emerging_patterns": []},
            "growth_milestones": [],
            "notes": [],
        }

    now = datetime(2026, 4, 26, 14, 20).isoformat()
    passport["last_analysis_date"] = now
    passport["bio"] = BIO
    passport["directions"] = ["AI Agent 工作流", "现金流实验", "编程自动化", "从代码到业务"]
    passport["total_analyses"] = len(passport.get("analyses", [])) + 1
    passport.setdefault("notes", []).append("2026-04-26 目标修订：放弃 30 天 2000 粉 KPI，改为从 X 上赚到第一个 $100。")

    cash_analysis = {
        "id": f"{TODAY.isoformat()}-cash-first",
        "date": TODAY.isoformat(),
        "mode": "GOAL_REVISION_CASH_FIRST",
        "data_period": "无历史CSV，按空号现金流起盘",
        "followers_at_time": 0,
        "stats": {
            "total_posts": 0,
            "total_imp": 0,
            "avg_imp": 0,
            "max_imp": 0,
            "new_follows_period": 0,
            "cash_revenue": 0,
            "pipeline_value": 0,
        },
        "plan": {
            "start_date": START.isoformat(),
            "end_date": END.isoformat(),
            "primary_goal": "Earn first $100 from X-sourced customers, not from follower growth.",
            "kpi_targets": {
                "cash_revenue_7d": 100,
                "paid_customers_7d": 2,
                "offer_price": 50,
                "qualified_conversations_7d": 20,
                "strategic_replies_per_day": 30,
                "public_case_studies_30d": 3,
                "x_creator_revenue_share": "Later-stage only; requires Premium, 5M organic impressions in 3 months, and 500 verified followers.",
            },
            "offer": {
                "name": "AI Agent 工作流急诊",
                "price_usd": 50,
                "delivery_window": "24 hours",
                "deliverables": ["流程拆解", "可复制提示词/规则文件", "验收清单", "下一步建议"],
            },
            "daily_plan": DAILY_PLAN,
        },
        "self_reported_execution": None,
        "execution_score": None,
    }

    passport.setdefault("analyses", []).append(cash_analysis)
    passport.setdefault("growth_milestones", []).append(
        {"date": TODAY.isoformat(), "followers": 0, "note": "目标从粉丝增长改为现金流：7天赚到第一个$100"}
    )
    passport.setdefault("viral_patterns", {}).setdefault("emerging_patterns", []).append(
        {"pattern": "公开现金流实验 + $50微服务 + 匿名案例复盘", "first_seen": TODAY.isoformat(), "status": "to_test"}
    )
    return passport


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUT_DIR / f"{HANDLE_SLUG}_赚钱作战计划_{TODAY.isoformat()}.html"
    pdf_path = OUT_DIR / f"{HANDLE_SLUG}_赚钱作战计划_{TODAY.isoformat()}.pdf"
    passport_path = OUT_DIR / f"{HANDLE_SLUG}_passport.json"
    cash_passport_path = OUT_DIR / f"{HANDLE_SLUG}_cash_passport_{TODAY.isoformat()}.json"

    html_path.write_text(render_html(), encoding="utf-8")
    passport = build_passport()
    passport_path.write_text(json.dumps(passport, ensure_ascii=False, indent=2), encoding="utf-8")
    cash_passport_path.write_text(json.dumps(passport, ensure_ascii=False, indent=2), encoding="utf-8")

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
    print(f"Cash passport copy: {cash_passport_path}")


if __name__ == "__main__":
    main()

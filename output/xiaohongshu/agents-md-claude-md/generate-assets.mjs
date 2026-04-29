import fs from "node:fs";
import path from "node:path";

const outDir = path.resolve("output/xiaohongshu/agents-md-claude-md");
const slidesDir = path.join(outDir, "slides");
fs.mkdirSync(slidesDir, { recursive: true });

const W = 1080;
const H = 1440;
const navy = "#0b2545";
const cream = "#fff7e8";
const card = "#fffdf8";
const muted = "#5f6f86";
const orange = "#ffbe73";
const blue = "#d8ecff";
const green = "#d9f0d1";
const coral = "#ff897d";

const slides = [
  {
    no: "01",
    kicker: "AI 编程工具真正好用的关键",
    title: ["别只跑", "/init"],
    subtitle: "AGENTS.md / CLAUDE.md 真正该怎么养",
    kind: "cover",
  },
  {
    no: "02",
    kicker: "核心观点",
    title: ["它不是配置文件", "而是工作契约"],
    body: [
      "第一次生成多少内容不重要",
      "重要的是每次 agent 猜错、漏测、乱改边界后",
      "你能不能把纠正沉淀成下次会生效的规则",
    ],
    tags: ["长期记忆", "团队约定", "减少返工"],
  },
  {
    no: "03",
    kicker: "初始化之后先做这一步",
    title: ["别急着开工", "先验证规则是否生效"],
    steps: [
      "生成或手写 AGENTS.md / CLAUDE.md",
      "删掉空话、重复信息、代码里能推断的内容",
      "让 agent 复述它读到的规则",
      "跑一个小任务，看它是否会按规则收尾",
    ],
  },
  {
    no: "04",
    kicker: "文件里最该写什么",
    title: ["只写会改变行为的内容"],
    grid: [
      ["命令", "能直接复制执行"],
      ["风格", "项目特有偏好"],
      ["边界", "哪里不能乱改"],
      ["验收", "怎么才算完成"],
      ["踩坑", "老工程师\n知道的坑"],
      ["协作", "分支、提交\nPR 规则"],
    ],
  },
  {
    no: "05",
    kicker: "维护方法",
    title: ["把 prompt", "沉淀成规则"],
    loop: ["Agent 做错", "判断是否重复", "写成短规则", "小任务验证", "删除过期规则"],
    quote: "做错一次先纠正，做错两次写进文件",
  },
  {
    no: "06",
    kicker: "一个反直觉提醒",
    title: ["文件不是越厚越好"],
    body: [
      "短而准的规则是导航",
      "长而乱的规则是噪音",
      "上下文是预算，不是仓库",
    ],
    callout: "不要塞完整 API 文档、历史流水账和“写干净代码”这种空话",
  },
  {
    no: "07",
    kicker: "推荐结构",
    title: ["按作用范围", "拆成三层记忆"],
    layers: [
      ["全局层", "~/.codex/AGENTS.md\n~/.claude/CLAUDE.md", "个人稳定习惯"],
      ["项目层", "AGENTS.md / CLAUDE.md", "团队约定\n验证命令"],
      ["局部层", "子目录 AGENTS.md\n.claude/rules/", "模块差异\n高风险边界"],
    ],
  },
  {
    no: "08",
    kicker: "可直接照做",
    title: ["最小模板", "先从这 6 块开始"],
    checklist: [
      "项目心智模型",
      "常用命令",
      "完成定义",
      "代码约定",
      "架构边界",
      "已知坑 + 维护规则",
    ],
    footer: "目标不是写满，而是让 agent 少猜、少返工、会验证",
  },
];

function esc(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function tspans(lines, x, y, size, weight = 700, fill = navy, gap = 1.25, anchor = "start") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${fill}" font-size="${size}" font-weight="${weight}" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">${lines
    .map((line, i) => `<tspan x="${x}" dy="${i === 0 ? 0 : size * gap}">${esc(line)}</tspan>`)
    .join("")}</text>`;
}

function badge(x, y, text, color = blue) {
  return `<g><rect x="${x}" y="${y}" width="${text.length * 28 + 42}" height="54" rx="27" fill="${color}" stroke="${navy}" stroke-width="5"/><text x="${x + 21}" y="${y + 37}" fill="${navy}" font-size="28" font-weight="800" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">${esc(text)}</text></g>`;
}

function bg(slide) {
  return `<rect width="${W}" height="${H}" fill="${cream}"/>
  <circle cx="900" cy="165" r="190" fill="#ffe0a6" opacity="0.72"/>
  <circle cx="145" cy="1280" r="210" fill="${blue}" opacity="0.78"/>
  <path d="M70 170 C250 120 385 145 545 95" fill="none" stroke="${orange}" stroke-width="18" stroke-linecap="round" opacity="0.65"/>
  <path d="M600 1310 C760 1260 900 1290 1040 1215" fill="none" stroke="${orange}" stroke-width="18" stroke-linecap="round" opacity="0.65"/>
  <rect x="38" y="38" width="1004" height="1364" rx="44" fill="none" stroke="${navy}" stroke-width="10"/>
  <text x="86" y="112" fill="${muted}" font-size="28" font-weight="800" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">码农小余知识图解</text>
  <text x="936" y="112" text-anchor="end" fill="${muted}" font-size="28" font-weight="800" font-family="SFMono-Regular, Menlo, monospace">${slide.no}/08</text>`;
}

function iconDoc(x, y, label, fill = card) {
  return `<g>
    <path d="M${x} ${y} h168 l46 48 v214 h-214 z" fill="${fill}" stroke="${navy}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M${x + 168} ${y} v52 h46" fill="none" stroke="${navy}" stroke-width="8"/>
    <text x="${x + 22}" y="${y + 138}" fill="${navy}" font-size="34" font-weight="900" font-family="SFMono-Regular, Menlo, monospace">${esc(label)}</text>
  </g>`;
}

function render(slide) {
  let body = bg(slide);
  body += badge(86, 150, slide.kicker, green);

  if (slide.kind === "cover") {
    body += `<rect x="104" y="235" width="872" height="430" rx="42" fill="${card}" stroke="${navy}" stroke-width="10"/>`;
    body += tspans(slide.title, 540, 370, 112, 900, navy, 1.05, "middle");
    body += tspans([slide.subtitle], 540, 590, 44, 800, navy, 1.2, "middle");
    body += iconDoc(172, 780, "AGENTS", blue);
    body += iconDoc(696, 780, "CLAUDE", card);
    body += `<path d="M425 900 C500 820 600 820 675 900" fill="none" stroke="${navy}" stroke-width="10" stroke-linecap="round"/>
    <path d="M655 865 l28 35 l-44 8" fill="${orange}" stroke="${navy}" stroke-width="8" stroke-linejoin="round"/>
    <rect x="215" y="1060" width="650" height="92" rx="32" fill="${orange}" stroke="${navy}" stroke-width="8"/>
    <text x="540" y="1120" text-anchor="middle" fill="${navy}" font-size="35" font-weight="900" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">纠错 → 写规则 → 验证 → 修剪</text>
    <text x="540" y="1270" text-anchor="middle" fill="${muted}" font-size="34" font-weight="700" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif">让 AI 不再每次都像第一次进项目</text>`;
    return wrapSvg(body);
  }

  body += tspans(slide.title, 86, 295, 74, 900, navy, 1.12);

  if (slide.body) {
    body += `<rect x="86" y="500" width="908" height="${slide.callout ? 455 : 520}" rx="40" fill="${card}" stroke="${navy}" stroke-width="8"/>`;
    slide.body.forEach((line, i) => {
      body += `<circle cx="145" cy="${590 + i * 96}" r="18" fill="${[orange, green, blue][i % 3]}" stroke="${navy}" stroke-width="5"/>`;
      body += tspans([line], 190, 606 + i * 96, 42, 800, navy);
    });
    if (slide.callout) {
      body += `<rect x="126" y="945" width="828" height="185" rx="32" fill="${blue}" stroke="${navy}" stroke-width="7"/>`;
      body += tspans(["不要塞完整 API 文档、历史流水账", "也不要写“写干净代码”这种空话"], 540, 1015, 36, 800, navy, 1.35, "middle");
    }
    if (slide.tags) {
      slide.tags.forEach((t, i) => { body += badge(132 + i * 270, 1190, t, [blue, green, orange][i]); });
    }
    return wrapSvg(body);
  }

  if (slide.steps) {
    slide.steps.forEach((s, i) => {
      const y = 482 + i * 170;
      body += `<rect x="104" y="${y}" width="872" height="126" rx="34" fill="${card}" stroke="${navy}" stroke-width="7"/>`;
      body += `<circle cx="168" cy="${y + 63}" r="35" fill="${[blue, green, orange, coral][i]}" stroke="${navy}" stroke-width="6"/>`;
      body += `<text x="168" y="${y + 76}" text-anchor="middle" fill="${navy}" font-size="34" font-weight="900" font-family="Arial, sans-serif">${i + 1}</text>`;
      body += tspans([s], 230, y + 78, 36, 800, navy);
    });
    return wrapSvg(body);
  }

  if (slide.grid) {
    slide.grid.forEach(([a, b], i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const x = 86 + col * 462;
      const y = 475 + row * 215;
      body += `<rect x="${x}" y="${y}" width="410" height="165" rx="34" fill="${card}" stroke="${navy}" stroke-width="7"/>`;
      body += `<rect x="${x + 28}" y="${y + 28}" width="94" height="54" rx="27" fill="${[blue, green, orange, coral, blue, green][i]}" stroke="${navy}" stroke-width="5"/>`;
      body += tspans([a], x + 75, y + 66, 30, 900, navy, 1.2, "middle");
      body += tspans(b.split("\n"), x + 150, y + 96, 29, 800, navy, 1.18);
    });
    body += tspans(["一句话标准：", "只写 agent 不容易自己猜对、但会影响结果的东西"], 540, 1190, 34, 800, muted, 1.35, "middle");
    return wrapSvg(body);
  }

  if (slide.loop) {
    const coords = [[540, 485], [802, 655], [710, 965], [370, 965], [278, 655]];
    coords.forEach(([x, y], i) => {
      body += `<rect x="${x - 135}" y="${y - 54}" width="270" height="108" rx="30" fill="${[blue, green, orange, blue, green][i]}" stroke="${navy}" stroke-width="7"/>`;
      body += tspans([slide.loop[i]], x, y + 13, 30, 900, navy, 1.1, "middle");
      const [nx, ny] = coords[(i + 1) % coords.length];
      body += `<path d="M${x + (nx > x ? 145 : nx < x ? -145 : 0)} ${y} Q${(x + nx) / 2} ${(y + ny) / 2 - 40} ${nx + (nx > x ? -145 : nx < x ? 145 : 0)} ${ny}" fill="none" stroke="${navy}" stroke-width="7" stroke-linecap="round" opacity="0.75"/>`;
    });
    body += `<rect x="130" y="1130" width="820" height="150" rx="40" fill="${card}" stroke="${navy}" stroke-width="8"/>`;
    body += tspans([slide.quote], 540, 1220, 42, 900, navy, 1.2, "middle");
    return wrapSvg(body);
  }

  if (slide.layers) {
    slide.layers.forEach(([a, b, c], i) => {
      const y = 430 + i * 250;
      body += `<rect x="94" y="${y}" width="892" height="190" rx="36" fill="${card}" stroke="${navy}" stroke-width="8"/>`;
      body += `<circle cx="175" cy="${y + 95}" r="52" fill="${[blue, green, orange][i]}" stroke="${navy}" stroke-width="7"/>`;
      body += tspans([a], 260, y + 76, 42, 900, navy);
      body += tspans(b.split("\n"), 260, y + 130, 29, 800, muted, 1.15);
      body += tspans(c.split("\n"), 788, y + 90, 29, 800, navy, 1.2, "middle");
    });
    body += tspans(["越全局，越稳定；越靠近代码，越具体"], 540, 1240, 36, 900, navy, 1.2, "middle");
    return wrapSvg(body);
  }

  if (slide.checklist) {
    slide.checklist.forEach((s, i) => {
      const y = 440 + i * 110;
      body += `<rect x="126" y="${y}" width="828" height="82" rx="28" fill="${card}" stroke="${navy}" stroke-width="6"/>`;
      body += `<circle cx="180" cy="${y + 41}" r="25" fill="${[blue, green, orange][i % 3]}" stroke="${navy}" stroke-width="5"/>`;
      body += `<path d="M168 ${y + 39} l10 12 l20 -25" fill="none" stroke="${navy}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`;
      body += tspans([s], 230, y + 55, 34, 850, navy);
    });
    body += `<rect x="105" y="1165" width="870" height="132" rx="36" fill="${orange}" stroke="${navy}" stroke-width="8"/>`;
    body += tspans([slide.footer], 540, 1245, 35, 900, navy, 1.2, "middle");
    return wrapSvg(body);
  }

  return wrapSvg(body);
}

function wrapSvg(inner) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <style>text{letter-spacing:0}</style>
  ${inner}
</svg>`;
}

for (const slide of slides) {
  const filename = `${slide.no}-agents-md-claude-md.svg`;
  fs.writeFileSync(path.join(slidesDir, filename), render(slide), "utf8");
}

const caption = `# 小红书图文发布文案

## 标题备选

1. 别只跑 /init，AGENTS.md 和 CLAUDE.md 要这样养
2. 让 AI 真懂你的项目：AGENTS.md / CLAUDE.md 使用指南
3. Coding Agent 越用越顺手的关键，不是 prompt，而是这份文件

## 正文

很多人用 Codex 或 Claude Code，第一步都会跑 /init。

但问题是：跑完就不管，AI 下次还是会猜错测试命令、乱改边界、漏掉验证。

我现在更建议把 AGENTS.md / CLAUDE.md 当成一份“长期工作契约”，而不是一次性配置文件。

真正有用的做法是：

1. 初始化后先让 agent 复述它读到的规则，确认文件真的生效。
2. 文件里只写会改变行为的内容：命令、项目风格、架构边界、完成定义、已知坑、协作规则。
3. 每次 agent 犯重复错误，就把纠正沉淀成一条短规则。
4. 文件不要越写越厚，短而准才是导航，长而乱就是噪音。
5. 按全局层、项目层、局部层拆分，不要把所有规则塞进一个文件。

一句话总结：

不要把 AGENTS.md / CLAUDE.md 当成 AI 配置。
把它当成你和 agent 之间不断迭代的工作契约。

这样 AI 才不会每次都像第一次进项目。

## 标签

#AI编程 #ClaudeCode #Codex #程序员 #效率工具 #AI工具 #软件工程 #提示词工程 #AGENTSmd #CLAUDEmd

## 图片顺序

1. 封面：别只跑 /init
2. 核心观点：不是配置文件，而是工作契约
3. 初始化后先验证规则是否生效
4. 文件里最该写的 6 类内容
5. 把 prompt 沉淀成规则
6. 文件不是越厚越好
7. 三层记忆结构
8. 最小模板行动清单
`;

fs.writeFileSync(path.join(outDir, "caption.md"), caption, "utf8");
fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify({
  title: "别只跑 /init，AGENTS.md 和 CLAUDE.md 要这样养",
  platform: "xiaohongshu",
  format: "8-image carousel, 1080x1440",
  sourceArticle: "outputs/agents-md-claude-md.md",
  slides: slides.map((s) => ({
    no: s.no,
    svg: `slides/${s.no}-agents-md-claude-md.svg`,
    png: `slides/${s.no}-agents-md-claude-md.png`,
    title: s.title.join(" "),
  })),
  caption: "caption.md",
}, null, 2), "utf8");

console.log(`Wrote ${slides.length} SVG slides and caption to ${outDir}`);

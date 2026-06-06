import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outputPath = path.join(__dirname, 'imgs', '01-claude-code-setup-single.png');

const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      width: 896px;
      height: 1200px;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", Arial, sans-serif;
      color: #10233a;
      background: #f7efe2;
    }
    .card {
      width: 100%;
      height: 100%;
      padding: 44px;
      background:
        linear-gradient(90deg, rgba(15,76,129,.05) 1px, transparent 1px),
        linear-gradient(0deg, rgba(15,76,129,.05) 1px, transparent 1px),
        #fbf5e9;
      background-size: 38px 38px;
      border: 9px solid #10233a;
      border-radius: 42px;
    }
    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 12px 18px;
      border: 4px solid #10233a;
      border-radius: 999px;
      background: #dff0e6;
      font-size: 26px;
      font-weight: 850;
      color: #10233a;
      margin-bottom: 20px;
    }
    h1 {
      margin: 0;
      font-size: 76px;
      line-height: 1.08;
      letter-spacing: 0;
      font-weight: 950;
      color: #10233a;
    }
    .slug {
      margin-top: 16px;
      display: inline-block;
      padding: 12px 18px;
      border-radius: 18px;
      background: #10233a;
      color: #fff7e8;
      font-size: 34px;
      font-weight: 820;
    }
    .summary {
      margin-top: 24px;
      padding: 22px 24px;
      border: 5px solid #10233a;
      border-radius: 26px;
      background: #d9ecf7;
      font-size: 35px;
      line-height: 1.3;
      font-weight: 820;
    }
    .flow {
      margin-top: 30px;
      display: grid;
      grid-template-columns: 1fr 74px 1fr;
      gap: 14px;
      align-items: center;
    }
    .flowBox {
      min-height: 138px;
      padding: 22px 18px;
      border: 5px solid #10233a;
      border-radius: 28px;
      background: #fffaf0;
      box-shadow: 10px 10px 0 rgba(16,35,58,.12);
    }
    .flowBox strong {
      display: block;
      font-size: 35px;
      line-height: 1.12;
      margin-bottom: 10px;
    }
    .flowBox span {
      display: block;
      color: #496074;
      font-size: 24px;
      line-height: 1.25;
      font-weight: 750;
    }
    .arrow {
      text-align: center;
      font-size: 58px;
      font-weight: 950;
      color: #e7863d;
    }
    .grid {
      margin-top: 30px;
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
    }
    .pill {
      min-height: 112px;
      padding: 14px 8px;
      border: 4px solid #10233a;
      border-radius: 22px;
      background: #fff;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      font-size: 23px;
      line-height: 1.1;
      font-weight: 900;
    }
    .pill:nth-child(1) { background: #fde0bd; }
    .pill:nth-child(2) { background: #dff0e6; }
    .pill:nth-child(3) { background: #d9ecf7; }
    .pill:nth-child(4) { background: #f4dfef; }
    .pill:nth-child(5) { background: #f6e7b8; }
    .pill small {
      display: block;
      margin-top: 8px;
      color: #50677a;
      font-size: 18px;
      font-weight: 780;
    }
    .action {
      margin-top: 30px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    .actionCard {
      padding: 20px;
      border: 5px solid #10233a;
      border-radius: 24px;
      background: #fffaf0;
    }
    .actionCard h2 {
      margin: 0 0 10px;
      font-size: 31px;
      line-height: 1.15;
      font-weight: 950;
      color: #10233a;
    }
    .actionCard p {
      margin: 0;
      font-size: 24px;
      line-height: 1.28;
      font-weight: 760;
      color: #334b5f;
    }
    .bottom {
      margin-top: 30px;
      padding: 22px 24px;
      border: 5px solid #10233a;
      border-radius: 28px;
      background: #10233a;
      color: #fff7e8;
      font-size: 32px;
      line-height: 1.25;
      font-weight: 900;
      text-align: center;
    }
  </style>
</head>
<body>
  <main class="card">
    <div class="eyebrow">现在就能实操</div>
    <h1>神级！<br>项目自动化配置</h1>
    <div class="slug">Claude Code Setup</div>
    <section class="summary">一个插件先读懂仓库，再告诉你当前项目最该先配什么。</section>

    <section class="flow">
      <div class="flowBox">
        <strong>先读项目</strong>
        <span>目录结构、依赖、语言文件、代码模式</span>
      </div>
      <div class="arrow">→</div>
      <div class="flowBox">
        <strong>再给建议</strong>
        <span>每类先挑 1-2 个最值得落地的配置</span>
      </div>
    </section>

    <section class="grid">
      <div class="pill">MCP<small>接工具</small></div>
      <div class="pill">Skills<small>沉淀流程</small></div>
      <div class="pill">Hooks<small>自动检查</small></div>
      <div class="pill">Subagents<small>专项助手</small></div>
      <div class="pill">Slash<small>快捷命令</small></div>
    </section>

    <section class="action">
      <div class="actionCard">
        <h2>第一步</h2>
        <p>在项目里问：推荐这个仓库该配哪些自动化？</p>
      </div>
      <div class="actionCard">
        <h2>落地策略</h2>
        <p>别全装，先选最痛的 1-2 个配置验证效果。</p>
      </div>
    </section>

    <div class="bottom">不是替你改代码，而是告诉你第一刀该切哪里。</div>
  </main>
</body>
</html>`;

const browser = await chromium.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
});

try {
  const page = await browser.newPage({ viewport: { width: 896, height: 1200 }, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: outputPath, fullPage: false });
  console.log(outputPath);
} finally {
  await browser.close();
}

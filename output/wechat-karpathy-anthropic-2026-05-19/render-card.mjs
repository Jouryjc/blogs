import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const avatarPath = path.join(__dirname, 'assets', 'karpathy-avatar.jpg');
const outputPath = path.join(__dirname, 'images', '01-karpathy-anthropic.png');
const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const avatar = fs.readFileSync(avatarPath).toString('base64');

const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      width: 1080px;
      height: 1350px;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      color: #14202a;
      background:
        radial-gradient(circle at 12% 12%, rgba(88, 141, 174, .24), transparent 28%),
        radial-gradient(circle at 90% 18%, rgba(222, 169, 93, .30), transparent 28%),
        linear-gradient(145deg, #f6f1e8 0%, #e7eef3 47%, #f8f7f3 100%);
    }
    .frame {
      position: relative;
      width: 100%;
      height: 100%;
      padding: 72px;
      overflow: hidden;
    }
    .topline {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 86px;
      font-size: 24px;
      color: #49606f;
      letter-spacing: 0;
    }
    .source {
      display: flex;
      align-items: center;
      gap: 18px;
    }
    .avatar {
      width: 82px;
      height: 82px;
      border-radius: 50%;
      border: 4px solid rgba(255,255,255,.86);
      box-shadow: 0 10px 30px rgba(27, 44, 56, .18);
    }
    .name {
      font-weight: 750;
      color: #1c2d38;
      font-size: 30px;
    }
    .handle {
      margin-top: 4px;
      color: #627584;
      font-size: 22px;
    }
    .date {
      padding: 12px 18px;
      border: 1px solid rgba(34, 58, 72, .14);
      border-radius: 999px;
      background: rgba(255,255,255,.48);
    }
    h1 {
      margin: 0;
      font-size: 92px;
      line-height: 1.08;
      letter-spacing: 0;
      color: #102631;
      max-width: 850px;
    }
    .accent {
      color: #0f4c81;
    }
    .quote {
      margin-top: 42px;
      width: 780px;
      padding-left: 32px;
      border-left: 9px solid #c9893f;
      color: #304552;
      font-size: 34px;
      line-height: 1.42;
      font-weight: 620;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-top: 82px;
    }
    .point {
      min-height: 210px;
      padding: 28px;
      border-radius: 24px;
      background: rgba(255,255,255,.58);
      border: 1px solid rgba(38, 64, 78, .12);
      box-shadow: 0 24px 70px rgba(29, 49, 62, .10);
    }
    .num {
      color: #0f4c81;
      font-size: 25px;
      font-weight: 800;
      margin-bottom: 20px;
    }
    .point p {
      margin: 0;
      color: #213642;
      font-size: 31px;
      line-height: 1.28;
      font-weight: 710;
    }
    .bottom {
      position: absolute;
      left: 72px;
      right: 72px;
      bottom: 58px;
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 46px;
      color: #536a79;
    }
    .takeaway {
      max-width: 690px;
      font-size: 31px;
      line-height: 1.38;
      font-weight: 610;
    }
    .tag {
      width: 196px;
      height: 196px;
      border-radius: 28px;
      background: #102631;
      color: #f9f3e9;
      display: grid;
      place-items: center;
      text-align: center;
      font-size: 30px;
      line-height: 1.2;
      font-weight: 820;
      box-shadow: 0 24px 60px rgba(16, 38, 49, .28);
    }
    .mark {
      position: absolute;
      right: 52px;
      top: 372px;
      width: 222px;
      height: 222px;
      border: 2px solid rgba(15, 76, 129, .22);
      border-radius: 50%;
    }
    .mark::before,
    .mark::after {
      content: "";
      position: absolute;
      border-radius: 999px;
      background: rgba(201, 137, 63, .36);
    }
    .mark::before {
      width: 126px;
      height: 16px;
      left: 47px;
      top: 102px;
      transform: rotate(28deg);
    }
    .mark::after {
      width: 16px;
      height: 126px;
      left: 102px;
      top: 47px;
      transform: rotate(28deg);
    }
  </style>
</head>
<body>
  <main class="frame">
    <div class="topline">
      <div class="source">
        <img class="avatar" src="data:image/jpeg;base64,${avatar}" alt="" />
        <div>
          <div class="name">Andrej Karpathy</div>
          <div class="handle">@karpathy</div>
        </div>
      </div>
      <div class="date">2026.05.19</div>
    </div>

    <div class="mark"></div>

    <h1>Karpathy<br><span class="accent">加入 Anthropic</span></h1>
    <div class="quote">“I've joined Anthropic.”</div>

    <section class="grid">
      <div class="point">
        <div class="num">01</div>
        <p>前沿 LLM 进入关键成形期</p>
      </div>
      <div class="point">
        <div class="num">02</div>
        <p>回到一线研发工作</p>
      </div>
      <div class="point">
        <div class="num">03</div>
        <p>教育方向仍会继续</p>
      </div>
    </section>

    <footer class="bottom">
      <div class="takeaway">这不是普通的人事变动。Anthropic 的研究阵容继续加厚，Claude 及前沿模型研发值得持续关注。</div>
      <div class="tag">AI<br>快讯</div>
    </footer>
  </main>
</body>
</html>`;

const browser = await chromium.launch({
  executablePath: chromePath,
  headless: true,
});
try {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: outputPath, fullPage: false });
  console.log(outputPath);
} finally {
  await browser.close();
}

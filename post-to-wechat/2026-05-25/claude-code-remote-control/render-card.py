from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
IMG_DIR = ROOT / "imgs"
SOURCE = IMG_DIR / "original-thumbnail.jpg"
OUTPUT = IMG_DIR / "01-claude-code-remote-control.png"

W, H = 896, 1200
NAVY = "#10233a"
CREAM = "#fbf5e9"
BLUE = "#d9ecf7"
MINT = "#dff0e6"
YELLOW = "#f6e7b8"
PINK = "#f4dfef"
ORANGE = "#e7863d"
GRAY = "#496074"


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F = {
    "eyebrow": font(24, True),
    "title": font(65, True),
    "subtitle": font(31, True),
    "h": font(30, True),
    "body": font(24, True),
    "small": font(20, True),
    "tiny": font(17, True),
}


def rounded(draw, box, radius, fill, outline=NAVY, width=4):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_text(draw, xy, text, fnt, fill=NAVY, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def text_w(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap(draw, text, fnt, max_width):
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if text_w(draw, trial, fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_width, fill=GRAY, line_gap=7):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw_text(draw, (x, y), line, fnt, fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
    return y


def paste_rounded(base, img, box, radius=28):
    x1, y1, x2, y2 = box
    target_w, target_h = x2 - x1, y2 - y1
    src = img.convert("RGB")
    scale = max(target_w / src.width, target_h / src.height)
    resized = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    cropped = resized.crop((left, top, left + target_w, top + target_h))
    mask = Image.new("L", (target_w, target_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, target_w, target_h), radius=radius, fill=255)
    base.paste(cropped, (x1, y1), mask)


def grid(draw):
    draw.rectangle((0, 0, W, H), fill=CREAM)
    for x in range(0, W, 38):
        draw.line((x, 0, x, H), fill="#eadfce", width=1)
    for y in range(0, H, 38):
        draw.line((0, y, W, y), fill="#eadfce", width=1)


def chip(draw, box, text, fill):
    rounded(draw, box, 18, fill, width=3)
    draw_text(draw, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), text, F["tiny"], NAVY, anchor="mm")


def bullet_card(draw, box, num, title, body, fill):
    rounded(draw, box, 22, fill, width=4)
    draw_text(draw, (box[0] + 20, box[1] + 16), num, F["h"], ORANGE)
    draw_text(draw, (box[0] + 64, box[1] + 16), title, F["h"], NAVY)
    draw_wrapped(draw, (box[0] + 20, box[1] + 55), body, F["small"], box[2] - box[0] - 40)


def main():
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)
    grid(draw)
    draw.rounded_rectangle((5, 5, W - 5, H - 5), radius=42, outline=NAVY, width=9)

    rounded(draw, (52, 48, 302, 102), 28, MINT, width=4)
    draw_text(draw, (76, 63), "Claude Code 新玩法", F["eyebrow"])

    draw_text(draw, (52, 134), "炸裂！手机", F["title"])
    draw_text(draw, (52, 206), "接管 Claude", F["title"])

    rounded(draw, (52, 294, 844, 370), 24, BLUE, width=4)
    draw_text(draw, (78, 313), "电脑开任务，离开工位后手机继续盯进度", F["subtitle"])

    src = Image.open(SOURCE)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((68, 406, 858, 802), radius=28, fill=(16, 35, 58, 38))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(canvas)
    rounded(draw, (52, 392, 844, 786), 30, "#ffffff", width=5)
    paste_rounded(canvas, src, (66, 406, 830, 772), 22)
    draw = ImageDraw.Draw(canvas)

    rounded(draw, (52, 808, 844, 874), 22, YELLOW, width=4)
    draw_text(draw, (78, 826), "核心机制：Claude 仍在你的电脑上跑，手机只是接管会话", F["body"])

    bullet_card(draw, (52, 898, 430, 1016), "1", "怎么用", "终端里启动 Claude Code 任务，再从 Claude App 或网页入口接着看。", BLUE)
    bullet_card(draw, (466, 898, 844, 1016), "2", "适合谁", "长任务、排错、生成 PR、开会/通勤时想继续盯进度的人。", MINT)

    chip(draw, (52, 1038, 300, 1096), "不用守着终端", "#ffffff")
    chip(draw, (324, 1038, 572, 1096), "手机继续追问", PINK)
    chip(draw, (596, 1038, 844, 1096), "电脑别睡眠", "#fde0bd")

    rounded(draw, (52, 1118, 844, 1172), 22, NAVY, outline=NAVY, width=4)
    draw_text(draw, (80, 1134), "第一步：在 Claude Code 里试 /remote-control", F["body"], "#fff7e8")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()

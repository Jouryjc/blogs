from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
IMG_DIR = ROOT / "imgs"
SOURCE = IMG_DIR / "original-deepseek-v4-pro.jpg"
OUTPUT = IMG_DIR / "01-deepseek-v4-pro-1m.png"

W, H = 896, 1200
NAVY = "#10233a"
BLUE = "#d9ecf7"
CREAM = "#fbf5e9"
MINT = "#dff0e6"
YELLOW = "#f6e7b8"
PINK = "#f4dfef"
ORANGE = "#e7863d"
RED = "#d94b4b"
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
    "eyebrow": font(25, True),
    "title": font(64, True),
    "subtitle": font(28, True),
    "h": font(29, True),
    "body": font(23, True),
    "small": font(18, True),
    "code": font(20, True),
}


def rounded(draw, box, radius, fill, outline=NAVY, width=4):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_text(draw, xy, text, fnt, fill=NAVY, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def wrap(draw, text, fnt, max_width):
    lines = []
    cur = ""
    for ch in text:
        trial = cur + ch
        if text_size(draw, trial, fnt)[0] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_width, fill=GRAY, line_gap=8):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw_text(draw, (x, y), line, fnt, fill)
        y += text_size(draw, line, fnt)[1] + line_gap
    return y


def paste_rounded(base, image, box, radius=24):
    x1, y1, x2, y2 = box
    target_w, target_h = x2 - x1, y2 - y1
    src = image.convert("RGB")
    scale = max(target_w / src.width, target_h / src.height)
    resized = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    cropped = resized.crop((left, top, left + target_w, top + target_h))
    mask = Image.new("L", (target_w, target_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, target_w, target_h), radius=radius, fill=255)
    base.paste(cropped, (x1, y1), mask)


def grid_background(draw):
    draw.rectangle((0, 0, W, H), fill=CREAM)
    for x in range(0, W, 38):
        draw.line((x, 0, x, H), fill="#eadfce", width=1)
    for y in range(0, H, 38):
        draw.line((0, y, W, y), fill="#eadfce", width=1)


def pill(draw, box, text, fill, fnt=F["small"]):
    rounded(draw, box, 18, fill, width=3)
    cx = (box[0] + box[2]) // 2
    cy = (box[1] + box[3]) // 2
    draw_text(draw, (cx, cy), text, fnt, NAVY, anchor="mm")


def main():
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)
    grid_background(draw)
    draw.rounded_rectangle((5, 5, W - 5, H - 5), radius=42, outline=NAVY, width=9)

    rounded(draw, (52, 48, 316, 104), 28, MINT, width=4)
    draw_text(draw, (74, 64), "官方更新 · 适合实操", F["eyebrow"])

    draw_text(draw, (52, 138), "炸裂！DeepSeek", F["title"])
    draw_text(draw, (52, 210), "1M 接入", F["title"])

    rounded(draw, (52, 296, 844, 358), 22, BLUE, width=4)
    draw_text(draw, (80, 314), "V4-Pro API：75% OFF 到 2026-05-31 23:59 北京时间", F["subtitle"])

    src = Image.open(SOURCE)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((65, 386, 855, 804), radius=28, fill=(16, 35, 58, 38))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB"))
    rounded(draw, (52, 374, 844, 790), 28, "#ffffff", width=5)
    paste_rounded(canvas, src, (64, 386, 832, 778), 20)
    draw = ImageDraw.Draw(canvas)

    rounded(draw, (52, 810, 844, 866), 20, YELLOW, width=4)
    draw_text(draw, (76, 826), "原图写 5/5；官网现写 5/31，hit 已降到 $0.003625/M", F["body"])

    boxes = [
        ((52, 888, 430, 1010), "Claude Code", "模型设为 deepseek-v4-pro[1m]，走 Anthropic API 格式", BLUE),
        ((466, 888, 844, 1010), "成本窗口", "官网现价：hit $0.003625/M，miss $0.435/M，output $0.87/M", MINT),
    ]
    for box, title, body, fill in boxes:
        rounded(draw, box, 24, fill, width=4)
        draw_text(draw, (box[0] + 22, box[1] + 18), title, F["h"])
        if title == "成本窗口":
            draw_text(draw, (box[0] + 22, box[1] + 58), "现价：hit $0.003625/M", F["small"], GRAY)
            draw_text(draw, (box[0] + 22, box[1] + 86), "miss $0.435/M；output $0.87/M", F["small"], GRAY)
        else:
            draw_wrapped(draw, (box[0] + 22, box[1] + 58), body, F["small"], box[2] - box[0] - 44)

    pill(draw, (52, 1032, 300, 1092), "OpenCode ≥ 1.14.24", "#ffffff")
    pill(draw, (324, 1032, 572, 1092), "OpenClaw ≥ 2026.4.24", PINK)
    pill(draw, (596, 1032, 844, 1092), "先拿 API Key 再跑 claude", "#fde0bd")

    rounded(draw, (52, 1114, 844, 1170), 22, NAVY, outline=NAVY, width=4)
    draw_text(draw, (80, 1130), "第一步：配置 ANTHROPIC_BASE_URL + ANTHROPIC_MODEL", F["body"], "#fff7e8")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
IMG_DIR = ROOT / "imgs"
SOURCE = IMG_DIR / "gemini-remote-control-base.png"
OUTPUT = IMG_DIR / "01-claude-code-remote-control-gemini.png"

W, H = 896, 1200
NAVY = "#10233a"
CREAM = "#fff8ea"
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
    "tag": font(24, True),
    "title": font(50, True),
    "subtitle": font(29, True),
    "h": font(25, True),
    "body": font(20, True),
    "cta": font(25, True),
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


def wrapped(draw, xy, text, fnt, max_width, fill=GRAY, line_gap=6):
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw_text(draw, (x, y), line, fnt, fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap


def fit_cover(img):
    scale = max(W / img.width, H / img.height)
    resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    left = (resized.width - W) // 2
    top = (resized.height - H) // 2
    return resized.crop((left, top, left + W, top + H)).convert("RGB")


def mini_card(draw, box, title, body, fill):
    rounded(draw, box, 20, fill, width=3)
    draw_text(draw, (box[0] + 18, box[1] + 14), title, F["h"], NAVY)
    wrapped(draw, (box[0] + 18, box[1] + 48), body, F["body"], box[2] - box[0] - 36)


def main():
    base = fit_cover(Image.open(SOURCE))
    draw = ImageDraw.Draw(base)

    # Top text panel, aligned to Gemini's blank area.
    rounded(draw, (54, 54, 842, 214), 30, CREAM, width=5)
    rounded(draw, (82, 78, 282, 128), 24, MINT, width=3)
    draw_text(draw, (104, 91), "Claude Code", F["tag"])
    draw_text(draw, (82, 142), "别守终端了：手机接管", F["title"])

    rounded(draw, (54, 238, 842, 304), 22, BLUE, width=4)
    draw_text(draw, (82, 256), "电脑继续跑任务，手机继续看进度、追问、推进", F["subtitle"])

    # Bottom outline panel, aligned to Gemini's blank area.
    rounded(draw, (54, 910, 842, 1148), 28, CREAM, width=5)
    mini_card(draw, (82, 936, 320, 1038), "痛点", "长任务一跑，人就被终端绑住。", BLUE)
    mini_card(draw, (340, 936, 578, 1038), "机制", "Claude 仍在电脑跑，手机接管同一会话。", MINT)
    mini_card(draw, (598, 936, 814, 1038), "适用", "开会、通勤、排错、生成 PR。", PINK)

    rounded(draw, (82, 1064, 814, 1124), 20, NAVY, outline=NAVY, width=3)
    draw_text(draw, (112, 1081), "接下来做：打开 Remote Control，用手机盯长任务", F["cta"], "#fff7e8")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()

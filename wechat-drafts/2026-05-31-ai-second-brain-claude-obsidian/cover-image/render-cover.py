from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "imgs" / "article-cover.png"

W, H = 1080, 458
BG = "#EAF6FF"
BLUE = "#0F4C81"
ORANGE = "#F59E0B"
DARK = "#123047"
INK = "#19384F"
PANEL = "#FFFDF6"
MINT = "#BFE7D2"
PINK = "#FFD6D6"
LAV = "#DCE4FF"

FONT_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def center_text(draw, box, text, fnt, fill):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = left + (right - left - (bbox[2] - bbox[0])) / 2
    y = top + (bottom - top - (bbox[3] - bbox[1])) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def rounded(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Soft grid and sketch lines.
    for x in range(-40, W, 64):
        draw.line((x, 0, x + 180, H), fill="#D4ECFB", width=2)
    for y in range(28, H, 64):
        draw.line((0, y, W, y), fill="#DDEFF8", width=1)

    # Decorative corner objects remain outside the 1:1 center crop.
    rounded(draw, (38, 54, 226, 186), 26, "#DFF4FF", BLUE, 4)
    center_text(draw, (54, 70, 210, 112), "Obsidian", font(27, True), BLUE)
    center_text(draw, (54, 118, 210, 158), "本地 Markdown", font(22), INK)
    for i in range(4):
        y = 205 + i * 28
        draw.line((58, y, 196, y), fill=BLUE, width=3)
        draw.circle((42, y), 5, fill=ORANGE)

    rounded(draw, (858, 64, 1036, 190), 26, "#FFF1C8", ORANGE, 4)
    center_text(draw, (875, 82, 1018, 128), "Claude", font(30, True), DARK)
    center_text(draw, (875, 130, 1018, 166), "检索 / 总结", font(21), INK)
    draw.arc((904, 206, 1014, 316), 20, 330, fill=ORANGE, width=5)
    draw.polygon([(1012, 240), (1030, 242), (1018, 256)], fill=ORANGE)

    # Center safe crop.
    safe_left = (W - H) // 2
    safe_right = safe_left + H
    rounded(draw, (safe_left + 18, 36, safe_right - 18, 338), 34, PANEL, BLUE, 5)
    center_text(draw, (safe_left + 40, 66, safe_right - 40, 118), "别再囤笔记了", font(54, True), DARK)
    center_text(draw, (safe_left + 36, 130, safe_right - 36, 188), "让 Claude 读懂", font(43, True), BLUE)
    center_text(draw, (safe_left + 36, 184, safe_right - 36, 242), "你的 Obsidian", font(43, True), BLUE)

    # Mini workflow in the safe area.
    cards = [
        (safe_left + 54, 270, safe_left + 166, 320, "笔记", MINT),
        (safe_left + 194, 270, safe_left + 306, 320, "链接", LAV),
        (safe_left + 334, 270, safe_left + 446, 320, "工作流", PINK),
    ]
    for x1, y1, x2, y2, label, color in cards:
        rounded(draw, (x1, y1, x2, y2), 16, color, INK, 3)
        center_text(draw, (x1, y1, x2, y2), label, font(24, True), DARK)
    for x in (safe_left + 170, safe_left + 310):
        draw.line((x, 295, x + 22, 295), fill=INK, width=4)
        draw.polygon([(x + 22, 295), (x + 10, 286), (x + 10, 304)], fill=INK)

    rounded(draw, (314, 365, 766, 424), 22, "#FFFFFF", "#7DB7DC", 3)
    center_text(draw, (334, 374, 746, 414), "Markdown · 双链 · Projects · MCP", font(27, True), BLUE)

    # Signature dots and hand-drawn accents.
    for x, y, c in [(276, 56, ORANGE), (790, 44, ORANGE), (836, 340, BLUE), (248, 350, BLUE)]:
        draw.ellipse((x, y, x + 14, y + 14), fill=c)
    draw.line((250, 244, 308, 264, 250, 284), fill="#7DB7DC", width=4)
    draw.line((830, 240, 780, 260, 830, 282), fill="#7DB7DC", width=4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)


if __name__ == "__main__":
    main()

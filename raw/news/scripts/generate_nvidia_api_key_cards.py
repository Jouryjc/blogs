#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "news" / "images" / "2026-04-20-nvidia-key"
FONT_REGULAR = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_ALT = "/System/Library/Fonts/PingFang.ttc"
W, H = 1080, 1440


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT_REGULAR, FONT_ALT):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_canvas():
    img = Image.new("RGB", (W, H), "#0C1220")
    draw = ImageDraw.Draw(img)

    # Soft gradient blocks to avoid a flat background.
    draw.ellipse((-120, -80, 520, 460), fill="#142847")
    draw.ellipse((680, 100, 1260, 680), fill="#102A32")
    draw.rectangle((0, 0, W, H), fill=(0, 0, 0, 40))
    draw.rounded_rectangle((44, 44, W - 44, H - 44), radius=40, outline="#223451", width=2)
    return img, draw


def wrap_text(draw, text, font, max_width):
    lines = []
    current = ""
    for ch in text:
        candidate = current + ch
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_multiline(draw, text, xy, font, fill, max_width, line_gap=10):
    x, y = xy
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def pill(draw, xy, text, fill, text_fill="#EAF4FF"):
    x1, y1, x2, y2 = xy
    font = load_font(28)
    draw.rounded_rectangle(xy, radius=24, fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    tx = x1 + (x2 - x1 - (bbox[2] - bbox[0])) / 2
    ty = y1 + (y2 - y1 - (bbox[3] - bbox[1])) / 2 - 2
    draw.text((tx, ty), text, font=font, fill=text_fill)


def title_block(draw, kicker, title, subtitle):
    pill(draw, (72, 72, 350, 128), kicker, "#163C65")
    draw.text((72, 172), title, font=load_font(72), fill="#F5FAFF")
    draw.text((72, 266), subtitle, font=load_font(34), fill="#93B7D8")


def footer(draw, note):
    draw.line((74, H - 122, W - 74, H - 122), fill="#284766", width=2)
    draw.text((74, H - 94), note, font=load_font(24), fill="#7FA1C2")


def card_one():
    img, draw = make_canvas()
    title_block(draw, "NVIDIA API KEY", "怎么拿？", "按这 5 步操作就行")

    steps = [
        "打开 build.nvidia.com",
        "登录或注册 NVIDIA 账号",
        "进入任意 NIM / 模型页面",
        "点击 Get API Key，再点 Generate Key",
        "复制生成的 key，并立即保存",
    ]

    start_y = 400
    for idx, step in enumerate(steps, start=1):
        cy = start_y + (idx - 1) * 170
        draw.ellipse((90, cy, 170, cy + 80), fill="#76B900")
        nfont = load_font(38)
        nb = draw.textbbox((0, 0), str(idx), font=nfont)
        draw.text((130 - (nb[2] - nb[0]) / 2, cy + 18), str(idx), font=nfont, fill="#081117")

        if idx < len(steps):
            draw.line((130, cy + 80, 130, cy + 170), fill="#315274", width=6)

        box = (210, cy - 12, 968, cy + 110)
        draw.rounded_rectangle(box, radius=28, fill="#101D32", outline="#27496B", width=2)
        draw_multiline(draw, step, (246, cy + 14), load_font(36), "#EAF4FF", 660, line_gap=8)

    footer(draw, "重点：不是单独找后台，而是在模型页里点 Get API Key。")
    return img


def card_two():
    img, draw = make_canvas()
    title_block(draw, "三点提醒", "这 3 点先记住", "流程不长，容易漏的是注册和保存")

    panels = [
        ("注册验证", "注册流程里可能会碰到手机验证码。", "#163C65"),
        ("只显示一次", "Key 通常不会反复展示，先复制再切页面。", "#18403A"),
        ("保存位置", "建议立刻存进密码管理器或安全环境变量。", "#3C2B12"),
    ]

    top = 380
    for i, (head, body, color) in enumerate(panels):
        y1 = top + i * 270
        y2 = y1 + 214
        draw.rounded_rectangle((74, y1, W - 74, y2), radius=34, fill="#101A2A", outline="#264764", width=2)
        pill(draw, (108, y1 + 26, 306, y1 + 78), head, color)
        draw_multiline(draw, body, (110, y1 + 108), load_font(38), "#F4FAFF", 820, line_gap=10)

    draw.rounded_rectangle((74, 1198, W - 74, 1320), radius=30, fill="#132A20", outline="#2E5C45", width=2)
    draw.text((108, 1230), "页面里的关键按钮：", font=load_font(34), fill="#DFF6EA")
    draw.text((108, 1278), "Get API Key  →  Generate Key", font=load_font(42), fill="#76B900")
    footer(draw, "流程很短，但保存 key 这一步最容易漏掉。")
    return img


def code_box(draw, xy, lines):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=28, fill="#0B111A", outline="#2B4D71", width=2)
    font = load_font(32)
    y = y1 + 26
    for line in lines:
        draw.text((x1 + 28, y), line, font=font, fill="#CDE7FF")
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + 16


def card_three():
    img, draw = make_canvas()
    title_block(draw, "拿到后怎么填", "最常见的配置", "先配环境变量，再填通用推理入口")

    code_box(
        draw,
        (74, 386, W - 74, 566),
        [
            "export NVIDIA_API_KEY=<your_key>",
            "",
            "# 建议先在本地 shell / 密钥管理器里保存",
        ],
    )
    code_box(
        draw,
        (74, 612, W - 74, 770),
        [
            "Base URL",
            "https://integrate.api.nvidia.com/v1",
        ],
    )

    draw.rounded_rectangle((74, 826, W - 74, 1242), radius=34, fill="#101A2A", outline="#264764", width=2)
    draw.text((110, 864), "照着这样填就够了", font=load_font(42), fill="#F4FAFF")
    bullets = [
        "环境变量名：NVIDIA_API_KEY",
        "Base URL：https://integrate.api.nvidia.com/v1",
        "先测试能不能通，再接 SDK、CLI 或应用。",
    ]
    y = 944
    for bullet in bullets:
        draw.ellipse((112, y + 10, 132, y + 30), fill="#76B900")
        y = draw_multiline(draw, bullet, (156, y), load_font(34), "#D8E7F7", 760, line_gap=8) + 28

    footer(draw, "一句话：登录 build.nvidia.com，点 Get API Key，生成后马上保存。")
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = [card_one(), card_two(), card_three()]
    for idx, img in enumerate(cards, start=1):
        out = OUT_DIR / f"2026-04-20-nvidia-key-card-{idx}.png"
        img.save(out, quality=95)
        print(out)


if __name__ == "__main__":
    main()

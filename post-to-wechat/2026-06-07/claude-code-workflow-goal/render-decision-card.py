from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "imgs" / "04-decision-matrix.png"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

W, H = 1672, 941
NAVY = "#102A56"
CREAM = "#FBF2DA"
BLUE = "#DCEBFA"
GREEN = "#DDF1E6"
YELLOW = "#FFF0B8"
PINK = "#F6D7D9"
PEACH = "#F8E2C4"


def font(size, index=1):
    return ImageFont.truetype(FONT, size, index=index)


img = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img)

title_font = font(68)
head_font = font(40)
body_font = font(32)
small_font = font(24)
mono_font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 32)


def rounded(xy, fill, width=5, radius=28):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=NAVY, width=width)


def centered(text, box, fnt, fill=NAVY):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 4), text, font=fnt, fill=fill)


draw.rounded_rectangle((86, 54, W - 86, H - 64), radius=34, outline=NAVY, width=6)
centered("怎么选：先看任务痛点", (120, 66, W - 120, 150), title_font)
draw.line((280, 160, W - 280, 160), fill=NAVY, width=5)

cards = [
    ((140, 230, 750, 395), BLUE, "一句话能完成", "用 prompt", "小改动 / 单次解释 / 明确动作"),
    ((920, 230, 1530, 395), GREEN, "多分片并行", "用 workflow", "审计 / 迁移 / 交叉验证"),
    ((140, 470, 750, 635), YELLOW, "单线多轮验收", "用 goal", "测试通过 / 指标达标 / 报告完成"),
    ((920, 470, 1530, 635), PINK, "高风险决策", "plan + 人类确认", "权限 / 支付 / 产品判断"),
]

for box, color, title, action, desc in cards:
    rounded(box, color)
    x1, y1, x2, y2 = box
    draw.text((x1 + 36, y1 + 24), title, font=head_font, fill=NAVY)
    draw.text((x1 + 36, y1 + 78), action, font=body_font, fill=NAVY)
    draw.text((x1 + 36, y1 + 124), desc, font=small_font, fill=NAVY)

draw.line((805, 245, 865, 245), fill=NAVY, width=6)
draw.line((865, 245, 845, 230), fill=NAVY, width=6)
draw.line((865, 245, 845, 260), fill=NAVY, width=6)
draw.line((805, 515, 865, 515), fill=NAVY, width=6)
draw.line((865, 515, 845, 500), fill=NAVY, width=6)
draw.line((865, 515, 845, 530), fill=NAVY, width=6)

rounded((350, 690, 1322, 800), PEACH, width=5, radius=30)
draw.text((410, 718), "workflow = 编排脚本", font=mono_font, fill=NAVY)
draw.text((850, 718), "goal = 完成合同", font=mono_font, fill=NAVY)

rounded((190, 832, W - 190, 895), "#FFF7D8", width=5, radius=24)
centered("规模问题用 workflow，收工问题用 goal。", (190, 832, W - 190, 895), head_font)

for x, y, label in [(235, 200, "1"), (1015, 200, "2"), (235, 440, "3"), (1015, 440, "4")]:
    draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill="#FFFFFF", outline=NAVY, width=4)
    centered(label, (x - 28, y - 28, x + 28, y + 28), small_font)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)
print(OUT)

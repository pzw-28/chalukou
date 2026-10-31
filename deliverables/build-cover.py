from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

root = Path(__file__).parent.parent
W, H = 1920, 1080
img = Image.new('RGB', (W, H), '#0d1b33')
draw = ImageDraw.Draw(img)
for y in range(H):
    ratio = y / H
    draw.line((0, y, W, y), fill=(13 + int(8 * ratio), 27 + int(15 * ratio), 51 + int(25 * ratio)))
for x, y, r in [(1580, 100, 430), (1750, 920, 560), (780, 950, 300)]:
    draw.ellipse((x-r, y-r, x+r, y+r), outline='#1b3965', width=2)

font_dir = Path('C:/Windows/Fonts')
def font(size, bold=False):
    candidates = ['msyhbd.ttc' if bold else 'msyh.ttc', 'simhei.ttf']
    for name in candidates:
        path = font_dir / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

navy = '#0d1b33'
white = '#f5f8ff'
muted = '#a9bad7'
blue = '#6ea8ff'
green = '#55d6a5'

draw.rounded_rectangle((110, 92, 510, 148), radius=26, fill='#17365d')
draw.text((140, 105), 'VIBE CODING · 预指导作品', font=font(25), fill=blue)
draw.text((112, 205), '岔路口', font=font(132, True), fill=white)
draw.text((118, 390), '数字程序算，AI只讲解', font=font(52, True), fill=green)
draw.text((120, 500), '2027 国考职位三态筛选', font=font(37), fill=white)
draw.text((120, 560), '原表行号溯源｜地点变化量与新增职位', font=font(31), fill=muted)

draw.rounded_rectangle((118, 670, 290, 730), radius=24, fill='#2457d6')
draw.text((143, 683), '考公·本版', font=font(25, True), fill=white)
draw.rounded_rectangle((310, 670, 482, 730), radius=24, outline='#536783', width=2)
draw.text((335, 683), '考研·后续', font=font(25), fill=muted)
draw.rounded_rectangle((502, 670, 674, 730), radius=24, outline='#536783', width=2)
draw.text((527, 683), '就业·后续', font=font(25), fill=muted)

shot = Image.open(root / 'evidence' / 'screenshots' / '001-main.png').convert('RGB')
shot = shot.resize((800, 450), Image.Resampling.LANCZOS)
mask = Image.new('L', shot.size, 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle((0, 0, 800, 450), radius=30, fill=255)
shadow = Image.new('RGBA', (860, 510), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.rounded_rectangle((20, 20, 840, 500), radius=38, fill=(0, 0, 0, 95))
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
img.paste(shadow, (950, 190), shadow)
img.paste(shot, (980, 180), mask)
draw = ImageDraw.Draw(img)
draw.rounded_rectangle((978, 178, 1782, 632), radius=32, outline='#4b6eaa', width=2)
draw.text((982, 680), '官方职位表 → 程序判定 → 原表可回查', font=font(29), fill=white)
draw.text((982, 740), '符合 / 不符 / 待确认', font=font(27), fill=green)

draw.line((118, 870, 1780, 870), fill='#29466f', width=2)
draw.text((120, 920), '19,426 条官方职位｜浏览器本地计算｜公开 GitHub', font=font(28), fill=muted)

out = root / 'deliverables' / '岔路口_视频封面.png'
img.save(out)
print(out)

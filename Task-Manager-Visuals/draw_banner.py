#!/usr/bin/env python3
"""Task-Manager wordmark banner: a straight flight from the third step looking
up, cropped tight, every tread in checkered red runner, every riser foot with
its brass rod, the row climbing out of focus toward a landing lit by a green
shaded lamp. A thumb at the left margin has just polished the nearest rod,
which shines harder and carries a faint thumbprint. Halfway up a folded duster
and a polish tin sit on a step. On the landing wall a framed household list
hangs behind glass, too far to read. Task-Manager is lettered on the brass
plate fixed to the bottom riser, Antic capitals in enamel white infill."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W, H = 2560, 640
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
BRASS = (206, 164, 66); RED = (160, 42, 38); WHITE = (240, 238, 228); HERB = (94, 114, 80)
img = Image.new("RGB", (W, H), (70, 62, 52)); d = ImageDraw.Draw(img, "RGBA")
# perspective flight: treads widen toward the viewer (bottom), landing at top centre
cxm = 1420
for i in range(8):
    t = i / 8
    y_top = 560 - i * 64
    half = 1180 - i * 108
    tone = (196 - i * 6, 190 - i * 6, 176 - i * 5)
    d.polygon([(cxm - half, y_top), (cxm + half, y_top), (cxm + half - 108, y_top - 64), (cxm - half + 108, y_top - 64)], fill=tone)
    rh = half - 190
    d.polygon([(cxm - rh, y_top), (cxm + rh, y_top), (cxm + rh - 84, y_top - 64), (cxm - rh + 84, y_top - 64)], fill=RED)
    if i % 2 == 0:
        d.polygon([(cxm - 60, y_top - 6), (cxm + 60, y_top - 6), (cxm + 40, y_top - 52), (cxm - 40, y_top - 52)], fill=(242, 236, 216, 90))
    ry = y_top - 8
    bright = 240 - i * 10
    rod = (bright, int(bright * 0.8), int(bright * 0.32))
    rw = max(5, 13 - i)
    d.line([(cxm - rh + 30, ry), (cxm + rh - 30, ry)], fill=rod, width=rw)
    for kx in (cxm - rh + 22, cxm + rh - 22):
        d.ellipse([kx - rw, ry - rw, kx + rw, ry + rw], fill=rod)
# green shaded landing lamp and its glow
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
ld.ellipse([cxm - 260, 0, cxm + 260, 190], fill=(255, 214, 120, 70))
img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(24))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
d.polygon([(cxm - 90, 26), (cxm + 90, 26), (cxm + 130, 84), (cxm - 130, 84)], fill=(52, 104, 62))
d.rectangle([cxm - 6, 0, cxm + 6, 26], fill=(40, 38, 34))
# framed household list on the landing wall, behind glass, unreadable by distance
d.rectangle([290, 60, 560, 300], fill=(52, 46, 38)); d.rectangle([306, 76, 544, 284], fill=(238, 234, 218))
for ly in range(104, 268, 26):
    d.line([(330, ly), (520, ly)], fill=(170, 166, 154), width=4)
d.polygon([(306, 284), (430, 76), (500, 76), (376, 284)], fill=(255, 255, 255, 36))
# duster and polish tin halfway up, on the fourth tread edge
d.polygon([(2060, 300), (2180, 300), (2152, 262), (2088, 262)], fill=(228, 224, 206))
d.rectangle([2210, 282, 2266, 302], fill=(206, 202, 190)); d.rectangle([2216, 274, 2260, 282], fill=(140, 138, 130))
# thumb at the left margin, just polished the nearest rod
d.polygon([(0, 470), (120, 452), (168, 486), (150, 540), (40, 566), (0, 556)], fill=(206, 168, 132))
d.ellipse([118, 462, 168, 512], fill=(220, 186, 150))
# brass plate on the bottom riser with the name in enamel white infill
d.rectangle([cxm - 330, 566, cxm + 330, 626], fill=(168, 128, 48))
d.rectangle([cxm - 330, 566, cxm + 330, 626], outline=(120, 88, 30), width=4)
for sx in (cxm - 306, cxm + 282):
    d.ellipse([sx, 588, sx + 16, 604], fill=(90, 66, 24))
f = ImageFont.truetype("fonts/Antic.ttf", 44 if v == "ship" else 30)
txt = "TASK-MANAGER"; tw = d.textlength(txt, font=f)
d.text(((W - tw) / 2 + 60, 574), txt, font=f, fill=WHITE)
rng = np.random.default_rng(6); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "banner.png" if v == "ship" else f"scratch/banner-{v}.png"
img.save(out); print(out)

#!/usr/bin/env python3
"""Task-Manager logo: one brass stair rod held horizontally end to end, its two
finial knobs and the pair of small eye brackets that pin it to the tread, over
a narrow slice of checkered red runner cut off top and bottom. Three inks:
brass, checkered red, kitchen enamel white. Name beneath in Antic, letter
spaced, brass, like a maker's plate. At 64px the lettering goes and the rod
with its two knobs remains."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
W = H = 1024
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
BRASS = (198, 156, 62); COPPER = (150, 92, 52); RED = (164, 44, 40); WHITE = (242, 240, 232)
img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img, "RGBA")
# runner slice across the middle, cut off top and bottom of the rod zone
d.rectangle([0, 300, W, 560], fill=RED)
for i, cx in enumerate(range(0, W, 84)):
    if i % 2 == 0:
        d.rectangle([cx, 316, cx + 42, 358], fill=(242, 236, 216, 130))
        d.rectangle([cx, 502, cx + 42, 544], fill=(242, 236, 216, 130))
    else:
        d.rectangle([cx, 400, cx + 42, 442], fill=(242, 236, 216, 110))
# the rod, horizontal, with copper shadow line under the brass
ry = 430
lw = 22 if v == "v1" else 34
d.line([(120, ry + 10), (904, ry + 10)], fill=COPPER, width=lw)
d.line([(120, ry), (904, ry)], fill=BRASS, width=lw)
d.line([(120, ry - lw // 3), (904, ry - lw // 3)], fill=(240, 214, 130), width=max(4, lw // 4))
kr = 26 if v == "v1" else 40
d.ellipse([120 - kr, ry - kr, 120 + kr, ry + kr], fill=BRASS, outline=COPPER, width=5)
d.ellipse([904 - kr, ry - kr, 904 + kr, ry + kr], fill=BRASS, outline=COPPER, width=5)
for bxx in (330, 694):  # eye brackets pinning rod to tread, enamel showing at the screw hole
    d.ellipse([bxx - 24, ry - 24, bxx + 24, ry + 24], outline=(96, 74, 30), width=8)
    d.ellipse([bxx - 6, ry - 6, bxx + 6, ry + 6], fill=WHITE)
if v != "v1":
    f = ImageFont.truetype("fonts/Antic.ttf", 84)
    txt = "T a s k - M a n a g e r"; tw = d.textlength(txt, font=f)
    if tw > W - 80:
        f = ImageFont.truetype("fonts/Antic.ttf", 64); tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, 660), txt, font=f, fill=(146, 110, 40))
rng = np.random.default_rng(4); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "logo.png" if v == "ship" else f"scratch/logo-{v}.png"
img.save(out); print(out)
img.resize((64, 64), Image.LANCZOS).save(f"scratch/logo64-{v}.png"); print("64px saved")

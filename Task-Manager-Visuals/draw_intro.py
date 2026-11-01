#!/usr/bin/env python3
"""Task-Manager intro banner, side profile of the flight, no writing anywhere.
The staircase is drawn as a stepped profile climbing from bottom left to the
landing at top right: pale painted treads, a checkered red runner draped over
the profile and worn paler at the centre of the lowest treads, one brass rod
at every riser foot with eye brackets and finial knobs, the second rod from
the bottom crooked by a few degrees, the lowest rod bright with a thumbprint
shine, a duster over the newel post, a polish tin and folded cloth on the
fifth step, herb wall above the stringer, lamplight at the landing turn."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
W, H = 1600, 900
v = sys.argv[1] if len(sys.argv) > 1 else "ship"
BRASS = (206, 164, 66); COPPER = (150, 92, 52); RED = (160, 42, 38); PALE = (198, 116, 100)
WHITE = (238, 236, 226); HERB = (94, 114, 80)
img = Image.new("RGB", (W, H), HERB); d = ImageDraw.Draw(img, "RGBA")
# hall window light, cool, off frame left: a soft cool wash low left
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
ld.polygon([(0, 300), (420, 430), (300, 900), (0, 900)], fill=(210, 226, 235, 44))
ld.polygon([(1240, 0), (1600, 0), (1600, 300), (1150, 190)], fill=(255, 206, 110, 92))  # landing lamp warmth
img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(22))).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# stair profile: 9 steps, run 158, rise 74, starting bottom left
X0, YBASE, RUN, RISE, N = 90, 838, 158, 74, 9
pts = [(X0, 900), (X0, YBASE)]
for i in range(N):
    pts.append((X0 + (i + 1) * RUN, YBASE - i * RISE))
    pts.append((X0 + (i + 1) * RUN, YBASE - (i + 1) * RISE))
pts += [(1600, YBASE - N * RISE), (1600, 900)]
d.polygon(pts, fill=(70, 58, 46))
# skirting board following the profile, enamel white
sk = []
for i in range(N + 1):
    sk.append((X0 + i * RUN, YBASE - i * RISE - 26))
d.line(sk, fill=WHITE, width=16)
# each tread top in pale painted wood, riser face darker
for i in range(N):
    x = X0 + i * RUN; y = YBASE - i * RISE
    d.rectangle([x, y - 10, x + RUN, y], fill=(232, 228, 216))
    d.rectangle([x + RUN - 10, y, x + RUN, y + RISE], fill=(120, 104, 84))
# runner draped over the profile: stepped red band inset from both edges
def runner_path(inset):
    p = []
    for i in range(N):
        x = X0 + i * RUN + inset; y = YBASE - i * RISE - 4
        p.append((x, y)); p.append((x + RUN - inset * 0 - 6, y))
        p.append((x + RUN - 6, y - RISE + 8))
    return p
rp = runner_path(30)
d.line(rp, fill=RED, width=44, joint="curve")
if v == "ship":  # worn paler centre only on the lowest treads
    wp = [(X0 + 62, YBASE - 4), (X0 + RUN - 8, YBASE - 4), (X0 + RUN - 8, YBASE - RISE + 4), (X0 + 2 * RUN - 8, YBASE - RISE - 4), (X0 + 2 * RUN - 8, YBASE - 2 * RISE + 4)]
    d.line(wp, fill=PALE, width=18, joint="curve")
for i in range(N):  # check notches along the runner
    x = X0 + i * RUN + 52; y = YBASE - i * RISE - 26
    if i % 2 == 0:
        d.rectangle([x, y, x + 13, y + 13], fill=(240, 232, 214, 110))
# brass rods at every riser foot
for i in range(N):
    x = X0 + i * RUN; y = YBASE - i * RISE + RISE - 16
    crooked = (i == 1 and v == "ship")
    tilt = -8 if crooked else 0
    bright = 232 if i == 0 else max(150, 210 - i * 8)
    rod = (bright, int(bright * 0.8), int(bright * 0.32))
    rx0, rx1 = x + 22, x + RUN - 16
    d.line([(rx0, y + tilt), (rx1, y - tilt)], fill=COPPER, width=11)
    d.line([(rx0, y + tilt), (rx1, y - tilt)], fill=rod, width=7)
    d.ellipse([rx0 - 13, y + tilt - 8, rx0 + 3, y + tilt + 8], fill=rod)
    d.ellipse([rx1 - 3, y - tilt - 8, rx1 + 13, y - tilt + 8], fill=rod)
    for bxx, byy in ((rx0 + 22, y + tilt * 0.7), (rx1 - 22, y - tilt * 0.7)):
        d.ellipse([bxx - 7, byy - 7, bxx + 7, byy + 7], outline=(88, 68, 28), width=3)
    if i == 0 and v == "ship":
        d.ellipse([x + 66, y - 5, x + 102, y + 5], fill=(255, 242, 196, 200))  # thumbprint shine
# polish tin and folded cloth resting on the fifth tread (i=4)
fx = X0 + 4 * RUN + 18; fy = YBASE - 4 * RISE - 12
d.rectangle([fx, fy - 16, fx + 58, fy], fill=(206, 202, 190)); d.rectangle([fx + 4, fy - 23, fx + 54, fy - 16], fill=(140, 138, 130))
d.polygon([(fx + 74, fy), (fx + 132, fy), (fx + 118, fy - 18), (fx + 86, fy - 18)], fill=(228, 224, 206))
# landing: plant pot and chair back just visible past the turn
d.ellipse([1330, 96, 1426, 168], fill=(50, 72, 42)); d.rectangle([1364, 160, 1392, 218], fill=(122, 76, 44))
d.rectangle([1470, 130, 1570, 268], outline=(42, 38, 32), width=10)
# handrail on balusters following the flight, newel post with duster at base
hr = [(X0 - 18, YBASE - 300), (X0 + N * RUN - 60, YBASE - N * RISE - 300)]
d.line(hr, fill=(86, 62, 36), width=17)
for i in range(1, N):
    bx = X0 + i * RUN - 30; by = YBASE - i * RISE
    d.line([(bx, by - 292 + i * 2), (bx, by - 6)], fill=(104, 78, 46), width=8)
d.rectangle([30, 430, 92, 880], fill=(84, 60, 36)); d.ellipse([20, 402, 102, 452], fill=(102, 74, 42))
d.polygon([(44, 452), (146, 452), (124, 548), (94, 606), (62, 548)], fill=(228, 222, 200))
d.polygon([(44, 452), (146, 452), (136, 486), (54, 486)], fill=(242, 238, 220))
rng = np.random.default_rng(8); a = np.asarray(img).astype(np.int16); n = rng.normal(0, 4, a.shape[:2])[..., None]
img = Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8))
out = "intro-banner.png" if v == "ship" else f"scratch/intro-{v}.png"
img.save(out); print(out)

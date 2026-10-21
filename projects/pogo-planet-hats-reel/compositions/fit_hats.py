# Seats each hat on the head individually (body.png coords).
# Hats: the centroid of the brim (lowest band of the hat) is pinned just above the head centre,
# and the hat is scaled by its brim width. Masks/animal heads: whole-shape centroid on the head centre.
import json, os, sys
import numpy as np
from PIL import Image
HEAD_CX, HEAD_CY, HEAD_D = 217, 75, 62
MASK = {9, 10, 11} | set(range(16, 29))           # h29 crab is worn like a hat in-game
TUNE = {6: dict(scale=0.9), 9: dict(dx=-8), 29: dict(drop=-9), 13: dict(dx=6), 12: dict(drop=4), 3: dict(drop=-3), 1: dict(dx=6), 2: dict(dx=5), 8: dict(dx=6)}
S = 3
os.makedirs("img/hatfit", exist_ok=True)

def alpha(img): return np.asarray(img.getchannel("A")) > 40

info = {}
for i in range(30):
    h = Image.open(f"img/hats/h{i:02d}.png").convert("RGBA")
    h = h.crop(h.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox())
    a = alpha(h); ys, xs = np.nonzero(a); hgt = ys.max() - ys.min() + 1
    t = TUNE.get(i, {})
    if i in MASK:
        k = 96 / h.width * t.get("scale", 1); rot = -8
    else:
        band = a[int(ys.max() - 0.18 * hgt):]                # bottom 18 % = brim
        brim_w = np.ptp(np.nonzero(band.any(0))[0]) + 1
        k = min(1.3 * HEAD_D / brim_w, 96 / max(h.size)) * t.get("scale", 1); rot = -10
    hs = h.resize((round(h.width * k * S), round(h.height * k * S)), Image.LANCZOS).rotate(rot, expand=True, resample=Image.BICUBIC)
    A = alpha(hs); ys, xs = np.nonzero(A)
    if i in MASK:
        cx, cy = xs.mean() / S, ys.mean() / S
        tx, ty = HEAD_CX + 2 + t.get("dx", 0), HEAD_CY - 4
    else:
        cut = ys.max() - 0.18 * (ys.max() - ys.min())
        sel = ys >= cut
        cx, cy = xs[sel].mean() / S, ys[sel].mean() / S
        tx, ty = HEAD_CX + 3 + t.get("dx", 0), HEAD_CY + 15 + t.get("drop", 0)   # hat sits low: only the lower third of the head shows
    hs.save(f"img/hatfit/h{i:02d}.png")
    info[f"img/hats/h{i:02d}.png"] = (round(tx - cx, 1), round(ty - cy, 1), round(hs.width / S, 1), round(hs.height / S, 1))
json.dump(info, open("hatfit.json", "w"))

if len(sys.argv) > 1:   # review sheet: every hat on the head
    from PIL import ImageDraw
    b = Image.open("img/body.png").convert("RGBA")
    out = Image.new("RGBA", (10 * 180, 3 * 190), (150, 170, 120, 255)); d = ImageDraw.Draw(out)
    for i in range(30):
        cv = Image.new("RGBA", (330, 420), (0, 0, 0, 0)); cv.alpha_composite(b, (0, 60))
        l, tp, W, H = info[f"img/hats/h{i:02d}.png"]
        hi = Image.open(f"img/hatfit/h{i:02d}.png").resize((round(W), round(H)), Image.LANCZOS)
        cv.alpha_composite(hi, (round(l), round(tp) + 60))
        out.alpha_composite(cv.crop((130, 0, 310, 190)), ((i % 10) * 180, (i // 10) * 190))
        d.text(((i % 10) * 180 + 4, (i // 10) * 190 + 4), f"h{i:02d}", fill=(0, 0, 0, 255))
    out.save(sys.argv[1])

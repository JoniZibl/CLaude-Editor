# Crops each hat to its opaque bounds and computes its placement on the head (body.png coords).
import json, os, sys
from PIL import Image
HEAD_CX, HEAD_CY, HEAD_D = 217, 75, 62
MASK = {9, 10, 11} | set(range(16, 30))
os.makedirs("img/hatfit", exist_ok=True)
info = {}
for i in range(30):
    h = Image.open(f"img/hats/h{i:02d}.png").convert("RGBA")
    h = h.crop(h.getchannel("A").point(lambda a: 255 if a > 20 else 0).getbbox())
    mask = i in MASK
    w = 108 if mask else 96                       # opaque width in body px
    S = 3                                        # bake at 3x for sharpness
    hs = h.resize((w * S, round(h.height * w / h.width) * S), Image.LANCZOS)
    rot = -8 if mask else -12
    hs = hs.rotate(rot, expand=True, resample=Image.BICUBIC)
    hs.save(f"img/hatfit/h{i:02d}.png")
    W, H = hs.width / S, hs.height / S
    if mask:   # centred on the head
        left, top = HEAD_CX - W / 2 + 4, HEAD_CY - H / 2 - 2
    else:      # opaque bottom sits just below head centre, covering the crown of the head
        left, top = HEAD_CX - W / 2 + 6, HEAD_CY + 8 - H
    info[f"img/hats/h{i:02d}.png"] = (round(left, 1), round(top, 1), round(W, 1), round(H, 1))
json.dump(info, open("hatfit.json", "w"))
if len(sys.argv) > 1:   # preview sheet
    b = Image.open("img/body.png").convert("RGBA"); s = Image.open("img/stick.png").convert("RGBA")
    picks = [0, 3, 4, 5, 8, 13, 14, 11, 16, 29, 18, 26]
    out = Image.new("RGBA", (len(picks) * 150, 170), (150, 170, 120, 255))
    for k, i in enumerate(picks):
        cv = Image.new("RGBA", (330, 420), (0, 0, 0, 0)); cv.alpha_composite(s, (10, 89)); cv.alpha_composite(b, (0, 40))
        l, t, W, H = info[f"img/hats/h{i:02d}.png"]
        hi = Image.open(f"img/hatfit/h{i:02d}.png").resize((round(W), round(H)), Image.LANCZOS)
        cv.alpha_composite(hi, (round(l), round(t) + 40))
        out.alpha_composite(cv.crop((130, 0, 310, 200)).resize((150, 167)), (k * 150, 0))
    out.save(sys.argv[1])

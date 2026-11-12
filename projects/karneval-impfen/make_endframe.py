"""Blue gradient endframe: pin + headline + phone. Writes PNG frames to endframe_frames/."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = Path(__file__).parent
OUT = D / "endframe_frames"; OUT.mkdir(exist_ok=True)
W, H, FPS, DUR = 1080, 1920, 30, 3.96
FONT = "/usr/share/fonts/truetype/inter/InterDisplay-Black.ttf"
LINES = ["Impftermin in", "deiner Apotheke –", "jetzt in der", "iA.de-App buchen!"]
FS, LH, TOP = 94, 112, 360

def find_font():
    import subprocess
    p = subprocess.run(["fc-match", "-f", "%{file}", "Inter Display:black"], capture_output=True, text=True).stdout
    return p or FONT
font = ImageFont.truetype(find_font(), FS)

# gradient background (light teal top-left -> deep teal bottom-right)
c1, c2 = (122, 196, 212), (18, 104, 128)
bg = Image.new("RGB", (W, H))
px = bg.load()
for y in range(H):
    for x in range(0, W):
        t = min(max((x / W) * 0.35 + (y / H) * 0.65, 0), 1)
        px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
bg = bg.convert("RGBA")

pin = Image.open(D / "assets/ia_pin.png").convert("RGBA").resize((150, 150), Image.LANCZOS)
phone = Image.open(D / "assets/phone_cut.png").convert("RGBA")
ph_s = 1.75
phone = phone.resize((int(phone.width * ph_s), int(phone.height * ph_s)), Image.LANCZOS)
phone = phone.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
# soft drop shadow
sh = Image.new("RGBA", (phone.width + 80, phone.height + 80), (0, 0, 0, 0))
sh.paste((0, 0, 0, 90), (40, 40), phone.split()[3])
sh = sh.filter(ImageFilter.GaussianBlur(22))

def ease_out(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def ease_back(t, s=1.4):
    t = min(max(t, 0), 1) - 1; return t * t * ((s + 1) * t + s) + 1

def text_layer(text):
    bb = font.getbbox(text)
    im = Image.new("RGBA", (bb[2] + 20, bb[3] + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); d.text((10, 5), text, font=font, fill=(255, 255, 255, 255))
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    shadow.paste((0, 40, 60, 70), (0, 0), im.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(shadow, (0, 4)); out.alpha_composite(im)
    return out
texts = [text_layer(l) for l in LINES]

def with_alpha(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a))); return im

for f in range(int(DUR * FPS)):
    t = f / FPS
    fr = bg.copy()
    # pin pop
    p = (t - 0.25) / 0.4
    if p > 0:
        sc = 0.6 + 0.4 * ease_back(p, 2.0)
        sz = max(int(150 * sc), 1)
        pi = with_alpha(pin.resize((sz, sz), Image.LANCZOS), ease_out(p * 2))
        fr.alpha_composite(pi, ((W - sz) // 2, 175 + (150 - sz) // 2))
    # headline lines
    for i, tl in enumerate(texts):
        p = (t - 0.45 - 0.12 * i) / 0.4
        if p <= 0: continue
        e = ease_out(p)
        fr.alpha_composite(with_alpha(tl, e), ((W - tl.width) // 2, int(TOP + i * LH + 40 * (1 - e))))
    # phone fly-in + float
    p = (t - 0.85) / 0.7
    if p > 0:
        y0 = 850 + int(700 * (1 - ease_back(p, 1.2))) + int(6 * math.sin((t - 1.55) * 2.4) if t > 1.55 else 0)
        x0 = (W - phone.width) // 2
        a = ease_out(p * 1.6)
        fr.alpha_composite(with_alpha(sh, a), (x0 - 40 + 10, y0 - 40 + 24))
        fr.alpha_composite(with_alpha(phone, a), (x0, y0))
    fr.convert("RGB").save(OUT / f"f_{f:04d}.png")
print("frames:", f + 1)

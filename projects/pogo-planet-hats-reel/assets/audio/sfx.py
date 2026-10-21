# Layered stereo SFX for the hats reel, timed to the composition's beat grid.
# Each sound = transient + body + tail, then a shared stereo room reverb.
import numpy as np, wave, pathlib
SR = 44100; N = SR * 15; rng = np.random.default_rng(3)
L = np.zeros(N); R = np.zeros(N)
B = lambda k: -0.0146 + k * 60 / 139.67
tt = lambda d: np.arange(int(SR * d)) / SR

def lp(x, fc):                       # one-pole low-pass (fc may be an array)
    a = 1 - np.exp(-2 * np.pi * np.asarray(fc) / SR) * np.ones(len(x))
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def hp(x, fc): return x - lp(x, fc)
def add(sig, t, g, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    L[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 - pan)); R[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 + pan))

def pop(p=1.0):        # bubbly "plop": pitched body with fast downward glide + click
    t = tt(0.18); f = (300 + 1400 * np.exp(-t * 55)) * p
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28)
    click = hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 400) * 0.35
    return np.tanh((body + click) * 1.4) * 0.8
def sparkle():          # bell-like FM shimmer for the crown
    t = tt(1.6); out = np.zeros(len(t))
    for k, (f, d) in enumerate([(1568, 0), (2093, .05), (2637, .1), (3136, .15)]):
        tk = np.clip(t - d, 0, None); env = (t >= d) * np.exp(-tk * 3.2)
        out += np.sin(2 * np.pi * f * tk + 1.8 * np.sin(2 * np.pi * f * 3.5 * tk) * np.exp(-tk * 6)) * env
    return out * 0.3
def impact(big=False):  # sub drop + punch + crack
    d = 1.2 if big else 0.7; t = tt(d)
    sub = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 14)) / SR) * np.exp(-t * (2.5 if big else 5))
    punch = np.sin(2 * np.pi * np.cumsum(110 + 300 * np.exp(-t * 60)) / SR) * np.exp(-t * 25) * 0.6
    crack = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 45) * 0.9
    return np.tanh((sub * 1.2 + punch + crack) * 1.3)
def whoosh(d=0.45):     # band-passed noise sweep, rising cutoff
    t = tt(d); n = rng.standard_normal(len(t)); fc = 300 + 5000 * (t / d) ** 2
    y = hp(lp(n, fc), 150) * np.sin(np.pi * t / d) ** 2
    return y / np.max(np.abs(y))
def riser(d=1.2):       # tension riser into the crown hit
    t = tt(d); n = lp(rng.standard_normal(len(t)), 400 + 6000 * (t / d) ** 2)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 600 * (t / d) ** 2) / SR) * 0.25
    return (n * 0.6 + tone) * (t / d) ** 2.5
def jump():             # soft pogo spring: short rising chirp + body
    t = tt(0.22); f = 250 + 900 * (t / 0.22) ** 0.7
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) * (1 - np.exp(-t * 400)) * 0.7
def tick():             # counter tick
    t = tt(0.03); return hp(rng.standard_normal(len(t)), 4000) * np.exp(-t * 300) * 0.5

swaps = [B(k) for k in range(5, 9)] + [B(9 + k / 2) for k in range(8)] + [B(13 + k / 4) for k in range(20)]
for i, t in enumerate(swaps):
    add(pop(0.85 + 0.012 * i), t, 0.42 - 0.004 * i, pan=0.25 * np.sin(i * 1.7))
add(riser(1.4), B(18) - 1.4, 0.35)
add(impact(True), B(18), 0.9); add(sparkle(), B(18.4), 0.55, 0.15)
for t in [B(1), B(22), B(29)]: add(impact(False), t, 0.7)
add(impact(True), B(31), 0.95)
for k in range(54): add(pop(1.2 + 0.015 * (k % 9)), B(20) + 0.012 * k, 0.09, pan=((k % 6) - 2.5) / 3)
for t in [B(26), B(31)]: add(whoosh(), t - 0.4, 0.45, -0.3)
add(whoosh(0.35), B(5) - 0.35, 0.3, 0.3)
for k in range(3): add(jump(), B(26 + k), 0.4, (k - 1) * 0.5)
add(pop(0.75), B(32), 0.7)

# shared room reverb (decaying stereo noise IR), mixed in at low level
ir_t = tt(1.1); irL = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 5); irR = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 5)
irL, irR = lp(irL, 5000), lp(irR, 5000)
conv = lambda x, ir: np.fft.irfft(np.fft.rfft(x, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]
wetL, wetR = conv(L, irL), conv(R, irR)
g = 0.18 * np.max(np.abs(L)) / np.max(np.abs(wetL))
outL, outR = L + wetL * g, R + wetR * g
m = max(np.max(np.abs(outL)), np.max(np.abs(outR)))
st = (np.stack([outL, outR], 1) / m * 0.9 * 32767).astype("<i2")
f = wave.open(str(pathlib.Path(__file__).with_name("sfx.wav")), "wb"); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()

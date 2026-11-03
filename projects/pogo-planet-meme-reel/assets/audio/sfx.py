# Trailer-parody SFX for the "change your life" reel: braams, impacts, scratch, silence, dry pop. No music.
import numpy as np, wave, pathlib
SR = 44100; END = 11.0; N = int(SR * END); rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)
tt = lambda d: np.arange(int(SR * d)) / SR
def env(t, a, d): return (1 - np.exp(-t / a)) * np.exp(-t / d)
def lp(x, fc):
    a = 1 - np.exp(-2 * np.pi * np.asarray(fc) / SR) * np.ones(len(x)); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def add(sig, t, g, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if j <= i: return
    L[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 - pan)); R[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 + pan))
def braam(f=55, d=1.4):   # brassy trailer hit: detuned saws, low-passed
    t = tt(d); saw = lambda ff: 2 * ((t * ff) % 1) - 1
    x = saw(f) + saw(f * 1.006) + 0.6 * saw(f * 2) + 0.4 * saw(f * 1.498)
    return np.tanh(lp(x, 600 * np.exp(-t * 1.5) + 180) * 1.2) * env(t, 0.03, 0.55)
def thump(f0=48, d=0.3):
    t = tt(1.0); return np.sin(2 * np.pi * np.cumsum(f0 + 50 * np.exp(-t * 22)) / SR) * env(t, 0.003, d)
def hit():   # montage cut impact
    t = tt(0.6); return thump(46, 0.22)[:len(t)] * 1.0 + lp(rng.standard_normal(len(t)), 1800) * np.exp(-t * 40) * 0.5
def rise(d):
    t = tt(d); return lp(rng.standard_normal(len(t)), 300 + 5000 * (t / d) ** 2) * (t / d) ** 2.2 * 0.5
def tick():
    t = tt(0.04); return np.sin(2 * np.pi * 2400 * t) * env(t, 0.0005, 0.008)
def shimmer():
    t = tt(1.2); return sum(np.sin(2 * np.pi * f * t) * env(np.clip(t - d, 0, None), .003, .5) * (t >= d) for f, d in ((1568, 0), (2093, .06), (2637, .12), (3136, .18))) / 4
def scratch():
    t = tt(0.4); f = 1100 * np.exp(-t * 6) + 150 * np.sin(2 * np.pi * 10 * t)
    return np.tanh(lp(rng.standard_normal(len(t)), 3500) * 0.4 + np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 4)
def pop():
    t = tt(0.12); return np.sin(2 * np.pi * np.cumsum(700 * np.exp(-t * 35) + 250) / SR) * env(t, 0.001, 0.03)
def boing():
    t = tt(0.3); f = 220 + 900 * (t / 0.3) ** 0.7; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(t, 0.003, 0.08)
# intro: one braam per line, rising tension
for t, f in [(0.15, 55), (0.65, 49), (1.05, 41)]: add(braam(f, 1.4), t, 0.55); add(thump(42, 0.35), t, 0.6)
add(rise(0.6), 0.9, 0.5)
# montage cuts
for k, c in enumerate([1.5, 2.5, 3.5, 4.5, 5.5]): add(hit(), c, 0.9, (-.2, .2, 0, -.2, .2)[k]); add(braam(41 + 3 * k, 0.9), c, 0.35)
for k in range(12): add(tick(), 2.54 + k * 0.075, 0.35, 0.3 * np.sin(k))
add(shimmer(), 3.55, 0.5)
add(thump(36, 0.5), 4.75, 1.0)
for k in range(4): add(thump(60 - 6 * k, 0.12), 5.58 + k * 0.16, 0.6)
add(rise(0.9), 5.6, 0.45)
# freeze: record scratch, then dead silence; dry pop on the punchline
add(scratch(), 6.5, 0.75)
add(pop(), 7.65, 0.5)
# then you play again
add(boing(), 9.0, 0.5); add(hit(), 9.35, 0.7)
for k in range(4): add(boing(), 9.4 + 0.5 * (k + 1), 0.3)
fade = np.ones(N); n = int(SR * 0.3); fade[-n:] = np.linspace(1, 0, n); L *= fade; R *= fade
ir_t = tt(1.2); irL = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 4), 4000); irR = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 4), 4000)
conv = lambda x, ir: np.fft.irfft(np.fft.rfft(x, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]
wl, wr = conv(L, irL), conv(R, irR); g = .18 * np.max(np.abs(L)) / np.max(np.abs(wl))
# keep the punchline dry: no reverb tail from 6.9 s on except after 9 s
mask = np.ones(N); mask[int(6.9 * SR):int(9.0 * SR)] = 0
oL, oR = L + wl * g * mask, R + wr * g * mask; m = max(np.abs(oL).max(), np.abs(oR).max())
st = (np.stack([oL, oR], 1) / m * .9 * 32767).astype("<i2")
f = wave.open(str(pathlib.Path(__file__).with_name("sfx.wav")), "wb"); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()

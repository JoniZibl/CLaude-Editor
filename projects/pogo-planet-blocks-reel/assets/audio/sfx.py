# Layered stereo SFX for the block-chaos reel, timed to the beat grid of "Clowns" (120.19 BPM from 0:16.52).
import numpy as np, wave, pathlib
SR = 44100; N = SR * 15; rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N); P = 60 / 120.19; B = lambda k: k * P
tt = lambda d: np.arange(int(SR * d)) / SR
def lp(x, fc):
    a = 1 - np.exp(-2 * np.pi * np.asarray(fc) / SR) * np.ones(len(x)); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def hp(x, fc): return x - lp(x, fc)
def add(sig, t, g, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    L[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 - pan)); R[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 + pan))
def clack(p=1.0):      # wooden block placed: knock + short resonant body
    t = tt(0.25); body = sum(np.sin(2 * np.pi * f * p * t) * np.exp(-t * d) for f, d in [(320, 30), (780, 45), (1650, 70)])
    return np.tanh((body * 0.6 + hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 250) * 0.6) * 1.5)
def impact(big=False):
    d = 1.1 if big else 0.6; t = tt(d)
    sub = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 14)) / SR) * np.exp(-t * (2.5 if big else 5))
    crack = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 45) * 0.9
    return np.tanh((sub * 1.2 + crack + np.sin(2 * np.pi * np.cumsum(110 + 300 * np.exp(-t * 60)) / SR) * np.exp(-t * 25) * .6) * 1.3)
def whoosh(d=0.4):
    t = tt(d); fc = 300 + 5000 * (t / d) ** 2; y = hp(lp(rng.standard_normal(len(t)), fc), 150) * np.sin(np.pi * t / d) ** 2
    return y / np.max(np.abs(y))
def rumble(d=0.7):     # block falling away: low noise with downward filter
    t = tt(d); return lp(rng.standard_normal(len(t)), 900 * np.exp(-t * 3) + 80) * np.exp(-t * 3) * 3
def ratchet():         # rotating block snap
    t = tt(0.12); return (hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 90) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 60)) * 0.6
def spring():          # pogo jump
    t = tt(0.26); f = 220 + 1000 * (t / 0.26) ** 0.7 + 25 * np.sin(2 * np.pi * 30 * t)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * (1 - np.exp(-t * 400)) * 0.7
def land():
    t = tt(0.15); return lp(rng.standard_normal(len(t)), 1200) * np.exp(-t * 40) * 1.5
def scratch():         # record-scratch freeze
    t = tt(0.45); f = 900 * np.exp(-t * 5) + 120 * np.sin(2 * np.pi * 9 * t)
    return np.tanh(lp(rng.standard_normal(len(t)), 3000) * 0.5 + np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 3)
def riser(d):
    t = tt(d); return (lp(rng.standard_normal(len(t)), 400 + 6000 * (t / d) ** 2) * 0.6 + np.sin(2 * np.pi * np.cumsum(200 + 700 * (t / d) ** 2) / SR) * .25) * (t / d) ** 2.5

add(impact(), B(1), 0.7)
for k, (t, pan) in enumerate([(B(3), -.4), (B(3.5), 0), (B(4), .4), (B(7), 0), (B(11), 0), (B(15), .2)]): add(clack(1 + .06 * k), t, .75, pan)
add(rumble(), B(5.6), .55); add(clack(1.1), B(6.5), .5)
for k in range(6): add(whoosh(.3), B(8 + k) - .05, .12, -.6 if k % 2 else .6)
for k in [12, 13, 14, 15]: add(ratchet(), B(k) - .1, .6)
for k in range(4): add(clack(.8), B(16) + k * .3, .25)
for c in [2.4, 6.6, 10.6, 14.6]: add(whoosh(.45), B(c), .35, .3)
add(whoosh(.8), B(16.6), .4, -.3)
add(land(), B(18), .8)
for i in range(1, 7):
    add(spring(), B(17.6 + i), .5, -.3 + .1 * i); add(land(), B(17.6 + i) + P * .85, .6)
for i in range(3): add(rumble(), B(18.6 + i + 1) + .12, .4, -.2 + .2 * i)
add(ratchet(), B(23.9), .5); add(spring(), B(25.2), .55); add(riser(1.0), B(25.2), .3)
add(scratch(), B(26.6), .7); add(impact(), B(26.8), .75); add(impact(True), B(28.2), .9); add(whoosh(.35), B(28.6), .35)
ir_t = tt(1.0); irL = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 5), 5000); irR = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 5), 5000)
conv = lambda x, ir: np.fft.irfft(np.fft.rfft(x, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]
wl, wr = conv(L, irL), conv(R, irR); g = .16 * np.max(np.abs(L)) / np.max(np.abs(wl))
oL, oR = L + wl * g, R + wr * g; m = max(np.abs(oL).max(), np.abs(oR).max())
st = (np.stack([oL, oR], 1) / m * .9 * 32767).astype("<i2")
f = wave.open(str(pathlib.Path(__file__).with_name("sfx.wav")), "wb"); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()

# Minimal, clean UI-style SFX for the block-chaos reel (no music).
# Soft sine "tocks", light clicks and airy swishes; timed to the composition's beat grid (0.4992 s).
import numpy as np, wave, pathlib
SR = 44100; N = int(SR * 18.5); rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N); P = 60 / 120.19; B = lambda k: k * P
tt = lambda d: np.arange(int(SR * d)) / SR

def lp(x, fc):
    a = 1 - np.exp(-2 * np.pi * np.asarray(fc) / SR) * np.ones(len(x)); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def env(t, a, d): return (1 - np.exp(-t / a)) * np.exp(-t / d)
def add(sig, t, g, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    L[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 - pan)); R[i:j] += sig[:j - i] * g * np.sqrt(0.5 * (1 + pan))

def tock(f=520):        # block placed: soft rounded sine with a hint of overtone
    t = tt(0.35); return (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 30)) * env(t, 0.002, 0.07)
def click(f=1900):      # rotation step / tap: tiny, clean
    t = tt(0.06); return np.sin(2 * np.pi * f * t) * env(t, 0.0005, 0.012)
def swish(d=0.5):       # camera move: airy, low-passed, very soft
    t = tt(d); return lp(rng.standard_normal(len(t)), 600 + 1800 * np.sin(np.pi * t / d)) * np.sin(np.pi * t / d) ** 3 * 1.8
def thud():             # block falling away: low, soft
    t = tt(0.5); return np.sin(2 * np.pi * np.cumsum(140 * np.exp(-t * 3) + 50) / SR) * env(t, 0.004, 0.12)
def glide(up=True):     # touch-moving block travelling
    t = tt(0.6); f = (420 + 260 * (t / 0.6)) if up else (680 - 260 * (t / 0.6))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.6) ** 2 * 0.35
def hit():              # headline: soft sub thump + chord
    t = tt(1.2); sub = np.sin(2 * np.pi * np.cumsum(55 + 40 * np.exp(-t * 20)) / SR) * env(t, 0.003, 0.25)
    chord = sum(np.sin(2 * np.pi * f * t) for f in (523.25, 659.25, 783.99)) / 3 * env(t, 0.01, 0.45)
    return sub * 0.9 + chord * 0.35
def chime():            # logo
    t = tt(1.5); return sum(np.sin(2 * np.pi * f * t) * env(np.clip(t - d, 0, None), 0.003, 0.5) * (t >= d)
                            for f, d in ((783.99, 0), (1046.5, 0.08), (1318.5, 0.16))) / 3

add(hit(), B(1), 0.8)
for k, t in enumerate([B(3), B(4), B(5), B(9), B(15), B(20), B(25)]): add(tock(480 + 30 * k), t, 0.7, (-.3, 0, .3, 0, .2, 0, .2)[k])
for t in [B(6), B(17)]: add(click(2200), t, 0.5)
add(thud(), B(6.6), 0.6); add(tock(560), B(8), 0.45)
add(glide(True), B(17.3), 0.6, .2); add(glide(False), B(18.8), 0.6, .2)
for k in [21, 22, 23, 24]: add(click(1600), B(k) - .1, 0.45)
for c in [2.4, 8.6, 14.6, 19.6, 24.6]: add(swish(0.55), B(c), 0.25)
add(swish(0.9), B(28.6), 0.3)
add(hit(), B(31), 0.8); add(chime(), B(33.5), 0.6)

# light room reverb
ir_t = tt(0.8); irL = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 6), 4000); irR = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 6), 4000)
conv = lambda x, ir: np.fft.irfft(np.fft.rfft(x, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]
wl, wr = conv(L, irL), conv(R, irR); g = .12 * np.max(np.abs(L)) / np.max(np.abs(wl))
oL, oR = L + wl * g, R + wr * g; m = max(np.abs(oL).max(), np.abs(oR).max())
st = (np.stack([oL, oR], 1) / m * .9 * 32767).astype("<i2")
f = wave.open(str(pathlib.Path(__file__).with_name("sfx.wav")), "wb"); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()

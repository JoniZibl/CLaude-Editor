# Minimal, clean tension SFX for the "Ultra Hardcore" reel (no music).
import numpy as np, wave, pathlib
SR = 44100; END = 12.5; N = int(SR * END); rng = np.random.default_rng(9)
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
def tock(f):
    t = tt(0.4); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 25)) * env(t, 0.002, 0.09)
def thump(f0=55, d=0.25):
    t = tt(1.0); return np.sin(2 * np.pi * np.cumsum(f0 + 45 * np.exp(-t * 22)) / SR) * env(t, 0.003, d)
def beat():   # heartbeat lub-dub
    return np.concatenate([thump(48, 0.09)[:int(SR * 0.18)], np.zeros(int(SR * 0.04)), thump(44, 0.08)[:int(SR * 0.3)] * 0.7])
def pop():
    t = tt(0.15); return np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t * 30) + 200) / SR) * env(t, 0.001, 0.03)
def click():
    t = tt(0.05); return np.sin(2 * np.pi * 2000 * t) * env(t, 0.0005, 0.01)
def rise(f0, f1, d):
    t = tt(d); f = f0 + (f1 - f0) * (t / d); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2

# hook
add(thump(60, 0.2), 0.27, 0.7); add(tock(660), 0.27, 0.35)
# each level: tock gets lower, thump heavier
for i, t in enumerate([1.1, 2.9, 4.7, 6.5]):
    add(tock([700, 560, 440, 330][i]), t + 0.45, 0.7); add(thump(60 - 4 * i, 0.15 + 0.06 * i), t + 0.45, 0.4 + 0.15 * i)
    add(rise(500, 760, 0.25), t + 0.45, 0.12)   # meter fill
# low drone swelling from easy to black
t = tt(8.6 - 1.1); sw = (t / t[-1]) ** 2
drone = (np.sin(2 * np.pi * 46 * t) + 0.5 * np.sin(2 * np.pi * 69 * t) + 0.25 * np.sin(2 * np.pi * 92.5 * t + 0.6 * np.sin(2 * np.pi * 0.7 * t))) * sw
add(drone, 1.1, 0.35)
# sweat drops (hard)
for k in range(4): add(click(), 5.0 + 0.7 * k + 0.6, 0.25, 0.4)
# insane: heartbeat + hearts popping
for t in [6.95, 7.35, 7.75, 8.15]: add(beat(), t - 0.16, 0.9)
for t in [7.35, 7.75, 8.15]: add(pop(), t, 0.45, 0.2)
# black: silence (nothing scheduled 8.6-9.3), hard skull hit
add(thump(42, 0.6), 9.62, 1.0)
t = tt(2.5); add((np.sin(2 * np.pi * 110 * t) + np.sin(2 * np.pi * 116.5 * t) + 0.5 * np.sin(2 * np.pi * 164.8 * t)) / 2.5 * env(t, 0.01, 0.9), 9.62, 0.45)
for k in range(5): add(thump(50, 0.12), 9.62 + 0.9 * (k + 1), 0.35)   # glow pulses
add(click(), 10.8, 0.4); add(tock(520), 11.3, 0.4)
# fade the tail into the loop
fade = np.ones(N); n = int(SR * 0.4); fade[-n:] = np.linspace(1, 0, n); L *= fade; R *= fade
ir_t = tt(0.9); irL = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 5), 3500); irR = lp(rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 5), 3500)
conv = lambda x, ir: np.fft.irfft(np.fft.rfft(x, N + len(ir)) * np.fft.rfft(ir, N + len(ir)))[:N]
wl, wr = conv(L, irL), conv(R, irR); g = .12 * np.max(np.abs(L)) / np.max(np.abs(wl))
oL, oR = L + wl * g, R + wr * g; m = max(np.abs(oL).max(), np.abs(oR).max())
st = (np.stack([oL, oR], 1) / m * .9 * 32767).astype("<i2")
f = wave.open(str(pathlib.Path(__file__).with_name("sfx.wav")), "wb"); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()

# SFX track for the hats reel, timed to the composition's beat grid.
import numpy as np, wave, pathlib
SR=44100; N=SR*15; rng=np.random.default_rng(3); out=np.zeros(N)
B=lambda k: 0.14+k*60/139.67
tt=lambda d: np.arange(int(SR*d))/SR
def add(sig,t,g):
    i=int(t*SR); j=min(N,i+len(sig)); out[i:j]+=sig[:j-i]*g
def pop(p):
    t=tt(0.12); f=(500+900*np.exp(-t*40))*p; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)
def impact(big):
    t=tt(0.8 if big else 0.5); f=40+90*np.exp(-t*18); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*(4 if big else 7))*1.2+rng.standard_normal(len(t))*np.exp(-t*30)*0.5
def whoosh(d=0.35):
    t=tt(d); n=rng.standard_normal(len(t)); y=np.empty_like(n); s=0.0; a=0.05+0.4*t/d
    for i in range(len(n)): s+=a[i]*(n[i]-s); y[i]=s
    return y*np.sin(np.pi*t/d)**2*1.6
def boing():
    t=tt(0.35); f=180+500*t/0.35+30*np.sin(2*np.pi*25*t); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
def ding():
    t=tt(0.9); return (np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*1976*t))*np.exp(-t*4)
swaps=[B(k) for k in range(5,9)]+[B(9+k/2) for k in range(8)]+[B(13+k/4) for k in range(20)]
for i,t in enumerate(swaps): add(pop(0.9+0.02*i),t,0.5)
for t in [B(1),B(22),B(29)]: add(impact(False),t,0.7)
for t in [B(18),B(31)]: add(impact(True),t,0.95)
add(ding(),B(18.5),0.6)
for k in range(54): add(pop(1.1+0.01*(k%9)),B(20)+0.012*k,0.12)
for t in [B(26),B(31)]: add(whoosh(),t-0.3,0.5)
for k in range(3): add(boing(),B(26+k),0.45)
add(pop(0.8),B(32),0.8)
x=out/np.max(np.abs(out))*0.9; st=np.repeat((x*32767).astype('<i2')[:,None],2,1)
f=wave.open(str(pathlib.Path(__file__).with_name('sfx.wav')),'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()

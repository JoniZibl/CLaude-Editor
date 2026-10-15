import numpy as np, wave
SR=44100; D=20.0; N=int(SR*D)
rng=np.random.default_rng(7)
def tt(d): return np.arange(int(SR*d))/SR
def env(n,a=0.005,r=0.2):
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))*np.exp(-t/r); return e
def add(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(sig)); 
    if i<N: buf[i:j]+=sig[:j-i]*g
def nf(m): return 440*2**((m-69)/12)
def lp(x,a): # one-pole lowpass
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
# ---------- instruments
def kick():
    t=tt(0.45); f=50+120*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7)+0.3*np.sin(ph)*np.exp(-t*60)
def snare():
    t=tt(0.3); n=rng.standard_normal(len(t))
    return (0.7*n*np.exp(-t*18)+0.5*np.sin(2*np.pi*190*t)*np.exp(-t*25))
def hat(o=False):
    t=tt(0.25 if o else 0.06); n=rng.standard_normal(len(t)); n=n-lp(n,0.6)
    return n*np.exp(-t*(12 if o else 70))*0.5
def bass(m,d):
    t=tt(d); f=nf(m); x=2*((t*f)%1)-1; x=lp(x,0.08)
    return x*np.minimum(1,t/0.01)*np.exp(-t*2.5)
def pluck(m,d=0.35):
    t=tt(d); f=nf(m); x=np.sign(np.sin(2*np.pi*f*t))*0.5+0.5*np.sin(2*np.pi*2*f*t)
    return lp(x,0.25)*env(len(t),0.003,0.12)
def pad(ms,d):
    t=tt(d); x=sum(np.sin(2*np.pi*nf(m)*t)+0.3*np.sin(2*np.pi*nf(m)*1.005*t) for m in ms)
    return x*np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.4)/len(ms)
# ---------- music: 96 BPM, 1 bar = 2.5 s = one scene
music=np.zeros(N); B=0.625; bar=2.5; s16=B/4
chords=[(57,[69,72,76]),(53,[69,72,77]),(48,[67,72,76]),(55,[67,71,74])]  # Am F C G
arp=[0,1,2,1,2,1,0,2]
for b in range(8):
    T0=b*bar; root,ch=chords[b%4]
    if b==0:   # intro: arp + riser only, kick on logo hit
        for k in range(8): add(music,pluck(ch[arp[k]]+12),T0+k*2*s16,0.25+0.03*k)
        r=tt(2.4); f=200+1800*(r/2.4)**2; add(music,rng.standard_normal(len(r))*(r/2.4)**3*0.25,0.1)
        continue
    if b==7:   # outro: big chord + kick, ring out
        add(music,kick(),T0+0.45,1.0); add(music,pad([root+12]+ch,2.0),T0+0.45,0.5)
        add(music,bass(root-12,1.8),T0+0.45,0.6)
        for k in range(6): add(music,pluck(ch[k%3]+12+(12 if k>2 else 0)),T0+0.45+k*0.12,0.22)
        continue
    for q in range(4):
        add(music,kick(),T0+q*B,0.95 if q in(0,2) else 0)
        if q==2: add(music,kick(),T0+1.5*B,0.6)
        if q in(1,3): add(music,snare(),T0+q*B,0.55)
        for h in range(2): add(music,hat(h==1 and q==3),T0+q*B+h*2*s16,0.35)
        for h in range(2): add(music,hat(),T0+q*B+(2*h+1)*s16,0.18)
    for k,ofs in enumerate([0,1.5,2,3,3.5]): add(music,bass(root-12,0.35),T0+ofs*B,0.55)
    for k in range(16):
        if k%3!=2: add(music,pluck(ch[arp[k%8]]+12),T0+k*s16,0.22)
    add(music,pad(ch,bar),T0,0.18)
    if b==6:  # build into outro
        r=tt(1.2); add(music,rng.standard_normal(len(r))*(r/1.2)**2*0.2,T0+1.3)
fade=np.ones(N); fe=int(SR*1.2); fade[-fe:]=np.linspace(1,0,fe); music*=fade
# ---------- SFX
sfx=np.zeros(N)
def whoosh(d=0.35):
    t=tt(d); n=rng.standard_normal(len(t)); e=np.sin(np.pi*t/d)**2
    a=0.05+0.4*(t/d); y=np.empty_like(n); s=0.0
    for i in range(len(n)): s+=a[i]*(n[i]-s); y[i]=s
    return y*e*1.6
def impact(big=False):
    t=tt(0.9 if big else 0.5); f=40+90*np.exp(-t*18); ph=2*np.pi*np.cumsum(f)/SR
    n=rng.standard_normal(len(t))
    return np.sin(ph)*np.exp(-t*(4 if big else 7))*1.2+n*np.exp(-t*30)*0.5
def pop(p=1.0):
    t=tt(0.12); f=(500+900*np.exp(-t*40))*p; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*0.6
def tap():
    t=tt(0.08); return np.sin(2*np.pi*1500*t)*np.exp(-t*60)*0.5+rng.standard_normal(len(t))*np.exp(-t*120)*0.2
def boing():
    t=tt(0.35); f=180+500*(t/0.35)+30*np.sin(2*np.pi*25*t); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)*0.45
def ding():
    t=tt(0.8); return (np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*1976*t))*np.exp(-t*5)*0.35
for c in [2.5,5,7.5,10,12.5,15,17.5]: add(sfx,whoosh(),c-0.3,0.5)
add(sfx,impact(True),0.7,0.9); add(sfx,impact(True),17.95,1.0)
for t in [3.22,5.72,8.22,10.72,13.22,16.42]: add(sfx,impact(),t,0.7)
for t in [15.27,15.6,15.93]: add(sfx,impact(True),t,0.8)
for t in [2.7,3.75,5.8,5.96,6.44,6.6]: add(sfx,tap(),t,0.8)
for t in [2.75,3.8,5.82,5.98,6.46,6.62,10.3,11.0,11.7]: add(sfx,boing(),t,0.6)
for k in range(6): add(sfx,pop(1+0.08*k),8.05+0.07*k,0.6)
for k in range(15): add(sfx,pop(0.9+0.04*k),13.0+0.05*k,0.45)
add(sfx,ding(),11.7,0.8); add(sfx,pop(0.8),18.35,0.9)
def w(name,x):
    x=x/np.max(np.abs(x))*0.9; st=np.repeat((x*32767).astype('<i2')[:,None],2,1)
    f=wave.open(name,'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes(st.tobytes()); f.close()
w('music.wav',music); w('sfx.wav',sfx)

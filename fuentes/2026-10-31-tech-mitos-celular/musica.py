import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf
sr=44100; dur=46.02; n=int(dur*sr); out=np.zeros((n,2)); rng=np.random.default_rng(11)
T1,T2,T3=9.10,18.62,28.68
SC=[0,5.0,9.85,14.45,19.2,24.85,29.45,33.65,40.95]
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*sr); j=min(n,i+len(sig))
    if i>=n or i<0: return
    l=np.sqrt(0.5*(1-pan)); r=np.sqrt(0.5*(1+pan))
    out[i:j,0]+=sig[:j-i]*g*l; out[i:j,1]+=sig[:j-i]*g*r
def note(m): return 440*2**((m-69)/12)
def pluck(f,d=0.4):
    t=np.arange(int(d*sr))/sr
    s=(np.sin(2*np.pi*f*t)+0.3*np.sin(4*np.pi*f*t)+0.1*np.sin(6*np.pi*f*t))*np.exp(-t*8)
    return s*np.minimum(1,t*200)
def bass(f,d):
    t=np.arange(int(d*sr))/sr
    return (np.sin(2*np.pi*f*t)+0.25*np.sin(4*np.pi*f*t))*np.exp(-t*2.4)*np.minimum(1,t*80)
def kick():
    t=np.arange(int(0.25*sr))/sr; f=50+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*14)
def hat():
    t=np.arange(int(0.05*sr))/sr; s=rng.standard_normal(len(t))
    b,a=sg.butter(2,7000/(sr/2),'high'); return sg.lfilter(b,a,s)*np.exp(-t*70)
def pad(fs,d):
    t=np.arange(int(d*sr))/sr; s=sum(sg.sawtooth(2*np.pi*f*t)*0.25+np.sin(2*np.pi*f*1.003*t)*0.5 for f in fs)
    b,a=sg.butter(2,1100/(sr/2)); s=sg.lfilter(b,a,s)
    return s*np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.4)
def whoosh(d=0.55,up=True):
    t=np.arange(int(d*sr))/sr; s=rng.standard_normal(len(t)); o=np.zeros_like(s)
    for k in range(6):
        lo=300+k*600; b,a=sg.butter(2,[lo/(sr/2),(lo+500)/(sr/2)],'band'); seg=sg.lfilter(b,a,s)
        c=(0.1+k*0.07) if up else (d-0.1-k*0.07)
        o+=seg*np.exp(-((t-c)/0.08)**2)
    return o/np.max(np.abs(o))
def pop(f=700):
    t=np.arange(int(0.12*sr))/sr; fr=f*0.6+f*np.exp(-t*40)
    return np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-t*34)
def ding(f=1318,d=0.5):
    t=np.arange(int(d*sr))/sr
    return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*7)*np.minimum(1,t*300)
def smash():
    t=np.arange(int(0.7*sr))/sr
    nz=rng.standard_normal(len(t)); b,a=sg.butter(2,[200/(sr/2),9000/(sr/2)],'band'); nz=sg.lfilter(b,a,nz)*np.exp(-t*9)
    thump=np.sin(2*np.pi*np.cumsum(45+120*np.exp(-t*25))/sr)*np.exp(-t*8)
    s=nz*0.8+thump*1.3
    # vidrio: campanitas agudas
    for k in range(10):
        f=2400+rng.random()*3800; off=int(rng.random()*0.18*sr)
        g=np.sin(2*np.pi*f*t[:len(t)-off])*np.exp(-np.arange(len(t)-off)/sr*18)*0.18
        s[off:]+=g
    return s
def drop_whoosh():  # martillo cayendo
    d=0.5; t=np.arange(int(d*sr))/sr; s=rng.standard_normal(len(t))
    b,a=sg.butter(2,[400/(sr/2),5000/(sr/2)],'band'); s=sg.lfilter(b,a,s)
    return s*(t/d)**2*np.exp(-((t-d)/0.5)**2)
def sweep(f0,f1,d=0.6):
    t=np.arange(int(d*sr))/sr; fr=np.linspace(f0,f1,len(t))
    return np.sin(2*np.pi*np.cumsum(fr)/sr)*np.minimum(1,t*60)*np.minimum(1,(d-t)*20)
def buzz(d=0.35):
    t=np.arange(int(d*sr))/sr; return sg.square(2*np.pi*110*t)*0.5*np.minimum(1,(d-t)*30)
# ---- música: C G Am F, 112 bpm ----
bpm=112;beat=60/bpm;bar=4*beat
chords=[[60,64,67],[55,59,62],[57,60,64],[53,57,60]];roots=[36,43,45,41]
arp=[0,1,2,1,2,1,2,1]
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4]
    add(pad([note(m) for m in c],bar),t0,0,0.05)
    for k in range(8):
        add(pluck(note(c[arp[k]%3]+12),0.35),t0+k*beat/2,0.3 if k%2 else -0.3,0.15 if b_>0 else 0.08)
    add(bass(note(r),beat*1.8),t0,0,0.3);add(bass(note(r),beat*1.8),t0+2*beat,0,0.24)
    for k in range(4):
        add(kick(),t0+k*beat,0,0.30 if b_>0 else 0.0)
        add(hat(),t0+k*beat+beat/2,0.2,0.05)
# ---- efectos ----
for c in SC[1:]: add(whoosh(),max(0,c-0.35),0,0.13)
for T in (T1,T2,T3):
    add(drop_whoosh(),T-0.5,0,0.18); add(smash(),T,0,0.55)
for t in (0.30,0.95,1.60): add(pop(),t,0.0,0.14)
add(pop(520),3.45,0.3,0.16)
for t in (5.2,14.6,25.0): add(pop(500),t,0,0.14)
for t in (6.8,7.3,7.76,8.2): add(whoosh(0.3),t-0.05,0,0.07)
for t in (10.96,11.18,11.4,11.62): add(ding(2600,0.35),t,0.2,0.07)
add(pop(800),12.45,0,0.12); add(buzz(0.3),13.5,0,0.06)
add(sweep(900,220,1.8),15.6,0,0.07); add(ding(1568,0.4),17.2,0,0.1); add(pop(600),17.84,0,0.12)
add(ding(1046,0.5),20.84,0,0.1); add(sweep(500,120,1.0),23.36,0,0.07); add(buzz(0.4),24.2,0,0.06)
add(ding(1568,0.6),24.85,0,0.14); add(pop(900),24.95,0.2,0.1)
add(sweep(300,90,0.7),27.3,0,0.08)
add(buzz(0.4),29.9,0,0.08)
for k in range(10): add(pop(1400),32.3+k*0.07,0.3,0.03)
add(ding(880,0.4),32.9,0,0.1)
for t,f in zip([34.55,35.55,36.4,37.65,39.1],[1046,1175,1318,1568,2093]): add(ding(f,0.45),t+0.35,0,0.12)
for t in (33.7,): add(pop(700),t,0,0.12)
for t in (41.0,41.5,42.0,42.45,42.96): add(pop(650+int((t-41)*80)),t,0,0.12)
add(pop(500),43.7,0,0.12); add(pop(300),44.3,0,0.2)
for k,m in enumerate([72,76,79,84,88]): add(ding(note(m),0.6),44.35+k*0.06,0,0.1)
t=np.arange(n)/sr
out*=(np.minimum(1,t/0.25)*np.minimum(1,(dur-t)/1.2))[:,None]
out=np.tanh(out*1.2)/1.2
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16))
print('ok',20*np.log10(np.sqrt(np.mean(out**2))))

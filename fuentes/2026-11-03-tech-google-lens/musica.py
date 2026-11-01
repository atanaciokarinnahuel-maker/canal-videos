import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, json
sr=44100; dur=json.load(open('words.json'))['voice_dur']+1.3; n=int(dur*sr); out=np.zeros((n,2)); rng=np.random.default_rng(33)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*sr); 
    if i>=n or i<0: return
    j=min(n,i+len(sig)); l=np.sqrt(0.5*(1-pan)); r=np.sqrt(0.5*(1+pan))
    out[i:j,0]+=sig[:j-i]*g*l; out[i:j,1]+=sig[:j-i]*g*r
def note(m): return 440*2**((m-69)/12)
def lp(x,fc,o=2):
    b,a=sg.butter(o,fc/(sr/2)); return sg.lfilter(b,a,x)
def T(d): return np.arange(int(d*sr))/sr
def pluck(f,d=0.3):
    t=T(d); s=(sg.square(2*np.pi*f*t,0.3)*0.4+np.sin(2*np.pi*f*t))*np.exp(-t*10); return lp(s,6000)*np.minimum(1,t*400)
def bell(f,d=0.6):
    t=T(d); return (np.sin(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*2*t)*np.exp(-t*6)+0.2*np.sin(2*np.pi*f*3.01*t))*np.exp(-t*5)*np.minimum(1,t*500)
def bass(f,d):
    t=T(d); s=sg.sawtooth(2*np.pi*f*t)*0.6+np.sin(2*np.pi*f*t); return lp(s,600)*np.exp(-t*3)*np.minimum(1,t*200)
def kick():
    t=T(0.3); return np.sin(2*np.pi*np.cumsum(50+120*np.exp(-t*30))/sr)*np.exp(-t*11)
def clap():
    t=T(0.22); s=rng.standard_normal(len(t)); b,a=sg.butter(2,[1000/(sr/2),6000/(sr/2)],'band'); e=np.exp(-t*25)+0.6*np.exp(-np.maximum(0,t-0.012)*30)*(t>0.012)
    return sg.lfilter(b,a,s)*e
def hat(o=False):
    t=T(0.12 if o else 0.05); s=rng.standard_normal(len(t)); b,a=sg.butter(2,8000/(sr/2),'high'); return sg.lfilter(b,a,s)*np.exp(-t*(25 if o else 80))
def pad(fs,d):
    t=T(d); s=sum(sg.sawtooth(2*np.pi*f*t)*0.2+np.sin(2*np.pi*f*1.003*t)*0.4 for f in fs); return lp(s,1800)*np.minimum(1,t/0.25)*np.minimum(1,(d-t)/0.4)
def whoosh(d=0.45):
    t=T(d); s=rng.standard_normal(len(t)); o=np.zeros_like(s)
    for k in range(6):
        lo=300+k*700; b,a=sg.butter(2,[lo/(sr/2),(lo+600)/(sr/2)],'band'); o+=sg.lfilter(b,a,s)*np.exp(-((t-(0.06+k*0.055))/0.07)**2)
    return o/np.max(np.abs(o))
def pop(f=700):
    t=T(0.12); return np.sin(2*np.pi*np.cumsum(f*0.6+f*np.exp(-t*40))/sr)*np.exp(-t*34)
def bip(f=1760,d=0.08):
    t=T(d); return sg.square(2*np.pi*f*t)*0.35*np.exp(-t*30)
def boom():
    t=T(0.8); nz=lp(rng.standard_normal(len(t)),2500)*np.exp(-t*8); th=np.sin(2*np.pi*np.cumsum(50+110*np.exp(-t*18))/sr)*np.exp(-t*6); return nz*0.5+th*1.2
def riser(d,f0=300,f1=2600):
    t=T(d); fr=np.linspace(f0,f1,len(t)); s=sg.sawtooth(2*np.pi*np.cumsum(fr)/sr)*0.4+rng.standard_normal(len(t))*0.25; return lp(s,7000)*(t/d)**1.6
def scan(d=0.8):
    t=T(d); fr=900+700*np.sin(np.pi*t/d); return np.sin(2*np.pi*np.cumsum(fr)/sr)*0.4*(0.5+0.5*np.sign(np.sin(2*np.pi*14*t)))*np.minimum(1,(d-t)*20)*np.minimum(1,t*40)
def shutter():
    t=T(0.18); return rng.standard_normal(len(t))*(np.exp(-t*60)+0.7*np.exp(-np.maximum(0,t-0.07)*70)*(t>0.07))
# ---- música: C G Am F, 114 bpm (tonalidad mayor) ----
bpm=114;beat=60/bpm;bar=4*beat
chords=[[60,64,67],[55,59,62],[57,60,64],[53,57,60]];roots=[36,31,33,29]
mel=[[72,76,79,76],[74,79,83,79],[76,72,69,72],[77,72,69,74]]
arp=[0,1,2,1,2,1,0,2]
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4];full=t0>=3.2 and t0<42.4
    add(pad([note(m) for m in c],bar),t0,0,0.045)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.26),t0+k*beat/2,0.35 if k%2 else -0.35,0.10)
    for k in range(8): add(bass(note(r if k!=7 else r+7),beat*0.48),t0+k*beat/2,0,0.20)
    if b_%2==1 or t0>=42.4:
        for k,m in enumerate(mel[b_%4]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.035)
    for k in range(4):
        add(kick(),t0+k*beat,0,0.34)
        if k%2==1: add(clap(),t0+k*beat,0,0.14 if full else 0.09)
        add(hat(k==3),t0+k*beat+beat/2,0.25,0.06)
        if full: add(hat(),t0+k*beat+beat/4,-0.25,0.03); add(hat(),t0+k*beat+3*beat/4,-0.25,0.03)
# ---- efectos alineados a los cortes ----
for t in [1.55,3.35,4.95,10.6,11.45,17.72,21.7,24.62,31.98,39.25,42.3]: add(whoosh(),t,0,0.17)
add(riser(0.55),0.5,0,0.16); add(boom(),1.08,0,0.30); [add(bell(note(m),0.7),1.08+k*0.05,0,0.07) for k,m in enumerate([84,88,91,96])]
for k in range(5): add(pop(500+k*60),1.64+k*0.07,(k-2)*0.2,0.07)
add(boom(),2.8,0,0.18); add(pop(300),2.8,0,0.12)
add(pop(800),3.6,0,0.12); add(bell(1568,0.5),3.65,0,0.06); add(pop(650),4.08,0,0.10)
add(pop(500),5.28,0,0.16); add(bell(2093,0.5),5.33,0.2,0.07)
add(pop(700),6.8,-0.4,0.12); add(pop(800),7.44,0.4,0.12); add(pop(600),8.2,0,0.10)
for t in [9.04,13.44,21.45,35.72,36.88]: add(bip(1760),t,0,0.20); add(bip(2349,0.06),t+0.06,0,0.14)
for t,d in [(10.7,1.0),(15.45,.65),(26.6,1.0),(33.2,1.2)]: add(scan(d),t,0,0.06)
add(boom(),10.64,0,0.14)
for t,c in zip([12.2,18.44,25.44,32.24],[[72,76,79],[74,77,81],[76,79,83],[77,81,84]]):
    add(pop(600),t,0,0.12); [add(bell(note(m+12),0.6),t+0.02+k*0.06,0,0.07) for k,m in enumerate(c)]
add(pop(900),13.6,0,0.09)
add(riser(0.4,600,3000),15.65,0,0.08); add(bell(1760,0.5),16.05,0,0.09); [add(bell(note(m),0.4),16.55+k*0.14,0.2,0.05) for k,m in enumerate([84,86,88,91])]
add(shutter(),19.6,0,0.22)
for k in range(5): add(bip(1400+k*120,0.05),20.72+k*0.1,0,0.08)
add(pop(750),21.92,0,0.14); add(bell(1318,0.4),22.1,0,0.06); add(boom(),23.36,0,0.18); add(pop(300),23.36,0,0.12)
for t in [27.12,27.92,28.72]: add(bip(1976,0.07),t,0,0.14); add(pop(900),t+0.04,0,0.06)
add(whoosh(0.35),29.55,0,0.08)
for k,t in enumerate([30.08,30.4,30.8]): add(pop(700+k*120),t,0,0.10)
add(boom(),33.07,0,0.14); [add(bell(note(m),0.6),33.07+k*0.05,0,0.06) for k,m in enumerate([84,88,91,96])]
add(whoosh(0.35),35.78,0,0.08); add(pop(700),37.0,0,0.08); add(bip(1976,0.07),37.6,0,0.12)
add(whoosh(0.3),38.12,0,0.06); [add(pop(800+k*100),38.4+k*0.1,0,0.07) for k in range(3)]
add(riser(0.5,300,3000),38.95,0,0.12); [add(bell(note(m),0.9),39.44+k*0.07,0,0.08) for k,m in enumerate([72,76,79,84,88,91])]
add(boom(),41.12,0,0.12); add(boom(),41.68,0,0.24)
for k in range(4): add(pop(600+k*90),42.96+k*0.12,0,0.10)
add(pop(800),43.96,0,0.12); add(pop(650),44.9,0,0.10)
add(bip(1760),45.36,0,0.16); [add(bell(note(m),0.8),45.4+k*0.06,0,0.08) for k,m in enumerate([79,84,88,91,96])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.08)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

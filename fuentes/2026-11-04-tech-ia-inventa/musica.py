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
def glitch(d=0.35):
    t=T(d); s=sg.square(2*np.pi*(220+1800*(np.floor(t*40)%5)/5)*t)*0.4*(np.sin(2*np.pi*30*t)>0); return s*np.exp(-t*4)
def ding(f=1318):
    return bell(f,0.8)+0.6*bell(f*1.5,0.8)
def boing():
    t=T(0.4); return np.sin(2*np.pi*np.cumsum(200+180*np.sin(2*np.pi*6*t)*np.exp(-t*4))/sr)*np.exp(-t*6)
def buzz():
    t=T(0.35); return lp(sg.sawtooth(2*np.pi*110*t)+sg.sawtooth(2*np.pi*116*t),2200)*0.5*np.exp(-t*5)
def fuse(d):
    t=T(d); return lp(rng.standard_normal(len(t)),5000)*0.5*(0.6+0.4*np.abs(np.sin(2*np.pi*13*t)))
# ---- música: Am F C G, 116 bpm, enérgica con un toque de misterio ----
bpm=116;beat=60/bpm;bar=4*beat
chords=[[57,60,64],[53,57,60],[60,64,67],[55,59,62]];roots=[33,29,36,31]
mel=[[76,72,69,72],[77,72,69,77],[79,76,72,76],[74,79,83,79]]
arp=[0,1,2,1,2,1,0,2]
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4];full=(t0>=4.8 and t0<22.0) or (t0>=31.0 and t0<46.5)
    dark=22.0<=t0<28.0
    add(pad([note(m) for m in c],bar),t0,0,0.05 if not dark else 0.07)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.26),t0+k*beat/2,0.35 if k%2 else -0.35,0.09 if not dark else 0.05)
    for k in range(8): add(bass(note(r if k!=7 else r+7),beat*0.48),t0+k*beat/2,0,0.20)
    if b_%2==1 or t0>=38.0:
        for k,m in enumerate(mel[b_%4]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.035)
    for k in range(4):
        add(kick(),t0+k*beat,0,0.34 if not dark else 0.24)
        if k%2==1: add(clap(),t0+k*beat,0,0.14 if full else 0.08)
        add(hat(k==3),t0+k*beat+beat/2,0.25,0.06)
        if full: add(hat(),t0+k*beat+beat/4,-0.25,0.03); add(hat(),t0+k*beat+3*beat/4,-0.25,0.03)
# ---- efectos alineados a cada golpe visual ----
add(pop(800),0.12,0.3,0.12); add(pop(650),0.45,-0.3,0.10)
for k in range(6): add(bip(1500+k*90,0.04),0.82+k*0.07,0,0.06)
add(boom(),1.28,0,0.30); add(glitch(),1.28,0,0.10); add(pop(300),1.28,0,0.12)
add(riser(0.5,500,2600),2.42,0,0.08); add(bip(2093,0.07),2.92,0,0.14)
add(whoosh(),3.55,0,0.14); add(boom(),3.67,0,0.16); add(glitch(0.2),3.67,0,0.06)
add(riser(0.8,300,3000),4.85,0,0.12); add(whoosh(0.5),5.4,0,0.18); add(boom(),5.95,0,0.16); [add(bell(note(m),0.6),5.95+k*0.05,0,0.06) for k,m in enumerate([81,84,88,93])]
add(pop(700),6.8,0,0.12); add(bell(1760,0.5),7.0,0,0.06); add(bip(1976,0.07),7.76,0,0.12); add(pop(900),8.4,0,0.10)
add(whoosh(0.4),9.3,0,0.10); add(pop(600),10.3,0,0.10); add(pop(500),10.88,0,0.14)
add(whoosh(0.3),12.6,0,0.10); add(pop(250),12.64,0,0.14); add(pop(250),12.85,0,0.12); add(buzz(),12.66,0,0.10)
add(whoosh(0.5),13.35,0,0.10); add(pop(800),13.76,0,0.12); add(bell(1568,0.4),13.8,0,0.06)
for k in range(18): add(pop(500+k*40),15.56+k*0.08,(k%3-1)*0.4,0.05)
add(riser(1.6,300,3200),15.7,0,0.10); add(boom(),17.3,0,0.18)
for k in range(3): add(pop(600+k*100),17.6+k*0.12,0,0.08)
add(boing(),18.45,0,0.16); add(pop(400),19.2,0,0.14); add(bell(1318,0.4),19.25,0,0.06)
add(whoosh(0.35),20.0,0,0.10); for_=[add(pop(650+k*90),20.25+k*0.12,0,0.07) for k in range(3)]
add(ding(1318),21.48,0,0.10); add(boom(),21.48,0,0.10)
add(whoosh(0.5),22.2,0,0.12); add(boom(),22.3,0,0.12)
for k in range(6): add(bell(note(69+k*2),0.5),22.6+k*0.35,0.3*(k%2*2-1),0.03)
add(pop(700),23.52,0,0.12)
for k in range(11): add(bip(900+k*70,0.04),25.64+k*0.07,0,0.07)
add(pop(800),26.48,0,0.14); add(bell(1760,0.4),26.5,0,0.06)
add(ding(1568),27.36,0,0.07); add(glitch(0.4),27.9,0,0.14); add(buzz(),27.9,0,0.12)
add(whoosh(),28.1,0,0.16); add(boom(),28.23,0,0.18); add(riser(0.3,800,3000),28.25,0,0.06)
add(pop(500),30.32,0,0.12); add(whoosh(0.35),30.6,0,0.14); add(boom(),30.62,0,0.08)
add(whoosh(0.4),31.2,0,0.12); add(pop(700),31.3,0,0.12); add(bell(1318,0.4),31.4,0,0.05)
add(whoosh(0.3),33.15,0,0.08); add(pop(600),33.4,0,0.10); add(pop(700),33.6,0,0.10)
for t in [34.88,35.2,35.52]: add(bip(1976,0.07),t,0,0.14); add(pop(900),t+0.03,0,0.06)
add(ding(1568),35.55,0,0.06); add(buzz(),36.4,0,0.12)
add(fuse(1.4),36.9,0.6,0.05); add(riser(0.7,300,3200),37.6,0,0.14)
add(boom(),38.3,0,0.32); [add(bell(note(m),0.9),38.3+k*0.06,0,0.08) for k,m in enumerate([69,72,76,81,84,88])]
add(whoosh(0.5),38.35,0,0.12)
for t in [39.02,40.24,41.52]: add(bell(note(81),0.4),t,0,0.04)
add(riser(0.5,800,3500),41.8,0,0.06); add(ding(1760),42.0,0,0.05)
add(whoosh(0.4),42.7,0,0.10)
for t,f in [(43.36,600),(44.0,700),(44.56,800)]: add(pop(f),t,0,0.14); add(bell(f*2,0.4),t+0.02,0,0.05)
add(boom(),45.2,0,0.16); [add(bip(1976,0.06),45.35+k*0.32,0,0.12) for k in range(3)]
add(whoosh(),46.8,0,0.14); add(pop(700),46.88,0,0.12)
add(pop(800),47.4,0,0.10); add(pop(650),49.0,0,0.10)
for k in range(8): add(bip(1800,0.03),49.0+k*0.075,0,0.05)
add(pop(700),50.0,0,0.10); add(bip(1760),50.48,0,0.16); [add(bell(note(m),0.8),50.6+k*0.06,0,0.08) for k,m in enumerate([81,84,88,93,96])]
add(boom(),50.6,0,0.14)
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.08)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

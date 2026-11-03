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
# ---- música: Dm Bb F C, 114 bpm, misterio "hacker" con energía ----
bpm=114;beat=60/bpm;bar=4*beat
chords=[[62,65,69],[58,62,65],[57,60,65],[60,64,67]];roots=[38,34,41,36]
mel=[[74,77,81,77],[74,70,74,77],[72,77,81,84],[79,76,72,76]]
arp=[0,1,2,1,2,1,0,2]
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4];full=(t0>=7.5 and t0<21.5) or (t0>=28.8 and t0<38.8) or (t0>=44.4 and t0<52.5)
    dark=(13.0<=t0<15.0) or (38.8<=t0<44.4)
    add(pad([note(m) for m in c],bar),t0,0,0.05 if not dark else 0.08)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.24),t0+k*beat/2,0.35 if k%2 else -0.35,0.09 if not dark else 0.05)
    for k in range(8): add(bass(note(r if k!=7 else r+7),beat*0.48),t0+k*beat/2,0,0.20)
    if b_%2==1 or t0>=44.0:
        for k,m in enumerate(mel[b_%4]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.035)
    for k in range(4):
        add(kick(),t0+k*beat,0,0.34 if not dark else 0.26)
        if k%2==1: add(clap(),t0+k*beat,0,0.14 if full else 0.08)
        add(hat(k==3),t0+k*beat+beat/2,0.25,0.06)
        if full: add(hat(),t0+k*beat+beat/4,-0.25,0.03); add(hat(),t0+k*beat+3*beat/4,-0.25,0.03)
# ---- efectos alineados a cada golpe visual ----
add(glitch(0.3),0.0,0,0.10); add(boom(),0.07,0,0.22)
for k in range(8): add(bip(1400+k*80,0.04),0.15+k*0.14,0,0.06)
add(pop(700),0.88,0,0.10); add(whoosh(0.35),1.5,0,0.12); add(pop(600),1.6,0,0.12)
add(boom(),2.24,0,0.26); add(glitch(),2.24,0,0.12)
add(whoosh(),2.95,0,0.14); [add(bip(1200+k*100,0.04),3.3+k*0.09,0,0.05) for k in range(12)]; add(pop(800),3.19,0,0.12)
add(pop(700),4.48,0,0.10); add(boing(),4.64,0,0.14); add(riser(1.0,300,2600),5.5,0,0.08); add(pop(900),6.48,0,0.12)
add(whoosh(0.6),6.6,0,0.16); add(ding(1568),7.55,0,0.10)
add(whoosh(0.4),7.8,0,0.12); [add(bip(1700,0.03),8.1+k*0.075,0,0.05) for k in range(8)]
add(buzz(),8.8,0,0.16); add(boom(),8.8,0,0.10); add(pop(300),9.52,0,0.14); add(whoosh(0.3),9.5,0,0.10)
add(whoosh(0.4),10.22,0,0.12); add(pop(700),10.28,0,0.10); add(riser(1.2,200,1400),10.6,0,0.07)
for k in range(10): add(pop(300+k*30),10.9+k*0.12,0,0.04)
add(ding(1318),11.5,0,0.08); add(pop(800),11.76,0,0.12); add(pop(600),12.36,0,0.10)
add(whoosh(0.4),13.3,0,0.12); add(pop(500),13.36,0,0.10); add(riser(0.8,300,2200),13.45,0,0.08)
add(boom(),14.24,0,0.30); add(glitch(0.45),14.24,0,0.14); add(buzz(),14.3,0,0.10)
add(whoosh(0.4),14.85,0,0.12)
for i in range(4):
    for k in range(6): add(bip(1500+k*60,0.03),15.0+i*0.42+k*0.04,0,0.04)
    add(buzz() if i<3 else ding(1760),15.25+i*0.42,0,0.06 if i<3 else 0.10)
add(boom(),16.64,0,0.14); [add(bell(note(m),0.6),16.64+k*0.05,0,0.05) for k,m in enumerate([81,86,89,93])]
add(whoosh(0.5),17.45,0,0.16); add(riser(1.4,300,3600),17.6,0,0.10); add(boom(),19.0,0,0.14); add(pop(800),19.12,0,0.10)
add(whoosh(0.4),19.8,0,0.12); add(pop(700),20.08,0,0.12); add(fuse(1.6),20.0,0,0.05); add(pop(600),20.9,0,0.10)
add(whoosh(0.5),21.95,0,0.16); add(boing(),22.15,0,0.18); add(glitch(0.2),22.05,0,0.06); add(pop(900),22.8,0,0.10)
for k,t in enumerate([23.84,24.56,24.88,25.48,26.12,26.72]): add(pop(400+k*80),t,0,0.14); add(bip(900+k*120,0.06),t,0,0.08)
add(boom(),27.39,0,0.34); add(glitch(0.5),27.39,0,0.16); add(buzz(),27.45,0,0.16); add(pop(900),27.92,0,0.10)
add(whoosh(0.5),28.95,0,0.14); add(whoosh(0.4),29.04,0,0.10)
for k in range(12): add(bip(1800,0.02),29.4+k*0.11,0,0.04)
add(buzz(),30.72,0,0.12); add(pop(300),30.72,0,0.12)
add(whoosh(0.4),31.76,0,0.12)
for k in range(18): add(bip(1500,0.02),32.1+k*0.11,0,0.04)
add(pop(500),34.16,0,0.14); add(bell(1318,0.4),34.2,0,0.05)
add(whoosh(0.4),35.36,0,0.12); add(riser(2.0,200,3200),35.6,0,0.10)
add(boom(),37.52,0,0.20); [add(bell(note(m),0.9),37.52+k*0.06,0,0.08) for k,m in enumerate([74,77,81,86,89,93])]
add(boom(),38.87,0,0.28); add(glitch(0.35),38.87,0,0.12); add(buzz(),38.9,0,0.12)
add(pop(700),39.84,0,0.12); add(ding(1568),40.0,0,0.05); for_=[add(pop(500+k*90),40.48+k*0.08,0,0.08) for k in range(4)]
add(whoosh(0.4),41.3,0,0.12); add(pop(600),41.6,0,0.10); add(pop(900),42.56,0,0.12)
for t in [42.6,42.95,43.25,43.5,43.75]: add(buzz(),t,0,0.07); add(pop(350),t,0,0.10)
add(riser(0.6,400,3000),43.85,0,0.10); add(whoosh(0.6),44.42,0,0.16); add(ding(1318),44.9,0,0.08)
add(pop(800),45.44,0,0.12); [add(bip(1200+k*60,0.03),45.6+k*0.06,0,0.05) for k in range(16)]
add(ding(1568),45.7,0,0.06)
add(pop(800),47.2,0,0.12); add(ding(1568),47.45,0,0.06); add(pop(700),48.96,0,0.12)
add(pop(800),50.48,0,0.12); add(ding(1568),50.73,0,0.06); add(pop(900),51.2,0,0.10)
add(riser(0.5,500,3500),51.26,0,0.10); add(boom(),51.76,0,0.26); [add(bell(note(m),1.0),51.76+k*0.06,0,0.09) for k,m in enumerate([74,77,81,86,89,93,98])]
add(whoosh(0.4),52.5,0,0.12); add(pop(700),52.54,0,0.10); add(pop(800),53.0,0,0.10); add(pop(900),53.32,0,0.10); add(boing(),53.68,0,0.14)
add(whoosh(0.3),54.42,0,0.12); add(pop(500),54.46,0,0.12)
add(whoosh(0.4),55.46,0,0.12); add(pop(800),55.6,0,0.12); add(pop(1000),56.15,0,0.14); add(ding(1760),56.9,0,0.10); [add(bell(note(m),0.8),56.9+k*0.06,0,0.06) for k,m in enumerate([81,86,89,93])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.08)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

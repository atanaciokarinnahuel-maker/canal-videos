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
# ---- música: D A Bm G, 112 bpm (Re mayor), cálida tipo aventura ----
bpm=112;beat=60/bpm;bar=4*beat
chords=[[62,66,69],[57,61,64],[59,62,66],[55,59,62]];roots=[38,33,35,31]
mel=[[74,78,81,78],[76,73,69,73],[74,71,78,74],[71,74,79,78]]
arp=[0,1,2,1,2,1,0,2]
night=(30.7,34.9)
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4];full=(t0>=5.4 and t0<30.0) or (t0>=38.0 and t0<52.5)
    calm=night[0]-bar<t0<night[1]
    add(pad([note(m) for m in c],bar),t0,0,0.05 if not calm else 0.07)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.26),t0+k*beat/2,0.35 if k%2 else -0.35,0.09 if not calm else 0.05)
    for k in range(8): add(bass(note(r if k!=7 else r+7),beat*0.48),t0+k*beat/2,0,0.19)
    if b_%2==1 or t0>=38.0:
        for k,m in enumerate(mel[b_%4]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.035)
    for k in range(4):
        if not calm or k%2==0: add(kick(),t0+k*beat,0,0.32)
        if k%2==1 and not calm: add(clap(),t0+k*beat,0,0.13 if full else 0.08)
        add(hat(k==3),t0+k*beat+beat/2,0.25,0.055)
        if full: add(hat(),t0+k*beat+beat/4,-0.25,0.028); add(hat(),t0+k*beat+3*beat/4,-0.25,0.028)
# ---- efectos alineados a los cortes y golpes ----
cuts=[3.2,5.6,8.0,10.5,12.6,15.2,18.3,20.2,22.5,24.2,27.7,30.7,32.5,34.9,38.4,41.3,44.1,46.3,48.1,50.2,52.9]
for t in cuts: add(whoosh(),t-0.08,0,0.15)
add(riser(0.5),3.1,0,0.14)
for t in [3.62,21.06,23.46,40.3,41.38,47.62,49.18]: add(boom(),t,0,0.22)
for t,c in [(3.62,[74,78,81,86]),(15.75,[74,78,81,86]),(41.38,[74,78,81,86,90]),(44.5,[74,78,81,86,90,93])]:
    [add(bell(note(m+12),0.8),t+k*0.06,0,0.07) for k,m in enumerate(c)]
for k in range(3): add(pop(500+k*80),1.62+k*0.2,0,0.10)
for t in [4.66,9.0,14.1,17.2,18.5,25.0,29.0,33.12,35.8,37.3,42.8,46.4,48.2,53.84,54.2]: add(pop(700),t,0,0.12)
for t in [23.0,23.3,23.6]: add(pop(420),t,0,0.08)
add(whoosh(0.35),25.62,0,0.12); add(pop(900),25.92,0,0.14)
add(boom(),26.64,0,0.10); add(boom(),27.0,0,0.08)
for k in range(5): add(pop(500+k*100),28.3+k*0.45,0,0.08)
add(riser(0.6,250,1800),31.2,0,0.08)
add(riser(0.4,800,4000),36.7,0,0.08); add(bell(2637,0.6),37.02,0,0.10)
for k in range(12): add(bip(1400+k*60,0.04),38.65+k*0.14,0,0.05)
add(riser(0.5,300,3000),39.8,0,0.12)
for k in range(12): add(pop(500+(k%4)*120),48.2+k*0.1,(k%3-1)*0.3,0.06)
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.05)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

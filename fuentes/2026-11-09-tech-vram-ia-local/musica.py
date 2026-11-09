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
def clank():
    t=T(0.7); s=sum(np.sin(2*np.pi*f*t)*np.exp(-t*d) for f,d in [(523,7),(1187,9),(1873,12),(2741,15),(3307,18)]); nz=rng.standard_normal(len(t))*np.exp(-t*40)*0.6
    return (s*0.35+nz)*np.minimum(1,t*800)
def scratch():
    t=T(0.35); fr=np.linspace(1800,200,len(t)); return sg.sawtooth(2*np.pi*np.cumsum(fr)/sr)*0.4*np.exp(-t*4)+rng.standard_normal(len(t))*0.2*np.exp(-t*8)
def snare():
    t=T(0.12); s=rng.standard_normal(len(t)); b,a=sg.butter(2,[1500/(sr/2),7000/(sr/2)],'band'); return sg.lfilter(b,a,s)*np.exp(-t*30)+np.sin(2*np.pi*190*t)*np.exp(-t*25)*0.5
# ---- música tech: La menor, 118 bpm, arpegio sintético + bajo con pulso; zonas tensas en los números grandes ----
import json as _j,unicodedata,re
info=_j.load(open('info.json')); cuts=[c for c in info['cuts'] if c>0]; REV=info['reveal']
W_=_j.load(open('words.json'))['words']
def wt(w,occ=1):
    n=lambda x:re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',x.lower()).encode('ascii','ignore').decode())
    c=0
    for x in W_:
        if n(x['text'])==w:
            c+=1
            if c==occ: return x['start']
bpm=118;beat=60/bpm;bar=4*beat
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]];roots=[33,29,36,31]
tense=[(wt('setenta')-.7,wt('tienes')-.5),(wt('ojo'),wt('entonces'))]
def inz(t): return any(a-bar*.5<t<b for a,b in tense)
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;tz=inz(t0)
    c=chords[b_%4];r=roots[b_%4]
    add(pad([note(m) for m in c],bar),t0,0,0.08)
    for k in range(8): add(pluck(note(c[[0,1,2,1,2,1,0,2][k]]+12),0.22),t0+k*beat/2,0.35 if k%2 else -0.35,0.075)
    for k in range(8): add(bass(note(r),beat*0.48),t0+k*beat/2,0,0.17)
    if b_%2==1: 
        for k,m in enumerate([69,72,76,72]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.03)
    for k in range(4):
        if t0>=1.0:
            add(kick(),t0+k*beat,0,0.30)
            if k%2==1: add(clap(),t0+k*beat,0,0.12 if not tz else 0.15)
            add(hat(k==3),t0+k*beat+beat/2,0.25,0.05)
            if tz: add(hat(),t0+k*beat+beat/4,-0.25,0.04)
# ---- efectos ----
for t in cuts: add(whoosh(),t-0.08,0,0.13)
add(boom(),0.0,0,0.12)
add(scratch(),wt('pero')-0.05,0,0.12)
for t in [wt('procesador')+0.15,wt('nucleos')+0.15]: add(clank(),t,0,0.22); add(boom(),t,0,0.14)
for k in range(10): add(snare(),wt('vram',1)-.8+k*0.08,0,0.04+0.05*k/10)
add(boom(),wt('vram',1),0,0.2);[add(bell(note(m+12),0.9),wt('vram',1)+k*0.07,0,0.08) for k,m in enumerate([57,60,64,69,72])]
for w,oc in [('completo',1),('ocho',1),('doce',1)]: [add(bell(note(m+12),0.7),wt(w,oc)+0.3+k*0.06,0,0.07) for k,m in enumerate([64,69,76])]
add(boom(),wt('cuarenta')-0.1,0,0.2);add(boom(),wt('ahi')+0.1,0,0.16);add(clank(),wt('alcanza',1)+0.1,0,0.2)
add(riser(1.0,300,3000),REV-1.0,0,0.10);[add(bell(note(m+12),0.9),REV+k*0.07,0,0.08) for k,m in enumerate([57,60,64,69,72])]
add(pop(900),wt('lento')+.1,0,0.1)
for k in range(8): add(pop(500+(k%4)*120),wt('cuentame')+0.3+k*0.12,(k%3-1)*0.3,0.06)
tc=wt('sigueme'); [add(bell(note(m+12),0.9),tc+k*0.07,0,0.07) for k,m in enumerate([57,60,64,69,72,76])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.05)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

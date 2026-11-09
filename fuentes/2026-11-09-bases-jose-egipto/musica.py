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
# ---- música: modo frigio dominante (Egipto), 100 bpm. Oscuro en hambre/pérdida, luminoso en abundancia/final ----
import json as _j
info=_j.load(open('info.json')); cuts=[c for c in info['cuts'] if c>0]; REV=info['reveal']
bpm=100;beat=60/bpm;bar=4*beat
minor=[[62,65,69],[63,67,70],[62,65,69],[63,67,70]];mroots=[38,39,38,39]
major=[[62,66,69],[63,67,70],[62,66,69],[67,71,74]];jroots=[38,39,38,43]
scale=[62,63,66,67,69,70,72,74]
arp=[0,1,2,1,2,1,0,2]
dark=[(17.5,18.8),(31.0,32.9),(40.2,48.9)]   # hambre / pérdida
bright=[(15.9,17.5),(32.9,40.2),(50.2,52.7),(57.3,99)]
def inz(t,zs): return any(a-bar*.5<t<b for a,b in zs)
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;dk=inz(t0,dark);br=inz(t0,bright)
    c=(major if br else minor)[b_%4];r=(jroots if br else mroots)[b_%4]
    add(pad([note(m) for m in c],bar),t0,0,0.09 if dk else 0.06)
    for k in range(8):
        if not dk or k%2==0: add(pluck(note(c[arp[k]]+12),0.24),t0+k*beat/2,0.35 if k%2 else -0.35,0.07 if not dk else 0.04)
    for k in range(8):
        if not dk or k%4==0: add(bass(note(r),beat*0.48),t0+k*beat/2,0,0.18)
    if br or (b_%2==1 and not dk):
        for k,m in enumerate([scale[(b_*3+k*2)%8] for k in range(4)]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.03)
    for k in range(4):
        if t0>=1.0:
            add(kick(),t0+k*beat,0,0.30 if not dk else 0.2)
            if k%2==1: add(clap(),t0+k*beat,0,0.12 if br else 0.07)
            if not dk: add(hat(k==3),t0+k*beat+beat/2,0.25,0.05)
            if br: add(hat(),t0+k*beat+beat/4,-0.25,0.025)
# ---- efectos ----
for t in cuts: add(whoosh(),t-0.08,0,0.13)
W_=_j.load(open('words.json'))['words']
def wt(w,occ=1):
    import unicodedata,re
    n=lambda x:re.sub('[^a-z0-9]','',unicodedata.normalize('NFD',x.lower()).encode('ascii','ignore').decode())
    c=0
    for x in W_:
        if n(x['text'])==w:
            c+=1
            if c==occ: return x['start']
add(boom(),0.0,0,0.14)
tw=wt('creo'); add(boom(),tw+0.05,0,0.2); add(clank(),tw+0.05,0,0.15)
te=wt('exesclavo')+0.1; add(clank(),te,0,0.25); add(boom(),te,0,0.15); [add(bell(note(m+12),0.8),te+0.1+k*0.07,0,0.07) for k,m in enumerate([62,66,69,74])]
add(scratch(),wt('siete',2),0,0.15)
for k in range(10): add(snare(),wt('siete',3)-.9+k*0.08,0,0.04+0.05*k/10)
[add(bell(note(m+12),0.9),wt('siete',3)+k*0.07,0,0.07) for k,m in enumerate([62,66,69,74,78])]
add(boom(),wt('siete',4)-0.15,0,0.18)
tp=wt('propuso'); [add(bell(note(m+12),0.8),tp+k*0.07,0,0.06) for k,m in enumerate([62,66,69,74])]
tq=wt('veinte'); add(pop(900),tq,0,0.1)
add(boom(),wt('tercero')-.05,0,0.15)
add(riser(1.0,300,3000),REV-1.0,0,0.10); [add(bell(note(m+12),0.9),REV+k*0.07,0,0.08) for k,m in enumerate([62,66,69,74,78])]; add(boom(),REV,0,0.15)
tm=wt('aqui'); add(scratch(),tm-0.1,0,0.1)
for nme,off in [('pago',0.9),]:
    for k in range(6): add(pop(900+(k%3)*150),wt('pago')+0.5+k*0.07,0,0.06)
add(boom(),wt('final')-0.05,0,0.16); add(clank(),wt('final')+0.2,0,0.12)
tb=wt('biblia'); [add(bell(note(m+12),0.8),tb+k*0.08,0,0.06) for k,m in enumerate([62,66,69,74])]
add(boom(),wt('necio')-0.1,0,0.14)
for k in range(8): add(pop(500+(k%4)*120),wt('necio')+0.1+k*0.1,(k%3-1)*0.3,0.05)
tc=wt('cuentame')
for k in range(10): add(pop(500+(k%4)*120),tc+0.2+k*0.1,(k%3-1)*0.3,0.06)
[add(bell(note(m+12),0.9),tc+k*0.07,0,0.07) for k,m in enumerate([62,66,69,74,78,81])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.05)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

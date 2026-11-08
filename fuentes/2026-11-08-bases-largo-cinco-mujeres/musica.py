import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, json
sr=44100; dur=json.load(open('data.json'))['dur']; n=int(dur*sr); out=np.zeros((n,2)); rng=np.random.default_rng(33)
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
# ---- música larga: tranquila, cambia de color por capítulo ----
D=json.load(open('data.json'));CH={c['id']:c['t'] for c in D['chapters']}
bpm=92;beat=60/bpm;bar=4*beat
PROG={'luz':([[60,64,67],[55,59,62],[57,60,64],[53,57,60]],[36,43,45,41]),
      'calido':([[62,66,69],[57,61,64],[59,62,66],[55,59,62]],[38,45,47,43]),
      'osc':([[57,60,64],[53,57,60],[55,59,62],[52,55,59]],[45,41,43,40])}
def mood(t):
    if CH['rizpa']+16<t<CH['rizpa']+52: return 'osc'
    if CH['abigail']<t<CH['debora'] or CH['ana']<t<CH['rizpa']: return 'calido'
    return 'luz'
arp=[0,1,2,1,2,1,0,2]
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;m=mood(t0);ch,rt=PROG[m];c=ch[b_%4];r=rt[b_%4];card=any(abs(t0-(v-1.6))<bar for v in CH.values())
    add(pad([note(x) for x in c],bar),t0,0,0.07)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.3),t0+k*beat/2,0.35 if k%2 else -0.35,0.05 if m!='osc' else 0.03)
    for k in range(4): add(bass(note(r),beat*0.9),t0+k*beat,0,0.12)
    if m!='osc':
        for k in range(4):
            add(kick(),t0+k*beat,0,0.12)
            add(hat(k==3),t0+k*beat+beat/2,0.25,0.025)
    if b_%2==1 and m=='luz':
        for k,x in enumerate([76,79,74,72]): add(bell(note(x+12),0.6),t0+k*beat,0.15,0.02)
for k,v in CH.items():
    if k!='intro':
        t=v-1.6;add(whoosh(),t-0.1,0,0.16);add(boom(),t,0,0.14);[add(bell(note(x+12),0.9),t+0.15+i*0.08,0,0.06) for i,x in enumerate([60,64,67,72])]
R_=[w for w in D['words'] if w['b']=='cierre' and w['text'].lower().startswith('principio')][0]['start']
add(riser(1.4,300,3000),R_-1.2,0,0.10);[add(bell(note(x+12),1.0),R_+0.6+i*0.08,0,0.08) for i,x in enumerate([60,64,67,72,76,79])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.5)*np.minimum(1,(dur-tt)/2.0))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-22/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

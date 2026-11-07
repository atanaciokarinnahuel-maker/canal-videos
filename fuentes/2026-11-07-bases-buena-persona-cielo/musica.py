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
# ---- música: C G Am F, 104 bpm, esperanzadora; tramo oscuro (pecado) y tramo luminoso (gracia) ----
bpm=104;beat=60/bpm;bar=4*beat
chords=[[60,64,67],[59,62,67],[57,60,64],[57,60,65]];roots=[36,43,45,41]
dark=[[57,60,64],[53,57,60],[55,59,62],[52,55,59]];droots=[45,41,43,40]
mel=[[76,79,84,79],[74,79,83,79],[72,76,81,76],[72,77,81,77]]
arp=[0,1,2,1,2,1,0,2]
calmz=(12.6,14.5); darkz=(14.5,23.0)
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;dk=darkz[0]-bar<t0<darkz[1];c=(dark if dk else chords)[b_%4];r=(droots if dk else roots)[b_%4]
    calm=calmz[0]-bar<t0<calmz[1];full=t0>=23.0 and t0<52.5
    add(pad([note(m) for m in c],bar),t0,0,0.06 if not calm else 0.08)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.24),t0+k*beat/2,0.35 if k%2 else -0.35,0.08 if not calm else 0.04)
    for k in range(8):
        if not calm or k%4==0: add(bass(note(r),beat*0.48),t0+k*beat/2,0,0.18)
    if (b_%2==1 or full) and not dk:
        for k,m in enumerate(mel[b_%4]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.03)
    for k in range(4):
        if not calm: add(kick(),t0+k*beat,0,0.30 if not dk else 0.22)
        if k%2==1 and not calm: add(clap(),t0+k*beat,0,0.12 if full else 0.07)
        if not calm and not dk: add(hat(k==3),t0+k*beat+beat/2,0.25,0.05)
        if full and not calm: add(hat(),t0+k*beat+beat/4,-0.25,0.025)
# ---- efectos ----
cuts=[2.36,4.17,5.27,9.2,10.37,12.89,14.53,17.65,18.4,21.47,23.12,25.1,27.4,28.62,31.93,33.58,35.53,37.32,38.83,41.65,45.22,48.85,52.85,54.62]
for t in cuts: add(whoosh(),t-0.08,0,0.13)
for t in [2.36,17.65]: add(clank(),t,0,0.2); add(boom(),t,0,0.18)
add(scratch(),12.89,0,0.15)
for t in [23.12,28.62,35.53]: [add(bell(note(m+12),0.8),t+0.1+k*0.07,0,0.06) for k,m in enumerate([60,64,67,72])]
add(riser(1.2,300,3000),37.6,0,0.10); [add(bell(note(m+12),0.9),38.98+k*0.07,0,0.08) for k,m in enumerate([60,64,67,72,76])]
for t in [27.4,28.62,41.65]: add(boom(),t,0,0.15)
for k in range(12): add(snare(),51.3+k*0.08,0,0.04+0.05*k/12)
for k in range(10): add(pop(500+(k%4)*120),57.6+k*0.08,(k%3-1)*0.3,0.06)
[add(bell(note(m+12),0.9),57.6+k*0.07,0,0.07) for k,m in enumerate([60,64,67,72,76,79,84])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.05)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

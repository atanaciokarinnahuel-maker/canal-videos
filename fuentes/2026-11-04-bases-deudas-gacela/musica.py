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
# ---- música: G D Em C, 116 bpm (Sol mayor), alegre tipo aventura en el oasis ----
bpm=116;beat=60/bpm;bar=4*beat
chords=[[67,71,74],[62,66,69],[64,67,71],[60,64,67]];roots=[43,38,40,36]
mel=[[79,83,86,83],[81,78,74,78],[79,76,83,79],[76,79,84,83]]
arp=[0,1,2,1,2,1,0,2]
calmz=(29.9,33.35)
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4];full=(t0>=3.9 and t0<29.5) or (t0>=33.3 and t0<57.0)
    calm=calmz[0]-bar<t0<calmz[1]
    add(pad([note(m) for m in c],bar),t0,0,0.05 if not calm else 0.075)
    for k in range(8): add(pluck(note(c[arp[k]]+12),0.24),t0+k*beat/2,0.35 if k%2 else -0.35,0.085 if not calm else 0.045)
    for k in range(8):
        if not calm or k%4==0: add(bass(note(r if k!=7 else r+7),beat*0.48),t0+k*beat/2,0,0.19)
    if b_%2==1 or t0>=40.9:
        for k,m in enumerate(mel[b_%4]): add(bell(note(m+12),0.5),t0+k*beat,0.15,0.035)
    for k in range(4):
        if not calm or k%2==0: add(kick(),t0+k*beat,0,0.32 if not calm else 0.18)
        if k%2==1 and not calm: add(clap(),t0+k*beat,0,0.13 if full else 0.08)
        if not calm: add(hat(k==3),t0+k*beat+beat/2,0.25,0.055)
        if full and not calm: add(hat(),t0+k*beat+beat/4,-0.25,0.028); add(hat(),t0+k*beat+3*beat/4,-0.25,0.028)
# ---- efectos alineados a cortes y golpes ----
cuts=[1.85,3.93,5.6,7.64,8.44,10.62,11.85,13.31,15.49,17.89,20.04,22.18,23.31,24.95,26.62,27.85,29.95,31.64,33.38,34.37,36.36,38.04,39.59,41.75,43.56,45.09,46.29,47.4,49.53,51.75,53.48,55.16,56.51]
for t in cuts: add(whoosh(),t-0.08,0,0.14)
for t in [0.16,14.33,26.9]: add(clank(),t,0,0.20)
for t in [0.16,11.85,14.33,21.38,38.55,51.75]: add(boom(),t,0,0.2)
for t in [15.49,24.95,34.37]: add(boom(),t,0,0.14); [add(bell(note(m+12),0.7),t+0.1+k*0.06,0,0.06) for k,m in enumerate([67,71,74,79])]
add(scratch(),29.95,0,0.16)
add(riser(0.9,300,2200),32.4,0,0.10); [add(bell(note(m+12),0.8),33.38+k*0.07,0,0.07) for k,m in enumerate([67,71,74,79,83])]
for k in range(16): add(snare(),39.75+k*0.07,0,0.05+0.06*k/16)
add(riser(1.2,300,3200),39.75,0,0.10)
add(boom(),40.95,0,0.26); [add(bell(note(m+12),0.9),40.95+k*0.06,0,0.08) for k,m in enumerate([67,71,74,79,83,86])]
for k in range(3): add(pop(500+k*90),3.93+k*0.18,0,0.10)
for t in [5.6,8.44,10.62,16.47,17.2,20.04,23.31,25.96,28.44,32.44,36.36,38.04,39.78,43.56,45.09,46.29,49.53,53.48,55.16,56.6]: add(pop(720),t,0,0.11)
for k in range(4): add(pop(600+k*90),36.5+k*0.3,0,0.07)
for k in range(6): add(pop(400+k*120),16.0+k*0.16,0,0.06)
add(whoosh(0.5),28.3,0,0.14)
add(whoosh(0.35),43.5,0,0.14); add(whoosh(0.35),44.5,0,0.12); add(whoosh(0.35),45.4,0,0.12)
add(bip(1760,0.1),46.29,0,0.08); add(bip(2093,0.1),46.42,0,0.08)
for k in range(10): add(pop(500+(k%4)*120),57.5+k*0.08,(k%3-1)*0.3,0.06)
[add(bell(note(m+12),0.9),57.5+k*0.07,0,0.07) for k,m in enumerate([67,71,74,79,83,86,91])]
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.05)*np.minimum(1,(dur-tt)/1.2))[:,None]
out=np.tanh(out*1.1)/1.1
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok',dur)

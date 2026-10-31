import numpy as np, json, sys, scipy.signal as sg, scipy.io.wavfile as wf
sr=44100
info=json.loads(sys.argv[1]); dur=info['dur']; cuts=info['SC'][1:]; pops=info['pops']
n=int(dur*sr); out=np.zeros((n,2))
bpm=110; beat=60/bpm; bar=4*beat
def note(m): return 440*2**((m-69)/12)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*sr); j=min(n,i+len(sig))
    if i>=n: return
    l=np.sqrt(0.5*(1-pan)); r=np.sqrt(0.5*(1+pan))
    out[i:j,0]+=sig[:j-i]*g*l; out[i:j,1]+=sig[:j-i]*g*r
def pluck(f,d=0.5):
    t=np.arange(int(d*sr))/sr
    s=(np.sin(2*np.pi*f*t)+0.35*np.sin(4*np.pi*f*t)+0.12*np.sin(6*np.pi*f*t))*np.exp(-t*7)
    return s*np.minimum(1,t*200)
def bass(f,d):
    t=np.arange(int(d*sr))/sr
    return (np.sin(2*np.pi*f*t)+0.2*np.sin(4*np.pi*f*t))*np.exp(-t*2.2)*np.minimum(1,t*80)
def kick():
    t=np.arange(int(0.25*sr))/sr; f=50+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*14)
rng=np.random.default_rng(7)
def hat():
    t=np.arange(int(0.06*sr))/sr; s=rng.standard_normal(len(t))
    b,a=sg.butter(2,7000/(sr/2),'high'); return sg.lfilter(b,a,s)*np.exp(-t*60)
def pad(fs,d):
    t=np.arange(int(d*sr))/sr; s=sum(sg.sawtooth(2*np.pi*f*t)*0.3 + np.sin(2*np.pi*f*1.003*t)*0.5 for f in fs)
    b,a=sg.butter(2,1200/(sr/2)); s=sg.lfilter(b,a,s)
    env=np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.4); return s*env
def whoosh():
    d=0.6; t=np.arange(int(d*sr))/sr; s=rng.standard_normal(len(t))
    out_=np.zeros_like(s); 
    for k in range(6):
        lo=300+k*600; b,a=sg.butter(2,[lo/(sr/2),(lo+500)/(sr/2)],'band'); seg=sg.lfilter(b,a,s)
        w=np.exp(-((t-(0.1+k*0.07))/0.08)**2); out_+=seg*w
    return out_/np.max(np.abs(out_))
def popfx():
    t=np.arange(int(0.12*sr))/sr; f=600+900*np.exp(-t*40)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*35)
# C G Am F
chords=[[60,64,67],[55,59,62],[57,60,64],[53,57,60]]
roots=[36,43,45,41]
arp=[0,1,2,1,0+12,2,1,2]
nb=int(dur/bar)+1
for b_ in range(nb):
    t0=b_*bar; c=chords[b_%4]; r=roots[b_%4]
    add(pad([note(m) for m in c],bar),t0,0,0.05)
    for k in range(8):
        idx=arp[k]; m=c[idx%3]+(12 if idx>=12 else 0)+12
        add(pluck(note(m),0.45),t0+k*beat/2,0.3 if k%2 else -0.3,0.16 if b_>0 else 0.1)
    add(bass(note(r),beat*1.8),t0,0,0.32); add(bass(note(r),beat*1.8),t0+2*beat,0,0.26)
    for k in range(4):
        add(kick(),t0+k*beat,0,0.32 if b_>0 else 0.0)
        add(hat(),t0+k*beat+beat/2,0.2,0.06)
for c in cuts: add(whoosh(),max(0,c-0.3),0,0.12)
for p in pops: add(popfx(),p,0,0.1)
t=np.arange(n)/sr
out*= (np.minimum(1,t/0.3)*np.minimum(1,(dur-t)/1.5))[:,None]
out=np.tanh(out*1.2)/1.2
rms=np.sqrt(np.mean(out**2)); target=10**(-20/20); out*=target/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16))
print('ok',20*np.log10(np.sqrt(np.mean(out**2))))

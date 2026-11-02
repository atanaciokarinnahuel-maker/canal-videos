import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf
sr=44100; dur=45.7; n=int(dur*sr); out=np.zeros((n,2)); rng=np.random.default_rng(21)
PCT=[[0,10],[1,12],[3.6,11],[4.4,12],[4.95,100],[5.5,100],[6.25,14],[8.7,15],[11.5,17],[14.7,40],[20,46],[23.9,72],[27,76],[29.1,90],[33,92],[35.55,100],[45.7,100]]
SC=[8.75,14.8,24.15,29.2,35.9,41.2]
CLICKS=[9.9,11.0,21.9,23.3,25.5,27.2,27.85,28.5,32.5]
def kf(t,a):
    return np.interp(t,[x[0] for x in a],[x[1] for x in a])
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*sr); j=min(n,i+len(sig))
    if i>=n or i<0: return
    l=np.sqrt(0.5*(1-pan)); r=np.sqrt(0.5*(1+pan))
    out[i:j,0]+=sig[:j-i]*g*l; out[i:j,1]+=sig[:j-i]*g*r
def note(m): return 440*2**((m-69)/12)
def lp(x,fc,o=2):
    b,a=sg.butter(o,fc/(sr/2)); return sg.lfilter(b,a,x)
def pluck(f,d=0.3):
    t=np.arange(int(d*sr))/sr; s=(sg.sawtooth(2*np.pi*f*t)*0.6+np.sin(2*np.pi*f*t))*np.exp(-t*9)
    return lp(s,5000)*np.minimum(1,t*300)
def bass(f,d):
    t=np.arange(int(d*sr))/sr; s=sg.sawtooth(2*np.pi*f*t)+0.5*np.sin(2*np.pi*f*t)
    return lp(s,500)*np.exp(-t*2.2)*np.minimum(1,t*150)
def kick():
    t=np.arange(int(0.28*sr))/sr; return np.sin(2*np.pi*np.cumsum(48+110*np.exp(-t*28))/sr)*np.exp(-t*12)
def snare():
    t=np.arange(int(0.2*sr))/sr; s=rng.standard_normal(len(t)); b,a=sg.butter(2,[1500/(sr/2),9000/(sr/2)],'band'); return sg.lfilter(b,a,s)*np.exp(-t*20)
def hat():
    t=np.arange(int(0.05*sr))/sr; s=rng.standard_normal(len(t)); b,a=sg.butter(2,7500/(sr/2),'high'); return sg.lfilter(b,a,s)*np.exp(-t*70)
def pad(fs,d):
    t=np.arange(int(d*sr))/sr; s=sum(sg.sawtooth(2*np.pi*f*t)*0.25+np.sin(2*np.pi*f*1.004*t)*0.4 for f in fs)
    return lp(s,1400)*np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.5)
def whoosh(d=0.5):
    t=np.arange(int(d*sr))/sr; s=rng.standard_normal(len(t)); o=np.zeros_like(s)
    for k in range(6):
        lo=300+k*650; b,a=sg.butter(2,[lo/(sr/2),(lo+500)/(sr/2)],'band'); seg=sg.lfilter(b,a,s); o+=seg*np.exp(-((t-(0.08+k*0.06))/0.08)**2)
    return o/np.max(np.abs(o))
def pop(f=700):
    t=np.arange(int(0.12*sr))/sr; return np.sin(2*np.pi*np.cumsum(f*0.6+f*np.exp(-t*40))/sr)*np.exp(-t*34)
def ding(f=1318,d=0.5):
    t=np.arange(int(d*sr))/sr; return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*7)*np.minimum(1,t*300)
def tick():
    t=np.arange(int(0.05*sr))/sr; return np.sin(2*np.pi*1800*t)*np.exp(-t*120)+rng.standard_normal(len(t))*np.exp(-t*200)*0.3
def boom():
    t=np.arange(int(0.8*sr))/sr; nz=lp(rng.standard_normal(len(t)),3000)*np.exp(-t*7); th=np.sin(2*np.pi*np.cumsum(55+100*np.exp(-t*20))/sr)*np.exp(-t*6); return nz*0.7+th*1.2
def glitch(d=0.25):
    t=np.arange(int(d*sr))/sr; s=np.sign(np.sin(2*np.pi*(90+rng.random()*600)*t))*0.5+rng.standard_normal(len(t))*0.4
    return s*(rng.random(len(t))>0.45)*np.minimum(1,(d-t)*20)
def riser(d,f0=200,f1=2400):
    t=np.arange(int(d*sr))/sr; fr=np.linspace(f0,f1,len(t)); s=sg.sawtooth(2*np.pi*np.cumsum(fr)/sr)*0.5+rng.standard_normal(len(t))*0.2
    return lp(s,6000)*(t/d)**1.5
def sweep(f0,f1,d=0.6):
    t=np.arange(int(d*sr))/sr; return np.sin(2*np.pi*np.cumsum(np.linspace(f0,f1,len(t)))/sr)*np.minimum(1,t*60)*np.minimum(1,(d-t)*20)
def buzz(d=0.3):
    t=np.arange(int(d*sr))/sr; return lp(sg.square(2*np.pi*110*t),1200)*np.minimum(1,(d-t)*30)
def clack():
    t=np.arange(int(0.07*sr))/sr; return (np.sin(2*np.pi*220*t)*0.6+rng.standard_normal(len(t))*0.5)*np.exp(-t*60)
# --- música: Am F C G, 120 bpm ---
bpm=120;beat=60/bpm;bar=4*beat
chords=[[57,60,64],[53,57,60],[60,64,67],[55,59,62]];roots=[33,29,36,31]
arp=[0,1,2,1,2,1,0,1]
for b_ in range(int(dur/bar)+1):
    t0=b_*bar;c=chords[b_%4];r=roots[b_%4];lvl=float(kf(t0,PCT))/100
    add(pad([note(m) for m in c],bar),t0,0,0.05)
    for k in range(8): add(pluck(note(c[arp[k]%3]+12+(12 if k==7 else 0)),0.28),t0+k*beat/2,0.3 if k%2 else -0.3,0.07+0.12*lvl)
    for k in range(8): add(bass(note(r),beat*0.55),t0+k*beat/2,0,0.22)
    for k in range(4):
        add(kick(),t0+k*beat,0,0.34)
        if k%2==1: add(snare(),t0+k*beat,0,0.12+0.08*lvl)
        add(hat(),t0+k*beat+beat/2,0.2,0.05+0.03*lvl)
# motor del velocímetro: tono que sube con el porcentaje
t=np.arange(n)/sr; fr=140+3.2*kf(t,PCT); ph=2*np.pi*np.cumsum(fr)/sr
eng=lp(sg.sawtooth(ph),900); out+=(eng*0.035)[:,None]
# --- efectos ---
add(glitch(),1.9,0,0.25); add(boom(),2.64,0,0.3); add(glitch(0.3),2.64,0,0.2)
add(riser(0.55),4.4,0,0.22); add(ding(1568,0.7),4.95,0,0.16); add(ding(2093,0.5),4.97,0.2,0.1)
for t_ in (5.6,5.88,6.16): add(pop(800),t_,0,0.13)
add(pop(500),7.2,0,0.14); add(ding(880,0.3),7.4,0,0.06)
for s_ in SC: add(whoosh(),s_-0.35,0,0.14); add(glitch(0.25),s_-0.12,0,0.16)
for s_ in (8.75,14.8,24.15,29.2,35.9): add(boom(),s_,0,0.22)
for c in CLICKS: add(tick(),c,0,0.3); add(pop(900),c+0.02,0.2,0.06)
add(pop(600),9.95,0,0.12); add(buzz(0.35),11.2,0,0.08)
add(sweep(900,60,1.2),12.15,0,0.1); add(ding(1046,0.5),13.5,0,0.1); add(ding(1568,0.5),13.62,0,0.1); add(ding(2093,0.6),13.75,0.2,0.1)
for t_ in (16.32,17.04,17.76): add(clack(),t_,0,0.3); add(pop(400),t_,0,0.08)
add(pop(500),18.4,0,0.14)
add(boom(),23.35,0,0.25); add(whoosh(0.4),23.4,0,0.1)
for t_ in (27.2,27.85,28.5): add(ding(1200+int((t_-27)*300),0.35),t_+0.05,0.2,0.09)
add(ding(1046,0.6),29.3,0,0.14); add(riser(0.3,400,3000),29.0,0,0.14)
add(ding(1318,0.5),32.5,0,0.15); add(sweep(300,1800,1.7),33.6,0,0.08); add(ding(1760,0.5),35.0,0,0.12)
# 100% fanfarria
add(riser(0.4,300,3500),35.15,0,0.2); add(boom(),35.55,0,0.35)
for k,m in enumerate([69,73,76,81,85,88]): add(ding(note(m),0.9),35.55+k*0.07,0,0.1)
for t_ in (37.64,38.24,39.84): add(pop(750),t_,0,0.12)
for t_ in (41.3,42.0,42.45,42.9,43.3): add(pop(600+int((t_-41)*60)),t_,0,0.12)
add(pop(500),43.75,0,0.12); add(pop(300),44.35,0,0.22); add(tick(),44.35,0,0.3)
for k,m in enumerate([72,76,79,84,88]): add(ding(note(m),0.7),44.4+k*0.06,0,0.1)
tt=np.arange(n)/sr
out*=(np.minimum(1,tt/0.2)*np.minimum(1,(dur-tt)/1.3))[:,None]
out=np.tanh(out*1.15)/1.15
rms=np.sqrt(np.mean(out**2));out*=10**(-20/20)/rms
out=np.clip(out,-0.98,0.98)
wf.write('musica.wav',sr,(out*32767).astype(np.int16)); print('ok')

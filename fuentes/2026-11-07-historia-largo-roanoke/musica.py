import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, json
sr=44100; DUR=json.load(open('data.json'))['dur']; n=int(DUR*sr)
out=np.zeros((n,2)); rng=np.random.default_rng(11)
def T(d): return np.arange(int(d*sr))/sr
def hz(m): return 440*2**((m-69)/12)
def lp(x,fc,o=2): b,a=sg.butter(o,fc/(sr/2)); return sg.lfilter(b,a,x)
def hp(x,fc,o=2): b,a=sg.butter(o,fc/(sr/2),'high'); return sg.lfilter(b,a,x)
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*sr)
    if i>=n: return
    if i<0: sig=sig[-i:]; i=0
    j=min(n,i+len(sig)); l=np.sqrt(.5*(1-pan)); r=np.sqrt(.5*(1+pan))
    out[i:j,0]+=sig[:j-i]*g*l; out[i:j,1]+=sig[:j-i]*g*r
# --- pad de acordes (re menor) ---
CH=[[50,53,57,62],[46,50,53,58],[43,50,55,58],[45,49,52,57],[50,53,57,60],[46,53,58,62],[43,46,50,55],[45,52,57,61]]
CL=8.0
t=0;k=0
while t<DUR:
    ch=CH[k%len(CH)]; d=CL+2.5; tt=T(d)
    env=np.minimum(1,tt/2.5)*np.minimum(1,(d-tt)/2.5)
    s=np.zeros(len(tt))
    for m in ch:
        f=hz(m)
        for det in (-0.12,0.1):
            s+=sg.sawtooth(2*np.pi*f*(1+det/100)*tt+rng.random()*6)*0.5
        s+=np.sin(2*np.pi*f/2*tt)*0.6
    s=lp(s,700+250*np.sin(k*.7),2)*env
    add(s,t,0.05,pan=(-.25 if k%2 else .25))
    # nota grave
    b=np.sin(2*np.pi*hz(ch[0]-12)*tt)*env; add(b,t,0.09)
    t+=CL;k+=1
# --- arpa/caja de música suave ---
def pluck(f,d=2.2):
    tt=T(d); s=(np.sin(2*np.pi*f*tt)+.35*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*3)+.12*np.sin(2*np.pi*3*f*tt)*np.exp(-tt*6))*np.exp(-tt*2.2)
    return s*np.minimum(1,tt*300)
t=4.0;k=0
while t<DUR-4:
    ch=CH[int(t//CL)%len(CH)]; m=ch[[0,2,1,3,2,1][k%6]]+12
    if not (364<t<373): add(pluck(hz(m)),t,0.05,pan=np.sin(k)*.5)
    t+= 1.5 if (k%4!=3) else 3.0; k+=1
# --- golpes en los giros ---
def boom(d=3.0):
    tt=T(d); f=38+30*np.exp(-tt*6); s=np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*1.6)
    nz=lp(rng.standard_normal(len(tt)),180)*np.exp(-tt*3)*0.5
    return s+nz
def swell(d=1.6):
    tt=T(d); s=hp(lp(rng.standard_normal(len(tt)),3000),300)*(tt/d)**2.5; return s*0.6
def thud():
    tt=T(0.35); return lp(rng.standard_normal(len(tt)),900)*np.exp(-tt*18)*0.9+np.sin(2*np.pi*90*tt)*np.exp(-tt*20)
def bell(f=hz(74),d=4):
    tt=T(d); return (np.sin(2*np.pi*f*tt)+.5*np.sin(2*np.pi*f*2.76*tt)*np.exp(-tt*2)+.3*np.sin(2*np.pi*f*5.4*tt)*np.exp(-tt*4))*np.exp(-tt*1.1)
BIG=[30.55,89.4,238.2,259.0,280.7,307.0,377.6,425.6]
for x in BIG: add(swell(),x-1.6,0.18); add(boom(),x,0.42); add(bell(),x,0.05,pan=.3)
CAPS=[44.4,106.0,166.7,221.6,287.5,359.5,399.6]
for x in CAPS: add(swell(1.2),x-1.2,0.12); add(boom(2.2),x,0.25); add(bell(hz(69),5),x+0.1,0.06,pan=-.3)
STAMPS=[16.2,17.5,93.8,116.4,137.5,164.6,199.8,243.4,342.8,356.0,396.0,42.2]
for x in STAMPS: add(thud(),x,0.25)
# tormenta
tt=T(9.5); rum=lp(rng.standard_normal(len(tt)),250)*np.minimum(1,tt/1.5)*np.minimum(1,(9.5-tt)/1.5); add(rum,364.0,0.35)
rain=hp(rng.standard_normal(len(tt)),2500)*np.minimum(1,tt/1.5)*np.minimum(1,(9.5-tt)/1.5); add(rain,364.0,0.04)
for x in [366.6,367.1,369.9,371.4]: add(boom(2.5),x+0.15,0.3)
# fundido de entrada/salida
env=np.ones(n); a=int(1.5*sr); env[:a]=np.linspace(0,1,a); b=int(3.5*sr); env[-b:]=np.linspace(1,0,b)
out*=env[:,None]
# normalizar a ~ -22 dB RMS
rms=np.sqrt(np.mean(out**2)); out*=10**(-22/20)/rms
pk=np.abs(out).max()
if pk>0.89: out*=0.89/pk
wf.write('musica.wav',sr,(out*32767).astype(np.int16))
print('rms dB',20*np.log10(np.sqrt(np.mean(out**2))),'peak',np.abs(out).max())

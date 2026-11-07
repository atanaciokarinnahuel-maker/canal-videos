# Música de misterio generada con código (sin voz). Golpes en los giros. Nivel medio ≈ -20 dB.
import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, json
d=json.load(open('words.json')); T=d['tempo']
def W(txt,n=0):
    k=0
    for w in d['words']:
        if w['t'].startswith(txt):
            if k==n: return w['s']
            k+=1
sr=44100; dur=d['voice_dur']+1.3; n=int(dur*sr); out=np.zeros((n,2)); rng=np.random.default_rng(7)
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*sr)
    if i>=n or i<0: return
    j=min(n,i+len(sig)); l=np.sqrt(0.5*(1-pan)); r=np.sqrt(0.5*(1+pan))
    out[i:j,0]+=sig[:j-i]*g*l; out[i:j,1]+=sig[:j-i]*g*r
def note(m): return 440*2**((m-69)/12)
def lp(x,fc,o=2): b,a=sg.butter(o,fc/(sr/2)); return sg.lfilter(b,a,x)
def TT(x): return np.arange(int(x*sr))/sr
def pad(fs,dd):
    t=TT(dd); s=sum(np.sin(2*np.pi*f*t)*0.5+sg.sawtooth(2*np.pi*f*1.004*t)*0.12 for f in fs); return lp(s,1200)*np.minimum(1,t/1.2)*np.minimum(1,(dd-t)/1.2)
def bell(f,dd=2.2):
    t=TT(dd); return (np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*3)+0.25*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*6))*np.exp(-t*2.2)*np.minimum(1,t*600)
def pulse(f):
    t=TT(0.5); return lp(np.sin(2*np.pi*f*t)+0.3*sg.square(2*np.pi*f*t),300)*np.exp(-t*7)
def boom():
    t=TT(2.5); th=np.sin(2*np.pi*np.cumsum(38+70*np.exp(-t*9))/sr)*np.exp(-t*1.6); nz=lp(rng.standard_normal(len(t)),900)*np.exp(-t*4)*.5; return th*1.3+nz
def hit():
    t=TT(0.6); return lp(rng.standard_normal(len(t)),3000)*np.exp(-t*14)*0.8+np.sin(2*np.pi*90*t)*np.exp(-t*10)
def whoosh(dd=.5):
    t=TT(dd); s=lp(rng.standard_normal(len(t)),2500); return s*np.sin(np.pi*t/dd)**2*0.5
def click():
    t=TT(0.04); return lp(rng.standard_normal(len(t)),5000)*np.exp(-t*160)
def scrape(dd=.35):
    t=TT(dd); s=sg.lfilter(*sg.butter(2,[1500/(sr/2),5000/(sr/2)],'band'),rng.standard_normal(len(t))); return s*np.exp(-t*5)*(0.6+0.4*np.sin(2*np.pi*35*t))
def riser(dd):
    t=TT(dd); nz=rng.standard_normal(len(t)); a=lp(nz,900); b=lp(nz,4000); m=t/dd; return (a*(1-m)+b*m)*m**2*0.5
def rain(dd):
    t=TT(dd); return lp(rng.standard_normal(len(t)),4000)*0.25*np.minimum(1,t/.3)*np.minimum(1,(dd-t)/.3)
# ---- lecho: Re menor, 72 bpm, drone + pulso de corazón + campanas lejanas ----
bpm=72; beat=60/bpm; bar=4*beat
chords=[[50,57,62,65],[46,53,58,62],[48,55,60,64],[45,52,57,61]]
for b in range(int(dur/bar)+1):
    t0=b*bar; c=chords[b%4]; add(pad([note(m) for m in c],bar+1.2),t0,0,0.05)
    for k in range(4): add(pulse(note(c[0]-12)),t0+k*beat,0,0.22 if k%2==0 else 0.12)
    add(bell(note(c[2]+24)),t0+beat*2.5,0.4 if b%2 else -0.4,0.05)
add(lp(rng.standard_normal(n),180)*0.08,0)  # rumor grave
# ---- golpes en los giros ----
for t in [0.0, W('nadie.'), W('desaparecidas.'), W('cruz.'), W('CROATOAN.'), W('ninguna')]: add(boom(),max(0,t-0.03),0,0.55)
for t in [W('1587,'), W('1590.'), W('sino'), W('Ahora,')]: add(hit(),t,0,0.35)
# tallado de letras (C R O y CROATOAN) y de la tabla
for t in [W('C…'),W('R…'),W('O.')]: add(scrape(),t,0.2,0.5)
for i in range(8): add(scrape(.25),W('CROATOAN.')+i*.06,(i-4)/6,0.25)
T1=W('CROATOAN.'); step=(T1-0.6)/8
for i in range(8): add(scrape(.3),0.6+(i+1)*step-.5,0.6,0.12)
# máquina de escribir
for t0,nch in [(0.05,15),(12.7/T+0.1,4),(30.8/T,10)]:
    for k in range(nch): add(click(),t0+k/14,0.3,0.35)
# transiciones (whoosh) en cada cambio de escena
S=[2.0,4.6,6.5,7.85,10.25,12.7,14.95,16.45,18.7,21.0,23.35,25.2,26.45,27.95,29.4,30.8,32.55,34.6,36.65,38.65,40.55,41.95,43.25,44.65,47.1,48.95,51.05,53.45,54.65,55.95,58.25]
for s in S: add(whoosh(.45),s/T-.25,0,0.10)
add(riser(2.0),T1-2.0,0,0.5); add(riser(1.6),W('ninguna')-1.6,0,0.45)
add(rain(2.4),51.05/T,0,0.6); add(boom(),51.6/T,0,0.35)
# fade final
f=int(1.5*sr); out[-f:]*=np.linspace(1,0,f)[:,None]
x=out/np.max(np.abs(out))*0.9
rms=np.sqrt(np.mean(x**2)); target=10**(-20/20); x=x*min(1.0,target/rms) if rms>0 else x
x=np.clip(x,-0.98,0.98)
wf.write('musica.wav',sr,(x*32767).astype(np.int16)); print('ok',dur)

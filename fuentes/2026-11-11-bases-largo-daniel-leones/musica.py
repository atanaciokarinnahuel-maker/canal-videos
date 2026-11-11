#!/usr/bin/env python3
"""Música y efectos del documental (síntesis propia con numpy, sin samples ni IA).
Colchón de cuerdas + ney + arpa + tambor, cambia por capítulo; viento, rugidos lejanos, sello, piedra.
Uso: musica.py salida.wav   (lee data.json)"""
import numpy as np, json, scipy.signal as sg, wave, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); D=json.load(open(os.path.join(HERE,'data.json')))
sr=44100; dur=D['dur']; N=int(dur*sr); rng=np.random.default_rng(6)
out=np.zeros((N,2),np.float32); rev=np.zeros((N,2),np.float32)
def add(sig,t,g=1.0,pan=0.0,send=0.3):
    i=int(t*sr)
    if i<0: sig=sig[-i:]; i=0
    j=min(N,i+len(sig))
    if j<=i: return
    s=(sig[:j-i]*g).astype(np.float32); l=np.sqrt(.5*(1-pan)); r=np.sqrt(.5*(1+pan))
    out[i:j,0]+=s*l; out[i:j,1]+=s*r; rev[i:j,0]+=s*l*send; rev[i:j,1]+=s*r*send
def T(d): return np.arange(int(d*sr),dtype=np.float32)/sr
def hz(m): return 440*2**((m-69)/12)
def lp(x,fc,o=2): b,a=sg.butter(o,fc/(sr/2)); return sg.lfilter(b,a,x).astype(np.float32)
def bp(x,lo,hi,o=2): b,a=sg.butter(o,[lo/(sr/2),hi/(sr/2)],'band'); return sg.lfilter(b,a,x).astype(np.float32)
def S(b,i): return next(f['a'] for f in D['frases'] if f['b']==b and f['i']==i)
B={b['bloque']:(b['a'],b['e']) for b in D['bloques']}; CARD={c['bloque']:c['a'] for c in D['tarjetas']}; TIT=D['titulo']['a']

# ---------------- instrumentos ----------------
def pad(f,d,att=1.8,rel=2.6,bright=.5,det=1.0):
    t=T(d+rel); x=np.zeros(len(t),np.float32)
    for k,a in ((1,1.0),(2,.25+.4*bright),(3,.34*bright),(4,.2*bright),(5,.12*bright),(6,.06*bright)):
        x+=a*np.sin(2*np.pi*f*det*k*t+k*1.3*det)
    env=np.minimum(1,t/att)*np.clip((d+rel-t)/rel,0,1)*(1+.06*np.sin(2*np.pi*.23*t+f))
    return x*env
def pluck(f,d=2.6):
    t=T(d); x=np.zeros(len(t),np.float32)
    for k in range(1,9): x+=(1/k)*np.sin(2*np.pi*f*k*t)*np.exp(-t*(1.3+.9*k))
    return x*np.minimum(1,t*300)
def ney(f0,f1,d):
    t=T(d); f=f1+(f0-f1)*np.exp(-t/.07); vib=1+.007*np.sin(2*np.pi*5.1*t)*np.minimum(1,t/.7)
    ph=2*np.pi*np.cumsum(f*vib)/sr; x=np.sin(ph)+.22*np.sin(2*ph)+.07*np.sin(3*ph)
    br=bp(rng.standard_normal(len(t)).astype(np.float32),f1*1.6,f1*3.2)*.5
    env=np.minimum(1,t/.14)*np.clip((d-t)/.3,0,1)*(.85+.15*np.sin(2*np.pi*.6*t))
    return (x+br)*env
def drum(f=62,d=.9):
    t=T(d); x=np.sin(2*np.pi*np.cumsum(f*.75+f*1.1*np.exp(-t*26))/sr)*np.exp(-t*5.5)
    return x+lp(rng.standard_normal(len(t)).astype(np.float32),900)*np.exp(-t*30)*.5
def taiko(d=2.4):
    t=T(d); x=np.sin(2*np.pi*np.cumsum(36+95*np.exp(-t*14))/sr)*np.exp(-t*2.6)*1.3
    return x+lp(rng.standard_normal(len(t)).astype(np.float32),1800)*np.exp(-t*9)*.7
def swell(d=1.6,lo=500,hi=6000):
    t=T(d); x=bp(rng.standard_normal(len(t)).astype(np.float32),lo,hi); return x*(t/d)**2.6*np.clip((d-t)/.05,0,1)
def bell(f,d=3.0):
    t=T(d); x=sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*(1.1+r*.5)) for r,a in ((1,1),(2.01,.5),(3.02,.25),(4.2,.12)))
    return x*np.minimum(1,t*400)
def wind(d,g0=1,g1=1):
    n=int(d*sr); x=np.cumsum(rng.standard_normal(n)).astype(np.float32); x-=sg.lfilter(np.ones(4000)/4000,1,x).astype(np.float32)
    x=bp(x,180,1100); x/=np.max(np.abs(x))+1e-9; t=np.arange(n)/sr
    lfo=.55+.45*np.sin(2*np.pi*.11*t+1)*np.sin(2*np.pi*.047*t+.3)
    return x*lfo*np.linspace(g0,g1,n)*np.minimum(1,t/2)*np.clip((d-t)/2.5,0,1)
def growl(d=2.4,f0=64):
    t=T(d); f=f0*(1-.18*t/d)*(1+.03*np.sin(2*np.pi*3.1*t)); ph=2*np.pi*np.cumsum(f)/sr
    src=sg.sawtooth(ph).astype(np.float32)+.6*sg.sawtooth(ph*.5+1).astype(np.float32)
    rough=.55+.45*np.sin(2*np.pi*(27+4*np.sin(2*np.pi*.7*t))*t+rng.random()*6)
    x=bp(src*rough,180,420)*1.4+bp(src*rough,480,820)*.8+bp(src,900,1500)*.25+lp(rng.standard_normal(len(t)).astype(np.float32),1400)*.12*rough
    env=np.minimum(1,t/.35)**1.5*np.clip((d-t)/(d*.55),0,1)**1.4
    return lp(x*env,1700)
def stone(d=3.2):
    t=T(d); x=np.cumsum(rng.standard_normal(len(t))).astype(np.float32); x-=sg.lfilter(np.ones(2000)/2000,1,x).astype(np.float32)
    x=lp(x,520); x/=np.max(np.abs(x))+1e-9; wob=.6+.4*np.sin(2*np.pi*(7+2*np.sin(2*np.pi*.5*t))*t)
    return x*wob*np.minimum(1,t/.3)*np.clip((d-t)/.25,0,1)

# ---------------- armonía por secciones ----------------
CH={'Dm':[38,50,57,62,65],'Bb':[34,46,53,58,62],'F':[41,53,57,60,65],'C':[36,48,55,60,64],'Gm':[43,50,55,58,62],'A':[45,52,57,61,64],
    'D':[38,50,57,62,66],'G':[43,50,55,59,62],'Bm':[35,47,54,59,62,66],'Eb':[39,51,58,63,67],'Cm':[36,48,55,60,63],'D5':[26,38,45,50],'Dsus':[38,50,57,62,67],'Dp':[38,50,57,62,66,63]}
MOT={'min':[[69,67,65,64,62],[62,65,69,67],[74,72,69,70,69],[65,67,69,72,70,69]],'phr':[[62,63,66,63,62],[69,70,69,66,67],[66,67,69,70,69]],
     'maj':[[66,69,74,73,71,69],[62,66,69,71,69],[74,73,69,66,67,66],[69,71,74,78,76,74]]}
def section(t0,t1,chords,cd=6.0,g=(1,1),bright=.5,pulse=0,pg=.5,arp=0,lead=None,lg=.5,every=13,hi=0):
    k=0; t=t0
    while t<t1-.5:
        d=min(cd,t1-t); u=(t-t0)/max(1e-6,t1-t0); gg=g[0]+(g[1]-g[0])*u; notes=CH[chords[k%len(chords)]]
        for j,m in enumerate(notes):
            a=(.9 if j<2 else .55)/len(notes)*4
            add(pad(hz(m),d,bright=bright,det=.9975),t,gg*a*.5,-.55,send=.5); add(pad(hz(m),d,bright=bright,det=1.0025),t,gg*a*.5,.55,send=.5)
        if hi: add(pad(hz(notes[-1]+12),d,att=3,bright=.2),t,gg*hi*.3,0,send=.8)
        if arp:
            seq=[notes[1],notes[2],notes[3],notes[-1],notes[3],notes[2]]
            for q,m in enumerate(seq):
                if t+q*1.0<t1-.3: add(pluck(hz(m+12)),t+q*1.0,gg*arp*.5,(-1)**q*.35,send=.6)
        t+=d; k+=1
    if pulse:
        t=t0+pulse
        while t<t1-.3:
            u=(t-t0)/(t1-t0); gg=(g[0]+(g[1]-g[0])*u)*pg
            add(drum(),t,gg*.9,0,send=.25); add(drum(50,.7),t+.32,gg*.5,0,send=.25); t+=pulse
    if lead:
        t=t0+4.5; q=0; R=np.random.default_rng(int(t0*10))
        while t<t1-7:
            mot=MOT[lead][R.integers(len(MOT[lead]))]; tt=t; prev=mot[0]
            for m in mot:
                d=float(R.choice([.9,1.2,1.6,2.2])); add(ney(hz(prev),hz(m),d+.25),tt,lg*.55,.15,send=.9); tt+=d; prev=m
            t=tt+every*(.7+.6*R.random())

c2,c3,c4,c5,c6,c7,c8,c9,c10,c11=[CARD[k]-.6 for k in range(2,12)]
tT=TIT-.3; e11=B[11][1]; a12=B[12][0]; e12=B[12][1]; a13=B[13][0]
t_vivo=S(9,6); t_angel=S(8,9); t_sello=S(4,6); t_piedra=S(7,8); t_cita=S(7,5); t_perm=S(12,7)
section(0,tT,['D5'],cd=8,g=(.7,1.1),bright=.35,pulse=2.6,pg=.55)                                  # apertura: tensión
section(tT,c2,['Dm','Bb','Dm'],cd=3.4,g=(1.15,.85),bright=.8,hi=.8)                                # título
section(c2,c3,['Dm','Bb','F','C'],g=(.9,.9),bright=.5,arp=.55,lead='min',lg=.45,every=15)        # el imperio y el hombre fiel
section(c3,c4,['Dp','Eb','Dp','Cm'],cd=7,g=(.8,1.0),bright=.4,pulse=3.0,pg=.4,lead='phr',lg=.3,every=17)   # conspiración
section(c4,c5,['D','Eb','D','Cm'],cd=6,g=(.85,1.05),bright=.55,pulse=2.4,pg=.5)                   # una ley contra Dios
section(c5,c6,['Bb','F','Gm','Dm'],g=(.9,.95),bright=.45,arp=.4,lead='min',lg=.5,every=12,hi=.4)  # oración
section(c6,c7,['Dm','C','Bb','A'],g=(.8,1.15),bright=.6,pulse=2.0,pg=.55)                         # acusación
section(c7,t_cita-.5,['D5','Dm'],cd=7,g=(.9,1.0),bright=.35,pulse=3.2,pg=.75)                     # hacia el foso
section(t_cita-.5,t_piedra,['Bb','Gm','Dm'],cd=5,g=(.9,.8),bright=.4,hi=.5)                       # «él te libre»
section(t_piedra,c8,['D5'],cd=8,g=(.9,.6),bright=.25)                                             # piedra sellada
section(c8,t_angel-.6,['Dm','Gm','Bb','Dm'],cd=7,g=(.7,.75),bright=.3,lead='min',lg=.55,every=11,hi=.5)  # noche
section(t_angel-.6,c9,['Bb','F','C'],cd=5,g=(.9,1.05),bright=.55,hi=.9)                           # el ángel
section(c9,t_vivo-.3,['F','C','Dm','Bb'],cd=6,g=(.7,.95),bright=.45,arp=.35,hi=.4)                # amanecer
section(t_vivo-.3,c10,['D','G','Bm','A'],cd=6,g=(1.25,1.0),bright=.7,arp=.5,hi=.9,lead='maj',lg=.4,every=14)   # ¡vivo!
section(c10,c11,['D','G','Bm','A'],g=(.9,.95),bright=.55,arp=.45,hi=.5)                           # sale del foso
section(c11,S(11,5),['D','A','Bm','G'],g=(.92,.88),bright=.7,hi=.8,arp=.4)                        # el Dios viviente
section(S(11,5),a12-.5,['Bm','G','D','A'],g=(.75,.7),bright=.4,lead='maj',lg=.4,every=15,hi=.4)   # reflexión (+ pausa)
section(a12-.5,t_perm-.4,['Bm','G','D','A'],cd=5.5,g=(.8,1.1),bright=.55,arp=.4,hi=.6)            # aplicación
section(t_perm-.4,a13-1.2,['D','G','D'],cd=4.2,g=(1.2,.75),bright=.85,hi=1.0)                      # «permanece para siempre» + negro
section(a13-1.2,dur,['D','G','D','A'],cd=6,g=(.75,.8),bright=.45,arp=.45,hi=.4)                   # cierre

# ---------------- golpes y efectos ----------------
add(wind(16,1,.3),0,.55,0,send=.3); add(wind(c9-c8+4,.5,.6),c8-2,.22,0,send=.3); add(wind(8,.6,.6),e12-.5,.2,0,send=.3)
for t,g,f in [(.9,.5,60),(6.6,.42,68),(S(1,6)+.2,.4,62),(S(1,7)+3.5,.38,70),(S(1,12)+.3,.42,58),(S(4,3)+2.4,.4,64),(S(5,9)+.4,.34,66),(S(6,7)+.6,.38,60),
              (S(6,15)+.8,.42,64),(S(7,1)+1.9,.42,58),(S(7,10)+.5,.4,66),(S(7,11)+1.5,.34,60),(S(8,3)+.3,.3,62),(S(9,4)+1.2,.3,66)]:
    add(growl(2.2+rng.random()*1.0,f),t,g,rng.uniform(-.5,.5),send=1.6)
add(swell(2.4,200,3000),tT-2.3,.5,0,.6); add(taiko(3.2),tT+.3,1.15,0,.7); add(bell(hz(62),4),tT+.4,.25,0,1); add(bell(hz(74),4),tT+1.9,.14,0,1)
for k,c in CARD.items():
    add(swell(1.3),c-1.0,.22,0,.6); add(taiko(2.0),c+.25,.7,0,.6)
add(drum(70,.5),S(1,5)+.9,.9,0,.4)                                                         # "firmado el decreto"
add(drum(48,1.2),t_sello+.75,1.4,0,.6); add(taiko(2.2),t_sello+.78,.6,0,.7)               # el sello
add(swell(2.0,150,1200),S(4,7)-1.2,.3,0,.6); add(taiko(2.6),S(4,7)+2.6,.55,0,.7)           # "no podía ser revocado"
add(stone(3.4),t_piedra+.3,.9,-.1,.5); add(taiko(3.0),t_piedra+3.5,1.3,0,.9)               # la piedra
add(taiko(2.6),S(7,10)+.3,.7,0,.9)                                                         # "quedó cerrada"
for i,m in enumerate([74,78,81,86]): add(bell(hz(m),4.5),t_angel+.5+i*.45,.22,(-1)**i*.4,1.2)   # el ángel
add(swell(1.8),t_vivo-1.6,.3,0,.6)
for i,m in enumerate([62,66,69,74,78,81]): add(bell(hz(m),5),t_vivo+.15+i*.16,.26,(-1)**i*.5,1.2)   # "Daniel estaba vivo"
add(swell(2.6,300,5000),t_perm-2.4,.45,0,.6); add(taiko(3.4),t_perm+.2,1.0,0,.8)
for i,m in enumerate([62,69,74,78]): add(bell(hz(m),6),t_perm+.3+i*.3,.24,(-1)**i*.4,1.2)

# ---------------- reverberación, nivel y salida ----------------
ir_t=T(3.0); wet=np.zeros_like(out)
for ch in range(2):
    ir=lp(rng.standard_normal(len(ir_t)).astype(np.float32),5200)*np.exp(-ir_t*2.1)*np.minimum(1,ir_t/.012); ir/=np.sqrt(np.sum(ir**2))
    wet[:,ch]=sg.oaconvolve(rev[:,ch],ir)[:N].astype(np.float32)
mix=out+wet*.55
b,a=sg.butter(2,28/(sr/2),'high'); mix=sg.lfilter(b,a,mix,axis=0).astype(np.float32)
b,a=sg.butter(1,230/(sr/2)); mix=mix-.42*sg.lfilter(b,a,mix,axis=0).astype(np.float32)   # menos graves: deja lugar a la voz
tt=np.arange(N)/sr; mix*=(np.minimum(1,tt/1.2)*np.clip((dur-tt)/3.5,0,1))[:,None].astype(np.float32)
rms=np.sqrt(np.mean(mix**2)); mix*=10**(-21/20)/rms; mix=np.tanh(mix*1.15)/1.15
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes()); w.close()
print('música ok',round(dur,2),'s  pico',float(np.max(np.abs(mix))))

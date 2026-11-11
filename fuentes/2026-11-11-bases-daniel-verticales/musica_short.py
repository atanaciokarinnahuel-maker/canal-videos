#!/usr/bin/env python3
"""Música y efectos de una pieza vertical (síntesis propia). Uso: musica_short.py <cfg.json> <salida.wav>"""
import numpy as np, json, scipy.signal as sg, wave, sys
C=json.load(open(sys.argv[1])); sr=44100; dur=C['dur']; N=int(dur*sr); rng=np.random.default_rng(len(C['id'])*7+3)
out=np.zeros((N,2),np.float32); rev=np.zeros((N,2),np.float32)
def add(sig,t,g=1.0,pan=0.0,send=0.3):
    i=int(t*sr)
    if i<0: sig=sig[-i:]; i=0
    j=min(N,i+len(sig))
    if j<=i: return
    s=(sig[:j-i]*g).astype(np.float32); l=np.sqrt(.5*(1-pan)); r=np.sqrt(.5*(1+pan)); out[i:j,0]+=s*l; out[i:j,1]+=s*r; rev[i:j,0]+=s*l*send; rev[i:j,1]+=s*r*send
T=lambda d: np.arange(int(d*sr),dtype=np.float32)/sr
hz=lambda m: 440*2**((m-69)/12)
def lp(x,fc,o=2): b,a=sg.butter(o,fc/(sr/2)); return sg.lfilter(b,a,x).astype(np.float32)
def bp(x,lo,hi,o=2): b,a=sg.butter(o,[lo/(sr/2),hi/(sr/2)],'band'); return sg.lfilter(b,a,x).astype(np.float32)
def pad(f,d,att=1.2,rel=2.0,bright=.5,det=1.0):
    t=T(d+rel); x=np.zeros(len(t),np.float32)
    for k,a in ((1,1.0),(2,.25+.4*bright),(3,.34*bright),(4,.2*bright),(5,.12*bright),(6,.06*bright)): x+=a*np.sin(2*np.pi*f*det*k*t+k*1.3*det)
    return x*np.minimum(1,t/att)*np.clip((d+rel-t)/rel,0,1)*(1+.06*np.sin(2*np.pi*.23*t+f))
def pluck(f,d=2.4):
    t=T(d); x=np.zeros(len(t),np.float32)
    for k in range(1,9): x+=(1/k)*np.sin(2*np.pi*f*k*t)*np.exp(-t*(1.3+.9*k))
    return x*np.minimum(1,t*300)
def drum(f=62,d=.9):
    t=T(d); return np.sin(2*np.pi*np.cumsum(f*.75+f*1.1*np.exp(-t*26))/sr)*np.exp(-t*5.5)+lp(rng.standard_normal(len(t)).astype(np.float32),900)*np.exp(-t*30)*.5
def taiko(d=2.4):
    t=T(d); return np.sin(2*np.pi*np.cumsum(36+95*np.exp(-t*14))/sr)*np.exp(-t*2.6)*1.3+lp(rng.standard_normal(len(t)).astype(np.float32),1800)*np.exp(-t*9)*.7
def swell(d=1.6,lo=500,hi=6000):
    t=T(d); return bp(rng.standard_normal(len(t)).astype(np.float32),lo,hi)*(t/d)**2.6*np.clip((d-t)/.05,0,1)
def whoosh(d=.5):
    t=T(d); return bp(rng.standard_normal(len(t)).astype(np.float32),400,5000)*np.exp(-((t-d*.5)/(d*.22))**2)
def bell(f,d=3.0):
    t=T(d); return sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*(1.1+r*.5)) for r,a in ((1,1),(2.01,.5),(3.02,.25),(4.2,.12)))*np.minimum(1,t*400)
def growl(d=2.4,f0=64):
    t=T(d); f=f0*(1-.18*t/d)*(1+.03*np.sin(2*np.pi*3.1*t)); ph=2*np.pi*np.cumsum(f)/sr
    src=sg.sawtooth(ph).astype(np.float32)+.6*sg.sawtooth(ph*.5+1).astype(np.float32); rough=.55+.45*np.sin(2*np.pi*(27+4*np.sin(2*np.pi*.7*t))*t+rng.random()*6)
    x=bp(src*rough,180,420)*1.4+bp(src*rough,480,820)*.8+bp(src,900,1500)*.25
    return lp(x*np.minimum(1,t/.35)**1.5*np.clip((d-t)/(d*.55),0,1)**1.4,1700)
def stone(d=3.0):
    t=T(d); x=np.cumsum(rng.standard_normal(len(t))).astype(np.float32); x-=sg.lfilter(np.ones(2000)/2000,1,x).astype(np.float32); x=lp(x,520); x/=np.max(np.abs(x))+1e-9
    return x*(.6+.4*np.sin(2*np.pi*(7+2*np.sin(2*np.pi*.5*t))*t))*np.minimum(1,t/.3)*np.clip((d-t)/.25,0,1)
CH={'Dm':[38,50,57,62,65],'Bb':[34,46,53,58,62],'F':[41,53,57,60,65],'C':[36,48,55,60,64],'Gm':[43,50,55,58,62],'A':[45,52,57,61,64],'D':[38,50,57,62,66],'G':[43,50,55,59,62],
    'Bm':[35,47,54,59,62,66],'Eb':[39,51,58,63,67],'Cm':[36,48,55,60,63],'D5':[26,38,45,50],'Dp':[38,50,57,62,66,63]}
def section(t0,t1,chords,cd=5.0,g=(1,1),bright=.5,pulse=0,pg=.5,arp=0,hi=0):
    k=0; t=t0
    while t<t1-.4:
        d=min(cd,t1-t); gg=g[0]+(g[1]-g[0])*(t-t0)/max(1e-6,t1-t0); notes=CH[chords[k%len(chords)]]
        for j,m in enumerate(notes):
            a=(.9 if j<2 else .55)/len(notes)*4
            add(pad(hz(m),d,bright=bright,det=.9975),t,gg*a*.5,-.55,.5); add(pad(hz(m),d,bright=bright,det=1.0025),t,gg*a*.5,.55,.5)
        if hi: add(pad(hz(notes[-1]+12),d,att=2,bright=.2),t,gg*hi*.3,0,.8)
        if arp:
            seq=[notes[1],notes[2],notes[3],notes[-1],notes[3],notes[2]]
            for q,m in enumerate(seq):
                if t+q*.83<t1-.3: add(pluck(hz(m+12)),t+q*.83,gg*arp*.5,(-1)**q*.35,.6)
        t+=d; k+=1
    if pulse:
        t=t0+pulse*.5
        while t<t1-.2:
            gg=(g[0]+(g[1]-g[0])*(t-t0)/(t1-t0))*pg; add(drum(),t,gg*.9,0,.25); add(drum(50,.7),t+.3,gg*.5,0,.25); t+=pulse
mood=C['mood']; cta=C['cta']; cuts=[p['t'] for p in C['planos'][1:]]; F=C['frases']
if mood=='trailer':
    tc=C['title_card']; section(0,tc[0],['D5','Dp','D5','Eb'],cd=6,g=(.8,1.3),bright=.5,pulse=1.5,pg=.7); section(tc[0],dur,['Dm','Bb','D'],cd=3.4,g=(1.3,.9),bright=.8,hi=.9)
    for a,e in F[:-1]: add(taiko(1.8),a-.15,.75,0,.6)
    add(growl(2.2,60),.3,.5,-.3,1.5); add(growl(2.4,66),F[3][0]+2.0,.5,.3,1.5); add(growl(2.0,58),F[5][0]+1.0,.4,-.2,1.5)
    add(swell(2.2,200,4000),tc[0]-2.1,.6,0,.6); add(taiko(3.2),tc[0]+.05,1.6,0,.8); add(bell(hz(62),4),tc[0]+.1,.3,0,1); add(bell(hz(74),4),tc[0]+.9,.2,0,1)
elif mood=='tension':
    section(0,cta-.3,['Dp','Eb','Dp','Cm'],cd=6,g=(.85,1.15),bright=.45,pulse=2.4,pg=.5); section(cta-.3,dur,['Dm','Bb','D'],cd=3,g=(1.0,.8),bright=.6,hi=.6)
    add(taiko(2.2),F[10][0]-.1,.8,0,.7); add(taiko(2.6),F[13][0]+2.6,.8,0,.7)
elif mood=='prayer':
    section(0,cta-.3,['Bb','F','Gm','Dm'],cd=5.5,g=(.9,1.05),bright=.45,arp=.5,hi=.5); section(cta-.3,dur,['Bb','F','D'],cd=3,g=(1.0,.8),bright=.6,hi=.7)
    add(growl(2.2,62),F[9][0]+.5,.35,.2,1.5)
    for i,m in enumerate([62,65,69,74]): add(bell(hz(m),4),F[11][0]+i*.5,.2,(-1)**i*.4,1.2)
elif mood=='dark':
    tq=F[5][0]; tp=F[8][0]
    section(0,tq-.3,['D5','Dm'],cd=6,g=(.9,1.05),bright=.35,pulse=2.6,pg=.7); section(tq-.3,tp,['Bb','Gm','Dm'],cd=4.5,g=(.9,.8),bright=.4,hi=.5)
    section(tp,cta-.3,['D5'],cd=8,g=(.9,.75),bright=.25); section(cta-.3,dur,['Dm','Bb','D'],cd=3,g=(1.0,.8),bright=.6,hi=.6)
    add(growl(2.4,60),F[1][0]+1.2,.45,-.3,1.5); add(stone(3.0),tp+.2,.9,-.1,.5); add(taiko(3.0),tp+3.0,1.3,0,.9); add(taiko(2.6),F[10][0]+.2,.8,0,.9); add(growl(2.2,66),F[11][0]+.8,.4,.3,1.5)
else:
    tf=F[10][0]
    section(0,tf-.3,['Bm','G','D','A'],cd=5,g=(.8,1.1),bright=.5,arp=.45,hi=.5); section(tf-.3,dur,['D','G','D'],cd=3.6,g=(1.4,.9),bright=.85,hi=1.0)
    add(swell(2.2,300,5000),tf-2.1,.45,0,.6); add(taiko(3.2),tf+.15,1.1,0,.8)
    for i,m in enumerate([62,69,74,78]): add(bell(hz(m),5),tf+.25+i*.28,.24,(-1)**i*.4,1.2)
for t in cuts: add(whoosh(),t-.2,.10,rng.uniform(-.4,.4),.4)
add(swell(1.2),cta-1.3,.25,0,.6); add(taiko(2.2),cta-.3,.8,0,.7)
for i,m in enumerate([62,69,74]): add(bell(hz(m),3.5),cta+1.0+i*.25,.16,(-1)**i*.4,1.2)
ir_t=T(2.6); wet=np.zeros_like(out)
for ch in range(2):
    ir=lp(rng.standard_normal(len(ir_t)).astype(np.float32),5200)*np.exp(-ir_t*2.3)*np.minimum(1,ir_t/.012); ir/=np.sqrt(np.sum(ir**2)); wet[:,ch]=sg.oaconvolve(rev[:,ch],ir)[:N].astype(np.float32)
mix=out+wet*.55
b,a=sg.butter(2,28/(sr/2),'high'); mix=sg.lfilter(b,a,mix,axis=0).astype(np.float32); b,a=sg.butter(1,230/(sr/2)); mix=mix-.42*sg.lfilter(b,a,mix,axis=0).astype(np.float32)
tt=np.arange(N)/sr; mix*=(np.minimum(1,tt/.25)*np.clip((dur-tt)/1.2,0,1))[:,None].astype(np.float32)
mix*=10**(-20/20)/np.sqrt(np.mean(mix**2)); mix=np.tanh(mix*1.15)/1.15
w=wave.open(sys.argv[2],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(mix,-1,1)*32767).astype(np.int16).tobytes()); w.close(); print(C['id'],'música ok',round(dur,1))

#!/usr/bin/env python3
"""Alinea cada frase del guion con su bloque de voz (silencios + sílabas, sin IA).
Uso: align.py <carpeta_voz con 01.mp3..13.mp3>  ->  frases.json (tiempos por frase dentro de cada bloque)"""
import re, json, subprocess, sys, os
VOZ=sys.argv[1]; HERE=os.path.dirname(os.path.abspath(__file__))
G=json.load(open(os.path.join(HERE,'guion.json')))['bloques']
NUM={'6:16':'seis dieciséis','6:18':'seis dieciocho','6':'seis'}
def spoken(t):
    return re.sub(r'\b(6:16|6:18|6)\b',lambda m:NUM[m.group(1)],t)
def syl(w):
    w=re.sub(r'[^a-záéíóúüñ]','',w.lower())
    g=re.findall(r'[aeiouáéíóúü]+',w); n=0
    for x in g:
        n+=1
        if re.search(r'[aeo][áéíóú]|[áéíóú][aeo]|í[aeou]|ú[aeio]|[aeo]í|[aeo]ú|[aeo][aeo]',x): n+=1
    return max(1,n)
out=[]
for bi,b in enumerate(G):
    f=os.path.join(VOZ,f'{bi+1:02d}.mp3')
    words=[];kind=[]   # kind: 2 fin de frase, 1 coma/dos puntos internos, 0 nada
    sidx=[]
    for si,s in enumerate(b['frases']):
        ws=spoken(s).split()
        for k,w in enumerate(ws):
            words.append(w); sidx.append(si)
            kind.append(2 if k==len(ws)-1 else (1 if re.search(r'[,:;]$',w) else 0))
    S=[syl(w) for w in words]; N=len(words)
    err=subprocess.run(['ffmpeg','-v','info','-i',f,'-af','silencedetect=noise=-34dB:d=0.16','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',err)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',err)]
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    ivs=[];a=0.0
    for s,e in zip(st,en):
        if s-a>0.05: ivs.append([a,s])
        a=e
    if len(st)>len(en): pass
    elif dur-a>0.12: ivs.append([a,dur])
    K=len(ivs); gaps=[ivs[k+1][0]-ivs[k][1] for k in range(K-1)]+[0]
    r=sum(b_-a_ for a_,b_ in ivs)/sum(S)
    cs=[0]
    for s in S: cs.append(cs[-1]+s)
    INF=1e18
    dp=[[INF]*(N+1) for _ in range(K+1)]; bk=[[0]*(N+1) for _ in range(K+1)]; dp[0][0]=0
    # nº de fines de frase estrictamente dentro de (i,j)
    ce=[0]
    for k_ in kind: ce.append(ce[-1]+(1 if k_==2 else 0))
    for k in range(1,K+1):
        d=ivs[k-1][1]-ivs[k-1][0]; g=gaps[k-1]
        for j in range(k,N+1):
            if k==K and j!=N: continue
            kd=kind[j-1]
            if k<K:
                bc = 0.0 if kd==2 else (0.25+2.0*max(0,g-0.5) if kd==1 else 0.9+3.0*g)
                if kd==2 and g<0.3: bc+=0.15
            else: bc=0
            for i in range(max(k-1,j-60),j):
                if dp[k-1][i]>=INF: continue
                sy=cs[j]-cs[i]
                c=((d-r*sy)**2)/(0.25+0.05*sy)+bc
                inner=ce[j-1]-ce[i]      # frases que terminan dentro del intervalo sin silencio
                c+=1.6*inner
                v=dp[k-1][i]+c
                if v<dp[k][j]: dp[k][j]=v; bk[k][j]=i
    cuts=[];j=N
    for k in range(K,0,-1):
        i=bk[k][j]; cuts.append((i,j)); j=i
    cuts=cuts[::-1]
    wt=[None]*N
    for (i,j),(a_,b_) in zip(cuts,ivs):
        tot=sum(S[m]+0.5 for m in range(i,j)); t=a_
        for m in range(i,j):
            w=(S[m]+0.5)/tot*(b_-a_); wt[m]=[t,t+w]; t+=w
    fr=[]
    for si,s in enumerate(b['frases']):
        ms=[m for m in range(N) if sidx[m]==si]
        ws=[[words[m],round(wt[m][0],3),round(wt[m][1],3)] for m in ms]
        fr.append({'t':s,'a':round(wt[ms[0]][0],3),'b':round(wt[ms[-1]][1],3),'syl':sum(S[m] for m in ms),'w':ws})
    # ¿la frase termina en un silencio detectado? (para alargar pausas)
    ends=[iv[1] for iv in ivs]
    for x in fr:
        x['sil']=next((round(gaps[k],3) for k,e in enumerate(ends) if abs(e-x['b'])<0.02),0)
    out.append({'bloque':bi+1,'dur':round(dur,3),'frases':fr})
    if '-v' in sys.argv:
        print(f'--- bloque {bi+1} dur {dur:.2f} intervalos {K} ritmo {1/r:.2f} síl/s')
        for x in fr: print(f"{x['a']:6.2f}-{x['b']:6.2f} sil {x['sil']:.2f} {x['syl']/(x['b']-x['a']):5.2f} síl/s | {x['t'][:70]}")
json.dump(out,open(os.path.join(HERE,'frases.json'),'w'),ensure_ascii=False)
print('ok',sum(len(o['frases']) for o in out),'frases')

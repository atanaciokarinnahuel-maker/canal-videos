import json
w=[x for x in json.load(open('words_raw.json'))['words'] if x['type']=='word']
def rng(a,b): return list(range(a,b+1))
# primer intento de "La guerra ... española." (225.3–229.6)
g=[i for i,x in enumerate(w) if 225.0<=x['start']<230.5]
DEL=set(rng(279,280)+rng(389,392)+rng(412,423)+rng(446,452)+rng(463,477)+g+rng(738,750)+rng(774,788)+rng(818,827)+rng(850,854)+rng(877,882)+rng(948,953)+rng(1004,1011)+rng(1120,1123)+rng(1151,1153))
print('borrar:',' | '.join(' '.join(w[i]['text'] for i in sorted(DEL) if i in grp) for grp in [set(g)]), len(DEL))
keep=[i for i in range(len(w)) if i not in DEL]
# segmentos de audio a conservar (tiempos originales)
segs=[]; start=0.0; prev=None
for k,i in enumerate(keep):
    if prev is not None and i!=prev+1:
        d0=w[prev+1]['start']; d1=w[i-1]['end']
        a_end=min(w[prev]['end']+0.30, d0-0.06)
        b_start=max(w[i]['start']-0.40, d1+0.08)
        segs.append([round(start,3),round(a_end,3)]); start=b_start
    prev=i
segs=[[a,(116.86 if abs(b-117.02)<0.01 else b)] for a,b in segs]
END=508.3
segs.append([round(start,3),END])
segs=[[a,(116.86 if abs(b-117.02)<0.01 else b)] for a,b in segs]
# pausas de 1,1 s antes de cada capítulo (para la tarjeta de capítulo)
CAPS=[44.56,105.06,171.84,250.9,315.68,422.0,465.5]
PAD=1.1
segs=[s+[0] for s in segs]
for c in CAPS:
    wi=min(range(len(w)),key=lambda i:abs(w[i]['start']-c)) if False else None
    ci=min((i for i in keep),key=lambda i:abs(w[i]['start']-c)); c=w[ci]['start']
    pi=keep[keep.index(ci)-1]; p=w[pi]['end']
    for k,(a,b,pd) in enumerate(segs):
        if a<=c<=b:
            if c-a<0.6 and k>0: segs[k-1][2]=PAD
            else:
                sp=round((p+c)/2,3); segs[k:k+1]=[[a,sp,PAD],[sp,b,0]]
            break
def mapt(t):
    off=0
    for a,b,pd in segs:
        if t<a: return off
        if t<=b: return off+(t-a)
        off+=b-a+pd
    return off
nw=[]
for i in keep:
    x=dict(text=w[i]['text'],start=round(mapt(w[i]['start']),3),end=round(mapt(w[i]['end']),3),orig=w[i]['start'],idx=i)
    nw.append(x)
total=sum(b-a+pd for a,b,pd in segs)
chap=[round(mapt(w[min(keep,key=lambda i:abs(w[i]['start']-c))]['start']),3) for c in CAPS]
json.dump({'capitulos':[0]+chap,'segmentos':segs,'voice_dur':round(total,3),'words':nw},open('timeline.json','w'),ensure_ascii=False)
print(len(segs),'segmentos; voz final',round(total,2),'s')
print(segs); print('caps',chap)

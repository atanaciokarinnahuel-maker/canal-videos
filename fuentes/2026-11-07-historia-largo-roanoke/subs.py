import json,re
T=json.load(open('timeline.json')); w=T['words']
FIX={'croatoan,':'Croatoan,','croatoan':'Croatoan','croatoan.':'Croatoan.','C-R-O.':'«CRO».','C-R-O':'«CRO»','Isla':'isla','Outerers.':'Hatteras.','Harvey.':'Harvie.',}
words=[]
for i,x in enumerate(w):
    t=x['text']
    if t in FIX: t=FIX[t]
    prev=words[-1]['t'] if words else '.'
    if prev[-1] in '.?:!' and t[0].islower() and t not in('nació',): t=t[0].upper()+t[1:]
    words.append(dict(t=t,s=x['start'],e=x['end']))
sents=[];cur=[]
for k,x in enumerate(words):
    cur.append(x)
    nxt=words[k+1] if k+1<len(words) else None
    if x['t'][-1] in '.?!:' or (nxt and nxt['s']-x['e']>1.0): sents.append(cur);cur=[]
if cur: sents.append(cur)
import math
subs=[]
def L(ws): return len(' '.join(y['t'] for y in ws))
def split(ws):
    if L(ws)<=56: return [ws]
    n=math.ceil(L(ws)/50); best=None
    target=L(ws)/n
    # elegir un corte: cerca del objetivo, preferir comas
    for j in range(1,len(ws)):
        a=L(ws[:j]); pen=abs(a-target)
        if ws[j-1]['t'][-1] in ',;': pen-=14
        if ws[j]['t'] in ('y','o','pero','que','de','a','en','la','el','los','las','un','una','con','sin','del','al') and ws[j-1]['t'][-1] not in ',;': pen+=0
        if ws[j-1]['t'] in ('de','a','en','la','el','los','las','un','una','con','del','al','y','o','que','su','sus'): pen+=25
        if L(ws[j:])<12 or a<12: pen+=40
        if best is None or pen<best[0]: best=(pen,j)
    j=best[1]; return split(ws[:j])+split(ws[j:])
for se in sents:
    for p in split(se): subs.append(dict(s=p[0]['s'],e=p[-1]['e'],text=' '.join(y['t'] for y in p)))
# duración de pantalla: hasta el comienzo del siguiente (máx +0.8 s)
for i,s in enumerate(subs):
    nx=subs[i+1]['s'] if i+1<len(subs) else s['e']+1.2
    s['e']=round(min(nx-0.04,s['e']+0.8),3); s['s']=round(s['s']-0.08,3)
for x in subs:
    if x['text']=='Croatoan.': x['text']='«CROATOAN».'
json.dump(subs,open('subs.json','w'),ensure_ascii=False,indent=0)
print(len(subs),max(len(s['text']) for s in subs))
for s in subs[:12]+subs[95:110]: print(s['s'],s['text'])

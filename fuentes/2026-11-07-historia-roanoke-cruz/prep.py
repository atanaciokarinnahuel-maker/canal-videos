import json,re
TEMPO=1.04
raw=json.load(open('words_raw.json'))
w=[x for x in raw if x['type']=='word' and not x['text'].startswith('[')]
# fusionar números escritos en palabras -> cifras para subtítulos
out=[];i=0
def toks(i,n): return ' '.join(x['text'] for x in w[i:i+n])
while i<len(w):
    s=toks(i,5)
    if s.startswith('Mil quinientos ochenta y siete'):
        out.append({'t':'1587,','s':w[i]['start'],'e':w[i+4]['end']}); i+=5; continue
    if toks(i,3).startswith('Mil quinientos noventa'):
        out.append({'t':'1590.','s':w[i]['start'],'e':w[i+2]['end']}); i+=3; continue
    t=w[i]['text'].replace('Ce…','C…').replace('Erre…','R…')
    out.append({'t':t,'s':w[i]['start'],'e':w[i]['end']}); i+=1
for o in out: o['s']=round(o['s']/TEMPO,3); o['e']=round(o['e']/TEMPO,3)
# grupos de subtítulos: corte en puntuación fuerte o 4 palabras
groups=[];cur=[]
for k,o in enumerate(out):
    cur.append(k)
    if re.search(r'[.?!:…]$',o['t']) or (o['t'].endswith(',') and len(cur)>=2) or len(cur)>=4:
        groups.append(cur);cur=[]
if cur: groups.append(cur)
json.dump({'tempo':TEMPO,'voice_dur':round(59.04/TEMPO,3),'words':out,'groups':groups},open('words.json','w'),ensure_ascii=False)
print(len(out),len(groups),round(59.04/TEMPO,3))
for g in groups: print(out[g[0]]['s'], ' '.join(out[k]['t'] for k in g))

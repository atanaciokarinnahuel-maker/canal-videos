import re, json
txt = open('guion.txt').read()
txt = re.sub(r'\[[a-z ]+\]', '', txt)
toks = txt.split()
spoken = {"14:28":"catorce veintiocho","27:23":"veintisiete veintitrés","21:5":"veintiuno cinco","6:8":"seis ocho","4:2":"cuatro dos","1":"primera"}
TOTAL = 53.5
words=[]
for t in toks:
    core = t.strip('¿?¡!.,:;')
    sp = spoken.get(core, core)
    w = len(re.sub(r'[^a-záéíóúñü]', '', sp.lower())) + 1.5
    p = 0
    if t.endswith((',',';')): p = 0.22
    if t.endswith(('.', '?', '!', ':')): p = 0.42
    words.append([t, w, p])
pz = sum(x[2] for x in words); ch = sum(x[1] for x in words)
rate = (TOTAL - 0.25 - pz) / ch
t = 0.25; out=[]
for tok,w,p in words:
    d = w*rate
    out.append({"text":tok, "start":round(t,3), "end":round(t+d,3)})
    t += d + p
json.dump({"words":out, "voice_dur": round(t,2), "estimated": True}, open('words.json','w'), ensure_ascii=False, indent=0)
print(len(out), t, rate)

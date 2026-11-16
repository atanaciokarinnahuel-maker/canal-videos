import re, json, subprocess, sys
TEMPO=1.0
AUDIO='/home/claude/bat/voz.mp3'
TEXT='Si la tapa de tu celular se está despegando, o la pantalla se levanta, no es un defecto de fábrica. Es una batería hinchada, y es un riesgo de incendio. Por dentro, la batería de litio se desgasta con el tiempo, el calor y la mala carga, y suelta gas. Como está sellada, el gas no sale: la batería se infla, y empuja la tapa, la pantalla y la placa. Las señales: la tapa se despega, la pantalla se levanta, el celular se balancea sobre la mesa, o se calienta sin motivo. Lo que no debes hacer. No la pinches para desinflarla: adentro hay un líquido inflamable. No la aplastes. Y no la sigas cargando. Lo que sí debes hacer: apaga el celular, sácalo del cargador y llévalo a un técnico. Una batería hinchada no se desinfla: la única solución es cambiarla. Para prevenirlo, evita el sol y el calor, usa cargadores de calidad, y mantén la carga entre el veinte y el ochenta por ciento. Entonces, ¿tu celular se balancea sobre la mesa? Cuéntame abajo qué modelo es. Sígueme para más tecnología simple.'
words=TEXT.split()
def syl(w):
    w=re.sub(r'[^a-záéíóúüñ0-9]','',w.lower())
    if w=='3700': return 6
    g=re.findall(r'[aeiouáéíóúü]+',w)
    n=0
    for x in g:
        # diptongos: cuenta 1; hiatos con vocal tónica fuerte cuentan 2
        n+=1
        if re.search(r'[aeo][áéíóú]|[áéíóú][aeo]|í[aeou]|ú[aeio]|[aeo]í|[aeo]ú',x): n+=1
    return max(1,n)
S=[syl(w) for w in words]
ends=[bool(re.search(r'[.,:;…?!]$',w)) for w in words]
sent=[bool(re.search(r'[.:;…?!]$',w)) for w in words]
# silencios
out=subprocess.run(['ffmpeg','-v','info','-i',AUDIO,'-af','silencedetect=noise=-38dB:d=0.18','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',AUDIO],capture_output=True,text=True).stdout)
ivs=[]; a=0.0
for s,e in zip(st,en):
    ivs.append((a,s)); a=e
if a<dur-0.2: ivs.append((a,dur))
# la última "silencio" llega hasta el final: ya queda cubierta
K=len(ivs); N=len(words)
print('intervalos',K,'palabras',N,'sílabas',sum(S))
r=sum(b-a for a,b in ivs)/sum(S)
INF=1e18
cs=[0]
for s in S: cs.append(cs[-1]+s)
dp=[[INF]*(N+1) for _ in range(K+1)]; bk=[[0]*(N+1) for _ in range(K+1)]
dp[0][0]=0
for k in range(1,K+1):
    d=ivs[k-1][1]-ivs[k-1][0]
    for j in range(k,N+1):
        for i in range(k-1,j):
            if dp[k-1][i]>=INF: continue
            sy=cs[j]-cs[i]
            c=(d-r*sy)**2
            if k<K and j<N and not ends[j-1]: c+=1.2   # preferir cortes en puntuación
            v=dp[k-1][i]+c
            if v<dp[k][j]: dp[k][j]=v; bk[k][j]=i
cuts=[]; j=N
for k in range(K,0,-1):
    i=bk[k][j]; cuts.append((i,j)); j=i
cuts=cuts[::-1]
# tiempos de palabras (audio original)
W=[]; segs=[]
for k,((i,j),(a,b)) in enumerate(zip(cuts,ivs)):
    ta=max(0,a-0.03); tb=min(dur,b+0.04)
    tot=sum(S[m]+0.6 for m in range(i,j)); t=a
    for m in range(i,j):
        w=(S[m]+0.6)/tot*(b-a)
        W.append([words[m],t,t+w*0.92]); t+=w
    last=j-1
    pad = 0 if k==K-1 else (0.26 if sent[last] else 0.06)
    if k<K-1 and words[last].endswith(':'): pad=0.12
    segs.append([round(ta,3),round(tb,3),pad])
# línea de tiempo recortada y con tempo
cum=0.0; newW=[]; wi=0
for k,((i,j),sg) in enumerate(zip(cuts,segs)):
    ta,tb,pad=sg
    for m in range(i,j):
        w,s0,e0=W[wi]; wi+=1
        newW.append({'text':w,'start':round((cum+(s0-ta))/TEMPO,3),'end':round((cum+(e0-ta))/TEMPO,3)})
    cum+=(tb-ta)+pad
voice=round(cum/TEMPO,2)
json.dump({'words':newW,'voice_dur':voice},open('words.json','w'),ensure_ascii=False)
json.dump(segs,open('segmentos.json','w'))
print('voz recortada',round(cum,2),'-> final con tempo',TEMPO,':',voice,'s')
for k,(i,j) in enumerate(cuts): print(k,round(ivs[k][0],2),round(ivs[k][1],2),'|',' '.join(words[i:j]), '| pad',segs[k][2])

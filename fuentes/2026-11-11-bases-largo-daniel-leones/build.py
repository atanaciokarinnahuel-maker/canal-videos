#!/usr/bin/env python3
"""Arma la voz final (bloques + pausas alargadas entre frases + silencios de tarjetas) y la línea de tiempo.
Uso: build.py <carpeta_voz> <salida_voz.wav>  ->  data.json (tiempos de cada frase en el video)"""
import json, subprocess, sys, os, re, numpy as np
VOZ, OUT = sys.argv[1], sys.argv[2]; HERE=os.path.dirname(os.path.abspath(__file__)); SR=44100
F=json.load(open(os.path.join(HERE,'frases.json'))); G=json.load(open(os.path.join(HERE,'guion.json')))['bloques']
EXTRA=0.42          # segundos que se agregan a cada pausa entre frases (ritmo solemne de documental)
T0=3.2              # la voz empieza tras la apertura sonora
TITLE=8.0           # secuencia de título tras la escena 1
CARD=(1.0,3.8,0.6)  # antes, tarjeta de capítulo, después
PAUSA3=3.2          # "pausa de tres segundos" antes del bloque 12
NEGRO=4.5           # pantalla negra con música antes del cierre
FINAL=11.0          # tarjeta final tras la última frase
def load(i):
    raw=subprocess.run(['ffmpeg','-v','error','-i',os.path.join(VOZ,f'{i:02d}.mp3'),'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
audio=[]; t=T0; audio.append(np.zeros(int(T0*SR),np.float32)); blocks=[]; cards=[]; sents=[]
for bi,b in enumerate(F):
    x=load(bi+1)
    # igualar volumen por bloque (RMS de las partes habladas)
    sp=x[np.abs(x)>0.02]; x*=0.11/np.sqrt(np.mean(sp**2))
    if bi==0: pass
    elif bi==11: audio.append(np.zeros(int(PAUSA3*SR),np.float32)); t+=PAUSA3
    elif bi==12: audio.append(np.zeros(int(NEGRO*SR),np.float32)); t+=NEGRO
    else:
        pre=CARD[0]+(TITLE if bi==1 else 0)
        cards.append({'bloque':bi+1,'a':round(t+pre,3),'b':round(t+pre+CARD[1],3)})
        d=pre+CARD[1]+CARD[2]; audio.append(np.zeros(int(d*SR),np.float32)); t+=d
    bstart=t; pos=0.0; fr=b['frases']
    for si,f in enumerate(fr):
        last=si==len(fr)-1
        cut=b['dur'] if last else (f['b']+fr[si+1]['a'])/2
        seg=x[int(pos*SR):int(cut*SR)]; audio.append(seg)
        off=t-pos
        sw=f['w']; words=[]; k=0
        for tok in f['t'].split():          # palabras tal como se leen en pantalla ("6:16" ocupa dos palabras habladas)
            n=2 if re.search(r'\d:\d',tok) else 1
            words.append([tok,round(sw[k][1]+off,3),round(sw[k+n-1][2]+off,3)]); k+=n
        assert k==len(sw),(f['t'],k,len(sw))
        sents.append({'b':bi+1,'i':si,'t':f['t'],'a':round(f['a']+off,3),'e':round(f['b']+off,3),'w':words})
        t+=len(seg)/SR; pos=cut
        if not last and f['sil']>=0.2:
            ex=EXTRA+(0.35 if '«' in f['t'] or '«' in fr[si+1]['t'] else 0)
            audio.append(np.zeros(int(ex*SR),np.float32)); t+=ex
    blocks.append({'bloque':bi+1,'escena':G[bi]['escena'],'titulo':G[bi]['titulo'],'a':round(bstart,3),'e':round(t,3)})
audio.append(np.zeros(int(FINAL*SR),np.float32)); t+=FINAL
y=np.concatenate(audio); dur=len(y)/SR
y=np.tanh(y*1.0)   # limitador suave
import wave
w=wave.open(OUT,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes()); w.close()
title={'a':round(blocks[0]['e']+0.8,3),'b':round(blocks[0]['e']+0.8+TITLE-0.6,3)}
json.dump({'dur':round(dur,3),'fps':24,'bloques':blocks,'tarjetas':cards,'titulo':title,'frases':sents},open(os.path.join(HERE,'data.json'),'w'),ensure_ascii=False)
print('duración',round(dur,2),'s =',int(dur//60),'min',round(dur%60,1),'s; frases',len(sents))
for b in blocks: print(b)
print('titulo',title); print('tarjetas',cards[:2])

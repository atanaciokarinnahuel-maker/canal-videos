#!/usr/bin/env python3
"""Arma la voz y la configuración de las piezas verticales (tráiler TikTok + 4 Shorts) de "Daniel: una noche entre leones".
Reutiliza la narración del largo (insumos-voz/…-largo-daniel-leones/voz-final.mp3 + data.json) y agrega una frase de cierre nueva.
Uso: armar.py <carpeta_salida>   ->  <id>.voz.wav y <id>.json por pieza"""
import json, subprocess, sys, os, re, numpy as np, wave
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..'); OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)
LARGO=os.path.join(ROOT,'fuentes','2026-11-11-bases-largo-daniel-leones'); D=json.load(open(os.path.join(LARGO,'data.json')))
SR=44100; TEMPO=1.06; GAP=0.30
def dec(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
VOZ=dec(os.path.join(ROOT,'insumos-voz','2026-11-11-bases-largo-daniel-leones','voz-final.mp3'))
def syl(w):
    w=re.sub(r'[^a-záéíóúüñ]','',w.lower()); g=re.findall(r'[aeiouáéíóúü]+',w); return max(1,len(g))
# frases de cierre: texto por tramo hablado [inicio, fin] (medidos con silencedetect)
CTA={'cta1':[('La historia completa está en YouTube.',0.0,2.14),('Buscá:',2.60,3.09),('Bases Bíblicas.',3.41,4.70)],
     'cta2':[('La historia completa está en YouTube,',0.0,2.17),('en el canal Bases Bíblicas.',2.55,4.83)],
     'cta3':[('¿Qué pasó esa noche?',0.0,1.38),('Mirá el final en YouTube,',2.06,3.40),('en el canal Bases Bíblicas.',3.66,5.74)]}
def fade(x,n=400):
    x=x.copy(); n=min(n,len(x)//2); r=np.linspace(0,1,n,dtype=np.float32); x[:n]*=r; x[-n:]*=r[::-1]; return x

# vistas verticales: [imagen, centro x, centro y, alto] en fracciones de la imagen
PIEZAS={
 'trailer':{'titulo':'tráiler TikTok','hook':['CONDENADO','POR ORAR'],'cta':'cta1','mood':'trailer','title_card':2.6,
  'frases':[(1,0),(1,3),(1,4),(1,7),(1,8),(1,13)],
  'planos':[(0,0,{'a':'M_fig','z':.1,'fx':{'dark':[.35,.1],'rays':'M','rs':.45,'dust':1}}),
            (1,0,{'a':'V_up','z':.1}),(1,3.3,{'a':'V_dan','z':.08}),
            (2,0,{'a':'T_king','z':.12,'fx':{'flick':.05}}),(2,2.3,{'a':'S_seal','z':.16}),
            (3,0,{'a':'O_lions','z':.14}),(3,2.5,{'a':'M_pack','z':.1,'fx':{'dark':.25}}),(3,5.0,{'a':'L_lionR','z':.1,'fx':{'dark':.15}}),
            (4,0,{'a':'L_close','z':.16,'fx':{'rays':'L','rs':.4,'dust':1}}),
            (5,0,{'a':'L_lionL2','b':'L_dan','fx':{'rays':'L','rs':.5,'dust':1}})]},
 'short1-conspiracion':{'titulo':'Querían destruirlo','hook':['BUSCARON','UNA FALTA…'],'cta':'cta2','mood':'tension',
  'frases':[(3,i) for i in range(14)],
  'planos':[(0,0,{'a':'V_off','z':.1,'fx':{'dark':.1}}),(1,0,{'a':'O_scroll','z':.1}),(2,0,{'a':'O_off','z':.08}),(3,0,{'a':'P_lamp','z':.1,'fx':{'flick':.05}}),
            (4,0,{'a':'S_offR','z':.1}),(5,0,{'a':'V_up','z':.12}),(6,0,{'a':'V_dan','z':.08}),(7,0,{'a':'O_off','z':.12,'fx':{'dark':.15}}),
            (8,0,{'a':'O_scroll','z':.12}),(9,0,{'a':'V_win','b':'V_up'}),(10,0,{'a':'K_old','z':.1,'fx':{'dark':.15}}),(11,0,{'a':'K_young','z':.1,'fx':{'dark':.1}}),
            (12,0,{'a':'S_offR','z':.12,'fx':{'dark':.15}}),(13,0,{'a':'V_off','b':'V_dan'})]},
 'short2-oracion':{'titulo':'Orar estaba prohibido','hook':['ORAR ESTABA','PROHIBIDO'],'cta':'cta2','mood':'prayer',
  'frases':[(5,i) for i in range(14)],
  'planos':[(0,0,{'a':'S_king','z':.1}),(0,2.8,{'a':'P_man','z':.1,'fx':{'flick':.04}}),(1,0,{'a':'K_sold','z':.1}),(2,0,{'a':'C_off','z':.1}),(3,0,{'a':'O_scroll','z':.1}),
            (4,0,{'a':'V_dan','z':.08}),(4,4.4,{'a':'V_win','z':.1,'fx':{'rays':'V','rs':.3}}),(4,8.8,{'a':'V_up','z':.12}),
            (5,0,{'a':'P_lamp','z':.1,'fx':{'flick':.05}}),(6,0,{'a':'V_up','z':-.1}),(7,0,{'a':'V_win','z':.1}),(8,0,{'a':'P_man','z':-.1,'fx':{'flick':.04}}),
            (9,0,{'a':'O_lions','z':.14}),(10,0,{'a':'C_off','z':.1}),(10,3.3,{'a':'V_dan','z':.1}),(11,0,{'a':'V_up','z':.16,'fx':{'rays':'V','rs':.35,'dust':.6}})]},
 'short3-foso':{'titulo':'Arrojado a los leones','hook':['ARROJADO A','LOS LEONES'],'cta':'cta3','mood':'dark',
  'frases':[(7,i) for i in range(13)],
  'planos':[(0,0,{'a':'T_king','z':.12,'fx':{'flick':.05,'dark':.1}}),(1,0,{'a':'O_lions','z':.14}),(2,0,{'a':'K_sold','z':.1,'fx':{'dark':.15}}),
            (3,0,{'a':'V_up','z':.1}),(3,3.2,{'a':'O_off','z':.1,'fx':{'dark':.15}}),(4,0,{'a':'S_face','z':.1}),(5,0,{'a':'O_king','z':.1}),
            (6,0,{'a':'C_king','z':.1,'fx':{'dark':.1}}),(7,0,{'a':'L_dan','z':.08,'fx':{'rays':'L','rs':.45,'dust':1}}),(8,0,{'a':'L_dan','z':.05,'fx':{'close':1}}),
            (9,0,{'a':'S_seal','z':.14,'fx':{'dark':.2}}),(9,3.3,{'a':'S_offR','z':.1,'fx':{'dark':.25}}),(10,0,{'a':'M_pack','z':.06,'fx':{'dark':.8}}),
            (11,0,{'a':'M_pack','z':.1,'fx':{'dark':.6}}),(12,0,{'a':'L_close','z':.12,'fx':{'dark':[.6,.1],'rays':'L','rs':[.1,.45],'dust':1}})]},
 'short4-ensenanza':{'titulo':'Los imperios pasan','hook':['LOS IMPERIOS','PASAN'],'cta':'cta2','mood':'hope',
  'frases':[(11,11),(11,12),(11,13)]+[(12,i) for i in range(8)],
  'planos':[(0,0,{'a':'P_man','z':.1,'fx':{'flick':.04}}),(1,0,{'a':'V_up','z':.12}),(2,0,{'a':'V_win','b':'V_up'}),
            (3,0,{'a':'L_lionL2','b':'L_dan','fx':{'rays':'L','rs':.4,'dust':1}}),(4,0,{'a':'C_off','z':.1}),(4,3.3,{'a':'V_off','z':.1}),
            (5,0,{'a':'L_close','z':.14,'fx':{'rays':'L','rs':.45,'dust':1}}),(6,0,{'a':'S_seal','z':.12}),(6,2.3,{'a':'V_up','z':.1}),
            (7,0,{'a':'T_king','z':.1,'fx':{'dark':[.1,.55],'bw':[0,.8]}}),(8,0,{'a':'S_face','z':.1,'fx':{'dark':[.1,.55],'bw':[0,.8]}}),(9,0,{'a':'S_seal','z':.1,'fx':{'dark':[.1,.55],'bw':[0,.8]}}),
            (10,0,{'a':'L_dan','z':.1,'fx':{'rays':'L','rs':[.4,.8],'dust':1}})]}}

def S(b,i): return next(f for f in D['frases'] if f['b']==b and f['i']==i)
for pid,P in PIEZAS.items():
    audio=[np.zeros(int(.35*SR),np.float32)]; t=.35; words=[]; sents=[]
    for k,(b,i) in enumerate(P['frases']):
        f=S(b,i); a=f['a']-.07; e=f['e']+.13; seg=fade(VOZ[int(a*SR):int(e*SR)]); off=t-a
        ws=[[w,wa+off,we+off] for w,wa,we in f['w']]; words.append(ws); sents.append([f['a']+off,f['e']+off])
        audio.append(seg); t+=len(seg)/SR
        g=GAP+(.2 if '«' in f['t'] else 0); audio.append(np.zeros(int(g*SR),np.float32)); t+=g
    tc=None
    if P.get('title_card'): tc=[t+.1,t+.1+P['title_card']]; audio.append(np.zeros(int((P['title_card']+.3)*SR),np.float32)); t+=P['title_card']+.3
    else: audio.append(np.zeros(int(.35*SR),np.float32)); t+=.35
    c=dec(os.path.join(ROOT,'insumos-voz','2026-11-11-bases-daniel-verticales',P['cta']+'.mp3')); sp=c[np.abs(c)>.02]; vs=VOZ[np.abs(VOZ)>.02]
    c*=np.sqrt(np.mean(vs**2))/np.sqrt(np.mean(sp**2)); t_cta=t; cw=[]
    for txt,a,e in CTA[P['cta']]:
        ws=txt.split(); tot=sum(syl(w)+.5 for w in ws); tt=a
        for w in ws: d=(syl(w)+.5)/tot*(e-a); cw.append([w,t+tt,t+tt+d]); tt+=d
    words.append(cw); sents.append([t,t+CTA[P['cta']][-1][2]]); audio.append(c); t+=len(c)/SR
    audio.append(np.zeros(int(2.0*SR),np.float32)); t+=2.0
    y=np.concatenate(audio); tmp=os.path.join(OUT,pid+'.raw.wav')
    w=wave.open(tmp,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(['ffmpeg','-y','-v','error','-i',tmp,'-af',f'atempo={TEMPO}','-ar',str(SR),os.path.join(OUT,pid+'.voz.wav')],check=True); os.remove(tmp)
    q=lambda x:round(x/TEMPO,3)
    planos=[]
    for k,o,sh in P['planos']:
        s=dict(sh); s['t']=q(sents[k][0]+o)-.25; planos.append(s)
    planos[0]['t']=0
    cfg={'id':pid,'titulo':P['titulo'],'hook':P['hook'],'mood':P['mood'],'dur':q(t),'fps':30,'cta':q(t_cta),'title_card':[q(x) for x in tc] if tc else None,
         'planos':planos,'frases':[[q(a),q(e)] for a,e in sents],'palabras':[[[w,q(a),q(e)] for w,a,e in ws] for ws in words]}
    json.dump(cfg,open(os.path.join(OUT,pid+'.json'),'w'),ensure_ascii=False)
    print(pid,'dur',cfg['dur'],'cta',cfg['cta'],'planos',len(planos))

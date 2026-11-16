# Ensambla video.html: motor del video anterior (../2026-11-09-tech-vram-ia-local) + piezas/escenas nuevas (escenas.js)
import re
s=open('escenas.js').read()
if "];SC.forEach" not in s:
    s=s.replace("]; let t=0;SC.forEach((sc,i)=>{sc.t0=Math.max(t+.8,A(...sc.a).start+(sc.o||0));if(i==0)sc.t0=0;t=sc.t0})}",
"];SC.forEach(sc=>{const w=A(...sc.a);sc.t0=Math.max(0,w.start+sc.o)});SC[0].t0=0;\n for(let i=1;i<SC.length;i++)if(SC[i].t0<=SC[i-1].t0+.3)console.error('ORDEN '+i+' '+SC[i].t0.toFixed(2))}")
tail=open('tail.js').read()
O=open('../2026-11-09-tech-vram-ia-local/video.html').read()
def seg(a,b):
    i=O.index(a); j=O.index(b,i); return O[i:j]
head=O[:O.index('/* ===================== escenas (anclas en palabras de la voz) ===================== */\nconst pa')]
base=head+seg('const pa=(L,T0,w','let SC=[];')+'let SC=[];\n'
kt=seg('function buildKT','/* ===================== subtítulos'); subs=seg('/* ===================== subtítulos','/* ============ indicador')
chip=seg('let lastChip','/* ===================== partículas'); part=seg('/* ===================== partículas','function buildFX')
rend=seg('function drawCv','async function init').replace('[2,3,4,11,12,17].includes(i)','[2,3,4,6,7,9,12,16].includes(i)')
prog,fx,init=tail.split('/*SPLIT*/')
open('video.html','w').write(base+s+kt+subs+prog+chip+part+fx+rend+init)

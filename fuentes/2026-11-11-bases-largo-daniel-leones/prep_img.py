#!/usr/bin/env python3
"""Etalonaje unificado (look de cine) de las 9 imágenes ya ampliadas. Uso: prep_img.py <carpeta_up> -> img/*.jpg"""
import sys, os, numpy as np
from PIL import Image
UP=sys.argv[1]; HERE=os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(HERE,'img'),exist_ok=True)
#           archivo   clave  exposición contraste saturación calidez
SRC=[('img01','T',0.96,1.06,0.90,0.00),('img03','P',1.00,1.04,0.92,0.00),('img04','L',1.00,1.08,0.92,0.02),
     ('img06','M',1.00,1.06,0.92,0.00),('img08','K',0.98,1.08,0.90,0.02),('img02','S',0.98,1.06,0.92,0.00),
     ('img05','V',0.90,1.12,0.86,0.02),('img07','O',0.94,1.10,0.88,0.02),('img09','C',0.86,1.12,0.80,0.03)]
for f,k,ex,co,sa,wa in SRC:
    a=np.asarray(Image.open(os.path.join(UP,f+'.png')).convert('RGB')).astype(np.float32)/255
    a=a*ex
    l=(a*[0.299,0.587,0.114]).sum(2,keepdims=True)
    a=l+(a-l)*sa                                   # saturación
    a=0.5+(a-0.5)*co                               # contraste
    a=np.clip(a,0,1); a=a*a*(3-2*a)*0.35+a*0.65    # curva en S suave
    sh=np.clip(1-l*2.2,0,1); hi=np.clip(l*1.6-0.6,0,1)
    a[:,:,2]+=0.018*sh[:,:,0]; a[:,:,0]-=0.010*sh[:,:,0]     # sombras hacia azul verdoso
    a[:,:,0]+=(0.02+wa)*hi[:,:,0]; a[:,:,2]-=(0.02+wa)*hi[:,:,0]  # luces cálidas
    im=Image.fromarray((np.clip(a,0,1)*255+0.5).astype(np.uint8))
    im.save(os.path.join(HERE,'img',k+'.jpg'),quality=89,subsampling=0); print(k,im.size)

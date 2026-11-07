import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import os
rng=np.random.default_rng(7)
W,H=1920,1080
def noise(h,w,scale):
    n=rng.random((h//scale+2,w//scale+2))
    return np.array(Image.fromarray((n*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(float)/255
# papel envejecido
base=np.zeros((H,W,3))
col=np.array([228,214,184])/255
n=0.55*noise(H,W,300)+0.3*noise(H,W,80)+0.15*noise(H,W,12)
fib=noise(H,W,3)*0.06
img=col[None,None,:]*(0.86+0.2*n[...,None])-fib[...,None]
# manchas
for k in range(14):
    cx,cy=rng.integers(0,W),rng.integers(0,H); r=rng.integers(60,260)
    yy,xx=np.ogrid[:H,:W]; d=np.sqrt((xx-cx)**2+(yy-cy)**2)/r
    ring=np.exp(-((d-1)**2)/0.004)*0.06+np.exp(-d**2*1.5)*0.04
    img-=ring[...,None]*np.array([0.2,0.35,0.6])
# bordes quemados
yy,xx=np.ogrid[:H,:W]
e=np.minimum(np.minimum(xx,W-1-xx)/W,np.minimum(yy,H-1-yy)/H*1.6)
edge=np.clip(1-e*9,0,1)**2*(0.6+0.4*noise(H,W,40))
img=img*(1-edge[...,None]*np.array([0.55,0.62,0.75]))
Image.fromarray((np.clip(img,0,1)*255).astype(np.uint8)).save('assets/papel.jpg',quality=90)
# grano (4 cuadros, PNG con alfa)
for k in range(4):
    g=rng.random((540,960)); a=(np.abs(g-0.5)*2)**3*70
    rgba=np.zeros((540,960,4),np.uint8); v=(g>0.5)*255
    rgba[...,0]=v;rgba[...,1]=v;rgba[...,2]=v;rgba[...,3]=a.astype(np.uint8)
    Image.fromarray(rgba).resize((1920,1080),Image.NEAREST).save(f'assets/grano{k}.png')
# imágenes de Karin en tono sepia
src='../../piloto/archivos-del-tiempo/insumos/'
for f in os.listdir(src):
    if not f.endswith('.jpg'): continue
    im=Image.open(src+f).convert('RGB')
    g=ImageOps.grayscale(im); g=ImageEnhance.Contrast(g).enhance(1.08)
    sep=ImageOps.colorize(g,black=(28,18,10),white=(246,232,204),mid=(150,118,82))
    out=Image.blend(im,sep,0.62)
    out=out.resize((int(out.width*1.62),int(out.height*1.62)),Image.LANCZOS)
    out.save('assets/'+f[:2]+'.jpg',quality=90)
    if f.startswith('05'):
        out.filter(ImageFilter.GaussianBlur(9)).save('assets/05b.jpg',quality=88)
print('ok')

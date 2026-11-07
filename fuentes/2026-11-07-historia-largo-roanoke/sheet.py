import sys,glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob('frames/f_*.jpg')); cols=3; w,h=640,360
rows=(len(fs)+cols-1)//cols; im=Image.new('RGB',(cols*w,rows*(h+26)),'white'); d=ImageDraw.Draw(im)
for i,f in enumerate(fs):
    x=(i%cols)*w;y=(i//cols)*(h+26); im.paste(Image.open(f).resize((w,h)),(x,y+26)); d.text((x+5,y+6),f.split('_')[1][:-4],fill='black')
im.save(sys.argv[1],quality=85)

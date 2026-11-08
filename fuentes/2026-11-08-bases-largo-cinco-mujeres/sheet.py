import sys,glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob('frames/f_*.jpg')); n=len(fs); cols=4; w,h=480,270
rows=(n+cols-1)//cols; im=Image.new('RGB',(cols*w,rows*(h+30)),'white'); d=ImageDraw.Draw(im)
for i,f in enumerate(fs):
    x=(i%cols)*w;y=(i//cols)*(h+30); im.paste(Image.open(f).resize((w,h)),(x,y+30)); d.text((x+5,y+5),f.split('_')[1][:-4],fill='black')
im.save(sys.argv[1] if len(sys.argv)>1 else 'sheet.jpg',quality=85)

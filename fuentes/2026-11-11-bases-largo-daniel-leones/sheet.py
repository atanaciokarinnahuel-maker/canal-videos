import sys,glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob('frames/f_*.jpg')); n=len(fs); cols=int(sys.argv[2]) if len(sys.argv)>2 else 4; w,h=480,270
rows=(n+cols-1)//cols; im=Image.new('RGB',(cols*w,rows*(h+18)),'black'); d=ImageDraw.Draw(im)
for i,f in enumerate(fs):
    x=(i%cols)*w;y=(i//cols)*(h+18); im.paste(Image.open(f).resize((w,h),Image.LANCZOS),(x,y+18)); d.text((x+5,y+3),f.split('_')[1][:-4],fill='white')
im.save(sys.argv[1] if len(sys.argv)>1 else 'sheet.jpg',quality=82)

#!/bin/bash
# Hoja de control: un fotograma por plano -> out/qa/hoja-N.jpg  (uso: scripts/qa.sh [desde] [hasta])
cd "$(dirname "$0")/.." && rm -rf out/qa && mkdir -p out/qa
A=${1:-0}; B=${2:-999}
N=$(npx tsx -e "import('./src/shots.ts').then(m=>console.log(m.SHOTS.length))")
[ $B -ge $N ] && B=$((N-1))
npx remotion render src/index.ts QA out/qa/f --sequence --image-format=jpeg --jpeg-quality=80 --scale=0.3334 --frames=$A-$B --concurrency=4 --log=error 2>&1 | grep -iE "error|not found" | head -5
python3 - "$A" <<'PY'
import glob,sys
from PIL import Image,ImageDraw
fs=sorted(glob.glob('out/qa/f/*.jpeg')); a=int(sys.argv[1]); cols=4; w,h=480,270; per=24
for k in range(0,len(fs),per):
    part=fs[k:k+per]; rows=(len(part)+cols-1)//cols
    im=Image.new('RGB',(cols*w,rows*(h+22)),'black'); d=ImageDraw.Draw(im)
    for i,f in enumerate(part):
        x=(i%cols)*w; y=(i//cols)*(h+22); im.paste(Image.open(f).resize((w,h)),(x,y+22)); d.text((x+6,y+5),'plano %d'%(a+k+i),fill='white')
    im.save('out/qa/hoja-%d.jpg'%(k//per),quality=82)
print(len(fs),'planos')
PY

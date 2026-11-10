#!/bin/bash
# Revisa planos sueltos: scripts/qalist.sh 27 44 115 ...  -> out/qa/lista.jpg
cd "$(dirname "$0")/.." && rm -rf out/qal && mkdir -p out/qal
npx remotion bundle src/index.ts --out-dir=out/bundle --log=error >/dev/null 2>&1
for f in "$@"; do npx remotion still out/bundle QA out/qal/p$(printf %03d $f).jpg --frame=$f --scale=0.3334 --log=error >/dev/null 2>&1 & 
  while [ $(jobs -r | wc -l) -ge 4 ]; do wait -n; done; done; wait
python3 - <<'PY'
import glob
from PIL import Image,ImageDraw
fs=sorted(glob.glob('out/qal/p*.jpg')); cols=4; w,h=480,270; rows=(len(fs)+cols-1)//cols
im=Image.new('RGB',(cols*w,rows*(h+22)),'black'); d=ImageDraw.Draw(im)
for i,f in enumerate(fs):
    x=(i%cols)*w; y=(i//cols)*(h+22); im.paste(Image.open(f).resize((w,h)),(x,y+22)); d.text((x+6,y+5),f[-8:-4],fill='white')
im.save('out/qa/lista.jpg',quality=82); print(len(fs))
PY

#!/bin/bash
# Render por tramos (reanudable). Resultado: out/video.mp4 (sin audio).
cd "$(dirname "$0")/.." && mkdir -p out/parts
[ -d out/bundle ] || npx remotion bundle src/index.ts --out-dir=out/bundle --log=error >/dev/null
TOTAL=$(npx tsx -e "import('./src/tl.ts').then(m=>console.log(m.FRAMES))"); STEP=240
for ((a=0; a<TOTAL; a+=STEP)); do
  b=$((a+STEP-1)); [ $b -ge $TOTAL ] && b=$((TOTAL-1)); f=out/parts/p$(printf %05d $a).mp4
  [ -f "$f" ] && continue
  npx remotion render out/bundle Largo out/parts/tmp.mp4 --frames=$a-$b --muted --concurrency=4 --crf=16 --log=error && mv out/parts/tmp.mp4 "$f" && echo "tramo $a-$b listo $(date +%H:%M:%S)"
done
ls out/parts/p*.mp4 | sed "s#out/parts/#file '#;s#\$#'#" > out/parts/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i out/parts/list.txt -c copy out/video.mp4 && echo FIN

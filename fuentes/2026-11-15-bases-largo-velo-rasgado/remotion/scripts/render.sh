#!/bin/bash
# Render por tramos (reanudable) + mezcla de audio. Resultado: out/el-velo-rasgado.mp4
cd "$(dirname "$0")/.." && mkdir -p out/parts
STEP=120; TOTAL=1080
for ((a=0; a<TOTAL; a+=STEP)); do
  b=$((a+STEP-1)); f=out/parts/p$(printf %04d $a).mp4
  [ -f "$f" ] && continue
  npx remotion render src/index.ts VeloRasgado out/parts/tmp.mp4 --frames=$a-$b --muted --concurrency=4 --crf=15 --log=error && mv out/parts/tmp.mp4 "$f"
  echo "tramo $a-$b listo"
done
ls out/parts/p*.mp4 | sed "s#out/parts/#file '#;s#\$#'#" > out/parts/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i out/parts/list.txt -c copy out/video.mp4
# voz (entra en 1.5 s) + música, normalizado a -14 LUFS para redes
ffmpeg -y -loglevel error -i out/video.mp4 -i public/musica.wav -i public/voz.mp3 -filter_complex \
 "[2:a]adelay=1500:all=1,acompressor=threshold=-24dB:ratio=3:attack=8:release=160:makeup=4,volume=2.2[v];[1:a]volume=0.2[m];[m][v]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart out/el-velo-rasgado.mp4
echo FIN

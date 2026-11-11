#!/bin/bash
# Renderiza los 8 Shorts verticales con su audio (reanudable). -> out/shorts/short-N-<id>.mp4
cd "$(dirname "$0")/.." && mkdir -p out/shorts
[ -d out/bundle ] || npx remotion bundle src/index.ts --out-dir=out/bundle --log=error >/dev/null
[ -f out/voz_proc.wav ] || ffmpeg -y -v error -i public/voz.wav -af "highpass=f=75,acompressor=threshold=-28dB:ratio=3:attack=8:release=220:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9" -ar 44100 -ac 1 out/voz_proc.wav
npx tsx -e "import('./src/shorts.ts').then(m=>m.SHORTS.forEach((s,i)=>console.log(s.n,s.id,s.t0.toFixed(3),s.t1.toFixed(3),(s.t1-s.t0+(i===m.SHORTS.length-1?0:m.SHORT_TAIL)).toFixed(3))))" > out/shorts/lista.txt
while read n id t0 t1 total; do
  f=out/shorts/short-$n-$id.mp4; [ -f "$f" ] && continue
  npx remotion render out/bundle Short$n out/shorts/v$n.mp4 --muted --concurrency=4 --crf=17 --log=error < /dev/null || continue
  vd=$(echo "$t1 - $t0" | bc -l); fo=$(echo "$total - 0.5" | bc -l)
  ffmpeg -y -v error -ss $t0 -t $total -i public/musica.wav -ss $t0 -t $vd -i out/voz_proc.wav -filter_complex \
   "[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad=whole_dur=$total,asplit=2[v1][v2];[0:a]aresample=44100,volume=1.5[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.25,afade=t=out:st=$fo:d=0.5[a]" \
   -map "[a]" -ar 48000 out/shorts/a$n.wav < /dev/null
  ffmpeg -y -v error -i out/shorts/v$n.mp4 -i out/shorts/a$n.wav -map 0:v -map 1:a -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p -c:a aac -b:a 224k -shortest -movflags +faststart out/shorts/tmp.mp4 < /dev/null && mv out/shorts/tmp.mp4 "$f" && rm -f out/shorts/v$n.mp4 out/shorts/a$n.wav && echo "short $n listo $(date +%H:%M:%S)"
done < out/shorts/lista.txt
echo FIN

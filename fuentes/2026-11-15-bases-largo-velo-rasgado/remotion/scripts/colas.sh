#!/bin/bash
# Cambia el final de cada Short por la tarjeta «Mira el video completo» sin re-renderizar todo.
# Toma out/shorts/short-N-*.mp4 (render original) y deja el definitivo en out/shorts-final/.
cd "$(dirname "$0")/.." && mkdir -p out/shorts-final
[ -d out/bundle2 ] || npx remotion bundle src/index.ts --out-dir=out/bundle2 --log=error >/dev/null
npx tsx -e "import('./src/shorts.ts').then(m=>m.SHORTS.forEach(s=>{const a=Math.ceil((s.t1-s.t0)*24); const tot=s.t1-s.t0+m.SHORT_TAIL; console.log(s.n,s.id,s.t0.toFixed(3),s.t1.toFixed(3),tot.toFixed(3),a-12,Math.ceil(tot*24)-1)}))" > out/shorts-final/lista.txt
while read n id t0 t1 total cut last; do
  src=out/shorts/short-$n-$id.mp4; f=out/shorts-final/short-$n-$id.mp4
  [ -f "$src" ] || { echo "falta $src"; continue; }; [ -f "$f" ] && continue
  npx remotion render out/bundle2 Short$n out/shorts-final/t$n.mp4 --frames=$cut-$last --muted --concurrency=4 --crf=17 --log=error < /dev/null || continue
  vd=$(echo "$t1 - $t0" | bc -l); fo=$(echo "$total - 0.5" | bc -l)
  ffmpeg -y -v error -ss $t0 -t $total -i public/musica.wav -ss $t0 -t $vd -i out/voz_proc.wav -filter_complex \
   "[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,apad=whole_dur=$total,asplit=2[v1][v2];[0:a]aresample=44100,volume=1.5,apad=whole_dur=$total[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.25,afade=t=out:st=$fo:d=0.5[a]" \
   -map "[a]" -ar 48000 out/shorts-final/a$n.wav < /dev/null
  ffmpeg -y -v error -i "$src" -i out/shorts-final/t$n.mp4 -i out/shorts-final/a$n.wav -filter_complex "[0:v]trim=end_frame=$cut,setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v]" \
   -map "[v]" -map 2:a -r 24 -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 224k -movflags +faststart out/shorts-final/tmp.mp4 < /dev/null && mv out/shorts-final/tmp.mp4 "$f" && rm -f out/shorts-final/t$n.mp4 out/shorts-final/a$n.wav && echo "short $n final $(date +%H:%M:%S)"
done < out/shorts-final/lista.txt
echo FIN

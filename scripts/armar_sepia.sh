#!/usr/bin/env bash
# Arma un Short de la plantilla sepia a partir de su carpeta en fuentes/ y su voz en insumos-voz/.
# Uso: scripts/armar_sepia.sh <id> <carpeta_de_salida>
# Deja videos/<id>.mp4 (animación + música, sin voz, como el resto del repo) y
# <carpeta_de_salida>/<id>.mp4 (final con voz, misma mezcla que el flujo "Mezclar voz y publicar").
set -e
id="$1"; sal="$2"; raiz="$(cd "$(dirname "$0")/.." && pwd)"; D="$raiz/fuentes/$id"; V="$raiz/insumos-voz/$id"
cp "$raiz/plantillas/sepia/video.html" "$raiz/plantillas/sepia/render.js" "$raiz/plantillas/sepia/musica.py" "$D/"
cp "$V/words.json" "$D/words.json"
cd "$D"; rm -rf frames part_*.mp4
n=$(python3 -c "import json;print(int(round((json.load(open('words.json'))['voice_dur']+1.3)*30)))"); m=$((n/2))
node render.js full 0 $m > r1.log 2>&1 & p1=$!
node render.js full $m $((n+5)) > r2.log 2>&1; wait $p1
if grep -q "PAGEERROR\|ANCLA" r1.log r2.log; then grep -h "PAGEERROR\|ANCLA" r1.log r2.log | sort -u; exit 1; fi
python3 musica.py
printf "file 'part_%05d.mp4'\nfile 'part_%05d.mp4'\n" 0 $m > l.txt
ffmpeg -v error -y -f concat -i l.txt -i musica.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$raiz/videos/$id.mp4"
mkdir -p "$sal"
ffmpeg -y -v error -i "$raiz/videos/$id.mp4" -i "$V/voz.mp3" -filter_complex \
  "[1:a]aresample=44100,apad=pad_dur=6,asplit=2[v1][v2];[0:a]aresample=44100[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 44100 -movflags +faststart "$sal/$id.mp4"
rm -rf frames part_*.mp4 r1.log r2.log l.txt musica.wav
echo "$id: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$sal/$id.mp4") s"

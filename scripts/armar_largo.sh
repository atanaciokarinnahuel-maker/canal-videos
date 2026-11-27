#!/usr/bin/env bash
# Une las partes renderizadas de un video largo (plantilla grabado), le pone la música y mezcla la voz.
# Uso: scripts/armar_largo.sh <carpeta_del_video> <voz.mp3> <salida.mp4>
#   La carpeta debe tener part_*.mp4 (de "node render.js full a b") y musica.wav (de musica_largo.py).
# Misma mezcla que los Shorts: la música baja sola cuando habla la voz (sidechain) y todo a -15 LUFS.
# El video final pesa cientos de MB: NO va al repo (GitHub no acepta archivos de más de 100 MiB).
set -e
D="$1"; voz="$2"; sal="$3"; crf="${CRF:-21}"
cd "$D"
ls part_*.mp4 | sort | sed "s/^/file '/; s/$/'/" > l.txt
ffmpeg -v error -y -f concat -i l.txt -c copy unido.mp4
ffmpeg -y -v error -i unido.mp4 -i musica.wav -i "$voz" -filter_complex \
  "[2:a]aresample=44100,apad=pad_dur=6,asplit=2[v1][v2];[1:a]aresample=44100[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v libx264 -preset medium -crf "$crf" -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 \
  -shortest -movflags +faststart "$sal"
rm -f l.txt unido.mp4
echo "$(basename "$sal"): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$sal") s, $(du -h "$sal" | cut -f1)"

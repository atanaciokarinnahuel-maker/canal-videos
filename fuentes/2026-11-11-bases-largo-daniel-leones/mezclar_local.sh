#!/bin/bash
# Une las partes del render y mezcla música + voz en estéreo (la música baja sola cuando habla la voz).
# Nivel final: ganancia fija hasta -15 LUFS + limitador (sin normalización dinámica, para no inflar la música en las pausas).
# Uso: mezclar_local.sh <musica.wav> <voz-final.wav> <salida.mp4>   (desde esta carpeta, con parts/part_*.mp4 ya renderizadas)
set -e
MUS="$1"; VOZ="$2"; OUT="$3"
ls parts/part_*.mp4 | sort | sed "s#^#file '$PWD/#; s#\$#'#" > parts/lista.txt
ffmpeg -y -v error -f concat -safe 0 -i parts/lista.txt -c copy parts/video_mudo.mp4
FC="[1:a]aresample=44100,highpass=f=65,acompressor=threshold=-24dB:ratio=3:attack=8:release=200:makeup=2,aformat=channel_layouts=stereo,asplit=2[v1][v2];[0:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.6[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=40:release=1500[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0"
ffmpeg -y -v error -i "$MUS" -i "$VOZ" -filter_complex "$FC[a]" -map "[a]" parts/mezcla_cruda.wav
I=$(ffmpeg -hide_banner -nostats -i parts/mezcla_cruda.wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-15-($I),2))"); echo "medido I=$I LUFS -> ganancia ${G} dB"
ffmpeg -y -v error -i parts/video_mudo.mp4 -i parts/mezcla_cruda.wav -af "volume=${G}dB,alimiter=limit=0.84:attack=5:release=80:level=false,aformat=channel_layouts=stereo" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 44100 -movflags +faststart "$OUT"
rm -f parts/mezcla_cruda.wav
ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -vn -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):" | tail -3
ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$OUT"

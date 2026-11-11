#!/bin/bash
# Une las partes del render y mezcla música + voz (la música baja sola cuando habla la voz). Dos pasadas de loudnorm a -15 LUFS.
# Uso: mezclar_local.sh <musica.wav> <voz-final.wav> <salida.mp4>   (se ejecuta desde esta carpeta, con parts/part_*.mp4 ya renderizadas)
set -e
MUS="$1"; VOZ="$2"; OUT="$3"
ls parts/part_*.mp4 | sort | sed "s#^#file '$PWD/#; s#\$#'#" > parts/lista.txt
ffmpeg -y -v error -f concat -safe 0 -i parts/lista.txt -c copy parts/video_mudo.mp4
FC="[2:a]aresample=44100,highpass=f=65,asplit=2[v1][v2];[1:a]aresample=44100,volume=0.6[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=40:release=1500[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0"
M=$(ffmpeg -hide_banner -i parts/video_mudo.mp4 -i "$MUS" -i "$VOZ" -filter_complex "$FC,loudnorm=I=-15:TP=-1.5:LRA=15:print_format=json[a]" -map "[a]" -f null - 2>&1 | sed -n '/^{/,/^}/p')
I=$(echo "$M" | jq -r .input_i); TP=$(echo "$M" | jq -r .input_tp); LRA=$(echo "$M" | jq -r .input_lra); TH=$(echo "$M" | jq -r .input_thresh); OF=$(echo "$M" | jq -r .target_offset)
echo "medido: I=$I TP=$TP LRA=$LRA"
ffmpeg -y -v error -i parts/video_mudo.mp4 -i "$MUS" -i "$VOZ" -filter_complex \
  "$FC,loudnorm=I=-15:TP=-1.5:LRA=15:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$TH:offset=$OF:linear=true,aresample=44100[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 44100 -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$OUT"

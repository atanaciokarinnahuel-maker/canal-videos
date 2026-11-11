#!/bin/bash
# Mezcla una pieza vertical: video mudo + música + voz (la música baja bajo la voz), -14 LUFS con limitador.
# Uso: mezclar_v.sh <video_mudo.mp4> <musica.wav> <voz.wav> <salida.mp4>
set -e
V="$1"; MUS="$2"; VOZ="$3"; OUT="$4"; TMP="${OUT%.mp4}.tmp.wav"
FC="[1:a]aresample=44100,highpass=f=65,acompressor=threshold=-24dB:ratio=3:attack=8:release=200:makeup=2,aformat=channel_layouts=stereo,asplit=2[v1][v2];[0:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.6[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=30:release=900[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0"
ffmpeg -y -v error -i "$MUS" -i "$VOZ" -filter_complex "$FC[a]" -map "[a]" "$TMP"
I=$(ffmpeg -hide_banner -nostats -i "$TMP" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}'); G=$(python3 -c "print(round(-14-($I),2))")
ffmpeg -y -v error -i "$V" -i "$TMP" -af "volume=${G}dB,alimiter=limit=0.84:attack=5:release=80:level=false,aformat=channel_layouts=stereo" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart "$OUT"
rm -f "$TMP"; echo -n "$(basename $OUT): I=$I→-14  "; ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$OUT"

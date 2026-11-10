#!/bin/bash
# Mezcla final: voz procesada + música que baja sola cuando habla la voz (igual que el flujo "Mezclar voz"). -> out/<ID>.mp4
cd "$(dirname "$0")/.." && ID=2026-11-15-bases-largo-velo-rasgado
ffmpeg -y -v error -i public/voz.wav -af "highpass=f=75,acompressor=threshold=-28dB:ratio=3:attack=8:release=220:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9" -ar 44100 -ac 1 out/voz_proc.wav
ffmpeg -y -v error -i public/musica.wav -i out/voz_proc.wav -filter_complex \
 "[1:a]aresample=44100,pan=stereo|c0=c0|c1=c0,asplit=2[v1][v2];[0:a]aresample=44100,volume=1.5[bed];[bed][v1]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[duck];[duck][v2]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map "[a]" -ar 48000 -c:a pcm_s16le out/mezcla.wav
if [ -f out/video.mp4 ]; then
  ffmpeg -y -v error -i out/video.mp4 -i out/mezcla.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart out/$ID.mp4
  ffprobe -v error -show_entries format=duration,size -of csv=p=0 out/$ID.mp4
fi
ffmpeg -hide_banner -i out/mezcla.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "^ +I:|Peak:" | tail -2

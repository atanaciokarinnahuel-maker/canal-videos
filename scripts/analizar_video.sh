#!/usr/bin/env bash
# Baja un video de referencia y deja en analisis/<id>/ hojas de fotogramas, lista de cortes y un reporte.
# El video NO se guarda en el repo. Uso: analizar_video.sh analisis/pedidos/<id>.json
# Pedido: {"id": "...", "drive_id": "...", "youtube_id": "..."} (alcanza con uno de los dos orígenes).
# Para probar sin red: VIDEO_LOCAL=/ruta/video.mp4 analizar_video.sh pedido.json
set -u
pedido="$1"
id=$(jq -r .id "$pedido")
drive=$(jq -r '.drive_id // empty' "$pedido")
yt=$(jq -r '.youtube_id // empty' "$pedido")
out="analisis/$id"
tmp=$(mktemp -d)
v="$tmp/video.mp4"
rm -rf "$out"; mkdir -p "$out"
rep="$out/reporte.txt"
echo "pedido: $id" > "$rep"

es_video() { ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$1" 2>/dev/null | grep -q .; }

ok=0
if [ -n "${VIDEO_LOCAL:-}" ]; then
  cp "$VIDEO_LOCAL" "$v" && ok=1 && echo "origen: archivo local" >> "$rep"
fi
if [ $ok = 0 ] && [ -n "$drive" ]; then
  curl -sSL -o "$v" "https://drive.usercontent.google.com/download?id=${drive}&export=download&confirm=t" || true
  if es_video "$v"; then ok=1; echo "origen: drive" >> "$rep"
  else echo "drive: no se pudo bajar (el archivo no está compartido por enlace)" >> "$rep"; rm -f "$v"; fi
fi
if [ $ok = 0 ] && [ -n "$yt" ]; then
  pip install -q yt-dlp >/dev/null 2>&1 || true
  yt-dlp -q --no-playlist -f "bv*[height<=480]+ba/b[height<=480]/b" --merge-output-format mp4 \
    -o "$v" "https://www.youtube.com/watch?v=${yt}" 2> "$tmp/yt.txt" || true
  if es_video "$v"; then ok=1; echo "origen: youtube" >> "$rep"
  else echo "youtube: no se pudo bajar: $(tail -n 2 "$tmp/yt.txt" | tr '\n' ' ' | cut -c1-300)" >> "$rep"; rm -f "$v"; fi
fi
if [ $ok = 0 ]; then echo "RESULTADO: sin video" >> "$rep"; rm -rf "$tmp"; exit 0; fi

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
{
  echo "duracion_s: $dur"
  echo "tamano_bytes: $(stat -c %s "$v")"
  echo "video: $(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate -of csv=p=0 "$v")"
  echo "audio: $(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of csv=p=0 "$v")"
} >> "$rep"

fuente=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
marca="drawtext=fontfile=${fuente}:text='%{pts\:hms}':x=4:y=4:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6"
caja() { echo "scale=$1:$2:force_original_aspect_ratio=decrease,pad=$1:$2:(ow-iw)/2:(oh-ih)/2"; }

# 1) Todo el video: 1 fotograma cada 4 s, 30 por hoja.
ffmpeg -v error -y -i "$v" -an -vf "fps=1/4,$(caja 320 180),${marca},tile=6x5" -q:v 6 "$out/general_%02d.jpg"
# 2) Gancho: primeros 90 s, 1 fotograma por segundo, más grande.
ffmpeg -v error -y -t 90 -i "$v" -an -vf "fps=1,$(caja 480 270),${marca},tile=5x6" -q:v 5 "$out/gancho_%02d.jpg"
# 3) Cierre: últimos 60 s, 1 fotograma por segundo.
ffmpeg -v error -y -sseof -60 -i "$v" -an -vf "fps=1,$(caja 480 270),tile=5x6" -q:v 5 "$out/cierre_%02d.jpg"
# 4) Fotogramas grandes para ver estilo y textos en pantalla.
n=0
for p in 0.002 0.02 0.10 0.30 0.50 0.70 0.90 0.985; do
  n=$((n+1)); t=$(awk -v d="$dur" -v p="$p" 'BEGIN{printf "%.2f", d*p}')
  ffmpeg -v error -y -ss "$t" -i "$v" -an -frames:v 1 -vf "scale=1280:-2" -q:v 4 "$out/detalle_$(printf %02d $n)_${t%.*}s.jpg"
done
# 5) Cortes de plano (cambios de escena).
ffmpeg -v error -y -i "$v" -an -vf "scale=320:-2,select='gt(scene,0.25)',showinfo" -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$out/cortes.txt" || true
c=$(wc -l < "$out/cortes.txt")
{
  echo "cortes_detectados: $c"
  awk -v d="$dur" -v c="$c" 'BEGIN{ if (c>0) printf "plano_promedio_s: %.1f\n", d/(c+1) }'
  echo "cortes_por_minuto:"
  awk '{m=int($1/60); k[m]++} END{for(i=0;i<=m;i++) printf "  min %02d: %d\n", i, k[i]+0}' "$out/cortes.txt"
  echo "RESULTADO: ok"
} >> "$rep"
rm -rf "$tmp"

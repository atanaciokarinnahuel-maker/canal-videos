#!/usr/bin/env python3
"""Arma la voz final de un largo: corta repeticiones/errores según "segmentos"
[[inicio, fin, pausa_despues], ...] (segundos del audio original) y, si
"procesar_voz" es true, ecualiza + comprime + normaliza a -16 LUFS.
Uso: preparar_voz.py job.json entrada salida.wav"""
import json, subprocess, sys
job = json.load(open(sys.argv[1])); src, out = sys.argv[2], sys.argv[3]
segs = job.get('segmentos') or []
parts, labels = [], []
for k, s in enumerate(segs):
    a, b = float(s[0]), float(s[1]); pd = float(s[2]) if len(s) > 2 else 0.0
    f = f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={max(0,b-a-0.025):.3f}:d=0.025"
    if pd > 0: f += f",apad=pad_dur={pd}"
    parts.append(f + f"[s{k}]"); labels.append(f"[s{k}]")
chain = "highpass=f=75,acompressor=threshold=-28dB:ratio=3:attack=8:release=220:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9" if job.get('procesar_voz') else "anull"
if parts:
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1,aresample=44100,{chain}[v]"
else:
    fc = f"[0:a]aresample=44100,{chain}[v]"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-filter_complex', fc, '-map', '[v]', '-ac', '1', '-ar', '44100', out], check=True)

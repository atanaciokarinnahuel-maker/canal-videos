#!/usr/bin/env python3
"""Hace una voz más grave y más lenta sin volver a generarla (no gasta créditos).
Baja la velocidad de reproducción (como una cinta más lenta): el tono y el ritmo bajan juntos
y no aparecen los artefactos de un cambiador de tono. Ajusta también los tiempos de words.json.
Uso: voz_grave.py carpeta_insumos factor   (0.91 = 9 % más lenta y ~1,6 semitonos más grave)
Guarda la toma anterior como voz_normal.mp3 y words_normal.json."""
import json, os, subprocess, sys
d, k = sys.argv[1], float(sys.argv[2])
mp3, wj = os.path.join(d, "voz.mp3"), os.path.join(d, "words.json")
base_mp3, base_wj = os.path.join(d, "voz_normal.mp3"), os.path.join(d, "words_normal.json")
if not os.path.exists(base_mp3): os.replace(mp3, base_mp3); os.replace(wj, base_wj)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", base_mp3, "-af", f"asetrate={int(44100 * k)},aresample=44100,bass=g=2.5:f=120",
                "-b:a", "128k", mp3], check=True)
w = json.load(open(base_wj))
for x in w["words"]: x["start"] = round(x["start"] / k, 3); x["end"] = round(x["end"] / k, 3)
w["voice_dur"] = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                                            capture_output=True, text=True).stdout), 2)
w["grave"] = k
json.dump(w, open(wj, "w"), ensure_ascii=False)
print(f"{d}: factor {k}, {w['voice_dur']} s")

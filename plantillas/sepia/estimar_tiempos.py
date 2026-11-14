#!/usr/bin/env python3
"""Genera un words.json ESTIMADO a partir del guion, para armar y revisar la animación antes de
tener la voz. Cuando exista la voz real, se reemplaza words.json por los tiempos reales y se
vuelve a renderizar: las escenas están ancladas a palabras, no a segundos.
Uso: estimar_tiempos.py guion_voz.txt words.json [segundos_por_silaba]"""
import json, re, sys
texto = open(sys.argv[1], encoding='utf-8').read().split()
rate = float(sys.argv[3]) if len(sys.argv) > 3 else 0.165
def silabas(w):
    w = re.sub(r'[^a-záéíóúüñ0-9]', '', w.lower())
    if w.isdigit(): return 2 * len(w)
    return max(1, len(re.findall(r'[aeiouáéíóúü]+', w)))
t, out = 0.0, []
for w in texto:
    d = silabas(w) * rate + 0.03
    out.append({"text": w, "start": round(t, 3), "end": round(t + d, 3)})
    t += d + (0.42 if re.search(r'[.?!…]$', w) else 0.2 if re.search(r'[,:;]$', w) else 0.02)
json.dump({"words": out, "voice_dur": round(t, 2), "estimado": True}, open(sys.argv[2], 'w'), ensure_ascii=False)
print(len(out), 'palabras,', round(t, 1), 's estimados')

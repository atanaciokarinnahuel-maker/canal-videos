#!/usr/bin/env python3
"""Genera la voz de un guion con la API de ElevenLabs y saca los tiempos reales de cada palabra.
Uso: generar_voz.py guion_voz.txt carpeta_salida [voice_id] [modelo] [max_segundos]
Si la toma dura más que max_segundos (57 por defecto), se acelera lo justo (tope x1,15) y se
ajustan los tiempos; la toma original queda como voz_original.mp3.
Deja en la carpeta: voz.mp3, alineacion.json (respuesta cruda de tiempos) y words.json
({"words": [{"text", "start", "end"}], "voice_dur"}), que es lo que lee la animación.
La clave NO va en este archivo ni en variables: el proxy de la sesión la agrega sola al
encabezado xi-api-key (secreto de red del entorno "canal-videos").
OJO: cada llamada gasta créditos (1 por carácter con eleven_v4). No reintentar a ciegas."""
import base64, json, os, subprocess, sys, tempfile

guion, out = sys.argv[1], sys.argv[2]
voz = sys.argv[3] if len(sys.argv) > 3 else "18GZPpJvaVG53Nt3H52N"   # Sam Adam
modelo = sys.argv[4] if len(sys.argv) > 4 else "eleven_v4"
maximo = float(sys.argv[5]) if len(sys.argv) > 5 else 57.0
texto = " ".join(open(guion, encoding="utf-8").read().split())
os.makedirs(out, exist_ok=True)

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump({"text": texto, "model_id": modelo}, f, ensure_ascii=False)
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps?output_format=mp3_44100_128"
r = subprocess.run(["curl", "-sS", "--max-time", "300", "-X", "POST", url, "-H", "Content-Type: application/json",
                    "--data-binary", "@" + f.name], capture_output=True)
os.unlink(f.name)
try:
    d = json.loads(r.stdout)
except Exception:
    sys.exit("Respuesta no válida: " + r.stdout[:300].decode("utf-8", "replace") + r.stderr.decode()[:300])
if "audio_base64" not in d:
    sys.exit("ElevenLabs no devolvió audio: " + json.dumps(d, ensure_ascii=False)[:500])

open(os.path.join(out, "voz.mp3"), "wb").write(base64.b64decode(d["audio_base64"]))
al = d.get("alignment") or d.get("normalized_alignment")
json.dump({k: d.get(k) for k in ("alignment", "normalized_alignment")}, open(os.path.join(out, "alineacion.json"), "w"), ensure_ascii=False)
ch, t0, t1 = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
words, cur, a, b = [], "", None, None
for c, s, e in zip(ch, t0, t1):
    if c.isspace():
        if cur: words.append({"text": cur, "start": round(a, 3), "end": round(b, 3)})
        cur, a, b = "", None, None
    else:
        if a is None: a = s
        cur += c; b = e
if cur: words.append({"text": cur, "start": round(a, 3), "end": round(b, 3)})
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            os.path.join(out, "voz.mp3")], capture_output=True, text=True).stdout)
tempo = 1.0
if dur > maximo:
    tempo = round(min(1.15, dur / (maximo - 0.5)), 3)
    mp3 = os.path.join(out, "voz.mp3"); orig = os.path.join(out, "voz_original.mp3"); os.replace(mp3, orig)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", orig, "-af", f"atempo={tempo}", "-ar", "44100", "-b:a", "128k", mp3], check=True)
    for w in words: w["start"] = round(w["start"] / tempo, 3); w["end"] = round(w["end"] / tempo, 3)
    dur = dur / tempo
json.dump({"words": words, "voice_dur": round(dur, 2), "modelo": modelo, "voz": voz, "caracteres": len(texto), "tempo": tempo},
          open(os.path.join(out, "words.json"), "w"), ensure_ascii=False)
print(f"{len(words)} palabras, {dur:.2f} s, {len(texto)} caracteres, modelo {modelo}, tempo x{tempo}")

#!/usr/bin/env python3
"""Genera una narración con varias voces (narrador, Dios, Jesús, personajes, multitud) y deja
voz.mp3 + words.json listos para la plantilla sepia.

Uso: generar_dialogo.py lineas.json carpeta_salida

lineas.json:
{
 "modelo": "eleven_v4",
 "grave": 0.94,                       # velocidad de reproducción (0.94 = más lenta y grave); 1 = sin cambio
 "voces": {"narrador": "<voice_id>", "dios": "<voice_id>", ...},
 "lineas": [
   {"v": "narrador", "t": "[whispers] Texto con etiquetas de emoción…", "pausa": 0.5},
   {"v": "dios", "t": "…", "efecto": "eco"},
   {"v": ["a", "b", "c"], "t": "¡Crucifícale!", "efecto": "multitud"}
 ]
}

- Cada línea generada se guarda en carpeta_salida/lineas/ con un nombre que depende de la voz, el modelo
  y el texto: si se vuelve a correr, NO se vuelve a pagar. Para regenerar una línea, borrá su archivo.
- Las etiquetas entre corchetes ([whispers], [deep voice]…) indican la emoción a ElevenLabs y no aparecen
  en los subtítulos.
- La clave de ElevenLabs la agrega el proxy de la sesión (encabezado xi-api-key); no va en este archivo.
"""
import base64, hashlib, json, os, re, subprocess, sys

cfg = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
modelo = cfg.get("modelo", "eleven_v4"); grave = float(cfg.get("grave", 1.0)); voces = cfg["voces"]
cache = os.path.join(out, "lineas"); os.makedirs(cache, exist_ok=True)
tmp = os.path.join(out, "tmp"); os.makedirs(tmp, exist_ok=True)
gastados = 0

def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)

def tts(voz, texto):
    """Devuelve (mp3, palabras) de una línea, usando la caché si existe."""
    global gastados
    h = hashlib.sha1(f"{voz}|{modelo}|{texto}".encode()).hexdigest()[:16]
    mp3, js = os.path.join(cache, h + ".mp3"), os.path.join(cache, h + ".json")
    if not (os.path.exists(mp3) and os.path.exists(js)):
        body = os.path.join(tmp, "body.json")
        json.dump({"text": texto, "model_id": modelo}, open(body, "w", encoding="utf-8"), ensure_ascii=False)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voz}/with-timestamps?output_format=mp3_44100_128"
        r = subprocess.run(["curl", "-sS", "--max-time", "300", "-X", "POST", url, "-H", "Content-Type: application/json",
                            "--data-binary", "@" + body], capture_output=True)
        try:
            d = json.loads(r.stdout)
        except Exception:
            sys.exit("Respuesta no válida de ElevenLabs: " + r.stdout[:300].decode("utf-8", "replace"))
        if "audio_base64" not in d:
            sys.exit("ElevenLabs no devolvió audio: " + json.dumps(d, ensure_ascii=False)[:400])
        open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
        json.dump({"texto": texto, "voz": voz, "modelo": modelo, "alignment": d.get("alignment") or d.get("normalized_alignment")},
                  open(js, "w", encoding="utf-8"), ensure_ascii=False)
        gastados += len(texto)
    al = json.load(open(js, encoding="utf-8"))["alignment"]
    words, cur, a, b, prof = [], "", None, None, 0
    for c, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c == "[": prof += 1; continue
        if c == "]": prof = max(0, prof - 1); continue
        if prof: continue                                    # texto de etiqueta: no va a los subtítulos
        if c.isspace():
            if cur: words.append({"text": cur, "start": a, "end": b})
            cur, a, b = "", None, None
        else:
            if a is None: a = s
            cur += c; b = e
    if cur: words.append({"text": cur, "start": a, "end": b})
    return mp3, words

partes, todas, t = [], [], 0.0
for k, ln in enumerate(cfg["lineas"]):
    vs = ln["v"] if isinstance(ln["v"], list) else [ln["v"]]
    gen = [tts(voces[v], ln["t"]) for v in vs]
    mp3, words = gen[0]
    seg = os.path.join(tmp, f"seg_{k:03d}.wav")
    ef = ln.get("efecto", "")
    k_g = float(ln.get("grave", grave))
    base = f"asetrate={int(44100 * k_g)},aresample=44100" if k_g != 1 else "anull"
    if ef == "multitud" and len(gen) > 1:
        ins, fl = [], []
        for i, (m, _) in enumerate(gen):
            ins += ["-i", m]
            pan = [-.6, .6, -.25, .25, 0][i % 5]; dl = 45 * i
            fl.append(f"[{i}:a]{base},adelay={dl}|{dl},pan=stereo|c0={1 - pan:.2f}*c0|c1={1 + pan:.2f}*c0[m{i}]")
        fc = ";".join(fl) + ";" + "".join(f"[m{i}]" for i in range(len(gen))) + \
             f"amix=inputs={len(gen)}:normalize=0,aecho=0.8:0.5:70|130:0.25|0.15,volume=0.6,pan=mono|c0=.5*c0+.5*c1[o]"
        subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[o]", "-ar", "44100", "-ac", "1", seg], check=True)
    else:
        chain = base
        if ef == "eco":                                     # palabras de Dios: más presencia y un eco leve
            chain += ",bass=g=3:f=110,acompressor=threshold=-24dB:ratio=3:attack=5:release=200:makeup=3,aecho=0.85:0.55:95|190:0.28|0.14"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-af", chain, "-ar", "44100", "-ac", "1", seg], check=True)
    for w in words:
        todas.append({"text": w["text"], "start": round(t + w["start"] / k_g, 3), "end": round(t + w["end"] / k_g, 3), "v": vs[0]})
    d = dur(seg); pausa = float(ln.get("pausa", 0.45))
    partes.append((seg, pausa)); t += d + pausa

lst = os.path.join(tmp, "lista.txt")
with open(lst, "w") as f:
    for i, (seg, pausa) in enumerate(partes):
        sil = os.path.join(tmp, f"sil_{i:03d}.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{pausa:.3f}", sil], check=True)
        f.write(f"file '{os.path.abspath(seg)}'\nfile '{os.path.abspath(sil)}'\n")
voz = os.path.join(out, "voz.mp3")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "44100", "-b:a", "160k", voz], check=True)
total = dur(voz)
json.dump({"words": todas, "voice_dur": round(total, 2), "modelo": modelo, "grave": grave}, open(os.path.join(out, "words.json"), "w"), ensure_ascii=False)
subprocess.run(["rm", "-rf", tmp])
print(f"{len(cfg['lineas'])} líneas, {len(todas)} palabras, {total:.1f} s; créditos gastados en esta corrida: ~{gastados}")

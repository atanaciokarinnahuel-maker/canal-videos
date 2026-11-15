#!/usr/bin/env python3
"""Inserta una frase nueva en una voz ya generada, sin regenerar toda la toma.
Uso: insertar_frase.py carpeta_insumos carpeta_frase palabra_anterior n_aparicion
carpeta_frase: salida de generar_voz.py con la frase sola. Se inserta después de la palabra indicada."""
import json, os, re, subprocess, sys, unicodedata
d, f, pal, occ = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
norm = lambda s: re.sub(r"[^a-z0-9ñ]", "", "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn"))
A = json.load(open(os.path.join(d, "words.json"))); N = json.load(open(os.path.join(f, "words.json")))
w, nw = A["words"], N["words"]
c = 0
for i, x in enumerate(w):
    if norm(x["text"]) == norm(pal):
        c += 1
        if c == occ: break
else: sys.exit("No encontré la palabra")
cut1 = w[i]["end"] + 0.12; cut2 = w[i + 1]["start"] - 0.10
n0 = max(0, nw[0]["start"] - 0.05); n1 = nw[-1]["end"] + 0.12; g1, g2 = 0.38, 0.42
mp3 = os.path.join(d, "voz.mp3"); orig = os.path.join(d, "voz_sin_frase.mp3"); os.replace(mp3, orig)
fc = (f"[0:a]atrim=0:{cut1},asetpts=PTS-STARTPTS,afade=t=out:st={cut1-0.03:.3f}:d=0.03,apad=pad_dur={g1}[a];"
      f"[1:a]atrim={n0}:{n1},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={n1-n0-0.03:.3f}:d=0.03,apad=pad_dur={g2}[b];"
      f"[0:a]atrim={cut2},asetpts=PTS-STARTPTS,afade=t=in:d=0.02[c];[a][b][c]concat=n=3:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", orig, "-i", os.path.join(f, "voz.mp3"), "-filter_complex", fc, "-map", "[o]",
                "-ar", "44100", "-b:a", "128k", mp3], check=True)
o1 = cut1 + g1 - n0; o2 = cut1 + g1 + (n1 - n0) + g2 - cut2
out = w[:i + 1] + [{"text": x["text"], "start": round(x["start"] + o1, 3), "end": round(x["end"] + o1, 3)} for x in nw] + \
      [{"text": x["text"], "start": round(x["start"] + o2, 3), "end": round(x["end"] + o2, 3)} for x in w[i + 1:]]
A["words"] = out
A["voice_dur"] = round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                                            capture_output=True, text=True).stdout), 2)
A["caracteres"] = A.get("caracteres", 0) + N.get("caracteres", 0)
json.dump(A, open(os.path.join(d, "words.json"), "w"), ensure_ascii=False)
print(f"frase insertada después de '{w[i]['text']}': {len(nw)} palabras, total {A['voice_dur']} s")

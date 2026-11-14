#!/usr/bin/env python3
"""Transcribe un audio con Whisper (faster-whisper, en CPU) y escribe un texto con tiempos.
Uso: transcribir.py audio.wav salida.txt [modelo] [idioma]"""
import sys
from faster_whisper import WhisperModel

origen, salida = sys.argv[1], sys.argv[2]
modelo = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "small"
idioma = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] else "es"

m = WhisperModel(modelo, device="cpu", compute_type="int8")
segmentos, _ = m.transcribe(origen, language=idioma, vad_filter=True, beam_size=5)
with open(salida, "w", encoding="utf-8") as f:
    for s in segmentos:
        t = int(s.start)
        f.write(f"[{t // 60}:{t % 60:02d}] {s.text.strip()}\n")

#!/usr/bin/env python3
"""Transcribe un audio con Whisper (faster-whisper, en CPU) y escribe un texto con tiempos.
Uso: transcribir.py audio.wav salida.txt [modelo] [idioma]
El audio debe ser WAV mono de 16 kHz y 16 bits (lo prepara analizar_video.sh con ffmpeg).
Se lee con el módulo wave para no depender de la versión de PyAV instalada."""
import sys
import wave

import numpy as np
from faster_whisper import WhisperModel

origen, salida = sys.argv[1], sys.argv[2]
modelo = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "small"
idioma = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] else "es"

m = WhisperModel(modelo, device="cpu", compute_type="int8")
with wave.open(origen, "rb") as w:
    if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (16000, 1, 2):
        sys.exit("El audio debe ser WAV mono, 16 kHz, 16 bits")
    audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segmentos, _ = m.transcribe(audio, language=idioma, vad_filter=True, beam_size=5)
with open(salida, "w", encoding="utf-8") as f:
    for s in segmentos:
        t = int(s.start)
        f.write(f"[{t // 60}:{t % 60:02d}] {s.text.strip()}\n")

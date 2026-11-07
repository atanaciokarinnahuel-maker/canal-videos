# Largo HistorIAs · 7 nov 2026 · La colonia perdida de Roanoke
- Voz: Karin (Drive, 2026-11-07-roanoke.m4a, 508 s). Transcripción ElevenLabs Scribe → `words_raw.json`.
- `cortes.py` → `timeline.json`: 15 repeticiones/arranques en falso eliminados + 1,1 s de pausa antes de cada capítulo (voz final 436 s).
  Los mismos `segmentos` van en `jobs/<id>.json`; el workflow `mezclar.yml` los aplica con `scripts/preparar_voz.py` (cortes + EQ + compresión + -16 LUFS).
- `subs.py` → subtítulos frase por frase (corrige nombres: Croatoan, Hatteras, Harvie).
- `escenas.py` → `data.json` (59 escenas, 8 capítulos) · `video.html` (motor) · `render.py full A B` (4 partes en paralelo, 24 fps) · `musica.py` (música generada, -22 dB, golpes en los giros).
- Imágenes de Karin usadas (válidas según LEEME-correcciones): 02 (grabado 1876), 05 (solo fondo desenfocado), 06, 07, 09.
- Descarga de insumos desde Drive/ElevenLabs: workflow `descargar.yml` (el entorno de Claude no llega a esos dominios).

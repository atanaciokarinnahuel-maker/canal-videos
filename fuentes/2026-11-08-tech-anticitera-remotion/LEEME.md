# Short de Anticitera hecho con Remotion (prueba de comparación)
- Render: `npm install && npx remotion render src/index.ts Anticitera out/video.mp4 --muted` (usa Chrome del sistema, ver remotion.config.ts).
- Música/efectos: `python3 audio/musica.py` → musica.wav; se mezcla con ffmpeg y la voz se agrega por GitHub Actions (jobs/).
- Tiempos de la voz: src/words.ts (transcripción ElevenLabs scribe). Si cambia la voz, actualizar words.ts y los tiempos fijos en src/scenes*.tsx.
- Voz: JC (eleven_v4). Datos: ver guion.txt.

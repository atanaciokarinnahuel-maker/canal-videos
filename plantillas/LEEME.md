# Guía de retención y plantillas (Tecnología e IA + Bases Bíblicas)

Basada en el análisis de 3 videos de referencia de Karin (explainer de la grapadora, promo "/full-visual", promo "/effects") y en los videos propios ya hechos (mitos del celular, PC lenta TURBO).

## 1. Fórmula de retención (se aplica a TODO video nuevo)
1. **Cero segundos muertos.** Algo cambia en pantalla cada 1–2 s (zoom, elemento nuevo, palabra resaltada, transición). Nunca más de 2,5 s con la imagen igual.
2. **Gancho visual en el primer segundo** y pregunta/promesa en los primeros 2–3 s ("¿Tu PC va lenta…? ¡Espera!").
3. **Bucle abierto + recompensa tardía.** Anunciar al inicio algo que llega al final ("al final, un truco bonus") y mostrar un indicador que lo recuerde (candado, velocímetro, tarjeta tapada con "???"). La recompensa llega al ~85 % del video, no antes.
4. **Indicador de progreso entretenido** en lugar de una barra lisa. Variar: velocímetro turbo, 3 tarjetas que se rompen, candado que se abre, cofre, batería que se carga, mecha que se quema. Debe subir de forma continua y terminar con celebración (confeti + destello).
5. **Interruptor de atención a mitad del video (35–45 %).** Giro ("¿y si lo giras?"), broma o pausa de personalidad de Chispa (guiño, "sígueme", mini-chiste). Resetea la atención justo donde cae la retención.
6. **Subtítulos palabra por palabra**, grandes, con la palabra activa resaltada. Zona segura: nada importante bajo y=1560 ni sobre y=110. Para explainers continuos se pueden poner arriba con caja de selección en la palabra clave.
7. **Mostrar el resultado, no prometerlo** (la acción ocurre en pantalla: clic, tecla, programa que se cierra).
8. **Prueba social/abundancia** cuando sea real (cifras verificables, cuadrículas de ejemplos). Nunca inventar vistas ni cifras.
9. **Cierre con pregunta o palabra clave para comentarios** ("¿Cuál mito creías tú?"). No prometer enlaces/guías que no existan.
10. **Sonido:** música sin voz con efectos alineados a cada golpe visual; volumen medio final ≈ -14 a -15 dB (la voz se mezcla después por GitHub Actions con la música bajando sola).

## 2. Formatos (se alternan)
- **A) Explainer continuo** ("¿Cómo funciona…?"): una sola animación SVG que se transforma sin cortes duros, 45–60 s. Subtítulos con caja de selección. Estructura: gancho → mecanismo paso a paso → giro a la mitad → remate útil → cierre.
- **B) Demo con comandos y contadores:** pantalla tipo chat que "escribe" el pedido, resultado inmediato, indicador de progreso y cierre con pregunta.
- **C) Karin a cámara + efectos animados** (widgets, titulares, túneles): SOLO cuando Karin haya enviado un clip en el chat. La tarea nocturna NO puede hacerlo sola.
- Plantillas reutilizables en este repo: `plantillas/mitos/` (tarjetas de vidrio que se rompen a martillazos) y `plantillas/turbo/` (velocímetro + PC en 3D + synthwave). Para usarlas: copiar a `fuentes/<id>/`, cambiar `words.json` (tiempos reales de la voz) y las constantes de tiempo del `video.html`, renderizar con `python3 render.py full A B` (mitades en paralelo) y generar música con `musica.py`.

## 3. Series de Tecnología (rotar en este orden, un video por noche)
1. **IA práctica** (herramientas, prompts, agentes que se pueden usar hoy; siempre con pasos concretos y verificar nombres/funciones vigentes con WebSearch).
2. **Seguridad profunda** (cómo funciona el robo de WhatsApp, SIM swap, phishing, deepfakes, QR falsos, contraseñas y verificación en dos pasos).
3. **Reparación por dentro** (oficio de Karin en BITKAR: batería hinchada, pantallas, puertos de carga, celular mojado, PC que se calienta; explicado por dentro).
Después volver a la 1. Mezclar el ángulo "¿Cómo funciona…?" dentro de cada serie.

Bancos de temas (verificar cada dato antes de escribir; no repetir los ya hechos en jobs/ y fuentes/):
- IA práctica: 5 pedidos que mejoran cualquier respuesta de una IA; usar IA para revisar una factura o contrato (sin pegar datos personales); IA para detectar estafas; resumir un PDF largo; preparar una clase/guion con IA; qué es un agente de IA y qué NO debes delegarle; por qué la IA "inventa" cosas.
- Seguridad profunda: cómo te roban el WhatsApp con el código; SIM swap; qué es el phishing y 5 señales; deepfakes de voz (llamada del "familiar"); por qué un QR puede ser falso; verificación en dos pasos explicada; por qué reutilizar contraseñas es peligroso.
- Reparación por dentro: por qué se hincha una batería y qué hacer; por qué el celular se calienta; qué pasa por dentro cuando se moja; puerto de carga sucio vs roto; por qué una PC se apaga sola; SSD vs disco duro por dentro.

## 4. Paquete para otras plataformas (solo Bases Bíblicas, que se publica solo)
Karin quiere recibir el video terminado + descripción + hashtags DESPUÉS de que se publique automáticamente, para subirlo él a otras plataformas. La tarea nocturna de Bases escribe `paquetes/<id>.json`:
```
{"id":"<id>","titulo":"<≤70 caracteres>","descripcion":"<3–4 líneas>","hashtags":["#...", "..."]}
```
(8–10 hashtags universales: temáticos + #shorts #reels; en español.) La tarea de las 07:22 lo lee, arma el mp4 con audio y se lo envía.

## 5. Plantilla "sepia" (serie "Estaba escrito", Bases Bíblicas)
Grabado antiguo sobre pergamino, dibujado por código en SVG. Carpeta `plantillas/sepia/`.
- `video.html`: motor y biblioteca de escenas (`rollo`, `jardin`, `pareja`, `serpiente`, `talon`, `pesebre`, `escritura`, `cruz`, `nombre`, `biblia`). Las figuras no tienen rasgos de rostro a propósito: así un personaje no cambia de cara entre escenas.
- `escenas.json` (uno por video): lista de escenas con su palabra ancla (`"en": ["palabra", n.º de aparición, desfase en s]`), movimiento de cámara, referencias bíblicas en pantalla y el sello "CUMPLIDA". Las escenas siguen a las palabras, no a los segundos: al cambiar la voz solo se reemplaza `words.json`.
- `estimar_tiempos.py guion_voz.txt words.json`: tiempos ESTIMADOS para armar la animación antes de tener la voz. Con la voz real hay que reemplazar `words.json` por los tiempos reales y volver a renderizar.
- `render.js` (Node + Playwright): `node render.js frames 0,5,10` para revisar cuadros; `node render.js full 0 860` y `node render.js full 860 1720` en paralelo para el video, y unir con ffmpeg.
- Ritmo: una escena cada 4–8 s con cámara en movimiento continuo y subtítulos de 2–3 palabras. Es más lento que la regla de "algo cambia cada 1–2 s" del punto 1; es una prueba pedida por Karin el 14 nov.
- Falta: música propia de la plantilla (los videos anteriores la generan con `musica.py`) y las escenas de los Shorts 2 a 19.

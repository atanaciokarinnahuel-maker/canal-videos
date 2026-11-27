# Video largo "Estaba escrito" (Bases Bíblicas) — decisiones de Karin (26 nov 2026)

Respuestas de Karin a las preguntas previas (el video es largo y gasta muchos créditos).

## Formato
- Horizontal 16:9. Hay que adaptar la plantilla sepia (hoy es vertical) una sola vez.
- Total 25–30 minutos, en **dos partes**. Parte 1: 13–15 minutos, cortada en la mitad exacta por tiempo, en un momento de suspenso,
  y termina invitando a suscribirse para la parte 2 ("otro video de profecías sobre Jesús").
- Estructura: **orden de la Biblia** (de Génesis en adelante), cada profecía con su cumplimiento.
- Profecías: las 19 de la serie **y algunas más** (por ejemplo Gn 49:10, Nm 21 serpiente de bronce, Dt 18:15, Is 7:14, Is 9:6, Dn 9).
- Hilo de la sangre y la remisión en todo el video (Lv 17:11, Heb 9:22, Mt 26:28, Heb 9:12, 1 Jn 1:7).

## Contenido
- Errores del video de referencia: **corregir u omitir** (nada de Os 6:2 para el tercer día, ni "todos los discípulos mártires",
  ni la comparación con la tumba de Buda).
- Cierre (parte 2): **invitación clara a la fe** (Ef 2:8-9, Ro 10:9-10) **y oración guiada**.
- Nada obligatorio extra.

## Ilustraciones
- Jesús: figura sin rostro, como en los Shorts.
- Sangre: reverente y simbólica (gotas rojas, clavos, corona de espinas, sin heridas abiertas).
- Ilustraciones de la sangre pedidas: la copa de la Última Cena, Getsemaní y la corona de espinas, la puerta de Egipto que se
  transforma en la cruz, y la tela roja que se vuelve blanca (Is 1:18).

## Voz
- Narrador: Salvatore (t3eeeqhBjrUqcrPvDqUn) al 94 %.
- Emoción según el contexto: "dale vida, dale suspenso, dale emoción, atrapalos" (etiquetas de emoción de eleven_v4).
- Palabras de Dios: más fuerza y eco leve.
- Palabras de Jesús: "con un tono de sufrimiento y gozo". Voz elegida por Claude: Damián (BPwS5yO6aXvwg8auqNwS).
- Otros personajes con **voces distintas**, elegidas por Claude entre las de la cuenta. Muestra: Caín = Japa (ifgQptCyquMG1K4fdoT3);
  multitud = Sam Adam, JC, Horacio, César y Jorge mezclados.
- Muestra previa de 40–60 s antes de generar todo (hecha el 26 nov: 61,6 s, 946 créditos).
- Las voces de los Shorts 1 (jardín) y 2 (Isaac) se **reutilizan** en el largo.

## Créditos, fecha y entrega
- Créditos: la parte 1 con lo que queda hasta el 30 nov; la parte 2 con el mes nuevo.
- Publicación: cuando esté lista (sin fecha fija). Karin sube los videos a mano.
- Entrega: por el chat y en Google Drive.
- Miniatura: dos opciones para elegir.
- Después del largo: un Short por profecía, con gancho, cierre y enlace al largo.
- Título: "Estaba escrito: las profecías que anunciaron a Jesús (Parte 1)".

## Herramientas nuevas
- `scripts/generar_dialogo.py`: varias voces por línea, etiquetas de emoción, eco para Dios, multitud mezclada, caché por línea
  (re-correr no vuelve a pagar).

## Parte 1: producción (27 nov 2026)
- Guion: `fuentes/largo-01-estaba-escrito/parte1_lineas.json` (57 líneas, 15:38). Voz en `insumos-voz/largo-01-parte1/`.
- Animación: motor nuevo `plantillas/grabado/` (horizontal 1920x1080, ilustraciones IA en estilo grabado con cámara,
  transición de tinta, rayos, vela, niebla, brasas, temblores, títulos de capítulo y referencias en pantalla).
  38 ilustraciones (190 créditos c/u), 125 planos, 12 capítulos. Planos: `construir_escenas_parte1.py`.
- Música por capítulos: `plantillas/grabado/musica_largo.py` (pasa de menor a mayor en cada capítulo, trueno en cada temblor).
- Armado final: `scripts/armar_largo.sh` (une partes, música y voz con la misma mezcla que los Shorts).
- Miniaturas: `fuentes/largo-01-estaba-escrito/miniaturas/` (A: la puerta con sangre; B: el cuchillo de Abraham).
- Título, descripción con capítulos, hashtags y comentario fijado: `parte1/publicacion.txt`.
- Ilustraciones descartadas: hojas de higuera (mostraba un desnudo de espaldas). Corregida: la copa (tenía una cúpula anacrónica).
- Créditos: quedan unos 4.700 hasta el 30 nov. La parte 2 va con el mes nuevo.

## Parte 2 (pendiente, desde el 30 nov)
- Salmo 22 y los profetas (Is 7:14, Is 9:6, Is 53, Mi 5:2, Zac 9:9, Zac 11:12-13, Zac 12:10, Dn 9), la cruz, la tumba vacía.
- Ilustraciones de la sangre que faltan: Getsemaní con la corona y la tela roja que se vuelve blanca (Is 1:18).
  Ya están en la Parte 1: la copa (10:54) y la puerta que se vuelve cruz (9:20).
- 2 o 3 momentos con video IA (el velo que se rasga, la piedra que se mueve, la resurrección).
- Cierre: invitación a la fe (Ef 2:8-9, Ro 10:9-10) y oración guiada.

## Entrega de la Parte 1 (27 nov 2026)
- Video entregado por el chat: 15:39, 1080p, 345 MiB. Drive tiene las miniaturas y el documento con los textos (el video no entra: límite de 10 MB desde acá).
- "La sangre de Abel pedía justicia": Karin preguntó si es bíblico. Se deja igual (Gn 4:10-11, Mt 23:35, Ap 6:10, Heb 12:24);
  la explicación quedó como pregunta 4 en `parte1/publicacion.txt`.
- Miniatura: Karin va a **probar las dos** con "Probar y comparar" de YouTube Studio (A: la puerta; B: el cuchillo).
- Siguiente paso: **esperar** a que Karin vea el video completo y diga si hay que cambiar algo. Después: Shorts del largo y Parte 2 (créditos del 30 nov).

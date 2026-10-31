# youtube/<id>.json
Datos para subir el video a YouTube automáticamente vía Make (plan gratis).
El flujo "Mezclar voz y publicar" los envía al webhook (secreto MAKE_WEBHOOK_URL) cuando termina la mezcla.
Campos: channel (tech|bases), title (≤70), description, tags[], privacy ("private" + publish_at = programado), publish_at (ISO con -03:00), made_for_kids.
Reenviar a mano: Actions → "Reenviar video a Make (YouTube)" → id del trabajo.

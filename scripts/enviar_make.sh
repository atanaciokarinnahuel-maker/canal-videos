#!/bin/bash
# Uso: scripts/enviar_make.sh <id>
# Si existe youtube/<id>.json y el secreto MAKE_WEBHOOK_URL, envía a Make el video para subirlo a YouTube.
id="$1"; f="youtube/$id.json"
[ -f "$f" ] || { echo "youtube=sin_bloque"; exit 0; }
[ -n "$MAKE_WEBHOOK_URL" ] || { echo "make_webhook=sin_secreto"; exit 0; }
url="https://github.com/${GITHUB_REPOSITORY}/releases/download/$id/final.mp4"
jq --arg id "$id" --arg url "$url" '. + {id:$id, video_url:$url, tags_csv:((.tags // [])|join(","))}' "$f" > /tmp/payload.json
code=$(curl -sS -o /tmp/resp.txt -w "%{http_code}" -X POST -H 'Content-Type: application/json' -d @/tmp/payload.json "$MAKE_WEBHOOK_URL" || echo 000)
if [ "$code" = "200" ]; then echo "make_webhook=ok"; else echo "make_webhook=error_$code"; fi

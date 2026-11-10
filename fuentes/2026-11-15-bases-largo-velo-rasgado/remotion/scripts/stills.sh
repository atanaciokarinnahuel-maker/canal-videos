#!/bin/bash
# uso: scripts/stills.sh 90 315 435 ...   -> out/stills/sheet.jpg
cd "$(dirname "$0")/.." && rm -f out/stills/f*.jpg
for f in "$@"; do npx remotion still src/index.ts VeloRasgado out/stills/f$(printf %04d $f).jpg --frame=$f --log=error --scale=0.5 2>&1 | grep -iE "error" ; done
ffmpeg -y -loglevel error -pattern_type glob -i 'out/stills/f*.jpg' -vf "tile=5x2:padding=6" out/stills/sheet.jpg

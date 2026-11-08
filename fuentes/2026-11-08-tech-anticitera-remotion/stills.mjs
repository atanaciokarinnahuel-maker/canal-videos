import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
const times = process.argv[2].split(',').map(Number);
const out = process.argv[3] || 'out/stills';
import fs from 'fs'; fs.mkdirSync(out, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const comp = await selectComposition({serveUrl, id: 'Anticitera', browserExecutable: '/usr/bin/google-chrome'});
for (const t of times) {
  const frame = Math.round(t * 30);
  await renderStill({composition: comp, serveUrl, frame, output: `${out}/s_${String(t).padStart(5, '0')}.jpg`, imageFormat: 'jpeg', jpegQuality: 85, browserExecutable: '/usr/bin/google-chrome'});
  console.log('ok', t);
}

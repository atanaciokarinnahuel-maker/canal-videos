// Renderiza video.html cuadro por cuadro.
//   node render.js <H|V> frames 1,5.5,20      -> capturas sueltas en frames_<fmt>/
//   node render.js <H|V> full <desde> <hasta> -> part_<fmt>_<desde>.mp4 (cuadros a 30 fps)
const {chromium} = require('/opt/node-tools/node_modules/playwright');
const {spawn} = require('child_process'); const fs = require('fs'); const path = require('path');
const HERE = __dirname, [fmt, mode, a1, a2] = process.argv.slice(2);
const W = fmt === 'H' ? 1920 : 1080, H = fmt === 'H' ? 1080 : 1920;
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({viewport: {width: W, height: H}});
  pg.on('pageerror', e => console.log('PAGEERROR', e.message));
  pg.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await pg.goto('file://' + path.join(HERE, 'video.html'));
  await pg.evaluate(() => document.fonts.ready);
  const info = await pg.evaluate(f => init({format: f}), fmt);
  fs.writeFileSync(path.join(HERE, 'info.json'), JSON.stringify(info));
  if (mode === 'frames') {
    const dir = path.join(process.cwd(), 'frames_' + fmt); fs.mkdirSync(dir, {recursive: true});
    for (const t of a1.split(',').map(Number)) {
      await pg.evaluate(t => render(t), t);
      await pg.screenshot({path: path.join(dir, `f_${t.toFixed(2).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 85});
    }
  } else {
    const a = +a1, z = Math.min(+a2, Math.round(info.DUR * 30));
    const out = `part_${fmt}_${String(a).padStart(5, '0')}.mp4`, tmp = 'tmp_' + out;
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', tmp], {stdio: ['pipe', 'inherit', 'inherit']});
    const t0 = Date.now();
    for (let i = a; i < z; i++) {
      await pg.evaluate(t => render(t), i / 30);
      const buf = await pg.screenshot({type: 'jpeg', quality: 93});
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); const code = await new Promise(r => ff.on('close', r));
    if (code === 0) fs.renameSync(tmp, out);
    console.log(out, code, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  await b.close();
})();

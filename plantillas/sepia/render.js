// Renderiza video.html con Playwright (Node). Uso, desde la carpeta del video:
//   node render.js frames 0,2.5,5        -> frames/f_XX.XX.jpg (para revisar)
//   node render.js full 0 900            -> part_00000.mp4 (cuadros 0 a 899, 30 fps)
// Lee words.json (tiempos de la voz) y escenas.json (escenas ancladas a palabras).
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { chromium } = require('playwright');
const HERE = __dirname, mode = process.argv[2];
const data = JSON.parse(fs.readFileSync(path.join(HERE, 'words.json'), 'utf8'));
data.guion = JSON.parse(fs.readFileSync(path.join(HERE, 'escenas.json'), 'utf8'));
data.dur = Math.round((data.voice_dur + 1.3) * 100) / 100;
(async () => {
  const b = await chromium.launch();
  const HZ = data.guion.formato === 'h';
  const pg = await b.newPage({ viewport: HZ ? { width: 1920, height: 1080 } : { width: 1080, height: 1920 } });
  pg.on('pageerror', e => console.log('PAGEERROR', e.message));
  pg.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await pg.goto('file://' + path.join(HERE, 'video.html'));
  const info = await pg.evaluate(d => init(d), data);
  console.log(JSON.stringify(info));
  fs.writeFileSync(path.join(HERE, 'info.json'), JSON.stringify(info));
  if (mode === 'frames') {
    fs.mkdirSync(path.join(HERE, 'frames'), { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) {
      await pg.evaluate(x => render(x), t);
      await pg.screenshot({ path: path.join(HERE, 'frames', `f_${t.toFixed(2).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 85 });
    }
  } else {
    const a = parseInt(process.argv[3]), z = Math.min(parseInt(process.argv[4]), Math.round(data.dur * 30));
    const out = path.join(HERE, `part_${String(a).padStart(5, '0')}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = a; i < z; i++) {
      await pg.evaluate(x => render(x), i / 30);
      const buf = await pg.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();

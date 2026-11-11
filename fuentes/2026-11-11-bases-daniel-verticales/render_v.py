#!/usr/bin/env python3
"""Render de una pieza vertical.  render_v.py <cfg.json> frames 1,5,9 <carpeta>  |  render_v.py <cfg.json> full <salida.mp4>"""
import json, sys, subprocess, asyncio, os, base64
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); cfg=json.load(open(sys.argv[1])); mode=sys.argv[2]; FPS=cfg['fps']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/opt/pw-browsers/chromium'),args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('PAGEERROR',e,flush=True)); pg.on('console',lambda m:print('CONSOLE',m.text,flush=True) if m.type=='error' else None)
        await pg.goto('file://'+os.path.join(HERE,'short.html')); info=await pg.evaluate(f'init({json.dumps(cfg)})'); print(cfg['id'],info,flush=True)
        if mode=='frames':
            os.makedirs(sys.argv[4],exist_ok=True)
            for t in [float(x) for x in sys.argv[3].split(',')]:
                d=await pg.evaluate(f'frame({t},0.85)'); open(os.path.join(sys.argv[4],f"{cfg['id']}_{t:05.1f}.jpg"),'wb').write(base64.b64decode(d))
        else:
            out=sys.argv[3]; n=int(round(cfg['dur']*FPS))
            ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','21','-pix_fmt','yuv420p','-r',str(FPS),out],stdin=subprocess.PIPE)
            for i in range(n): ff.stdin.write(base64.b64decode(await pg.evaluate(f'frame({i/FPS},0.93)')))
            ff.stdin.close(); ff.wait()
        await b.close()
asyncio.run(main())

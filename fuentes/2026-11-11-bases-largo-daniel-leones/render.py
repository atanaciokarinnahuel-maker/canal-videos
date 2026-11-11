#!/usr/bin/env python3
"""Render del documental (Chromium + canvas → ffmpeg).
   render.py frames 12.5,80,300     -> frames/f_XXXX.X.jpg (prueba)
   render.py full A B                -> parts/part_A.mp4 (cuadros A..B a 24 fps)"""
import json, sys, subprocess, asyncio, os, base64
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); FPS=24
CHROME=os.environ.get('CHROME','/opt/pw-browsers/chromium')
mode=sys.argv[1]; data=json.load(open(os.path.join(HERE,'data.json'))); dur=data['dur']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME,args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('pageerror',lambda e:print('PAGEERROR',e,flush=True)); pg.on('console',lambda m:print('CONSOLE',m.text,flush=True) if m.type=='error' else None)
        await pg.goto('file://'+os.path.join(HERE,'video.html'))
        info=await pg.evaluate(f'init({json.dumps(data)})')
        if mode=='info': print(json.dumps(info,ensure_ascii=False))
        elif mode=='frames':
            os.makedirs('frames',exist_ok=True)
            for t in [float(x) for x in sys.argv[2].split(',')]:
                d=await pg.evaluate(f'frame({t},0.86)'); open(f'frames/f_{t:06.1f}.jpg','wb').write(base64.b64decode(d))
        else:
            a=int(sys.argv[2]); z=min(int(sys.argv[3]),int(round(dur*FPS)))
            os.makedirs('parts',exist_ok=True); out=f'parts/part_{a:06d}.mp4'; tmp=f'parts/tmp_{a:06d}.mp4'
            ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
                '-c:v','libx264','-preset','medium','-crf',os.environ.get('CRF','21'),'-pix_fmt','yuv420p','-r',str(FPS),'-g','48','-bf','2',tmp],stdin=subprocess.PIPE)
            for i in range(a,z):
                d=await pg.evaluate(f'frame({i/FPS},0.93)'); ff.stdin.write(base64.b64decode(d))
                if (i-a)%240==0: print(a,i,flush=True)
            ff.stdin.close(); r=ff.wait()
            if r==0: os.rename(tmp,out)
        await b.close()
asyncio.run(main())

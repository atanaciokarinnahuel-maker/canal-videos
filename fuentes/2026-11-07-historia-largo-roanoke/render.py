import json, sys, subprocess, asyncio, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
FPS=24
mode=sys.argv[1]
data=json.load(open(os.path.join(HERE,'data.json'))); dur=data['dur']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--disable-gpu-vsync'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('pageerror',lambda e:print('PAGEERROR',e))
        await pg.goto('file://'+os.path.join(HERE,'video.html'))
        await pg.evaluate('document.fonts.ready.then(()=>1)')
        info=await pg.evaluate(f'init({json.dumps(data)})'); print(info, flush=True)
        await pg.evaluate('render(0.5)'); await pg.wait_for_timeout(800)
        if mode=='frames':
            os.makedirs('frames',exist_ok=True)
            for t in [float(x) for x in sys.argv[2].split(',')]:
                await pg.evaluate(f'render({t})'); await pg.wait_for_timeout(60)
                await pg.screenshot(path=f'frames/f_{t:06.1f}.jpg',type='jpeg',quality=85)
        else:
            a=int(sys.argv[2]); z=min(int(sys.argv[3]),int(round(dur*FPS)))
            out=f'parts/part_{a:06d}.mp4'; tmp=f'parts/tmp_{a:06d}.mp4'; os.makedirs('parts',exist_ok=True)
            ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
                '-c:v','libx264','-preset','veryfast','-crf','25','-pix_fmt','yuv420p','-r',str(FPS),'-g','96',tmp],stdin=subprocess.PIPE)
            for i in range(a,z):
                await pg.evaluate(f'render({i/FPS})')
                ff.stdin.write(await pg.screenshot(type='jpeg',quality=90))
                if (i-a)%480==0: print(a,i,flush=True)
            ff.stdin.close(); r=ff.wait()
            if r==0: os.rename(tmp,out)
        await b.close()
asyncio.run(main())

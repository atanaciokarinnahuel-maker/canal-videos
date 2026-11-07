import json, sys, subprocess, asyncio, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
mode = sys.argv[1]
data = json.load(open('words.json'))
dur = round(data['voice_dur'] + 1.3, 2); data['dur'] = dur
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror', lambda e: print('PAGEERROR', e))
        pg.on('console', lambda m: print('CONSOLE', m.text) if m.type=='error' else None)
        await pg.goto('file://'+os.path.join(HERE,'video.html'))
        await pg.evaluate('document.fonts.ready')
        info = await pg.evaluate(f'init({json.dumps(data)})'); print(json.dumps(info), 'dur', dur)
        if mode == 'frames':
            os.makedirs('frames',exist_ok=True)
            for t in [float(x) for x in sys.argv[2].split(',')]:
                await pg.evaluate(f'render({t})')
                await pg.screenshot(path=f'frames/f_{t:05.2f}.jpg', type='jpeg', quality=85)
        else:
            a = int(sys.argv[2]); z = min(int(sys.argv[3]), int(round(dur*30)))
            out = f'part_{a:05d}.mp4'; tmp=f'tmp_{a:05d}.mp4'
            ff = subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-',
                '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30',tmp], stdin=subprocess.PIPE)
            for i in range(a,z):
                await pg.evaluate(f'render({i/30})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close(); r=ff.wait()
            if r==0: os.rename(tmp,out)
        await b.close()
asyncio.run(main())

import json, sys, subprocess, asyncio, os
from playwright.async_api import async_playwright
mode = sys.argv[1]
data = json.load(open('words.json'))
dur = round(data['voice_dur'] + 1.3, 2); data['dur'] = dur
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror', lambda e: print('PAGEERROR', e))
        pg.on('console', lambda m: print('CONSOLE', m.text) if m.type=='error' else None)
        await pg.goto('file://'+os.path.abspath('video.html')+'')
        info = await pg.evaluate(f'init({json.dumps(data)})')
        print(json.dumps(info))
        if mode == 'frames':
            for t in [float(x) for x in sys.argv[2].split(',')]:
                await pg.evaluate(f'render({t})')
                await pg.screenshot(path=f'frames/f_{t:05.2f}.jpg', type='jpeg', quality=85)
        else:
            a = int(sys.argv[2]) if len(sys.argv)>2 else 0
            z = int(sys.argv[3]) if len(sys.argv)>3 else int(round(dur*30))
            out = f'part_{a}_{z}.mp4'
            ff = subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-',
                '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30',out], stdin=subprocess.PIPE)
            for i in range(a,z):
                await pg.evaluate(f'render({i/30})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close(); ff.wait()
        await b.close()
asyncio.run(main())

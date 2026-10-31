import json, sys, subprocess, asyncio
from playwright.async_api import async_playwright
mode = sys.argv[1]  # frames | full
data = json.load(open('words.json'))
dur = round(data['voice_dur'] + 1.3, 2)
data['dur'] = dur
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file:///home/claude/work/video.html')
        info = await pg.evaluate(f'init({json.dumps(data)})')
        print(json.dumps(info))
        if mode == 'frames':
            ts = [float(x) for x in sys.argv[2].split(',')]
            for t in ts:
                await pg.evaluate(f'render({t})')
                await pg.screenshot(path=f'frames/f_{t:05.2f}.jpg', type='jpeg', quality=85)
        else:
            n = int(round(dur*30))
            ff = subprocess.Popen(['ffmpeg','-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-',
                '-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-r','30','video_mudo.tmp.mp4'], stdin=subprocess.PIPE)
            for i in range(n):
                await pg.evaluate(f'render({i/30})')
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
                if i % 150 == 0: print(i, n, flush=True)
            ff.stdin.close(); ff.wait()
            assert ff.returncode == 0
            import os; os.rename('video_mudo.tmp.mp4','video_mudo.mp4')
        await b.close()
asyncio.run(main())

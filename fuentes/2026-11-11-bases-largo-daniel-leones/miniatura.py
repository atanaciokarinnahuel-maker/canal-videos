import asyncio, os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('CHROME','/opt/pw-browsers/chromium'),args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1280,'height':720}); await pg.goto('file://'+os.path.join(HERE,'miniatura.html'))
        await pg.evaluate('document.fonts.ready.then(()=>1)'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(HERE,'miniatura.jpg'),type='jpeg',quality=92,clip={'x':0,'y':0,'width':1280,'height':720}); await b.close()
asyncio.run(main())

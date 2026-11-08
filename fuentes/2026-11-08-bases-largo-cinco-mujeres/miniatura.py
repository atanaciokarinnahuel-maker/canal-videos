import json,asyncio,os
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
JS='''()=>{const L=1.5;let s=sky('skyIndigo')+stars(L,90,4)+lightOn(1380,560,300,L)+mtn(980,120,'#4a3a7a',2,0);
['lea','abigail','debora','ana','rizpa'].forEach((w,i)=>s+=H(w,1010+i*190,1010-(i==2?30:0),1.15,{head:[-6,4,-10,8,-4][i]}));
s+=`<g transform="translate(1660,250)">${medal(0,0,110,'?','#5b4a8a',1)}</g>`;
s+=`<g transform="translate(540,330) rotate(-4)">${TX(0,0,'5 MUJERES',165,GOLD,INK,22)}</g>`;
s+=`<g transform="translate(540,490) rotate(-4)">${TX(0,0,'DE LA BIBLIA',110,'#fff',INK,16)}</g>`;
s+=`<g transform="translate(540,670) rotate(-4)"><rect x="-440" y="-95" width="880" height="140" rx="30" fill="${CORAL}" stroke="${INK}" stroke-width="12"/>${TX(0,10,'QUE CASI NADIE CONOCE',64,'#fff',INK,10)}</g>`;
document.getElementById('LB').innerHTML=`<svg width="1920" height="1080" viewBox="0 0 1920 1080">${s}</svg>`;document.getElementById('LB').style.transform='none';
['subs','prog','chip','flash','LA'].forEach(i=>document.getElementById(i).style.display='none');document.getElementById('cv').getContext('2d').clearRect(0,0,1920,1080)}'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('pageerror',lambda e:print('PAGEERROR',e))
        await pg.goto('file://'+os.path.join(HERE,'video.html'))
        await pg.evaluate(f'init({json.dumps(json.load(open("data.json")))})')
        await pg.evaluate(JS); await pg.screenshot(path='miniatura_full.png'); await b.close()
asyncio.run(main())

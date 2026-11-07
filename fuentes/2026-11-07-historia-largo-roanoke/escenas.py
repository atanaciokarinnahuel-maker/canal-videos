"""Genera data.json (escenas + subtítulos + capítulos) para video.html.
Tiempos en segundos de la VOZ FINAL (ya cortada) — ver timeline.json."""
import json, math, random
random.seed(5)
T = json.load(open('timeline.json'))
SUBS = json.load(open('subs.json'))
VOZ = 436.15
DUR = round(VOZ + 2.0, 2)
INK = '#2b1d12'; SEP = '#6b4a2b'; RED = '#8e2a1e'; BLUE = '#3d5466'; PAP = '#eadcc0'

# ---------- utilidades ----------
def A(tin, mode='fade', dur=None, out=None, extra=''):
    s = f' data-in="{tin}" data-mode="{mode}"'
    if dur is not None: s += f' data-dur="{dur}"'
    if out is not None: s += f' data-out="{out}"'
    return s + extra

def tag(text, x, y, tin, rot=0, dark=False, size=34, out=None, mode='fade'):
    return f'<div class="tag{" dark" if dark else ""}" style="left:{x}px;top:{y}px;font-size:{size}px;transform:rotate({rot}deg)"{A(tin, mode, out=out)}>{text}</div>'

def stamp(text, x, y, tin, rot=-8, size=44, color=RED, out=None):
    return f'<div class="stamp" style="left:{x}px;top:{y}px;font-size:{size}px;color:{color};border-color:{color};transform:rotate({rot}deg)"{A(tin, "pop", out=out)}>{text}</div>'

def card(kind, title, body, x, y, w, tin, rot=0, out=None, label=None):
    cls = {'HECHO': 'hecho', 'HIPÓTESIS': 'hip', 'NO DEMOSTRADO': 'nodem'}.get(kind, '')
    lab = label or kind
    return (f'<div class="card {cls}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)"{A(tin, "slide", out=out, extra=" data-dx=\"60\"")}>'
            f'<div class="k">{lab}</div><div class="h">{title}</div>' + (f'<div class="b">{body}</div>' if body else '') + '</div>')

def typed(text, x, y, tin, size=40, color=INK, font='TW', anchor='left', w=None, dur=None):
    al = {'left': 'left', 'center': 'center'}[anchor]
    ww = f'width:{w}px;' if w else ''
    return f'<div class="abs" style="left:{x}px;top:{y}px;{ww}text-align:{al};font-family:{font};font-size:{size}px;color:{color};white-space:pre-line;line-height:1.25"{A(tin, "type", dur=dur)}>{text}</div>'

def photo(src, x, y, w, h, kb, caption, rot=0, tin=None):
    a = A(tin, 'fade') if tin is not None else ''
    return (f'<div class="photo" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)"{a}>'
            f'<div class="win"><img src="assets/{src}" data-kb="{kb}"></div><div class="cap">{caption}</div>'
            f'<div class="tape" style="left:{w/2-75}px;top:-22px;transform:rotate({-rot*1.5+2}deg)"></div></div>')

def cam(inner, z0=1.0, z1=1.07, x0=0, x1=0, y0=0, y1=0):
    return f'<div class="cam" data-z0="{z0}" data-z1="{z1}" data-x0="{x0}" data-x1="{x1}" data-y0="{y0}" data-y1="{y1}">{inner}</div>'

def svg(inner, w=1920, h=1080):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg>'

def silhouette(cx, cy, s=1.0, col=SEP):
    # silueta genérica de persona de época (sin rasgos)
    return (f'<g transform="translate({cx},{cy}) scale({s})" fill="{col}">'
            f'<ellipse cx="0" cy="-118" rx="34" ry="40"/><path d="M-30,-150 Q0,-178 30,-150 L44,-136 L-44,-136 Z"/>'
            f'<path d="M-78,40 Q-74,-50 -36,-70 L36,-70 Q74,-50 78,40 Z"/><rect x="-14" y="-82" width="28" height="18"/></g>')

def dossier(name, role, lines, x, y, tin, rot=-1.5, w=1100, sil=True, out=None):
    ls = ''.join(f'<div class="b" style="font-size:40px;margin-top:10px">· {l}</div>' for l in lines)
    s = (f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);padding-left:{330 if sil else 40}px;min-height:430px"{A(tin, "slide", out=out, extra=" data-dx=\"-70\"")}>'
         + (f'<svg width="270" height="350" style="left:34px;top:44px" viewBox="-100 -190 200 250"><rect x="-96" y="-186" width="192" height="242" fill="#d8c7a3" stroke="#a88f66" stroke-width="3"/>{silhouette(0, 30, 0.95, "#7d6243")}</svg>' if sil else '')
         + f'<div class="k" style="color:{SEP}">FICHA</div><div class="h">{name}</div><div class="b" style="font-style:italic">{role}</div>{ls}</div>')
    return s

def bigdate(text, x, y, tin, size=120, color=INK):
    return f'<div class="abs" style="left:{x}px;top:{y}px;font-family:TW;font-size:{size}px;color:{color};letter-spacing:8px"{A(tin, "type", dur=len(text) * 0.07)}>{text}</div>'

# ---------- ilustraciones SVG ----------
def sea(night=True, ship_x=900, ship_y=640, island=True, fog=True, storm=False, moon=True):
    sky = '#1d2630' if night else '#b9a989'
    sky2 = '#4b4a42' if night else '#e3d4b2'
    s = f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky}"/><stop offset="1" stop-color="{sky2}"/></linearGradient></defs>'
    s += '<rect x="-200" y="-100" width="2400" height="1300" fill="url(#sk)"/>'
    if moon and not storm:
        s += '<circle cx="1480" cy="230" r="70" fill="#efe1bd" opacity=".85"/><circle cx="1480" cy="230" r="150" fill="#efe1bd" opacity=".08"/>'
    out = svg(s)
    if island:
        out += f'<div class="abs" style="inset:0" data-px="4">{svg("<path d=\"M-100,600 Q200,540 420,575 Q600,520 820,590 L860,640 L-100,640 Z\" fill=\"#2a2a26\" opacity=\".8\"/>")}</div>'
    if fog:
        out += f'<div class="abs" style="inset:0" data-px="9">{svg("<ellipse cx=\"600\" cy=\"600\" rx=\"1300\" ry=\"60\" fill=\"#cfc4ab\" opacity=\".18\"/><ellipse cx=\"2400\" cy=\"620\" rx=\"1300\" ry=\"50\" fill=\"#cfc4ab\" opacity=\".16\"/>", 4000)}</div>'
    # olas en 3 capas con parallax
    for i, (yy, col, sp, amp) in enumerate([(640, '#2e3a42', 12, 10), (720, '#25313a', 26, 16), (840, '#1b252c', 46, 24)]):
        if not night: col = ['#7c7563', '#6a6352', '#585141'][i]
        d = f'M-100,{yy} ' + ' '.join(f'Q{x+60},{yy-amp} {x+120},{yy} T{x+240},{yy}' for x in range(-100, 4200, 240)) + f' L4200,1200 L-100,1200 Z'
        out += f'<div class="abs" style="inset:0" data-px="{sp}">{svg(f"<path d=\"{d}\" fill=\"{col}\"/>", 4300)}</div>'
        if i == 0 and ship_x is not None:
            out += f'<div class="abs" style="left:{ship_x - 160}px;top:{ship_y - 300}px;width:320px;height:330px;transform-origin:50% 90%" data-bob="{4 if storm else 2},{1.6 if storm else 0.8},0,{8 if storm else 3}">{ship()}</div>'
    if storm:
        out += f'<div class="abs" style="inset:0;background:#e9edf0;mix-blend-mode:screen" data-flash="__FLASH__"></div>'
        rain = ''.join(f'<line x1="{x}" y1="{y}" x2="{x-40}" y2="{y+90}" stroke="#a9b3b8" stroke-width="2" opacity=".35"/>' for x, y in [(random.randint(0, 2400), random.randint(-100, 1080)) for _ in range(140)])
        out += f'<div class="abs" style="inset:0" data-px="-60">{svg(rain, 2600)}</div>'
    return out

def ship(col='#1c1712'):
    return svg(f'<g fill="{col}"><path d="M30,250 L290,250 L260,300 L60,300 Z"/><rect x="155" y="40" width="6" height="215"/><rect x="85" y="80" width="5" height="175"/><rect x="225" y="95" width="5" height="160"/>'
               f'<path d="M100,60 Q160,50 215,60 L210,180 Q158,170 105,180 Z" opacity=".92"/><path d="M45,100 Q88,92 128,100 L125,200 Q85,192 50,200 Z" opacity=".9"/><path d="M200,115 Q240,108 275,115 L272,205 Q238,198 205,205 Z" opacity=".9"/>'
               f'<path d="M158,30 L190,38 L158,46 Z"/><path d="M260,250 L310,215 L312,222 L272,252Z"/></g>', 320, 330)

def palisade(fogcol='#d6caa9', dusk=True):
    bg = '#cdbb94' if dusk else '#d9caa7'
    s = svg(f'<defs><linearGradient id="pg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f8065"/><stop offset=".55" stop-color="{bg}"/><stop offset="1" stop-color="#9c8762"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#pg)"/>')
    # árboles lejanos
    trees = ''.join(f'<path d="M{x},{620} L{x+18},{620 - h} L{x+36},{620} Z" fill="#5b5443" opacity=".55"/>' for x, h in [(i * 46 - 60, 90 + (i * 37 % 70)) for i in range(60)])
    s += f'<div class="abs" style="inset:0" data-px="3">{svg(trees + "<rect x=\"-100\" y=\"615\" width=\"3000\" height=\"600\" fill=\"#8a7a5c\"/>", 2900)}</div>'
    s += f'<div class="abs" style="inset:0" data-px="8">{svg("<ellipse cx=\"900\" cy=\"640\" rx=\"1500\" ry=\"70\" fill=\"" + fogcol + "\" opacity=\".45\"/>", 3000)}</div>'
    # empalizada en perspectiva
    stakes = ''
    for i in range(46):
        x = 120 + i * 40; h = 300 - abs(i - 23) * 3
        stakes += f'<path d="M{x},{780} L{x},{780 - h} L{x+17},{780 - h - 26} L{x+34},{780 - h} L{x+34},{780} Z" fill="{"#4a3a28" if i % 2 else "#55432e"}"/>'
    s += f'<div class="abs" style="inset:0" data-px="14">{svg(stakes + "<rect x=\"100\" y=\"770\" width=\"1900\" height=\"20\" fill=\"#3a2c1e\"/><rect x=\"-200\" y=\"780\" width=\"2600\" height=\"400\" fill=\"#6d5c41\"/>", 2200)}</div>'
    s += f'<div class="abs" style="inset:0" data-px="30">{svg("<ellipse cx=\"500\" cy=\"860\" rx=\"900\" ry=\"80\" fill=\"" + fogcol + "\" opacity=\".55\"/><ellipse cx=\"2300\" cy=\"900\" rx=\"900\" ry=\"70\" fill=\"" + fogcol + "\" opacity=\".5\"/>", 3400)}</div>'
    return s

def carving(word, x0, y0, tin, step, size=150, kind='tree'):
    # tronco o poste con letras talladas que aparecen una a una
    if kind == 'tree':
        bark = ''.join(f'<path d="M{620 + i * 36},-20 Q{640 + i * 36 + (i % 3) * 8},540 {610 + i * 36},1100" stroke="#3b2c1d" stroke-width="{3 + (i % 4)}" fill="none" opacity=".55"/>' for i in range(20))
        base = svg(f'<rect width="1920" height="1080" fill="#2a2119"/><path d="M560,-20 Q600,540 540,1100 L1380,1100 Q1320,540 1360,-20 Z" fill="#6e5639"/>{bark}'
                   f'<ellipse cx="960" cy="520" rx="330" ry="210" fill="#b39468" opacity=".9"/><ellipse cx="960" cy="520" rx="330" ry="210" fill="none" stroke="#4d3a26" stroke-width="10" opacity=".6"/>')
    else:
        planks = ''.join(f'<rect x="{-20 + i * 196}" y="0" width="190" height="1080" fill="{"#7a6143" if i % 2 else "#86694a"}"/><path d="M{-20 + i * 196 + 60},0 Q{-20 + i * 196 + 90},540 {-20 + i * 196 + 50},1080" stroke="#5b4630" stroke-width="3" fill="none" opacity=".6"/>' for i in range(11))
        base = svg(f'<rect width="1920" height="1080" fill="#3a2c1e"/>{planks}<rect x="0" y="390" width="1920" height="300" fill="#a68a63"/><path d="M0,390 L1920,395 M0,690 L1920,686" stroke="#4a3826" stroke-width="8"/>'
                   + ''.join(f'<path d="M{x},{410 + (x * 7) % 260} q120,{(x % 5) - 2} 260,{(x % 7) - 3}" stroke="#7d6446" stroke-width="3" fill="none" opacity=".7"/>' for x in range(0, 1920, 150)))
    letters = ''
    n = len(word); cw = size * 0.78; start = 960 - n * cw / 2
    for i, ch in enumerate(word):
        letters += (f'<div class="abs" style="left:{start + i * cw}px;top:{y0}px;width:{cw}px;text-align:center;font-family:Fell;font-size:{size}px;color:#2b1a0d;'
                    f'text-shadow:2px 2px 0 rgba(255,235,200,.35),-2px -2px 2px rgba(0,0,0,.6)"{A(round(tin + i * step, 2), "pop", dur=0.22)}>{ch}</div>')
    return base + letters

def mapa_atlantico(tin_route, tin_eng, tin_am, extra='', back=False):
    land = '#dcc79c'; edge = '#6b4a2b'
    s = (f'<rect width="1920" height="1080" fill="#b4b8a2"/>'
         + ''.join(f'<path d="M0,{y} Q480,{y - 12} 960,{y} T1920,{y}" stroke="#9da38b" stroke-width="2" fill="none" opacity=".7"/>' for y in range(120, 1080, 70))
         # América del Norte
         + f'<path d="M-40,80 L420,90 Q520,180 470,300 Q440,360 520,420 Q560,470 500,540 Q430,600 470,690 Q520,760 420,860 Q300,940 180,1100 L-40,1100 Z" fill="{land}" stroke="{edge}" stroke-width="4"/>'
         # Islas británicas
         + f'<path d="M1420,170 Q1470,140 1490,200 Q1520,260 1500,330 Q1470,380 1430,350 Q1400,300 1420,250 Z" fill="{land}" stroke="{edge}" stroke-width="4"/><path d="M1350,250 Q1380,230 1395,265 Q1395,300 1365,305 Q1340,290 1350,250Z" fill="{land}" stroke="{edge}" stroke-width="4"/>'
         # Europa / España
         + f'<path d="M1560,330 Q1700,300 1960,320 L1960,760 Q1760,780 1680,700 Q1600,690 1560,620 Q1480,600 1500,520 Q1520,460 1600,450 Q1580,400 1560,330 Z" fill="{land}" stroke="{edge}" stroke-width="4"/>'
         + f'<path d="M1500,860 Q1640,830 1960,860 L1960,1100 L1480,1100 Z" fill="{land}" stroke="{edge}" stroke-width="4"/>'
         # rosa de los vientos
         + f'<g transform="translate(980,860)" opacity=".7"><circle r="70" fill="none" stroke="{SEP}" stroke-width="3"/><path d="M0,-95 L14,0 L0,95 L-14,0Z" fill="{SEP}"/><path d="M-95,0 L0,14 L95,0 L0,-14Z" fill="{SEP}" opacity=".6"/><text y="-104" text-anchor="middle" font-family="TW" font-size="30" fill="{SEP}">N</text></g>'
         + (f'<path d="M505,500 C800,330 1150,180 1440,300" stroke="{RED}" stroke-width="6" fill="none"{A(tin_route, "draw", dur=3.0)}/>' if back else '')
         + f'<path d="M1440,300 C1150,180 800,330 505,500" stroke="{RED}" stroke-width="6" fill="none"{A(tin_route if not back else 99999, "draw", dur=3.0)}/>'
         + extra)
    s = svg(s)
    s += f'<div class="abs fell" style="left:1300px;top:120px;font-size:44px"{A(tin_eng)}>Inglaterra</div>'
    s += f'<div class="abs fell" style="left:90px;top:300px;font-size:52px;line-height:1"{A(tin_am)}>América<br>del Norte</div>'
    s += f'<div class="abs fell" style="left:820px;top:560px;font-size:46px;font-style:italic;color:{BLUE};letter-spacing:6px">Océano Atlántico</div>'
    return s

def mapa_costa(extra_svg='', extra_html=''):
    land = '#dcc79c'; edge = '#6b4a2b'; water = '#b4b8a2'
    s = (f'<rect width="1920" height="1080" fill="{water}"/>'
         + ''.join(f'<path d="M1100,{y} Q1500,{y - 10} 1920,{y}" stroke="#9da38b" stroke-width="2" fill="none" opacity=".7"/>' for y in range(100, 1080, 60))
         # tierra firme (izquierda) con estrechos
         + f'<path d="M-40,-40 L980,-40 Q900,80 940,170 Q1000,250 900,300 Q820,330 860,400 Q930,470 830,560 Q760,600 800,680 Q860,760 760,850 Q700,920 720,1120 L-40,1120 Z" fill="{land}" stroke="{edge}" stroke-width="4"/>'
         # Albemarle Sound (entrante de agua)
         + f'<path d="M380,300 Q600,270 900,300 Q860,340 860,380 Q600,370 400,360 Q330,330 380,300 Z" fill="{water}" stroke="{edge}" stroke-width="3"/>'
         # Bancos exteriores (islas barrera)
         + f'<path d="M1060,-40 Q1080,200 1120,330 Q1170,470 1230,600 Q1300,720 1420,800 Q1500,850 1560,900 L1552,912 Q1480,866 1400,815 Q1280,735 1212,610 Q1150,480 1100,340 Q1062,210 1046,-40 Z" fill="{land}" stroke="{edge}" stroke-width="3"/>'
         # isla de Roanoke
         + f'<path d="M985,410 Q1010,395 1022,430 Q1030,480 1012,505 Q992,515 982,480 Q975,440 985,410Z" fill="#b89f71" stroke="{edge}" stroke-width="3"/>'
         + extra_svg)
    s = svg(s)
    s += f'<div class="abs fell" style="left:250px;top:620px;font-size:40px;color:{SEP};font-style:italic;line-height:1">Tierra firme</div>'
    s += f'<div class="abs fell" style="left:1500px;top:330px;font-size:44px;font-style:italic;color:{BLUE};letter-spacing:5px">Océano Atlántico</div>'
    s += f'<div class="abs tw" style="left:1560px;top:1000px;font-size:20px;color:{SEP}">mapa ilustrativo</div>'
    return s + extra_html

# puntos del mapa de costa
ROA = (1000, 460); CRO = (1395, 800); DAS = (930, 470); SITIOX = (500, 250); CHES = (980, 40)

def pin(x, y, label, tin, dx=26, dy=-16, size=36, col=RED):
    return (f'<div class="abs" style="left:{x - 14}px;top:{y - 14}px;width:28px;height:28px;border-radius:50%;background:{col};border:4px solid #f1e6cd;box-shadow:0 2px 6px rgba(0,0,0,.4)"{A(tin, "pop")}></div>'
            f'<div class="tag" style="left:{x + dx}px;top:{y + dy - 26}px;font-size:{size}px;padding:4px 14px"{A(tin + 0.2, "fade")}>{label}</div>')

def notebook(lines, x, y, w, tins, title=None, title_t=None):
    rows = ''.join(f'<div style="height:84px;border-bottom:2px solid #b8c4cc;font-family:TW;font-size:38px;padding-top:28px;color:{INK}"{A(t, "type", dur=len(l) * 0.035)}>{l}</div>' for l, t in zip(lines, tins))
    tt = f'<div class="fell" style="font-size:54px;margin-bottom:8px"{A(title_t, "fade")}>{title}</div>' if title else ''
    return f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate(-1deg);border-left:6px solid #c98f7f"{A(tins[0] - 0.8 if title_t is None else title_t - 0.2, "fade")}>{tt}{rows}</div>'

def rings(tin):
    s = ''
    for i in range(26):
        r = 40 + i * 16 + (8 if i in (20, 21, 22) else 0)
        col = RED if i in (20, 21, 22) else '#7a5b3c'
        sw = 2.5 if i in (20, 21, 22) else 5 - (i % 3)
        s += f'<ellipse cx="0" cy="0" rx="{r}" ry="{r * 0.92}" fill="none" stroke="{col}" stroke-width="{sw}"{A(round(tin + i * 0.08, 2), "fade", dur=0.3)}/>'
    return svg(f'<rect width="1920" height="1080" fill="#3a2c1e"/><g transform="translate(700,560)"><ellipse rx="460" ry="430" fill="#c8a777"/>{s}</g>')

def icon_box(x, y, label, tin, sym):
    return (f'<div class="card" style="left:{x}px;top:{y}px;width:420px;height:400px;text-align:center;padding-top:40px"{A(tin, "pop")}>'
            f'<div style="font-size:150px;line-height:1;font-family:Fell;color:{SEP}">{sym}</div><div class="h" style="font-size:48px;margin-top:30px">{label}</div></div>')

# ---------- escenas ----------
S = []
def scene(t0, t1, html):
    S.append(dict(t0=round(t0, 2), t1=round(t1, 2), html=html))

# CAP I — El misterio (0 – 44.5)
scene(0, 9.0, cam(sea(night=True, ship_x=980, ship_y=650) + bigdate('AGOSTO · 1590', 120, 150, 1.6, size=84, color='#efe2c4')
                  + typed('Un hombre vuelve a su colonia…', 124, 270, 3.4, size=40, color='#d8c7a2')
                  + f'<div class="abs tw" style="left:1240px;top:760px;font-size:96px;color:#f2e6cc"{A(6.9, "pop")}>+<span data-count="0,100,6.9,1.2">0</span></div>'
                  + f'<div class="abs tw" style="left:1240px;top:880px;font-size:34px;color:#e2d2ae"{A(7.2)}>personas en la colonia</div>', 1.0, 1.12, 0, -30))
scene(9.0, 16.0, cam(photo('09.jpg', 230, 140, 1460, 810, '1.0,1.22,0,0,-4,-2', 'Ilustración · asentamiento vacío', rot=-1.2)
                     + tag('LAS CASAS: DESMONTADAS', 1080, 760, 11.3, rot=2, dark=True) + tag('UNA EMPALIZADA ALTA', 1150, 860, 13.7, rot=-1.5, dark=True), 1.0, 1.05))
scene(16.0, 20.0, cam(palisade() + stamp('SIN HABITANTES', 260, 200, 16.2, rot=-6) + stamp('SIN SEÑALES DE BATALLA', 900, 300, 17.5, rot=4), 1.0, 1.1, 0, -10))
scene(20.0, 26.0, cam(carving('CRO', 0, 420, 23.95, 0.45, size=190) + tag('1.ª INSCRIPCIÓN · en un árbol', 120, 140, 20.3, rot=-2), 1.18, 1.0))
scene(26.0, 30.5, cam(photo('02.jpg', 300, 130, 1320, 830, '1.0,1.3,0,0,6,4', 'Grabado, 1876 · dominio público', rot=1) , 1.0, 1.04))
scene(30.5, 34.3, cam(carving('CROATOAN', 0, 430, 30.55, 0.11, size=170, kind='post') + tag('2.ª INSCRIPCIÓN · en la empalizada', 120, 140, 30.6, rot=-2), 1.12, 1.0))
scene(34.3, 40.6, cam(svg(f'<rect width="1920" height="1080" fill="#2a2119" opacity=".18"/>')
                       + card('?', '¿Asesinados?', None, 110, 330, 520, 34.5, rot=-3, label='PREGUNTA 1')
                       + card('?', '¿Escaparon?', None, 700, 300, 520, 36.2, rot=1.5, label='PREGUNTA 2')
                       + card('?', '¿Sobrevivieron en otro lugar?', None, 1290, 340, 540, 37.9, rot=-1, label='PREGUNTA 3')
                       + typed('¿Qué le pasó a esta comunidad?', 160, 160, 34.4, size=52, font='Fell'), 1.0, 1.05))
scene(40.6, 44.4, cam(f'<div class="abs" style="inset:0;background:url(assets/05b.jpg) center/cover;opacity:.75"></div>'
                       + f'<div class="abs fell" style="left:0;right:0;top:330px;text-align:center;font-size:118px;color:#f6ecd4;text-shadow:0 4px 18px rgba(0,0,0,.7)"{A(40.8, "fade", dur=1.0)}>La colonia perdida<br>de Roanoke</div>'
                       + stamp('EXPEDIENTE 1587 – 1590', 640, 680, 42.2, rot=-4, size=40, color='#d9b48a'), 1.05, 1.0))

# CAP II — Un proyecto en tierras desconocidas (44.4 – 106.0)
scene(44.4, 49.9, cam(bigdate('1587', 700, 380, 47.1, size=230) + typed('Inglaterra · Isabel I · Nuevo Mundo', 640, 680, 47.8, size=40, color=SEP), 1.0, 1.06))
scene(49.9, 54.1, cam(mapa_atlantico(50.3, 50.0, 51.7), 1.0, 1.08, 30, 0))
scene(54.1, 58.2, cam(dossier('Sir Walter Raleigh', 'respaldó y financió la empresa', ['patente de la reina para colonizar', 'impulsó los viajes de 1584 a 1590'], 410, 250, 54.3) , 1.0, 1.05))
scene(58.2, 65.4, cam(photo('07.jpg', 110, 150, 1180, 640, '1.05,1.3,-3,0,3,-2', 'Ilustración · llegada de 1587', rot=-1.5)
                      + f'<div class="card" style="left:1340px;top:260px;width:470px;text-align:center"{A(58.3, "pop")}><div class="k">COLONOS</div><div class="tw" style="font-size:150px;line-height:1.1">≈<span data-count="0,118,58.4,1.6">0</span></div><div class="b">hombres, mujeres y niños</div></div>'
                      + tag('cruzan el océano', 1390, 680, 60.3, rot=2), 1.0, 1.04))
scene(65.4, 73.0, cam(dossier('John White', 'gobernador de la colonia', ['artista: dibujó pueblos y paisajes', 'cartógrafo de la costa'], 90, 260, 65.6, w=960)
                      + f'<div class="card" style="left:1090px;top:220px;width:660px;height:600px;padding:20px"{A(69.2, "fade")}>' + svg(
                          f'<path d="M60,520 Q120,380 200,400 Q260,300 340,330 Q420,200 520,230 Q580,150 620,90" stroke="{SEP}" stroke-width="5" fill="none"{A(69.4, "draw", dur=2.4)}/>'
                          f'<path d="M120,140 Q200,160 240,120 M380,470 Q450,440 520,480 M90,300 L150,250 L210,300 L150,350 Z" stroke="{SEP}" stroke-width="4" fill="none"{A(70.4, "draw", dur=2.0)}/>'
                          f'<text x="330" y="580" text-anchor="middle" font-family="Fell" font-size="36" font-style="italic" fill="{SEP}"{A(71.0)}>dibujos y mapas</text>', 660, 600) + '</div>', 1.0, 1.05))
scene(73.0, 84.2, cam(mapa_costa(
        f'<path d="M1050,560 Q1080,300 1000,60" stroke="{BLUE}" stroke-width="6" fill="none" stroke-dasharray="18 14"{A(73.4, "draw", dur=2)}/>'
        f'<path d="M1900,700 Q1500,560 1030,470" stroke="{RED}" stroke-width="7" fill="none"{A(77.1, "draw", dur=2.2)}/>',
        tag('↑ destino: bahía de Chesapeake', 1010, 90, 74.0) + pin(*ROA, 'Isla de Roanoke', 78.4, dx=-420, dy=40)
        + typed('actual Carolina del Norte', 140, 900, 81.0, size=42, color=SEP)), 1.0, 1.12, 0, 20))
scene(84.2, 91.2, cam(card('HECHO', 'La guarnición de la expedición anterior', 'Ingleses dejados en Roanoke en 1586', 300, 260, 820, 84.4, rot=-1.5)
                      + stamp('NO LOS ENCONTRARON', 760, 680, 89.4, rot=-7, size=56), 1.0, 1.05))
scene(91.2, 96.6, cam(mapa_costa(f'<path d="M1030,470 Q1080,280 1010,90" stroke="{RED}" stroke-width="7" fill="none"{A(91.5, "draw", dur=1.6)}/>',
        pin(*ROA, 'Roanoke', 91.4, dx=-260, dy=40) + f'<div class="abs tw" style="left:960px;top:150px;font-size:170px;color:{RED};line-height:1"{A(93.8, "pop")}>✕</div>'
        + tag('el capitán se niega a seguir al norte', 1150, 200, 94.0, rot=-2)), 1.1, 1.0))
scene(96.6, 101.0, cam(palisade(dusk=False) + tag('Quedarse y reconstruir', 160, 180, 96.9, rot=-2, dark=True), 1.0, 1.08, 0, 0))
scene(101.0, 106.0, cam(f'<div class="abs" style="inset:0;background:url(assets/05b.jpg) center/cover"></div><div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(20,12,6,.72),rgba(20,12,6,.35) 60%,rgba(20,12,6,0))"></div>'
                        + typed('Una parada…', 180, 330, 101.1, size=76, color='#f4e8cf', font='Fell')
                        + typed('…se convirtió en su hogar.', 520, 470, 101.8, size=76, color='#f4e8cf', font='Fell')
                        + f'<div class="abs tw" style="left:180px;top:920px;font-size:22px;color:#e8dab9">Ilustración (fondo)</div>', 1.0, 1.08))

# CAP III — Una colonia bajo presión (106.0 – 166.7)
scene(106.0, 116.0, cam(typed('Lo que necesitaban:', 160, 140, 108.6, size=48, font='Fell')
                        + icon_box(160, 300, 'Alimentos', 109.4, '❦') + icon_box(750, 300, 'Suministros', 111.3, '⚒') + icon_box(1340, 300, 'Relaciones estables', 112.3, '⚭'), 1.0, 1.04))
scene(116.0, 121.8, cam(dossier('George Howe', 'colono inglés', ['asesinado en 1587, días después de llegar'], 380, 300, 116.2) + stamp('TENSIONES', 1320, 190, 116.4, rot=8), 1.0, 1.05))
scene(121.8, 134.5, cam(mapa_costa(f'<path d="M995,455 Q960,445 940,468" stroke="{RED}" stroke-width="8" fill="none"{A(126.3, "draw", dur=1.2)}/>',
        pin(*ROA, 'Roanoke', 122.0, dx=40, dy=40) + pin(*DAS, 'Dasamonquepeuc', 123.0, dx=-470, dy=-40)), 1.3, 1.2, 200, 60)
        + card('HECHO', 'Atacaron por error', 'Eran Croatoan, aliados de los ingleses, que no habían participado.', 1150, 560, 680, 127.7, rot=1.5))
scene(134.5, 142.6, cam(dossier('Manteo', 'hombre croatoan, aliado de los ingleses', ['conocía el idioma inglés', 'había viajado a Inglaterra', 'ayudó a calmar la situación'], 380, 260, 134.7, w=880)
                        + stamp('INTÉRPRETE', 1300, 130, 137.5, rot=-6, color=BLUE), 1.0, 1.05))
scene(142.6, 154.3, cam(f'<div class="card" style="left:300px;top:150px;width:1320px;height:720px"{A(142.8, "fade")}></div>'
        + typed('18 de agosto de 1587', 360, 200, 143.4, size=44)
        + svg(f'<path d="M960,380 L960,470 M700,470 L1220,470 M700,470 L700,540 M1220,470 L1220,540" stroke="{SEP}" stroke-width="4" fill="none"{A(149.6, "draw", dur=1.2)}/>')
        + f'<div class="abs fell" style="left:760px;top:300px;width:400px;text-align:center;font-size:52px"{A(149.8)}>John White</div>'
        + f'<div class="abs fell" style="left:500px;top:550px;width:400px;text-align:center;font-size:40px;color:{SEP}"{A(150.6)}>Eleanor White</div>'
        + f'<div class="abs fell" style="left:1020px;top:550px;width:400px;text-align:center;font-size:40px;color:{SEP}"{A(150.8)}>Ananias Dare</div>'
        + f'<div class="abs fell" style="left:560px;top:650px;width:800px;text-align:center;font-size:84px;color:{RED}"{A(147.7, "pop")}>Virginia Dare</div>'
        + tag('primera niña inglesa nacida en la expedición', 520, 790, 151.4, rot=-1), 1.0, 1.05))
scene(154.3, 157.6, cam(card('HECHO', 'Otro nacimiento', 'Un hijo de Dyonis y Margery Harvie, días después', 460, 300, 1000, 154.5, rot=-2), 1.0, 1.06))
scene(157.6, 166.7, cam(photo('06.jpg', 170, 140, 1300, 740, '1.0,1.25,0,0,-3,2', 'Ilustración · colonos reunidos', rot=1.2)
        + tag('familias · niños · planes', 1200, 120, 158.0, rot=3)
        + tag('pero: comida escasa', 1250, 760, 161.7, rot=-2, dark=True) + tag('se acerca el invierno', 1290, 850, 163.3, rot=1, dark=True)
        + stamp('NECESITAN AYUDA', 480, 430, 164.6, rot=-8, size=64), 1.0, 1.05))

# CAP IV — La partida de John White (166.7 – 221.6)
scene(166.7, 176.3, cam(mapa_atlantico(170.5, 170.2, 170.2, extra=f'<circle cx="505" cy="500" r="16" fill="{RED}"/>', back=True)
        + tag('John White vuelve a Inglaterra', 1010, 620, 172.0, rot=-2, dark=True) + tag('por personas y provisiones', 1050, 710, 174.0, rot=1), 1.08, 1.0, -30, 0))
scene(176.3, 189.7, cam(notebook(['Si se mudan → tallar el nombre del lugar', 'Si es una emergencia → añadir una cruz ✠'], 260, 260, 1400, [181.8, 186.0], title='El código acordado', title_t=176.6), 1.0, 1.06))
scene(189.7, 196.5, cam(mapa_costa(f'<path d="M985,450 Q780,330 515,262" stroke="{RED}" stroke-width="7" fill="none" stroke-dasharray="20 12"{A(192.2, "draw", dur=2.2)}/>',
        pin(*ROA, 'Roanoke', 189.9, dx=40, dy=40) + tag('≈ 50 millas (80 km) tierra adentro', 330, 190, 194.2, rot=-2, dark=True)), 1.25, 1.15, 200, 60))
scene(196.5, 201.8, cam(f'<div class="card" style="left:620px;top:200px;width:680px;height:620px;text-align:center"{A(196.7, "fade")}><div class="k">CALENDARIO</div><div class="tw" style="font-size:200px;line-height:1.3;color:{INK}"><span data-count="1587,1588,198.6,1.6">1587</span></div><div class="b">«volvería pronto»</div></div>'
        + stamp('LAS CIRCUNSTANCIAS CAMBIARON', 520, 820, 199.8, rot=-4, size=46), 1.0, 1.05))
scene(201.8, 210.6, cam(mapa_atlantico(9999, 201.9, 201.9, extra=''.join(
            f'<g transform="translate({1560 - i * 95},{600 + (i % 2) * 60}) scale(.3)"><g{A(round(204.6 + i * 0.25, 2), "fade")}>{ship("#7b2a1e")[ship("#7b2a1e").index(">") + 1:-6]}</g></g>' for i in range(6)))
        + f'<div class="abs fell" style="left:1580px;top:770px;font-size:44px"{A(202.4)}>España</div>'
        + tag('1585–1604 · guerra anglo-española', 260, 160, 202.6, rot=-2, dark=True) + tag('1588 · la Armada española', 1050, 820, 205.0, rot=2), 1.0, 1.08, 0, 0))
scene(210.6, 221.6, cam(svg(f'<path d="M160,540 L1760,540" stroke="{SEP}" stroke-width="6"{A(210.8, "draw", dur=2.5)}/>' + ''.join(
            f'<circle cx="{260 + i * 466}" cy="540" r="22" fill="{RED if i == 3 else SEP}"{A(round(210.9 + i * 0.75, 2), "fade")}/>' for i in range(4)))
        + ''.join(f'<div class="abs tw" style="left:{180 + i * 466}px;top:420px;width:160px;text-align:center;font-size:52px"{A(round(211.0 + i * 0.75, 2))}>{y}</div>' for i, y in enumerate([1587, 1588, 1589, 1590]))
        + typed('Pasaron los meses… después, los años.', 160, 200, 210.9, size=46, font='Fell')
        + tag('¿Qué pasaba al otro lado del océano?', 560, 680, 216.6, rot=-1.5, dark=True, size=40), 1.0, 1.05))

# CAP V — El regreso y la palabra (221.6 – 287.5)
scene(221.6, 228.5, cam(sea(night=False, ship_x=760, ship_y=650, moon=False) + bigdate('18 · VIII · 1590', 150, 160, 224.0, size=110) + tag('John White regresa a Roanoke', 160, 330, 225.9, rot=-1), 1.0, 1.1, 0, -20))
scene(228.5, 238.0, cam(f'<div class="card" style="left:410px;top:170px;width:1100px;height:660px;text-align:center"{A(228.7, "fade")}><div class="k">ESE MISMO DÍA</div>'
        + f'<div class="fell" style="font-size:96px;margin-top:40px;color:{RED}">Virginia Dare</div><div class="tw" style="font-size:54px;margin-top:30px">cumplía <span data-count="0,3,234.5,1.0">0</span> años</div>'
        + f'<div class="b" style="margin-top:50px">18/08/1587 → 18/08/1590</div></div>', 1.0, 1.05))
scene(238.0, 246.5, cam(palisade() + stamp('DESHABITADA', 300, 220, 238.2, rot=-6, size=60) + stamp('SIN SEÑALES DE LUCHA', 960, 320, 243.4, rot=5), 1.08, 1.0))
scene(246.5, 256.3, cam(carving('CRO', 0, 420, 252.6, 0.4, size=190) + tag('«CRO» · tallado en un árbol', 120, 140, 252.0, rot=-2), 1.0, 1.15))
scene(256.3, 263.1, cam(photo('02.jpg', 260, 120, 1400, 860, '1.12,1.35,-4,-3,4,2', 'Grabado, 1876 · dominio público', rot=-1)
        + stamp('CROATOAN', 1180, 860, 259.0, rot=-6, size=64), 1.0, 1.03))
scene(263.1, 272.0, cam(mapa_costa('', pin(*ROA, 'Roanoke', 263.3, dx=-280, dy=40) + pin(*CRO, 'Croatoan', 266.0, dx=-330, dy=10)
        ), 1.0, 1.12, -120, -110)
        + tag('Croatoan: pueblo aliado y también una isla', 160, 160, 264.5, rot=-1.5, dark=True)
        + tag('hoy: isla Hatteras', 1360, 600, 269.5, rot=-2))
scene(272.0, 278.0, cam(notebook(['Si se mudan → tallar el nombre del lugar', 'Si es una emergencia → añadir una cruz ✠'], 260, 260, 1400, [272.2, 272.4], title='El código acordado', title_t=272.1)
        + f'<div class="abs tw" style="left:1600px;top:420px;font-size:110px;color:#3f5a3a"{A(274.4, "pop")}>✓</div>', 1.0, 1.06))
scene(278.0, 287.5, cam(notebook(['Si se mudan → tallar el nombre del lugar', 'Si es una emergencia → añadir una cruz ✠'], 260, 260, 1400, [278.0, 278.0], title='El código acordado', title_t=278.0)
        + f'<div class="abs tw" style="left:1600px;top:420px;font-size:110px;color:#3f5a3a">✓</div>'
        + stamp('SIN CRUZ', 1180, 640, 280.7, rot=-8, size=70) + tag('Para White: una pista importante', 330, 760, 284.1, rot=-1.5, dark=True), 1.0, 1.12, 0, -20))

# CAP VI — ¿Qué pudo haber ocurrido? (287.5 – 359.5)
scene(287.5, 300.4, cam(mapa_costa(f'<path d="M1010,490 Q1200,700 1385,795" stroke="{RED}" stroke-width="7" fill="none"{A(290.6, "draw", dur=1.8)}/>',
        pin(*ROA, 'Roanoke', 288.8, dx=40, dy=40) + pin(*CRO, 'Croatoan', 291.4, dx=-330, dy=10)
        + card('HIPÓTESIS', 'Se trasladaron a Croatoan', 'A favor: el mensaje coincide con el lugar y con lo acordado.', 120, 120, 680, 289.0, rot=-1.5, label='HIPÓTESIS 1')), 1.0, 1.06))
scene(300.4, 306.9, cam(dossier('Manteo', 'vínculo entre ingleses y croatoan', ['relaciones previas de confianza'], 410, 300, 300.6), 1.0, 1.05))
scene(306.9, 314.1, cam(card('HECHO', 'No hay prueba definitiva', 'Ni de que llegaran allí, ni de qué les pasó después.', 520, 280, 880, 307.4, rot=-1)
        + stamp('PERO…', 300, 160, 307.0, rot=-8, size=60), 1.0, 1.05))
scene(314.1, 319.9, cam(mapa_costa(f'<path d="M985,450 Q780,330 515,262" stroke="{BLUE}" stroke-width="7" fill="none" stroke-dasharray="20 12"{A(315.0, "draw", dur=2)}/>',
        pin(*ROA, 'Roanoke', 314.2, dx=40, dy=40) + pin(*SITIOX, '«Sitio X»', 317.0, dx=-80, dy=-50, col=BLUE)), 1.15, 1.25, 150, 50)
        + card('HIPÓTESIS', 'Tierra adentro', None, 1250, 520, 540, 314.4, rot=1.5, label='HIPÓTESIS 2'))
scene(319.9, 327.4, cam(card('HECHO', 'Objetos europeos de la época', 'Hallados tierra adentro y en Hatteras', 180, 250, 740, 320.2, rot=-2)
        + card('NO DEMOSTRADO', 'Que fueran de los colonos', 'Pueden venir de comercio u otros contactos', 1000, 330, 740, 322.7, rot=1.5), 1.0, 1.05))
scene(327.4, 332.9, cam(typed('Otras causas posibles', 160, 150, 327.6, size=48, font='Fell')
        + icon_box(160, 300, 'Hambre', 328.6, '⚘') + icon_box(750, 300, 'Enfermedades', 329.6, '✚') + icon_box(1340, 300, 'Dificultades ambientales', 330.6, '☂'), 1.0, 1.04))
scene(332.9, 338.7, cam(rings(333.0) + card('HECHO', 'Sequía de 1587 a 1589', 'La más severa en 800 años en la región, según los anillos de cipreses (Stahle et al., 1998).', 1220, 230, 620, 334.6, rot=1.5), 1.0, 1.06, 40, 0))
scene(338.7, 346.3, cam(card('HIPÓTESIS', 'Ataques españoles', None, 200, 300, 640, 339.0, rot=-2, label='OTRA TEORÍA')
        + card('HIPÓTESIS', 'Fenómenos naturales', None, 1060, 340, 640, 340.8, rot=1.5, label='OTRA TEORÍA')
        + stamp('NO EXPLICAN TODO', 650, 720, 342.8, rot=-5, size=52), 1.0, 1.05))
scene(346.3, 351.3, cam(f'<div class="abs fell" style="left:0;right:0;top:360px;text-align:center;font-size:120px"{A(346.6, "fade")}>posibilidad <span style="color:{RED}">≠</span> certeza</div>', 1.0, 1.08))
scene(351.3, 359.5, cam(svg(f'<path d="M420,330 L960,620 L1500,330 M420,330 L1500,330 M960,620 L960,860" stroke="{RED}" stroke-width="4" fill="none"{A(352.0, "draw", dur=2.5)}/>')
        + card('HIPÓTESIS', 'Croatoan', None, 200, 210, 440, 351.5, rot=-3, label='H1') + card('HIPÓTESIS', 'Tierra adentro', None, 1290, 210, 440, 351.9, rot=2, label='H2')
        + card('HIPÓTESIS', 'Hambre y sequía', None, 740, 520, 440, 352.3, rot=-1, label='H3')
        + stamp('SIN RESOLVER', 700, 860, 356.0, rot=-6, size=60), 1.0, 1.05))

# CAP VII — La última pista (359.5 – 399.6)
scene(359.5, 364.7, cam(mapa_costa(f'<path d="M1900,600 Q1650,700 1420,790" stroke="{RED}" stroke-width="7" fill="none" stroke-dasharray="20 12"{A(361.5, "draw", dur=1.8)}/>',
        pin(*CRO, 'Croatoan', 361.0, dx=-330, dy=10) + tag('White intenta ir a buscarlos', 1150, 300, 362.6, rot=-2, dark=True)), 1.1, 1.25, -200, -150))
scene(364.7, 373.2, cam(sea(night=True, storm=True, ship_x=880, ship_y=650, island=False).replace('__FLASH__', '366.6,367.1,369.9,371.4')
        + tag('tormenta · viaje interrumpido', 150, 160, 368.0, rot=-2, dark=True), 1.05, 1.15))
scene(373.2, 380.3, cam(mapa_atlantico(373.6, 373.3, 373.3, extra=f'<circle cx="505" cy="500" r="16" fill="{RED}"/>', back=True) + stamp('NUNCA VOLVIÓ', 720, 620, 377.6, rot=-6, size=60), 1.0, 1.06))
scene(380.3, 387.9, cam(f'<div class="abs" style="inset:0;background:url(assets/05b.jpg) center/cover"></div><div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(20,12,6,.72),rgba(20,12,6,.35) 60%,rgba(20,12,6,0))"></div>'
        + typed('Uno de los grandes enigmas\nde la colonización inglesa', 160, 300, 381.0, size=72, color='#f4e8cf', font='Fell')
        + f'<div class="abs tw" style="left:160px;top:920px;font-size:22px;color:#e8dab9">Ilustración (fondo)</div>', 1.0, 1.1))
scene(387.9, 399.6, cam(svg(f'<path d="M960,980 L960,700" stroke="{SEP}" stroke-width="10" fill="none"{A(388.0, "draw", dur=1)}/>'
            f'<path d="M960,700 Q760,560 520,430" stroke="{SEP}" stroke-width="8" fill="none"{A(388.9, "draw", dur=1.4)}/>'
            f'<path d="M960,700 Q1160,560 1400,430" stroke="{SEP}" stroke-width="8" fill="none"{A(390.6, "draw", dur=1.4)}/>'
            f'<path d="M960,700 Q980,520 960,330" stroke="{SEP}" stroke-width="8" fill="none" stroke-dasharray="14 12"{A(392.0, "draw", dur=1.4)}/>')
        + card('HIPÓTESIS', 'Refugio en otras comunidades', None, 130, 240, 520, 389.2, rot=-2, label='QUIZÁS')
        + card('HIPÓTESIS', 'Se dividieron', None, 1300, 240, 480, 391.0, rot=2, label='QUIZÁS')
        + stamp('PRUEBAS INSUFICIENTES', 600, 160, 396.0, rot=-4, size=50), 1.0, 1.05))

# CAP VIII — Una pregunta abierta (399.6 – fin)
scene(399.6, 408.0, cam(carving('CROATOAN', 0, 430, 400.0, 0.0, size=170, kind='post')
        + f'<div class="card" style="left:1260px;top:740px;width:520px;text-align:center"{A(405.2, "pop")}><div class="tw" style="font-size:64px"><span data-count="1590,2026,405.3,1.8">1590</span></div><div class="b">más de cuatro siglos</div></div>', 1.25, 1.0))
scene(408.0, 415.0, cam(f'<div class="abs" style="inset:0;background:#2a2119"></div>'
        + typed('¿Desaparecieron…', 200, 330, 408.2, size=96, color='#f4e8cf', font='Fell')
        + typed('…o dejaron de vivir donde\nlos ingleses esperaban encontrarlos?', 200, 480, 410.4, size=72, color='#e3cfa6', font='Fell'), 1.0, 1.06))
scene(415.0, 422.4, cam(mapa_costa(''.join(f'<circle cx="{x}" cy="{y}" r="40" fill="#e9b65a" fill-opacity=".6"{A(round(417 + i * 0.6, 2), "fade")}/>' for i, (x, y) in enumerate([(1395, 800), (560, 330), (760, 560), (1210, 600), (420, 760)])),
        tag('comunidades y lugares donde pudieron seguir viviendo', 300, 160, 417.5, rot=-1.5, dark=True)), 1.0, 1.08))
scene(422.4, 428.8, cam(photo('09.jpg', 280, 150, 1360, 760, '1.0,1.2,0,0,3,2', 'Ilustración · asentamiento vacío', rot=1.5)
        + stamp('CASO ABIERTO', 700, 420, 425.6, rot=-8, size=90), 1.0, 1.05))
scene(428.8, DUR, cam(f'<div class="abs" style="inset:0;background:#21180f"></div>'
        + typed('El pasado no siempre desaparece.', 0, 360, 429.1, size=78, color='#f4e8cf', font='Fell', anchor='center', w=1920)
        + typed('A veces, simplemente deja de ser comprendido.', 0, 480, 431.6, size=62, color='#e3cfa6', font='Fell', anchor='center', w=1920)
        + f'<div class="abs tw" style="left:0;right:0;top:700px;text-align:center;font-size:38px;color:#c8ae84;letter-spacing:6px"{A(434.0)}>HistorIAs del mundo</div>', 1.0, 1.05))

# capítulos
CAPS = [(0.0, 'I', 'El misterio', 'Roanoke · 1590'), (44.4, 'II', 'Un proyecto en tierras desconocidas', '1587'), (106.0, 'III', 'Una colonia bajo presión', '1587'),
        (166.7, 'IV', 'La partida de John White', '1587 – 1590'), (221.6, 'V', 'El regreso y la palabra', '18 de agosto de 1590'),
        (287.5, 'VI', '¿Qué pudo haber ocurrido?', 'hipótesis y evidencias'), (359.5, 'VII', 'La última pista', '1590'), (399.6, 'VIII', 'Una pregunta abierta', 'cierre')]
chapters = [dict(t=c[0], n=c[1], title=c[2], sub=c[3], card=(0.0 if c[0] == 0 else c[0]), cd=(2.4 if c[0] == 0 else 3.2)) for c in CAPS]
# continuidad: comprobar huecos
S.sort(key=lambda s: s['t0'])
for a, b in zip(S, S[1:]):
    if abs(a['t1'] - b['t0']) > 0.01: print('HUECO/SOLAPE', a['t0'], a['t1'], b['t0'])
gaps = [b['t0'] - a['t0'] for a, b in zip(S, S[1:])]
print('escenas', len(S), 'máx duración', max(s['t1'] - s['t0'] for s in S))
json.dump(dict(scenes=S, subs=SUBS, chapters=chapters, dur=DUR), open('data.json', 'w'), ensure_ascii=False)

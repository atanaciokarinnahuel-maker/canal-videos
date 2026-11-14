"""Render de la bienvenida de Bases Bíblicas (adaptado de .claude/skills/motion-design/scripts/render_template.py).
probe t1 t2 ...   -> probe/p_XX.png + probe/sheet.png
draft             -> 30 fps, 1 captura por cuadro, 540x960 -> out/draft.mp4 (para juzgar el ritmo)
chunk k n         -> parte k de n del render final (SUB subcuadros por cuadro, obturador 180 grados, tmix) -> out/part_k.mp4
concat n          -> une las partes -> out/video.mp4
pops              -> busca saltos de un cuadro en out/video.mp4
Uso típico: python3 render.py chunk 0 4 & ... (4 procesos) ; python3 render.py concat 4
"""
import asyncio, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from playwright.async_api import async_playwright

HERE = Path(__file__).parent
FF = shutil.which("ffmpeg") or __import__("imageio_ffmpeg").get_ffmpeg_exe()
URL = "file://" + str(HERE / "film.html")
VW, VH = 1080, 1920
FPS, T, SUB = 60, 31.2, 4
SHUTTER = 0.5
CHROME = os.environ.get("CHROME") or ("/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
ARGS = ["--font-render-hinting=none", "--force-color-profile=srgb", "--disable-threaded-animation"]


async def open_page(p):
    b = await p.chromium.launch(args=ARGS, **({"executable_path": CHROME} if CHROME else {}))
    pg = await b.new_page(viewport={"width": VW, "height": VH}, device_scale_factor=1)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type in ("error", "warning") else None)
    await pg.goto(URL)
    await pg.wait_for_function("window.ready === true", timeout=120000)
    await pg.evaluate("document.fonts.ready")
    await pg.add_style_tag(content="*,*::before,*::after{transition:none!important;caret-color:transparent!important}")
    await pg.evaluate("document.getAnimations().forEach(a => a.pause())")
    return b, pg, errs


async def shot(pg, t, path=None, fmt="png"):
    await pg.evaluate(f"window.seek({t})")
    await pg.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
    kw = {"quality": 94} if fmt == "jpeg" else {}
    return await pg.screenshot(type=fmt, clip={"x": 0, "y": 0, "width": VW, "height": VH}, **({"path": str(path)} if path else {}), **kw)


async def probe(times, cols=None):
    out = HERE / "probe"; shutil.rmtree(out, ignore_errors=True); out.mkdir()
    async with async_playwright() as p:
        b, pg, errs = await open_page(p)
        for i, t in enumerate(times): await shot(pg, t, out / f"p_{i:02d}.png")
        await b.close()
    if errs: print("PAGE ERRORS:", errs[:8])
    cols = cols or min(6, len(times)); rows = -(-len(times) // cols)
    subprocess.run([FF, "-v", "error", "-y", "-i", str(out / "p_%02d.png"), "-vf",
                    f"scale=360:-1,tile={cols}x{rows}:padding=6:color=white", "-frames:v", "1", str(out / "sheet.png")], check=True)
    print("probe:", len(times), "->", out / "sheet.png")


async def draft(fps=30):
    (HERE / "out").mkdir(exist_ok=True)
    ff = subprocess.Popen([FF, "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-", "-vf", "scale=540:-2",
                           "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(HERE / "out/draft.mp4")], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b, pg, errs = await open_page(p)
        for i in range(int(round(T * fps))): ff.stdin.write(await shot(pg, min(T - 1e-3, i / fps), fmt="jpeg"))
        await b.close()
    ff.stdin.close(); ff.wait()
    if errs: print("PAGE ERRORS:", errs[:8])
    print("draft ->", HERE / "out/draft.mp4")


async def chunk(k, n):
    """Cuadros [a, b) del master: SUB subcuadros repartidos en SHUTTER del intervalo, mezclados con tmix."""
    (HERE / "out").mkdir(exist_ok=True)
    total = int(round(T * FPS)); a, b_ = total * k // n, total * (k + 1) // n
    offs = [(j - (SUB - 1) / 2) * SHUTTER / (FPS * SUB) for j in range(SUB)]
    out = HERE / f"out/part_{k}.mp4"
    ff = subprocess.Popen([FF, "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS * SUB), "-c:v", "mjpeg", "-i", "-",
                           "-vf", f"tmix=frames={SUB},select='eq(mod(n\\,{SUB})\\,{SUB - 1})',setpts=N/{FPS}/TB,scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p",
                           "-r", str(FPS), "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-color_range", "tv", "-colorspace", "bt709",
                           "-color_primaries", "bt709", "-color_trc", "bt709", str(out)], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        br, pg, errs = await open_page(p)
        for i in range(a, b_):
            for o in offs: ff.stdin.write(await shot(pg, min(T - 1e-3, max(0.0, i / FPS + o)), fmt="jpeg"))
            if (i - a) % 120 == 0: print(f"parte {k}: cuadro {i - a}/{b_ - a}", flush=True)
        await br.close()
    ff.stdin.close(); r = ff.wait()
    if errs: print("PAGE ERRORS:", errs[:8])
    print("parte ->", out, "ffmpeg", r)


def concat(n):
    lst = HERE / "out/parts.txt"; lst.write_text("".join(f"file 'part_{k}.mp4'\n" for k in range(n)))
    subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(HERE / "out/video.mp4")], check=True)
    print("video ->", HERE / "out/video.mp4")


def pops(path=None):
    path = path or HERE / "out/video.mp4"
    raw = subprocess.run([FF, "-v", "quiet", "-i", str(path), "-vf", "scale=180:320,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 320, 180).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)); hits = []
    for i in range(1, len(d) - 1):
        nb = max(d[i - 1], d[i + 1], 0.3)
        if d[i] > 3 * nb and d[i] > 2.0: hits.append((i + 1, round((i + 1) / FPS, 3), round(float(d[i]), 2), round(float(nb), 2)))
    print("cuadros:", len(fr), "saltos:", len(hits))
    for h in hits: print("  cuadro", h[0], "t", h[1], "dif", h[2], "vecinos", h[3])
    flashes = []
    for n in range(1, len(fr) - 1):
        a, b = d[n - 1], d[n]; skip = np.abs(fr[n + 1] - fr[n - 1]).mean()
        if min(a, b) > 2.0 and skip < 0.35 * min(a, b): flashes.append((n, round(n / FPS, 3)))
    print("destellos de un cuadro:", len(flashes), flashes[:10])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "probe": asyncio.run(probe([float(x) for x in sys.argv[2:]]))
    elif cmd == "draft": asyncio.run(draft())
    elif cmd == "chunk": asyncio.run(chunk(int(sys.argv[2]), int(sys.argv[3])))
    elif cmd == "concat": concat(int(sys.argv[2]))
    elif cmd == "pops": pops()

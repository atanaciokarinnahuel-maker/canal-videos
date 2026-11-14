"""Banda sonora de la bienvenida de Bases Bíblicas (31,2 s, 100 BPM, re mayor), 100 % sintetizada con numpy/scipy:
no usa música ni efectos de terceros. Cada golpe cae en el mismo tiempo que su momento visual en film.html.
Salida: out/audio.wav normalizado a -14 LUFS (dos pasadas de loudnorm)."""
import json, shutil, subprocess
from pathlib import Path
import numpy as np, scipy.signal as sg

HERE = Path(__file__).parent
FF = shutil.which("ffmpeg") or __import__("imageio_ffmpeg").get_ffmpeg_exe()
SR, T, B = 48000, 31.2, 0.6
BAR, N = 4 * B, int(round(T * SR))
rng = np.random.default_rng(119105)
mus, drm, sfx = np.zeros((N, 2)), np.zeros((N, 2)), np.zeros((N, 2))   # melódico (con reverb), batería, efectos


def add(bus, sig, t, g=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N or i + len(sig) <= 0: return
    if i < 0: sig, i = sig[-i:], 0
    j = min(N, i + len(sig)); l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    bus[i:j, 0] += sig[:j - i] * g * l; bus[i:j, 1] += sig[:j - i] * g * r


def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, fc, o=2): b, a = sg.butter(o, fc / (SR / 2)); return sg.lfilter(b, a, x)
def hp(x, fc, o=2): b, a = sg.butter(o, fc / (SR / 2), "high"); return sg.lfilter(b, a, x)
def bp(x, lo, hi, o=2): b, a = sg.butter(o, [lo / (SR / 2), hi / (SR / 2)], "band"); return sg.lfilter(b, a, x)
def fade(x, a=.004, r=.03):
    n = len(x); e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return x * e


def keys(m, d=1.1):
    t = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6) + .25 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 9) + .1 * np.sin(2 * np.pi * 4.01 * f * t) * np.exp(-t * 14)
    return fade(s * np.exp(-t * 3.4), .004, .05)
def bell(m, d=1.6):
    t = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.5) + .45 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 7) + .22 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 12)
    return fade(s, .002, .05)
def bass(m, d):
    t = tt(d); f = hz(m); s = lp(sg.sawtooth(2 * np.pi * f * t) * .5, 420) + np.sin(2 * np.pi * f * t)
    return fade(s * np.exp(-t * 2.6), .006, .04)
def pad(ms, d, fc=1500):
    t = tt(d); s = sum(sg.sawtooth(2 * np.pi * hz(m) * 1.004 * t) * .18 + sg.sawtooth(2 * np.pi * hz(m) * .996 * t) * .18 + np.sin(2 * np.pi * hz(m) * t) * .4 for m in ms)
    return lp(s, fc) * np.minimum(1, t / .45) * np.minimum(1, (d - t) / .5)
def kick():
    t = tt(.32); return fade(np.sin(2 * np.pi * np.cumsum(46 + 120 * np.exp(-t * 28)) / SR) * np.exp(-t * 10) + .25 * hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 200), .001, .03)
def clap():
    t = tt(.24); e = np.exp(-t * 26) + .6 * np.exp(-np.maximum(0, t - .012) * 32) * (t > .012) + .4 * np.exp(-np.maximum(0, t - .024) * 30) * (t > .024)
    return bp(rng.standard_normal(len(t)), 900, 5500) * e
def hat(op=False):
    t = tt(.14 if op else .05); return hp(rng.standard_normal(len(t)), 8000) * np.exp(-t * (22 if op else 85))
def snare():
    t = tt(.16); return (bp(rng.standard_normal(len(t)), 1200, 7000) * np.exp(-t * 30) + .5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 40))
def crash(d=1.8):
    t = tt(d); return hp(rng.standard_normal(len(t)), 4500) * np.exp(-t * 4.6) * np.minimum(1, t * 300)
def boom():
    t = tt(1.1); return fade(np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 9)) / SR) * np.exp(-t * 3.6), .002, .1)
def sweep(d, up=True, lo=300, hi=7000, bands=10):
    """Barrido de ruido: bandas que se abren una tras otra (subida) o se cierran (bajada)."""
    t = tt(d); s = rng.standard_normal(len(t)); o = np.zeros(len(t))
    for k in range(bands):
        f0 = lo * (hi / lo) ** (k / bands); f1 = lo * (hi / lo) ** ((k + 1) / bands)
        c = (k + .5) / bands * d if up else (1 - (k + .5) / bands) * d
        o += bp(s, f0, f1) * np.exp(-((t - c) / (d * .22)) ** 2)
    e = (t / d) ** 2 if up else (1 - t / d) ** 1.5
    return fade(o * (.25 + .75 * e), .01, .01 if up else .05)
def whoosh(d=.42):
    t = tt(d); return bp(rng.standard_normal(len(t)), 500, 5000) * np.exp(-((t - d * .45) / (d * .22)) ** 2)
def popn(m):
    t = tt(.16); f = hz(m) * (1 + .5 * np.exp(-t * 60)); return fade(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 26), .001, .02)
def click():
    t = tt(.05); return (np.sin(2 * np.pi * 1900 * t) + .6 * hp(rng.standard_normal(len(t)), 3000)) * np.exp(-t * 110)
def thock():
    t = tt(.2); return (np.sin(2 * np.pi * np.cumsum(120 + 200 * np.exp(-t * 50)) / SR) * np.exp(-t * 22) + .4 * bp(rng.standard_normal(len(t)), 800, 3000) * np.exp(-t * 60))
def shing():
    t = tt(.9); return fade(sum(np.sin(2 * np.pi * f * t) * a for f, a in [(2637, 1), (3951, .6), (5274, .35), (6200, .2)]) * np.exp(-t * 6) + .3 * hp(rng.standard_normal(len(t)), 6000) * np.exp(-t * 40), .001, .05)
def fwoosh():
    t = tt(.7); return (bp(rng.standard_normal(len(t)), 250, 2600) * np.exp(-((t - .12) / .14) ** 2) + .5 * lp(rng.standard_normal(len(t)), 500) * np.exp(-t * 5)) * np.minimum(1, t * 60)
def fire(d):
    t = tt(d); n = len(t); bed = lp(rng.standard_normal(n), 380) * (.5 + .5 * lp(np.abs(rng.standard_normal(n)), 3)) * .5
    cr = np.zeros(n)
    for i in rng.integers(0, n - 400, int(d * 9)): cr[i:i + 300] += rng.standard_normal(300) * np.exp(-np.arange(300) / 40) * rng.uniform(.2, 1)
    return fade(bed + hp(cr, 1800) * .5, .25, .3)


CH = {"D": ([62, 66, 69], 38), "A": ([61, 64, 69], 45), "Bm": ([62, 66, 71], 47), "G": ([62, 67, 71], 43)}
MEL = {"D": [(0, 78), (2, 81), (3, 86), (6, 81)], "A": [(0, 76), (2, 81), (3, 85), (6, 81)], "Bm": [(0, 74), (2, 78), (3, 83), (6, 78), (7, 81)], "G": [(0, 79), (2, 83), (3, 86), (6, 83)]}


def groove(bar, ch, energy=1.0, drums=True, mel=True, beats=4):
    t0 = bar * BAR; notes, root = CH[ch]; e = B / 2
    add(mus, pad(notes, beats * B + .3), t0, .11 * energy)
    for k in range(beats * 2):
        tk = t0 + k * e
        if k in (0, 3, 6):
            for m in notes: add(mus, keys(m), tk, .15 * energy, (m - 65) / 20)
            add(drm, bass(root, e * 2.6), tk, .34 * energy)
        else: add(mus, keys(notes[(k * 2) % 3] + 12, .6), tk, .07 * energy, .25 if k % 2 else -.25)
        if drums:
            add(drm, hat(k == 7), tk, .07 if k % 2 == 0 else .11, .2)
            if k % 2 == 0: add(drm, kick(), tk, .78)
            if k in (2, 6): add(drm, clap(), tk, .3)
            for j in (0, 1): add(drm, hp(rng.standard_normal(1400), 6000) * np.exp(-np.arange(1400) / 260), tk + j * e / 2, .022, -.3)
    if mel:
        for k, m in MEL[ch]:
            if k < beats * 2: add(mus, bell(m), t0 + k * e, .17 * energy, .15)


def hit(t, g=1.0):
    add(drm, boom(), t, .8 * g); add(drm, crash(), t, .11 * g); add(drm, kick(), t, .7 * g)


# --- estructura (compás k empieza en 2,4·k) ---
add(mus, pad([50, 57, 62], 2.9, 700), 0, .2)                                   # 0: noche, re grave
add(sfx, fire(2.3), .35, .1, .35)
add(sfx, fwoosh(), .4 - .12, .5, .35); add(mus, bell(86, 1.2), .42, .09, .3)   # la llama se enciende (0,40 s)
for i, m in enumerate([74, 78, 81]): add(mus, bell(m, 1.2), .8 + i * .09, .08, -.2 + i * .2)
add(sfx, sweep(1.1, True), 2.4 - 1.1, .28)
hit(2.4)                                                                        # 1-3: bienvenida y "cada día"
for b, c in [(1, "D"), (2, "A"), (3, "Bm")]: groove(b, c)
for i, m in enumerate([74, 76, 78, 81, 83, 86, 90]): add(sfx, popn(m), 7.8 + i * .15, .3, -.6 + i * .2)
for tw in (6.9, 9.3): add(sfx, whoosh(.4), tw - .18, .13)
groove(4, "G", .8, drums=False)                                                 # 4: "lo que viene", sin batería y redoble
add(drm, kick(), 9.6, .7); add(drm, crash(1.2), 9.6, .08)
for i in range(3): add(sfx, thock(), 10.8 + i * .1, .28, -.4 + i * .4)
for i in range(8): add(drm, snare(), 10.8 + i * .15, .08 + .028 * i)
add(sfx, sweep(1.2, True), 12.0 - 1.2, .26)
hit(12.0)                                                                       # 5-7: las tres tarjetas
for b, c in [(5, "D"), (6, "A"), (7, "Bm")]: groove(b, c, 1.05)
for tw in (11.9, 14.3, 16.7, 18.98): add(sfx, whoosh(.38), tw - .17, .16)
add(sfx, whoosh(.5), 13.2, .14, .3); add(sfx, thock(), 13.7, .4, .4); add(mus, bell(93, .8), 13.72, .1, .4)   # la piedra
add(mus, bell(88, 1.0), 15.6, .09, -.2)                                         # "y pan en plena sequía"
add(sfx, shing(), 18.1, .1, -.3); add(sfx, thock(), 18.15, .25, -.3)            # la espada baja
hit(19.2, 1.1)                                                                  # 8: "Quédate." (golpe y silencio)
groove(8, "G", .75, drums=False, mel=False)
add(sfx, whoosh(.36), 19.5, .1)
for k, m in [(3, 83), (4, 86), (5, 91)]: add(mus, bell(m), 19.2 + k * .3, .12, .1)
add(sfx, sweep(.7, False), 21.55, .2)                                           # 9-10: versículo, calma
add(sfx, fire(4.9), 21.7, .1, .35)
for b, c in [(9, "G"), (10, "A")]:
    notes, root = CH[c]; t0 = b * BAR
    add(mus, pad(notes + [notes[0] - 12], BAR + .4, 1100), t0, .17); add(drm, bass(root, 2.2), t0, .22)
    for k, m in enumerate([notes[0], notes[1], notes[2], notes[1] + 12, notes[2], notes[1], notes[2] + 12, notes[1] + 12]): add(mus, keys(m + 12, 1.4), t0 + k * .3, .085, -.3 + .6 * (k % 2))
for tl, m in [(22.2, 79), (22.76, 83), (23.5, 86)]: add(mus, bell(m, 2.0), tl, .1, -.1)
add(mus, bell(90, 2.0), 24.5, .11, .1)
add(sfx, sweep(1.0, True), 26.4 - 1.0, .26)
hit(26.4)                                                                       # 11-12: cierre
groove(11, "D", 1.05)
groove(12, "G", 1.05, beats=2)
add(sfx, popn(81), 26.76, .25); add(sfx, click(), 27.6, .5); add(mus, bell(86, .9), 27.67, .16); add(mus, bell(93, 1.2), 27.79, .16)
for i in range(6): add(mus, bell(98 + (i % 2) * 2, .35), 28.0 + i * .085, .07 * (1 - i * .1), .4)   # campanita
add(sfx, whoosh(.4), 28.62, .12)
notes, root = CH["D"]                                                           # acorde final (30,0 s)
add(drm, boom(), 30.0, .7); add(drm, crash(1.4), 30.0, .12); add(drm, kick(), 30.0, .7); add(drm, bass(root, 1.3), 30.0, .4)
for m in notes + [74, 78, 86]: add(mus, keys(m, 1.4), 30.0, .16, (m - 70) / 24)
add(mus, bell(90, 1.3), 30.0, .16); add(mus, pad(notes, 1.3), 29.95, .12)

# --- reverb (respuesta al impulso sintética) y mezcla ---
ti = tt(1.7); ir = np.stack([lp(rng.standard_normal(len(ti)), 6500) * np.exp(-ti * 4.2) for _ in range(2)], 1); ir /= np.sqrt((ir ** 2).sum(0))
def rev(x): return np.stack([sg.fftconvolve(x[:, c], ir[:, c])[:N] for c in range(2)], 1)
mix = mus + .26 * rev(mus) + drm + .05 * rev(drm) + sfx + .12 * rev(sfx)
f0 = int(30.75 * SR); mix[f0:] *= np.linspace(1, 0, N - f0)[:, None] ** 1.5
mix = np.tanh(mix * 1.1) / 1.1
(HERE / "out").mkdir(exist_ok=True); rawp = HERE / "out/raw.wav"
subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(rawp)], input=mix.astype(np.float32).tobytes(), check=True)
m = subprocess.run([FF, "-hide_banner", "-i", str(rawp), "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-1:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
subprocess.run([FF, "-v", "error", "-y", "-i", str(rawp), "-af", af, "-ar", str(SR), str(HERE / "out/audio.wav")], check=True)
print("entrada", j["input_i"], "LUFS · pico", j["input_tp"], "-> out/audio.wav")

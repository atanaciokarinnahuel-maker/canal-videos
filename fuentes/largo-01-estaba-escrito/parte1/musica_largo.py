#!/usr/bin/env python3
"""Música para videos largos de la plantilla grabado. Lee info.json (dur, capitulos, temblores) y escribe musica.wav.
Cada capítulo empieza en modo menor (suspenso: nota grave, latido, lira espaciada) y pasa a mayor en su último tercio
(el cumplimiento). Golpe grave y tensión antes de cada temblor (palabras de Dios, gritos)."""
import json
import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf
sr = 32000
info = json.load(open('info.json')); dur = info['dur']; n = int(dur * sr)
out = np.zeros((n, 2), dtype=np.float32); rng = np.random.default_rng(11)
caps = sorted(set([0.0] + [c for c in info.get('capitulos', []) if c > 1])); caps.append(dur)
def add(sig, t, pan=0.0, g=1.0):
    i = int(t * sr)
    if i >= n or i < 0: return
    j = min(n, i + len(sig)); l = np.sqrt(.5 * (1 - pan)); r = np.sqrt(.5 * (1 + pan))
    out[i:j, 0] += (sig[:j - i] * g * l).astype(np.float32); out[i:j, 1] += (sig[:j - i] * g * r).astype(np.float32)
note = lambda m: 440 * 2 ** ((m - 69) / 12)
T = lambda d: np.arange(int(d * sr)) / sr
def lp(x, fc):
    b, a = sg.butter(2, fc / (sr / 2)); return sg.lfilter(b, a, x)
def pad(fs, d):
    t = T(d); s = sum(np.sin(2 * np.pi * f * t) * .5 + np.sin(2 * np.pi * f * 1.004 * t) * .35 for f in fs)
    return lp(s, 1000) * np.minimum(1, t / 1.6) * np.minimum(1, (d - t) / 1.6)
def lira(f, d=2.4):
    t = T(d); return (np.sin(2 * np.pi * f * t) * np.exp(-t * 2) + .4 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3.5)) * np.minimum(1, t * 300)
def latido():
    t = T(.5); return np.sin(2 * np.pi * np.cumsum(42 + 40 * np.exp(-t * 30)) / sr) * np.exp(-t * 9)
def tension(d=2.0):
    t = T(d); s = np.sin(2 * np.pi * note(69) * t) + np.sin(2 * np.pi * note(70) * t); return s * (.6 + .4 * np.sin(2 * np.pi * 8 * t)) * (t / d) ** 2.2
def trueno():
    t = T(1.8); return np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-t * 10)) / sr) * np.exp(-t * 3) + lp(rng.standard_normal(len(t)), 450) * np.exp(-t * 6) * .5
def soplo(d=1.2):
    t = T(d); return lp(rng.standard_normal(len(t)), 2200) * np.exp(-((t - d * .5) / (d * .22)) ** 2)
def brillo(d=3.5):
    t = T(d); s = sum(np.sin(2 * np.pi * note(m) * t) for m in (74, 78, 81, 86)); return s * np.minimum(1, t / 1.3) * np.minimum(1, (d - t) / 1.8)
menor = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 55, 58, 62], [45, 52, 57, 61]]
mayor = [[50, 57, 62, 66], [43, 55, 59, 62], [45, 52, 57, 61], [50, 57, 62, 66]]
arp = [1, 2, 3, 2]
for ci in range(len(caps) - 1):
    a, b = caps[ci], caps[ci + 1]; claro = a + (b - a) * .66; tr = (ci * 2) % 5 - 2       # cada capítulo, un poco transpuesto
    add(soplo(), max(0, a - .6), 0, .12)
    if ci: add(trueno(), a, 0, .18)
    t0 = a
    while t0 < b:
        br = t0 >= claro; c = (mayor if br else menor)[int((t0 - a) / 4) % 4]; c = [m + tr for m in c]
        d = min(4.0, b - t0) + 1.2
        add(pad([note(c[0] - 12), note(c[0]), note(c[1])], d), t0, 0, .15 if br else .19)
        for k in range(4):
            if t0 + k > b: break
            add(lira(note(c[arp[k]] + 12)), t0 + k, .3 if k % 2 else -.3, .07 if br else .05)
            if not br and k in (0, 2): add(latido(), t0 + k, 0, .16)
        t0 += 4.0
    if b - a > 20: add(brillo(), claro, 0, .03)
for t in info.get('temblores', []):
    add(tension(), t - 2.0, 0, .04); add(trueno(), t, 0, .26)
fade = int(2 * sr); out[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]; out[:int(.5 * sr)] *= np.linspace(0, 1, int(.5 * sr), dtype=np.float32)[:, None]
out *= .5 / np.max(np.abs(out))
wf.write('musica.wav', sr, (out * 32767).astype(np.int16))
print('musica.wav', round(dur, 1), 's,', len(caps) - 1, 'capítulos')

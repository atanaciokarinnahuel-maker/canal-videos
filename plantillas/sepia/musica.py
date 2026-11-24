#!/usr/bin/env python3
"""Música de la plantilla sepia: lira y colchón grave, lenta y con suspenso (60 pulsos por minuto).
Antes del cumplimiento: nota grave sostenida, latido suave y una tensión que crece antes de cada
escena clave. 
Empieza en modo menor y pasa a mayor cuando aparece la escena de la cruz (el cumplimiento).
Lee info.json (escenas y sello) que deja render.js. Escribe musica.wav.
La voz se mezcla después y la música baja sola cuando alguien habla."""
import json
import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf

sr = 44100
info = json.load(open('info.json')); dur = info['dur']; n = int(dur * sr)
out = np.zeros((n, 2)); rng = np.random.default_rng(7)
cortes = [e[1] for e in info['escenas'] if e[1] > 0]
claro = next((e[1] for e in info['escenas'] if e[0] in ('cruz', 'nombre', 'tumba')), dur * .75)
sello = info.get('sello')

def add(sig, t, pan=0.0, g=1.0):
    i = int(t * sr)
    if i >= n or i < 0: return
    j = min(n, i + len(sig)); l = np.sqrt(.5 * (1 - pan)); r = np.sqrt(.5 * (1 + pan))
    out[i:j, 0] += sig[:j - i] * g * l; out[i:j, 1] += sig[:j - i] * g * r
note = lambda m: 440 * 2 ** ((m - 69) / 12)
T = lambda d: np.arange(int(d * sr)) / sr
def lp(x, fc, o=2):
    b, a = sg.butter(o, fc / (sr / 2)); return sg.lfilter(b, a, x)
def pad(fs, d):
    t = T(d); s = sum(np.sin(2 * np.pi * f * t) * .5 + np.sin(2 * np.pi * f * 1.004 * t) * .35 + sg.sawtooth(2 * np.pi * f * .998 * t) * .12 for f in fs)
    return lp(s, 1100) * np.minimum(1, t / 1.3) * np.minimum(1, (d - t) / 1.4)
def lira(f, d=2.2):
    t = T(d); s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.0) + .45 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3.4) + .2 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 5.5)
    return s * np.minimum(1, t * 350)
def tambor():
    t = T(.9); return np.sin(2 * np.pi * np.cumsum(46 + 60 * np.exp(-t * 22)) / sr) * np.exp(-t * 5.5) + lp(rng.standard_normal(len(t)), 700) * np.exp(-t * 16) * .35
def soplo(d=.9):
    t = T(d); s = lp(rng.standard_normal(len(t)), 2400); return s * np.exp(-((t - d * .45) / (d * .22)) ** 2)
def brillo(d=3.2):
    t = T(d); s = sum(np.sin(2 * np.pi * note(m) * t) for m in (74, 78, 81, 86)); return s * np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.6)
def golpe_sello():
    t = T(.7); return np.sin(2 * np.pi * np.cumsum(60 + 150 * np.exp(-t * 30)) / sr) * np.exp(-t * 7) + lp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 28) * .7

def latido():
    t = T(.5); return np.sin(2 * np.pi * np.cumsum(42 + 40 * np.exp(-t * 30)) / sr) * np.exp(-t * 9)
def tension(d=2.2):
    t = T(d); s = np.sin(2 * np.pi * note(69) * t) + np.sin(2 * np.pi * note(70) * t) + .6 * np.sin(2 * np.pi * note(81.5) * t)
    trem = .6 + .4 * np.sin(2 * np.pi * 9 * t); nz = lp(rng.standard_normal(len(t)), 5000) * .25
    return (s * trem + nz) * (t / d) ** 2.2
def trueno():
    t = T(1.6); return np.sin(2 * np.pi * np.cumsum(38 + 50 * np.exp(-t * 10)) / sr) * np.exp(-t * 3.2) + lp(rng.standard_normal(len(t)), 500) * np.exp(-t * 6) * .5
claves = [e[1] for e in info['escenas'] if e[0] in ('serpiente', 'talon', 'pieles', 'cordero', 'altares', 'cruz', 'puerta', 'altar', 'calle', 'carga', 'llamado', 'carnero') and e[1] > 1]
compas = 4.0
menor = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 55, 58, 62], [45, 52, 57, 61]]      # Re m, Si b, Sol m, La
mayor = [[50, 57, 62, 66], [43, 55, 59, 62], [45, 52, 57, 61], [50, 57, 62, 66]]      # Re, Sol, La, Re
arp = [1, 2, 3, 2, 3, 2, 1, 3]
for b in range(int(dur / compas) + 1):
    t0 = b * compas; br = t0 + compas * .5 >= claro
    c = (mayor if br else menor)[b % 4]
    add(pad([note(c[0] - 12), note(c[0]), note(c[1])], compas + 1.2), t0, 0, .16 if br else .2)
    add(pad([note(m) for m in c[2:]], compas + 1.2), t0, 0, .07 if br else .04)
    for k in range(8):
        if t0 + k * .5 < .4: continue
        if not br and k % 2: continue                                  # antes del cumplimiento, la lira va más espaciada
        add(lira(note(c[arp[k]] + 12)), t0 + k * .5, .3 if k % 2 else -.3, .085 if br else .06)
    if not br:
        for k in (0, 2): add(latido(), t0 + k, 0, .2); add(latido(), t0 + k + .34, 0, .13)
    if b % 2 == 0: add(lira(note(c[0] + 12), 3.0), t0, 0, .09)
for t in cortes:
    add(soplo(), t - .45, 0, .10); add(tambor(), t, 0, .22)
for t in claves:
    add(tension(), t - 2.2, 0, .045); add(trueno(), t, 0, .3)
add(brillo(), max(0, claro - .4), 0, .035)
if sello is not None: add(tension(1.8), sello - 1.8, 0, .05); add(golpe_sello(), sello, 0, .5); add(brillo(2.4), sello, 0, .03)
fade = int(1.0 * sr); out[-fade:] *= np.linspace(1, 0, fade)[:, None]; out[:int(.15 * sr)] *= np.linspace(0, 1, int(.15 * sr))[:, None]
out *= .5 / np.max(np.abs(out))
wf.write('musica.wav', sr, (out * 32767).astype(np.int16))
print('musica.wav', round(dur, 2), 's; cambia a mayor en', round(claro, 2), 's')

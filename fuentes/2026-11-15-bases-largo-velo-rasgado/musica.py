#!/usr/bin/env python3
"""Banda sonora sintetizada (numpy, sin samples) para el largo «El velo rasgado».
Lee cues.json (tiempos reales de la locución) y escribe remotion/public/musica.wav.
Uso: python3 musica.py"""
import json, wave
import numpy as np

SR = 44100
c = json.load(open('cues.json'))
DUR = c['DUR']; B = c['B']; A = c['A']; K = c['K']; X = c['X']; REVEAL = c['REVEAL']
N = int(SR * DUR)
L = np.zeros(N, np.float32); R = np.zeros(N, np.float32)
rng = np.random.default_rng(7)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def add(t0, sig, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i + len(sig) <= 0: return
    a = max(0, -i); i = max(0, i); n = min(len(sig) - a, N - i)
    s = sig[a:a + n] * gain
    L[i:i + n] += s * (1 - max(0, pan)); R[i:i + n] += s * (1 - max(0, -pan))

def env(n, a, r):
    e = np.ones(n, np.float32); na = min(n, int(a * SR)); nr = min(n, int(r * SR))
    if na: e[:na] = np.linspace(0, 1, na) ** 1.5
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e

# ───────── 1) Pads: progresión de acordes por secciones ─────────
Dm = [26, 38, 45, 53]; Bb = [34, 41, 50, 58]; F = [29, 41, 48, 57]; Gm = [31, 43, 50, 58]; Eb = [27, 39, 46, 55]
Aph = [33, 45, 52, 57]; A7 = [33, 45, 52, 61]; Flamb = [29, 41, 48, 57, 60]; low = [26, 38]; Dten = [26, 38, 45, 53, 57]
D = [26, 38, 45, 54, 57, 62]; Bm = [35, 42, 47, 50, 54]; G = [31, 43, 50, 55, 59]; Am = [33, 45, 52, 57, 61]; Asus = [33, 45, 52, 57, 62]
Dfull = [26, 38, 45, 50, 54, 57, 62, 66, 69]; G6 = [31, 43, 50, 55, 59, 62]
SEC = [
    (0, Dm, .8), (B[1] - .5, Bb, .8), (X['ark'], F, .85), (X['veil1'], Dm, .85),
    (B[2] - .5, Gm, .8), (X['gen'], Eb, .9), (X['veil2'], Dm, .85),
    (B[3] - .5, Aph, .8), (X['goat'], F, .7), (X['out'], Dm, .85),
    (B[4] - .4, Gm, .8), (X['spirit'], Dm, .85), (X['better'], A7, .95),
    (B[5] - .4, Flamb, .75), (X['jer'], low, 1.0), (X['instant'], [26], .9), (A['tear0'], Dten, 1.0), (A['godTore'], D, 1.05),
    (B[6] - .4, Bm, .85), (X['isa'], G, .85), (X['peter'], Am, .9), (X['own'], Bm, .9), (X['heb'], G, .95), (X['tore'], Asus, 1.0),
    (B[7] - .4, Asus, 1.05), (REVEAL, Dfull, 1.15), (X['place'], G6, .95), (X['via'], D, 1.0), (X['one'], Bm, .95),
    (B[8] - .4, G, .95), (X['blood8'], Am, 1.0), (X['so'], D, 1.0), (X['ask'], Asus, .95), (X['sub'], Dfull, 1.1), (DUR, None, 0),
]
XF = 1.6
for (t0, notes, lv), (t1, _, _) in zip(SEC[:-1], SEC[1:]):
    a = max(0, t0 - XF / 2); b = min(DUR, t1 + XF / 2); n = int((b - a) * SR)
    t = np.arange(n, dtype=np.float32) / SR
    e = env(n, XF, XF) * lv
    for k, m in enumerate(notes):
        f = hz(m); g = (0.55 if m < 36 else 0.3 if m < 48 else 0.17 if m < 60 else 0.085)
        for det, pan in ((-0.003, -0.35), (0.003, 0.35)):
            ph = rng.uniform(0, 6.28)
            vib = 1 + det + 0.0012 * np.sin(6.283 * 0.17 * t + m)
            x = np.sin(6.283 * f * vib * t + ph) + 0.35 * np.sin(2 * 6.283 * f * vib * t + ph * 2) + (0.12 * np.sin(3 * 6.283 * f * vib * t) if m < 60 else 0)
            trem = 1 + 0.12 * np.sin(6.283 * (0.09 + 0.013 * k) * t + k)
            add(a, (x * e * trem).astype(np.float32), g * 0.5, pan * (0.4 if m < 40 else 1))

# ───────── 2) Pulso: arpegio suave que da avance (se apaga en las tinieblas) ─────────
def level(t):
    pts = [(0, 0), (X['stay'], .0), (X['stay'] + 3, .35), (B[1], .5), (B[2], .32), (X['gen'], .22), (X['veil2'], .34), (B[3], .3), (X['blood'], .12), (X['goat'], .22), (X['out'], .3),
           (B[4], .6), (X['spirit'], .3), (B[5], .28), (X['jer'], .1), (K['dark'], 0), (A['tear0'], 0), (A['tear1'], .3), (A['godTore'], .55), (B[6], .42), (X['heb'], .5),
           (B[7], .55), (REVEAL, .8), (X['place'], .6), (B[8], .5), (X['so'], .62), (X['sub'], .5), (DUR - 2, 0)]
    ts = [p[0] for p in pts]; vs = [p[1] for p in pts]
    return float(np.interp(t, ts, vs))
def chord(t):
    cur = SEC[0][1]
    for t0, notes, _ in SEC:
        if notes is not None and t0 <= t: cur = notes
    return cur
STEPT = 0.3
pl = int(0.9 * SR); tp = np.arange(pl, dtype=np.float32) / SR
k = 0; t = 1.0
PAT = [0, 2, 1, 3, 2, 1, 3, 2]
while t < DUR - 1:
    lv = level(t)
    if lv > 0.01:
        ch = [m for m in chord(t) if m >= 45] or chord(t)
        m = ch[PAT[k % 8] % len(ch)] + 12
        f = hz(m)
        x = (np.sin(6.283 * f * tp) + 0.3 * np.sin(6.283 * 2 * f * tp)) * np.exp(-tp * (5.5 if k % 2 else 4.2)) * np.minimum(1, tp * 400)
        add(t, x.astype(np.float32), 0.075 * lv * (1.0 if k % 4 == 0 else 0.7), ((k % 4) - 1.5) * 0.3)
    k += 1; t += STEPT

# ───────── 3) Efectos alineados a los golpes visuales ─────────
def noise(n): return rng.standard_normal(n).astype(np.float32)
def bandnoise(n, f0, f1, q=1.2):
    x = noise(n); out = np.zeros(n, np.float32); lp = 0.0; bp = 0.0
    fc = np.linspace(f0, f1, n); g = 2 * np.sin(np.pi * np.minimum(fc, SR * 0.2) / SR)
    for i in range(n):
        hp = x[i] - lp - q * bp; bp += g[i] * hp; lp += g[i] * bp; out[i] = bp
    return out
def whoosh(d=0.7, f0=400, f1=2600):
    n = int(d * SR); x = noise(n)
    # paso-banda barato: diferencia de dos medias móviles
    k1 = 9; k2 = 61
    y = np.convolve(x, np.ones(k1) / k1, 'same') - np.convolve(x, np.ones(k2) / k2, 'same')
    return (y * np.sin(np.linspace(0, np.pi, n)) ** 2).astype(np.float32)
def boom(f0=95, f1=34, d=2.6, drop=7.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * drop)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6) * np.minimum(1, t * 300)).astype(np.float32)
def bell(m, d=2.6, bright=1.0):
    n = int(d * SR); t = np.arange(n) / SR; f = hz(m)
    x = np.sin(6.283 * f * t) * np.exp(-t * 1.6) + 0.5 * bright * np.sin(6.283 * f * 2.76 * t) * np.exp(-t * 3.2) + 0.25 * bright * np.sin(6.283 * f * 5.4 * t) * np.exp(-t * 5)
    return (x * np.minimum(1, t * 500)).astype(np.float32)
def thump(d=0.35, f=62):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(6.283 * (f * t + 14 * (1 - np.exp(-t * 30)) / 30)) * np.exp(-t * 13)).astype(np.float32)
def tick(d=0.09, f=2200):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(6.283 * f * t) * np.exp(-t * 60)).astype(np.float32)

W_SOFT = whoosh(0.6); TH = thump(); TK = tick()
# cambios de set: aire suave
for i, t in enumerate(c['sets']): add(t - 0.22, W_SOFT, 0.11, (-1) ** i * 0.35)
# títulos grandes: golpe grave + clic
for t, size, col in c['keys']:
    g = min(1.0, size / 170)
    add(t - 0.02, TH, 0.26 * g + 0.08); add(t, TK, 0.03 + 0.02 * g, 0.2)
    if col == 'crimson': add(t, thump(0.5, 48), 0.3)
for t in c['strikes']: add(t + 0.35, whoosh(0.28), 0.16); add(t + 0.5, tick(0.06, 900), 0.06)
for t in c['quotes']: add(t, bell(74, 2.2, 0.6), 0.07, -0.2); add(t + 0.12, bell(81, 2.2, 0.6), 0.05, 0.2)
# cada capítulo enciende una llama: campana de dos notas que sube
SCALE = [62, 64, 66, 69, 71, 74, 78]
for i in range(1, 8):
    t = B[i] - 0.3
    add(t - 0.55, whoosh(0.7), 0.2)
    add(t, bell(SCALE[i - 1], 3.0), 0.16, -0.25); add(t + 0.16, bell(SCALE[i - 1] + 7, 3.0), 0.11, 0.25)
# gancho: dos destellos de la rasgadura
for t in (X['flash1'], X['flash2']): add(t, boom(80, 40, 1.4, 9), 0.42); add(t, whoosh(0.5), 0.25)
# la espada encendida
add(X['sword'] - 0.2, whoosh(1.4), 0.3)
# "para que no mueras": latidos
hb = thump(0.5, 50)
for q in range(8):
    t = A['warn'] + q * 0.62
    if t < A['warnEnd']: add(t, hb, 0.5); add(t + 0.2, hb, 0.34)
# el velo se cierra otra vez: portazo
add(A['closeAgain'] + 0.55, boom(70, 30, 1.8, 10), 0.6); add(A['closeAgain'] + 0.55, whoosh(0.25), 0.3)
# "Pero espera": corte en seco (subida al revés + golpe)
rev = whoosh(0.9)[::-1].copy(); add(B[4] - 0.85, rev * np.linspace(0, 1, len(rev)).astype(np.float32) ** 2, 0.5); add(B[4] + 0.02, boom(110, 40, 1.2, 12), 0.5)
# rueda de los años: tic-tac que acelera
t = c['W']['in']
while t < c['W']['still']:
    sp = 0.45 if t < c['W']['each'] else 0.16
    add(t, TK, 0.07, 0.3 if int(t / sp) % 2 else -0.3); t += sp
# tinieblas: rumor grave
n = int((K['instant'] - K['dark']) * SR); tt = np.arange(n) / SR
rum = (np.sin(6.283 * 31 * tt) * (1 + 0.5 * np.sin(6.283 * 0.4 * tt)) + 0.4 * np.sin(6.283 * 46.5 * tt)) * env(n, 2.5, 1.2)
add(K['dark'], rum.astype(np.float32), 0.34)
# "Consumado es": golpe y silencio
add(K['done'], boom(100, 32, 3.2, 6), 0.75); add(K['done'], bell(50, 3.5, 0.3), 0.2)
# LA RASGADURA: impacto + desgarro que cae de arriba abajo
add(A['tear0'], boom(120, 30, 3.6, 6), 0.95)
ln = A['tear1'] - A['tear0'] + 0.4
rip = bandnoise(int(ln * SR), 5200, 260)
tr = np.arange(len(rip)) / SR
rip *= (np.exp(-tr * 1.5) * 0.6 + 0.16) * (0.6 + 0.4 * np.abs(np.sin(tr * 47))) * env(len(rip), 0.01, 0.5)
add(A['tear0'], rip, 0.5, -0.2); add(A['tear0'] + 0.01, rip, 0.4, 0.3)
# "Lo rasgó Dios"
add(A['godTore'], boom(110, 36, 3.0, 6), 0.8); add(A['godTore'], whoosh(1.2), 0.3)
for m in (62, 66, 69): add(A['godTore'] + 0.05, bell(m, 3.5), 0.09)
# vuelo a través del velo y REVELACIÓN: el trono de la gracia
sw = whoosh(3.2); add(B[7] + 0.4, sw, 0.3)
add(REVEAL - 1.3, (whoosh(1.4)[::-1] * np.linspace(0, 1, int(1.4 * SR)) ** 2).astype(np.float32), 0.5)
add(REVEAL, boom(90, 37, 4.0, 5), 0.7)
for q, m in enumerate((62, 66, 69, 74, 78, 81)): add(REVEAL + q * 0.09, bell(m, 4.5), 0.12, (q % 3 - 1) * 0.4)
# "Cree. Acércate. Hoy." y final
for q, m in enumerate((74, 78, 81)): add(A['walk'] + q * 0.9, bell(m, 2.5), 0.1)
for q, m in enumerate((62, 69, 74, 78)): add(X['sub'] + q * 0.12, bell(m, 5), 0.11, (q % 2 - .5) * 0.5)

# ───────── 4) Espacio (reverb por convolución) y nivel ─────────
ir_n = int(2.4 * SR); ti = np.arange(ir_n) / SR
def reverb(x, seed):
    ir = np.random.default_rng(seed).standard_normal(ir_n).astype(np.float32) * np.exp(-ti * 2.6).astype(np.float32)
    ir = np.convolve(ir, np.ones(5) / 5, 'same'); ir /= np.sqrt((ir ** 2).sum())
    n = len(x) + ir_n; nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(ir, nf), nf)[:len(x)].astype(np.float32)
wl = reverb(L, 1); wr = reverb(R, 2)
L = L + 0.24 * wl + 0.08 * wr; R = R + 0.24 * wr + 0.08 * wl
fade = np.ones(N, np.float32); nf = int(2.6 * SR); fade[-nf:] = np.linspace(1, 0, nf) ** 1.5; fade[:int(1.0 * SR)] = np.linspace(0, 1, int(1.0 * SR))
L *= fade; R *= fade
rms = np.sqrt(np.mean((L ** 2 + R ** 2) / 2)); g = 10 ** (-17.5 / 20) / rms
out = np.tanh(np.stack([L, R], 1) * g * 1.05) / 1.05
pk = np.abs(out).max(); out = out / max(1.0, pk / 0.94)
w = wave.open('remotion/public/musica.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print('musica.wav', round(DUR, 1), 's  rms', round(20 * np.log10(np.sqrt(np.mean(out ** 2))), 1), 'dB  pico', round(float(np.abs(out).max()), 2))

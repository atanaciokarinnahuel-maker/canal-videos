# Música + efectos (sin voz) para la invitación a la Conferencia Misionera.
# Uso: python3 musica.py <salida.wav>   (lee info.json que deja render.js)
import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
I = json.load(open(os.path.join(HERE, 'info.json')))
sr = 44100; dur = I['DUR'] + 0.4; n = int(dur * sr); out = np.zeros((n, 2)); rng = np.random.default_rng(21)
T_C0, SEG, T_MID, T_ARC, T_IMP, T_FIN = I['T_C0'], I['SEG'], I['T_MID'], I['T_ARC'], I['T_IMP'], I['T_FIN']

def add(sig, t, pan=0.0, g=1.0):
    i = int(t * sr)
    if i >= n or i < 0: return
    j = min(n, i + len(sig)); l = np.sqrt(0.5 * (1 - pan)); r = np.sqrt(0.5 * (1 + pan))
    out[i:j, 0] += sig[:j - i] * g * l; out[i:j, 1] += sig[:j - i] * g * r
def note(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, fc, o=2):
    b, a = sg.butter(o, min(0.99, fc / (sr / 2))); return sg.lfilter(b, a, x)
def hp(x, fc, o=2):
    b, a = sg.butter(o, fc / (sr / 2), 'high'); return sg.lfilter(b, a, x)
def T(d): return np.arange(int(d * sr)) / sr
def pluck(f, d=0.22):
    t = T(d); s = (sg.sawtooth(2 * np.pi * f * t) * 0.5 + sg.square(2 * np.pi * f * t, 0.35) * 0.3) * np.exp(-t * 16); return lp(s, 4200) * np.minimum(1, t * 500)
def bell(f, d=0.9):
    t = T(d); return (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 6) + 0.18 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 9)) * np.exp(-t * 4) * np.minimum(1, t * 600)
def bass(f, d):
    t = T(d); s = sg.sawtooth(2 * np.pi * f * t) * 0.5 + np.sin(2 * np.pi * f * t); return lp(s, 500) * np.exp(-t * 4) * np.minimum(1, t * 250)
def kick(p=1.0):
    t = T(0.32); return np.sin(2 * np.pi * np.cumsum(48 + 130 * np.exp(-t * 28)) / sr) * np.exp(-t * 10) * p
def clap():
    t = T(0.22); s = rng.standard_normal(len(t)); b, a = sg.butter(2, [1000 / (sr / 2), 6000 / (sr / 2)], 'band'); e = np.exp(-t * 26) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012)
    return sg.lfilter(b, a, s) * e
def hat(o=False):
    t = T(0.14 if o else 0.05); return hp(rng.standard_normal(len(t)), 8000) * np.exp(-t * (22 if o else 85))
def snare():
    t = T(0.16); return hp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 28) * 0.8 + np.sin(2 * np.pi * 185 * t) * np.exp(-t * 24) * 0.5
def tom(f=90):
    t = T(0.5); return np.sin(2 * np.pi * np.cumsum(f + f * 0.9 * np.exp(-t * 20)) / sr) * np.exp(-t * 7)
def pad(fs, d, fc=1700):
    t = T(d); s = sum(sg.sawtooth(2 * np.pi * f * t) * 0.2 + sg.sawtooth(2 * np.pi * f * 1.004 * t) * 0.2 + np.sin(2 * np.pi * f * t) * 0.3 for f in fs)
    return lp(s, fc) * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.35)
def stab(fs, d=0.55, fc=3200):
    t = T(d); s = sum(sg.sawtooth(2 * np.pi * f * t) * 0.3 + sg.sawtooth(2 * np.pi * f * 0.996 * t) * 0.3 for f in fs)
    return lp(s, fc) * np.exp(-t * 5.5) * np.minimum(1, t * 300)
def whoosh(d=0.6):
    t = T(d); s = rng.standard_normal(len(t)); o = np.zeros_like(s)
    for k in range(6):
        lo = 300 + k * 750; b, a = sg.butter(2, [lo / (sr / 2), (lo + 650) / (sr / 2)], 'band'); o += sg.lfilter(b, a, s) * np.exp(-((t - (0.1 + k * 0.07) * d / 0.6) / (0.09 * d / 0.6)) ** 2)
    return o / np.max(np.abs(o))
def pop(f=700):
    t = T(0.12); return np.sin(2 * np.pi * np.cumsum(f * 0.6 + f * np.exp(-t * 40)) / sr) * np.exp(-t * 34)
def boom(d=1.6):
    t = T(d); nz = lp(rng.standard_normal(len(t)), 2200) * np.exp(-t * 6); th = np.sin(2 * np.pi * np.cumsum(38 + 120 * np.exp(-t * 14)) / sr) * np.exp(-t * 3.2); return nz * 0.55 + th * 1.3
def crash(d=2.6):
    t = T(d); return hp(rng.standard_normal(len(t)), 4500) * np.exp(-t * 1.9) * np.minimum(1, t * 300)
def riser(d, f0=180, f1=1900):
    t = T(d); fr = f0 * (f1 / f0) ** (t / d); s = sg.sawtooth(2 * np.pi * np.cumsum(fr) / sr) * 0.35 + rng.standard_normal(len(t)) * 0.3; return lp(s, 6500) * (t / d) ** 1.8
def blip(f, d=0.09):
    t = T(d); return sg.square(2 * np.pi * f * t) * 0.3 * np.exp(-t * 28)

beat = 0.5
# ---------------- INTRO (0–6): cortina de noticiero ----------------
add(boom(1.2), 0.2, 0, 0.55); add(stab([note(m) for m in (38, 50, 57, 62, 65)], 1.4), 0.2, 0, 0.16); add(crash(1.4), 0.2, 0, 0.05)
add(pad([note(26), note(38)], 6.2, 500), 0, 0, 0.22)
for k, t in enumerate(np.arange(2.0, 5.5, 0.25)): add(blip(1760 if k % 4 else 2349, 0.05), t, 0.3 if k % 2 else -0.3, 0.035)
for t, ch, g in [(2.05, (50, 57, 62), .09), (2.45, (50, 57, 62), .09), (2.9, (50, 57, 62, 65), .15), (3.25, (55, 58, 62, 67), .16), (3.6, (57, 61, 64, 69, 76), .2), (4.4, (62, 69, 74, 77), .13)]:
    add(stab([note(m) for m in ch], 0.7), t, 0, g); add(tom(80 if t < 3.6 else 62), t, 0, 0.22 if t >= 2.9 else 0.1)
add(bell(note(86), 1.2), 4.4, 0.2, 0.06); add(riser(1.0), 5.0, 0, 0.07); add(whoosh(0.7), 5.45, 0, 0.14)

# ---------------- cama rítmica: vista general + países ----------------
ROOTS = [38, 41, 43, 45, 46]                      # Re m, Fa, Sol m, La, Si♭ (un color por país)
CH = [(62, 65, 69), (60, 65, 69), (62, 67, 70), (61, 64, 69), (62, 65, 70)]
OST = [0, 0, 1, 0, 2, 0, 1, 0]
def bar_block(t0, t1, root, ch, drums=1.0, level=1.0, start_skip=0.0):
    k = 0; t = t0
    while t < t1 - 1e-6:
        b = k % 8
        if k % 8 == 0: add(pad([note(m - 12) for m in ch], min(4 * beat, t1 - t)), t, 0, 0.075 * level)
        add(pluck(note(ch[OST[b]] + (12 if b in (4, 6) else 0))), t, 0.3 if k % 2 else -0.3, 0.055 * level)
        if t - t0 >= start_skip:
            add(bass(note(root), beat * 0.46), t, 0, 0.2 * level)
            if b % 2 == 0: add(kick(), t, 0, 0.3 * drums)
            else: add(hat(b == 7), t, 0.25, 0.05 * drums)
            if b in (2, 6): add(clap(), t, 0, 0.08 * drums)
        k += 1; t += beat / 2
bar_block(6.0, 12.0, 38, CH[0], drums=0.55, level=0.9, start_skip=1.0)
for i, t in enumerate(I['PIN_T']):                 # pines: tonos que suben
    add(pop(500 + i * 90), t + .3, 0, 0.3); add(bell(note([74, 77, 81, 84, 86][i]), 0.7), t + .3, [-.5, 0, .1, .3, .6][i], 0.09)
add(stab([note(m) for m in (50, 56, 62, 68)], 1.5, 2000), I['T_MEET'], 0, 0.12); add(tom(55), I['T_MEET'], 0, 0.3)   # "¿dónde?"
add(riser(1.2), 10.8, 0, 0.07)

SFX = {'red': lambda t: (add(stab([note(m) for m in (38, 50, 51)], 0.5, 1500), t, 0, 0.2), add(stab([note(m) for m in (37, 49, 50)], 0.7, 1500), t + 0.17, 0, 0.2), add(tom(58), t, 0, 0.28)),
       'green': lambda t: [add(bell(note(m), 0.7), t + k * 0.09, 0.3, 0.09) for k, m in enumerate((74, 78, 81, 86))],
       'blue': lambda t: (add(blip(1175, 0.08), t, -0.2, 0.09), add(blip(1568, 0.1), t + 0.1, 0.2, 0.09)),
       'gold': lambda t: [add(bell(note(m), 1.1), t + k * 0.11, -0.3 + k * 0.2, 0.085) for k, m in enumerate((69, 74, 78, 81))] + [add(crash(1.0), t, 0, 0.02)]}
for i in range(5):
    t0 = T_C0 + SEG * i; root, ch = ROOTS[i], CH[i]
    add(whoosh(1.1), t0 - 0.1, 0.5 if i % 2 else -0.5, 0.2); add(riser(0.9, 300, 1400), t0, 0, 0.045)
    add(tom(70), t0 + 0.85, 0, 0.34); add(stab([note(m - 12) for m in ch] + [note(root)], 0.9, 2400), t0 + 0.85, 0, 0.15)   # título del país
    add(pop(900), t0 + 1.6, 0.3, 0.22)                                                                                     # pin de la capital
    bar_block(t0 + 1.0, t0 + SEG - 1.0, root, ch, drums=1.0, level=1.0, start_skip=1.0)
    for k in range(4): add(snare(), t0 + SEG - 1.0 + k * 0.25, 0, 0.07 + k * 0.03)                                         # redoble de salida
    add(pop(1200), t0 + SEG, 0, 0.2); add(bell(note(86), 0.6), t0 + SEG, 0.4, 0.07)                                        # ✓ en el rastreador
for c in I['cards']:
    add(whoosh(0.3), c['t'] - 0.05, -0.4, 0.07); SFX[c['c']](c['t'] + 0.04)

# ---------------- 5 naciones → un solo destino (87–93) ----------------
add(whoosh(1.2), T_MID - 0.1, 0, 0.2); add(pad([note(m) for m in (38, 45, 50, 55)], 2.2, 1200), T_MID, 0, 0.12)
add(tom(58), T_MID + 0.9, 0, 0.36); add(stab([note(m) for m in (38, 50, 57, 62)], 1.0), T_MID + 0.9, 0, 0.16)
add(riser(T_IMP - T_ARC - 0.05, 120, 2600), T_ARC, 0, 0.16); add(pad([note(26), note(38), note(45)], 4.0, 700), T_ARC, 0, 0.2)
t = T_ARC; step = 0.5
while t < T_IMP - 0.1:                                 # latido que se acelera
    add(kick(), t, 0, 0.3); t += step; step = max(0.11, step * 0.9)
for k, t in enumerate(np.arange(T_IMP - 1.5, T_IMP - 0.05, 0.0625)): add(snare(), t, 0, 0.03 + 0.006 * k)
for k, t in enumerate(sorted(I['ARC_T'])):             # salida de cada arco
    add(whoosh(0.8), t, [0.7, 0.4, 0.1, -0.2, -0.6][k], 0.17); add(bell(note([62, 66, 69, 74, 78][k]), 1.0), t, 0, 0.1)

# ---------------- ¡PUM! + himno final (93–109) ----------------
add(boom(2.4), T_IMP, 0, 0.95); add(boom(1.2), T_IMP + 0.02, 0, 0.4); add(crash(3.2), T_IMP, 0, 0.13)
add(stab([note(m) for m in (38, 50, 57, 62, 66, 69, 74)], 2.2, 4200), T_IMP, 0, 0.2)
PROG = [(38, (62, 66, 69)), (45, (61, 64, 69)), (47, (62, 66, 71)), (43, (62, 67, 71)), (38, (62, 66, 69)), (45, (61, 64, 69)), (43, (62, 67, 71)), (38, (62, 66, 69))]
MEL = [(78, 81, 86, 81), (76, 81, 85, 81), (78, 83, 86, 83), (79, 83, 86, 91), (78, 81, 86, 90), (76, 81, 85, 88), (79, 83, 86, 91), (86,)]
for b_, (root, ch) in enumerate(PROG):
    t0 = T_IMP + b_ * 2.0; last = b_ == len(PROG) - 1; d = 2.4 if last else 2.0
    add(pad([note(m) for m in ch] + [note(ch[0] - 12)], d, 2600), t0, 0, 0.11)
    if b_: add(stab([note(m) for m in ch] + [note(root + 12)], 0.8, 3600), t0, 0, 0.12 if not last else 0.2)
    if last:
        add(boom(1.6), t0, 0, 0.5); add(crash(2.4), t0, 0, 0.09); add(bass(note(root), 2.0), t0, 0, 0.26); add(bell(note(86), 2.0), t0, 0, 0.1); add(bell(note(90), 2.0), t0 + .12, 0.3, 0.08); break
    for k in range(8):
        tt = t0 + k * beat / 2
        add(bass(note(root), beat * 0.46), tt, 0, 0.2); add(pluck(note(ch[OST[k]] + 12)), tt, 0.3 if k % 2 else -0.3, 0.05)
        if b_ >= 1:
            if k % 2 == 0: add(kick(), tt, 0, 0.33)
            add(hat(k == 7), tt, 0.25 if k % 2 else -0.25, 0.04 if k % 2 == 0 else 0.055)
            if k in (2, 6): add(clap(), tt, 0, 0.11)
    for k, m in enumerate(MEL[b_]): add(bell(note(m), 0.9), t0 + k * beat, 0.15, 0.1 if b_ >= 1 else 0.06)
for k, dt in enumerate([0, .3, 1.0, 1.75, 2.15, 2.9]):   # entradas del cartel final
    add(whoosh(0.35), T_FIN + dt - 0.05, -0.3, 0.09)
    if k == 2: add(tom(62), T_FIN + dt, 0, 0.3); add(pop(800), T_FIN + dt, 0, 0.25)

# ---------------- mezcla ----------------
out = hp(out.T, 28).T
fade = np.minimum(1, (dur - np.arange(n) / sr) / 0.9).clip(0, 1); out *= fade[:, None]
out = np.tanh(out * 1.35); out *= 0.92 / np.max(np.abs(out))
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'musica.wav')
wf.write(dst, sr, (out * 32767).astype(np.int16)); print(dst, round(dur, 2), 's  rms(dB)=', round(20 * np.log10(np.sqrt(np.mean(out ** 2))), 1))

#!/usr/bin/env python3
"""Alinea cada bloque de voz con su texto (silencios + sílabas, igual que los Shorts),
recorta pausas, aplica tempo y arma la voz final + words.json en tiempos de VIDEO.
Uso: python3 align.py  (desde fuentes/<id>/)"""
import re, json, subprocess, glob, os
TEMPO = 1.1
ID = os.path.basename(os.getcwd())
VOZ = f'../../insumos-voz/{ID}'
OUT = 'remotion/public'
START = 0.7          # aire antes de la primera palabra
GAP = {0: 1.15}      # pausa tras el gancho (tarjeta de capítulo); resto:
GAP_DEF = 0.95

def syl(w):
    w = re.sub(r'[^a-záéíóúüñ]', '', w.lower())
    g = re.findall(r'[aeiouáéíóúü]+', w); n = 0
    for x in g:
        n += 1
        if re.search(r'[aeo][áéíóú]|[áéíóú][aeo]|í[aeou]|ú[aeio]|[aeo]í|[aeo]ú|[aeo][aeo]', x): n += 1
    return max(1, n)

def run(*a): return subprocess.run(a, capture_output=True, text=True)

def align(audio, text):
    words = text.split()
    S = [syl(w) for w in words]
    ends = [bool(re.search(r'[.,:;…?!]$', w)) for w in words]
    sent = [bool(re.search(r'[.:;…?!]$', w)) for w in words]
    err = run('ffmpeg', '-v', 'info', '-i', audio, '-af', 'silencedetect=noise=-38dB:d=0.18', '-f', 'null', '-').stderr
    st = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', err)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    dur = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', audio).stdout)
    ivs = []; a = 0.0
    for k, s in enumerate(st):
        s = max(0.0, s)
        if s - a > 0.10: ivs.append((a, s))
        a = en[k] if k < len(en) else dur
    if dur - a > 0.10: ivs.append((a, dur))
    K, N = len(ivs), len(words)
    r = sum(b - a for a, b in ivs) / sum(S)
    INF = 1e18; cs = [0]
    for s in S: cs.append(cs[-1] + s)
    dp = [[INF] * (N + 1) for _ in range(K + 1)]; bk = [[0] * (N + 1) for _ in range(K + 1)]
    dp[0][0] = 0
    for k in range(1, K + 1):
        d = ivs[k - 1][1] - ivs[k - 1][0]
        for j in range(k, N + 1):
            for i in range(k - 1, j):
                if dp[k - 1][i] >= INF: continue
                c = (d - r * (cs[j] - cs[i])) ** 2
                if k < K and j < N and not ends[j - 1]: c += 0.35
                v = dp[k - 1][i] + c
                if v < dp[k][j]: dp[k][j] = v; bk[k][j] = i
    cuts = []; j = N
    for k in range(K, 0, -1):
        i = bk[k][j]; cuts.append((i, j)); j = i
    cuts = cuts[::-1]
    segs = []; W = []; cum = 0.0; rep = []
    for k, ((i, j), (a, b)) in enumerate(zip(cuts, ivs)):
        ta = max(0, a - 0.03); tb = min(dur, b + 0.04)
        tot = sum(S[m] + 0.6 for m in range(i, j)); t = a
        for m in range(i, j):
            w = (S[m] + 0.6) / tot * (b - a)
            W.append({'text': words[m], 'start': (cum + (t - ta)) / TEMPO, 'end': (cum + (t + w * 0.92 - ta)) / TEMPO}); t += w
        last = j - 1
        pad = 0 if k == K - 1 else (0.30 if sent[last] else 0.07)
        if k < K - 1 and words[last].endswith(':'): pad = 0.14
        if k < K - 1 and words[last].endswith('…'): pad = 0.42
        segs.append([round(ta, 3), round(tb, 3), pad]); cum += (tb - ta) + pad
        rep.append((round((b - a) / max(1, cs[j] - cs[i]), 3), ' '.join(words[i:j])))
    return W, segs, cum / TEMPO, rep

os.makedirs(OUT, exist_ok=True)
allw = []; blocks = []; t0 = START; parts = []; segs_all = {}
for bi, f in enumerate(sorted(glob.glob('bloques/*.txt'))):
    audio = f'{VOZ}/b{bi}.mp3'
    W, segs, d, rep = align(audio, open(f).read().strip())
    segs_all[f'b{bi}'] = segs
    fc = ';'.join(
        f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={max(0, b - a - 0.025):.3f}:d=0.025" + (f",apad=pad_dur={p}" if p > 0 else '') + f"[s{k}]"
        for k, (a, b, p) in enumerate(segs))
    fc += ';' + ''.join(f'[s{k}]' for k in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1,atempo={TEMPO},aresample=44100[v]"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', audio, '-filter_complex', fc, '-map', '[v]', '-ac', '1', f'/tmp/vb{bi}.wav'], check=True)
    real = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'/tmp/vb{bi}.wav').stdout)
    k = real / d if d else 1
    for w in W: allw.append({'text': w['text'], 'start': round(t0 + w['start'] * k, 3), 'end': round(t0 + w['end'] * k, 3), 'block': bi})
    blocks.append({'name': os.path.basename(f)[:-4], 'start': round(t0, 3), 'end': round(t0 + real, 3)})
    parts.append((t0, f'/tmp/vb{bi}.wav'))
    slow = [x for x in rep if x[0] > 0.30 or x[0] < 0.11]
    print(f'b{bi}: {len(W)} palabras, {len(segs)} tramos, {real:.2f}s  | sospechosos: {slow[:4]}')
    t0 += real + GAP.get(bi, GAP_DEF)
DUR = round(t0 - GAP_DEF + 7.0, 2)   # cola final: tarjeta de suscripción
ins = sum((['-i', p] for _, p in parts), [])
fc = ';'.join(f"[{i}:a]adelay={int(t * 1000)}:all=1[a{i}]" for i, (t, _) in enumerate(parts)) + ';' + ''.join(f'[a{i}]' for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0:duration=longest,apad=whole_dur={DUR}[o]"
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fc, '-map', '[o]', '-ar', '44100', '-ac', '1', f'{OUT}/voz.wav'], check=True)
json.dump({'words': allw, 'blocks': blocks, 'DUR': DUR, 'tempo': TEMPO}, open('words.json', 'w'), ensure_ascii=False)
json.dump({'words': allw, 'blocks': blocks, 'DUR': DUR}, open('remotion/src/words.json', 'w'), ensure_ascii=False)
json.dump(segs_all, open('segmentos.json', 'w'))
print('DUR video', DUR, 's =', int(DUR // 60), 'min', round(DUR % 60, 1), 's')
for b in blocks: print(b)

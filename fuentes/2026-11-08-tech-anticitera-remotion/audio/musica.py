import numpy as np, wave
SR = 44100
DUR = 53.6
n = int(SR * DUR)
t = np.arange(n) / SR
rng = np.random.default_rng(7)
L = np.zeros(n); R = np.zeros(n)

def add(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR)
    if i >= n: return
    sig = sig[: n - i] * gain
    L[i:i+len(sig)] += sig * (1 - max(0, pan)); R[i:i+len(sig)] += sig * (1 + min(0, pan))

def env(m, a=0.005, d=0.2):
    e = np.ones(m); na = max(1, int(a*SR)); e[:na] = np.linspace(0, 1, na)
    e *= np.exp(-np.arange(m)/SR/d); return e

def tone(f, dur, a=0.01, d=0.3, harm=(1,), amp=(1,)):
    m = int(dur*SR); tt = np.arange(m)/SR
    s = sum(a_*np.sin(2*np.pi*f*h*tt) for h, a_ in zip(harm, amp))
    return s*env(m, a, d)

def noise(dur, lp=None):
    m = int(dur*SR); x = rng.standard_normal(m)
    if lp:
        k = int(SR/lp); x = np.convolve(x, np.ones(k)/k, mode='same')
    return x

# ── Drone: La menor misterioso, evoluciona con las escenas
def pad(f, start, end, gain):
    i0, i1 = int(start*SR), min(n, int(end*SR)); tt = t[i0:i1]
    fade = np.minimum(1, np.minimum((tt-start)/1.5, (end-tt)/1.5))
    s = (np.sin(2*np.pi*f*tt) + 0.5*np.sin(2*np.pi*f*2.003*tt) + 0.25*np.sin(2*np.pi*f*3.01*tt)) * (0.7+0.3*np.sin(2*np.pi*0.13*tt))
    L[i0:i1] += s*fade*gain; R[i0:i1] += s*fade*gain*0.95
for (a, b, fs) in [(0,12.9,(55,82.4)),(12.6,29.7,(55,82.4,110)),(29.5,37.6,(51.9,77.8)),(37.4,44.6,(55,82.4,130.8)),(44.4,DUR,(55,82.4,110,164.8))]:
    for f in fs: pad(f, a, b, 0.07)

# ── Subgrave pulso tipo corazón desde 4.4
beat = 0.5
for k in np.arange(0.4, DUR-1, beat*2):
    if k > 4.3:
        add(tone(48, 0.45, a=0.005, d=0.12, harm=(1,2), amp=(1,0.3)), k, gain=0.28 if k < 44.5 else 0.38)

# ── Ticks de reloj/engranajes
for k in np.arange(18.8, 29.7, 0.25):
    add(noise(0.03, 4000)*env(int(0.03*SR), 0.001, 0.008)*0.9, k, pan=0.3*np.sin(k*3), gain=0.22)
for k in np.arange(2.0, 18.4, 0.5):
    add(noise(0.02, 3500)*env(int(0.02*SR), 0.001, 0.006), k, gain=0.12)

# ── Whoosh en cambios de escena
def whoosh(at, dur=0.7, up=True):
    m = int(dur*SR); x = noise(dur, 800)*np.hanning(m)
    sweep = np.sin(2*np.pi*(300 + (900 if up else -200)*np.linspace(0,1,m)**2)*np.arange(m)/SR)*0.25
    add((x*3+sweep)*np.hanning(m), at, gain=0.5)
for tt_ in [0.3, 4.3, 12.5, 18.3, 29.6, 37.3, 44.4]: whoosh(tt_)

# ── Burbujas bajo el agua
for k in np.arange(5.0, 12.5, 0.18):
    f = rng.uniform(500, 1400)
    add(tone(f, 0.08, a=0.002, d=0.03)*0.18, k, pan=rng.uniform(-0.6, 0.6))

# ── Golpes de aterrizaje de fragmentos (13–14.3) y cuenta
for k in np.arange(13.0, 14.2, 0.09):
    add(noise(0.03, 2500)*env(int(0.03*SR), 0.001, 0.01)*0.8, k, pan=rng.uniform(-0.5,0.5), gain=0.2)
for i, k in enumerate(np.linspace(15.2, 16.1, 12)):
    add(tone(600*2**(i/12), 0.12, a=0.002, d=0.07)*0.3, k)

# ── Luna / eclipse / Saros
add(tone(220, 1.0, a=0.2, d=0.9, harm=(1,2,3), amp=(1,0.4,0.2)), 22.0, gain=0.12)
for k in np.arange(27.2, 28.9, 0.045):
    add(tone(900, 0.03, a=0.001, d=0.012)*0.4, k, gain=0.22)
# estallido de corona del eclipse (25.1)
m = int(1.6*SR); add(noise(1.6, 1500)*np.hanning(m)*2.5 + tone(110,1.6,a=0.3,d=0.8)*0.5, 24.5, gain=0.3)

# ── Escáner (30.3–35.2): barrido agudo oscilante
m = int(2.7*SR); tt = np.arange(m)/SR
scan = np.sin(2*np.pi*(700 + 300*np.sin(2*np.pi*0.37*tt))*tt)*0.12*np.hanning(m)
add(scan, 30.3, gain=1.0)
m = int(2.0*SR); tt = np.arange(m)/SR
add(np.sin(2*np.pi*(700 + 300*np.sin(2*np.pi*0.37*tt))*tt)*0.12*np.hanning(m), 33.2)
for i in range(6): add(tone(880*(1+0.12*i), 0.15, a=0.002, d=0.1)*0.3, 32.6+0.32*i)

# ── Planetas (39.1+0.5 i) y sello HIPÓTESIS (42.72) + NO ES UNA PRUEBA (43.55)
for i in range(5): add(tone(392*2**(i/5), 0.35, a=0.003, d=0.2, harm=(1,2), amp=(1,0.3))*0.35, 39.1+0.5*i)
def boom(at, g=1.0):
    m = int(1.2*SR); tt = np.arange(m)/SR
    s = np.sin(2*np.pi*(90*np.exp(-tt*3))*tt)*np.exp(-tt*3.2) + noise(1.2, 900)*np.exp(-tt*9)*1.5
    add(s*g, at, gain=0.9)
boom(42.72); boom(43.55, 0.55)
# riser antes de la pregunta (42.2–44.5)
m = int(2.3*SR); tt = np.arange(m)/SR
add(noise(2.3, 2500)*np.linspace(0,1,m)**2*0.6, 42.2, gain=0.3)

# ── Revelación y cierre
add(noise(0.4, 3000)*np.hanning(int(0.4*SR))*0.4, 44.45, gain=0.5)
for f, k in [(523.25,46.6),(659.25,46.66),(783.99,46.72),(1046.5,46.78)]:
    add(tone(f, 1.6, a=0.004, d=0.8, harm=(1,2,3), amp=(1,0.3,0.1)), k, gain=0.22)
boom(46.6, 0.5)
add(tone(660, 0.3, a=0.003, d=0.15)*0.4, 50.05)   # burbuja
for k in [51.35]: add(tone(880, 0.35, a=0.003, d=0.18, harm=(1,2), amp=(1,0.4))*0.4, k)

# fundido final y normalización
fade = np.minimum(1, (DUR - t)/1.2); L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max()); L, R = L/peak*0.8, R/peak*0.8
stereo = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open('musica.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(stereo.tobytes())
print('musica.wav', DUR, 's')

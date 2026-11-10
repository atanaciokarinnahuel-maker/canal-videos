// Banda sonora sintetizada 100 % en código (senos + ruido filtrado). Sin samples.
// node scripts/musica.mjs  ->  public/musica.wav
import {writeFileSync} from 'node:fs';

const SR = 44100;
const DUR = 36;
const N = SR * DUR;
const L = new Float32Array(N);
const R = new Float32Array(N);

// hitos (segundos de video) — deben coincidir con src/timeline.ts
const BLOOD = 10.0, TEAR = 13.9, TEAR_END = 17.2, DESCEND = 20.5, FLY = 23.8, FLY_END = 26.3;

const clamp01 = (x) => Math.min(1, Math.max(0, x));
const ramp = (t, a, b) => clamp01((t - a) / (b - a));
const sm = (x) => x * x * (3 - 2 * x);
const hz = (n) => 440 * 2 ** ((n - 69) / 12); // midi -> Hz

let seed = 1234567;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296) * 2 - 1;

/** Pad: suma de parciales con desafinación lenta, paneo y envolvente. */
const pad = (midi, env, gain, pan = 0, partials = [1, 0.5, 0.22, 0.1]) => {
  const f = hz(midi);
  for (const det of [-0.0035, 0.0035]) {
    let ph = partials.map(() => Math.random() * 6.283);
    for (let i = 0; i < N; i++) {
      const t = i / SR;
      const e = env(t);
      if (e <= 0) continue;
      const vib = 1 + det + 0.0012 * Math.sin(6.283 * 0.17 * t + midi);
      let s = 0;
      for (let k = 0; k < partials.length; k++) {
        ph[k] += (6.283 * f * (k + 1) * vib) / SR;
        s += partials[k] * Math.sin(ph[k]);
      }
      s *= e * gain * 0.5;
      const p = pan + det * 60;
      L[i] += s * (1 - clamp01(p));
      R[i] += s * (1 - clamp01(-p));
    }
  }
};

const fadeIO = (a, b, c, d) => (t) => sm(ramp(t, a, b)) * (1 - sm(ramp(t, c, d)));

// 1) Dron grave en Re: el pasillo, la distancia
pad(26, fadeIO(0, 3, 33, 36), 0.5, 0, [1, 0.35, 0.12]);          // D1
pad(38, fadeIO(0.5, 5, 33, 36), 0.26, -0.2);                      // D2
pad(45, fadeIO(2, 7, 33, 36), 0.16, 0.25);                        // A2
// 2) Re menor: separación (hasta la rasgadura)
pad(53, fadeIO(4, 9, TEAR - 0.3, TEAR + 1.5), 0.11, -0.35);       // F3
pad(58, fadeIO(BLOOD - 1, BLOOD + 0.5, TEAR - 0.2, TEAR + 0.8), 0.07, 0.4); // Bb3 (tensión: "sin sangre")
// 3) Re mayor: Dios desciende, el camino se abre
pad(54, fadeIO(DESCEND - 0.5, FLY + 1, 33, 36), 0.13, -0.3);      // F#3
pad(57, fadeIO(TEAR_END, DESCEND + 2, 33, 36), 0.11, 0.3);        // A3
pad(62, fadeIO(DESCEND, FLY_END, 33, 36), 0.1, 0);                // D4
pad(66, fadeIO(FLY, FLY_END + 1.5, 32.5, 36), 0.075, -0.45, [1, 0.25]); // F#4
pad(69, fadeIO(FLY + 0.8, FLY_END + 2.5, 32.5, 36), 0.06, 0.45, [1, 0.2]); // A4
pad(74, fadeIO(FLY_END, 29.5, 32, 36), 0.04, 0.15, [1, 0.12]);    // D5 (brillo final)

// 4) Latidos graves bajo "y nunca sin sangre"
for (const t0 of [BLOOD, BLOOD + 0.32, BLOOD + 1.25, BLOOD + 1.57]) {
  for (let i = 0; i < SR * 0.5; i++) {
    const t = i / SR;
    const s = Math.sin(6.283 * (52 * t + 9 * (1 - Math.exp(-t * 18)) * -0.6)) * Math.exp(-t * 11) * 0.42;
    const j = Math.floor(t0 * SR) + i;
    L[j] += s; R[j] += s;
  }
}

// 5) La rasgadura: impacto sub + desgarro de ruido que cae "de arriba abajo"
{
  let ph = 0;
  for (let i = 0; i < SR * 3.2; i++) {
    const t = i / SR;
    const f = 34 + 70 * Math.exp(-t * 7);
    ph += (6.283 * f) / SR;
    const s = Math.sin(ph) * Math.exp(-t * 1.5) * 0.85 * sm(ramp(t, 0, 0.004));
    const j = Math.floor(TEAR * SR) + i;
    L[j] += s; R[j] += s;
  }
  // ruido pasa-banda con frecuencia central descendente
  let lp = 0, bp = 0;
  const len = TEAR_END - TEAR + 0.4;
  for (let i = 0; i < SR * len; i++) {
    const t = i / SR;
    const u = t / len;
    const fc = 5200 * Math.pow(1 - u, 2.2) + 240;
    const g = 2 * Math.sin((Math.PI * fc) / SR);
    const x = rnd() * (0.6 + 0.4 * Math.abs(Math.sin(t * 47)));
    const hp = x - lp - 0.9 * bp;
    bp += g * hp; lp += g * bp;
    const e = (Math.exp(-t * 2.2) * 0.5 + 0.1 * (1 - u)) * sm(ramp(t, 0, 0.01)) * (1 - sm(ramp(u, 0.85, 1)));
    const j = Math.floor(TEAR * SR) + i;
    const pan = Math.sin(t * 9) * 0.3;
    L[j] += bp * e * (0.5 - pan * 0.5); R[j] += bp * e * (0.5 + pan * 0.5);
  }
}

// 6) Aire: subida hacia el fly-through y cola luminosa
{
  let lp = 0, bp = 0;
  for (let i = Math.floor((DESCEND - 1) * SR); i < N; i++) {
    const t = i / SR;
    const e = sm(ramp(t, DESCEND - 1, FLY + 1.3)) * (1 - 0.72 * sm(ramp(t, FLY + 1.3, FLY_END + 1.2))) * (1 - sm(ramp(t, 31, 35.5)));
    const fc = 500 + 3400 * sm(ramp(t, DESCEND, FLY + 1.3)) - 1800 * sm(ramp(t, FLY + 1.3, FLY_END + 1));
    const g = 2 * Math.sin((Math.PI * fc) / SR);
    const hp = rnd() - lp - 1.2 * bp;
    bp += g * hp; lp += g * bp;
    L[i] += bp * e * 0.1; R[i] += bp * e * 0.1 * (0.8 + 0.2 * Math.sin(t * 0.7));
  }
}

// 7) Espacio: cuatro combs con realimentación cruzada (reverb barata, de catedral)
{
  const wet = [new Float32Array(N), new Float32Array(N)];
  const taps = [[0.0897, 0.1373, 0.2011, 0.2671], [0.0953, 0.1429, 0.2113, 0.2579]];
  [L, R].forEach((src, ch) => {
    for (const d of taps[ch]) {
      const D = Math.floor(d * SR);
      const buf = new Float32Array(N);
      let lp = 0;
      for (let i = 0; i < N; i++) {
        const fb = i >= D ? buf[i - D] : 0;
        lp += 0.35 * (fb - lp);
        buf[i] = src[i] + lp * 0.78;
        wet[1 - ch][i] += fb * 0.1;
        wet[ch][i] += fb * 0.16;
      }
    }
  });
  for (let i = 0; i < N; i++) { L[i] += wet[0][i]; R[i] += wet[1][i]; }
}

// normalizar con techo suave y escribir WAV 16-bit
let peak = 0;
for (let i = 0; i < N; i++) peak = Math.max(peak, Math.abs(L[i]), Math.abs(R[i]));
const g = 0.89 / peak;
const pcm = Buffer.alloc(44 + N * 4);
pcm.write('RIFF', 0); pcm.writeUInt32LE(36 + N * 4, 4); pcm.write('WAVEfmt ', 8);
pcm.writeUInt32LE(16, 16); pcm.writeUInt16LE(1, 20); pcm.writeUInt16LE(2, 22);
pcm.writeUInt32LE(SR, 24); pcm.writeUInt32LE(SR * 4, 28); pcm.writeUInt16LE(4, 32); pcm.writeUInt16LE(16, 34);
pcm.write('data', 36); pcm.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  pcm.writeInt16LE(Math.round(Math.tanh(L[i] * g * 1.1) * 32000), 44 + i * 4);
  pcm.writeInt16LE(Math.round(Math.tanh(R[i] * g * 1.1) * 32000), 46 + i * 4);
}
writeFileSync(new URL('../public/musica.wav', import.meta.url), pcm);
console.log('musica.wav', DUR + 's', 'pico', peak.toFixed(3));

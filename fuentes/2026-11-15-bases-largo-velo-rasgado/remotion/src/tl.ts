import data from './words.json';

/* ───────────── Formato ───────────── */
export const FPS = 24;
export const WIDTH = 1920;
export const HEIGHT = 1080;

export type Word = {text: string; start: number; end: number; block: number};
export const WORDS = data.words as Word[];
export const BLOCKS = data.blocks as {name: string; start: number; end: number}[];
export const DUR = data.DUR as number;
export const FRAMES = Math.ceil(DUR * FPS);

export const C = {
  obsidian: '#06070a',
  gold: '#c9a35a',
  goldHi: '#f1d9a0',
  goldDeep: '#7d5a1e',
  crimson: '#b3202a',
  light: '#fff1d6',
  ink: '#f4efe4',
  linen: '#efe9dc',
};

export type V3 = [number, number, number];

/* ───────────── Anclas: el tiempo sale de la locución ───────────── */
const norm = (s: string) => s.toLowerCase().replace(/[^a-záéíóúüñ ]/g, '').trim();
const NW = WORDS.map((w) => norm(w.text));

const find = (block: number, phrase: string, nth = 0) => {
  const ph = norm(phrase).split(/\s+/);
  let seen = 0;
  for (let i = 0; i < WORDS.length; i++) {
    if (WORDS[i].block !== block) continue;
    let ok = true;
    for (let k = 0; k < ph.length; k++) {
      if (NW[i + k] !== ph[k] || WORDS[i + k].block !== block) {
        ok = false;
        break;
      }
    }
    if (ok && seen++ === nth) return [i, i + ph.length - 1];
  }
  throw new Error(`No encuentro "${phrase}" (#${nth}) en el bloque ${block}`);
};
/** Segundo de video en que empieza a decirse `phrase` dentro del bloque. */
export const at = (block: number, phrase: string, nth = 0) => WORDS[find(block, phrase, nth)[0]].start;
/** Segundo en que termina de decirse. */
export const atEnd = (block: number, phrase: string, nth = 0) => WORDS[find(block, phrase, nth)[1]].end;
/** Inicio del bloque (capítulo). */
export const B = (i: number) => BLOCKS[i].start;

/* ───────────── Matemática de animación ───────────── */
export const cl = (x: number) => Math.min(1, Math.max(0, x));
export const ramp = (t: number, a: number, b: number) => cl((t - a) / (b - a));
export const sm = (x: number) => {
  x = cl(x);
  return x * x * (3 - 2 * x);
};
export const outCubic = (x: number) => 1 - Math.pow(1 - cl(x), 3);
/** Fotogramas clave lineales (o con easing por tramo). */
export const key = (t: number, ts: number[], vs: number[], ease?: (n: number) => number) => {
  if (t <= ts[0]) return vs[0];
  for (let i = 1; i < ts.length; i++) {
    if (t <= ts[i]) {
      const d = ts[i] - ts[i - 1];
      let u = d > 0 ? (t - ts[i - 1]) / d : 1;
      if (ease) u = ease(u);
      return vs[i - 1] + (vs[i] - vs[i - 1]) * u;
    }
  }
  return vs[vs.length - 1];
};
/** Golpe: sube en `up` y cae en `down`. */
export const pulse = (t: number, t0: number, up = 0.12, down = 0.9) =>
  t < t0 ? 0 : t < t0 + up ? (t - t0) / up : Math.max(0, 1 - (t - t0 - up) / down);

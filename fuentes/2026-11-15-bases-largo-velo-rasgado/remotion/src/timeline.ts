import {Easing, interpolate} from 'remotion';

/* ───────────── Formato ───────────── */
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
export const DURATION_S = 36;

/* ───────────── Paleta ───────────── */
export const C = {
  obsidian: '#06070a',
  obsidianLift: '#0d0f15',
  gold: '#c9a35a',
  goldHi: '#f1d9a0',
  goldDeep: '#7d5a1e',
  crimson: '#9b1b22',
  light: '#fff1d6',
  ink: '#f4efe4',
};

/* ───────────── Guion sincronizado ─────────────
   Los tiempos salen de la locución real (silencedetect de ffmpeg sobre voz.mp3)
   y están en segundos de LOCUCIÓN. VO_OFFSET los pasa a segundos de video. */
export const VO_OFFSET = 1.5;

export type Phrase = {
  from: number;
  to: number;
  lines: string[];
  /** palabras resaltadas -> color */
  accent?: Record<string, 'gold' | 'crimson'>;
  ref?: string;
  big?: boolean;
};

export const SCRIPT: Phrase[] = [
  {from: 0.05, to: 4.07, lines: ['Durante siglos, un velo', 'separó al hombre', 'de la presencia de Dios.'], accent: {velo: 'gold', Dios: 'gold'}, ref: 'Éxodo 26:33'},
  {from: 4.85, to: 8.04, lines: ['Solo un hombre,', 'una vez al año,', 'podía cruzarlo…'], ref: 'Levítico 16'},
  {from: 8.53, to: 9.81, lines: ['…y nunca', 'sin sangre.'], accent: {sangre: 'crimson'}, ref: 'Hebreos 9:7'},
  {from: 10.47, to: 13.83, lines: ['Pero cuando Cristo murió,', 'el velo se rasgó en dos.'], accent: {Cristo: 'gold', rasgó: 'gold'}, ref: 'Mateo 27:51'},
  {from: 14.29, to: 15.62, lines: ['De arriba', 'abajo.'], accent: {arriba: 'gold', abajo: 'gold'}, ref: 'Mateo 27:51', big: true},
  {from: 16.15, to: 18.41, lines: ['No lo rasgó el hombre,', 'subiendo hacia Dios.']},
  {from: 19.06, to: 21.78, lines: ['Lo rasgó Dios,', 'descendiendo', 'hacia el hombre.'], accent: {Dios: 'gold', descendiendo: 'gold'}},
  {from: 22.34, to: 24.43, lines: ['Hoy, el camino', 'está abierto.'], accent: {abierto: 'gold'}, ref: 'Hebreos 10:19-20'},
  {from: 24.88, to: 27.35, lines: ['No por tus méritos,', 'sino por su sangre.'], accent: {sangre: 'crimson'}, ref: 'Efesios 2:8-9'},
  {from: 27.81, to: 29.5, lines: ['Acércate', 'con confianza.'], accent: {Acércate: 'gold'}, ref: 'Hebreos 4:16', big: true},
];

/* ───────────── Hitos visuales (segundos de video) ───────────── */
export const T = {
  blood: 10.0, // "…sin sangre"
  tearStart: 13.9, // "se rasgó"
  tearEnd: 17.2, // fin de "de arriba abajo"
  descend: 20.5, // "Lo rasgó Dios, descendiendo"
  flyStart: 23.8, // "Hoy, el camino está abierto"
  flyEnd: 26.3,
  endCard: 31.4,
};

/* ───────────── Geometría del velo ───────────── */
export const VEIL = {halfW: 3.7, height: 10.4};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const lerpT = (t: number, a: number[], b: number[], easing?: (n: number) => number) =>
  interpolate(t, a, b, {...clamp, easing});

/** Altura del frente de rasgadura: por encima de ella el velo ya está partido. */
export const tearFrontY = (t: number) =>
  t < T.tearStart
    ? 99
    : lerpT(t, [T.tearStart, T.tearEnd], [VEIL.height + 0.3, -1.6], Easing.bezier(0.5, 0, 0.8, 1));

/** Cuánto se han recogido las dos mitades hacia los lados (0-1). */
export const veilPart = (t: number) => {
  if (t < T.tearStart) return 0;
  if (t < T.descend) return lerpT(t, [T.tearStart, T.tearEnd, T.descend], [0.035, 0.07, 0.12]);
  return lerpT(t, [T.descend, T.flyStart + 0.9], [0.12, 1], Easing.inOut(Easing.cubic));
};

/** Intensidad de la luz que sale del Lugar Santísimo. */
export const glory = (t: number) =>
  lerpT(t, [T.tearStart, T.tearStart + 0.25, T.tearStart + 1.2, T.descend, T.flyStart, T.flyEnd, DURATION_S], [0, 1.5, 0.9, 1.1, 2.1, 1.5, 1.7]);

/** Fracción del velo ya rasgada (0-1). */
export const tornFraction = (t: number) =>
  Math.min(1, Math.max(0, (VEIL.height - tearFrontY(t)) / VEIL.height));

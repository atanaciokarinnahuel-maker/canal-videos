import React from 'react';
import {AbsoluteFill} from 'remotion';
import {B, C, at, pulse} from '../tl';

const BR = [-3, -2, -1, 0, 1, 2, 3];
export const CHAPTERS = ['', 'El velo', 'Los querubines', 'Un hombre, un día, con sangre', 'El problema', 'De arriba abajo', 'El Cordero que tomó tu lugar', 'El otro lado'];
const GHOST = at(0, 'la séptima lámpara');
export const REVEAL = at(7, 'Un trono de gracia');

/** Cuántas llamas hay encendidas en el segundo t. */
export const litAt = (t: number) => {
  let n = 0;
  for (let i = 1; i <= 7; i++) if (t >= B(i) - 0.1) n = i;
  return n;
};

/** Indicador de progreso: menorá de 7 llamas. */
export const Menorah: React.FC<{lit: number; pulse?: number; size?: number; ghost?: number}> = ({lit, pulse: pl = 0, size = 250, ghost = 0}) => {
  const top = 34;
  const base = 128;
  return (
    <svg width={size} height={size * 0.62} viewBox="-120 0 240 150" style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id="g-oro" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={C.goldHi} />
          <stop offset="1" stopColor={C.goldDeep} />
        </linearGradient>
        <radialGradient id="g-llama" cx="0.5" cy="0.7" r="0.6">
          <stop offset="0" stopColor="#fffbe8" />
          <stop offset="0.5" stopColor="#ffd27a" />
          <stop offset="1" stopColor="#ff9a2e" stopOpacity="0" />
        </radialGradient>
      </defs>
      {[1, 2, 3].map((k) => (
        <path key={k} d={`M ${-k * 30} ${top} A ${k * 30} ${k * 26} 0 0 0 ${k * 30} ${top}`} fill="none" stroke="url(#g-oro)" strokeWidth={5} strokeLinecap="round" />
      ))}
      <path d={`M 0 ${top} L 0 ${base}`} stroke="url(#g-oro)" strokeWidth={6} strokeLinecap="round" />
      <path d={`M -34 ${base + 10} L 34 ${base + 10} M -20 ${base} L 20 ${base}`} stroke="url(#g-oro)" strokeWidth={6} strokeLinecap="round" />
      {BR.map((b, i) => {
        const on = i < lit;
        const last = i === lit - 1;
        const g = !on ? ghost * (0.5 + 0.5 * Math.sin(i * 1.7 + ghost * 20)) : 0;
        const s = on ? 1 + (last ? pl * 0.9 : 0) : g;
        return (
          <g key={b} transform={`translate(${b * 30} ${top})`}>
            <rect x={-7} y={-5} width={14} height={6} rx={2} fill="url(#g-oro)" />
            {s > 0.02 ? (
              <g transform={`scale(${s})`} opacity={on ? 1 : 0.75}>
                <circle cx={0} cy={-18} r={26} fill="url(#g-llama)" opacity={0.55 + (last ? pl * 0.45 : 0)} />
                <path d="M 0 -34 C 9 -22 8 -9 0 -6 C -8 -9 -9 -22 0 -34 Z" fill="#ffe9b0" />
                <path d="M 0 -25 C 4 -18 4 -11 0 -9 C -4 -11 -4 -18 0 -25 Z" fill="#fff" />
              </g>
            ) : (
              <path d="M 0 -20 C 4 -14 4 -9 0 -7 C -4 -9 -4 -14 0 -20 Z" fill="#3a3324" />
            )}
          </g>
        );
      })}
    </svg>
  );
};

/** Barra superior: menorá + capítulo + puerta sellada «?» (el bucle abierto). */
export const Hud: React.FC<{t: number}> = ({t}) => {
  const lit = litAt(t);
  const pl = lit > 0 ? pulse(t, B(lit) - 0.1, 0.15, 1.4) : 0;
  const ghost = pulse(t, GHOST, 0.25, 1.6);
  const revealed = t >= REVEAL;
  const pop = pulse(t, REVEAL, 0.15, 1.5);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: 64, top: 40, display: 'flex', alignItems: 'center', gap: 24}}>
        <div style={{transform: `scale(${1 + pl * 0.12 + ghost * 0.1})`, transformOrigin: '30% 60%'}}>
          <Menorah lit={lit} pulse={pl} size={214} ghost={ghost} />
        </div>
        <div>
          <div style={{fontFamily: 'Inter', fontWeight: 500, fontSize: 24, letterSpacing: '0.32em', color: C.gold, textShadow: '0 1px 10px #000'}}>{lit > 0 ? `LÁMPARA ${lit} DE 7` : 'BASES BÍBLICAS'}</div>
          {lit > 0 ? <div style={{fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 48, color: C.ink, marginTop: 2, textShadow: '0 2px 20px rgba(0,0,0,.95)'}}>{CHAPTERS[lit]}</div> : null}
        </div>
      </div>
      <div style={{position: 'absolute', right: 64, top: 44, textAlign: 'center', transform: `scale(${1 + pop * 0.35})`, transformOrigin: '50% 30%'}}>
        <div
          style={{
            width: 100, height: 128, borderRadius: '50px 50px 6px 6px', border: `3px solid ${C.gold}`, margin: '0 auto',
            background: revealed ? 'radial-gradient(circle at 50% 60%, #fff6dc, #e9b65a 70%)' : 'linear-gradient(180deg,#141018,#06070a)',
            boxShadow: revealed ? `0 0 ${50 + pop * 80}px rgba(255,220,150,.85)` : '0 0 24px rgba(0,0,0,.8)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 64, color: C.goldHi,
          }}
        >
          {revealed ? (
            <svg width="44" height="62" viewBox="0 0 44 62">
              <path d="M18 0h8v16h18v8H26v38h-8V24H0v-8h18z" fill="#3b2606" />
            </svg>
          ) : (
            '?'
          )}
        </div>
        <div style={{fontFamily: 'Inter', fontWeight: 500, fontSize: 18, letterSpacing: '0.26em', color: C.gold, marginTop: 10, textShadow: '0 1px 10px #000'}}>{revealed ? 'TRONO DE LA GRACIA' : 'DEL OTRO LADO'}</div>
      </div>
    </AbsoluteFill>
  );
};

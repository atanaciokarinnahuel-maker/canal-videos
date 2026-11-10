import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C} from './timeline';

const BR = [-3, -2, -1, 0, 1, 2, 3];

/** Indicador de progreso: menorá de 7 llamas. `lit` = llamas encendidas, `pulse` 0-1 = destello de la última. */
export const Menorah: React.FC<{lit: number; pulse?: number; size?: number}> = ({lit, pulse = 0, size = 250}) => {
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
      {/* brazos */}
      {[1, 2, 3].map((k) => (
        <path key={k} d={`M ${-k * 30} ${top} A ${k * 30} ${k * 26} 0 0 0 ${k * 30} ${top}`} fill="none" stroke="url(#g-oro)" strokeWidth={5} strokeLinecap="round" />
      ))}
      <path d={`M 0 ${top} L 0 ${base}`} stroke="url(#g-oro)" strokeWidth={6} strokeLinecap="round" />
      <path d={`M -34 ${base + 10} L 34 ${base + 10} M -20 ${base} L 20 ${base}`} stroke="url(#g-oro)" strokeWidth={6} strokeLinecap="round" />
      {BR.map((b, i) => {
        const on = i < lit;
        const last = i === lit - 1;
        const s = on ? 1 + (last ? pulse * 0.9 : 0) : 0;
        return (
          <g key={b} transform={`translate(${b * 30} ${top})`}>
            <rect x={-7} y={-5} width={14} height={6} rx={2} fill="url(#g-oro)" />
            {on ? (
              <g transform={`scale(${s})`}>
                <circle cx={0} cy={-18} r={26} fill="url(#g-llama)" opacity={0.55 + (last ? pulse * 0.45 : 0)} />
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
export const Hud: React.FC<{lit: number; pulse?: number; chapter?: string; revealed?: boolean}> = ({lit, pulse, chapter, revealed}) => (
  <AbsoluteFill style={{pointerEvents: 'none'}}>
    <div style={{position: 'absolute', left: 70, top: 44, display: 'flex', alignItems: 'center', gap: 26}}>
      <Menorah lit={lit} pulse={pulse} size={190} />
      <div>
        <div style={{fontFamily: 'Inter', fontWeight: 500, fontSize: 22, letterSpacing: '0.32em', color: C.gold}}>{lit > 0 ? `LÁMPARA ${lit} DE 7` : 'BASES BÍBLICAS'}</div>
        {chapter ? <div style={{fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 46, color: C.ink, marginTop: 4, textShadow: '0 2px 20px rgba(0,0,0,.9)'}}>{chapter}</div> : null}
      </div>
    </div>
    <div style={{position: 'absolute', right: 70, top: 50, textAlign: 'center'}}>
      <div
        style={{
          width: 96, height: 124, borderRadius: '48px 48px 6px 6px', border: `3px solid ${C.gold}`,
          background: revealed ? 'radial-gradient(circle at 50% 60%, #fff6dc, #e9b65a 70%)' : 'linear-gradient(180deg,#141018,#06070a)',
          boxShadow: revealed ? '0 0 60px rgba(255,220,150,.8)' : '0 0 24px rgba(0,0,0,.8)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 70, color: revealed ? '#3b2606' : C.goldHi,
        }}
      >
        {revealed ? '✝' : '?'}
      </div>
      <div style={{fontFamily: 'Inter', fontWeight: 500, fontSize: 17, letterSpacing: '0.26em', color: C.gold, marginTop: 10}}>{revealed ? 'TRONO DE LA GRACIA' : 'DEL OTRO LADO'}</div>
    </div>
  </AbsoluteFill>
);

/** Subtítulos palabra por palabra: grupo corto, palabra activa resaltada. */
export const Words: React.FC<{words: string[]; active: number; accent?: string}> = ({words, active, accent = C.goldHi}) => (
  <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 96}}>
    <div style={{display: 'flex', gap: 22, flexWrap: 'wrap', justifyContent: 'center', maxWidth: 1500}}>
      {words.map((w, i) => {
        const on = i === active;
        return (
          <span
            key={i}
            style={{
              fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 92, lineHeight: 1.05,
              color: on ? '#1a1206' : i < active ? C.ink : 'rgba(244,239,228,.55)',
              background: on ? accent : 'transparent', borderRadius: 12, padding: '0 16px',
              transform: on ? 'scale(1.08)' : 'none',
              textShadow: on ? 'none' : '0 3px 26px rgba(0,0,0,.95), 0 0 6px rgba(0,0,0,.8)',
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  </AbsoluteFill>
);

/** Rótulo de cita bíblica en pantalla. */
export const VerseTag: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', left: 70, bottom: 250, fontFamily: 'Inter', fontWeight: 500, fontSize: 26, letterSpacing: '0.3em', color: '#1a1206', background: C.gold, padding: '10px 20px', borderRadius: 8}}>{text}</div>
);

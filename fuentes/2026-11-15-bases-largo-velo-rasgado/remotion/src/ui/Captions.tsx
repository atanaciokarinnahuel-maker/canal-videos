import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, WORDS} from '../tl';

/* Grupos cortos: se corta en la puntuación o al llegar a ~24 caracteres. */
type Group = {i0: number; i1: number; start: number; end: number};
const GROUPS: Group[] = (() => {
  const out: Group[] = [];
  let i0 = 0;
  let chars = 0;
  for (let i = 0; i < WORDS.length; i++) {
    const w = WORDS[i];
    chars += w.text.length + 1;
    const n = i - i0 + 1;
    const last = i === WORDS.length - 1 || WORDS[i + 1].block !== w.block;
    const punct = /[,;]$/.test(w.text);
    const stop = /[.:…?!]$/.test(w.text);
    const nextLen = last ? 0 : WORDS[i + 1].text.length;
    if (last || stop || (punct && n >= 2) || n >= 5 || chars + nextLen > 25) {
      out.push({i0, i1: i, start: WORDS[i0].start, end: w.end});
      i0 = i + 1;
      chars = 0;
    }
  }
  return out;
})();

/** Subtítulos palabra por palabra con la palabra activa resaltada. */
export const Captions: React.FC<{t: number; bottom?: number; size?: number}> = ({t, bottom = 78, size = 84}) => {
  let g: Group | null = null;
  for (const x of GROUPS) if (x.start - 0.06 <= t) g = x;
  if (!g || t > g.end + 0.55) return null;
  const words = WORDS.slice(g.i0, g.i1 + 1);
  let active = 0;
  words.forEach((w, i) => {
    if (w.start <= t + 0.02) active = i;
  });
  const inn = Math.min(1, (t - (g.start - 0.06)) / 0.12);
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: bottom}}>
      <div style={{display: 'flex', gap: 20, flexWrap: 'wrap', justifyContent: 'center', maxWidth: 1560, opacity: inn, transform: `translateY(${(1 - inn) * 14}px)`}}>
        {words.map((w, i) => {
          const on = i === active;
          return (
            <span
              key={i}
              style={{
                fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: size, lineHeight: 1.06,
                color: on ? '#1a1206' : i < active ? C.ink : 'rgba(244,239,228,.5)',
                background: on ? C.goldHi : 'transparent', borderRadius: 12, padding: '0 16px',
                transform: on ? 'scale(1.08)' : 'none',
                textShadow: on ? 'none' : '0 3px 26px rgba(0,0,0,.95), 0 0 6px rgba(0,0,0,.85)',
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

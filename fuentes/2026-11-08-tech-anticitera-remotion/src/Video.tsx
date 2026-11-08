import React from 'react';
import {useCurrentFrame, interpolateColors} from 'remotion';
import {C, Dust, FPS, Gear, H, W, Txt, clamp, lerp, ramp, back, eo, shake} from './lib';
import {S1, S2, S3} from './scenes1';
import {S4, S5, S6, S7} from './scenes2';
import {WORDS} from './words';

const BG_T = [0, 4.1, 4.7, 12.3, 12.9, 29.4, 30.0, 37.1, 37.7, 44.2, 44.8, 70];
const BG_TOP = ['#05060c', '#05060c', '#06222b', '#06222b', '#1a0f08', '#1a0f08', '#031a1a', '#031a1a', '#0a0d2a', '#0a0d2a', '#070509', '#070509'];
const BG_BOT = ['#12131f', '#12131f', '#0c4452', '#0c4452', '#33200f', '#33200f', '#07403d', '#07403d', '#1d2266', '#1d2266', '#241a06', '#241a06'];

const Defs = () => (
  <defs>
    <linearGradient id="bronze" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stopColor="#F6CF86" /><stop offset="0.5" stopColor="#C98A3B" /><stop offset="1" stopColor="#6b3f17" />
    </linearGradient>
    <radialGradient id="glowGold"><stop offset="0" stopColor="#F2C46D" stopOpacity={0.55} /><stop offset="1" stopColor="#F2C46D" stopOpacity={0} /></radialGradient>
    <radialGradient id="glowTeal"><stop offset="0" stopColor="#46f0d0" stopOpacity={0.35} /><stop offset="1" stopColor="#46f0d0" stopOpacity={0} /></radialGradient>
    <radialGradient id="glowIndigo"><stop offset="0" stopColor="#6c7bff" stopOpacity={0.4} /><stop offset="1" stopColor="#6c7bff" stopOpacity={0} /></radialGradient>
    <radialGradient id="goldDisc"><stop offset="0" stopColor="#FFF1C2" /><stop offset="0.7" stopColor="#F2C46D" /><stop offset="1" stopColor="#D98A25" /></radialGradient>
    <linearGradient id="scanGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6ff2d8" stopOpacity={0} /><stop offset="0.5" stopColor="#6ff2d8" stopOpacity={0.5} /><stop offset="1" stopColor="#6ff2d8" stopOpacity={0} /></linearGradient>
    <radialGradient id="vig" cx="0.5" cy="0.45" r="0.75"><stop offset="0.55" stopColor="#000" stopOpacity={0} /><stop offset="1" stopColor="#000" stopOpacity={0.7} /></radialGradient>
  </defs>
);

const END = 46.6;
const Hud: React.FC<{t: number}> = ({t}) => {
  const p = clamp((t - 0.2) / (END - 0.2));
  const x0 = 110, x1 = 880, y = 205;
  const gx = lerp(x0, x1, p);
  const opened = ramp(t, END, END + 0.2);
  const pop = ramp(t, END, END + 0.35, back);
  const sk = shake(t, END, 8, 0.4);
  return (
    <g>
      <Txt x={80} y={140} size={26} weight={800} fill={C.gold} anchor="start" spacing={5}>EXPEDIENTE · ANTICITERA</Txt>
      <Txt x={1000} y={140} size={26} weight={800} fill={C.cream} anchor="end" spacing={4} opacity={0.7}>TECNOLOGÍA E IA</Txt>
      <rect x={x0} y={y - 6} width={x1 - x0 + 40} height={12} rx={6} fill="#2a1a0c" stroke="#8a5a26" strokeWidth={2} />
      <rect x={x0} y={y - 6} width={Math.max(2, gx - x0)} height={12} rx={6} fill={C.gold} />
      {Array.from({length: 20}).map((_, i) => (<line key={i} x1={x0 + i * 41} y1={y + 12} x2={x0 + i * 41} y2={y + 22} stroke="#8a5a26" strokeWidth={3} />))}
      <Gear n={14} r={34} x={gx} y={y} rot={((gx - x0) / 34) * 57.3} />
      {/* medallón sellado */}
      <g transform={`translate(${960 + sk.x} ${y + sk.y}) scale(${1 + 0.55 * pop - 0.25 * ramp(t, END + 0.9, END + 1.6)})`}>
        <circle r={opened ? 80 : 54} fill="url(#glowGold)" opacity={opened ? 1 : 0.3} />
        <circle r={46} fill="#1b1006" stroke={C.gold} strokeWidth={6} />
        {!opened && <path d="M-46 -10 L 46 10" stroke="#C98A3B" strokeWidth={5} opacity={0.8} />}
        <Txt x={0} y={22} size={64} family="GFS Baskerville" weight={700} fill={opened ? '#fff' : C.gold}>?</Txt>
      </g>
    </g>
  );
};

const Subs: React.FC<{t: number}> = ({t}) => {
  // chunks por puntuación o ≤4 palabras
  const chunks = React.useMemo(() => {
    const phrases: [string, number, number][][] = [];
    let cur: [string, number, number][] = [];
    WORDS.forEach((w, i) => {
      cur.push(w);
      if (/[.,:?!…]$/.test(w[0]) || i === WORDS.length - 1) { phrases.push(cur); cur = []; }
    });
    const out: {w: [string, number, number][]; a: number; b: number}[] = [];
    phrases.forEach((ph) => {
      const parts = Math.ceil(ph.length / 4);
      const size = Math.ceil(ph.length / parts);
      for (let k = 0; k < ph.length; k += size) {
        const c = ph.slice(k, k + size);
        out.push({w: c, a: c[0][1], b: c[c.length - 1][2]});
      }
    });
    return out;
  }, []);
  const idx = chunks.findIndex((c, i) => t >= c.a - 0.04 && (t < c.b + 0.18 || (chunks[i + 1] && t < chunks[i + 1].a - 0.04)));
  if (idx < 0) return null;
  const ch = chunks[idx];
  const pop = ramp(t, ch.a - 0.04, ch.a + 0.12, back);
  const half = Math.ceil(ch.w.length / 2);
  const lines = ch.w.length > 2 ? [ch.w.slice(0, half), ch.w.slice(half)] : [ch.w];
  const maxChars = Math.max(...lines.map((l) => l.map((w) => w[0]).join(' ').length));
  const fs = Math.round(clamp(930 / (maxChars * 0.6), 54, 80));
  const pw = Math.min(1020, maxChars * fs * 0.6 + 90);
  const ph = lines.length * (fs + 20) + 34;
  const cy = 1395;
  return (
    <g transform={`translate(540 ${cy}) scale(${0.9 + 0.1 * pop})`} opacity={clamp(pop * 3)}>
      <rect x={-pw / 2} y={-ph / 2} width={pw} height={ph} rx={30} fill="rgba(6,8,16,0.68)" stroke="rgba(242,196,109,0.5)" strokeWidth={3} />
      {lines.map((ln, li) => (
        <text key={li} x={0} y={-ph / 2 + fs + 8 + li * (fs + 20)} textAnchor="middle" fontFamily="Inter" fontWeight={900} fontSize={fs} stroke="#000" strokeWidth={0} >
          {ln.map((w, wi) => {
            const active = t >= w[1] - 0.02 && t < w[2] + 0.06;
            const done = t >= w[2] + 0.06;
            return (<tspan key={wi} fill={active ? C.gold : done ? '#ffffff' : 'rgba(255,255,255,0.55)'}>{w[0].replace(/\.\.\.$/, '…') + (wi < ln.length - 1 ? ' ' : '')}</tspan>);
          })}
        </text>
      ))}
    </g>
  );
};

export const Video: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const top = interpolateColors(t, BG_T, BG_TOP);
  const bot = interpolateColors(t, BG_T, BG_BOT);
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{background: '#000'}}>
      <Defs />
      <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bot} /></linearGradient>
      <rect width={W} height={H} fill="url(#bg)" />
      <Dust t={t} />
      {t < 4.8 && <S1 t={t} />}
      {t > 4.3 && t < 12.9 && <S2 t={t} />}
      {t > 12.5 && t < 18.7 && <S3 t={t} />}
      {t > 18.3 && t < 30.0 && <S4 t={t} />}
      {t > 29.6 && t < 37.7 && <S5 t={t} />}
      {t > 37.3 && t < 44.9 && <S6 t={t} />}
      {t > 44.4 && <S7 t={t} />}
      <rect width={W} height={H} fill="url(#vig)" />
      <Hud t={t} />
      <Subs t={t} />
    </svg>
  );
};

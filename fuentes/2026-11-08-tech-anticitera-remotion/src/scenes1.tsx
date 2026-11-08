import React from 'react';
import {random} from 'remotion';
import {C, CY, Gear, Txt, W, clamp, lerp, ramp, win, eo, eio, back, meshRot, typed, gearPath} from './lib';

type P = {t: number};

// ───────── ESCENA 1 · 0–4.6 ─────────
export const S1: React.FC<P> = ({t}) => {
  const o = ramp(t, 0.05, 1.6) * (1 - ramp(t, 4.0, 4.6));
  const sc = lerp(0.8, 1.02, ramp(t, 0, 4.6, eio));
  const rot = t * 16;
  const sink = ramp(t, 4.0, 4.6) * 160;
  const r1 = 300, n1 = 40, n2 = 20, r2 = (r1 * n2) / n1, phi = 32;
  const cx2 = (r1 + r2) * Math.cos((phi * Math.PI) / 180), cy2 = (r1 + r2) * Math.sin((phi * Math.PI) / 180);
  return (
    <g opacity={o} transform={`translate(540 ${CY + sink}) scale(${sc})`}>
      <circle r={560} fill="url(#glowGold)" opacity={0.5 + 0.1 * Math.sin(t * 3)} />
      <Gear n={n1} r={r1} x={0} y={0} rot={rot} />
      <Gear n={n2} r={r2} x={cx2} y={cy2} rot={meshRot(n1, n2, rot, phi)} />
      <g opacity={ramp(t, 2.6, 3.2)}>
        <Txt x={0} y={r1 + 120} size={54} family="GFS Baskerville" fill={C.gold} spacing={14} weight={400}>ΑΝΤΙΚΥΘΗΡΑ</Txt>
      </g>
      <g opacity={ramp(t, 0.35, 0.8)} transform={`scale(${lerp(1.5, 1, ramp(t, 0.3, 0.8, back))})`}>
        <Txt x={0} y={-r1 - 120} size={78} fill={C.gold} weight={900} spacing={3}>HACE +2.000 AÑOS</Txt>
      </g>
    </g>
  );
};

// ───────── Cuerpo corroído (bloque con engranaje asomando) ─────────
const lumpPts = Array.from({length: 18}).map((_, i) => {
  const a = (i / 18) * Math.PI * 2;
  const r = 100 + random('lp' + i) * 38;
  return `${(r * Math.cos(a)).toFixed(1)},${(r * 0.82 * Math.sin(a)).toFixed(1)}`;
}).join(' ');
export const Lump: React.FC<{x: number; y: number; s: number; rot?: number; green: number; t: number}> = ({x, y, s, rot = 0, green, t}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
    <circle r={190} fill="url(#glowGold)" opacity={0.35 + 0.15 * Math.sin(t * 4)} />
    <Gear n={26} r={84} x={26} y={-14} rot={t * 20} opacity={1 - green * 0.2} />
    <polygon points={lumpPts} fill="#3b4a3c" stroke="#1c2a22" strokeWidth={4} />
    <polygon points={lumpPts} fill={`rgba(70,179,160,${0.15 + green * 0.5})`} />
    {Array.from({length: 24}).map((_, i) => (
      <circle key={i} cx={(random('cx' + i) - 0.5) * 170} cy={(random('cy' + i) - 0.5) * 120} r={4 + random('cr' + i) * 11} fill={random('cc' + i) > 0.5 ? '#6f8f75' : '#2a3a30'} opacity={0.75} />
    ))}
  </g>
);

const Diver: React.FC<{x: number; y: number; t: number; flip?: boolean}> = ({x, y, t, flip}) => (
  <g transform={`translate(${x} ${y}) scale(${flip ? -1 : 1} 1)`}>
    <line x1={-10} y1={-30} x2={-10} y2={-1200} stroke="#8dd3c8" strokeOpacity={0.5} strokeWidth={3} />
    <rect x={-26} y={-16} width={52} height={78} rx={20} fill="#0b1c25" stroke="#46B3A0" strokeWidth={3} />
    <circle cx={0} cy={-30} r={30} fill="#13303a" stroke="#F2C46D" strokeWidth={4} />
    <circle cx={8} cy={-32} r={11} fill="#8dd3c8" opacity={0.7} />
    <rect x={-22} y={56} width={16} height={58} rx={8} fill="#0b1c25" stroke="#46B3A0" strokeWidth={3} transform={`rotate(${Math.sin(t * 5) * 12} -14 56)`} />
    <rect x={6} y={56} width={16} height={58} rx={8} fill="#0b1c25" stroke="#46B3A0" strokeWidth={3} transform={`rotate(${-Math.sin(t * 5) * 12} 14 56)`} />
    <rect x={-48} y={-4} width={22} height={14} rx={7} fill="#0b1c25" stroke="#46B3A0" strokeWidth={3} transform={`rotate(${Math.sin(t * 4) * 18} -37 3)`} />
    <rect x={26} y={-4} width={22} height={14} rx={7} fill="#0b1c25" stroke="#46B3A0" strokeWidth={3} />
  </g>
);

// ───────── ESCENA 2 · 4.45–12.7 · naufragio ─────────
export const S2: React.FC<P> = ({t}) => {
  const o = win(t, 4.45, 12.7, 0.5, 0.45);
  const zoom = lerp(1.0, 1.12, ramp(t, 4.45, 12.7, eio));
  // buzos
  const dd = ramp(t, 7.7, 9.0, eio);
  const up = ramp(t, 9.0, 11.0, eio);
  const diverY1 = lerp(330, 1010, dd) - up * 560;
  const diverY2 = lerp(300, 1040, dd) - up * 590;
  // bloque
  const lumpX = lerp(710, 540, up);
  const lumpY = lerp(1085, 640, up);
  const lumpS = lerp(1, 2.0, ramp(t, 10.8, 12.4, eo)) * lerp(1, 1.0, up);
  const green = ramp(t, 11.2, 12.2);
  const yr = typed('1900', t, 5.0, 5.9);
  return (
    <g opacity={o} transform={`translate(540 ${CY}) scale(${zoom}) translate(-540 ${-CY})`}>
      {/* rayos de luz */}
      {[0, 1, 2, 3, 4].map((i) => (
        <polygon key={i} points={`${100 + i * 220},300 ${180 + i * 220},300 ${60 + i * 220 + Math.sin(t * 0.8 + i) * 40},1200 ${-60 + i * 220 + Math.sin(t * 0.8 + i) * 40},1200`} fill="#9fe6da" opacity={0.045} />
      ))}
      {/* fondo marino */}
      <path d={`M0 1150 Q 200 1110 400 1150 T 800 1140 T 1080 1130 L1080 1300 L0 1300 Z`} fill="#071a21" />
      <path d={`M0 1200 Q 300 1170 600 1210 T 1080 1190 L1080 1300 L0 1300 Z`} fill="#05131a" />
      {/* casco del barco */}
      <g opacity={0.9} transform="translate(70 1000)">
        <path d="M0 110 Q 40 150 170 160 Q 300 160 360 100 L 340 40 L 300 100 L 250 20 L 210 105 L 170 10 L 130 105 L 80 30 L 40 100 Z" fill="#071a21" stroke="#2f7f77" strokeWidth={3} />
        <line x1={170} y1={10} x2={150} y2={-130} stroke="#2f7f77" strokeWidth={6} />
        <line x1={150} y1={-130} x2={235} y2={-60} stroke="#2f7f77" strokeWidth={3} />
      </g>
      {/* ánforas */}
      {[0, 1, 2].map((i) => (
        <g key={i} transform={`translate(${840 + i * 70} ${1120 + i * 10}) rotate(${-20 + i * 24})`}>
          <path d="M-14 -50 Q -40 0 -14 40 L 14 40 Q 40 0 14 -50 Z" fill="#0b2a33" stroke="#2f7f77" strokeWidth={3} />
          <rect x={-8} y={-66} width={16} height={18} fill="#0b2a33" stroke="#2f7f77" strokeWidth={3} />
        </g>
      ))}
      {/* año + lugar */}
      <g opacity={ramp(t, 5.0, 5.3) * (1 - ramp(t, 7.6, 8.1))}>
        <Txt x={540} y={470} size={230} weight={900} fill={C.gold}>{yr}</Txt>
        <Txt x={540} y={560} size={34} weight={700} fill={C.cream} spacing={6} opacity={ramp(t, 6.3, 6.8)}>ISLA DE ANTICITERA · GRECIA</Txt>
      </g>
      {/* buzos */}
      <g opacity={ramp(t, 7.6, 8.0)}>
        <Diver x={600} y={diverY1} t={t} />
        <Diver x={800} y={diverY2} t={t + 1} flip />
      </g>
      {/* cuerda del bloque */}
      <line x1={lumpX} y1={lumpY - 60 * lumpS} x2={lumpX} y2={-200} stroke="#c9b28a" strokeWidth={4} opacity={ramp(t, 9.0, 9.3)} />
      <Lump x={lumpX} y={lumpY} s={lumpS} green={green} t={t} rot={up * 8} />
      {/* burbujas */}
      {Array.from({length: 22}).map((_, i) => {
        const sp = 40 + random('bs' + i) * 80;
        const y = 1250 - (((t * sp + random('by' + i) * 1000) % 1000) / 1000) * 950;
        const x = 100 + random('bx' + i) * 880 + Math.sin(t * 2 + i) * 14;
        return <circle key={i} cx={x} cy={y} r={3 + random('br' + i) * 7} fill="none" stroke="#bff3ea" strokeOpacity={0.5} strokeWidth={2} />;
      })}
      <g opacity={ramp(t, 11.4, 11.9)}>
        <Txt x={540} y={1010} size={40} weight={800} fill="#8dd3c8" spacing={8}>BLOQUE DE CORROSIÓN</Txt>
      </g>
    </g>
  );
};

// ───────── ESCENA 3 · 12.6–18.5 · 82 fragmentos ─────────
const COLS = 12, ROWS = 7;
const frag = Array.from({length: 82}).map((_, i) => {
  const c = i % COLS, r = Math.floor(i / COLS);
  const pts = Array.from({length: 6}).map((_, k) => {
    const a = (k / 6) * Math.PI * 2 + random('fa' + i) * 0.6;
    const rr = 24 + random('fr' + i + k) * 15;
    return `${(rr * Math.cos(a)).toFixed(1)},${(rr * Math.sin(a)).toFixed(1)}`;
  }).join(' ');
  return {i, gx: 540 + (c - (COLS - 1) / 2) * 76, gy: 710 + (r - (ROWS - 1) / 2) * 76, pts, sx: (random('sx' + i) - 0.5) * 1800, sy: (random('sy' + i) - 0.5) * 1400, sr: (random('sr' + i) - 0.5) * 720, patina: random('pt' + i), t0: 12.85 + random('st' + i) * 0.9};
});
const gearIdx = Array.from({length: 82}).map((_, i) => ({i, k: random('gi' + i)})).sort((a, b) => a.k - b.k).slice(0, 30).map((o, n) => ({...o, n}));

export const S3: React.FC<P> = ({t}) => {
  const o = win(t, 12.6, 18.5, 0.35, 0.4);
  const count = Math.round(82 * ramp(t, 13.2, 14.0, eio));
  const gcount = Math.round(30 * ramp(t, 15.2, 16.0, eio));
  const lost = ramp(t, 16.55, 17.4, eio);
  const gridFade = 1 - lost * 0.9;
  return (
    <g opacity={o}>
      <g opacity={gridFade}>
        {frag.map((f) => {
          const k = ramp(t, f.t0, f.t0 + 0.7, eo);
          const x = lerp(540 + f.sx, f.gx, k), y = lerp(CY + f.sy, f.gy, k), rot = lerp(f.sr, 0, k);
          const isG = gearIdx.find((g) => g.i === f.i);
          const glow = isG ? ramp(t, 15.2 + isG.n * 0.028, 15.45 + isG.n * 0.028) : 0;
          return (
            <g key={f.i} transform={`translate(${x} ${y}) rotate(${rot})`}>
              <polygon points={f.pts} fill={f.patina > 0.55 ? '#4e6b58' : '#8a5a26'} stroke={glow ? C.gold : '#1d1108'} strokeWidth={glow ? 4 : 2.5} />
              {glow > 0 && <g transform={`scale(${0.2 * glow}) rotate(${t * 60})`}><path d={gearPath(12, 60, 14, false)} fill={C.gold} fillRule="evenodd" /></g>}
            </g>
          );
        })}
      </g>
      {/* contadores */}
      <g opacity={ramp(t, 13.1, 13.4)}>
        <Txt x={540} y={350} size={170} weight={900} fill={C.gold}>{count}</Txt>
        <Txt x={540} y={405} size={36} weight={800} fill={C.cream} spacing={8}>FRAGMENTOS</Txt>
      </g>
      <g opacity={ramp(t, 15.2, 15.5) * (1 - ramp(t, 16.5, 16.8))}>
        <Txt x={540} y={1130} size={64} weight={900} fill={C.gold}>{`≈ ${gcount} ENGRANAJES`}</Txt>
      </g>
      {/* silueta de lo perdido */}
      <g opacity={lost}>
        <rect x={90} y={520} width={900} height={560} rx={24} fill="none" stroke={C.cream} strokeOpacity={0.6} strokeWidth={4} strokeDasharray="22 16" />
        <rect x={90} y={520} width={300} height={560} rx={24} fill="url(#bronze)" opacity={0.9} />
        {Array.from({length: 10}).map((_, i) => (
          <line key={i} x1={400 + i * 60} y1={540} x2={340 + i * 60} y2={1060} stroke={C.cream} strokeOpacity={0.18} strokeWidth={3} />
        ))}
        <Txt x={240} y={820} size={46} weight={900} fill="#2a1606">LO QUE</Txt>
        <Txt x={240} y={874} size={46} weight={900} fill="#2a1606">SOBREVIVE</Txt>
        <Txt x={700} y={820} size={64} weight={900} fill={C.cream} opacity={0.85}>PERDIDO</Txt>
        <Txt x={540} y={1170} size={52} weight={800} fill={C.gold}>SOBREVIVE ≈ 1/3 DE LA MÁQUINA</Txt>
      </g>
    </g>
  );
};

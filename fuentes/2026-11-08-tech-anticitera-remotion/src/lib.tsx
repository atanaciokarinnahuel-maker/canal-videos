import React from 'react';
import {Easing, random} from 'remotion';

export const FPS = 30;
export const W = 1080;
export const H = 1920;
export const CY = 780; // centro del escenario
export const C = {gold: '#F2C46D', bronze: '#C98A3B', dark: '#4a2a10', verd: '#46B3A0', cream: '#F7EBD3', night: '#0A0F1F', red: '#E4572E'};

export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const eo = Easing.out(Easing.cubic);
export const eio = Easing.inOut(Easing.cubic);
export const back = Easing.out(Easing.back(1.8));
export const ramp = (t: number, a: number, b: number, ease: (x: number) => number = eo) => ease(clamp((t - a) / (b - a)));
export const win = (t: number, a: number, b: number, fi = 0.3, fo = 0.3) => ramp(t, a, a + fi) * (1 - ramp(t, b - fo, b));

export function gearPath(n: number, ro: number, depth: number, windows = true): string {
  const ri = ro - depth;
  const step = (2 * Math.PI) / n;
  const f = (r: number, a: number) => `${(r * Math.cos(a)).toFixed(1)} ${(r * Math.sin(a)).toFixed(1)}`;
  let d = '';
  for (let i = 0; i < n; i++) {
    const a = i * step;
    const pts = [f(ri, a - step * 0.32), f(ro, a - step * 0.17), f(ro, a + step * 0.17), f(ri, a + step * 0.32)];
    d += (i === 0 ? 'M ' : 'L ') + pts[0] + ' L ' + pts[1] + ' L ' + pts[2] + ' L ' + pts[3] + ' ';
  }
  d += 'Z ';
  const circ = (cx: number, cy: number, r: number) =>
    `M ${cx - r} ${cy} a ${r} ${r} 0 1 0 ${2 * r} 0 a ${r} ${r} 0 1 0 ${-2 * r} 0 Z `;
  d += circ(0, 0, ri * 0.14);
  if (windows && n >= 16) {
    const k = n >= 30 ? 6 : 5;
    for (let i = 0; i < k; i++) {
      const a = (i / k) * Math.PI * 2 + 0.3;
      d += circ(ri * 0.58 * Math.cos(a), ri * 0.58 * Math.sin(a), ri * 0.19);
    }
  }
  return d;
}

export const Gear: React.FC<{n: number; r: number; x: number; y: number; rot: number; opacity?: number; outline?: boolean; stroke?: string}> = ({n, r, x, y, rot, opacity = 1, outline = false, stroke}) => {
  const depth = Math.max(7, r * 0.13);
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={opacity}>
      <path d={gearPath(n, r, depth)} fillRule="evenodd" fill={outline ? 'none' : 'url(#bronze)'} stroke={stroke || (outline ? C.gold : '#2a1606')} strokeWidth={outline ? 3 : 2.5} />
      {!outline && <circle r={r - depth - 3} fill="none" stroke="#F6CF86" strokeOpacity={0.35} strokeWidth={2} />}
    </g>
  );
};

// engrane acoplado: devuelve rotación del 2º para que encajen
export const meshRot = (n1: number, n2: number, rot1: number, phi: number) => phi + 180 + 180 / n2 - (n1 / n2) * (rot1 - phi);

export const Moon: React.FC<{x: number; y: number; r: number; p: number}> = ({x, y, r, p}) => {
  const ang = p * Math.PI * 2;
  const c = Math.cos(ang);
  const rx = Math.abs(c) * r;
  const waxing = p % 1 < 0.5;
  const lit = '#F4EAD0';
  const dark = '#1b2038';
  const half = waxing ? `M 0 ${-r} A ${r} ${r} 0 0 1 0 ${r} Z` : `M 0 ${-r} A ${r} ${r} 0 0 0 0 ${r} Z`;
  return (
    <g transform={`translate(${x} ${y})`}>
      <circle r={r} fill={dark} />
      <path d={half} fill={lit} />
      <ellipse rx={Math.max(0.01, rx)} ry={r} fill={c < 0 ? lit : dark} />
      <circle r={r} fill="none" stroke="#9fa6c8" strokeOpacity={0.5} strokeWidth={3} />
    </g>
  );
};

export const Dust: React.FC<{t: number; n?: number}> = ({t, n = 46}) => (
  <g>
    {Array.from({length: n}).map((_, i) => {
      const sx = random('dx' + i) * W;
      const sp = 8 + random('ds' + i) * 26;
      const y = ((random('dy' + i) * 1500 - t * sp) % 1500 + 1500) % 1500 + 200;
      const x = sx + Math.sin(t * 0.6 + i) * 18;
      const tw = 0.25 + 0.5 * Math.abs(Math.sin(t * 1.3 + i * 2.1));
      return <circle key={i} cx={x} cy={y} r={1.4 + random('dr' + i) * 2.6} fill="#F7E3B0" opacity={tw * 0.5} />;
    })}
  </g>
);

export const Txt: React.FC<{x: number; y: number; size: number; fill?: string; weight?: number; family?: string; anchor?: 'start' | 'middle' | 'end'; spacing?: number; opacity?: number; rotate?: number; children: React.ReactNode}> = ({x, y, size, fill = C.cream, weight = 800, family = 'Inter', anchor = 'middle', spacing = 0, opacity = 1, rotate = 0, children}) => (
  <text x={x} y={y} fontSize={size} fill={fill} fontWeight={weight} fontFamily={family} textAnchor={anchor} letterSpacing={spacing} opacity={opacity} transform={rotate ? `rotate(${rotate} ${x} ${y})` : undefined}>
    {children}
  </text>
);

export const typed = (s: string, t: number, a: number, b: number) => s.slice(0, Math.floor(s.length * clamp((t - a) / (b - a))));

export const shake = (t: number, t0: number, amp = 14, dur = 0.5) => {
  const u = t - t0;
  if (u < 0 || u > dur) return {x: 0, y: 0};
  const k = 1 - u / dur;
  return {x: Math.sin(u * 90) * amp * k, y: Math.cos(u * 77) * amp * k};
};

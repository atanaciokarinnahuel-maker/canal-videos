import React from 'react';
import {random} from 'remotion';
import {C, CY, Gear, Moon, Txt, clamp, lerp, ramp, win, eo, eio, back, meshRot, typed, shake, gearPath} from './lib';

type P = {t: number};
const rad = (d: number) => (d * Math.PI) / 180;

// ───────── ESCENA 4 · 18.4–29.75 · manivela, Luna, eclipse, Saros ─────────
const train = (() => {
  const defs = [{n: 24, r: 88, phi: 0}, {n: 44, r: 162, phi: -40}, {n: 20, r: 74, phi: -8}, {n: 36, r: 132, phi: -55}];
  const out: {n: number; r: number; x: number; y: number; phi: number}[] = [];
  let x = 190, y = 1130;
  defs.forEach((d, i) => {
    if (i > 0) {
      const p = out[i - 1];
      const dist = p.r + d.r;
      x = p.x + dist * Math.cos(rad(d.phi));
      y = p.y + dist * Math.sin(rad(d.phi));
    }
    out.push({...d, x, y});
  });
  return out;
})();

export const S4: React.FC<P> = ({t}) => {
  const o = win(t, 18.4, 29.75, 0.35, 0.35);
  const spin = Math.max(0, t - 18.8);
  const rot1 = 130 * spin + 20 * Math.min(spin, 1) ** 2;
  const rots: number[] = [rot1];
  for (let i = 1; i < train.length; i++) rots.push(meshRot(train[i - 1].n, train[i].n, rots[i - 1], train[i].phi));
  const trainOp = ramp(t, 18.6, 19.2) * (1 - 0.7 * ramp(t, 22.0, 22.5)) * (1 - 0.1 * ramp(t, 26, 26.5));
  const pulse = 1 + 0.04 * Math.sin(t * 12) * win(t, 21.1, 21.7, 0.1, 0.2);
  // manivela
  const k0 = train[0];
  const ka = rad(rot1 + 200);
  const kx = k0.x + Math.cos(ka) * 150, ky = k0.y + Math.sin(ka) * 150;
  // Luna
  const moonOp = win(t, 21.95, 23.75, 0.25, 0.3);
  const moonP = clamp((t - 22.0) / 1.7) % 1;
  // eclipse
  const eclOp = win(t, 23.75, 26.1, 0.3, 0.4);
  const mx = lerp(150, 560, ramp(t, 24.0, 25.2, eio)) + ramp(t, 25.3, 26.1) * 60;
  const covered = 1 - clamp(Math.abs(mx - 540) / 130);
  const corona = ramp(t, 25.0, 25.4) * (1 - ramp(t, 25.4, 26.1));
  // Saros
  const sarOp = win(t, 26.2, 29.75, 0.35, 0.4);
  const dots = Math.round(223 * ramp(t, 27.2, 28.9, eio));
  const spirals = Array.from({length: 223}).map((_, i) => {
    const th = i * 0.19;
    const rr = 26 + th * 6.2;
    return {x: 540 + rr * Math.cos(th), y: 540 + rr * Math.sin(th), i};
  });
  return (
    <g opacity={o}>
      {/* tren de engranajes */}
      <g opacity={trainOp} transform={`translate(${k0.x} ${k0.y}) scale(${pulse}) translate(${-k0.x} ${-k0.y})`}>
        {train.map((g, i) => <Gear key={i} n={g.n} r={g.r} x={g.x} y={g.y} rot={rots[i]} />)}
        <line x1={k0.x} y1={k0.y} x2={kx} y2={ky} stroke="#F6CF86" strokeWidth={14} strokeLinecap="round" />
        <circle cx={kx} cy={ky} r={30} fill="url(#bronze)" stroke="#2a1606" strokeWidth={4} />
        <circle cx={k0.x} cy={k0.y} r={14} fill="#2a1606" />
      </g>
      <g opacity={ramp(t, 19.5, 19.9) * (1 - ramp(t, 22, 22.4))}>
        <Txt x={190} y={1272} size={36} weight={900} fill={C.gold} spacing={6}>MANIVELA</Txt>
      </g>
      <g opacity={ramp(t, 19.6, 20.0) * (1 - ramp(t, 21.9, 22.2))} transform={`translate(540 430) scale(${lerp(1.4, 1, ramp(t, 19.6, 20.0, back))})`}>
        <Txt x={0} y={0} size={84} weight={900} fill={C.cream}>UNA MANIVELA</Txt>
        <Txt x={0} y={92} size={84} weight={900} fill={C.gold}>MUEVE TODO</Txt>
      </g>
      {/* fases lunares */}
      <g opacity={moonOp}>
        <circle cx={540} cy={560} r={200} fill="none" stroke={C.gold} strokeWidth={8} />
        {Array.from({length: 36}).map((_, i) => (
          <line key={i} x1={540 + 206 * Math.cos(rad(i * 10))} y1={560 + 206 * Math.sin(rad(i * 10))} x2={540 + 226 * Math.cos(rad(i * 10))} y2={560 + 226 * Math.sin(rad(i * 10))} stroke={C.gold} strokeWidth={i % 3 === 0 ? 6 : 3} />
        ))}
        <Moon x={540} y={560} r={150} p={moonP} />
        <Txt x={540} y={850} size={48} weight={900} fill={C.cream} spacing={7}>FASES DE LA LUNA</Txt>
      </g>
      {/* eclipse */}
      <g opacity={eclOp}>
        <circle cx={540} cy={560} r={150 + 230 * corona} fill="url(#glowGold)" opacity={0.5 + 0.5 * corona} />
        <g transform={`translate(540 560) rotate(${t * 12})`}>
          {Array.from({length: 24}).map((_, i) => (
            <polygon key={i} points={`-10,-170 10,-170 0,${-230 - (i % 2) * 36}`} fill={C.gold} opacity={0.8} transform={`rotate(${i * 15})`} />
          ))}
        </g>
        <circle cx={540} cy={560} r={140} fill="url(#goldDisc)" />
        <circle cx={mx} cy={560} r={136} fill="#05060d" />
        <circle cx={540} cy={560} r={144 + 16 * corona} fill="none" stroke="#fff" strokeOpacity={0.9 * corona} strokeWidth={5} />
        <Txt x={540} y={850} size={56} weight={900} fill={C.cream} spacing={8}>ECLIPSE</Txt>
        <Txt x={540} y={905} size={32} weight={700} fill={C.gold} spacing={5} opacity={covered}>SOL · LUNA · TIERRA ALINEADOS</Txt>
      </g>
      {/* Saros */}
      <g opacity={sarOp}>
        {spirals.filter((s) => s.i < dots).map((s) => (
          <circle key={s.i} cx={s.x} cy={s.y} r={s.i === dots - 1 ? 10 : 5.5} fill={s.i === dots - 1 ? '#fff' : C.gold} opacity={0.55 + 0.45 * (s.i / 223)} />
        ))}
        <circle cx={540} cy={540} r={12 + 4 * Math.sin(t * 6)} fill={C.gold} />
        <Txt x={540} y={1000} size={170} weight={900} fill={C.gold}>{dots}</Txt>
        <Txt x={540} y={1060} size={38} weight={800} fill={C.cream} spacing={6}>MESES LUNARES · CICLO SAROS</Txt>
        <g opacity={ramp(t, 28.9, 29.3)}>
          <Txt x={540} y={1130} size={44} weight={700} fill={C.gold}>≈ 18 años y 11 días</Txt>
        </g>
      </g>
    </g>
  );
};

// ───────── ESCENA 5 · 29.7–37.45 · tomografía 2005 ─────────
const slab = (() => {
  const pts = Array.from({length: 14}).map((_, i) => {
    const a = (i / 14) * Math.PI * 2;
    const rx = 240 + random('sl' + i) * 40, ry = 300 + random('sm' + i) * 40;
    return [rx * Math.cos(a), ry * Math.sin(a)];
  });
  return pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
})();
const greek = ['ΑΒΓΔΕΖΗΘΙΚΛΜ', 'ΝΞΟΠΡΣΤΥΦΧΨΩ', 'ΚΑΙΤΟΥΗΛΙΟΥ', 'ΜΗΝΩΝΚΥΚΛΟΣ', 'ΣΕΛΗΝΗΣΟΔΟΣ', 'ΑΣΤΕΡΩΝΔΡΟΜΟΙ'];

export const S5: React.FC<P> = ({t}) => {
  const o = win(t, 29.7, 37.45, 0.35, 0.4);
  const scan = t < 33.0 ? ramp(t, 30.3, 33.0, eio) : 1 - ramp(t, 33.2, 35.0, eio) * 0.0;
  const scanY = lerp(-330, 330, scan);
  const sy = t >= 33.0 ? lerp(330, -330, ramp(t, 33.0, 35.2, eio)) : scanY;
  const revealTo = t < 33.0 ? scanY : 330;
  const title = typed('TOMOGRAFÍA DE RAYOS X · 2005', t, 29.9, 30.9);
  return (
    <g opacity={o}>
      <Txt x={540} y={370} size={46} weight={900} fill="#8ff0dc" spacing={4}>{title}</Txt>
      <g transform={`translate(540 ${CY - 10})`}>
        <circle r={430} fill="url(#glowTeal)" opacity={0.5} />
        {/* losa de bronce */}
        <polygon points={slab} fill="url(#bronze)" stroke="#2a1606" strokeWidth={5} />
        <polygon points={slab} fill="rgba(70,179,160,0.25)" />
        {Array.from({length: 34}).map((_, i) => (<circle key={i} cx={(random('tx' + i) - 0.5) * 420} cy={(random('ty' + i) - 0.5) * 520} r={5 + random('tr' + i) * 14} fill={random('tc' + i) > 0.5 ? '#6f8f75' : '#5a3414'} opacity={0.55} />))}
        {/* capa de rayos X: aparece donde pasa el escáner */}
        <clipPath id="xr"><rect x={-300} y={-330} width={600} height={Math.max(0.01, revealTo + 330)} /></clipPath>
        <g clipPath="url(#xr)">
          <polygon points={slab} fill="#031a1a" opacity={0.92} />
          <Gear n={22} r={110} x={-90} y={-130} rot={t * 30} outline stroke="#6ff2d8" />
          <Gear n={30} r={140} x={110} y={140} rot={-t * 22} outline stroke="#6ff2d8" />
          <Gear n={14} r={66} x={-110} y={170} rot={t * 50} outline stroke="#6ff2d8" />
          {greek.map((g, i) => {
            const on = ramp(t, 32.6 + i * 0.32, 32.9 + i * 0.32);
            return <Txt key={i} x={0} y={-150 + i * 62} size={44} family="GFS Baskerville" weight={700} fill="#c5fff4" spacing={9} opacity={0.3 + 0.7 * on}>{g}</Txt>;
          })}
        </g>
        {/* línea del escáner */}
        <g opacity={ramp(t, 30.3, 30.6) * (1 - ramp(t, 35.1, 35.5))}>
          <rect x={-330} y={sy - 6} width={660} height={12} rx={6} fill="#c5fff4" />
          <rect x={-330} y={sy - 40} width={660} height={80} fill="url(#scanGlow)" />
        </g>
      </g>
      <g opacity={ramp(t, 32.7, 33.1) * (1 - ramp(t, 35.3, 35.7))}>
        <Txt x={540} y={1190} size={38} weight={800} fill="#8ff0dc" spacing={5}>INSCRIPCIONES GRIEGAS OCULTAS</Txt>
        <Txt x={540} y={1232} size={24} weight={600} fill={C.cream} opacity={0.6}>(texto ilustrativo)</Txt>
      </g>
      {/* manual */}
      <g opacity={ramp(t, 35.4, 35.8)} transform={`translate(540 1130) scale(${lerp(0.5, 1, ramp(t, 35.4, 35.9, back))})`}>
        <rect x={-190} y={-70} width={380} height={140} rx={22} fill="#0b1c25" stroke={C.gold} strokeWidth={5} />
        <line x1={0} y1={-60} x2={0} y2={60} stroke={C.gold} strokeWidth={4} />
        {[0, 1, 2].map((i) => (<React.Fragment key={i}><line x1={-160} y1={-34 + i * 34} x2={-30} y2={-34 + i * 34} stroke={C.cream} strokeWidth={6} strokeLinecap="round" opacity={0.8} /><line x1={30} y1={-34 + i * 34} x2={160} y2={-34 + i * 34} stroke={C.cream} strokeWidth={6} strokeLinecap="round" opacity={0.8} /></React.Fragment>))}
        <Txt x={0} y={118} size={36} weight={900} fill={C.gold} spacing={6}>¿UN MANUAL?</Txt>
      </g>
    </g>
  );
};

// ───────── ESCENA 6 · 37.4–44.6 · hipótesis 2021 ─────────
const planets = [
  {name: 'MERCURIO', r: 92, col: '#c7c7d1', sp: 70},
  {name: 'VENUS', r: 154, col: '#f4e3b6', sp: 45},
  {name: 'MARTE', r: 216, col: '#e4572e', sp: 31},
  {name: 'JÚPITER', r: 278, col: '#f0a35c', sp: 19},
  {name: 'SATURNO', r: 340, col: '#F2C46D', sp: 12},
];
export const S6: React.FC<P> = ({t}) => {
  const o = win(t, 37.4, 44.6, 0.35, 0.4);
  const hyp = ramp(t, 42.2, 42.5);
  const stamp = ramp(t, 42.72, 42.98, back);
  const sk = shake(t, 42.72, 18, 0.5);
  const title = typed('UCL · 2021 · MODELO PROPUESTO', t, 37.7, 38.7);
  return (
    <g opacity={o} transform={`translate(${sk.x} ${sk.y})`}>
      <Txt x={540} y={370} size={46} weight={900} fill="#b7c3ff" spacing={4}>{title}</Txt>
      <g transform={`translate(540 ${CY - 30})`}>
        <circle r={430} fill="url(#glowIndigo)" opacity={0.7} />
        {planets.map((p, i) => {
          const on = ramp(t, 39.1 + i * 0.5, 39.5 + i * 0.5);
          const ang = rad(-90 + (t - 37) * p.sp + i * 70);
          return (
            <g key={i} opacity={on}>
              <circle r={p.r * on} fill="none" stroke={p.col} strokeOpacity={0.75 - 0.35 * hyp} strokeWidth={4} strokeDasharray={hyp > 0.5 ? '10 14' : undefined} />
              <circle cx={p.r * Math.cos(ang)} cy={p.r * Math.sin(ang)} r={13 + (i === 4 ? 4 : 0)} fill={p.col} opacity={1 - 0.25 * hyp} />
            </g>
          );
        })}
        <circle r={26} fill="#4aa3ff" /><circle r={26} fill="none" stroke="#bfe0ff" strokeWidth={4} />
        {/* leyenda de planetas */}
        {planets.map((p, i) => (
          <g key={i} opacity={ramp(t, 39.4 + i * 0.5, 39.8 + i * 0.5)}>
            <circle cx={-395 + i * 193} cy={442} r={9} fill={p.col} />
            <Txt x={-377 + i * 193} y={450} size={24} weight={800} fill={p.col} anchor="start" spacing={1}>{p.name}</Txt>
          </g>
        ))}
      </g>
      {/* sello */}
      <g opacity={stamp} transform={`translate(540 ${CY - 30}) rotate(-9) scale(${lerp(2.4, 1, stamp)})`}>
        <rect x={-330} y={-92} width={660} height={184} rx={14} fill="rgba(10,15,31,0.82)" stroke={C.red} strokeWidth={12} />
        <rect x={-312} y={-76} width={624} height={152} rx={8} fill="none" stroke={C.red} strokeWidth={3} />
        <Txt x={0} y={38} size={118} weight={900} fill={C.red} spacing={6}>HIPÓTESIS</Txt>
      </g>
      <g opacity={ramp(t, 43.55, 43.85)} transform={`translate(540 1000) scale(${lerp(1.5, 1, ramp(t, 43.55, 43.9, back))})`}>
        <Txt x={0} y={0} size={60} weight={900} fill={C.cream}>NO ES UNA PRUEBA</Txt>
      </g>
    </g>
  );
};

// ───────── ESCENA 7 · 44.5–53.7 · la pregunta ─────────
export const S7: React.FC<P> = ({t}) => {
  const o = ramp(t, 44.45, 44.9);
  const qs = ramp(t, 44.6, 45.2, back);
  const flash = ramp(t, 46.6, 46.75) * (1 - ramp(t, 46.75, 47.6));
  const ghosts = Array.from({length: 9}).map((_, i) => {
    const gx = 100 + random('gx' + i) * 880, gy = 360 + random('gy' + i) * 900;
    const lifeStart = 48.3 + i * 0.12;
    return {gx, gy, n: 14 + Math.floor(random('gn' + i) * 30), r: 50 + random('gr' + i) * 70, on: ramp(t, 44.8 + i * 0.1, 45.3 + i * 0.1) * (1 - ramp(t, lifeStart + 0.5, lifeStart + 1.4))};
  });
  const cta = ramp(t, 50.05, 50.4);
  const qOn = ramp(t, 46.55, 46.85, back) * (1 - ramp(t, 49.9, 50.1));
  const q2On = ramp(t, 48.35, 48.7, back) * (1 - ramp(t, 49.9, 50.1));
  const sk = shake(t, 46.6, 12, 0.4);
  return (
    <g opacity={o} transform={`translate(${sk.x} ${sk.y})`}>
      {ghosts.map((g, i) => (<Gear key={i} n={g.n} r={g.r} x={g.gx} y={g.gy} rot={t * (i % 2 ? 20 : -20)} outline opacity={0.35 * g.on} />))}
      <circle cx={540} cy={CY - 30} r={380 + 120 * flash} fill="url(#glowGold)" opacity={0.35 + 0.5 * flash} />
      <g opacity={lerp(1, 0.28, cta)} transform={`translate(540 ${CY + 215}) scale(${qs})`}>
        <Txt x={0} y={0} size={560} family="GFS Baskerville" weight={700} fill={C.gold}>?</Txt>
      </g>
      <g opacity={qOn} transform={`translate(540 440) scale(${lerp(1.4, 1, qOn)})`}>
        <Txt x={0} y={0} size={96} weight={900} fill={C.cream}>¿QUIÉN LA</Txt>
        <Txt x={0} y={100} size={96} weight={900} fill={C.gold}>CONSTRUYÓ?</Txt>
      </g>
      <g opacity={q2On} transform={`translate(540 1135) scale(${lerp(1.4, 1, q2On)})`}>
        <Txt x={0} y={0} size={58} weight={900} fill={C.cream}>¿CUÁNTAS MÁS</Txt>
        <Txt x={0} y={66} size={58} weight={900} fill={C.red}>SE PERDIERON?</Txt>
      </g>
      {/* CTA */}
      <g opacity={cta} transform={`translate(540 560) scale(${lerp(0.5, 1, ramp(t, 50.05, 50.5, back))})`}>
        <path d="M-210 -100 h420 a46 46 0 0 1 46 46 v108 a46 46 0 0 1 -46 46 h-250 l-70 70 v-70 h-100 a46 46 0 0 1 -46 -46 v-108 a46 46 0 0 1 46 -46 z" fill="#101a33" stroke={C.gold} strokeWidth={8} transform="translate(-20 -20)" />
        {[0, 1, 2].map((i) => (<circle key={i} cx={-70 + i * 70} cy={-4} r={20} fill={C.gold} opacity={0.4 + 0.6 * Math.abs(Math.sin(t * 5 - i * 0.9))} />))}
      </g>
      <g opacity={ramp(t, 50.9, 51.2)}>
        <Txt x={540} y={870} size={72} weight={900} fill={C.cream}>COMENTA TU TEORÍA</Txt>
      </g>
      <g opacity={ramp(t, 51.35, 51.65)} transform={`translate(540 1030) scale(${1 + 0.05 * Math.sin(t * 8) * ramp(t, 51.7, 51.8)})`}>
        <rect x={-300} y={-62} width={600} height={124} rx={62} fill={C.red} />
        <path d="M-210 -26 l46 26 l-46 26 z" fill="#fff" />
        <Txt x={45} y={18} size={46} weight={900} fill="#fff">SIGUE EL CANAL</Txt>
      </g>
    </g>
  );
};

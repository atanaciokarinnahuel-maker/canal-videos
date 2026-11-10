import '@react-three/fiber';
import {B, C, V3, at, cl, key, pulse, ramp, sm} from '../tl';
import {Glory, LightCross, PathLight} from './Glory';
import {Figure, Glow, Gold, Motes, Obsidian, Priest} from './Props';
import {VEIL, Veil} from './Veil';

/* ───────────── Anclas de la locución ───────────── */
export const A = {
  colA: at(1, 'Azul'), colB: at(1, 'púrpura'), colC: at(1, 'carmesí'), colEnd: at(1, 'Una obra de arte'),
  fig2: at(2, 'Isaías lo explica'), us: at(2, 'El problema éramos nosotros'),
  priestIn: at(3, 'Uno solo'), warn: at(3, 'no entres en cualquier momento'), warnEnd: at(3, 'Ese día se lavaba'),
  cross: at(3, 'y cruzaba el velo'), priestOut: at(3, 'Y cuando el sacerdote salía'), closeAgain: at(3, 'el velo se cerraba'),
  path: at(4, 'Y el Espíritu Santo'), notYet: at(4, 'todavía no'), shadow: at(4, 'Todo era una sombra'), better: at(4, 'De Alguien mejor'),
  pre: at(5, 'En ese mismo instante'), tear0: at(5, 'el velo se rasga'), tear1: at(5, 'Piénsalo'),
  hands: at(5, 'desde donde alcanzan'), topA: at(5, 'Pero empezó arriba'), godTore: at(5, 'Lo rasgó Dios'), descend: at(5, 'fue Dios bajando'),
  newWay: at(6, 'el camino nuevo'),
  fly: B(7), throne: at(7, 'Un trono'), grace: at(7, 'Un trono de gracia'), priestFade: at(7, 'Ya no tienes que buscar'), via: at(7, 'Por medio de Jesucristo'),
  way: at(8, 'yo soy el camino'), walk: at(8, 'Cree en Él'), ask: at(8, 'Y dime'),
};

/* ───────────── Estado del santuario en el tiempo ───────────── */
export type HallMode = 'flash' | 'priestLoop' | 'priestFade' | undefined;

export const hallState = (t: number, mode?: string) => {
  let front = t < A.tear0 ? 99 : key(t, [A.tear0, A.tear1], [VEIL.height + 0.3, -1.6], (u) => Math.pow(u, 1.25));
  let part = t < A.tear0 ? 0 : key(t, [A.tear0, A.tear1, A.godTore, A.godTore + 1.6, A.fly, A.fly + 3.2], [0.035, 0.07, 0.09, 0.27, 0.27, 1], sm);
  let glory = key(t, [A.tear0, A.tear0 + 0.25, A.tear0 + 1.2, A.godTore, A.godTore + 0.4, A.godTore + 2.2, A.fly, A.fly + 3, A.throne + 2], [0, 1.7, 0.95, 1.0, 2.1, 1.3, 1.3, 2.0, 1.55]);
  let gust = key(t, [A.tear0, A.tear0 + 0.5, A.tear1 + 2, A.godTore, A.godTore + 0.5, A.godTore + 4], [0, 1, 0.25, 0.25, 1, 0.2]);
  if (mode === 'priestLoop' || mode === 'priestFade') {
    // recuerdo: el velo todavía cerrado
    front = 99;
    part = 0;
    glory = 0;
    gust = 0;
  }
  if (mode === 'flash') {
    front = 4.2;
    part = 0.05;
    glory = 1.5;
    gust = 0.8;
  }
  const warn = t > A.warn - 0.1 && t < A.warnEnd ? 0.55 + 0.45 * Math.sin((t - A.warn) * 9) : 0;
  const tintK = Math.max(pulse(t, A.colA, 0.1, 0.9), pulse(t, A.colB, 0.1, 0.9), pulse(t, A.colC, 0.1, 1.2));
  const tint = t < A.colB ? '#3558ff' : t < A.colC ? '#9a3be0' : '#e0283a';
  const closeDim = pulse(t, A.closeAgain + 0.55, 0.08, 1.4);
  const pre = t >= A.pre && t < A.tear0 ? sm(ramp(t, A.pre, A.pre + 0.8)) : 0;
  const dim = cl(1 - closeDim * 0.55 - pre * 0.6);
  const path = t < A.path ? 0 : t < B(5) ? key(t, [A.path, A.notYet], [0, 1], sm) : t >= A.newWay ? key(t, [A.newWay, A.newWay + 2.2], [1, 2], sm) : 0;
  const shadow = t >= A.shadow && t < A.tear0 ? sm(ramp(t, A.shadow, A.shadow + 1)) * (1 + pulse(t, A.better, 0.2, 1.5)) : 0;
  const inside = mode === 'priestLoop' || mode === 'priestFade' ? 0 : sm(ramp(t, A.fly + 0.5, A.fly + 4));
  return {front, part, glory, gust, warn, tint, tintK, dim, path, shadow, inside};
};

/** Posición del sumo sacerdote (z). null = fuera de escena. */
export const priestState = (t: number, mode?: string): {z: number; alpha: number} | null => {
  if (mode === 'priestLoop') return {z: 15 - ((t * 1.7) % 13), alpha: 1};
  if (mode === 'priestFade') return {z: 8, alpha: 1 - sm(ramp(t, A.priestFade + 0.9, A.priestFade + 2.8))};
  if (t >= A.priestIn - 0.1 && t < A.priestOut) return {z: key(t, [A.priestIn, A.cross + 1.4], [17, 1.9], sm), alpha: 1};
  if (t >= A.priestOut && t < A.closeAgain + 3) return {z: key(t, [A.priestOut, A.closeAgain + 2.5], [2, 9.5]), alpha: 1};
  return null;
};

/** La persona (tú): dónde está y cómo la toca la luz. */
export const figureState = (t: number): {pos: V3; reach: number; red: number; lit: number} | null => {
  if (t >= A.fig2 && t < B(3)) return {pos: [0, 0, 5], reach: 0, red: sm(ramp(t, A.us - 0.2, A.us + 0.6)), lit: 0};
  if (t >= A.pre && t < B(6)) {
    const reach = sm(ramp(t, A.hands - 0.6, A.hands + 0.5)) * (1 - sm(ramp(t, A.topA + 0.2, A.topA + 1)));
    return {pos: [0, 0, 2.3], reach, red: 0, lit: sm(ramp(t, A.descend, A.descend + 1.6))};
  }
  if (t >= A.via && t < B(8)) return {pos: [0, 0, key(t, [A.via, B(8)], [-5, -13])], reach: 0, red: 0, lit: 1};
  if (t >= B(8)) return {pos: [0, 0, key(t, [A.walk + 0.2, A.walk + 5.5, A.ask + 6], [4.2, -8, -12], sm)], reach: 0, red: 0, lit: sm(ramp(t, A.walk, A.walk + 3))};
  return null;
};

/* ───────────── Arquitectura ───────────── */
const PILLAR_Z = [3.2, 7.4, 11.6, 15.8, 20, 24.2, 28.4];
const Pillar: React.FC<{x: number; z: number}> = ({x, z}) => (
  <group position={[x, 0, z]}>
    <mesh position={[0, 8, 0]}>
      <boxGeometry args={[1.1, 16, 1.1]} />
      <Obsidian />
    </mesh>
    <mesh position={[0, 0.12, 0]}>
      <boxGeometry args={[1.32, 0.24, 1.32]} />
      <Gold />
    </mesh>
    <mesh position={[0, 7.2, 0]}>
      <boxGeometry args={[1.16, 0.07, 1.16]} />
      <Gold />
    </mesh>
  </group>
);

const Temple: React.FC = () => {
  const openW = VEIL.halfW - 0.1;
  const topY = VEIL.height - 0.1;
  return (
    <group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -10]}>
        <planeGeometry args={[110, 150]} />
        <meshStandardMaterial color="#07080b" roughness={0.3} metalness={0.8} />
      </mesh>
      {PILLAR_Z.flatMap((z) => [<Pillar key={`l${z}`} x={-5.4} z={z} />, <Pillar key={`r${z}`} x={5.4} z={z} />, <Pillar key={`l2${z}`} x={-10.4} z={z} />, <Pillar key={`r2${z}`} x={10.4} z={z} />])}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * (openW + 25), 15, -0.7]}>
          <boxGeometry args={[50, 30, 1]} />
          <Obsidian />
        </mesh>
      ))}
      <mesh position={[0, topY + 10, -0.7]}>
        <boxGeometry args={[openW * 2, 20, 1]} />
        <Obsidian />
      </mesh>
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * (openW + 0.14), topY / 2, 0]}>
          <boxGeometry args={[0.28, topY, 0.6]} />
          <Gold />
        </mesh>
      ))}
      <mesh position={[0, topY + 0.16, 0]}>
        <boxGeometry args={[openW * 2 + 0.56, 0.32, 0.6]} />
        <Gold />
      </mesh>
    </group>
  );
};

/** El trono de la gracia: oro mate sobre gradas, con la cruz de luz detrás. */
const Throne: React.FC<{k: number}> = ({k}) => (
  <group position={[0, 0, -22]}>
    {[0, 1, 2].map((i) => (
      <mesh key={i} position={[0, 0.2 + i * 0.4, 1.6 - i * 0.7]}>
        <boxGeometry args={[7 - i * 1.2, 0.4, 5 - i * 1.4]} />
        <Obsidian />
      </mesh>
    ))}
    {[0, 1, 2].map((i) => (
      <mesh key={i} position={[0, 0.41 + i * 0.4, 4.1 - i * 1.4]}>
        <boxGeometry args={[7 - i * 1.2, 0.03, 0.06]} />
        <Gold glow={0.4} />
      </mesh>
    ))}
    <mesh position={[0, 1.75, 0.2]}>
      <boxGeometry args={[2.3, 0.5, 1.9]} />
      <Gold glow={0.18} />
    </mesh>
    <mesh position={[0, 3.3, -0.75]}>
      <boxGeometry args={[2.3, 3.6, 0.32]} />
      <Gold glow={0.18} />
    </mesh>
    <mesh position={[0, 5.25, -0.75]}>
      <boxGeometry args={[2.7, 0.3, 0.42]} />
      <Gold glow={0.3} />
    </mesh>
    {[-1, 1].map((s) => (
      <mesh key={s} position={[s * 1.3, 2.3, 0.2]}>
        <boxGeometry args={[0.3, 1.6, 1.9]} />
        <Gold glow={0.18} />
      </mesh>
    ))}
    <LightCross pos={[0, 2.2, -4.5]} h={13.5} k={0.3 * k} color="#ffc97a" />
    <Glow pos={[0, 4.5, -2]} size={[16, 16]} color="#ffdb9a" k={0.3 * k} />
  </group>
);

export const Hall: React.FC<{t: number; mode?: string}> = ({t, mode}) => {
  const s = hallState(t, mode);
  const torn = cl((VEIL.height - s.front) / VEIL.height);
  const k = s.glory * torn;
  const fadeIn = sm(ramp(t, 0, 2));
  const priest = priestState(t, mode);
  const fig = mode ? null : figureState(t);
  const amb = fadeIn * s.dim;
  return (
    <>
      <ambientLight intensity={0.2 * amb} color="#93a4c8" />
      <spotLight position={[0, 17, 10]} angle={0.5} penumbra={1} intensity={950 * amb * (1 - s.warn * 0.5)} color="#9fb2d8" distance={50} decay={1.6} />
      {[-1, 1].map((sd) => (
        <pointLight key={sd} position={[sd * 4.4, 6.5, 2.2]} intensity={26 * amb} color="#ffc26b" distance={14} decay={1.8} />
      ))}
      {[6, 14, 22].map((z) => (
        <pointLight key={z} position={[0, 10, z]} intensity={85 * amb} color="#8ea2cc" distance={20} decay={1.7} />
      ))}
      <pointLight position={[0, 3.2, 3.4]} intensity={170 * s.warn} color={C.crimson} distance={20} decay={1.6} />
      <pointLight position={[0, 5, 4]} intensity={230 * s.tintK} color={s.tint} distance={18} decay={1.5} />
      <pointLight position={[1.5, 6, -15]} intensity={80 * s.inside} color="#ffd9a0" distance={20} decay={1.6} />

      <Temple />
      <Veil s={{time: t, front: s.front, part: s.part, gust: s.gust}} />
      <Glory k={s.glory} front={s.front} part={s.part} />
      <Throne k={Math.max(0.35, s.inside) * (s.glory > 0 ? 1 : 0)} />
      <PathLight reach={s.path} />
      <LightCross pos={[0, 1.2, 0.75]} h={8.4} k={0.34 * s.shadow} />

      {priest ? <Priest pos={[0, 0, priest.z]} opacity={priest.alpha} /> : null}
      {fig ? (
        <>
          <Figure pos={fig.pos} reach={fig.reach} color={fig.lit > 0.5 ? '#3a352c' : '#1b1d25'} emissive="#ffe2ad" glow={fig.lit * 0.35} />
          <pointLight position={[fig.pos[0] + 0.8, 2.2, fig.pos[2] + 1.6]} intensity={30 * fig.red} color={C.crimson} distance={7} decay={1.5} />
          <pointLight position={[fig.pos[0] - 1, 1.8, fig.pos[2] + 2.2]} intensity={5 * amb} color="#9fb2d8" distance={6} decay={1.6} />
        </>
      ) : null}
      <Motes t={t} k={0.1 * fadeIn + k * 0.75} box={[10, 11, 44]} center={[0, 5.5, 2]} count={900} axis={0.55} />
    </>
  );
};

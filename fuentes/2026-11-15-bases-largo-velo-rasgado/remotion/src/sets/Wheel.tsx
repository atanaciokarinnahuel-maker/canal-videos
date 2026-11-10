import '@react-three/fiber';
import {B, C, at, cl, key, pulse, ramp, sm} from '../tl';
import {LightCross} from './Glory';
import {Floor, Glow, Gold, Motes, Obsidian} from './Props';

export const W = {
  in: at(4, 'Aquí hay un problema'), rep: at(4, 'por qué había que repetirlo'), cannot: at(4, 'no puede quitar'), each: at(4, 'Cada año, el mismo'), still: at(4, 'el pecado sigue ahí'),
  notYear: at(6, 'No cada año'), once: at(6, 'una vez para siempre'),
};
const N = 14;
const STEP = (Math.PI * 2) / N;

/** Ángulo de la rueda de los años. */
export const wheelAngle = (t: number) => {
  if (t < B(5)) return 0.9 * Math.max(0, t - W.in) + 2.2 * Math.max(0, t - W.each);
  const stop = W.once + 0.5;
  const tt = Math.min(t, stop);
  return 2.4 * (tt - W.notYear) - (t > W.once ? (2.4 * Math.pow(tt - W.once, 2)) / (2 * 0.5) : 0);
};
/** Contador de años que se muestra en pantalla. */
export const wheelYears = (t: number) => {
  const a1 = 0.9 * Math.max(0, Math.min(t, W.each) - W.in);
  const a2 = 3.1 * Math.max(0, t - W.each);
  return 1 + Math.floor(a1 / STEP) + Math.floor(Math.pow(a2 / STEP, 2.35));
};

/** La rueda: el mismo sacrificio, año tras año, y la mancha que sigue ahí (Heb 10:1-4). */
export const Wheel: React.FC<{t: number}> = ({t}) => {
  const ang = wheelAngle(t);
  const once = t > B(5) ? sm(ramp(t, W.once + 0.2, W.once + 1.6)) : 0;
  const hit = t < B(5) ? (ang / STEP) % 1 : 1;
  const flash = t < B(5) ? Math.pow(1 - hit, 6) : 0;
  const stainK = 1 - once;
  return (
    <>
      <ambientLight intensity={0.16} color="#93a4c8" />
      <spotLight position={[0, 12, 0.1]} angle={0.9} penumbra={1} intensity={260} color="#aab8dc" distance={30} decay={1.6} />
      <pointLight position={[0, 2.6, 0]} intensity={30 * flash + 6} color={C.crimson} distance={12} decay={1.5} />
      <pointLight position={[0, 3, 0]} intensity={120 * once} color="#ffe0a0" distance={24} decay={1.5} />
      <Floor />
      {Array.from({length: N}).map((_, i) => {
        const a = i * STEP + ang;
        const r = 8.5;
        return (
          <group key={i} position={[Math.sin(a) * r, -once * 7, Math.cos(a) * r]} rotation={[0, a + Math.PI, 0]}>
            {[-1, 1].map((s) => (
              <mesh key={s} position={[s * 1.1, 1.6, 0]}>
                <boxGeometry args={[0.12, 3.2, 0.2]} />
                <Gold glow={0.15} />
              </mesh>
            ))}
            <mesh position={[0, 3.26, 0]}>
              <boxGeometry args={[2.44, 0.14, 0.2]} />
              <Gold glow={0.15} />
            </mesh>
            <mesh position={[0, 1.6, 0]}>
              <boxGeometry args={[2.08, 3.2, 0.04]} />
              <meshStandardMaterial color="#2c1546" roughness={0.9} emissive="#3a1a62" emissiveIntensity={0.35} />
            </mesh>
          </group>
        );
      })}
      {/* la mancha: el pecado que sigue ahí */}
      <mesh position={[0, 0.5, 0]}>
        <cylinderGeometry args={[0.55, 0.7, 1, 24]} />
        <Obsidian />
      </mesh>
      <mesh position={[0, 1.55, 0]} scale={stainK + 0.001}>
        <icosahedronGeometry args={[0.5, 1]} />
        <meshStandardMaterial color="#120406" roughness={0.5} metalness={0.3} emissive="#5a0a10" emissiveIntensity={0.5 + flash * 0.6} flatShading />
      </mesh>
      {t < B(5) && hit < 0.5 ? (
        <mesh position={[0, 1.95 + (1 - hit * 2) * 2.4, 0]}>
          <sphereGeometry args={[0.07, 10, 10]} />
          <meshBasicMaterial color="#ff2a36" toneMapped={false} />
        </mesh>
      ) : null}
      <Glow pos={[0, 1.6, 0]} size={3.2} color="#ff2030" k={0.5 * flash * stainK} />
      <LightCross pos={[0, 0.9, 0]} h={5} k={0.9 * once} />
      <Glow pos={[0, 3.2, 0]} size={12} color="#ffdb9a" k={0.45 * once} />
      <Motes t={t} k={0.3 + once} box={[14, 7, 14]} center={[0, 3.5, 0]} count={300} axis={0.15} />
    </>
  );
};

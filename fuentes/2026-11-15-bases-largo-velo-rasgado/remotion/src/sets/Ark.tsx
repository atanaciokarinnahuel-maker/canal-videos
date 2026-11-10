import '@react-three/fiber';
import {C, at, pulse, ramp, sm} from '../tl';
import {Floor, Glow, Gold, Motes, Obsidian, Priest} from './Props';

const K = {
  meet: at(1, 'Allí, dijo Dios'), cloud: at(3, 'envuelto en una nube'), blood: at(3, 'y con sangre'),
  b1: at(3, 'Sangre por sus propios'), b2: at(3, 'Y sangre por los del pueblo'), never: at(3, 'Nunca sin sangre'),
};

/** El arca del pacto y el propiciatorio, entre dos querubines (Éx 25:17-22). */
export const Ark: React.FC<{t: number; mode?: string}> = ({t, mode}) => {
  const ritual = mode === 'ritual';
  const meet = ritual ? 0.55 : 0.35 + 0.9 * sm(ramp(t, K.meet, K.meet + 1.6));
  const cloud = ritual ? sm(ramp(t, K.cloud - 0.4, K.cloud + 1.5)) : 0;
  const blood = ritual ? Math.max(pulse(t, K.blood, 0.15, 1.3), pulse(t, K.b1 + 0.5, 0.15, 1.3), pulse(t, K.b2 + 0.6, 0.15, 1.3), pulse(t, K.never, 0.15, 1.6)) : 0;
  const drops = ritual ? [K.b1 + 0.3, K.b2 + 0.4] : [];
  return (
    <>
      <ambientLight intensity={0.12} color="#93a4c8" />
      <spotLight position={[0, 9, 4]} angle={0.5} penumbra={1} intensity={130} color="#ffe2b0" distance={22} decay={1.6} />
      <pointLight position={[0, 2.0, 0]} intensity={16 * meet} color="#fff3d2" distance={9} decay={1.6} />
      <pointLight position={[1.2, 1.4, 2]} intensity={34 * blood} color={C.crimson} distance={9} decay={1.5} />
      <Floor />
      <mesh position={[0, 5, -3.2]}>
        <boxGeometry args={[14, 10, 0.3]} />
        <Gold glow={0.03} />
      </mesh>
      <mesh position={[0, 0.15, 0]}>
        <boxGeometry args={[2.6, 0.3, 1.8]} />
        <Obsidian />
      </mesh>
      <mesh position={[0, 0.76, 0]}>
        <boxGeometry args={[1.6, 0.92, 0.92]} />
        <Gold glow={0.12} />
      </mesh>
      <mesh position={[0, 1.26, 0]}>
        <boxGeometry args={[1.72, 0.09, 1.02]} />
        <Gold glow={0.2} />
      </mesh>
      {[-0.52, 0.52].map((z) => (
        <mesh key={z} position={[0, 0.5, z]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.035, 0.035, 2.9, 12]} />
          <Gold glow={0.15} />
        </mesh>
      ))}
      {[-1, 1].map((s) => (
        <group key={s} position={[s * 0.62, 1.3, 0]}>
          <mesh position={[0, 0.27, 0]}>
            <boxGeometry args={[0.15, 0.54, 0.2]} />
            <Gold glow={0.2} />
          </mesh>
          <mesh position={[0, 0.62, 0]}>
            <sphereGeometry args={[0.09, 14, 10]} />
            <Gold glow={0.2} />
          </mesh>
          {[-1, 1].map((w) => (
            <group key={w} position={[-s * 0.05, 0.5, w * 0.12]} rotation={[0, 0, s * 0.62]}>
              <mesh position={[-s * 0.36, 0, w * 0.1]}>
                <boxGeometry args={[0.74, 0.035, 0.3]} />
                <Gold glow={0.25} />
              </mesh>
            </group>
          ))}
        </group>
      ))}
      <Glow pos={[0, 1.85, 0]} size={2.6} color="#fff0c8" k={0.55 * meet} />
      <Glow pos={[0, 1.7, 0]} size={7} color="#ffd590" k={0.16 * meet} />
      {ritual ? <Priest pos={[1.9, 0, 1.7]} /> : null}
      {/* la sangre rociada */}
      {drops.flatMap((t0, d) =>
        [0, 1, 2, 3, 4, 5, 6].map((i) => {
          const u = (t - t0 - i * 0.07) / 0.55;
          if (u < 0 || u > 1) return null;
          const x = 1.6 - u * (1.3 + (i % 3) * 0.2);
          const y = 1.3 + Math.sin(u * Math.PI) * 0.5 - u * 0.2;
          const z = 1.5 - u * (1.0 + (i % 2) * 0.25);
          return (
            <mesh key={`${d}-${i}`} position={[x, y, z]}>
              <sphereGeometry args={[0.035, 8, 8]} />
              <meshBasicMaterial color="#ff2a36" toneMapped={false} />
            </mesh>
          );
        }),
      )}
      {/* nube de incienso */}
      <Motes t={t * 2.2} k={cloud * 0.2} box={[5, 3.4, 4]} center={[0.4, 1.7, 0.8]} count={260} axis={0.05} color="#d9d2c4" size={3.2} />
      <Motes t={t} k={0.3} box={[8, 5, 8]} center={[0, 2.5, 0]} count={220} axis={0.2} size={0.7} />
    </>
  );
};

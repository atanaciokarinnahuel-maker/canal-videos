import '@react-three/fiber';
import {B, C, at, key, pulse, ramp, sm} from '../tl';
import {Floor, Glow, Gold, Motes} from './Props';

const M = {
  court: at(1, 'Afuera, el atrio'), altar: at(1, 'con el altar'), holy: at(1, 'Adentro, el Lugar Santo'), lamps: at(1, 'un candelabro'),
  holiest: at(1, 'Y al fondo'), gone: at(7, 'Ya no tienes que ir'),
};
const POSTS: [number, number][] = [];
for (let z = -5; z <= 5; z += 1.25) POSTS.push([-2.5, z], [2.5, z]);
for (let x = -1.25; x <= 1.25; x += 1.25) POSTS.push([x, -5], [x, 5]);

/** Maqueta del tabernáculo: atrio, Lugar Santo y Lugar Santísimo (Éx 26-27; 40). */
export const Model: React.FC<{t: number; mode?: string}> = ({t, mode}) => {
  const gone = mode === 'gone' ? sm(ramp(t, M.gone + 0.6, M.gone + 3.4)) : 0;
  const zone = t < M.court ? 0 : t < M.holy ? 1 : t < M.holiest ? 2 : 3;
  const z1 = t < B(2) ? (zone === 1 ? 1 : zone === 0 ? 0.6 : 0.2) : 0.6;
  const z2 = t < B(2) ? (zone === 2 ? 1 : zone === 0 ? 0.6 : 0.18) : 0.6;
  const z3 = t < B(2) ? (zone === 3 ? 1 : zone === 0 ? 0.6 : 0.3) : 0.6;
  const ember = 0.6 + 0.4 * Math.sin(t * 9) + pulse(t, M.altar, 0.15, 1.5) * 2;
  const lit = t < B(2) ? Math.floor(key(t, [M.lamps, M.lamps + 1.6], [0, 7.99])) : 7;
  const fade = 1 - gone * 0.75;
  return (
    <>
      <ambientLight intensity={0.25 * fade} color="#93a4c8" />
      <directionalLight position={[6, 10, 5]} intensity={0.9 * fade} color="#b9c6e6" />
      <pointLight position={[0, 3, 2.5]} intensity={22 * z1 * fade} color="#cfdcff" distance={10} decay={1.6} />
      <pointLight position={[0, 1.6, -1.9]} intensity={7 * z2 * fade} color="#ffc977" distance={5} decay={1.6} />
      <pointLight position={[0, 1.2, -3.8]} intensity={9 * z3 * fade} color="#fff0c8" distance={4} decay={1.6} />
      <Floor color="#08090c" />
      <group position={[0, -gone * 1.2, 0]} scale={[1, 1 - gone + 0.001, 1]}>
        {/* atrio: postes de oro y cortinas de lino */}
        {POSTS.map(([x, z], i) => (
          <mesh key={i} position={[x, 0.32, z]}>
            <boxGeometry args={[0.06, 0.64, 0.06]} />
            <Gold glow={0.2} />
          </mesh>
        ))}
        {[-2.5, 2.5].map((x) => (
          <mesh key={x} position={[x, 0.3, 0]}>
            <boxGeometry args={[0.015, 0.5, 10]} />
            <meshStandardMaterial color={C.linen} roughness={1} emissive={C.linen} emissiveIntensity={0.05 + 0.12 * z1} />
          </mesh>
        ))}
        <mesh position={[0, 0.3, -5]}>
          <boxGeometry args={[5, 0.5, 0.015]} />
          <meshStandardMaterial color={C.linen} roughness={1} emissive={C.linen} emissiveIntensity={0.05 + 0.12 * z1} />
        </mesh>
        {/* altar del holocausto y fuente */}
        <mesh position={[0, 0.2, 2.6]}>
          <boxGeometry args={[0.75, 0.4, 0.75]} />
          <meshStandardMaterial color="#8a5a2b" roughness={0.45} metalness={0.8} />
        </mesh>
        <mesh position={[0, 0.41, 2.6]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[0.6, 0.6]} />
          <meshBasicMaterial color="#ff7a1e" toneMapped={false} />
        </mesh>
        <pointLight position={[0, 0.9, 2.6]} intensity={2.5 * ember} color="#ff8a2a" distance={4} decay={1.8} />
        <Glow pos={[0, 0.7, 2.6]} size={1.6} color="#ff8a2a" k={0.35 * ember * fade} />
        <mesh position={[0, 0.12, 1.1]}>
          <cylinderGeometry args={[0.2, 0.14, 0.24, 20]} />
          <meshStandardMaterial color="#8a5a2b" roughness={0.4} metalness={0.8} />
        </mesh>
        {/* la tienda: paredes de oro, sin techo (corte) */}
        {[-0.78, 0.78].map((x) => (
          <mesh key={x} position={[x, 0.4, -2.5]}>
            <boxGeometry args={[0.07, 0.8, 3.8]} />
            <Gold glow={0.12} />
          </mesh>
        ))}
        <mesh position={[0, 0.4, -4.42]}>
          <boxGeometry args={[1.63, 0.8, 0.07]} />
          <Gold glow={0.12} />
        </mesh>
        {/* el velo interior */}
        <mesh position={[0, 0.4, -3.2]}>
          <boxGeometry args={[1.49, 0.8, 0.03]} />
          <meshStandardMaterial color="#3a1550" roughness={0.9} emissive="#5a2390" emissiveIntensity={0.35} />
        </mesh>
        {/* Lugar Santo: candelabro, mesa, altar del incienso */}
        <group position={[-0.45, 0, -2]}>
          <mesh position={[0, 0.14, 0]}>
            <cylinderGeometry args={[0.02, 0.05, 0.28, 10]} />
            <Gold glow={0.3} />
          </mesh>
          <mesh position={[0, 0.28, 0]}>
            <boxGeometry args={[0.02, 0.02, 0.5]} />
            <Gold glow={0.3} />
          </mesh>
          {[-3, -2, -1, 0, 1, 2, 3].map((n, i) => (
            <group key={n} position={[0, 0.32, n * 0.08]}>
              <mesh>
                <sphereGeometry args={[0.022, 8, 8]} />
                <meshBasicMaterial color={i < lit ? '#fff3c0' : '#3a3324'} toneMapped={false} />
              </mesh>
              <Glow pos={[0, 0.02, 0]} size={0.26} color="#ffcf70" k={i < lit ? 0.9 * fade : 0} />
            </group>
          ))}
        </group>
        <mesh position={[0.45, 0.12, -2]}>
          <boxGeometry args={[0.22, 0.24, 0.42]} />
          <Gold glow={0.2} />
        </mesh>
        <mesh position={[0, 0.13, -2.9]}>
          <boxGeometry args={[0.16, 0.26, 0.16]} />
          <Gold glow={0.2} />
        </mesh>
        {/* Lugar Santísimo: el arca */}
        <mesh position={[0, 0.13, -3.82]}>
          <boxGeometry args={[0.36, 0.2, 0.22]} />
          <Gold glow={0.5 + z3 * 0.8} />
        </mesh>
        <Glow pos={[0, 0.45, -3.82]} size={1.5} color="#fff0c8" k={0.55 * z3 * fade} />
      </group>
      <Motes t={t} k={0.25 * fade} box={[12, 6, 14]} center={[0, 3, 0]} count={300} axis={0.1} size={0.6} />
    </>
  );
};

import '@react-three/fiber';
import {at, key, ramp, sm} from '../tl';
import {Sheet} from './Glory';
import {CherubStatue, Figure, Floor, Glow, Gold, Motes} from './Props';

export const E = {
  sin: at(2, 'Cuando el hombre pecó'), guards: at(2, 'Dios puso querubines'), sword: at(2, 'una espada encendida'), keep: at(2, 'para guardar el camino'),
};
const F_STRIP = `void main(){ float x=abs(vUv.x-0.5)*2.0; gl_FragColor=vec4(uColor*exp(-x*x*5.0)*(0.25+0.75*vUv.y)*uK,1.0); }`;

export const edenFigureZ = (t: number) => key(t, [E.sin, E.guards + 0.5, E.keep], [-2.5, 6.5, 9], sm);

/** El huerto: el árbol de la vida, los querubines y la espada encendida (Gn 3:24). */
export const Eden: React.FC<{t: number}> = ({t}) => {
  const guards = sm(ramp(t, E.guards - 0.2, E.guards + 1.1));
  const sword = sm(ramp(t, E.sword - 0.5, E.sword + 0.4));
  const fall = sm(ramp(t, E.sin, E.sin + 2));
  const flick = 0.8 + 0.2 * Math.sin(t * 23) * Math.sin(t * 7.3);
  return (
    <>
      <ambientLight intensity={0.16} color="#8fb39a" />
      <pointLight position={[0, 5, -5.5]} intensity={150 * (1 - fall * 0.35)} color="#d9ffb8" distance={26} decay={1.6} />
      <pointLight position={[0, 2.1, 3.4]} intensity={60 * sword * flick} color="#ff9a3a" distance={12} decay={1.6} />
      <directionalLight position={[-4, 6, 8]} intensity={0.35} color="#9fb2d8" />
      <Floor color="#06110a" />
      <Sheet frag={F_STRIP} k={0.5} color="#ffe6a0" rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.03, 3]}>
        <planeGeometry args={[1.5, 20]} />
      </Sheet>
      {/* árbol de la vida */}
      <mesh position={[0, 1.7, -6]}>
        <cylinderGeometry args={[0.2, 0.42, 3.4, 16]} />
        <Gold glow={0.35} />
      </mesh>
      {[0, 1, 2, 3, 4].map((i) => (
        <mesh key={i} position={[Math.cos(i * 1.26) * 0.7, 3.5, -6 + Math.sin(i * 1.26) * 0.7]} rotation={[Math.sin(i * 1.26) * 0.7, 0, -Math.cos(i * 1.26) * 0.7]}>
          <cylinderGeometry args={[0.06, 0.14, 1.9, 8]} />
          <Gold glow={0.35} />
        </mesh>
      ))}
      <Motes t={t} k={1.5} box={[5.4, 4.4, 5.4]} center={[0, 5, -6]} count={900} axis={0} color="#c8ff9a" size={1.3} />
      <Glow pos={[0, 4.8, -6]} size={11} color="#c8ffa0" k={0.3} />
      <Glow pos={[0, 4.8, -6]} size={4} color="#fffbe0" k={0.5} />
      {/* los guardianes */}
      {guards > 0.01
        ? [-1, 1].map((s) => <CherubStatue key={s} pos={[s * 2.6, -5.2 * (1 - guards), 3.4]} side={s as 1 | -1} glow={0.15 + guards * 0.25} />)
        : null}
      {/* la espada encendida que se revolvía por todos lados */}
      {sword > 0.01 ? (
        <group position={[0, 2.1, 3.4]} rotation={[0, t * 2.6, t * 5.2]} scale={sword}>
          <mesh>
            <boxGeometry args={[0.1, 2.9, 0.03]} />
            <meshBasicMaterial color="#fff0c0" toneMapped={false} />
          </mesh>
          <mesh position={[0, -0.95, 0]}>
            <boxGeometry args={[0.6, 0.08, 0.06]} />
            <meshBasicMaterial color="#ffb44a" toneMapped={false} />
          </mesh>
        </group>
      ) : null}
      <Glow pos={[0, 2.1, 3.4]} size={5.5} color="#ff8a2a" k={0.5 * sword * flick} />
      <Figure pos={[0, 0, edenFigureZ(t)]} />
      <Motes t={t} k={0.5} box={[12, 6, 20]} center={[0, 3, 3]} count={300} axis={0.3} />
    </>
  );
};

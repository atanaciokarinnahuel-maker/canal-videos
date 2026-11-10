import '@react-three/fiber';
import {B, C, at, key, pulse, ramp, sm} from '../tl';
import {Sheet} from './Glory';
import {Beam, CrossMesh, Figure, Floor, Glow, Lamb, Motes, Priest} from './Props';

export const S = {
  wash: at(3, 'Ese día se lavaba'), linen: at(3, 'se vestía de lino'),
  lambs: at(6, 'Durante siglos'), perfect: at(6, 'Ahora moría'), place: at(6, 'Y murió en un lugar'), yours: at(6, 'Era el tuyo'), mine: at(6, 'Era el mío'), peter: at(6, 'Y Pedro lo resume'),
  pray: at(7, 'Tú mismo puedes'), bro: at(7, 'Tus hermanos'), bridge: at(7, 'Pero nadie más'), one: at(7, 'Porque hay un solo mediador'),
};
const F_BEAMX = `void main(){ float y=abs(vUv.y-0.5)*2.0; float head=smoothstep(uA,uA-0.05,vUv.x); gl_FragColor=vec4(uColor*(exp(-y*y*14.0)*0.9+exp(-y*y*220.0))*head*uK,1.0); }`;
const F_SPOT = `void main(){ float d=length(vUv-0.5)*2.0; gl_FragColor=vec4(uColor*smoothstep(1.0,0.2,d)*uK,1.0); }`;

/** Charco de luz en el suelo. */
const Pool: React.FC<{x: number; z: number; color: string; k: number; r?: number}> = ({x, z, color, k, r = 1.6}) => (
  <Sheet frag={F_SPOT} k={k} color={color} rotation={[-Math.PI / 2, 0, 0]} position={[x, 0.02, z]}>
    <planeGeometry args={[r * 2, r * 2]} />
  </Sheet>
);

/** Escenario abstracto: el Cordero, la sustitución, la oración, el único mediador. */
export const Stage: React.FC<{t: number; mode?: string}> = ({t, mode = 'lamb'}) => {
  const base = (
    <>
      <ambientLight intensity={0.14} color="#93a4c8" />
      <Floor />
      <Motes t={t} k={0.45} box={[12, 7, 12]} center={[0, 3.5, 0]} count={320} axis={0.25} />
    </>
  );

  if (mode === 'lamb' || mode === 'lambGlow') {
    const g = mode === 'lambGlow' ? 1 : 0.35;
    return (
      <>
        {base}
        <spotLight position={[0, 9, 2]} angle={0.42} penumbra={1} intensity={150 + g * 70} color="#ffe6b8" distance={22} decay={1.6} />
        <pointLight position={[-2, 1.2, 2]} intensity={6} color="#9fb2d8" distance={8} decay={1.6} />
        <pointLight position={[1.5, 1.4, 2.6]} intensity={9} color="#fff1dc" distance={8} decay={1.6} />
        <Lamb pos={[0, 0, 0]} glow={0.14 + g * 0.1} rotY={-0.5} />
        <Beam pos={[0, 0, 0]} h={10} r0={0.9} r1={2.6} k={0.35 + g * 0.5} />
        <Pool x={0} z={0} color="#ffe2a8" k={0.15 + g * 0.2} />
        <Glow pos={[0, 0.6, 0]} size={5} color="#ffe6b0" k={0.12 * g} />
      </>
    );
  }

  if (mode === 'lambs') {
    const n = 9;
    const u = key(t, [S.lambs + 0.4, S.perfect - 0.3], [0, n]);
    return (
      <>
        {base}
        <directionalLight position={[2, 8, 6]} intensity={1.6} color="#cfd8f0" />
        {Array.from({length: n}).map((_, i) => {
          const gone = sm(ramp(u, i, i + 0.9));
          return gone > 0.98 ? null : (
            <group key={i}>
              <Lamb pos={[(i - (n - 1) / 2) * 1.35, -gone * 0.5, 0]} opacity={1 - gone} rotY={-0.4} />
              <Pool x={(i - (n - 1) / 2) * 1.35} z={0} color="#b3202a" k={0.5 * pulse(u, i, 0.2, 0.8)} r={0.9} />
            </group>
          );
        })}
      </>
    );
  }

  if (mode === 'priest') {
    const white = sm(ramp(t, S.linen - 0.2, S.linen + 0.9));
    const water = pulse(t, S.wash + 0.1, 0.3, 1.6);
    return (
      <>
        {base}
        <spotLight position={[0, 8, 3]} angle={0.45} penumbra={1} intensity={130 + white * 90} color="#fff0d8" distance={20} decay={1.6} />
        <pointLight position={[0, 0.6, 1.2]} intensity={40 * water} color="#5aa8ff" distance={7} decay={1.5} />
        <Priest pos={[0, 0, 0]} white={white} />
        <Pool x={0} z={0} color="#5aa8ff" k={0.5 * water} r={2.2} />
        <Beam pos={[0, 0, 0]} h={9} r0={0.4} r1={1.3} k={0.3 + white * 0.7} />
      </>
    );
  }

  if (mode === 'swap') {
    const late = t > B(7);
    const f1 = late ? 1 : sm(ramp(t, S.yours - 0.1, S.yours + 0.35));
    const f2 = late ? 0 : sm(ramp(t, S.mine - 0.1, S.mine + 0.35));
    const p = late ? 1 : sm(ramp(t, S.peter + 0.8, S.peter + 3.4));
    const x1 = -0.4 + p * 3.5;
    const x2 = 0.5 + p * 3.5;
    return (
      <>
        {base}
        <spotLight position={[0, 8, 3]} angle={0.35} penumbra={1} intensity={170} color={C.crimson} distance={18} decay={1.5} />
        <spotLight position={[3.4, 8, 3]} angle={0.4} penumbra={1} intensity={230 * p} color="#ffe2a8" distance={18} decay={1.5} />
        <pointLight position={[0, 3, 1.5]} intensity={8} color="#9fb2d8" distance={9} decay={1.6} />
        <pointLight position={[0, 4.2, -4.5 + p * 1.9]} intensity={70} color="#ffd9a0" distance={12} decay={1.5} />
        <Glow pos={[0, 3.6, -2.2 + p * 1.9]} size={7} color="#ffcf80" k={0.16} />
        <CrossMesh pos={[0, 0, -1.3 + p * 1.9]} h={5.4} gold={false} />
        <Pool x={0} z={0.7} color="#d0202c" k={0.75} r={1.7} />
        <Pool x={3.4} z={0.8} color="#ffe2a8" k={0.6 * p} r={1.9} />
        <Beam pos={[3.4, 0, 0.8]} h={9} r0={0.5} r1={1.6} k={p} />
        {f1 > 0.01 ? <Figure pos={[x1, 0, 0.8]} scale={f1} emissive="#ffe2ad" glow={p * 0.3} /> : null}
        {f2 > 0.01 ? <Figure pos={[x2, 0, 1.0]} scale={f2 * 0.95} emissive="#ffe2ad" glow={p * 0.3} /> : null}
      </>
    );
  }

  if (mode === 'pray' || mode === 'brothers') {
    const bro = mode === 'brothers';
    const others: [number, number][] = [[-1.7, -0.5], [-0.9, -1.3], [0.9, -1.3], [1.7, -0.5]];
    const k = sm(ramp(t, bro ? S.bro - 1 : S.pray - 0.2, bro ? S.bro : S.pray + 0.9));
    return (
      <>
        {base}
        <spotLight position={[0, 10, 1]} angle={0.4} penumbra={1} intensity={170 * (0.4 + k)} color="#ffe9c0" distance={22} decay={1.5} />
        <pointLight position={[-2, 1.4, 2.5]} intensity={5} color="#9fb2d8" distance={8} decay={1.6} />
        <Figure pos={[0, 0, 0]} kneel={0.55} emissive="#ffe2ad" glow={0.25 * k} color="#2a2823" />
        <Beam pos={[0, 0, 0]} h={12} r0={0.35} r1={1.2} k={1.4 * k} />
        <Pool x={0} z={0} color="#ffe2a8" k={0.5 * k} />
        <Glow pos={[0, 11, 0]} size={9} color="#fff0cc" k={0.5 * k} />
        {bro
          ? others.map(([x, z], i) => {
              const a = sm(ramp(t, S.bro + i * 0.18, S.bro + 0.5 + i * 0.18));
              return (
                <group key={i}>
                  <Figure pos={[x, 0, z]} kneel={0.55} scale={a} color="#24252b" emissive="#ffe2ad" glow={0.12} />
                  <Beam pos={[x, 0, z]} h={12} r0={0.2} r1={0.7} k={0.6 * a} />
                </group>
              );
            })
          : null}
      </>
    );
  }

  // 'bridge': intermediarios que desaparecen; queda un solo mediador
  const fade = sm(ramp(t, S.bridge + 1.0, S.bridge + 2.6));
  const one = sm(ramp(t, S.one - 0.2, S.one + 1.3));
  return (
    <>
      {base}
      <pointLight position={[-4, 3, 3]} intensity={16} color="#9fb2d8" distance={10} decay={1.6} />
      <pointLight position={[6, 3, 1]} intensity={90} color="#ffe2a8" distance={16} decay={1.5} />
      <Figure pos={[-4, 0, 0]} emissive="#ffe2ad" glow={0.3 * one} color="#2a2823" />
      {[-1.9, -0.2, 1.5, 3.2].map((x, i) => (
        <Figure key={i} pos={[x, -fade * 0.6, 0]} opacity={1 - fade} color="#16171c" />
      ))}
      <Glow pos={[6.5, 2.2, 0]} size={9} color="#fff0cc" k={0.8} />
      <Glow pos={[6.5, 2.2, 0]} size={3} color="#ffffff" k={0.8} />
      <Sheet frag={F_BEAMX} k={one * 1.1} a={one * 1.05} color="#ffe2a8" position={[1.1, 1.5, 0]}>
        <planeGeometry args={[10.2, 1.4]} />
      </Sheet>
      <LightCrossSmall k={one} />
    </>
  );
};

/** La cruz como puente: en el centro del haz. */
const LightCrossSmall: React.FC<{k: number}> = ({k}) => (
  <group position={[1.1, 0.2, 0.05]}>
    <Sheet frag={F_SPOT} k={k * 0.9} color="#fff3d0" position={[0, 1.5, 0]}>
      <planeGeometry args={[0.34, 3.0]} />
    </Sheet>
    <Sheet frag={F_SPOT} k={k * 0.9} color="#fff3d0" position={[0, 2.0, 0]}>
      <planeGeometry args={[1.7, 0.34]} />
    </Sheet>
  </group>
);

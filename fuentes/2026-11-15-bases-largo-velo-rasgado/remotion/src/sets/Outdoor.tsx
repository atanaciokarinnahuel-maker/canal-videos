import '@react-three/fiber';
import {useMemo} from 'react';
import * as THREE from 'three';
import {C, at, cl, key, pulse, ramp, sm} from '../tl';
import {Sheet} from './Glory';
import {CrossMesh, Glow, Goat, Motes} from './Props';

/* ═════════════ Desierto: el macho cabrío (Lv 16:20-22) ═════════════ */
const D = {on: at(3, 'Afuera, sobre la cabeza'), conf: at(3, 'confesaba'), away: at(3, 'y lo enviaban lejos'), sub: at(3, 'Un sustituto')};
export const goatZ = (t: number) => key(t, [D.away + 0.3, D.away + 7], [0, -24]);
const F_SKY = `void main(){ float h=vUv.y; float glow=exp(-pow((h-0.34)*7.0,2.0)); vec3 c=mix(vec3(0.02,0.025,0.05),uColor,glow*0.9);
  float sun=exp(-pow(length((vUv-vec2(0.5+uB,0.36))*vec2(2.2,1.0))*16.0,2.0)); gl_FragColor=vec4((c+vec3(1.0,0.75,0.45)*sun*(1.0-uA))*uK,1.0); }`;

export const Desert: React.FC<{t: number}> = ({t}) => {
  const geo = useMemo(() => {
    const g = new THREE.PlaneGeometry(160, 160, 80, 80);
    const p = g.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i);
      const y = p.getY(i);
      const far = cl((Math.hypot(x, y) - 5) / 30);
      p.setZ(i, (Math.sin(x * 0.16 + y * 0.05) * 1.3 + Math.sin(y * 0.21 + 1.7) * 0.9 + Math.sin(x * 0.5 + y * 0.4) * 0.25) * far);
    }
    g.computeVertexNormals();
    return g;
  }, []);
  const z = goatZ(t);
  const guilt = sm(ramp(t, D.conf - 0.3, D.conf + 1.4));
  const walking = t > D.away + 0.3;
  return (
    <>
      <ambientLight intensity={0.22} color="#8f9cc0" />
      <directionalLight position={[-8, 3, -20]} intensity={2.2} color="#ffb060" />
      <directionalLight position={[5, 8, 8]} intensity={0.5} color="#9fb2d8" />
      <pointLight position={[0.6, 2.2, z + 1.2]} intensity={26 * guilt} color={C.crimson} distance={8} decay={1.5} />
      <mesh geometry={geo} rotation={[-Math.PI / 2, 0, 0]}>
        <meshStandardMaterial color="#3a2710" roughness={1} metalness={0} />
      </mesh>
      <Sheet frag={F_SKY} k={1} a={0.2} b={-0.06} color="#c8622a" position={[0, 18, -75]}>
        <planeGeometry args={[260, 80]} />
      </Sheet>
      <Goat pos={[0, walking ? Math.abs(Math.sin(t * 7)) * 0.04 : 0, z]} rotY={walking ? Math.PI / 2 : 0.5} />
      {/* la culpa confesada sobre él */}
      <Motes t={t * 2.5} k={guilt * 1.3} box={[1.9, 1.5, 1.9]} center={[0, 1.75, z]} count={240} axis={0} color="#ff2b2b" size={0.9} />
      <Glow pos={[0, 1.7, z]} size={3.2} color="#b3101a" k={0.4 * guilt} />
      <Motes t={t} k={0.35} box={[16, 6, 30]} center={[0, 3, -6]} count={260} axis={0.1} size={0.7} />
    </>
  );
};

/* ═════════════ Calvario: tres cruces, tinieblas (Mt 27:45-50) ═════════════ */
export const K = {
  jer: at(5, 'Tiempo después'), dark: at(5, 'Desde el mediodía'), three: at(5, 'Cerca de las tres'), cry: at(5, 'Jesús clama'),
  done: at(5, 'consumado es'), gave: at(5, 'Y entrega el espíritu'), instant: at(5, 'En ese mismo instante'),
};

export const Calvary: React.FC<{t: number; mode?: string}> = ({t, mode}) => {
  const story = !mode;
  const dark = story ? key(t, [K.dark, K.dark + 2.6], [0, 1], sm) : mode === 'dawn' ? 0 : 0.82;
  const out = story ? sm(ramp(t, K.gave + 0.5, K.instant - 0.1)) : 0;
  const rim = story ? pulse(t, K.done, 0.2, 2.2) : mode === 'rim' ? 1 : 0;
  const day = (1 - dark * 0.9) * (1 - out);
  const dawn = mode === 'dawn' ? 1 : 0;
  return (
    <>
      <ambientLight intensity={(0.1 + 0.25 * day + 0.2 * dawn) * (1 - out)} color="#9aa6c6" />
      <directionalLight position={[2, 6, -14]} intensity={(2.4 * day + 1.6 * rim + 2.6 * dawn) * (1 - out)} color={dawn ? '#ffd9a0' : '#ffb070'} />
      <directionalLight position={[-6, 5, 10]} intensity={(0.5 * day + 0.25 + 0.5 * dawn) * (1 - out)} color="#93a4c8" />
      <pointLight position={[0, 7, 3.5]} intensity={90 * rim * (1 - out)} color="#ffd590" distance={16} decay={1.6} />
      <mesh position={[0, -38.6, 0]}>
        <sphereGeometry args={[40, 96, 48]} />
        <meshStandardMaterial color="#1a1612" roughness={1} />
      </mesh>
      <CrossMesh pos={[0, 1.25, 0]} h={7.6} gold={false} />
      <CrossMesh pos={[-5.2, 0.95, -0.8]} h={6} gold={false} />
      <CrossMesh pos={[5.2, 0.95, -0.8]} h={6} gold={false} />
      {/* filo de oro en la cruz central */}
      <mesh position={[0, 5.05, 0.24]}>
        <boxGeometry args={[0.06, 7.6, 0.02]} />
        <meshBasicMaterial color="#ffd27a" toneMapped={false} transparent opacity={cl(rim + dawn * 0.8) * (1 - out)} />
      </mesh>
      <mesh position={[0, 6.72, 0.24]}>
        <boxGeometry args={[3.9, 0.06, 0.02]} />
        <meshBasicMaterial color="#ffd27a" toneMapped={false} transparent opacity={cl(rim + dawn * 0.8) * (1 - out)} />
      </mesh>
      <Sheet frag={F_SKY} k={(0.18 + 0.82 * day + dawn * 0.5) * (1 - out)} a={dark} b={0.0} color={dawn ? '#ffb45a' : '#b8501e'} position={[0, 14, -70]}>
        <planeGeometry args={[260, 90]} />
      </Sheet>
      <Glow pos={[0, 6.5, -1]} size={22} color="#ffcf80" k={(0.22 * rim + 0.3 * dawn) * (1 - out)} />
      <Motes t={t} k={(0.25 + rim * 0.8 + dawn * 0.6) * (1 - out)} box={[18, 10, 16]} center={[0, 5, 3]} count={320} axis={0.12} />
    </>
  );
};

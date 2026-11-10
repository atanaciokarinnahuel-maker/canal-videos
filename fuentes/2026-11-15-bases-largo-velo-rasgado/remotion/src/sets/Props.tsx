import '@react-three/fiber';
import {useMemo} from 'react';
import * as THREE from 'three';
import {random} from 'remotion';
import {C, V3} from '../tl';

/* ───────────── Materiales del modelo visual ───────────── */
export const Obsidian: React.FC<{opacity?: number}> = ({opacity = 1}) => (
  <meshStandardMaterial color="#14161d" roughness={0.24} metalness={0.45} transparent={opacity < 1} opacity={opacity} />
);
export const Gold: React.FC<{glow?: number; opacity?: number}> = ({glow = 0.08, opacity = 1}) => (
  <meshStandardMaterial color={C.gold} roughness={0.42} metalness={0.85} emissive={C.goldDeep} emissiveIntensity={glow} transparent={opacity < 1} opacity={opacity} />
);
export const Floor: React.FC<{color?: string; size?: number; y?: number}> = ({color = '#07080b', size = 160, y = 0}) => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, y, 0]}>
    <planeGeometry args={[size, size]} />
    <meshStandardMaterial color={color} roughness={0.3} metalness={0.8} />
  </mesh>
);

/* ───────────── Resplandor (sprite aditivo) ───────────── */
let glowTex: THREE.DataTexture | null = null;
const getGlowTex = () => {
  if (glowTex) return glowTex;
  const n = 64;
  const d = new Uint8Array(n * n * 4);
  for (let y = 0; y < n; y++)
    for (let x = 0; x < n; x++) {
      const r = Math.hypot(x - n / 2 + 0.5, y - n / 2 + 0.5) / (n / 2);
      const a = Math.pow(Math.max(0, 1 - r), 2.2);
      const i = (y * n + x) * 4;
      d[i] = d[i + 1] = d[i + 2] = 255 * a;
      d[i + 3] = 255;
    }
  glowTex = new THREE.DataTexture(d, n, n, THREE.RGBAFormat);
  glowTex.magFilter = THREE.LinearFilter;
  glowTex.minFilter = THREE.LinearFilter;
  glowTex.needsUpdate = true;
  return glowTex;
};
export const Glow: React.FC<{pos: V3; size: number | [number, number]; color?: string; k?: number}> = ({pos, size, color = C.light, k = 1}) => {
  const s = typeof size === 'number' ? [size, size] : size;
  if (k <= 0.001) return null;
  return (
    <sprite position={pos} scale={[s[0], s[1], 1]}>
      <spriteMaterial map={getGlowTex()} color={color} opacity={Math.min(1, k)} blending={THREE.AdditiveBlending} depthWrite={false} fog={false} toneMapped={false} transparent />
    </sprite>
  );
};

/** Haz de luz vertical (cono aditivo). */
export const Beam: React.FC<{pos: V3; h: number; r0?: number; r1?: number; color?: string; k?: number}> = ({pos, h, r0 = 0.3, r1 = 1.2, color = C.light, k = 1}) =>
  k <= 0.001 ? null : (
    <mesh position={[pos[0], pos[1] + h / 2, pos[2]]}>
      <cylinderGeometry args={[r0, r1, h, 32, 1, true]} />
      <meshBasicMaterial color={color} transparent opacity={Math.min(0.12, 0.045 * k)} blending={THREE.AdditiveBlending} depthWrite={false} side={THREE.DoubleSide} fog={false} toneMapped={false} />
    </mesh>
  );

/* ───────────── Figuras abstractas (sin rostro) ───────────── */
/** Persona: túnica + cabeza. `reach` levanta un brazo. */
export const Figure: React.FC<{pos: V3; color?: string; emissive?: string; glow?: number; reach?: number; opacity?: number; scale?: number; kneel?: number}> = ({
  pos, color = '#1b1d25', emissive = '#000000', glow = 0, reach = 0, opacity = 1, scale = 1, kneel = 0,
}) => {
  const mat = <meshStandardMaterial color={color} roughness={0.6} metalness={0.1} emissive={emissive} emissiveIntensity={glow} transparent={opacity < 1} opacity={opacity} />;
  return (
    <group position={pos} scale={scale}>
      <group scale={[1, 1 - kneel * 0.32, 1]}>
        <mesh position={[0, 0.72, 0]}>
          <cylinderGeometry args={[0.2, 0.36, 1.44, 20]} />
          {mat}
        </mesh>
        <mesh position={[0, 1.44, 0]} scale={[1, 0.55, 0.8]}>
          <sphereGeometry args={[0.24, 20, 14]} />
          {mat}
        </mesh>
        <mesh position={[0, 1.7, 0]}>
          <sphereGeometry args={[0.15, 20, 14]} />
          {mat}
        </mesh>
        {reach > 0.01 ? (
          <group position={[0.2, 1.4, 0]} rotation={[-0.5 * reach, 0, -0.35 - 0.2 * reach]}>
            <mesh position={[0, 0.3 * reach + 0.05, 0]}>
              <capsuleGeometry args={[0.055, 0.5 * reach + 0.1, 4, 10]} />
              {mat}
            </mesh>
          </group>
        ) : null}
      </group>
    </group>
  );
};

/** Sumo sacerdote: lino blanco, cinto y mitra de oro. */
export const Priest: React.FC<{pos: V3; white?: number; opacity?: number}> = ({pos, white = 1, opacity = 1}) => {
  const col = new THREE.Color('#5c5a55').lerp(new THREE.Color(C.linen), white);
  return (
    <group position={pos}>
      <Figure pos={[0, 0, 0]} color={`#${col.getHexString()}`} emissive={C.linen} glow={0.1 + white * 0.22} opacity={opacity} />
      <mesh position={[0, 1.0, 0]}>
        <cylinderGeometry args={[0.265, 0.285, 0.09, 20]} />
        <Gold glow={0.3} opacity={opacity} />
      </mesh>
      <mesh position={[0, 1.83, 0]}>
        <cylinderGeometry args={[0.13, 0.15, 0.1, 16]} />
        <Gold glow={0.3} opacity={opacity} />
      </mesh>
    </group>
  );
};

const Quad: React.FC<{color: string; glow?: number; horns?: boolean; opacity?: number; em?: string}> = ({color, glow = 0, horns, opacity = 1, em = '#ffffff'}) => {
  const mat = <meshStandardMaterial color={color} roughness={0.95} metalness={0} emissive={em} emissiveIntensity={glow} transparent={opacity < 1} opacity={opacity} />;
  const dark = <meshStandardMaterial color="#2a2622" roughness={0.9} transparent={opacity < 1} opacity={opacity} />;
  return (
    <group>
      <mesh position={[0, 0.5, 0]} scale={[0.72, 0.5, 0.46]}>
        <sphereGeometry args={[0.5, 24, 16]} />
        {mat}
      </mesh>
      <mesh position={[0.36, 0.72, 0]} scale={[1.1, 0.9, 0.85]}>
        <sphereGeometry args={[0.16, 18, 14]} />
        {mat}
      </mesh>
      {[-1, 1].map((s) => (
        <mesh key={s} position={[0.32, 0.8, s * 0.14]} rotation={[s * 0.7, 0, 0.4]} scale={[0.5, 1, 0.3]}>
          <sphereGeometry args={[0.08, 10, 8]} />
          {mat}
        </mesh>
      ))}
      {horns
        ? [-1, 1].map((s) => (
            <mesh key={s} position={[0.3, 0.93, s * 0.08]} rotation={[s * 0.3, 0, 0.5]}>
              <coneGeometry args={[0.035, 0.26, 8]} />
              <Gold glow={0.1} />
            </mesh>
          ))
        : null}
      {[
        [0.22, 0.13], [0.22, -0.13], [-0.22, 0.13], [-0.22, -0.13],
      ].map(([x, z], i) => (
        <mesh key={i} position={[x, 0.16, z]}>
          <cylinderGeometry args={[0.04, 0.035, 0.34, 8]} />
          {dark}
        </mesh>
      ))}
    </group>
  );
};
export const Lamb: React.FC<{pos: V3; glow?: number; opacity?: number; rotY?: number; scale?: number}> = ({pos, glow = 0.05, opacity = 1, rotY = 0, scale = 1}) => (
  <group position={pos} rotation={[0, rotY, 0]} scale={scale}>
    <Quad color="#f3efe6" glow={glow} opacity={opacity} em="#fff3d6" />
  </group>
);
export const Goat: React.FC<{pos: V3; rotY?: number}> = ({pos, rotY = 0}) => (
  <group position={pos} rotation={[0, rotY, 0]} scale={1.15}>
    <Quad color="#4a4138" horns />
  </group>
);

/** Querubín como estatua: cuerpo de obsidiana, alas de oro. */
export const CherubStatue: React.FC<{pos: V3; side: 1 | -1; glow?: number; scale?: number}> = ({pos, side, glow = 0.15, scale = 1}) => (
  <group position={pos} scale={scale}>
    <mesh position={[0, 1.5, 0]}>
      <cylinderGeometry args={[0.24, 0.52, 3, 20]} />
      <Obsidian />
    </mesh>
    <mesh position={[0, 3.25, 0]}>
      <sphereGeometry args={[0.27, 20, 14]} />
      <Obsidian />
    </mesh>
    {[1, -1].map((w) => (
      <group key={w} position={[w * 0.2, 2.7, 0]} rotation={[0, 0, w * (w === -side ? 1.05 : 0.6)]}>
        <mesh position={[w * 1.25, 0, 0]} scale={[1, 1, 1]}>
          <boxGeometry args={[2.3, 0.06, 0.62]} />
          <Gold glow={glow} />
        </mesh>
        <mesh position={[w * 0.95, -0.14, 0]}>
          <boxGeometry args={[1.6, 0.05, 0.5]} />
          <Gold glow={glow} />
        </mesh>
      </group>
    ))}
  </group>
);

export const CrossMesh: React.FC<{pos: V3; h?: number; gold?: boolean; glow?: number; opacity?: number}> = ({pos, h = 8, gold = true, glow = 0.08, opacity = 1}) => {
  const M = gold ? <Gold glow={glow} opacity={opacity} /> : <Obsidian opacity={opacity} />;
  const t = h * 0.058;
  return (
    <group position={pos}>
      <mesh position={[0, h / 2, 0]}>
        <boxGeometry args={[t, h, t]} />
        {M}
      </mesh>
      <mesh position={[0, h * 0.72, 0]}>
        <boxGeometry args={[h * 0.52, t, t]} />
        {M}
      </mesh>
    </group>
  );
};

/** Polvo de oro en suspensión, visible donde hay luz. */
export const Motes: React.FC<{t: number; k: number; box?: V3; center?: V3; count?: number; axis?: number; color?: string; size?: number}> = ({
  t, k, box = [12, 8, 14], center = [0, 4, 0], count = 500, axis = 0.25, color = C.goldHi, size = 1,
}) => {
  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    const p = new Float32Array(count * 3);
    const s = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      p[i * 3] = (random(`mx${i}`) - 0.5) * box[0];
      p[i * 3 + 1] = random(`my${i}`) * box[1];
      p[i * 3 + 2] = (random(`mz${i}`) - 0.5) * box[2];
      s[i] = random(`ms${i}`);
    }
    g.setAttribute('position', new THREE.BufferAttribute(p, 3));
    g.setAttribute('aSeed', new THREE.BufferAttribute(s, 1));
    return g;
  }, [count, box[0], box[1], box[2]]);
  const uniforms = useMemo(() => ({uT: {value: 0}, uK: {value: 0}, uH: {value: 8}, uAxis: {value: 0.25}, uSize: {value: 1}, uColor: {value: new THREE.Color(color)}}), [color]);
  uniforms.uT.value = t;
  uniforms.uK.value = k;
  uniforms.uH.value = box[1];
  uniforms.uAxis.value = axis;
  uniforms.uSize.value = size;
  return (
    <points geometry={geo} frustumCulled={false} position={[center[0], center[1] - box[1] / 2, center[2]]}>
      <shaderMaterial
        uniforms={uniforms}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        fog={false}
        toneMapped={false}
        vertexShader={/* glsl */ `
          attribute float aSeed;
          uniform float uT; uniform float uH; uniform float uAxis; uniform float uSize;
          varying float vA;
          void main() {
            vec3 p = position;
            p.y = mod(p.y + uT * (0.05 + aSeed * 0.12), uH);
            p.x += sin(uT * 0.3 + aSeed * 40.0) * 0.35;
            p.z += cos(uT * 0.22 + aSeed * 17.0) * 0.4;
            vec4 mv = modelViewMatrix * vec4(p, 1.0);
            gl_Position = projectionMatrix * mv;
            float depth = -mv.z;
            gl_PointSize = uSize * (5.0 + aSeed * 13.0) * 12.0 / max(depth, 0.6);
            float nearAxis = exp(-abs(p.x) * uAxis);
            float twinkle = 0.6 + 0.4 * sin(uT * 1.7 + aSeed * 90.0);
            vA = nearAxis * twinkle * smoothstep(0.4, 2.0, depth) * (1.0 - smoothstep(24.0, 40.0, depth));
          }
        `}
        fragmentShader={/* glsl */ `
          uniform float uK; uniform vec3 uColor; varying float vA;
          void main() {
            float d = length(gl_PointCoord - 0.5);
            float a = smoothstep(0.5, 0.0, d);
            gl_FragColor = vec4(uColor * a * a * vA * uK, 1.0);
          }
        `}
      />
    </points>
  );
};

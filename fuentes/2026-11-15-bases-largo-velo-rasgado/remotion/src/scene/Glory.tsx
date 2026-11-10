import {useMemo} from 'react';
import * as THREE from 'three';
import {C, VEIL, glory, tearFrontY, tornFraction, veilPart} from '../timeline';

const VERT = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const additive = {
  transparent: true,
  depthWrite: false,
  blending: THREE.AdditiveBlending,
  side: THREE.DoubleSide,
  fog: false,
  toneMapped: false,
} as const;

/** Fuente de luz del Lugar Santísimo: un plano radiante al fondo. */
const Source: React.FC<{k: number}> = ({k}) => {
  const uniforms = useMemo(() => ({uK: {value: 0}, uColor: {value: new THREE.Color(C.light)}}), []);
  uniforms.uK.value = k;
  return (
    <mesh position={[0, 9, -40]}>
      <planeGeometry args={[90, 60]} />
      <shaderMaterial
        uniforms={uniforms}
        vertexShader={VERT}
        fog={false}
        toneMapped={false}
        fragmentShader={/* glsl */ `
          varying vec2 vUv;
          uniform float uK;
          uniform vec3 uColor;
          void main() {
            vec2 p = (vUv - vec2(0.5, 0.42)) * vec2(1.5, 1.0);
            float d = length(p);
            float core = exp(-d * d * 34.0);
            float halo = exp(-d * 3.2);
            vec3 col = uColor * (core * 0.8 + halo * 0.2) + vec3(0.95, 0.5, 0.16) * halo * 0.3;
            gl_FragColor = vec4(col * uK, 1.0);
          }
        `}
      />
    </mesh>
  );
};

/** Haz volumétrico falso: lámina aditiva que nace en la rasgadura y se abre hacia cámara. */
const Shaft: React.FC<{angle: number; k: number; top: number; bottom: number; len: number; seed: number}> = ({angle, k, top, bottom, len, seed}) => {
  const uniforms = useMemo(() => ({uK: {value: 0}, uSeed: {value: seed}, uColor: {value: new THREE.Color(C.light)}}), [seed]);
  uniforms.uK.value = k;
  const h = Math.max(0.001, top - bottom);
  return (
    <group rotation={[0, angle, 0]}>
      <mesh position={[0, bottom + h / 2 - 0.6, len / 2]} rotation={[0, Math.PI / 2, 0]} scale={[len, h + 1.2, 1]}>
        <planeGeometry args={[1, 1, 1, 1]} />
        <shaderMaterial
          uniforms={uniforms}
          vertexShader={VERT}
          {...additive}
          fragmentShader={/* glsl */ `
            varying vec2 vUv;
            uniform float uK;
            uniform float uSeed;
            uniform vec3 uColor;
            void main() {
              float along = vUv.x;                  // 1 en la rasgadura, 0 lejos
              float fall = pow(along, 1.7);
              float edge = smoothstep(0.0, 0.18, vUv.y) * smoothstep(1.0, 0.8, vUv.y);
              float streak = 0.65 + 0.35 * sin(vUv.y * 23.0 + uSeed * 9.0) * sin(vUv.y * 7.0 + uSeed);
              gl_FragColor = vec4(uColor * fall * edge * streak * uK * 0.16, 1.0);
            }
          `}
        />
      </mesh>
    </group>
  );
};

/** Línea de luz en la rasgadura + derrame sobre el suelo pulido. */
const Seam: React.FC<{k: number; top: number; bottom: number; width: number}> = ({k, top, bottom, width}) => {
  const uniforms = useMemo(() => ({uK: {value: 0}, uColor: {value: new THREE.Color(C.light)}}), []);
  uniforms.uK.value = k;
  const h = Math.max(0.001, top - bottom);
  return (
    <mesh position={[0, bottom + h / 2, 0.35]} scale={[width, h + 2.4, 1]}>
      <planeGeometry args={[1, 1]} />
      <shaderMaterial
        uniforms={uniforms}
        vertexShader={VERT}
        {...additive}
        fragmentShader={/* glsl */ `
          varying vec2 vUv;
          uniform float uK;
          uniform vec3 uColor;
          void main() {
            float x = abs(vUv.x - 0.5) * 2.0;
            float y = smoothstep(0.0, 0.2, vUv.y) * smoothstep(1.0, 0.85, vUv.y);
            float g = exp(-x * 7.0) * 0.28 + exp(-x * x * 260.0) * 1.3;
            gl_FragColor = vec4(uColor * g * y * uK, 1.0);
          }
        `}
      />
    </mesh>
  );
};

const FloorSpill: React.FC<{k: number; spread: number}> = ({k, spread}) => {
  const uniforms = useMemo(() => ({uK: {value: 0}, uSpread: {value: 0}, uColor: {value: new THREE.Color(C.light)}}), []);
  uniforms.uK.value = k;
  uniforms.uSpread.value = spread;
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 13]}>
      <planeGeometry args={[26, 26]} />
      <shaderMaterial
        uniforms={uniforms}
        vertexShader={VERT}
        {...additive}
        fragmentShader={/* glsl */ `
          varying vec2 vUv;
          uniform float uK;
          uniform float uSpread;
          uniform vec3 uColor;
          void main() {
            float z = 1.0 - vUv.y;                       // 0 junto al velo
            float x = abs(vUv.x - 0.5) * 26.0;
            float w = 0.1 + z * (0.55 + uSpread * 5.0) + uSpread * 1.2;
            float beam = exp(-(x * x) / (w * w));
            float fall = pow(1.0 - z, 1.6);
            gl_FragColor = vec4(uColor * beam * fall * uK * 0.55, 1.0);
          }
        `}
      />
    </mesh>
  );
};

/** Reflejo de la gloria sobre el suelo del Lugar Santísimo. */
const InnerFloor: React.FC<{k: number}> = ({k}) => {
  const uniforms = useMemo(() => ({uK: {value: 0}, uColor: {value: new THREE.Color('#ffd9a0')}}), []);
  uniforms.uK.value = k;
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, -24]}>
      <planeGeometry args={[60, 48]} />
      <shaderMaterial
        uniforms={uniforms}
        vertexShader={VERT}
        {...additive}
        fragmentShader={/* glsl */ `
          varying vec2 vUv;
          uniform float uK;
          uniform vec3 uColor;
          void main() {
            float x = abs(vUv.x - 0.5) * 60.0;
            float far = vUv.y;                           // 1 hacia la fuente
            float w = 2.0 + far * 9.0;
            float beam = exp(-(x * x) / (w * w));
            float fall = pow(far, 1.4) * smoothstep(0.0, 0.25, 1.0 - far + 0.25);
            gl_FragColor = vec4(uColor * beam * fall * uK * 0.5, 1.0);
          }
        `}
      />
    </mesh>
  );
};

const SHAFTS = [-0.52, -0.3, -0.13, 0.11, 0.27, 0.5];

export const Glory: React.FC<{t: number}> = ({t}) => {
  const k = glory(t);
  const torn = tornFraction(t);
  const part = veilPart(t);
  const front = Math.max(0, tearFrontY(t));
  const top = VEIL.height;
  const open = k * torn;

  return (
    <group>
      <Source k={k > 0 ? 0.5 + k * 0.28 : 0} />
      {torn > 0 && (
        <>
          <Seam k={k * (1 - part * 0.75)} top={top} bottom={front} width={1.6 + part * 7} />
          <FloorSpill k={open} spread={part} />
          <InnerFloor k={open} />
          {SHAFTS.map((a, i) => (
            <Shaft key={i} angle={a * (0.5 + part * 0.9)} k={open} top={top} bottom={front} len={15 + (i % 3) * 3} seed={i + 1} />
          ))}
          {/* la luz real que baña pilares, suelo y oro */}
          <pointLight position={[0, front + (top - front) * 0.5, 1.2]} color={C.light} intensity={open * 60} distance={46} decay={1.7} />
          <pointLight position={[0, 1.2, 2.5]} color={C.light} intensity={open * torn * 40} distance={30} decay={1.8} />
        </>
      )}
    </group>
  );
};

import {useMemo} from 'react';
import * as THREE from 'three';
import {C} from '../tl';
import {VEIL} from './Veil';

const VERT = /* glsl */ `
  varying vec2 vUv;
  void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`;
const additive = {transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, fog: false, toneMapped: false} as const;

/** Lámina aditiva genérica con un fragment shader propio (uK = intensidad, uA/uB = parámetros). */
export const Sheet: React.FC<{frag: string; k: number; a?: number; b?: number; color?: string; children: React.ReactNode} & JSX.IntrinsicElements['mesh']> = ({frag, k, a = 0, b = 0, color = C.light, children, ...mesh}) => {
  const uniforms = useMemo(() => ({uK: {value: 0}, uA: {value: 0}, uB: {value: 0}, uColor: {value: new THREE.Color(color)}}), [color]);
  uniforms.uK.value = k;
  uniforms.uA.value = a;
  uniforms.uB.value = b;
  if (k <= 0.0005) return null;
  return (
    <mesh {...mesh}>
      {children}
      <shaderMaterial uniforms={uniforms} vertexShader={VERT} fragmentShader={`varying vec2 vUv; uniform float uK; uniform float uA; uniform float uB; uniform vec3 uColor;\n${frag}`} {...additive} />
    </mesh>
  );
};

const F_SOURCE = `void main(){ vec2 p=(vUv-vec2(0.5,0.42))*vec2(1.5,1.0); float d=length(p); float core=exp(-d*d*34.0); float halo=exp(-d*3.2);
  gl_FragColor=vec4((uColor*(core*0.8+halo*0.2)+vec3(0.95,0.5,0.16)*halo*0.3)*uK,1.0); }`;
const F_SHAFT = `void main(){ float fall=pow(vUv.x,1.7); float edge=smoothstep(0.0,0.18,vUv.y)*smoothstep(1.0,0.8,vUv.y);
  float streak=0.65+0.35*sin(vUv.y*23.0+uA*9.0)*sin(vUv.y*7.0+uA); gl_FragColor=vec4(uColor*fall*edge*streak*uK*0.16,1.0); }`;
const F_SEAM = `void main(){ float x=abs(vUv.x-0.5)*2.0; float y=smoothstep(0.0,0.2,vUv.y)*smoothstep(1.0,0.85,vUv.y);
  float g=exp(-x*7.0)*0.28+exp(-x*x*260.0)*1.3; gl_FragColor=vec4(uColor*g*y*uK,1.0); }`;
const F_SPILL = `void main(){ float z=1.0-vUv.y; float x=abs(vUv.x-0.5)*26.0; float w=0.1+z*(0.55+uA*5.0)+uA*1.2;
  float beam=exp(-(x*x)/(w*w)); gl_FragColor=vec4(uColor*beam*pow(1.0-z,1.6)*uK*0.55,1.0); }`;
const F_INNER = `void main(){ float x=abs(vUv.x-0.5)*60.0; float far=vUv.y; float w=2.0+far*9.0; float beam=exp(-(x*x)/(w*w));
  gl_FragColor=vec4(uColor*beam*pow(far,1.4)*uK*0.5,1.0); }`;
/** uA = hasta dónde llega el camino (0-1 del largo). */
const F_PATH = `void main(){ float x=abs(vUv.x-0.5)*2.0; float along=1.0-vUv.y; float head=smoothstep(uA,uA-0.04,along);
  float core=exp(-x*x*9.0); float tip=exp(-pow((along-uA)*26.0,2.0))*1.6; gl_FragColor=vec4(uColor*core*(0.55*head+tip)*uK,1.0); }`;
const F_SOFT = `void main(){ vec2 p=abs(vUv-0.5)*2.0; float a=smoothstep(1.0,0.55,p.x)*smoothstep(1.0,0.7,p.y); gl_FragColor=vec4(uColor*a*uK,1.0); }`;

const SHAFTS = [-0.52, -0.3, -0.13, 0.11, 0.27, 0.5];

/** La gloria que sale del Lugar Santísimo: fuente, rasgadura, derrame y haces. */
export const Glory: React.FC<{k: number; front: number; part: number}> = ({k, front, part}) => {
  const top = VEIL.height;
  const f = Math.max(0, front);
  const torn = Math.min(1, Math.max(0, (top - front) / top));
  const open = k * torn;
  const h = Math.max(0.001, top - f);
  return (
    <group>
      <Sheet frag={F_SOURCE} k={k > 0 ? 0.5 + k * 0.28 : 0} position={[0, 9, -40]}>
        <planeGeometry args={[90, 60]} />
      </Sheet>
      {torn > 0 ? (
        <>
          <Sheet frag={F_SEAM} k={k * (1 - part * 0.75)} position={[0, f + h / 2, 0.35]} scale={[1.6 + part * 7, h + 2.4, 1]}>
            <planeGeometry args={[1, 1]} />
          </Sheet>
          <Sheet frag={F_SPILL} k={open} a={part} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 13]}>
            <planeGeometry args={[26, 26]} />
          </Sheet>
          <Sheet frag={F_INNER} k={open} color="#ffd9a0" rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, -24]}>
            <planeGeometry args={[60, 48]} />
          </Sheet>
          {SHAFTS.map((a, i) => {
            const len = 15 + (i % 3) * 3;
            return (
              <group key={i} rotation={[0, a * (0.5 + part * 0.9), 0]}>
                <Sheet frag={F_SHAFT} k={open} a={i + 1} position={[0, f + h / 2 - 0.6, len / 2]} rotation={[0, Math.PI / 2, 0]} scale={[len, h + 1.2, 1]}>
                  <planeGeometry args={[1, 1]} />
                </Sheet>
              </group>
            );
          })}
          <pointLight position={[0, f + h * 0.5, 1.2]} color={C.light} intensity={open * 60} distance={46} decay={1.7} />
          <pointLight position={[0, 1.2, 2.5]} color={C.light} intensity={open * torn * 40} distance={30} decay={1.8} />
        </>
      ) : null}
    </group>
  );
};

/** Camino de luz sobre el suelo: de z=22 hacia el velo (reach 1 = se detiene en el velo; 2 = lo cruza hasta el trono). */
export const PathLight: React.FC<{reach: number; k?: number}> = ({reach, k = 1}) => {
  const z0 = 22;
  const z1 = -21;
  const len = z0 - z1;
  const a = reach <= 1 ? (reach * (z0 - 0.9)) / len : ((z0 - 0.9) + (reach - 1) * (0.9 - z1)) / len;
  return (
    <Sheet frag={F_PATH} k={reach > 0 ? k : 0} a={a} color="#ffd98a" rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.03, (z0 + z1) / 2]}>
      <planeGeometry args={[1.5, len]} />
    </Sheet>
  );
};

/** Cruz de luz (sombra/anuncio sobre el velo, o gloria detrás del trono). */
export const LightCross: React.FC<{pos: [number, number, number]; h: number; k: number; color?: string}> = ({pos, h, k, color = '#ffe2a8'}) => (
  <group position={pos}>
    <Sheet frag={F_SOFT} k={k} color={color} position={[0, h / 2, 0]}>
      <planeGeometry args={[h * 0.11, h]} />
    </Sheet>
    <Sheet frag={F_SOFT} k={k} color={color} position={[0, h * 0.7, 0]}>
      <planeGeometry args={[h * 0.56, h * 0.11]} />
    </Sheet>
  </group>
);

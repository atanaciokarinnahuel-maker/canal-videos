import {useMemo} from 'react';
import * as THREE from 'three';
import {random} from 'remotion';
import {C} from '../timeline';

const COUNT = 900;

/** Polvo de oro en suspensión: solo se ve donde lo toca la luz. */
export const Dust: React.FC<{t: number; k: number}> = ({t, k}) => {
  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry();
    const p = new Float32Array(COUNT * 3);
    const s = new Float32Array(COUNT);
    for (let i = 0; i < COUNT; i++) {
      const r = Math.pow(random(`x${i}`), 1.6) * 5.2 * (random(`sx${i}`) > 0.5 ? 1 : -1);
      p[i * 3] = r;
      p[i * 3 + 1] = random(`y${i}`) * 11;
      p[i * 3 + 2] = -20 + random(`z${i}`) * 44;
      s[i] = random(`s${i}`);
    }
    g.setAttribute('position', new THREE.BufferAttribute(p, 3));
    g.setAttribute('aSeed', new THREE.BufferAttribute(s, 1));
    return g;
  }, []);

  const uniforms = useMemo(() => ({uT: {value: 0}, uK: {value: 0}, uColor: {value: new THREE.Color(C.goldHi)}}), []);
  uniforms.uT.value = t;
  uniforms.uK.value = k;

  return (
    <points geometry={geo} frustumCulled={false}>
      <shaderMaterial
        uniforms={uniforms}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
        fog={false}
        toneMapped={false}
        vertexShader={/* glsl */ `
          attribute float aSeed;
          uniform float uT;
          varying float vA;
          void main() {
            vec3 p = position;
            p.y = mod(p.y + uT * (0.05 + aSeed * 0.12), 11.0);
            p.x += sin(uT * 0.3 + aSeed * 40.0) * 0.35;
            p.z += cos(uT * 0.22 + aSeed * 17.0) * 0.4;
            vec4 mv = modelViewMatrix * vec4(p, 1.0);
            gl_Position = projectionMatrix * mv;
            float depth = -mv.z;
            gl_PointSize = (5.0 + aSeed * 13.0) * 14.0 / max(depth, 0.6);
            float nearAxis = exp(-abs(p.x) * 0.55);
            float twinkle = 0.6 + 0.4 * sin(uT * 1.7 + aSeed * 90.0);
            vA = nearAxis * twinkle * smoothstep(0.5, 2.5, depth) * (1.0 - smoothstep(22.0, 36.0, depth));
          }
        `}
        fragmentShader={/* glsl */ `
          uniform float uK;
          uniform vec3 uColor;
          varying float vA;
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

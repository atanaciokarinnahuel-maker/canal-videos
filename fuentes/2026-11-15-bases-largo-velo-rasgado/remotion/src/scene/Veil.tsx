import {useMemo} from 'react';
import * as THREE from 'three';
import {T, VEIL, lerpT, tearFrontY, veilPart} from '../timeline';

const SEG_U = 44;
const SEG_V = 90;

/** Textura procedural: azul, púrpura y carmesí (Éx 26:31) con hilos de oro. */
const makeVeilTexture = () => {
  const w = 64;
  const h = 512;
  const data = new Uint8Array(w * h * 4);
  const blue = new THREE.Color('#141c4a');
  const purple = new THREE.Color('#3a1550');
  const scarlet = new THREE.Color('#6e1220');
  const gold = new THREE.Color('#c9a35a');
  const c = new THREE.Color();
  for (let y = 0; y < h; y++) {
    const v = y / (h - 1);
    if (v > 0.5) c.copy(purple).lerp(blue, (v - 0.5) * 2);
    else c.copy(scarlet).lerp(purple, v * 2);
    const band = [0.045, 0.06, 0.94, 0.955].some((b) => Math.abs(v - b) < 0.0035);
    for (let x = 0; x < w; x++) {
      const weave = 0.9 + 0.1 * Math.sin(x * 2.4) * Math.sin(y * 3.1);
      const px = band ? gold : c;
      const i = (y * w + x) * 4;
      data[i] = px.r * 255 * (band ? 1 : weave);
      data[i + 1] = px.g * 255 * (band ? 1 : weave);
      data[i + 2] = px.b * 255 * (band ? 1 : weave);
      data[i + 3] = 255;
    }
  }
  const tex = new THREE.DataTexture(data, w, h, THREE.RGBAFormat);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.wrapS = THREE.RepeatWrapping;
  tex.repeat.set(6, 1);
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = THREE.LinearMipmapLinearFilter;
  tex.generateMipmaps = true;
  tex.needsUpdate = true;
  return tex;
};

const smoothstep = (a: number, b: number, x: number) => {
  const k = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return k * k * (3 - 2 * k);
};

/** Una mitad del velo. `side` = -1 izquierda, +1 derecha. Toda la tela se calcula en CPU por frame. */
const Half: React.FC<{side: 1 | -1; t: number; map: THREE.Texture}> = ({side, t, map}) => {
  const geo = useMemo(() => new THREE.PlaneGeometry(1, 1, SEG_U, SEG_V), []);

  useMemo(() => {
    const pos = geo.attributes.position as THREE.BufferAttribute;
    const uv = geo.attributes.uv as THREE.BufferAttribute;
    const front = tearFrontY(t);
    const part = veilPart(t);
    // golpe de aire cuando la luz irrumpe
    const gust = lerpT(t, [T.tearStart, T.tearStart + 0.5, T.tearEnd + 2], [0, 1, 0.25]);
    for (let i = 0; i < pos.count; i++) {
      // u: 0 en el borde central (la rasgadura), 1 en el borde exterior
      const u = side === 1 ? uv.getX(i) : 1 - uv.getX(i);
      const v = uv.getY(i);
      const y = v * VEIL.height;
      const torn = smoothstep(0, 1.6, y - front); // 0 = intacto, 1 = ya rasgado
      const gather = torn * part * 0.9;
      const edge = Math.pow(1 - u, 3);

      const x = side * (VEIL.halfW * gather + u * VEIL.halfW * (1 - gather)) + side * torn * edge * 0.04 * Math.sin(y * 7.0 + side);

      const foldAmp = 0.17 + 0.4 * gather;
      const folds = foldAmp * Math.sin(u * 21 + side * 1.3 + 0.5 * Math.sin(y * 0.45 + t * 0.55));
      const sway = 0.07 * (1 - v * 0.85) * Math.sin(t * 0.7 + y * 0.4 + u * 2);
      const flutter = torn * edge * (0.25 + 0.55 * gust) * Math.sin(t * 3.1 + y * 1.25 + side * 0.8);
      const blown = torn * edge * gust * 0.55;

      pos.setXYZ(i, x, y, folds + sway + flutter + blown);
    }
    pos.needsUpdate = true;
    geo.computeVertexNormals();
    geo.computeBoundingSphere();
  }, [geo, side, t]);

  return (
    <mesh geometry={geo} frustumCulled={false}>
      <meshStandardMaterial
        map={map}
        emissiveMap={map}
        emissive="#ffffff"
        emissiveIntensity={0.1}
        roughness={0.92}
        metalness={0}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
};

export const Veil: React.FC<{t: number}> = ({t}) => {
  const map = useMemo(makeVeilTexture, []);
  return (
    <group>
      <Half side={-1} t={t} map={map} />
      <Half side={1} t={t} map={map} />
    </group>
  );
};

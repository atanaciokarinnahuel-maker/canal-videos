import {useMemo} from 'react';
import * as THREE from 'three';

export const VEIL = {halfW: 3.7, height: 10.4};
const SEG_U = 44;
const SEG_V = 90;

/** Un querubín bordado con hilo de oro (trazo). */
const cherub = (ctx: CanvasRenderingContext2D, x: number, y: number, s: number) => {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(s, s);
  ctx.beginPath();
  ctx.arc(0, -34, 9, 0, Math.PI * 2); // cabeza
  ctx.moveTo(0, -24);
  ctx.bezierCurveTo(13, -6, 11, 26, 0, 46); // túnica
  ctx.bezierCurveTo(-11, 26, -13, -6, 0, -24);
  for (const d of [-1, 1]) {
    // ala alzada: contorno + dos plumas interiores
    ctx.moveTo(d * 7, -16);
    ctx.bezierCurveTo(d * 22, -58, d * 58, -78, d * 80, -70);
    ctx.bezierCurveTo(d * 74, -44, d * 52, -14, d * 9, -4);
    ctx.moveTo(d * 12, -18);
    ctx.bezierCurveTo(d * 28, -44, d * 48, -58, d * 64, -58);
    ctx.moveTo(d * 13, -11);
    ctx.bezierCurveTo(d * 30, -28, d * 44, -38, d * 56, -42);
  }
  ctx.stroke();
  ctx.restore();
};

/** Tela: azul, púrpura y carmesí con querubines (Éx 26:31). Devuelve color y mapa emisivo (hilo de oro). */
const makeVeilTextures = () => {
  const W = 512;
  const H = 1440;
  const mk = () => {
    const c = document.createElement('canvas');
    c.width = W;
    c.height = H;
    return c;
  };
  const base = mk();
  const emis = mk();
  const b = base.getContext('2d')!;
  const e = emis.getContext('2d')!;
  const g = b.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, '#141c4a');
  g.addColorStop(0.5, '#3a1550');
  g.addColorStop(1, '#6e1220');
  b.fillStyle = g;
  b.fillRect(0, 0, W, H);
  // trama
  b.globalAlpha = 0.07;
  b.strokeStyle = '#000';
  for (let x = 0; x < W; x += 4) {
    b.beginPath();
    b.moveTo(x, 0);
    b.lineTo(x, H);
    b.stroke();
  }
  b.globalAlpha = 1;
  e.fillStyle = '#000';
  e.fillRect(0, 0, W, H);
  e.globalAlpha = 0.1;
  e.drawImage(base, 0, 0);
  e.globalAlpha = 1;
  for (const ctx of [b, e]) {
    ctx.strokeStyle = ctx === b ? '#c9a35a' : '#e7c27a';
    ctx.fillStyle = ctx.strokeStyle;
    for (const v of [0.045, 0.06, 0.94, 0.955]) ctx.fillRect(0, H * v - 4, W, 7);
    ctx.lineWidth = 2.6;
    ctx.lineCap = 'round';
    for (let r = 0; r < 4; r++) for (let col = 0; col < 2; col++) cherub(ctx, W * (0.27 + col * 0.46), H * (0.2 + r * 0.2), 1.1);
  }
  const tex = (c: HTMLCanvasElement) => {
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.anisotropy = 4;
    return t;
  };
  return {map: tex(base), emissiveMap: tex(emis)};
};

const smoothstep = (a: number, b: number, x: number) => {
  const k = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return k * k * (3 - 2 * k);
};

export type VeilState = {time: number; front: number; part: number; gust: number; emis?: number};

/** Una mitad del velo. Toda la tela se calcula en CPU por frame (determinista). */
const Half: React.FC<{side: 1 | -1; s: VeilState; tex: {map: THREE.Texture; emissiveMap: THREE.Texture}}> = ({side, s, tex}) => {
  const geo = useMemo(() => new THREE.PlaneGeometry(1, 1, SEG_U, SEG_V), []);
  useMemo(() => {
    const pos = geo.attributes.position as THREE.BufferAttribute;
    const uv = geo.attributes.uv as THREE.BufferAttribute;
    const t = s.time;
    for (let i = 0; i < pos.count; i++) {
      const u = side === 1 ? uv.getX(i) : 1 - uv.getX(i); // 0 = rasgadura, 1 = borde exterior
      const v = uv.getY(i);
      const y = v * VEIL.height;
      const torn = smoothstep(0, 1.6, y - s.front);
      const gather = torn * s.part * 0.9;
      const edge = Math.pow(1 - u, 3);
      const x = side * (VEIL.halfW * gather + u * VEIL.halfW * (1 - gather)) + side * torn * edge * 0.04 * Math.sin(y * 7.0 + side);
      const folds = (0.17 + 0.4 * gather) * Math.sin(u * 21 + side * 1.3 + 0.5 * Math.sin(y * 0.45 + t * 0.55));
      const sway = 0.07 * (1 - v * 0.85) * Math.sin(t * 0.7 + y * 0.4 + u * 2);
      const flutter = torn * edge * (0.25 + 0.55 * s.gust) * Math.sin(t * 3.1 + y * 1.25 + side * 0.8);
      pos.setXYZ(i, x, y, folds + sway + flutter + torn * edge * s.gust * 0.55);
    }
    pos.needsUpdate = true;
    geo.computeVertexNormals();
  }, [geo, side, s.time, s.front, s.part, s.gust]);
  return (
    <mesh geometry={geo} frustumCulled={false}>
      <meshStandardMaterial map={tex.map} emissiveMap={tex.emissiveMap} emissive="#ffffff" emissiveIntensity={s.emis ?? 0.42} roughness={0.92} metalness={0} side={THREE.DoubleSide} />
    </mesh>
  );
};

export const Veil: React.FC<{s: VeilState}> = ({s}) => {
  const tex = useMemo(makeVeilTextures, []);
  return (
    <group>
      <Half side={-1} s={s} tex={tex} />
      <Half side={1} s={s} tex={tex} />
    </group>
  );
};

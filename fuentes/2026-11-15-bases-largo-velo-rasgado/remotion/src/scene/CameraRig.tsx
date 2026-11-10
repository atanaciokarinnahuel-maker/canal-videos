import {useThree} from '@react-three/fiber';
import {useMemo} from 'react';
import * as THREE from 'three';
import {T} from '../timeline';

/** Un solo plano secuencia: avance por el pasillo → tilt de arriba abajo → fly-through. */
const KEYS: {t: number; p: [number, number, number]; l: [number, number, number]}[] = [
  {t: 0, p: [0.7, 1.5, 24], l: [0, 4.6, 0]},
  {t: 6, p: [-0.6, 1.7, 19.5], l: [0, 4.9, 0]},
  {t: 12, p: [0.35, 2.3, 15.5], l: [0, 5.2, 0]},
  {t: T.tearStart, p: [0.25, 4.3, 13.6], l: [0, 7.4, 0]},
  {t: T.tearEnd, p: [0, 2.3, 12.2], l: [0, 2.2, 0]},
  {t: 19.6, p: [-1.3, 0.75, 11.2], l: [0, 5.6, 0]},
  {t: T.flyStart, p: [0.5, 2.7, 10.4], l: [0, 5.0, -4]},
  {t: T.flyEnd, p: [0, 3.2, -3.5], l: [0, 4.8, -22]},
  {t: 31, p: [0.9, 3.7, -9.5], l: [0, 5.1, -22]},
  {t: 36, p: [-0.5, 4.1, -12.5], l: [0, 5.3, -22]},
];

const smooth = (x: number) => x * x * (3 - 2 * x);

export const CameraRig: React.FC<{t: number}> = ({t}) => {
  const camera = useThree((s) => s.camera);
  const {pos, look} = useMemo(
    () => ({
      pos: new THREE.CatmullRomCurve3(KEYS.map((k) => new THREE.Vector3(...k.p)), false, 'centripetal'),
      look: new THREE.CatmullRomCurve3(KEYS.map((k) => new THREE.Vector3(...k.l)), false, 'centripetal'),
    }),
    [],
  );

  // tiempo -> parámetro de curva (suavizado por tramo para que nada arranque ni frene en seco)
  let i = KEYS.findIndex((k, n) => n < KEYS.length - 1 && t < KEYS[n + 1].t);
  if (i < 0) i = KEYS.length - 2;
  const local = Math.min(1, Math.max(0, (t - KEYS[i].t) / (KEYS[i + 1].t - KEYS[i].t)));
  const u = (i + (local * 0.6 + smooth(local) * 0.4)) / (KEYS.length - 1);

  // Mutación determinista por frame (Remotion renderiza cada frame de forma aislada).
  const p = pos.getPoint(u);
  const l = look.getPoint(u);
  const breathe = Math.sin(t * 0.9) * 0.03;
  camera.position.set(p.x, p.y + breathe, p.z);
  camera.lookAt(l);
  camera.updateMatrixWorld();
  return null;
};

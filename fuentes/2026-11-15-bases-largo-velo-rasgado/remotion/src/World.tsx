import {Bloom, EffectComposer, Noise, Vignette} from '@react-three/postprocessing';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {B, at, cl, pulse} from './tl';
import {shotAt} from './shots';
import {Ark} from './sets/Ark';
import {Eden, edenFigureZ} from './sets/Eden';
import {A, Hall, figureState, hallState, priestState} from './sets/Hall';
import {Model} from './sets/Model';
import {Calvary, Desert} from './sets/Outdoor';
import {Stage} from './sets/Stage';
import {VEIL} from './sets/Veil';
import {Wheel} from './sets/Wheel';

const FOG: Record<string, [string, number]> = {
  model: ['#020306', 0.018], ark: ['#070503', 0.03], eden: ['#020a06', 0.026], desert: ['#0a0705', 0.01],
  wheel: ['#020306', 0.028], stage: ['#020306', 0.034], calvary: ['#050406', 0.007],
};
const dark = new THREE.Color('#020306');
const warm = new THREE.Color('#1c1206');
const tmp = new THREE.Color();
const CRY = at(5, 'Jesús clama');

/** Temblor de cámara en los golpes del relato. */
const shake = (t: number) =>
  0.13 * pulse(t, A.tear0, 0.05, 1.3) + 0.09 * pulse(t, A.godTore, 0.05, 1.2) + 0.07 * pulse(t, CRY + 0.3, 0.1, 1.6) + 0.05 * pulse(t, A.closeAgain + 0.55, 0.04, 0.7) + 0.05 * pulse(t, B(4), 0.04, 0.6);

/** Mundo 3D: elige el set del plano actual, mueve la cámara y aplica el acabado. */
export const World: React.FC<{t: number; fov?: number}> = ({t, fov}) => {
  const {shot, u} = shotAt(t);
  const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
  const scene = useThree((s) => s.scene);

  // cámara: deriva con salida suave entre los dos encuadres del plano
  const e = 1 - Math.pow(1 - u, 1.7);
  const [p0, l0, p1, l1] = shot.cam;
  let oz = 0;
  if (shot.follow === 'priest') oz = priestState(t, shot.mode)?.z ?? 0;
  if (shot.follow === 'figure') oz = figureState(t)?.pos[2] ?? 0;
  if (shot.follow === 'edenFig') oz = edenFigureZ(t) + 2.5;
  const sk = shake(t);
  camera.position.set(p0[0] + (p1[0] - p0[0]) * e + sk * Math.sin(t * 47), p0[1] + (p1[1] - p0[1]) * e + sk * Math.sin(t * 61 + 1), p0[2] + (p1[2] - p0[2]) * e + oz);
  camera.lookAt(l0[0] + (l1[0] - l0[0]) * e, l0[1] + (l1[1] - l0[1]) * e + sk * 0.5 * Math.sin(t * 53 + 2), l0[2] + (l1[2] - l0[2]) * e + oz);
  camera.fov = fov ?? shot.fov ?? 42;
  camera.updateProjectionMatrix();
  camera.updateMatrixWorld();

  // niebla por set
  if (!scene.fog) scene.fog = new THREE.FogExp2(0x020306, 0.03);
  const fog = scene.fog as THREE.FogExp2;
  if (shot.set === 'hall') {
    const s = hallState(t, shot.mode);
    const k = s.glory * cl((VEIL.height - s.front) / VEIL.height);
    fog.color.copy(dark).lerp(warm, Math.min(1, k * 0.25 + s.inside * 0.8));
    fog.density = 0.03 - s.inside * 0.012;
  } else {
    fog.color.copy(tmp.set(FOG[shot.set][0]));
    fog.density = FOG[shot.set][1];
  }
  scene.background = fog.color;

  return (
    <>
      {shot.set === 'hall' ? <Hall t={t} mode={shot.mode} /> : null}
      {shot.set === 'model' ? <Model t={t} mode={shot.mode} /> : null}
      {shot.set === 'ark' ? <Ark t={t} mode={shot.mode} /> : null}
      {shot.set === 'eden' ? <Eden t={t} /> : null}
      {shot.set === 'desert' ? <Desert t={t} /> : null}
      {shot.set === 'wheel' ? <Wheel t={t} /> : null}
      {shot.set === 'stage' ? <Stage t={t} mode={shot.mode} /> : null}
      {shot.set === 'calvary' ? <Calvary t={t} mode={shot.mode} /> : null}
      <EffectComposer multisampling={0}>
        <Bloom intensity={0.7} luminanceThreshold={0.74} luminanceSmoothing={0.3} mipmapBlur radius={0.82} />
        <Noise opacity={0.045} />
        <Vignette eskil={false} offset={0.22} darkness={0.82} />
      </EffectComposer>
    </>
  );
};

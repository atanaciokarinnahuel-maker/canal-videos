import {Bloom, EffectComposer, Noise, Vignette} from '@react-three/postprocessing';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {C, T, glory, lerpT, tornFraction} from '../timeline';
import {CameraRig} from './CameraRig';
import {Dust} from './Dust';
import {Glory} from './Glory';
import {Cross, Temple} from './Temple';
import {Veil} from './Veil';

const dark = new THREE.Color('#020306');
const warm = new THREE.Color('#1c1206');

export const Scene: React.FC<{t: number}> = ({t}) => {
  const scene = useThree((s) => s.scene);
  const k = glory(t) * tornFraction(t);

  // La niebla pasa de negro frío a ámbar al cruzar el velo.
  const inside = lerpT(t, [T.flyStart, T.flyEnd + 1], [0, 1]);
  if (!scene.fog) scene.fog = new THREE.FogExp2(dark.getHex(), 0.028);
  const fog = scene.fog as THREE.FogExp2;
  fog.color.copy(dark).lerp(warm, Math.min(1, k * 0.25 + inside * 0.8));
  fog.density = 0.03 - inside * 0.012;
  scene.background = fog.color;

  const fadeIn = lerpT(t, [0, 2.2], [0, 1]);
  // pulso carmesí: "y nunca sin sangre"
  const blood = lerpT(t, [T.blood - 0.6, T.blood + 0.5, T.tearStart - 0.6, T.tearStart], [0, 1, 0.7, 0]);

  return (
    <>
      <CameraRig t={t} />

      <ambientLight intensity={0.2 * fadeIn} color="#93a4c8" />
      {/* luz fría cenital: el pasillo antes de la rasgadura */}
      <spotLight position={[0, 17, 10]} angle={0.5} penumbra={1} intensity={950 * fadeIn * (1 - blood * 0.55)} color="#9fb2d8" distance={50} decay={1.6} />
      {/* lámparas cálidas que hacen brillar el oro del marco */}
      {[-1, 1].map((s) => (
        <pointLight key={s} position={[s * 4.6, 6.5, 2.2]} intensity={26 * fadeIn} color="#ffc26b" distance={14} decay={1.8} />
      ))}
      <pointLight position={[0, 3.2, 3.4]} intensity={150 * blood} color={C.crimson} distance={18} decay={1.6} />
      {/* luces frías de contra entre pilares: dan lectura al pasillo */}
      {[6, 14, 22].map((z) => (
        <pointLight key={z} position={[0, 10, z]} intensity={85 * fadeIn} color="#8ea2cc" distance={20} decay={1.7} />
      ))}
      {/* relleno frontal de la cruz */}
      <pointLight position={[1.5, 6, -15]} intensity={70 * inside} color="#ffd9a0" distance={18} decay={1.6} />

      <Temple />
      <Cross />
      <Veil t={t} />
      <Glory t={t} />
      <Dust t={t} k={0.1 * fadeIn + k * 0.75} />

      <EffectComposer multisampling={4}>
        <Bloom intensity={0.7} luminanceThreshold={0.74} luminanceSmoothing={0.3} mipmapBlur radius={0.82} />
        <Noise opacity={0.045} />
        <Vignette eskil={false} offset={0.22} darkness={0.82} />
      </EffectComposer>
    </>
  );
};

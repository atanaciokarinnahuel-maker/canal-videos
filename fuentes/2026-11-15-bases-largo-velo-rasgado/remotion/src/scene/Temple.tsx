import {C, VEIL} from '../timeline';

const Obsidian: React.FC = () => <meshStandardMaterial color="#14161d" roughness={0.24} metalness={0.45} />;
const MatteGold: React.FC = () => <meshStandardMaterial color={C.gold} roughness={0.42} metalness={0.85} emissive={C.goldDeep} emissiveIntensity={0.08} />;

const PILLAR_Z = [3.2, 7.4, 11.6, 15.8, 20, 24.2, 28.4];
const PILLAR_H = 16;

const Pillar: React.FC<{x: number; z: number}> = ({x, z}) => (
  <group position={[x, 0, z]}>
    <mesh position={[0, PILLAR_H / 2, 0]}>
      <boxGeometry args={[1.1, PILLAR_H, 1.1]} />
      <Obsidian />
    </mesh>
    {/* zócalo y anillo de oro mate */}
    <mesh position={[0, 0.12, 0]}>
      <boxGeometry args={[1.32, 0.24, 1.32]} />
      <MatteGold />
    </mesh>
    <mesh position={[0, 7.2, 0]}>
      <boxGeometry args={[1.16, 0.07, 1.16]} />
      <MatteGold />
    </mesh>
  </group>
);

/** Arquitectura: pasillo de obsidiana, muro del santuario y marco de oro del velo. */
export const Temple: React.FC = () => {
  const openW = VEIL.halfW - 0.1;
  const topY = VEIL.height - 0.1;
  return (
    <group>
      {/* suelo pulido (pasillo + Lugar Santísimo) */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, -10]}>
        <planeGeometry args={[90, 140]} />
        <meshStandardMaterial color="#07080b" roughness={0.3} metalness={0.8} />
      </mesh>

      {PILLAR_Z.flatMap((z) => [<Pillar key={`l${z}`} x={-4.7} z={z} />, <Pillar key={`r${z}`} x={4.7} z={z} />])}

      {/* muro que separa: solo el velo deja pasar */}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * (openW + 20), 15, -0.7]}>
          <boxGeometry args={[40, 30, 1]} />
          <Obsidian />
        </mesh>
      ))}
      <mesh position={[0, topY + 10, -0.7]}>
        <boxGeometry args={[openW * 2, 20, 1]} />
        <Obsidian />
      </mesh>

      {/* marco de oro mate */}
      {[-1, 1].map((s) => (
        <mesh key={s} position={[s * (openW + 0.14), topY / 2, 0.0]}>
          <boxGeometry args={[0.28, topY, 0.6]} />
          <MatteGold />
        </mesh>
      ))}
      <mesh position={[0, topY + 0.16, 0.0]}>
        <boxGeometry args={[openW * 2 + 0.56, 0.32, 0.6]} />
        <MatteGold />
      </mesh>
    </group>
  );
};

/** Lo que hay al otro lado: la cruz —«por el velo, esto es, su carne» (Heb 10:20). */
export const Cross: React.FC = () => (
  <group position={[0, 0, -22]}>
    <mesh position={[0, 0.2, 0]}>
      <boxGeometry args={[3.2, 0.4, 3.2]} />
      <Obsidian />
    </mesh>
    <mesh position={[0, 4.4, 0]}>
      <boxGeometry args={[0.46, 8, 0.46]} />
      <MatteGold />
    </mesh>
    <mesh position={[0, 6.1, 0]}>
      <boxGeometry args={[4.2, 0.46, 0.46]} />
      <MatteGold />
    </mesh>
  </group>
);

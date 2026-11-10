import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFonts} from './fonts';
import {DUR, cl, pulse} from './tl';
import {SHOTS, shotAt} from './shots';
import {A} from './sets/Hall';
import {Captions} from './ui/Captions';
import {Cards} from './ui/Cards';
import {Hud, REVEAL} from './ui/Hud';
import {World} from './World';

loadFonts();

/** Largo 16:9 «El velo se rasgó de arriba abajo». Todo se deriva del frame actual. */
export const Largo: React.FC<{qa?: boolean; qaAt?: number}> = ({qa, qaAt = 0.55}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  // modo QA: el frame i muestra el plano i (a mitad de su duración)
  const t = qa ? SHOTS[frame].t + shotAt(SHOTS[frame].t + 0.001).dur * qaAt : frame / fps;
  const flash = 0.5 * pulse(t, A.tear0, 0.04, 0.5) + 0.35 * pulse(t, A.godTore, 0.05, 0.6) + 0.4 * pulse(t, REVEAL, 0.06, 0.8);
  const black = Math.max(1 - cl(t / 1.2), cl((t - (DUR - 1.2)) / 1.1));
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas width={width} height={height} dpr={1} camera={{fov: 42, near: 0.1, far: 260}} gl={{antialias: false}}>
        <World t={t} />
      </ThreeCanvas>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.5) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 62%, rgba(0,0,0,.62) 100%)'}} />
      <AbsoluteFill style={{background: '#fff3d6', opacity: flash}} />
      <Cards t={t} />
      <Hud t={t} />
      <Captions t={t} />
      <AbsoluteFill style={{background: '#000', opacity: black}} />
    </AbsoluteFill>
  );
};

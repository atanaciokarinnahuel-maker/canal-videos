import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {Captions} from './Captions';
import {loadFonts} from './fonts';
import {Scene} from './scene/Scene';
import {VO_OFFSET} from './timeline';

loadFonts();

export const VeloRasgado: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const t = frame / fps;

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas
        width={width}
        height={height}
        dpr={1}
        camera={{fov: 50, near: 0.1, far: 200, position: [0, 2, 24]}}
        gl={{antialias: false, powerPreference: 'high-performance'}}
      >
        <Scene t={t} />
      </ThreeCanvas>

      <Captions />

      <Audio src={staticFile('musica.wav')} volume={0.9} />
      <Sequence from={Math.round(VO_OFFSET * fps)}>
        <Audio src={staticFile('voz.mp3')} volume={1} />
      </Sequence>
    </AbsoluteFill>
  );
};

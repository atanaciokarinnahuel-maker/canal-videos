import React from 'react';
import {Composition} from 'remotion';
import {Previz} from './Previz';
import {VeloRasgado} from './Video';
import {DURATION_S, FPS, HEIGHT, WIDTH} from './timeline';

export const Root: React.FC = () => (
  <>
  <Composition id="Previz" component={Previz} durationInFrames={3} fps={FPS} width={1920} height={1080} />
  <Composition
    id="VeloRasgado"
    component={VeloRasgado}
    durationInFrames={DURATION_S * FPS}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
  />
  </>
);

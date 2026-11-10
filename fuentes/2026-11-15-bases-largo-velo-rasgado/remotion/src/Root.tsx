import React from 'react';
import {Composition} from 'remotion';
import {Largo} from './Largo';
import {SHOTS} from './shots';
import {FPS, FRAMES, HEIGHT, WIDTH} from './tl';

export const Root: React.FC = () => (
  <>
    <Composition id="Largo" component={Largo} durationInFrames={FRAMES} fps={FPS} width={WIDTH} height={HEIGHT} />
    {/* Hoja de control: un frame por plano */}
    <Composition id="QA" component={Largo} durationInFrames={SHOTS.length} fps={FPS} width={WIDTH} height={HEIGHT} defaultProps={{qa: true, qaAt: 0.55}} />
  </>
);

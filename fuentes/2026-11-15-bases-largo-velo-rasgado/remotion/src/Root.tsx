import React from 'react';
import {Composition} from 'remotion';
import {Largo} from './Largo';
import {Short} from './Short';
import {SHORTS, SHORT_TAIL} from './shorts';
import {SHOTS} from './shots';
import {FPS, FRAMES, HEIGHT, WIDTH} from './tl';

export const Root: React.FC = () => (
  <>
    <Composition id="Largo" component={Largo} durationInFrames={FRAMES} fps={FPS} width={WIDTH} height={HEIGHT} />
    {/* Hoja de control: un frame por plano */}
    <Composition id="QA" component={Largo} durationInFrames={SHOTS.length} fps={FPS} width={WIDTH} height={HEIGHT} defaultProps={{qa: true, qaAt: 0.55}} />
    {SHORTS.map((s, i) => (
      <Composition key={s.id} id={`Short${s.n}`} component={Short} durationInFrames={Math.ceil((s.t1 - s.t0 + SHORT_TAIL) * FPS)} fps={FPS} width={1080} height={1920} defaultProps={{index: i}} />
    ))}
  </>
);

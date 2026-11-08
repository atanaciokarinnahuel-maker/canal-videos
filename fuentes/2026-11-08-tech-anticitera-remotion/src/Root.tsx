import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {FPS, H, W} from './lib';
import {VOICE_DUR} from './words';

export const DUR_FRAMES = Math.ceil((VOICE_DUR + 1.3) * FPS);
export const Root: React.FC = () => (
  <Composition id="Anticitera" component={Video} durationInFrames={DUR_FRAMES} fps={FPS} width={W} height={H} />
);

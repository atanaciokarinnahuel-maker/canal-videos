import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFonts} from './fonts';
import {Hud, VerseTag, Words} from './Hud';
import {Scene} from './scene/Scene';

loadFonts();

/** Tres fotogramas de muestra del formato largo 16:9 (para aprobar el estilo antes del render). */
const SHOTS = [
  {t: 5, lit: 0, chapter: undefined, words: ['algo', 'se', 'rompió', 'dentro', 'del', 'templo'], active: 2, verse: undefined, revealed: false},
  {t: 16.1, lit: 6, chapter: 'De arriba abajo', words: ['Lo', 'rasgó', 'Dios.'], active: 2, verse: 'MATEO 27:51', revealed: false},
  {t: 30.5, lit: 7, chapter: 'El otro lado', words: ['Un', 'trono', 'de', 'gracia.'], active: 3, verse: 'HEBREOS 4:16', revealed: true},
];

export const Previz: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const s = SHOTS[frame % SHOTS.length];
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas width={width} height={height} dpr={1} camera={{fov: 42, near: 0.1, far: 200}} gl={{antialias: false}}>
        <Scene t={s.t} />
      </ThreeCanvas>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 24%, rgba(0,0,0,0) 62%, rgba(0,0,0,.6) 100%)'}} />
      <Hud lit={s.lit} pulse={0.4} chapter={s.chapter} revealed={s.revealed} />
      {s.verse ? <VerseTag text={s.verse} /> : null}
      <Words words={s.words} active={s.active} />
    </AbsoluteFill>
  );
};

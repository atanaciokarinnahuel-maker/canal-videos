import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFonts} from './fonts';
import {A} from './sets/Hall';
import {SHORTS, SHORT_TAIL} from './shorts';
import {C, cl, outCubic, pulse} from './tl';
import {Captions} from './ui/Captions';
import {Cards} from './ui/Cards';
import {REVEAL} from './ui/Hud';
import {World} from './World';

loadFonts();

/** Short vertical 9:16: un tramo del largo con cabecera propia (título-gancho + barra con llama). */
export const Short: React.FC<{index: number; qa?: number}> = ({index, qa}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = SHORTS[index];
  const last = index === SHORTS.length - 1;
  const total = s.t1 - s.t0 + SHORT_TAIL;
  const lt = qa !== undefined ? (s.t1 - s.t0) * qa : frame / fps;
  const t = Math.min(s.t0 + lt, s.t1); // en la cola, la imagen se queda en el último instante
  const tail = cl((lt - (s.t1 - s.t0)) / 0.4);
  void last;
  const prog = cl(lt / total);
  const flash = 0.5 * pulse(t, A.tear0, 0.04, 0.5) + 0.35 * pulse(t, A.godTore, 0.05, 0.6) + 0.4 * pulse(t, REVEAL, 0.06, 0.8);
  const black = Math.max(1 - cl(lt / 0.3), cl((lt - (total - 0.35)) / 0.3));
  const hookIn = outCubic(lt / 0.35);
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas width={width} height={height} dpr={1} camera={{fov: 42, near: 0.1, far: 260}} gl={{antialias: false}}>
        <World t={t} fov={70} />
      </ThreeCanvas>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,.72) 0%, rgba(0,0,0,.35) 20%, rgba(0,0,0,0) 34%, rgba(0,0,0,0) 62%, rgba(0,0,0,.6) 80%, rgba(0,0,0,.6) 100%)'}} />
      <AbsoluteFill style={{background: '#fff3d6', opacity: flash}} />
      <AbsoluteFill style={{opacity: 1 - tail}}>
        <Cards t={t} v />
      </AbsoluteFill>
      {/* cabecera: barra de progreso con llama + título-gancho */}
      <div style={{position: 'absolute', left: 56, right: 56, top: 128}}>
        <div style={{position: 'relative', height: 8, borderRadius: 4, background: 'rgba(241,217,160,.22)'}}>
          <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${prog * 100}%`, borderRadius: 4, background: `linear-gradient(90deg, ${C.goldDeep}, ${C.goldHi})`}} />
          <svg width="44" height="60" viewBox="-22 -44 44 60" style={{position: 'absolute', left: `calc(${prog * 100}% - 22px)`, top: -40, overflow: 'visible'}}>
            <circle cx="0" cy="-14" r={22 + 3 * Math.sin(lt * 9)} fill="#ffb84a" opacity="0.35" />
            <path d="M 0 -34 C 9 -22 8 -9 0 -6 C -8 -9 -9 -22 0 -34 Z" fill="#ffe9b0" />
            <path d="M 0 -25 C 4 -18 4 -11 0 -9 C -4 -11 -4 -18 0 -25 Z" fill="#fff" />
          </svg>
        </div>
        <div style={{marginTop: 26, fontFamily: 'Inter', fontWeight: 500, fontSize: 25, letterSpacing: '0.3em', color: C.gold, textShadow: '0 1px 10px #000'}}>{`EL VELO RASGADO · ${s.n} DE ${SHORTS.length}`}</div>
        <div style={{marginTop: 10, fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 66, lineHeight: 1.04, color: C.ink, whiteSpace: 'pre-line', textShadow: '0 3px 24px rgba(0,0,0,.95)', opacity: hookIn, transform: `translateY(${(1 - hookIn) * 20}px)`}}>
          {s.hook}
        </div>
      </div>
      {tail < 0.5 ? <Captions t={t} bottom={430} size={80} maxWidth={980} /> : null}
      {/* cola: invita a la parte siguiente */}
      {tail > 0 ? (
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', background: `rgba(2,3,6,${0.8 * tail})`, opacity: tail, padding: '0 60px', textAlign: 'center'}}>
          <div style={{fontFamily: 'Inter', fontWeight: 500, fontSize: 30, letterSpacing: '0.34em', color: C.gold}}>ESTO ES SOLO UNA PARTE</div>
          <div style={{marginTop: 26, fontFamily: 'Cormorant Garamond', fontWeight: 600, fontSize: 122, lineHeight: 1.0, color: C.goldHi, transform: `scale(${0.88 + 0.12 * tail})`, textShadow: '0 4px 40px rgba(0,0,0,.9)'}}>
            Mira el video
            <br />
            completo
          </div>
          <div style={{width: 130, height: 3, background: C.gold, margin: '38px 0 30px'}} />
          <div style={{fontFamily: 'Cormorant Garamond', fontStyle: 'italic', fontWeight: 500, fontSize: 56, lineHeight: 1.12, color: C.ink}}>
            «El velo se rasgó
            <br />
            de arriba abajo»
          </div>
          <div style={{marginTop: 44, transform: `scale(${1 + 0.035 * Math.sin(lt * 6)})`, fontFamily: 'Inter', fontWeight: 500, fontSize: 36, letterSpacing: '0.2em', color: '#1a1206', background: `linear-gradient(180deg, ${C.goldHi}, ${C.gold})`, padding: '20px 46px', borderRadius: 60, boxShadow: '0 0 60px rgba(241,217,160,.5)'}}>
            EN EL CANAL · BASES BÍBLICAS
          </div>
        </AbsoluteFill>
      ) : null}
      <AbsoluteFill style={{background: '#000', opacity: black}} />
    </AbsoluteFill>
  );
};

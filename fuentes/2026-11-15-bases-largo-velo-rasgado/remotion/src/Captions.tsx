import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, DURATION_S, Phrase, SCRIPT, T, VO_OFFSET} from './timeline';

const SERIF = 'Cormorant Garamond';
const SANS = 'Inter';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const strip = (w: string) => w.replace(/[.,…;:!?¡¿«»]/g, '');

/** Una frase: las palabras entran una a una, repartidas sobre la duración real de la locución. */
const PhraseBlock: React.FC<{phrase: Phrase; t: number}> = ({phrase, t}) => {
  const start = phrase.from + VO_OFFSET;
  const end = phrase.to + VO_OFFSET;
  const words = phrase.lines.map((l) => l.split(' '));
  const flat = words.flat();
  const weights = flat.map((w) => w.length + 2);
  const total = weights.reduce((a, b) => a + b, 0);
  const span = (end - start) * 0.86;

  const out = interpolate(t, [end + 0.18, end + 0.5], [1, 0], clamp);
  if (t < start - 0.2 || out <= 0) return null;

  let acc = 0;
  let idx = 0;
  const size = phrase.big ? 124 : 82;

  return (
    <div style={{textAlign: 'center', opacity: out, transform: `translateY(${(1 - out) * -14}px)`}}>
      {words.map((line, li) => (
        <div key={li} style={{lineHeight: 1.08}}>
          {line.map((w) => {
            const at = start + (acc / total) * span - 0.06;
            acc += weights[idx++];
            const p = interpolate(t, [at, at + 0.42], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
            const accent = phrase.accent?.[strip(w)];
            return (
              <span
                key={w + at}
                style={{
                  display: 'inline-block',
                  margin: '0 0.13em',
                  fontFamily: SERIF,
                  fontWeight: accent ? 600 : 500,
                  fontStyle: accent === 'gold' && !phrase.big ? 'italic' : 'normal',
                  fontSize: size,
                  letterSpacing: '-0.01em',
                  color: accent === 'crimson' ? '#e2454d' : accent === 'gold' ? C.goldHi : C.ink,
                  opacity: p,
                  filter: `blur(${(1 - p) * 10}px)`,
                  transform: `translateY(${(1 - p) * 22}px)`,
                  textShadow: '0 2px 30px rgba(0,0,0,0.85), 0 0 4px rgba(0,0,0,0.6)',
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
      ))}
      {phrase.ref ? (
        <div
          style={{
            marginTop: 34,
            fontFamily: SANS,
            fontWeight: 500,
            fontSize: 26,
            letterSpacing: '0.34em',
            textTransform: 'uppercase',
            color: C.gold,
            opacity: interpolate(t, [start + 0.5, start + 1.1], [0, 0.9], clamp),
            textShadow: '0 1px 14px rgba(0,0,0,0.9)',
          }}
        >
          {phrase.ref}
        </div>
      ) : null}
    </div>
  );
};

const EndCard: React.FC<{t: number}> = ({t}) => {
  const p = (d: number) => interpolate(t, [T.endCard + d, T.endCard + d + 0.9], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  if (t < T.endCard) return null;
  return (
    <div style={{textAlign: 'center', color: C.ink}}>
      <div style={{fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: 60, lineHeight: 1.18, opacity: p(0), transform: `translateY(${(1 - p(0)) * 18}px)`, textShadow: '0 2px 30px rgba(0,0,0,0.9)'}}>
        «…teniendo libertad para entrar
        <br />
        en el Lugar Santísimo
        <br />
        por la sangre de Jesucristo»
      </div>
      <div style={{width: 120 * p(0.5), height: 2, background: C.gold, margin: '40px auto 30px'}} />
      <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 30, letterSpacing: '0.34em', color: C.goldHi, opacity: p(0.6), textShadow: '0 1px 14px rgba(0,0,0,0.9)'}}>HEBREOS 10:19</div>
    </div>
  );
};

export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const fadeOut = interpolate(t, [DURATION_S - 1.1, DURATION_S - 0.1], [0, 1], clamp);
  const fadeIn = interpolate(t, [0, 1.4], [1, 0], clamp);

  return (
    <AbsoluteFill>
      {/* degradado para que el texto siempre se lea sobre la luz */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0) 46%, rgba(0,0,0,0.5) 66%, rgba(0,0,0,0.5) 80%, rgba(0,0,0,0.15) 100%)'}} />
      <AbsoluteFill style={{top: '57%', height: '26%', justifyContent: 'center', alignItems: 'center', padding: '0 70px'}}>
        {SCRIPT.map((ph, i) => (
          <AbsoluteFill key={i} style={{justifyContent: 'center', alignItems: 'center'}}>
            <PhraseBlock phrase={ph} t={t} />
          </AbsoluteFill>
        ))}
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
          <EndCard t={t} />
        </AbsoluteFill>
      </AbsoluteFill>
      <AbsoluteFill style={{background: '#000', opacity: Math.max(fadeIn, fadeOut)}} />
    </AbsoluteFill>
  );
};

import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, cl, outCubic} from '../tl';
import {wheelYears} from '../sets/Wheel';
import {CARDS, Card} from './cards';
import {Menorah} from './Hud';

const SERIF = 'Cormorant Garamond';
const SANS = 'Inter';
const COL = {gold: C.goldHi, crimson: '#ff4a52', ink: C.ink};
const shadow = '0 4px 40px rgba(0,0,0,.95), 0 0 10px rgba(0,0,0,.95), 0 2px 3px rgba(0,0,0,.9)';

const One: React.FC<{c: Card; t: number; v?: boolean}> = ({c, t, v}) => {
  const k = v ? 0.6 : 1; // escala de texto en vertical
  const zone: React.CSSProperties = v ? {alignItems: 'center', top: '24%', height: '26%', justifyContent: 'center', padding: '0 50px'} : {alignItems: 'center', top: '21%', height: '36%', justifyContent: 'center'};
  const lt = t - c.t;
  const inn = outCubic(lt / 0.28);
  const out = cl((c.t + c.d - t) / 0.25);
  const a = Math.min(inn, out);
  const color = COL[c.color ?? 'gold'];

  if (c.kind === 'key')
    return (
      <AbsoluteFill style={zone}>
        <div style={{position: 'absolute', width: v ? '100%' : '74%', height: '150%', background: 'radial-gradient(ellipse at center, rgba(2,3,6,.42) 0%, rgba(2,3,6,.22) 45%, rgba(2,3,6,0) 72%)', opacity: a}} />
        <div
          style={{
            position: 'relative', fontFamily: SERIF, fontWeight: 600, fontSize: Math.max(v ? 76 : 0, (c.size ?? 130) * k), lineHeight: 0.98, letterSpacing: '0.02em', color, textAlign: 'center', whiteSpace: 'pre-line',
            opacity: a, transform: `scale(${0.82 + 0.18 * inn + lt * 0.012})`, filter: `blur(${(1 - inn) * 12}px)`, textShadow: shadow,
          }}
        >
          {c.text}
        </div>
      </AbsoluteFill>
    );

  if (c.kind === 'boxes')
    return (
      <AbsoluteFill style={{alignItems: 'center', top: '22%', height: '34%', justifyContent: 'center', opacity: out}}>
        <div style={{display: 'flex', gap: 34}}>
          {[0, 1, 2].map((i) => {
            const p = outCubic((lt - 0.25 - i * 0.28) / 0.3);
            return (
              <div key={i} style={{width: [150, 250, 210][i], height: 120, borderRadius: 16, border: `4px solid ${C.goldHi}`, background: 'rgba(8,8,12,.55)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SERIF, fontWeight: 600, fontSize: 96, color: C.goldHi, opacity: p, transform: `translateY(${(1 - p) * 30}px) scale(${0.8 + 0.2 * p})`, boxShadow: '0 0 40px rgba(0,0,0,.8)'}}>
                ?
              </div>
            );
          })}
        </div>
        <div style={{marginTop: 26, fontFamily: SANS, fontWeight: 500, fontSize: 30, letterSpacing: '0.4em', color: C.gold, opacity: inn, textShadow: shadow}}>{c.text}</div>
      </AbsoluteFill>
    );

  if (c.kind === 'verse')
    return (
      <div style={{position: 'absolute', left: v ? 56 : 64, ...(v ? {top: 400} : {bottom: 232}), opacity: a, transform: `translateX(${(1 - inn) * -30}px)`, fontFamily: SANS, fontWeight: 500, fontSize: 26, letterSpacing: '0.3em', color: '#1a1206', background: C.gold, padding: '10px 20px', borderRadius: 8, boxShadow: '0 6px 30px rgba(0,0,0,.6)'}}>
        {c.text}
      </div>
    );

  if (c.kind === 'label')
    return (
      <div style={{position: 'absolute', right: v ? 56 : 64, ...(v ? {top: 396} : {bottom: 232}), opacity: a, transform: `translateX(${(1 - inn) * 30}px)`, display: 'flex', alignItems: 'center', gap: 18}}>
        <div style={{width: 70 * inn, height: 2, background: C.goldHi}} />
        <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 38, letterSpacing: '0.3em', color: C.goldHi, textShadow: shadow}}>{c.text}</div>
      </div>
    );

  if (c.kind === 'strike') {
    const line = outCubic((lt - 0.35) / 0.3);
    return (
      <AbsoluteFill style={zone}>
        <div style={{position: 'absolute', width: v ? '100%' : '74%', height: '150%', background: 'radial-gradient(ellipse at center, rgba(2,3,6,.42) 0%, rgba(2,3,6,.22) 45%, rgba(2,3,6,0) 72%)', opacity: a}} />
        <div style={{position: 'relative', textAlign: 'center', opacity: a * (1 - line * 0.35), fontFamily: SERIF, fontWeight: 600, fontSize: v ? 74 : c.size ?? 112, letterSpacing: '0.03em', color: C.ink, textShadow: shadow, transform: `scale(${0.9 + 0.1 * inn})`}}>
          {c.text}
          <div style={{position: 'absolute', left: '-3%', top: '52%', height: 8, width: `${106 * line}%`, background: '#ff4a52', borderRadius: 4, boxShadow: '0 0 24px rgba(255,60,70,.8)'}} />
        </div>
      </AbsoluteFill>
    );
  }

  if (c.kind === 'quote') {
    const lines = c.text.split('\n');
    return (
      <AbsoluteFill style={{alignItems: 'center', top: v ? '22%' : '17%', height: v ? '34%' : '48%', justifyContent: 'center', opacity: out, padding: v ? '0 40px' : 0}}>
        <div style={{background: 'rgba(6,7,10,.8)', border: `1px solid rgba(201,163,90,.6)`, borderRadius: 18, padding: v ? '30px 34px 26px' : '34px 60px 30px', textAlign: 'center', opacity: inn, transform: `translateY(${(1 - inn) * 24}px)`, boxShadow: '0 20px 80px rgba(0,0,0,.6)'}}>
          {lines.map((l, i) => {
            const p = outCubic((lt - 0.15 - i * 0.55) / 0.4);
            return (
              <div key={i} style={{fontFamily: SERIF, fontStyle: 'italic', fontWeight: 500, fontSize: v ? 52 : 60, lineHeight: 1.16, color: C.ink, opacity: p, transform: `translateY(${(1 - p) * 12}px)`}}>
                {l}
              </div>
            );
          })}
          <div style={{width: 110, height: 2, background: C.gold, margin: '22px auto 16px'}} />
          <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 26, letterSpacing: '0.34em', color: C.goldHi}}>{c.sub}</div>
        </div>
      </AbsoluteFill>
    );
  }

  if (c.kind === 'years')
    return (
      <AbsoluteFill style={{alignItems: 'center', top: v ? '24%' : '20%', height: v ? '24%' : '30%', justifyContent: 'center', opacity: a}}>
        <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 30, letterSpacing: '0.5em', color: C.gold, textShadow: shadow}}>{c.text}</div>
        <div style={{fontFamily: SERIF, fontWeight: 600, fontSize: 210, lineHeight: 1, color: C.goldHi, textShadow: shadow, fontVariantNumeric: 'tabular-nums'}}>{wheelYears(t)}</div>
      </AbsoluteFill>
    );

  if (c.kind === 'chapter') {
    const flame = outCubic((lt - 0.55) / 0.3);
    return (
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: `rgba(2,3,6,${0.74 * a})`}}>
        <div style={{opacity: a, transform: `scale(${0.9 + 0.1 * inn})`, textAlign: 'center'}}>
          <Menorah lit={flame > 0.05 ? c.n! : c.n! - 1} pulse={1 - flame * 0.4} size={420} />
          <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 30, letterSpacing: '0.5em', color: C.gold, marginTop: 30}}>{`LÁMPARA ${c.n} DE 7`}</div>
          <div style={{fontFamily: SERIF, fontWeight: 600, fontSize: 104, color: C.ink, marginTop: 6}}>{c.text}</div>
        </div>
      </AbsoluteFill>
    );
  }

  if (c.kind === 'ask')
    return (
      <AbsoluteFill style={{alignItems: 'center', top: v ? '22%' : '16%', height: v ? '30%' : '50%', justifyContent: 'center', opacity: out}}>
        {c.text.split('\n').map((l, i) => {
          const p = outCubic((lt - i * 0.9) / 0.35);
          return (
            <div key={i} style={{fontFamily: SERIF, fontWeight: 600, fontSize: v ? 104 : 150, lineHeight: 1.02, color: i === 0 ? C.goldHi : C.ink, opacity: p, transform: `scale(${0.85 + 0.15 * p})`, textShadow: shadow}}>
              {l}
            </div>
          );
        })}
      </AbsoluteFill>
    );

  // 'end': tarjeta final de suscripción
  const p2 = outCubic((lt - 0.5) / 0.5);
  const p3 = outCubic((lt - 1.1) / 0.5);
  const beat = 1 + 0.04 * Math.sin(lt * 5);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: `rgba(2,3,6,${0.5 * inn})`}}>
      <div style={{opacity: inn, transform: `scale(${0.9 + 0.1 * inn})`}}>
        <Menorah lit={7} pulse={0.35 + 0.25 * Math.sin(lt * 3)} size={460} />
      </div>
      <div style={{fontFamily: SERIF, fontWeight: 600, fontSize: 124, color: C.ink, marginTop: 34, opacity: p2, textShadow: shadow}}>Bases Bíblicas</div>
      <div style={{fontFamily: SANS, fontWeight: 500, fontSize: 28, letterSpacing: '0.42em', color: C.gold, marginTop: 4, opacity: p2}}>A LA LUZ DE LA PALABRA</div>
      <div style={{marginTop: 40, opacity: p3, transform: `scale(${beat * (0.8 + 0.2 * p3)})`, fontFamily: SANS, fontWeight: 500, fontSize: 40, letterSpacing: '0.26em', color: '#1a1206', background: `linear-gradient(180deg, ${C.goldHi}, ${C.gold})`, padding: '20px 54px', borderRadius: 60, boxShadow: '0 0 60px rgba(241,217,160,.5)'}}>
        SUSCRÍBETE
      </div>
    </AbsoluteFill>
  );
};

export const Cards: React.FC<{t: number; v?: boolean}> = ({t, v}) => (
  <AbsoluteFill>
    {CARDS.filter((c) => t >= c.t && t < c.t + c.d && !(v && (c.kind === 'chapter' || c.kind === 'boxes'))).map((c, i) => (
      <One key={`${c.t}-${i}`} c={c} t={t} v={v} />
    ))}
  </AbsoluteFill>
);

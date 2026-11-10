// Vuelca los tiempos que necesita la música (golpes, capítulos, cambios de set). npx tsx scripts/cues.ts
import {writeFileSync} from 'node:fs';
import {A} from '../src/sets/Hall';
import {K} from '../src/sets/Outdoor';
import {W} from '../src/sets/Wheel';
import {SHOTS} from '../src/shots';
import {B, BLOCKS, DUR, at} from '../src/tl';
import {CARDS} from '../src/ui/cards';
import {REVEAL} from '../src/ui/Hud';

const sets: number[] = [];
SHOTS.forEach((s, i) => {
  if (i > 0 && s.set !== SHOTS[i - 1].set) sets.push(+s.t.toFixed(3));
});
const T = (b: number, p: string, n = 0) => +at(b, p, n).toFixed(3);
writeFileSync(
  new URL('../../cues.json', import.meta.url),
  JSON.stringify({
    DUR, B: BLOCKS.map((b) => b.start), A, K, W, REVEAL, sets,
    cuts: SHOTS.map((s) => +s.t.toFixed(3)),
    keys: CARDS.filter((c) => c.kind === 'key').map((c) => [+c.t.toFixed(3), c.size ?? 130, c.color ?? 'gold']),
    strikes: CARDS.filter((c) => c.kind === 'strike').map((c) => +c.t.toFixed(3)),
    quotes: CARDS.filter((c) => c.kind === 'quote').map((c) => +c.t.toFixed(3)),
    X: {
      flash1: T(0, 'algo se rompió'), flash2: T(0, 'pero que lo cambia todo'), stay: T(0, 'Quédate hasta el final'),
      ark: T(1, 'Allí estaba el arca'), veil1: T(1, 'Pero entre ese lugar'), gen: T(2, 'En Génesis tres'), sword: T(2, 'una espada encendida'), veil2: T(2, 'El velo repetía'),
      blood: T(3, 'y con sangre'), goat: T(3, 'Afuera, sobre la cabeza'), out: T(3, 'Y cuando el sacerdote salía'),
      spirit: T(4, 'Y el Espíritu Santo'), better: T(4, 'De Alguien mejor'),
      jer: T(5, 'Tiempo después'), instant: T(5, 'En ese mismo instante'),
      isa: T(6, 'Isaías lo anunció'), peter: T(6, 'Y Pedro lo resume'), own: T(6, 'Por eso no entró'), heb: T(6, 'Y Hebreos dice'), tore: T(6, 'El velo se rasgó'),
      throne: T(7, 'Un trono'), place: T(7, 'Ya no tienes que ir'), via: T(7, 'Por medio de Jesucristo'), one: T(7, 'Porque hay un solo mediador'),
      blood8: T(8, 'Por su sangre'), so: T(8, 'Así que no te quedes'), ask: T(8, 'Y dime'), sub: T(8, 'Y suscríbete'),
    },
  }),
);
console.log('cues.json listo');

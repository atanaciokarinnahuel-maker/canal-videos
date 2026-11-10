import {B, DUR, at} from '../tl';
import {W as WH} from '../sets/Wheel';

export type Card = {
  t: number;
  d: number;
  kind: 'key' | 'verse' | 'label' | 'quote' | 'strike' | 'chapter' | 'years' | 'boxes' | 'ask' | 'end';
  text: string;
  sub?: string;
  color?: 'gold' | 'crimson' | 'ink';
  size?: number;
  n?: number;
};

const key = (t: number, text: string, o: Partial<Card> = {}): Card => ({t, d: 1.6, kind: 'key', text, ...o});
const verse = (t: number, text: string, d = 3.6): Card => ({t, d, kind: 'verse', text});
const label = (t: number, text: string, d = 2.2): Card => ({t, d, kind: 'label', text});
const strike = (t: number, text: string, d = 1.9): Card => ({t, d, kind: 'strike', text});
const quote = (t: number, until: number, text: string, sub: string): Card => ({t, d: until - t - 0.1, kind: 'quote', text, sub});
const chapter = (n: number, text: string): Card => ({t: B(n) - 0.85, d: 1.5, kind: 'chapter', text, n});
const R = {color: 'crimson'} as const;
const I = {color: 'ink'} as const;

/** Todo lo que aparece escrito en pantalla (además de los subtítulos), anclado a la voz. */
export const CARDS: Card[] = ([
  // GANCHO
  {t: at(0, 'un detalle de tres'), d: 2.5, kind: 'boxes', text: '3 PALABRAS'},
  key(at(0, 'lo cambia todo'), 'LO CAMBIA TODO', {d: 1.3, size: 130}),
  key(at(0, 'la séptima lámpara'), 'LA 7.ª LÁMPARA', {d: 1.7, size: 110}),
  key(at(0, 'qué hay hoy'), '¿QUÉ HAY DEL OTRO LADO?', {d: 2.6, size: 96}),
  // 1
  chapter(1, 'El velo'),
  key(at(1, 'tres espacios'), '3 ESPACIOS', {size: 110, d: 1.4}),
  label(at(1, 'Afuera, el atrio') + 0.3, 'EL ATRIO'),
  label(at(1, 'Adentro, el Lugar Santo') + 0.3, 'EL LUGAR SANTO'),
  key(at(1, 'siete lámparas'), '7 LÁMPARAS', {size: 110, d: 1.3}),
  label(at(1, 'el Lugar Santísimo'), 'EL LUGAR SANTÍSIMO', 2.4),
  key(at(1, 'el arca del pacto'), 'EL ARCA DEL PACTO', {size: 100}),
  verse(at(1, 'Allí estaba el arca'), 'ÉXODO 26:33-34', 3),
  key(at(1, 'me encontraré contigo'), '«Me encontraré contigo»', {size: 100, ...I, d: 2}),
  verse(at(1, 'Allí, dijo Dios'), 'ÉXODO 30:6', 3.4),
  key(at(1, 'el velo'), 'EL VELO', {size: 190, d: 1.4}),
  verse(at(1, 'Azul'), 'ÉXODO 26:31', 3.5),
  key(at(1, 'como un muro'), 'UN MURO', {size: 170, d: 1.5}),
  // 2
  chapter(2, 'Los querubines'),
  key(at(2, 'En Génesis tres'), 'GÉNESIS 3', {size: 170, d: 1.4}),
  verse(at(2, 'Cuando el hombre pecó'), 'GÉNESIS 3:24', 6),
  key(at(2, 'una espada encendida'), 'UNA ESPADA ENCENDIDA', {size: 92}),
  key(at(2, 'hasta aquí llegas'), 'HASTA AQUÍ LLEGAS', {size: 124, ...R, d: 1.8}),
  verse(at(2, 'Isaías lo explica'), 'ISAÍAS 59:2', 5),
  key(at(2, 'separación'), 'SEPARACIÓN', {size: 150}),
  strike(at(2, 'El problema nunca fue') + 0.5, 'LA CORTINA'),
  key(at(2, 'éramos nosotros'), 'NOSOTROS', {size: 180, ...R, d: 1.8}),
  // 3
  chapter(3, 'Un hombre, un día, con sangre'),
  key(at(3, 'Uno solo'), '1 HOMBRE', {size: 150, d: 1.3}),
  key(at(3, 'un solo día'), '1 DÍA AL AÑO', {size: 130, d: 1.5}),
  verse(at(3, 'el Día de la Expiación'), 'LEVÍTICO 16', 3),
  verse(at(3, 'Dios le advirtió'), 'LEVÍTICO 16:2', 4.5),
  key(at(3, 'para que no mueras'), '«…PARA QUE NO MUERAS»', {size: 100, ...R, d: 1.7}),
  label(at(3, 'Ese día se lavaba') + 0.3, 'SE LAVABA', 1.3),
  label(at(3, 'se vestía de lino') + 0.2, 'DE LINO', 1.3),
  label(at(3, 'envuelto en una nube') + 0.3, 'INCIENSO', 1.6),
  key(at(3, 'y con sangre') + 0.2, 'CON SANGRE', {size: 150, ...R, d: 1.2}),
  key(at(3, 'Nunca sin sangre'), 'NUNCA SIN SANGRE', {size: 124, ...R, d: 1.8}),
  verse(at(3, 'Nunca sin sangre'), 'HEBREOS 9:7', 2.4),
  verse(at(3, 'Afuera, sobre la cabeza'), 'LEVÍTICO 16:21-22', 6),
  key(at(3, 'Un sustituto'), 'UN SUSTITUTO', {size: 140, d: 2}),
  key(at(3, 'otra vez'), 'CERRADO. OTRA VEZ.', {size: 110, ...I, d: 1.7}),
  // 4
  chapter(4, 'El problema'),
  key(at(4, 'Pero espera') + 0.5, 'PERO ESPERA.', {size: 180, d: 1.1}),
  {t: WH.rep, d: at(4, 'Hebreos responde') - WH.rep, kind: 'years', text: 'AÑO'},
  verse(at(4, 'Hebreos responde'), 'HEBREOS 10:4', 6),
  key(at(4, 'no puede quitar'), 'NO PUEDE QUITAR EL PECADO', {size: 92, ...R, d: 2.2}),
  {t: WH.each, d: WH.still - WH.each, kind: 'years', text: 'AÑO'},
  key(at(4, 'el pecado sigue ahí'), 'SIGUE AHÍ', {size: 150, ...R, d: 1.4}),
  verse(at(4, 'Y el Espíritu Santo'), 'HEBREOS 9:8', 6),
  key(at(4, 'todavía no'), 'TODAVÍA NO', {size: 150, d: 1.8}),
  key(at(4, 'una sombra'), 'UNA SOMBRA', {size: 150, ...I, d: 1.5}),
  verse(at(4, 'Todo era una sombra'), 'HEBREOS 10:1', 3),
  key(at(4, 'De Alguien mejor'), 'ALGUIEN MEJOR', {size: 160, d: 1.6}),
  // 5
  chapter(5, 'De arriba abajo'),
  key(at(5, 'el Cordero de Dios'), 'EL CORDERO DE DIOS', {size: 110, d: 2}),
  verse(at(5, 'he aquí el Cordero'), 'JUAN 1:29', 4),
  label(at(5, 'Jerusalén'), 'JERUSALÉN', 1.6),
  verse(at(5, 'Desde el mediodía'), 'MATEO 27:45', 3.5),
  key(at(5, 'tinieblas'), 'TINIEBLAS', {size: 170, ...I, d: 1.7}),
  key(at(5, 'las tres de la tarde'), '15:00 · HORA NOVENA', {size: 100, d: 1.8}),
  verse(at(5, 'Juan registra'), 'JUAN 19:30', 4),
  key(at(5, 'consumado es'), 'CONSUMADO ES', {size: 180, d: 2}),
  verse(at(5, 'el velo se rasga'), 'MATEO 27:51', 6),
  key(at(5, 'se rasga en dos') + 0.2, 'SE RASGÓ EN DOS', {size: 124, d: 1.5}),
  key(at(5, 'de arriba abajo'), 'DE ARRIBA\nABAJO', {size: 170, d: 2.4}),
  key(at(5, 'desde abajo'), '¿DESDE ABAJO?', {size: 120, ...I, d: 1.4}),
  key(at(5, 'empezó arriba'), 'ARRIBA', {size: 200, d: 1.4}),
  strike(at(5, 'Nadie escaló'), 'ESCALAR HASTA DIOS', 1.7),
  strike(at(5, 'Nadie pagó'), 'PAGAR LA ENTRADA', 1.7),
  key(at(5, 'Lo rasgó Dios'), 'LO RASGÓ DIOS', {size: 180, d: 1.9}),
  key(at(5, 'fue Dios bajando') + 0.3, 'DIOS BAJÓ', {size: 170, d: 2}),
  // 6
  chapter(6, 'El Cordero que tomó tu lugar'),
  key(at(6, 'el sacrificio verdadero'), 'EL SACRIFICIO VERDADERO', {size: 92, d: 1.9}),
  key(at(6, 'el Cordero perfecto'), 'EL CORDERO PERFECTO', {size: 104, d: 1.7}),
  verse(at(6, 'sin mancha'), '1 PEDRO 1:19', 3),
  key(at(6, 'Era el tuyo'), 'ERA EL TUYO', {size: 160, ...R, d: 1.1}),
  key(at(6, 'Era el mío'), 'ERA EL MÍO', {size: 160, ...R, d: 1.2}),
  quote(at(6, 'herido fue'), at(6, 'Y Pedro lo resume'), '«Herido fue por nuestras rebeliones…\nel castigo de nuestra paz fue sobre él»', 'ISAÍAS 53:5'),
  quote(at(6, 'Cristo padeció'), at(6, 'Lo oíste'), '«Cristo padeció una sola vez por los pecados,\nel justo por los injustos,\npara llevarnos a Dios»', '1 PEDRO 3:18'),
  key(at(6, 'Para llevarnos a Dios', 1), 'PARA LLEVARNOS A DIOS', {size: 108, d: 2}),
  strike(at(6, 'con sangre ajena'), 'SANGRE AJENA', 1.6),
  key(at(6, 'su propia sangre'), 'SU PROPIA SANGRE', {size: 120, ...R, d: 1.6}),
  verse(at(6, 'Por eso no entró'), 'HEBREOS 9:12', 4.5),
  strike(at(6, 'No cada año'), 'CADA AÑO', 1.3),
  key(at(6, 'una vez para siempre'), 'UNA VEZ PARA SIEMPRE', {size: 104, d: 2}),
  verse(at(6, 'Cristo ofreció'), 'HEBREOS 10:12', 4),
  key(at(6, 'y se sentó'), '…Y SE SENTÓ', {size: 170, d: 1.7}),
  verse(at(6, 'Y Hebreos dice'), 'HEBREOS 10:20', 7),
  key(at(6, 'el camino nuevo'), 'EL CAMINO NUEVO', {size: 124, d: 1.6}),
  key(at(6, 'de su carne'), '«…ESTO ES, DE SU CARNE»', {size: 88, ...I, d: 1.7}),
  key(at(6, 'por ti'), 'POR TI', {size: 230, d: 1.8}),
  // 7
  chapter(7, 'El otro lado'),
  strike(at(7, 'un lugar prohibido'), 'LUGAR PROHIBIDO', 1.7),
  key(at(7, 'Un trono'), 'UN TRONO', {size: 190, d: 1.1}),
  key(at(7, 'Un trono de gracia') + 0.35, 'EL TRONO DE LA GRACIA', {size: 116, d: 2.3}),
  quote(at(7, 'acerquémonos'), at(7, 'Entiendes lo que'), '«Acerquémonos, pues, confiadamente\nal trono de la gracia,\npara alcanzar misericordia»', 'HEBREOS 4:16'),
  key(at(7, 'Entiendes lo que'), '¿ENTIENDES?', {size: 150, ...I, d: 1.5}),
  strike(at(7, 'un lugar especial'), 'UN LUGAR ESPECIAL', 1.8),
  verse(at(7, 'Ya no tienes que ir'), 'JUAN 4:21-24', 3.5),
  strike(at(7, 'alguien que entre'), 'ALGUIEN QUE ENTRE POR TI', 1.9),
  key(at(7, 'Tú mismo'), 'TÚ MISMO', {size: 190, d: 1.4}),
  key(at(7, 'Hoy', 1), 'HOY', {size: 230, d: 0.8}),
  key(at(7, 'Donde estés'), 'DONDE ESTÉS', {size: 150, d: 1.1}),
  key(at(7, 'Por medio de Jesucristo'), 'POR MEDIO DE JESUCRISTO', {size: 92, d: 1.6}),
  key(at(7, 'tu Redentor'), 'TU REDENTOR', {size: 160, d: 1.3}),
  key(at(7, 'tomó tu lugar'), 'TOMÓ TU LUGAR', {size: 140, ...R, d: 1.6}),
  label(at(7, 'Tus hermanos') + 0.4, 'ORAN CONTIGO', 1.8),
  strike(at(7, 'hacer de puente'), 'OTRO PUENTE', 1.5),
  key(at(7, 'un solo mediador'), 'UN SOLO MEDIADOR', {size: 124, d: 2.2}),
  verse(at(7, 'Porque hay un solo'), '1 TIMOTEO 2:5', 4.5),
  verse(at(7, 'Y Él vive'), 'HEBREOS 7:25', 4),
  key(at(7, 'para interceder'), 'INTERCEDE POR TI', {size: 124, d: 2}),
  // CIERRE
  key(at(8, 'hay que entrar'), 'HAY QUE ENTRAR', {size: 150, d: 1.6}),
  strike(at(8, 'No por tus obras'), 'TUS OBRAS', 1.4),
  strike(at(8, 'No por tus méritos'), 'TUS MÉRITOS', 1.4),
  key(at(8, 'Por su sangre'), 'POR SU SANGRE', {size: 170, ...R, d: 1.7}),
  quote(at(8, 'yo soy el camino'), at(8, 'Así que no te quedes'), '«Yo soy el camino…\nnadie viene al Padre, sino por mí»', 'JUAN 14:6'),
  key(at(8, 'que ya no existe'), 'YA NO EXISTE', {size: 140, ...I, d: 1.4}),
  key(at(8, 'Cree en Él'), 'CREE', {size: 230, d: 0.9}),
  key(at(8, 'Acércate'), 'ACÉRCATE', {size: 210, d: 0.9}),
  key(at(8, 'Hoy'), 'HOY', {size: 250, d: 1.1}),
  {t: at(8, 'le hablas a Dios'), d: at(8, 'Te leo en los comentarios') - at(8, 'le hablas a Dios') - 0.1, kind: 'ask', text: '¿CON CONFIANZA…\nO CON MIEDO?'},
  key(at(8, 'Te leo en los comentarios'), 'TE LEO EN LOS COMENTARIOS', {size: 84, d: 2}),
  {t: at(8, 'Y suscríbete'), d: DUR - at(8, 'Y suscríbete'), kind: 'end', text: 'BASES BÍBLICAS'},
] as Card[]).sort((a, b) => a.t - b.t);

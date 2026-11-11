import {B, BLOCKS, at} from './tl';

export type ShortDef = {id: string; n: number; t0: number; t1: number; hook: string};
const TAIL = 1.9; // cola con la llamada a seguir
export const SHORT_TAIL = TAIL;
const blk = (n: number) => [B(n) - 0.15, BLOCKS[n].end + 0.35] as const;

/** Los 8 Shorts: cada uno es un tramo del largo, con la misma voz. */
export const SHORTS: ShortDef[] = [
  {id: 'el-velo', n: 1, t0: blk(1)[0], t1: blk(1)[1], hook: 'La casa de Dios tenía\nuna cortina que era un muro'},
  {id: 'los-querubines', n: 2, t0: blk(2)[0], t1: blk(2)[1], hook: '¿Por qué el velo\ntenía querubines?'},
  {id: 'un-hombre-un-dia', n: 3, t0: blk(3)[0], t1: blk(3)[1], hook: 'Solo un hombre podía cruzar\n(y un solo día al año)'},
  {id: 'el-problema', n: 4, t0: blk(4)[0], t1: blk(4)[1], hook: 'El sacrificio que había\nque repetir cada año'},
  {id: 'de-arriba-abajo', n: 5, t0: at(5, 'Cerca de las tres') - 0.25, t1: blk(5)[1], hook: '¿Quién rasgó\nel velo del templo?'},
  {id: 'el-cordero', n: 6, t0: blk(6)[0], t1: at(6, 'Por eso no entró') - 0.2, hook: 'El Cordero que\ntomó tu lugar'},
  {id: 'el-otro-lado', n: 7, t0: blk(7)[0], t1: blk(7)[1], hook: '¿Qué hay hoy\ndel otro lado del velo?'},
  {id: 'hay-que-entrar', n: 8, t0: blk(8)[0], t1: blk(8)[1] + 4.6, hook: 'El velo está abierto…\n¿y ahora?'},
];

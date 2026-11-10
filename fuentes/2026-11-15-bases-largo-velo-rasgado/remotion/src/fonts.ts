import {continueRender, delayRender, staticFile} from 'remotion';

const FACES: [string, string, FontFaceDescriptors][] = [
  ['Cormorant Garamond', 'fonts/cormorant-garamond-latin-500-normal.woff2', {weight: '500', style: 'normal'}],
  ['Cormorant Garamond', 'fonts/cormorant-garamond-latin-600-normal.woff2', {weight: '600', style: 'normal'}],
  ['Cormorant Garamond', 'fonts/cormorant-garamond-latin-500-italic.woff2', {weight: '500', style: 'italic'}],
  ['Cormorant Garamond', 'fonts/cormorant-garamond-latin-500-italic.woff2', {weight: '600', style: 'italic'}],
  ['Inter', 'fonts/inter-latin-500-normal.woff2', {weight: '500', style: 'normal'}],
];

let started = false;
export const loadFonts = () => {
  if (started || typeof document === 'undefined') return;
  started = true;
  const handle = delayRender('fuentes');
  Promise.all(
    FACES.map(([family, file, desc]) => new FontFace(family, `url(${staticFile(file)}) format('woff2')`, desc).load().then((f) => document.fonts.add(f))),
  ).then(() => continueRender(handle));
};

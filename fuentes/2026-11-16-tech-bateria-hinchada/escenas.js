/* ===================== piezas batería ===================== */
const OR='#ffb627';
const mixC=(a,b,t)=>{const A=hex(a),B=hex(b);return '#'+A.map((v,i)=>Math.round(lerp(v,B[i],clamp(t))).toString(16).padStart(2,'0')).join('')};
function flame(x,y,s,L,op=1){const f=1+Math.sin(L*14)*.08,g=1+Math.sin(L*11+1)*.1;return `<g transform="translate(${x},${y}) scale(${s*f},${s*g})" opacity="${op}"><path d="M0 -150 C60 -80 110 -40 90 30 C75 90 30 110 0 110 C-30 110 -80 90 -90 30 C-100 -30 -50 -50 -30 -110 C-15 -80 -5 -110 0 -150Z" fill="#ff6a3d" stroke="${NV}" stroke-width="9"/><path d="M0 -60 C35 -10 60 10 50 55 C42 90 18 100 0 100 C-18 100 -48 90 -52 55 C-56 20 -20 0 0 -60Z" fill="#ffb627"/><path d="M0 10 C18 40 28 55 20 80 C14 96 -14 96 -20 80 C-28 55 -14 40 0 10Z" fill="#fff3b0"/></g>`}
function warn(x,y,s,L,op=1){const p=1+Math.sin(L*8)*.06;return `<g transform="translate(${x},${y}) scale(${s*p})" opacity="${op}"><path d="M0 -110 L105 80 L-105 80Z" fill="${YL}" stroke="${NV}" stroke-width="12" stroke-linejoin="round"/>${TX(0,52,'!',130,NV,YL,0)}</g>`}
function batt(x,y,s,o={}){const {sw=0,col='#5eead4',L=0,rot=0,shake=0,bolt=1}=o;const w=300,h=170,sh=shake?Math.sin(L*60)*shake:0,hh=h*(1+sw*.55),ww=w*(1+sw*.1),c=mixC(col,OR,sw);
 let wr='';if(sw>.2)for(let i=0;i<3;i++)wr+=`<path d="M${-ww/2+50} ${-hh/2+40+i*hh*.22} Q0 ${-hh/2+20+i*hh*.22+sw*14} ${ww/2-50} ${-hh/2+40+i*hh*.22}" stroke="${NV}" stroke-opacity=".28" stroke-width="7" fill="none"/>`;
 return `<g transform="translate(${x+sh},${y}) rotate(${rot}) scale(${s})"><ellipse cy="${hh/2+30}" rx="${ww*.6}" ry="16" fill="#000" opacity=".22"/><rect x="${ww/2-6}" y="-34" width="38" height="68" rx="10" fill="#c9d2f0" stroke="${NV}" stroke-width="9"/><rect x="${-ww/2}" y="${-hh/2}" width="${ww}" height="${hh}" rx="${34+sw*34}" fill="${c}" stroke="${NV}" stroke-width="10"/><rect x="${-ww/2+24}" y="${-hh/2+16}" width="${ww-48}" height="${24+sw*8}" rx="14" fill="#fff" opacity=".3"/>${wr}${bolt?`<path d="M14 ${-hh*.3} L-36 8 L-4 8 L-18 ${hh*.3} L40 -12 L6 -12Z" fill="#fff" stroke="${NV}" stroke-width="7" stroke-linejoin="round"/>`:''}</g>`}
function gasB(x,y,w,h,L,n=10,col='#e9d5ff'){let s='';for(let i=0;i<n;i++){const px=x+(R(i+3)-.5)*w,py=y+h/2-((L*34*(.5+R(i+9))+R(i)*h)%h),r=8+R(i+20)*12;s+=`<circle cx="${(px+Math.sin(L*3+i)*8).toFixed(1)}" cy="${py.toFixed(1)}" r="${r.toFixed(1)}" fill="${col}" fill-opacity=".6" stroke="#fff" stroke-width="3"/>`}return s}
/* celular de lado: c = tapa trasera que se curva, sc = pantalla que se levanta */
function phoneSide(x,y,s,L,o={}){const {c=0,sc=0,wob=0,hot=0,gas=0,lab=0}=o,rot=wob?Math.sin(L*5)*wob:0;
 const bt=-26-sc*104,bb=26+c*104,sw=(c+sc)/2,bc=mixC('#5eead4',OR,Math.min(1,sw*1.3));
 const cov=`M-290 44 Q0 ${44+c*190} 290 44`,scr=`M-290 -44 Q0 ${-44-sc*190} 290 -44`,scl=`M-280 -52 Q0 ${-52-sc*190} 280 -52`;
 let heat='';if(hot>0)for(let i=0;i<4;i++){const px=-150+i*100;heat+=`<path d="M${px} ${-170-sc*60} q-18 -30 0 -60 q18 -30 0 -60" stroke="#ff6b6b" stroke-width="10" fill="none" stroke-linecap="round" opacity="${hot*(.5+.5*Math.sin(L*6+i))}" transform="translate(0,${-Math.sin(L*4+i)*10})"/>`}
 return `<g transform="translate(${x},${y}) scale(${s}) rotate(${rot} 0 110)">${hot>0?`<circle cy="0" r="${300*hot}" fill="url(#tGlowR)" opacity=".8"/>`:''}<ellipse cy="${150+c*70}" rx="330" ry="20" fill="#000" opacity=".22"/>
 <path d="${cov}" stroke="${NV}" stroke-width="48" fill="none" stroke-linecap="round"/><path d="${cov}" stroke="#8a93c4" stroke-width="32" fill="none" stroke-linecap="round"/>
 <path d="M-290 ${bt} L290 ${bt} L290 ${bb} L-290 ${bb}Z" fill="none"/>
 <rect x="-235" y="${bt}" width="470" height="${bb-bt}" rx="${30+sw*20}" fill="${bc}" stroke="${NV}" stroke-width="9"/><rect x="-205" y="${bt+10}" width="410" height="16" rx="8" fill="#fff" opacity=".3"/>${gas>0?gasB(0,(bt+bb)/2,420,Math.max(40,bb-bt-30),L,Math.round(4+gas*8)):''}
 <path d="${scr}" stroke="${NV}" stroke-width="48" fill="none" stroke-linecap="round"/><path d="${scr}" stroke="#2f3f8f" stroke-width="32" fill="none" stroke-linecap="round"/><path d="${scl}" stroke="#67e8f9" stroke-width="9" fill="none" stroke-linecap="round" opacity=".85"/>
 <rect x="-318" y="-44" width="36" height="88" rx="14" fill="#aab4d8" stroke="${NV}" stroke-width="8"/><rect x="282" y="-44" width="36" height="88" rx="14" fill="#aab4d8" stroke="${NV}" stroke-width="8"/>${heat}${lab?`<g transform="translate(0,${-120-sc*95})"><rect x="-120" y="-30" width="240" height="56" rx="28" fill="#fff" stroke="${NV}" stroke-width="7"/>${TX(0,12,'PANTALLA',34,NV,'#fff',0)}</g><g transform="translate(0,${135+c*95})"><rect x="-90" y="-30" width="180" height="56" rx="28" fill="#fff" stroke="${NV}" stroke-width="7"/>${TX(0,12,'TAPA',34,NV,'#fff',0)}</g>`:''}</g>`}
function gear(x,y,s,L,col='#8a93c4'){let t='';for(let i=0;i<10;i++)t+=`<rect x="-20" y="-150" width="40" height="50" rx="8" transform="rotate(${i*36})"/>`;return `<g transform="translate(${x},${y}) scale(${s}) rotate(${L*20})"><g fill="${col}" stroke="${NV}" stroke-width="8">${t}<circle r="120"/></g><circle r="50" fill="${NV}"/></g>`}
function sunI(x,y,s,L){let r='';for(let i=0;i<12;i++)r+=`<rect x="-14" y="-190" width="28" height="60" rx="12" transform="rotate(${i*30+L*30})"/>`;return `<g transform="translate(${x},${y}) scale(${s})"><circle r="150" fill="url(#gSun)" opacity=".7"/><g fill="${YL}" stroke="${NV}" stroke-width="6">${r}</g><circle r="105" fill="${YL}" stroke="${NV}" stroke-width="9"/><circle r="70" fill="#fff4b0" opacity=".7"/></g>`}
function clockI(x,y,s,L){return `<g transform="translate(${x},${y}) scale(${s})"><circle r="120" fill="#fff" stroke="${NV}" stroke-width="12"/>${[0,1,2,3].map(i=>`<rect x="-5" y="-108" width="10" height="22" rx="4" fill="${NV}" transform="rotate(${i*90})"/>`).join('')}<path d="M0 0 L0 -80" stroke="${NV}" stroke-width="12" stroke-linecap="round" transform="rotate(${L*120})"/><path d="M0 0 L0 -54" stroke="${CY}" stroke-width="12" stroke-linecap="round" transform="rotate(${L*10})"/><circle r="12" fill="${NV}"/></g>`}
function plug(x,y,s,L,o={}){const {rot=0,bad=0}=o,cc=bad?'#ff6b6b':'#fff';return `<g transform="translate(${x},${y}) rotate(${rot}) scale(${s})"><path d="M-320 0 Q-220 70 -130 0" stroke="${NV}" stroke-width="32" fill="none"/><path d="M-320 0 Q-220 70 -130 0" stroke="${bad?'#ff6b6b':'#e2e8f0'}" stroke-width="18" fill="none"/><rect x="-140" y="-54" width="160" height="108" rx="24" fill="${cc}" stroke="${NV}" stroke-width="10"/><rect x="20" y="-34" width="64" height="22" fill="#c9d2f0" stroke="${NV}" stroke-width="6"/><rect x="20" y="12" width="64" height="22" fill="#c9d2f0" stroke="${NV}" stroke-width="6"/></g>`}
function stopS(x,y,s,L){let d='';for(let i=0;i<8;i++){const a=(i*45+22.5)*Math.PI/180;d+=`${i?'L':'M'}${Math.cos(a)*170} ${Math.sin(a)*170} `}const p=1+Math.sin(L*9)*.04;return `<g transform="translate(${x},${y}) scale(${s*p})"><path d="${d}Z" fill="${RD}" stroke="#fff" stroke-width="14"/><path d="${d}Z" fill="none" stroke="${NV}" stroke-width="8" transform="scale(1.07)"/>${TX(0,52,'NO',150,'#fff',NV,10)}</g>`}
function powerI(x,y,s,on,p){const q=1+.18*Math.sin(clamp(p)*Math.PI);return `<g transform="translate(${x},${y}) scale(${s*q})"><circle r="140" fill="${on?LM:'#5a5f8a'}" stroke="${NV}" stroke-width="12"/><path d="M-60 -30 A80 80 0 1 0 60 -30" stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M0 -90 L0 -10" stroke="#fff" stroke-width="22" stroke-linecap="round"/></g>`}
function arr(x,y,dir,s,col=RD,L=0){const m=Math.sin(L*10)*10*dir;return `<g transform="translate(${x},${y+m}) scale(${s})"><path d="M0 ${-70*dir} L60 ${10*dir} L22 ${10*dir} L22 ${80*dir} L-22 ${80*dir} L-22 ${10*dir} L-60 ${10*dir}Z" fill="${col}" stroke="${NV}" stroke-width="9" stroke-linejoin="round"/></g>`}
function gauge(x,y,L,v){const w=800,h=110;return `<g transform="translate(${x},${y})"><rect x="${-w/2-8}" y="-8" width="${w+16}" height="${h+16}" rx="40" fill="#fff" stroke="${NV}" stroke-width="10"/><rect x="${-w/2}" y="0" width="${w*.2}" height="${h}" rx="30" fill="${RD}"/><rect x="${-w/2+w*.2}" y="0" width="${w*.6}" height="${h}" fill="${LM}"/><rect x="${w/2-w*.2}" y="0" width="${w*.2}" height="${h}" rx="30" fill="${RD}"/>${TX(-w/2+w*.1,72,'20',50,'#fff',NV,6)}${TX(w/2-w*.1,72,'80',50,'#fff',NV,6)}<g transform="translate(${-w/2+w*clamp(v)},0)"><path d="M0 -14 L26 -60 L-26 -60Z" fill="${YL}" stroke="${NV}" stroke-width="8"/><rect x="-6" y="-14" width="12" height="${h+28}" fill="${NV}"/></g></g>`}
/* ===================== escenas ===================== */
const tBgN=['tBg1','tBg2','tBg3'];
function buildSC(){SC=[
// 0 Si la tapa de tu celular se está despegando, o la pantalla se levanta
{a:['si',1],o:0,tr:'cut',chip:'',cam:[[0,1.1,540,1000],[3.2,1.0,540,960]],draw:(L,T0)=>{
 const c=eo(pa(L,T0,'tapa',1,.9)),sc=eo(pa(L,T0,'pantalla',1,.9));
 let s=bgT('tBg1')+hexes(L)+gridF(1330,L);
 s+=phoneSide(540,1000,1.35,L,{c,sc,gas:Math.max(c,sc),lab:1});
 s+=chispa(190,1260,.95,'sad',L);if(c>.5)s+=warn(880,740,.75*back(c),L);return s}},
// 1 no es un defecto de fábrica
{a:['no',1],o:-.05,tr:'flash',chip:'',cam:[[0,1.12,540,1000],[2.4,1.0,540,960]],draw:(L,T0)=>{
 const x=pa(L,T0,'defecto',1,.3),f=pa(L,T0,'fabrica',1,.3);let s=bgT('tBg3')+hexes(L,16,4)+gridF(1380,L);
 s+=gear(540,980,1.7,L)+xmark(540,980,1.8,x);
 if(f>0)s+=`<g transform="translate(540,1330) scale(${back(f)})"><rect x="-260" y="-54" width="520" height="108" rx="54" fill="#fff" stroke="${NV}" stroke-width="9"/>${TX(0,24,'DE FÁBRICA',56,NV,'#fff',2)}</g>`;return s}},
// 2 Es una batería hinchada, y es un riesgo de incendio
{a:['es',2],o:-.05,tr:'zoom',chip:'',cam:[[0,1.1,540,1000],[3.4,1.0,540,960]],draw:(L,T0)=>{
 const sw=eo(pa(L,T0,'hinchada',1,.9)),fi=pa(L,T0,'incendio',1,.4);
 let s=bgT('tBgBad')+rays(540,1000,22,1500,L*.25,.1,'#fff',.05)+hexes(L,14,6,'#ffb4a8');
 s+=batt(540,1060,1.2,{sw,L,shake:sw>.9?3:0});
 if(fi>0)s+=flame(540,800,1.55*eo(fi),L)+warn(200,800,.85*back(fi),L);return s}},
// 3 Por dentro... se desgasta con el tiempo, el calor y la mala carga, y suelta gas
{a:['por',1],o:-.05,tr:'wipe',chip:'',cam:[[0,1.0,540,1000],[6.4,1.08,540,1000]],draw:(L,T0)=>{
 const a=pa(L,T0,'tiempo',1,.4),b=pa(L,T0,'calor',1,.4),c=pa(L,T0,'carga',1,.4),g=pa(L,T0,'suelta',1,.6);
 let s=bgT('tBg2')+hexes(L,18,3,'#fff')+gridF(1400,L,'#fff',.25);
 s+=batt(540,1090,1.15,{L,sw:.3+.4*g,shake:g>0?4:0});
 if(g>0)s+=gasB(540,1010,420,240,L,12);
 if(a>0)s+=clockI(200,820,.8*back(a),L);if(b>0)s+=sunI(540,720,.8*back(b),L);if(c>0)s+=plug(900,830,.7*back(c),L,{bad:1,rot:-12});return s}},
// 4 Como está sellada, el gas no sale: la batería se infla, y empuja la tapa, la pantalla y la placa
{a:['como',1],o:-.05,tr:'circle',cx:540,cy:1000,chip:'',cam:[[0,1.1,540,1000],[6.2,1.0,540,960]],draw:(L,T0)=>{
 const inf=eo(pa(L,T0,'infla',1,1.3)),ei=pa(L,T0,'empuja',1,.4),lk=pa(L,T0,'sellada',1,.3);
 let s=bgT('tBg3')+hexes(L,16,8)+gridF(1380,L);
 s+=phoneSide(540,1060,1.35,L,{c:inf,sc:inf,gas:1});
 if(lk>0)s+=lock(540,700,1.2*back(lk),1);
 if(ei>0){s+=arr(540,840-inf*20,-1,.9*eo(ei),RD,L)+arr(540,1330,1,.9*eo(ei),RD,L)}return s}},
// 5 Las señales (4 tarjetas)
{a:['senales',1],o:-.05,tr:'slide',chip:'',cam:[[0,1.0,540,1000],[7.4,1.05,540,1000]],draw:(L,T0)=>{
 const d=[pa(L,T0,'despega',1,.3),pa(L,T0,'levanta',2,.3),pa(L,T0,'balancea',1,.3),pa(L,T0,'calienta',1,.3)];
 const P4=[[300,790,'TAPA SE DESPEGA',{c:1,sc:0}],[780,790,'PANTALLA SE LEVANTA',{c:0,sc:1}],[300,1110,'SE BALANCEA',{c:.8,sc:.8,wob:4}],[780,1110,'SE CALIENTA',{c:.5,sc:.5,hot:1}]];
 let s=bgT('tBg2')+hexes(L,16,2,'#fff');if(d[0]<=0)s+=warn(540,1030,1.7,L);
 P4.forEach((p,i)=>{if(d[i]<=0)return;const q=back(d[i]);s+=`<g transform="translate(${p[0]},${p[1]}) scale(${q})"><rect x="-225" y="-150" width="450" height="320" rx="40" fill="#fff" stroke="${NV}" stroke-width="10"/><rect x="-225" y="-150" width="450" height="64" rx="40" fill="${[CY,MG,YL,RD][i]}"/><rect x="-225" y="-110" width="450" height="24" fill="${[CY,MG,YL,RD][i]}"/>${TX(0,-100,'SEÑAL '+(i+1),40,'#fff',NV,6)}<g transform="translate(0,10)">${phoneSide(0,10,.42,L,Object.assign({gas:.4},p[3]))}</g><text y="150" x="0" text-anchor="middle" ${F} font-size="36" fill="${NV}">${p[2]}</text></g>`});return s}},
// 6 Lo que no debes hacer
{a:['lo',1],o:-.05,tr:'flash',chip:'',cam:[[0,1.2,540,1000],[1.6,1.0,540,960]],draw:(L,T0)=>{
 let s=bgT('tBgBad')+rays(540,1000,26,1700,L*.3,.12,'#fff',.04)+hexes(L,16,3,'#ffb4a8');s+=stopS(540,1020,1.9,L);return s}},
// 7 No la pinches para desinflarla: adentro hay un líquido inflamable
{a:['pinches',1],o:-.45,tr:'slide',chip:'',cam:[[0,1.08,540,1000],[4.0,1.0,540,960]],draw:(L,T0)=>{
 const nd=eo(pa(L,T0,'pinches',1,.7)),fl=pa(L,T0,'inflamable',1,.4);
 let s=bgT('tBgBad')+hexes(L,14,5,'#ffb4a8')+gridF(1400,L,'#ffb4a8',.3);
 s+=batt(540,1100,1.2,{sw:.8,L});
 s+=`<g transform="translate(${lerp(1000,640,nd)},${lerp(760,1040,nd)}) rotate(-40)"><rect x="0" y="-11" width="300" height="22" rx="11" fill="#e2e8f0" stroke="${NV}" stroke-width="7"/><path d="M0 -11 L-80 0 L0 11Z" fill="#fff" stroke="${NV}" stroke-width="6"/><circle cx="308" cy="0" r="26" fill="${RD}" stroke="${NV}" stroke-width="8"/></g>`;
 s+=xmark(190,780,.9,pa(L,T0,'pinches',1,.3));if(fl>0)s+=flame(540,830,1.2*eo(fl),L);return s}},
// 8 No la aplastes
{a:['aplastes',1],o:-.4,tr:'wipeup',chip:'',cam:[[0,1.1,540,1000],[2.0,1.0,540,960]],draw:(L,T0)=>{
 const p=eo(pa(L,T0,'aplastes',1,.4)),y=lerp(430,985,p);
 let s=bgT('tBg3')+hexes(L,14,9)+gridF(1400,L,'#ff6b6b',.3);
 s+=`<g transform="translate(540,1180) scale(1,${1-.5*p}) translate(-540,-1180)">${batt(540,1180,1.15,{sw:.8,L})}</g>`;
 s+=`<g transform="translate(540,${y})"><path d="M-220 -70 L220 -70 L260 60 L-260 60Z" fill="#8a93c4" stroke="${NV}" stroke-width="10"/>${TX(0,28,'PESO',60,'#fff',NV,8)}</g>`;
 s+=xmark(900,740,.9,pa(L,T0,'aplastes',1,.3));return s}},
// 9 Y no la sigas cargando
{a:['sigas',1],o:-.5,tr:'circle',cx:540,cy:1050,chip:'',cam:[[0,1.1,540,1000],[2.4,1.0,540,960]],draw:(L,T0)=>{
 const p=eo(pa(L,T0,'sigas',1,.8)),x=lerp(-60,350,p);
 let s=bgT('tBgBad')+hexes(L,14,4,'#ffb4a8')+gridF(1400,L,'#ffb4a8',.3);
 s+=batt(740,1080,1.0,{sw:.8,L,shake:p>.95?4:0})+plug(x,1080,1.0,L);
 if(p>.9)s+=`<g opacity="${Math.abs(Math.sin(L*20))}"><path d="M540 1000 L580 1040 L550 1040 L590 1100" stroke="${YL}" stroke-width="12" fill="none"/></g>`;
 s+=xmark(540,760,1.4,pa(L,T0,'cargando',1,.3));return s}},
// 10 Lo que sí debes hacer: apaga el celular, sácalo del cargador
{a:['debes',2],o:-.4,tr:'zoom',chip:'',cam:[[0,1.1,540,1000],[4.0,1.0,540,960]],draw:(L,T0)=>{
 const ap=pa(L,T0,'apaga',1,.4),sa=eo(pa(L,T0,'sacalo',1,.8));
 let s=bgT('tBgOk')+rays(540,900,22,1500,L*.25,.14,'#fff',.05)+hexes(L,14,8,'#fff');
 s+=powerI(540,760,1.0,ap<.5,ap>0&&ap<1?ap:0)+check(870,700,.9,pa(L,T0,'apaga',1,.5));
 s+=phoneSide(380,1180,.85,L,{c:.35,sc:.35});
 s+=plug(lerp(640,900,sa)+40,1180,.8,L,{rot:180});return s}},
// 11 y llévalo a un técnico
{a:['llevalo',1],o:-.1,tr:'wipe',chip:'',cam:[[0,1.08,540,1000],[3.0,1.0,540,960]],draw:(L,T0)=>{
 const p=eo(pa(L,T0,'llevalo',1,1.2)),t=pa(L,T0,'tecnico',1,.3);
 let s=bgT('tBgSun')+hexes(L,12,6,'#fff');
 s+=`<rect x="170" y="700" width="740" height="560" rx="30" fill="#fff" stroke="${NV}" stroke-width="12"/><path d="M130 700 L950 700 L900 580 L180 580Z" fill="${CY}" stroke="${NV}" stroke-width="12"/>${[0,1,2,3,4].map(i=>`<path d="M${180+i*144} 580 L${250+i*144-30} 700 L${250+i*144+40} 700 L${324+i*144-50} 580Z" fill="${i%2?'#fff':MG}" opacity=".85"/>`).join('')}`;
 s+=`<rect x="250" y="800" width="360" height="300" rx="20" fill="#cfe9ff" stroke="${NV}" stroke-width="9"/><rect x="660" y="800" width="190" height="460" rx="14" fill="${YL}" stroke="${NV}" stroke-width="9"/>`;
 if(t>0)s+=`<g transform="translate(540,470) scale(${back(t)})"><rect x="-250" y="-60" width="500" height="120" rx="30" fill="#fff" stroke="${NV}" stroke-width="10"/>${TX(0,24,'TÉCNICO',72,NV,'#fff',0)}</g>`;
 s+=phoneSide(lerp(100,430,p),lerp(1300,950,p),.38,L,{c:.6,sc:.6})+chispa(lerp(80,300,p)+60,1330,.8,'happy',L);return s}},
// 12 Una batería hinchada no se desinfla: la única solución es cambiarla
{a:['una',2],o:-.05,tr:'slide',chip:'',cam:[[0,1.08,540,1000],[4.0,1.0,540,960]],draw:(L,T0)=>{
 const ch=eo(pa(L,T0,'cambiarla',1,.8));
 let s=bgT('tBg3')+hexes(L,16,4)+gridF(1400,L);
 s+=batt(lerp(540,-300,ch),1050,1.15,{sw:1,L});
 if(ch>0)s+=batt(lerp(1400,540,ch),1050,1.15,{sw:0,L,col:LM});
 s+=bub(540,760,.9,'NO SE DESINFLA',54,'#fff',NV,640,pa(L,T0,'desinfla',1,.3));
 s+=check(880,1380,.9,pa(L,T0,'cambiarla',1,1.2));return s}},
// 13 Para prevenirlo, evita el sol y el calor
{a:['prevenirlo',1],o:-.1,tr:'circle',cx:540,cy:1000,chip:'',cam:[[0,1.1,540,1000],[3.0,1.0,540,960]],draw:(L,T0)=>{
 const a=pa(L,T0,'sol',1,.4),x=pa(L,T0,'calor',2,.3);
 let s=bgT('tBgSun')+hexes(L,12,8,'#fff');
 s+=sunI(300,800,1.0*back(Math.max(a,.001)),L)+phoneSide(540,1160,.95,L,{hot:Math.min(1,a+.2)});
 s+=xmark(780,800,1.2,x);return s}},
// 14 usa cargadores de calidad
{a:['usa',1],o:-.1,tr:'slide',chip:'',cam:[[0,1.1,540,1000],[3.0,1.0,540,960]],draw:(L,T0)=>{
 const q=pa(L,T0,'calidad',1,.4);
 let s=bgT('tBgOk')+rays(540,950,22,1500,L*.25,.14,'#fff',.05)+hexes(L,14,2,'#fff');
 s+=plug(640,1000,1.5,L)+check(840,800,1.0,pa(L,T0,'cargadores',1,.5));
 if(q>0)s+=`<g transform="translate(700,1260) scale(${back(q)})"><rect x="-230" y="-60" width="460" height="120" rx="60" fill="${YL}" stroke="${NV}" stroke-width="10"/>${TX(0,22,'★ CALIDAD',64,NV,YL,0)}</g>`;return s}},
// 15 mantén la carga entre el veinte y el ochenta por ciento
{a:['manten',1],o:-.1,tr:'wipe',chip:'Recomendación general',cam:[[0,1.1,540,1000],[3.2,1.0,540,960]],draw:(L,T0)=>{
 const v=pa(L,T0,'veinte',1,.3)<=0?.5:(pa(L,T0,'ochenta',1,.3)<=0?.2:.8);
 const vv=pa(L,T0,'veinte',1,.3)<=0?eio(P(L,0,.5))*.5:(pa(L,T0,'ochenta',1,.3)<=0?lerp(.5,.2,eio(pa(L,T0,'veinte',1,.4))):lerp(.2,.8,eio(pa(L,T0,'ochenta',1,.6))));
 let s=bgT('tBg2')+hexes(L,16,6,'#fff')+gridF(1400,L,'#fff',.25);
 s+=gauge(540,1100,L,vv)+batt(540,820,.8,{L,col:LM,sw:0});return s}},
// 16 ¿tu celular se balancea sobre la mesa?
{a:['entonces',1],o:0,tr:'circle',cx:540,cy:1050,chip:'',cam:[[0,1.1,540,1000],[4.0,1.0,540,960]],draw:(L,T0)=>{
 let s=bgT('tBgBad')+hexes(L,14,7,'#ffb4a8')+gridF(1400,L,'#ffb4a8',.3);
 s+=`<rect x="-200" y="1290" width="1480" height="40" fill="#b07a4a" stroke="${NV}" stroke-width="8"/>`;
 s+=phoneSide(540,1130,1.25,L,{c:.9,sc:.9,wob:3.5});
 [[220,860],[860,820],[540,640]].forEach((p,i)=>{s+=`<g transform="translate(${p[0]},${p[1]+Math.sin(L*3+i)*10}) rotate(${Math.sin(L*2+i)*12})">${TX(0,50,'?',150,YL,NV,12)}</g>`});return s}},
// 17 Cuéntame abajo qué modelo es
{a:['cuentame',1],o:0,tr:'zoom',chip:'',cam:[[0,1.1,540,1000],[2.6,1.0,540,960]],draw:(L,T0)=>{
 let s=bgT('tBg1')+hexes(L,18,5)+gridF(1380,L,MG,.3);
 const p=back(P(L,.1,.4));
 s+=`<g transform="translate(540,960) scale(${p})"><rect x="-400" y="-190" width="800" height="380" rx="46" fill="#fff" stroke="${NV}" stroke-width="12"/><circle cx="-310" cy="-90" r="52" fill="${CY}" stroke="${NV}" stroke-width="8"/><rect x="-230" y="-120" width="300" height="26" rx="13" fill="#b9c2e6"/><rect x="-230" y="-72" width="480" height="20" rx="10" fill="#dbe1f7"/>${TX(0,118,'¿QUÉ MODELO?',84,NV,'#fff',0)}</g>`;
 s+=chispa(190,1290,.9,'wow',L);return s}},
// 18 Sígueme para más tecnología simple
{a:['sigueme',1],o:0,tr:'circle',cx:540,cy:1000,chip:'',cam:[[0,1.12,540,1000],[2.0,1.0,540,960]],draw:(L,T0)=>{
 let s=bgT('tBgSun')+rays(540,950,24,1600,L*.3,.16,'#fff',.05)+hexes(L,16,9,'#fff');
 s+=chispa(540,1020,1.5,'happy',L)+heart(860,780+Math.sin(L*4)*10,1.1,MG,.95)+heart(210,860,.8,MG,.9);
 s+=bub(540,640,1.0,'¡SEGUIR!',80,YL,NV,520,back(P(L,.15,.4)));return s}},
];SC.forEach(sc=>{const w=A(...sc.a);sc.t0=Math.max(0,w.start+sc.o)});SC[0].t0=0;
 for(let i=1;i<SC.length;i++)if(SC[i].t0<=SC[i-1].t0+.3)console.error('ORDEN '+i+' '+SC[i].t0.toFixed(2))}
function SC_T0(i){return SC[i].t0}
/* ===================== textos cinéticos (anclas) ===================== */
let KT=[];
const KTD=[
 [['si',1],0,['no',1],-.1,300,88,'¿TAPA <span class="r">DESPEGADA</span><br>O PANTALLA<br><span class="r">LEVANTADA</span>?','slam'],
 [['no',1],0,['es',2],-.1,300,100,'NO ES <span class="g">DEFECTO</span><br>DE FÁBRICA','slam'],
 [['es',2],0,['por',1],-.1,300,92,'BATERÍA <span class="r">HINCHADA</span><br>= RIESGO DE<br><span class="o">INCENDIO</span>','pop'],
 [['por',1],0,['suelta',1],-.1,300,96,'SE <span class="o">DESGASTA</span><br>CON EL TIEMPO','pop'],
 [['suelta',1],-.05,['como',1],-.1,300,150,'SUELTA <span class="r">GAS</span>','slam'],
 [['como',1],0,['infla',1],-.1,300,96,'ESTÁ <span class="t">SELLADA</span><br>EL GAS NO SALE','pop'],
 [['infla',1],-.1,['senales',1],-.1,300,104,'SE <span class="r">INFLA</span><br>Y EMPUJA TODO','slam'],
 [['senales',1],0,['lo',1],-.1,300,110,'4 <span class="g">SEÑALES</span>','slam'],
 [['lo',1],0,['pinches',1],-.45,300,104,'LO QUE <span class="r">NO</span><br>DEBES HACER','slam'],
 [['pinches',1],-.45,['aplastes',1],-.4,300,88,'NO LA <span class="r">PINCHES</span><br>LÍQUIDO<br><span class="o">INFLAMABLE</span>','slam'],
 [['aplastes',1],-.4,['sigas',1],-.5,300,110,'NO LA <span class="r">APLASTES</span>','slam'],
 [['sigas',1],-.5,['debes',2],-.4,300,104,'NO LA SIGAS<br><span class="r">CARGANDO</span>','slam'],
 [['debes',2],-.4,['llevalo',1],-.1,300,104,'LO QUE <span class="g">SÍ</span><br>DEBES HACER','slam'],
 [['llevalo',1],-.1,['una',2],-.05,300,104,'LLÉVALO A UN<br><span class="g">TÉCNICO</span>','pop'],
 [['una',2],-.05,['prevenirlo',1],-.1,300,96,'NO SE DESINFLA:<br><span class="g">SE CAMBIA</span>','pop'],
 [['prevenirlo',1],-.1,['usa',1],-.1,300,100,'EVITA EL <span class="o">SOL</span><br>Y EL <span class="r">CALOR</span>','pop'],
 [['usa',1],-.1,['manten',1],-.1,300,100,'CARGADORES<br>DE <span class="g">CALIDAD</span>','pop'],
 [['manten',1],-.1,['entonces',1],-.1,350,100,'CARGA ENTRE<br><span class="g">20% Y 80%</span>','slam'],
 [['entonces',1],0,['cuentame',1],-.1,300,104,'¿TU CELU SE<br><span class="r">BALANCEA</span>?','slam'],
 [['cuentame',1],0,['sigueme',1],-.15,300,112,'COMENTA<br>TU <span class="g">MODELO</span>','slam'],
 [['sigueme',1],0,['simple',1],.9,300,92,'MÁS TECNOLOGÍA<br><span class="g">SIMPLE</span>','pop'],
];

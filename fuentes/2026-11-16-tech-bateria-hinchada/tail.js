/* ============ indicador: barra de carga de batería ============ */
const X0=70,X1=880;let REVEAL=0,MS=[];
function renderProg(T){const p=clamp(T/(VOICE+.2)),kx=X0+(X1-X0)*p,fin=T>VOICE+.1;let s='';
 s+=`<rect x="${X0-20}" y="116" width="${X1-X0+40}" height="68" rx="34" fill="rgba(11,16,48,.8)" stroke="#fff" stroke-width="4"/>`;
 const n=16;for(let i=0;i<n;i++){const x=X0+i*(X1-X0)/n,on=x+(X1-X0)/n<=kx+4,c=p<.5?LM:p<.8?YL:MG;s+=`<rect x="${x+4}" y="130" width="${(X1-X0)/n-8}" height="40" rx="8" fill="${on?c:'#2a3a7a'}"/>`}
 MS.forEach(([t,lab])=>{const x=X0+(X1-X0)*clamp(t/(VOICE+.2)),on=T>=t;s+=`<g transform="translate(${x},200)"><path d="M0 -26 L10 -14 L-10 -14Z" fill="${on?GOLD:'#7d86b8'}"/><rect x="-27" y="-14" width="54" height="34" rx="17" fill="${on?GOLD:'#4a4670'}" stroke="#fff" stroke-width="3"/>${TX(0,11,lab,22,'#fff',NV,4)}</g>`});
 const on=T>=REVEAL,o=eo(P(T,REVEAL,.5)),pu=1+(fin?.1*Math.sin(T*10):0);
 s+=`<g transform="translate(985,150) scale(${.27*pu})">${batt(0,0,1,{sw:on?o:0,col:'#5eead4',L:T*.5,bolt:1})}</g>`;
 if(T<REVEAL&&T>2&&T<6){const q=P(T,2,.3)*(1-P(T,5.6,.3));s+=`<g opacity="${q}" transform="translate(900,250)"><rect x="-170" y="-24" width="340" height="48" rx="24" fill="${GOLD}" stroke="#fff" stroke-width="4"/>${TX(0,12,'al final: tu celu',30,'#fff',NV,5)}</g>`}
 if(fin){const f=P(T,VOICE+.1,.4);s+=`<g transform="translate(940,252) scale(${back(f)})"><rect x="-100" y="-26" width="200" height="52" rx="26" fill="${MG}" stroke="#fff" stroke-width="4"/>${TX(0,14,'¡COMENTA!',34,'#fff',NV,5)}</g>`}
 $('prog').innerHTML=s}
/*SPLIT*/function buildFX(){const bt=[[0,540,1000,30],[SC[1].t0,540,820,40],[A('hinchada').start+.6,540,1050,50],[A('suelta').start,540,1000,36],[A('infla',1).start+.4,540,1000,36],[A('senales').start,540,900,30],[A('lo',1).start,540,1000,40],[A('debes',2).start,540,760,36],[A('llevalo').start+.6,540,1000,30],[A('cambiarla').start+.4,540,1000,36],[A('entonces').start,540,760,30],[A('cuentame').start,540,1000,40],[VOICE+.1,540,900,50],[VOICE+.1,985,150,30]];
 BURSTS=bt.map(([t,x,y,n],k)=>({t,x,y,arr:Array.from({length:n},(_,i)=>({a:R(k*100+i)*Math.PI*2,v:380+R(k*100+i+50)*700,s:7+R(k*100+i+9)*12,c:['#22d3ee','#ff4fa3','#a3e635','#fff','#ffd23f'][i%5],r:R(i+k)*6,st:i%3==0}))}));
 SHAKES=[[A('hinchada').start+.6,12],[A('lo',1).start,16],[A('pinches').start,14],[A('aplastes').start+.1,16],[A('sigas').start,10],[A('infla',1).start+.5,10],[A('cuentame').start,8]]}
/*SPLIT*/async function init(data){W=data.words;VOICE=data.voice_dur;DUR=data.dur;buildSC();REVEAL=A('entonces').start;MS=[[A('debes',1).start,'NO'],[A('debes',2).start,'SÍ'],[A('prevenirlo').start,'TIP']];buildKT();buildGroups();buildFX();await document.fonts.ready;render(0);
 return {n:W.length,groups:GROUPS.length,DUR,cuts:SC.map(s=>+s.t0.toFixed(2)),reveal:REVEAL}}
</script></body></html>
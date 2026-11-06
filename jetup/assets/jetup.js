/* JetUP and TAG Markets guide by MTG | page behaviour
   Menu, reveals, the illustrative candle chart, the who-is-who flow, the 70/30 slider,
   tick lists, copy buttons, the device-frame video player, the screenshot zoom and the two calculators.
   Everything works without it: it only adds movement and interaction. */
(function(){
"use strict";
var d=document,w=window,html=d.documentElement,reduce=w.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,c){return (c||d).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
var toastT;function toast(t){var el=$('#toast');if(!el)return;el.textContent=t;el.classList.add('on');clearTimeout(toastT);toastT=setTimeout(function(){el.classList.remove('on')},2200)}

/* ---- menu: a drawer on phones, docked on wide inner pages ---- */
(function(){
  var side=$('#side'),scrim=$('#scrim');if(!side)return;
  var docked=html.classList.contains('docked'),wide=matchMedia('(min-width:1100px)');
  function isDrawer(){return !(docked&&wide.matches)}
  function open(){if(!isDrawer()){html.classList.remove('side-off');store('jetup-side','on');return}
    side.classList.add('open');scrim.classList.add('on');html.classList.add('lock');side.setAttribute('aria-hidden','false');var f=$('.snav[aria-current="page"]',side)||$('.snav',side);if(f)f.focus({preventScroll:true})}
  function close(){side.classList.remove('open');scrim.classList.remove('on');html.classList.remove('lock');if(isDrawer())side.setAttribute('aria-hidden','true')}
  function sync(){if(isDrawer()){if(!side.classList.contains('open'))side.setAttribute('aria-hidden','true')}else{side.removeAttribute('aria-hidden');close()}}
  $$('[data-menu]').forEach(function(b){b.addEventListener('click',open)});
  $$('[data-menu-x]').forEach(function(b){b.addEventListener('click',close)});
  scrim.addEventListener('click',close);
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&side.classList.contains('open'))close()});
  var tog=$('#side-tog');if(tog)tog.addEventListener('click',function(){var off=html.classList.toggle('side-off');store('jetup-side',off?'off':'on');tog.setAttribute('aria-expanded',String(!off))});
  if(wide.addEventListener)wide.addEventListener('change',sync);sync();
})();

/* ---- reveals ---- */
if('IntersectionObserver'in w&&!reduce){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
  $$('.rv,[data-in]').forEach(function(el){io.observe(el)})}else $$('.rv,[data-in]').forEach(function(el){el.classList.add('in')});

/* ---- count up numbers when they appear ---- */
function fmt(n,dec){return Number(n).toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec})}
(function(){
  var els=$$('[data-count]');if(!els.length)return;
  function run(el){var to=parseFloat(el.getAttribute('data-count')),dec=+(el.getAttribute('data-dec')||0),pre=el.getAttribute('data-pre')||'',suf=el.getAttribute('data-suf')||'';
    if(reduce){el.textContent=pre+fmt(to,dec)+suf;return}var t0=0;function step(t){if(!t0)t0=t;var f=Math.min(1,(t-t0)/1100),e=1-Math.pow(1-f,3);el.textContent=pre+fmt(to*e,dec)+suf;if(f<1)requestAnimationFrame(step)}requestAnimationFrame(step)}
  if('IntersectionObserver'in w){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);o.unobserve(e.target)}})},{threshold:.4});els.forEach(function(el){o.observe(el)})}else els.forEach(run);
})();

/* ---- the candle chart behind the hero: an illustration, clearly labelled, never live prices ---- */
(function(){
  var cv=$('canvas.candles');if(!cv||!cv.getContext)return;
  var cx=cv.getContext('2d'),W=0,H=0,dpr=1,cs=[],run=false,last=0,acc=0,seed=7;
  function rnd(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}
  function mk(prev){var o=prev?prev.c:100,v=1.6+rnd()*1.6,c=o+(rnd()-.47)*v*2,h=Math.max(o,c)+rnd()*v,l=Math.min(o,c)-rnd()*v;return{o:o,c:c,h:h,l:l}}
  var STEP=16,N=0;
  function size(){var r=cv.getBoundingClientRect();W=r.width;H=r.height;dpr=Math.min(w.devicePixelRatio||1,2);cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);STEP=W<640?12:16;N=Math.ceil(W/STEP)+3;while(cs.length<N)cs.push(mk(cs[cs.length-1]));if(cs.length>N)cs=cs.slice(cs.length-N)}
  function draw(shift){
    cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);
    var lo=Infinity,hi=-Infinity;cs.forEach(function(k){lo=Math.min(lo,k.l);hi=Math.max(hi,k.h)});
    var pad=H*.18,sc=(H-pad*2)/Math.max(1,hi-lo);function y(v){return H-pad-(v-lo)*sc}
    var bw=Math.max(4,STEP*.56),ma=[],sum=0;
    cs.forEach(function(k,i){var x=i*STEP-shift*STEP+STEP/2,up=k.c>=k.o;
      cx.strokeStyle=up?'rgba(47,224,160,.85)':'rgba(255,95,122,.85)';cx.fillStyle=up?'rgba(47,224,160,.55)':'rgba(255,95,122,.55)';
      cx.lineWidth=1.2;cx.beginPath();cx.moveTo(x,y(k.h));cx.lineTo(x,y(k.l));cx.stroke();
      var t=y(Math.max(k.o,k.c)),b=y(Math.min(k.o,k.c));cx.fillRect(x-bw/2,t,bw,Math.max(1.5,b-t));
      sum+=k.c;if(i>=8)sum-=cs[i-8].c;if(i>=7)ma.push([x,y(sum/8)])});
    var g=cx.createLinearGradient(0,0,W,0);g.addColorStop(0,'rgba(140,108,231,.9)');g.addColorStop(1,'rgba(227,113,252,.9)');
    cx.strokeStyle=g;cx.lineWidth=2.2;cx.beginPath();ma.forEach(function(p,i){i?cx.lineTo(p[0],p[1]):cx.moveTo(p[0],p[1])});cx.stroke();
  }
  function tick(t){if(!run)return;var dt=last?Math.min(.05,(t-last)/1000):0;last=t;acc+=dt/1.4;
    var k=cs[cs.length-1];k.c+=(rnd()-.5)*.5;k.h=Math.max(k.h,k.c);k.l=Math.min(k.l,k.c);
    if(acc>=1){acc=0;cs.push(mk(cs[cs.length-1]));cs.shift()}
    draw(acc);requestAnimationFrame(tick)}
  size();draw(0);w.addEventListener('resize',function(){size();draw(0)});
  if(reduce)return;
  if('IntersectionObserver'in w)new IntersectionObserver(function(e){if(e[0].isIntersecting){if(!run){run=true;last=0;requestAnimationFrame(tick)}}else run=false}).observe(cv);
})();

/* ---- who is who: tap a step, a dot travels to it ---- */
(function(){
  var flow=$('.flow');if(!flow)return;
  var nodes=$$('.node',flow),dot=$('.dot',flow),info=$('#flow-info'),data={};
  $$('template[data-node]').forEach(function(t){data[t.getAttribute('data-node')]=t.innerHTML});
  function pick(n,quiet){nodes.forEach(function(x){x.setAttribute('aria-pressed',String(x===n))});
    if(info&&data[n.getAttribute('data-k')]){info.innerHTML=data[n.getAttribute('data-k')]}
    if(dot){var r=flow.getBoundingClientRect(),o=$('.orb',n).getBoundingClientRect();dot.style.opacity='1';dot.style.transition=reduce||quiet?'none':'left .7s cubic-bezier(.16,1,.3,1)';dot.style.left=(o.left-r.left+o.width/2)+'px'}}
  nodes.forEach(function(n){n.addEventListener('click',function(){pick(n);stopAuto()})});
  var i=0,auto=null;function stopAuto(){if(auto){clearInterval(auto);auto=null}}
  pick(nodes[0],true);
  w.addEventListener('resize',function(){var p=$('.node[aria-pressed="true"]',flow);if(p)pick(p,true)});
  if(!reduce&&'IntersectionObserver'in w){var o=new IntersectionObserver(function(e){if(e[0].isIntersecting&&!auto&&i<nodes.length-1){auto=setInterval(function(){i++;pick(nodes[i]);if(i>=nodes.length-1)stopAuto()},2600)}else if(!e[0].isIntersecting)stopAuto()},{threshold:.5});o.observe(flow)}
})();

/* ---- 70/30: drag the profit, watch it split ---- */
(function(){
  var r=$('#split-range');if(!r)return;
  var a=$('#split-amt'),y=$('#split-you'),f=$('#split-fee'),fy=$('#fill-you'),ff=$('#fill-fee');
  function upd(){var v=+r.value;a.textContent='$'+fmt(v,0);y.textContent='$'+fmt(v*.7,2);f.textContent='$'+fmt(v*.3,2);fy.style.width='70%';ff.style.width='30%'}
  r.addEventListener('input',upd);upd();
})();

/* ---- tick lists that remember (5 checks, get ready) ---- */
/* one list can be spread over several cards: every [data-ticks="name"] on the page shares one store and one ring */
(function(){
  var groups={};$$('[data-ticks]').forEach(function(box){var g=box.getAttribute('data-ticks');(groups[g]=groups[g]||[]).push.apply(groups[g],$$('.tick',box))});
  Object.keys(groups).forEach(function(g){
    var key='jetup-'+g,saved={},ticks=groups[g],ring=$('[data-ring="'+g+'"]');try{saved=JSON.parse(store(key)||'{}')||{}}catch(e){}
    function upd(){var n=0;ticks.forEach(function(t){if(t.getAttribute('aria-pressed')==='true')n++});
      if(ring){var c=$('.fg',ring),L=2*Math.PI*30;c.style.strokeDasharray=L;c.style.strokeDashoffset=L*(1-n/ticks.length);$('b',ring).textContent=n;var p=ring.parentNode.querySelector('[data-msg]');if(p)p.textContent=n===ticks.length?p.getAttribute('data-done'):p.getAttribute('data-msg')}}
    ticks.forEach(function(t){var id=t.getAttribute('data-id');if(saved[id])t.setAttribute('aria-pressed','true');
      t.addEventListener('click',function(){var on=t.getAttribute('aria-pressed')!=='true';t.setAttribute('aria-pressed',String(on));saved[id]=on;store(key,JSON.stringify(saved));upd()})});
    upd();
  });
})();

/* ---- copy buttons ---- */
$$('[data-copy]').forEach(function(b){b.addEventListener('click',function(){var t=b.getAttribute('data-copy');
  function ok(){b.classList.add('ok');toast('Copied: '+t);setTimeout(function(){b.classList.remove('ok')},1800)}
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(ok,function(){fallback(t);ok()});else{fallback(t);ok()}})});
function fallback(t){var ta=d.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';d.body.appendChild(ta);ta.select();try{d.execCommand('copy')}catch(e){}d.body.removeChild(ta)}

/* ---- the video player: laptop for 16:9, slim phone for 9:16, and it closes itself at the end ---- */
(function(){
  var dlg=$('#vm');if(!dlg)return;
  var vid=$('#vm-video'),dev=$('#vm-dev'),x=$('#vm-x'),ttl=$('#vm-title'),opener=null,native=typeof dlg.showModal==='function';
  function open(e){var b=e.currentTarget;e.preventDefault();if(dlg.open)return;opener=b;
    var src=b.getAttribute('data-video'),h=b.getAttribute('data-orient')!=='v';
    if(vid.getAttribute('src')!==src){vid.setAttribute('src',src);vid.setAttribute('poster',b.getAttribute('data-poster')||'');vid.load()}
    vid.setAttribute('aria-label',b.getAttribute('data-title')||'Video');ttl.textContent=b.getAttribute('data-title')||'';
    dev.classList.toggle('laptop',h);dev.classList.toggle('phone',!h);
    if(native)dlg.showModal();else dlg.setAttribute('open','');
    html.classList.add('vm-lock');requestAnimationFrame(function(){requestAnimationFrame(function(){dlg.classList.add('show')})});
    x.focus({preventScroll:true});var p=vid.play();if(p&&p.catch)p.catch(function(){})}
  function close(){if(!dlg.open)return;vid.pause();dlg.classList.remove('show');html.classList.remove('vm-lock');
    setTimeout(function(){if(native)dlg.close();else dlg.removeAttribute('open');if(opener&&opener.focus)opener.focus({preventScroll:true})},reduce?0:330)}
  $$('[data-video]').forEach(function(b){b.addEventListener('click',open)});
  vid.addEventListener('ended',function(){
    try{if(d.fullscreenElement&&d.exitFullscreen)d.exitFullscreen().catch(function(){});else if(vid.webkitDisplayingFullscreen&&vid.webkitExitFullscreen)vid.webkitExitFullscreen()}catch(_){}
    close();setTimeout(function(){try{vid.currentTime=0;vid.load()}catch(_){}},reduce?50:420)});
  x.addEventListener('click',close);$('.vm-bg',dlg).addEventListener('click',close);
  dlg.addEventListener('click',function(e){if(e.target===dlg)close()});
  dlg.addEventListener('cancel',function(e){e.preventDefault();close()});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&dlg.open&&!native)close()});
})();

/* ---- screenshot zoom ---- */
(function(){
  var lb=$('#lb');if(!lb)return;var img=$('img',lb),cap=$('p',lb),x=$('.vm-x',lb),op=null;
  function close(){lb.classList.remove('on');html.classList.remove('lock');if(op)op.focus({preventScroll:true})}
  $$('[data-zoom]').forEach(function(b){b.addEventListener('click',function(){op=b;img.src=b.getAttribute('data-zoom');img.alt=b.getAttribute('data-alt')||'';cap.textContent=b.getAttribute('data-alt')||'';lb.classList.add('on');html.classList.add('lock');x.focus({preventScroll:true})})});
  x.addEventListener('click',close);lb.addEventListener('click',function(e){if(e.target===lb)close()});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&lb.classList.contains('on'))close()});
})();

/* ---- shared helpers for the calculators ---- */
function num(inp,min,max){var raw=String(inp.value).trim().replace(/[\s,$%]/g,''),box=inp.closest('.inp'),err=inp.closest('.field').querySelector('.err');
  var v=raw===''?NaN:Number(raw),msg='';
  if(raw==='')msg='Please enter a number.';else if(!isFinite(v))msg='Numbers only, for example 150.';else if(v<min)msg='The lowest allowed is '+fmt(min,0)+'.';else if(v>max)msg='The highest allowed is '+fmt(max,0)+'.';
  if(box)box.classList.toggle('bad',!!msg);if(err)err.textContent=msg;return msg?null:v}
function r2(v){return Math.round((v+(v<0?-Number.EPSILON:Number.EPSILON))*100)/100}
function money(v){v=r2(v);var s=v<0?'-':'';return s+'$'+fmt(Math.abs(v),2)}

/* ---- Exposure Calculator ---- */
(function(){
  var f=$('#exp-form');if(!f)return;
  var own=$('#exp-own'),bon=$('#exp-bonus'),mul=$('#exp-mult'),mv=$('#exp-move'),mvo=$('#exp-move-out');
  function calc(){
    var o=num(own,1,1000000),b=num(bon,0,1000000),m=num(mul,1,500),p=+mv.value;
    mvo.textContent=(p>0?'+':'')+fmt(p,1)+'%';mvo.className='mono '+(p<0?'down':p>0?'up':'');
    var ok=o!==null&&b!==null&&m!==null;$$('[data-ok]',f.parentNode).forEach(function(e){e.style.opacity=ok?'1':'.35'});if(!ok)return;
    var bal=o+b,ex=bal*m,pl=ex*p/100,ofOwn=pl/o*100,eqOwn=o/ex*100,eqBal=100/m;
    $('#exp-bal').textContent=money(bal);$('#exp-ex').textContent=money(ex);
    var plE=$('#exp-pl');plE.textContent=(pl>0?'+':'')+money(pl);plE.parentNode.parentNode.classList.toggle('red',pl<0);
    $('#exp-ofown').textContent=(ofOwn>0?'+':'')+fmt(ofOwn,1)+'%';
    $('#exp-eqown').textContent=fmt(eqOwn,2)+'%';$('#exp-eqbal').textContent=fmt(eqBal,2)+'%';
    var lossShare=pl<0?Math.min(100,-ofOwn):0;$('#exp-needle').style.left=lossShare+'%';
    $('#exp-meter-t').textContent=pl<0?(-ofOwn>=100?'This move is bigger than all of your own money.':'This move costs '+fmt(-ofOwn,1)+'% of your own money.'):(pl>0?'A move your way. The same size against you costs the same amount.':'No move, no profit or loss.');
    $('#exp-how').innerHTML='<b>Balance</b> '+money(o)+' + '+money(b)+' = '+money(bal)+'<br><b>Exposure</b> '+money(bal)+' × '+fmt(m,0)+' = '+money(ex)+'<br><b>Result</b> '+money(ex)+' × '+fmt(p,1)+'% = '+money(pl)+'<br><b>Move that equals your own money</b> '+money(o)+' ÷ '+money(ex)+' = '+fmt(eqOwn,2)+'%<br><b>Move that equals the whole balance</b> 100% ÷ '+fmt(m,0)+' = '+fmt(eqBal,2)+'%';
  }
  [own,bon,mul].forEach(function(i){i.addEventListener('input',calc)});mv.addEventListener('input',calc);
  $$('[data-preset]',f).forEach(function(b){b.addEventListener('click',function(){var v=b.getAttribute('data-preset').split(',');own.value=v[0];bon.value=v[1];mul.value=v[2];$$('[data-preset]',f).forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});calc()})});
  $('#exp-reset').addEventListener('click',function(){own.value=150;bon.value=100;mul.value=24;mv.value=-1;$$('[data-preset]',f).forEach(function(x,i){x.setAttribute('aria-pressed',String(i===0))});calc()});
  f.addEventListener('submit',function(e){e.preventDefault()});calc();
})();

/* ---- Profit Split Calculator ---- */
(function(){
  var f=$('#ps-form');if(!f)return;
  var amt=$('#ps-amt'),pct=$('#ps-pct'),share=70;
  function calc(){
    var a=num(amt,1,10000000),g=num(pct,-100,1000);var ok=a!==null&&g!==null;$$('[data-ok]',f.parentNode).forEach(function(e){e.style.opacity=ok?'1':'.35'});if(!ok)return;
    // round to cents first, then take the fee as the remainder, so your share + fee always equals the result
    var gross=r2(a*g/100),you=gross>0?r2(gross*share/100):gross,fee=gross>0?r2(gross-you):0,net=gross>0?g*share/100:g;
    $('#ps-gross').textContent=(gross>0?'+':'')+money(gross);$('#ps-you').textContent=(you>0?'+':'')+money(you);$('#ps-fee').textContent=money(fee);
    $('#ps-net').textContent=(net>0?'+':'')+fmt(net,2)+'%';$('#ps-end').textContent=money(a+you);
    var youRow=$('#ps-you').parentNode.parentNode;youRow.classList.toggle('red',you<0);
    $('#ps-note').textContent=gross>0?'Your share is '+share+'% of the profit. The performance fee is '+(100-share)+'%, and it comes from profit only.':(gross<0?'A loss: no performance fee is charged, and the whole loss is yours.':'No profit and no loss: no fee.');
    $('#ps-how').innerHTML='<b>Strategy result</b> '+money(a)+' × '+fmt(g,2)+'% = '+money(gross)+'<br>'+(gross>0?'<b>Your '+share+'%</b> '+money(gross)+' × '+share+'% = '+money(you)+'<br><b>Fee '+(100-share)+'%</b> '+money(gross)+' × '+(100-share)+'% = '+money(fee)+'<br><b>Your return</b> '+fmt(g,2)+'% × '+share+'% = '+fmt(net,2)+'%':'<b>Fee</b> $0.00 (no fee on a loss)<br><b>Your result</b> '+money(you));
  }
  [amt,pct].forEach(function(i){i.addEventListener('input',calc)});
  $$('[data-preset]',f).forEach(function(b){b.addEventListener('click',function(){var v=b.getAttribute('data-preset').split(',');amt.value=v[0];pct.value=v[1];$$('[data-preset]',f).forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});calc()})});
  $('#ps-reset').addEventListener('click',function(){amt.value=50;pct.value=30.1;$$('[data-preset]',f).forEach(function(x,i){x.setAttribute('aria-pressed',String(i===0))});calc()});
  f.addEventListener('submit',function(e){e.preventDefault()});calc();
})();

})();

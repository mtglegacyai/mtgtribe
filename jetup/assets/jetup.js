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

/* ---- menu: a drawer on phones and tablets, docked on wide inner pages; the edge pill opens and closes it everywhere ---- */
(function(){
  var side=$('#side'),scrim=$('#scrim'),tog=$('#side-tog');if(!side)return;
  var docked=html.classList.contains('docked'),wide=matchMedia('(min-width:1100px)'),last=null;
  function isDrawer(){return !(docked&&wide.matches)}
  function expanded(){return isDrawer()?html.classList.contains('menu-open'):!html.classList.contains('side-off')}
  function hide(on){if(on){side.setAttribute('aria-hidden','true');side.setAttribute('inert','')}else{side.removeAttribute('aria-hidden');side.removeAttribute('inert')}}
  function label(){if(!tog)return;var e=expanded(),t=e?'Close the menu':'Open the menu';tog.setAttribute('aria-expanded',String(e));tog.setAttribute('aria-label',t);tog.setAttribute('title',t)}
  function open(){
    if(!isDrawer()){html.classList.remove('side-off');store('jetup-side','on');hide(false);label();return}
    last=d.activeElement;html.classList.add('menu-open');html.classList.add('lock');side.classList.add('open');scrim.classList.add('on');hide(false);label();
    var f=$('.snav[aria-current="page"]',side)||$('.snav',side);if(f)setTimeout(function(){try{f.focus({preventScroll:true})}catch(e){}},80)}
  function close(restore){
    if(!isDrawer()){html.classList.add('side-off');store('jetup-side','off');hide(true);label();return}
    html.classList.remove('menu-open');html.classList.remove('lock');side.classList.remove('open');scrim.classList.remove('on');hide(true);label();
    if(restore&&last&&last.focus){try{last.focus({preventScroll:true})}catch(e){}}last=null}
  function sync(){
    if(isDrawer()){if(!html.classList.contains('menu-open'))hide(true)}
    else{html.classList.remove('menu-open');html.classList.remove('lock');side.classList.remove('open');scrim.classList.remove('on');hide(html.classList.contains('side-off'))}
    label()}
  $$('[data-menu]').forEach(function(b){b.addEventListener('click',function(){open()})});
  $$('[data-menu-x]').forEach(function(b){b.addEventListener('click',function(){close(true)})});
  scrim.addEventListener('click',function(){close(true)});
  if(tog)tog.addEventListener('click',function(){if(expanded())close(true);else open()});
  d.addEventListener('keydown',function(e){if((e.key==='Escape'||e.key==='Esc')&&isDrawer()&&html.classList.contains('menu-open'))close(true)});
  $$('a',side).forEach(function(a){a.addEventListener('click',function(){if(isDrawer()&&html.classList.contains('menu-open'))close(false)})});
  if(wide.addEventListener)wide.addEventListener('change',sync);else if(wide.addListener)wide.addListener(sync);
  sync();
  requestAnimationFrame(function(){requestAnimationFrame(function(){html.classList.add('ready')})});
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

/* ---- the chart behind the hero (MTG, 9 Nov 2026: premium, and always moving forward) ----
   An illustration, clearly labelled, never live prices. A rising series draws itself from left to right: on wide
   screens it runs under the laptop, climbs behind it and carries on above it to a glowing price line at the top right.
   The newest candle keeps forming, a light sweeps forward, then a fresh series draws again. Nothing scrolls backwards,
   the scale never jumps, and it pauses when it is off screen. */
(function(){
  var cv=$('canvas.candles');if(!cv||!cv.getContext)return;
  var cx=cv.getContext('2d'),W=0,H=0,dpr=1,G={},S=null,cyc=11,seed=11,run=false,t0=0,tNow=0,BUILD=5.6,LIVE=17,FADE=1.2;
  function rnd(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}
  function cl(x){return x<0?0:x>1?1:x}
  function eio(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
  function eob(x){var c=1.7;x=cl(x);return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}
  function route(){var r=cv.getBoundingClientRect(),v=$('.hero .vcard'),L=v&&v.getBoundingClientRect();
    if(L&&L.width&&L.left-r.left>W*.4){var ly=Math.max(160,L.top-r.top);   // laptop on the right: the chart rises across the space above it
      return {wide:true,x0:W*.45,x1:W-190,y0:ly*.93,y1:ly*.15,floor:ly-4}}
    return {wide:false,x0:W*.04,x1:W*.88,y0:H*.56,y1:H*.15,floor:H*.6}}
  function along(R,x){var u=(x-R.x0)/(R.x1-R.x0);return R.y0+(R.y1-R.y0)*(.8*u+.2*u*u)}
  function build(){var R=route(),x0=R.x0,x1=R.x1,step=R.wide?Math.max(26,Math.min(40,W/42)):Math.max(15,W/22),n=Math.max(12,Math.round((x1-x0)/step));
    step=(x1-x0)/n;seed=cyc;var A=(R.y0-R.y1)*.085,p1=rnd()*6.283,p2=rnd()*6.283,cs=[],prev=null,e=null;
    for(var i=0;i<=n;i++){var x=x0+i*step,t=i/n,yv=along(R,x)+A*Math.sin(t*12.5+p1)+A*.45*Math.sin(t*29+p2)+(rnd()-.5)*A*1.25;
      if(i===n)yv=Math.min(yv,along(R,x));
      if(prev!==null){var o=prev,c=yv,mb=(R.y0-R.y1)/n*.5;if(Math.abs(c-o)<mb){c=o+(c<o||rnd()<.72?-mb:mb)*(.8+rnd()*.5)}yv=c;var r=Math.abs(c-o)+3;e=e===null?o:e+(c-e)*.34;
        cs.push({x:x-step/2,o:o,c:c,h:Math.min(o,c)-rnd()*r*.45,l:Math.max(o,c)+rnd()*r*.45,e:e,vol:.25+rnd()*.75})}prev=yv}
    G={wide:R.wide,step:step,bw:Math.max(5,step*.58),gy0:Math.max(8,R.y1-24),gy1:R.floor,vb:R.floor,vh:(R.y0-R.y1)*.09};S=cs}
  function layout(){var r=cv.getBoundingClientRect();W=r.width;H=r.height;dpr=Math.min(w.devicePixelRatio||1,2);cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);build()}
  function rr(x,y,ww,hh,r){r=Math.min(r,ww/2,hh/2);cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+ww,y,x+ww,y+hh,r);cx.arcTo(x+ww,y+hh,x,y+hh,r);cx.arcTo(x,y+hh,x,y,r);cx.arcTo(x,y,x+ww,y,r);cx.closePath()}
  function curve(pts){cx.moveTo(pts[0][0],pts[0][1]);for(var i=1;i<pts.length-1;i++){cx.quadraticCurveTo(pts[i][0],pts[i][1],(pts[i][0]+pts[i+1][0])/2,(pts[i][1]+pts[i+1][1])/2)}var l=pts[pts.length-1];cx.lineTo(l[0],l[1])}
  function draw(t){
    var N=S.length,live=Math.max(0,t-BUILD),reveal=eio(cl(t/BUILD))*N,full=Math.floor(reveal),part=reveal-full,bw=G.bw;
    var a=t>BUILD+LIVE?cl(1-(t-BUILD-LIVE)/FADE):1;
    cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);cx.globalAlpha=a;
    var cs=[],i,k,last=null;
    for(i=0;i<N&&i<=full;i++){k=S[i];var c=k.c,h=k.h,l=k.l,e=k.e;
      if(i===full&&t<BUILD){c=k.o+(k.c-k.o)*part;h=Math.min(k.o,c)-(Math.min(k.o,k.c)-k.h)*part;l=Math.max(k.o,c)+(k.l-Math.max(k.o,k.c))*part;e=(i?S[i-1].e:k.o)+(k.e-(i?S[i-1].e:k.o))*part}
      if(i===N-1&&t>=BUILD){var wv=Math.sin(live*1.9)*.6+Math.sin(live*3.7)*.4,amp=Math.abs(k.c-k.o)*.35+2;c=k.c+wv*amp;h=Math.min(h,c);l=Math.max(l,c)}
      cs.push({x:k.x,o:k.o,c:c,h:h,l:l,e:e,vol:k.vol,pop:cl((reveal-i)/1.6)});last=cs[cs.length-1]}
    if(!cs.length)return;
    var pts=cs.map(function(q){return [q.x,q.e]}),bot=G.gy1+(G.wide?90:60);
    // glow under the average line
    if(pts.length>1){var ag=cx.createLinearGradient(0,G.gy0,0,bot);ag.addColorStop(0,'rgba(155,124,255,.30)');ag.addColorStop(.6,'rgba(155,124,255,.10)');ag.addColorStop(1,'rgba(155,124,255,0)');
      var ex=pts[pts.length-1][0]+G.step*1.2;cx.beginPath();curve(pts);cx.lineTo(ex,pts[pts.length-1][1]);cx.lineTo(ex,bot);cx.lineTo(pts[0][0],bot);cx.closePath();cx.fillStyle=ag;cx.fill();
      cx.globalCompositeOperation='destination-out';var fx=cx.createLinearGradient(ex-G.step*3,0,ex,0);fx.addColorStop(0,'rgba(0,0,0,0)');fx.addColorStop(1,'rgba(0,0,0,1)');cx.fillStyle=fx;cx.fillRect(ex-G.step*3,0,G.step*3+2,H);
      var fl=cx.createLinearGradient(pts[0][0],0,pts[0][0]+G.step*4,0);fl.addColorStop(0,'rgba(0,0,0,1)');fl.addColorStop(1,'rgba(0,0,0,0)');cx.fillStyle=fl;cx.fillRect(pts[0][0]-2,0,G.step*4+2,H);cx.globalCompositeOperation='source-over'}
    // grid: a quiet trading-terminal frame
    cx.lineWidth=1;cx.setLineDash([2,7]);cx.strokeStyle='rgba(255,255,255,.06)';
    for(var g=0;g<=5;g++){var gy=G.gy0+(G.gy1-G.gy0)*g/5;cx.beginPath();cx.moveTo(S[0].x-G.step,gy);cx.lineTo(W,gy);cx.stroke()}
    cx.setLineDash([]);
    // volume along the floor
    cs.forEach(function(q){var up=q.c<=q.o,vh=G.vh*q.vol*cl(q.pop*1.4);cx.fillStyle=up?'rgba(203,251,97,.10)':'rgba(227,113,252,.08)';rr(q.x-bw/2,G.vb-vh,bw,vh,2);cx.fill()});
    // candles: soft glow, gradient body, fine wick, a little pop as each one lands
    cs.forEach(function(q){var up=q.c<=q.o,sc=.35+.65*eob(q.pop),top=Math.min(q.o,q.c),bt=Math.max(q.o,q.c),mid=(top+bt)/2,hh=Math.max(2,(bt-top)*sc);
      var ty=mid-hh/2,by=mid+hh/2,wt=mid-(mid-q.h)*sc,wb=mid+(q.l-mid)*sc;cx.globalAlpha=a*cl(q.pop*1.6);
      cx.strokeStyle=up?'rgba(203,251,97,.8)':'rgba(227,113,252,.6)';cx.lineWidth=1.5;cx.beginPath();cx.moveTo(q.x,wt);cx.lineTo(q.x,wb);cx.stroke();
      if(up){var bg=cx.createLinearGradient(0,ty,0,by);bg.addColorStop(0,'#f0ffb8');bg.addColorStop(.45,'#cbfb61');bg.addColorStop(1,'#2fe0a0');cx.fillStyle=bg;cx.shadowColor='rgba(203,251,97,.55)';cx.shadowBlur=16}
      else{var rg=cx.createLinearGradient(0,ty,0,by);rg.addColorStop(0,'rgba(240,140,255,.85)');rg.addColorStop(1,'rgba(155,124,255,.7)');cx.fillStyle=rg;cx.shadowColor='rgba(227,113,252,.35)';cx.shadowBlur=10}
      rr(q.x-bw/2,ty,bw,hh,Math.min(4,bw/3.2));cx.fill();cx.shadowBlur=0;
      cx.fillStyle='rgba(255,255,255,'+(up?.35:.18)+')';rr(q.x-bw/2+2,ty+1.5,Math.max(1.5,bw*.18),Math.max(1,hh-3),1);cx.fill()});
    cx.globalAlpha=a;
    // the average line: violet into pink into lime, with a glow
    if(pts.length>1){var lg=cx.createLinearGradient(S[0].x,0,S[N-1].x,0);lg.addColorStop(0,'rgba(155,124,255,.85)');lg.addColorStop(.5,'rgba(227,113,252,.95)');lg.addColorStop(1,'#cbfb61');
      cx.lineJoin='round';cx.lineCap='round';cx.beginPath();curve(pts);cx.strokeStyle=lg;cx.lineWidth=3;cx.shadowColor='rgba(227,113,252,.6)';cx.shadowBlur=14;cx.stroke();cx.shadowBlur=0}
    // a light that sweeps forward across the chart
    if(t>=BUILD){var sp=(live%6)/2;if(sp<1){var sx=S[0].x-200+(S[N-1].x-S[0].x+400)*eio(sp),sg=cx.createLinearGradient(sx-160,0,sx+160,0);
      sg.addColorStop(0,'rgba(255,255,255,0)');sg.addColorStop(.5,'rgba(255,255,255,.18)');sg.addColorStop(1,'rgba(255,255,255,0)');
      cx.globalCompositeOperation='source-atop';cx.fillStyle=sg;cx.fillRect(sx-160,0,320,H);cx.globalCompositeOperation='source-over'}}
    // the head: the pen while it draws, then the price line with a pulse and the illustration tag
    var hx=pts[pts.length-1][0],hy=pts[pts.length-1][1];
    if(t>=BUILD){var py=last.c;cx.setLineDash([4,6]);cx.strokeStyle='rgba(203,251,97,.6)';cx.lineWidth=1.2;cx.beginPath();cx.moveTo(last.x+bw/2+6,py);cx.lineTo(W,py);cx.stroke();cx.setLineDash([]);
      if(G.wide){cx.font='700 10px "JetBrains Mono",ui-monospace,monospace';var tw=cx.measureText('ILLUSTRATION').width+20,tx=W-tw-18;
        cx.fillStyle='#cbfb61';cx.shadowColor='rgba(203,251,97,.5)';cx.shadowBlur=12;rr(tx,py-11,tw,22,11);cx.fill();cx.shadowBlur=0;cx.fillStyle='#14110b';cx.textBaseline='middle';cx.fillText('ILLUSTRATION',tx+10,py+.5)}}
    var pr=(live%1.8)/1.8;cx.fillStyle='rgba(203,251,97,'+(.45*(1-pr)).toFixed(3)+')';cx.beginPath();cx.arc(hx,hy,6+20*eio(pr),0,6.283);cx.fill();
    cx.fillStyle='rgba(203,251,97,.28)';cx.beginPath();cx.arc(hx,hy,11,0,6.283);cx.fill();
    cx.fillStyle='#f0ffc4';cx.beginPath();cx.arc(hx,hy,5,0,6.283);cx.fill();
    cx.globalAlpha=1}
  function frame(now){if(!run)return;if(!t0)t0=now-tNow*1000;tNow=(now-t0)/1000;
    if(tNow>BUILD+LIVE+FADE){cyc=(cyc*48271)%2147483647;build();t0=now;tNow=0}
    draw(tNow);requestAnimationFrame(frame)}
  function start(){if(!run&&!reduce){run=true;t0=0;requestAnimationFrame(frame)}}
  function stop(){run=false}
  layout();draw(reduce?BUILD:0);
  w.addEventListener('resize',function(){layout();draw(reduce?BUILD:tNow)});
  w.__jetupChart={draw:function(t){tNow=t;draw(t)},stop:stop,relayout:function(){layout()},next:function(){cyc=(cyc*48271)%2147483647;build()},cycle:BUILD+LIVE+FADE};
  if(reduce)return;
  if('IntersectionObserver'in w)new IntersectionObserver(function(e){e[0].isIntersecting?start():stop()}).observe(cv);else start();
  d.addEventListener('visibilitychange',function(){d.hidden?stop():start()});
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
    $('#exp-meter-t').textContent=pl<0?(-ofOwn>=100?'This move is bigger than your deposit.':'This move costs '+fmt(-ofOwn,1)+'% of your own money.'):(pl>0?'A move your way. The same size against you costs the same amount.':'No move, no profit or loss.');
    $('#exp-how').innerHTML='<b>Balance</b> '+money(o)+' + '+money(b)+' = '+money(bal)+'<br><b>Exposure</b> '+money(bal)+' × '+fmt(m,0)+' = '+money(ex)+'<br><b>Result</b> '+money(ex)+' × '+fmt(p,1)+'% = '+money(pl)+'<br><b>Move that equals your deposit</b> '+money(o)+' ÷ '+money(ex)+' = '+fmt(eqOwn,2)+'%<br><b>Move that equals the whole balance</b> 100% ÷ '+fmt(m,0)+' = '+fmt(eqBal,2)+'%';
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
    $('#ps-note').textContent=gross>0?'Your share is '+share+'% of the profit. The performance fee is '+(100-share)+'%, and it comes from profit only.':(gross<0?'On a loss, no performance fee is charged.':'No profit and no loss: no fee.');
    $('#ps-how').innerHTML='<b>Strategy result</b> '+money(a)+' × '+fmt(g,2)+'% = '+money(gross)+'<br>'+(gross>0?'<b>Your '+share+'%</b> '+money(gross)+' × '+share+'% = '+money(you)+'<br><b>Fee '+(100-share)+'%</b> '+money(gross)+' × '+(100-share)+'% = '+money(fee)+'<br><b>Your return</b> '+fmt(g,2)+'% × '+share+'% = '+fmt(net,2)+'%':'<b>Fee</b> $0.00 (no fee on a loss)<br><b>Your result</b> '+money(you));
  }
  [amt,pct].forEach(function(i){i.addEventListener('input',calc)});
  $$('[data-preset]',f).forEach(function(b){b.addEventListener('click',function(){var v=b.getAttribute('data-preset').split(',');amt.value=v[0];pct.value=v[1];$$('[data-preset]',f).forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});calc()})});
  $('#ps-reset').addEventListener('click',function(){amt.value=50;pct.value=30.1;$$('[data-preset]',f).forEach(function(x,i){x.setAttribute('aria-pressed',String(i===0))});calc()});
  f.addEventListener('submit',function(e){e.preventDefault()});calc();
})();

})();

/* Phones never scroll sideways (MTG, 6 Nov 2026): a table that would not fit its box stacks its rows (class "stack").
   Checked on load, after the fonts arrive and whenever the box changes width. Tables that fit stay as tables. */
(function () {
  var wraps = [].slice.call(document.querySelectorAll('.tbl-wrap'));
  if (!wraps.length) return;
  var last = [], timer;
  function fit(force) {
    wraps.forEach(function (w, i) {
      var wd = w.clientWidth;
      if (!force && last[i] === wd) return;
      w.classList.remove('stack');
      if (w.scrollWidth > w.clientWidth + 1) w.classList.add('stack');
      last[i] = w.clientWidth;
    });
  }
  function soon() { clearTimeout(timer); timer = setTimeout(function () { fit(true); }, 80); }
  fit(true);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { fit(true); });
  window.addEventListener('load', function () { fit(true); });
  window.addEventListener('resize', soon);
  window.addEventListener('orientationchange', soon);
  if (window.ResizeObserver) { var ro = new ResizeObserver(soon); wraps.forEach(function (w) { ro.observe(w); }); }
})();

/* Back to the top (MTG, 6 Nov 2026): shows after a short scroll, its ring fills as you read,
   one tap glides back to the top (instant with reduced motion) and puts keyboard focus on the top bar. */
(function () {
  var b = document.getElementById('totop');
  if (!b) return;
  var root = document.documentElement, ticking = false;
  function update() {
    ticking = false;
    var y = window.scrollY || root.scrollTop, max = root.scrollHeight - window.innerHeight;
    b.classList.toggle('on', y > Math.min(600, window.innerHeight * 0.75));
    b.style.setProperty('--sp', max > 0 ? Math.min(1, y / max).toFixed(3) : 0);
  }
  function soon() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', soon, { passive: true });
  window.addEventListener('resize', soon);
  update();
  function jump(y) { root.style.scrollBehavior = 'auto'; window.scrollTo(0, y); root.style.scrollBehavior = ''; }
  b.addEventListener('click', function () {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var y = window.scrollY || root.scrollTop, near = Math.round(window.innerHeight * 1.2);
    if (reduce) jump(0);
    else {
      if (y > near * 2) jump(near);   /* long pages: skip most of the way at once, then glide the last stretch */
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    var t = document.querySelector('.top .brand');
    if (t) { try { t.focus({ preventScroll: true }); } catch (e) { t.focus(); } }
  });
})();

/* Navigation and learning helpers (MTG, 7 Nov 2026): FAQ links open their answer, the jump bar on long pages,
   "continue where you left off" (saved only on this phone), tap a word to see what it means, and search the guide. */
(function () {
  'use strict';
  var d = document, w = window, html = d.documentElement;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function del(k) { try { localStorage.removeItem(k); } catch (e) {} }
  function json(k, fb) { try { return JSON.parse(get(k) || 'null') || fb; } catch (e) { return fb; } }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function topH() { var t = $('.top'); return t ? t.getBoundingClientRect().height : 60; }
  function docTop(el) { var y = 0; for (var e = el; e; e = e.offsetParent) y += e.offsetTop; return y; }   /* ignores slide-in animations */
  function scrollToY(y) {
    y = Math.max(0, Math.round(y));
    try { w.scrollTo({ top: y, behavior: reduce ? 'instant' : 'smooth' }); } catch (e) { w.scrollTo(0, y); }
  }
  var path = location.pathname, pageName = d.body.getAttribute('data-page') || 'JetUP guide';

  /* ---- FAQ links (from search or anywhere) open their answer ---- */
  function openHash() {
    if (!location.hash) return;
    var el = null; try { el = d.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) {}
    for (var p = el; p; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
  }
  openHash();
  w.addEventListener('hashchange', openHash);
  /* arriving with an address like #part-4: once fonts and images have settled, land exactly on it
     (unless the visitor has already started scrolling) */
  var touched = false;
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) { w.addEventListener(ev, function () { touched = true; }, { passive: true, once: true }); });
  function settleHash() {
    if (touched || !location.hash) return;
    var el = null; try { el = d.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) {}
    if (!el) return;
    var j = $('#jump'), y = Math.max(0, docTop(el) - topH() - (j ? j.offsetHeight : 0) - 14);
    if (Math.abs(w.scrollY - y) > 16) { html.style.scrollBehavior = 'auto'; w.scrollTo(0, y); html.style.scrollBehavior = ''; }
  }
  if (location.hash) {
    var settled = function () { settleHash(); setTimeout(settleHash, 400); };
    if (d.readyState === 'complete') settled(); else w.addEventListener('load', settled);
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(settleHash);
  }

  del('jetup-last');   // the welcome-back card was removed (MTG, 7 Nov 2026): nothing reads this any more

  /* ---- 1. jump bar ---- */
  var jump = $('#jump');
  if (jump) (function () {
    var btn = $('.jcur', jump), list = $('#jlist'), jn = $('[data-jn]', jump), jt = $('[data-jt]', jump);
    var links = $$('a', list), chips = $$('.jc', jump);
    var items = links.map(function (a) {
      var id = a.getAttribute('href').slice(1);
      return { id: id, label: $('.jl', a).textContent, el: d.getElementById(id) };
    }).filter(function (x) { return x.el; });
    if (!items.length) return;
    html.classList.add('has-jump');
    var cur = -2, shown = false, ticking = false, tkey = jump.getAttribute('data-ticks-key');
    /* a section is "current" once its top reaches the upper third of the screen (and is never hidden under the bars) */
    function line() { return Math.max(topH() + jump.offsetHeight + 28, w.innerHeight * 0.35); }
    function update() {
      ticking = false;
      var L = line(), y = w.scrollY, i = -1;
      for (var k = 0; k < items.length; k++) if (docTop(items[k].el) - y <= L) i = k;
      var on = docTop(items[0].el) - y < w.innerHeight * 0.55;
      if (on !== shown) { shown = on; jump.classList.toggle('on', on); if (!on) close(false); }
      if (i < 0) i = 0;
      if (i !== cur) {
        cur = i;
        jn.textContent = i + 1; jt.textContent = items[i].label;
        jump.style.setProperty('--jp', ((i + 1) / items.length).toFixed(3));
        links.forEach(function (a, k) { if (k === i) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
        chips.forEach(function (a, k) { a.classList.toggle('cur', k === i); if (k === i) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      }
    }
    function soon() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    function ticks() {
      if (!tkey) return;
      var saved = json(tkey, {});
      links.concat(chips).forEach(function (a) { var t = a.getAttribute('data-tick'); if (t) a.classList.toggle('done', !!saved[t]); });
    }
    function open() { list.hidden = false; btn.setAttribute('aria-expanded', 'true'); jump.classList.add('open');
      var a = $('a[aria-current]', list) || links[0]; if (a) { try { a.focus({ preventScroll: true }); } catch (e) { a.focus(); } } }
    function close(focus) { if (list.hidden) return; list.hidden = true; btn.setAttribute('aria-expanded', 'false'); jump.classList.remove('open'); if (focus) btn.focus(); }
    function goTo(t) {
      scrollToY(docTop(t) - topH() - jump.offsetHeight - 14);
      if (!t.hasAttribute('tabindex')) t.setAttribute('tabindex', '-1');
      try { t.focus({ preventScroll: true }); } catch (e) {}
    }
    btn.addEventListener('click', function () { if (list.hidden) open(); else close(true); });
    links.concat(chips).forEach(function (a) {
      a.addEventListener('click', function (e) {
        var t = d.getElementById(a.getAttribute('href').slice(1)); if (!t) return;
        e.preventDefault(); close(false); goTo(t);
        if (history.replaceState) history.replaceState(null, '', '#' + t.id);
      });
    });
    d.addEventListener('click', function (e) { if (!list.hidden && !jump.contains(e.target)) close(false); });
    d.addEventListener('keydown', function (e) { if ((e.key === 'Escape' || e.key === 'Esc') && !list.hidden) close(true); });
    d.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('.tick')) setTimeout(ticks, 0); });
    w.addEventListener('scroll', soon, { passive: true });
    w.addEventListener('resize', soon);
    ticks(); update();
  })();

  /* ---- 4. tap a word to see what it means ---- */
  var pop = $('#glpop'), gdata = null;
  if (pop) (function () {
    try { gdata = JSON.parse($('#gl-data').textContent); } catch (e) { return; }
    var gh = $('.glh', pop), gd = $('.gld', pop), more = $('.gll', pop), x = $('.glx', pop), open = null;
    function bottomBar() { var t = $('.thumb'); return t && t.offsetHeight ? t.offsetHeight : 0; }
    function place(b) {
      var r = b.getBoundingClientRect(), vw = html.clientWidth, pw = Math.min(320, vw - 24);
      pop.style.width = pw + 'px';
      var left = Math.max(12, Math.min(r.left + r.width / 2 - pw / 2, vw - pw - 12));
      var ph = pop.offsetHeight, below = r.bottom + 12, above = r.top - ph - 12;
      var up = below + ph > w.innerHeight - bottomBar() - 8 && above > topH() + 8;
      pop.style.left = (left + w.scrollX) + 'px';
      pop.style.top = ((up ? above : below) + w.scrollY) + 'px';
      pop.style.setProperty('--ax', Math.max(18, Math.min(pw - 18, r.left + r.width / 2 - left)) + 'px');
      pop.classList.toggle('up', up);
    }
    function show(b) {
      var g = gdata[b.getAttribute('data-g')]; if (!g) return;
      if (open && open !== b) open.setAttribute('aria-expanded', 'false');
      gh.textContent = g[0]; gd.textContent = g[1]; more.setAttribute('href', g[2]); more.textContent = 'See it in the glossary';
      pop.hidden = false; place(b); pop.classList.add('on');
      b.setAttribute('aria-expanded', 'true'); open = b;
    }
    function hide(focus) {
      if (!open) return;
      pop.classList.remove('on'); pop.hidden = true; open.setAttribute('aria-expanded', 'false');
      if (focus) open.focus(); open = null;
    }
    $$('button.gl').forEach(function (b) {
      b.addEventListener('click', function (e) { e.stopPropagation(); if (open === b) hide(false); else show(b); });
    });
    x.addEventListener('click', function () { hide(true); });
    d.addEventListener('click', function (e) { if (open && !pop.contains(e.target)) hide(false); });
    d.addEventListener('keydown', function (e) { if ((e.key === 'Escape' || e.key === 'Esc') && open) hide(true); });
    w.addEventListener('resize', function () { if (open) place(open); });
  })();

  /* ---- 5. search the guide (in the menu) ---- */
  var sq = $('#sq');
  if (sq) (function () {
    var res = $('#sres'), nav = $('#side nav'), clr = $('.sclear'), idx = null, loading = null;
    function load() {
      if (idx) return Promise.resolve(idx);
      if (loading) return loading;
      loading = fetch(sq.getAttribute('data-index')).then(function (r) { return r.json(); }).then(function (j) {
        idx = j.map(function (e) { e.hl = e.h.toLowerCase(); e.pl = e.p.toLowerCase(); e.tl = e.t.toLowerCase(); return e; });
        return idx;
      }).catch(function () { loading = null; return null; });
      return loading;
    }
    function hl(s, toks) {   /* mark every match, escaping the text around it */
      var low = s.toLowerCase(), on = [];
      toks.forEach(function (t) { var i = low.indexOf(t); while (i > -1) { for (var k = i; k < i + t.length; k++) on[k] = true; i = low.indexOf(t, i + t.length); } });
      var out = '', open = false;
      for (var i = 0; i < s.length; i++) {
        if (on[i] && !open) { out += '<mark>'; open = true; } else if (!on[i] && open) { out += '</mark>'; open = false; }
        out += esc(s[i]);
      }
      return out + (open ? '</mark>' : '');
    }
    function snip(e, toks) {
      var p = -1; toks.forEach(function (t) { var i = e.tl.indexOf(t); if (i > -1 && (p < 0 || i < p)) p = i; });
      if (p < 0) p = 0;
      var a = Math.max(0, p - 50), b = Math.min(e.t.length, p + 120);
      while (a > 0 && e.t[a - 1] !== ' ') a--;
      return (a > 0 ? '… ' : '') + hl(e.t.slice(a, b), toks) + (b < e.t.length ? ' …' : '');
    }
    function run() {
      var q = sq.value.trim().toLowerCase();
      clr.hidden = !q;
      if (q.length < 2) { res.hidden = true; res.innerHTML = ''; if (nav) nav.hidden = false; return; }
      if (nav) nav.hidden = true;
      res.hidden = false;
      if (!idx) { res.innerHTML = '<p class="snone">Searching the guide</p>'; load().then(function (r) { if (r) run(); else res.innerHTML = '<p class="snone">Search is not available right now. Use the pages below.</p>'; }); return; }
      var toks = q.split(/\s+/).filter(function (t) { return t.length > 1; });
      if (!toks.length) toks = [q];
      var hits = [];
      idx.forEach(function (e) {
        var s = 0, all = true;
        toks.forEach(function (t) {
          var h = e.hl.indexOf(t) > -1, p = e.pl.indexOf(t) > -1, x = e.tl.indexOf(t) > -1;
          if (!h && !p && !x) all = false;
          s += (h ? 6 : 0) + (p ? 2 : 0) + (x ? 1 : 0);
        });
        if (!all) return;
        if (e.hl.indexOf(q) > -1) s += 8; else if (e.tl.indexOf(q) > -1) s += 3;
        hits.push([s, e]);
      });
      hits.sort(function (a, b) { return b[0] - a[0]; });
      hits = hits.slice(0, 8);
      if (!hits.length) {
        res.innerHTML = '<p class="snone">Nothing found for “' + esc(sq.value.trim()) + '”. Try another word, or ask in the tribe.</p><a class="btn btn-lime btn-sm" href="/group/">Ask in the MTG TRIBE</a>';
        return;
      }
      res.innerHTML = '<p class="scount">' + hits.length + (hits.length === 1 ? ' result' : ' results') + '</p>' + hits.map(function (x) {
        var e = x[1];
        return '<a class="sitem" href="' + esc(e.u) + '"><b>' + hl(e.h, toks) + '</b><small>' + esc(e.p) + '</small><span>' + snip(e, toks) + '</span></a>';
      }).join('');
    }
    sq.addEventListener('focus', load);
    sq.addEventListener('input', run);
    sq.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var a = $('.sitem', res); if (a) { e.preventDefault(); a.click(); } }
      else if (e.key === 'ArrowDown') { var f = $('.sitem', res); if (f) { e.preventDefault(); f.focus(); } }
      else if ((e.key === 'Escape' || e.key === 'Esc') && sq.value) { e.stopPropagation(); sq.value = ''; run(); }
    });
    clr.addEventListener('click', function () { sq.value = ''; run(); sq.focus(); });
    res.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a'); if (!a) return;
      var u = new URL(a.href, location.href);
      if (u.pathname === location.pathname && html.classList.contains('menu-open')) { var s = $('#scrim'); if (s) s.click(); }
    });
  })();
})();

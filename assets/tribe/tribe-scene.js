/* MTG TRIBE | "One tribe becomes many": a small animated community scene.
   Little people (the flat style of MTG's explainer videos) stand in a circle around a campfire,
   swaying, cheering in a wave and sending up hearts. Two members walk out and each starts a new
   circle; newcomers walk in and join. Three tribes side by side, all on the same ground: a community,
   not a ladder. Plays once when it comes into view, then stays alive. Reduced motion: one still frame.
   Markup: <canvas id="tribe-scene"> inside <figure class="scene" id="scene-wrap">, optional <button id="scene-replay">. */
(function(){
"use strict";
var cv=document.getElementById('tribe-scene');if(!cv||!cv.getContext)return;
var wrap=document.getElementById('scene-wrap')||cv.parentNode,replay=document.getElementById('scene-replay');
var cx=cv.getContext('2d'),reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var TAU=Math.PI*2,W=0,H=0,dpr=1,T=0,last=0,visible=false,running=false;

/* ---------- the people ---------- */
var SKIN=['#f1c9a5','#d9a066','#b5763f','#8d5524','#8d5524','#6b3e1f','#6b3e1f','#4a2a14'];
var SHIRT=['#6ee7b7','#93c5fd','#f8fafc','#fdba74','#ffd98e','#f9a8d4','#c4b5fd','#fca5a5','#5eead4'];
var HAIR=['#1b120c','#2a1a10','#3b2414','#120c08','#4a2c17'];
var NAVY='#1f2b47',FACE='#2a1408';
function rnd(n){var x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x)}
function look(i){return{skin:SKIN[Math.floor(rnd(i)*SKIN.length)],shirt:SHIRT[Math.floor(rnd(i+50)*SHIRT.length)],hair:HAIR[Math.floor(rnd(i+90)*HAIR.length)],style:Math.floor(rnd(i+130)*4),ph:rnd(i+170)*TAU}}

/* circle 0 = left, 1 = centre (the first tribe), 2 = right */
var people=[],K0=10,K1=8,KS=7;
var LEAVE_L={t0:1.4,dur:2.2},LEAVE_R={t0:2.2,dur:2.2};
(function build(){
  var i,k,final=[],rest=[];
  for(i=0;i<K0;i++)people.push({id:i,lk:look(i+3),home:1,a0:i*TAU/K0});
  // members 5 (left edge) and 0 (right edge) walk out to lead new tribes
  for(i=0;i<K0;i++)if(i!==5&&i!==0)rest.push(people[i]);
  rest.forEach(function(p,j){p.a1=Math.PI/K1+j*TAU/K1});
  // keep the angular order sensible: sort both lists by angle so nobody crosses the circle
  rest.sort(function(a,b){return a.a0-b.a0});
  var finals=rest.map(function(p){return p.a1}).sort(function(a,b){return a-b});
  rest.forEach(function(p,j){p.a1=finals[j]});
  var L=people[5],R=people[0];
  L.lead=0;L.walk={t0:LEAVE_L.t0,dur:LEAVE_L.dur};L.dest={c:0,a:0};
  R.lead=2;R.walk={t0:LEAVE_R.t0,dur:LEAVE_R.dur};R.dest={c:2,a:Math.PI};
  for(k=1;k<KS;k++){
    people.push({id:100+k,lk:look(100+k),from:'left',walk:{t0:3.9+(k-1)*.7,dur:1.9},dest:{c:0,a:k*TAU/KS}});
    people.push({id:200+k,lk:look(200+k),from:'right',walk:{t0:4.5+(k-1)*.7,dur:1.9},dest:{c:2,a:Math.PI+k*TAU/KS}});
  }
})();
var END=11.2,hearts=[],arcs=[],soft=[],nextHeart=0,nextArc=0,nextSoft=0;

/* ---------- layout (recomputed on resize, so any width works) ---------- */
var G={};
function layout(){
  var r=cv.getBoundingClientRect();W=r.width;H=r.height;dpr=Math.min(window.devicePixelRatio||1,2);
  cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
  G.narrow=W<560;
  if(G.narrow){
    // phones: the first tribe big in the middle, the two new tribes half visible at the edges
    G.s=Math.max(.8,Math.min(1.05,W/400));
    G.cy=H*.72;G.cx=[0,W*.5,W];G.rx=[W*.17,W*.26,W*.17];
  }else{
    G.s=Math.max(.7,Math.min(1.45,W/620));
    G.cy=H*.7;G.cx=[W*.17,W*.5,W*.83];G.rx=[W*.105,W*.14,W*.105];
  }
  G.ry=G.rx.map(function(x){return x*.34});
}
function onCircle(c,a){var sn=Math.sin(a);return{x:G.cx[c]+G.rx[c]*Math.cos(a),y:G.cy+G.ry[c]*sn,ds:.8+.2*(sn+1)/2,face:sn<.25}}
function ease(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2}
function clamp(v,a,b){return Math.max(a,Math.min(b,v))}

/* where is each person at time t */
function where(p,t){
  var o;
  if(p.home===1&&!p.walk){var e=ease(clamp((t-1.6)/2.2,0,1));o=onCircle(1,p.a0+(p.a1-p.a0)*e);o.state='circle';o.c=1;o.ang=p.a0+(p.a1-p.a0)*e;return o}
  var w=p.walk,end=onCircle(p.dest.c,p.dest.a);
  if(t>=w.t0+w.dur){end.state='circle';end.c=p.dest.c;end.ang=p.dest.a;end.arrived=t-(w.t0+w.dur);return end}
  var start;
  if(p.home===1){start=onCircle(1,p.a0)}
  else if(p.from==='left'){start={x:-30*G.s,y:G.cy+G.ry[0]*.9,ds:1}}
  else{start={x:W+30*G.s,y:G.cy+G.ry[2]*.9,ds:1}}
  if(t<w.t0){if(p.home===1){start.state='circle';start.c=1;start.ang=p.a0;return start}return null}
  var f=(t-w.t0)/w.dur,e2=ease(f);
  return{x:start.x+(end.x-start.x)*e2,y:start.y+(end.y-start.y)*e2,ds:start.ds+(end.ds-start.ds)*e2,face:true,state:'walk',walk:(t-w.t0)*11}
}

/* ---------- drawing ---------- */
function rr(x,y,w,h,r){cx.beginPath();cx.moveTo(x+r,y);cx.arcTo(x+w,y,x+w,y+h,r);cx.arcTo(x+w,y+h,x,y+h,r);cx.arcTo(x,y+h,x,y,r);cx.arcTo(x,y,x+w,y,r);cx.closePath()}
function seg(x1,y1,x2,y2){cx.beginPath();cx.moveTo(x1,y1);cx.lineTo(x2,y2);cx.stroke()}
function heartPath(x,y,s){cx.save();cx.translate(x,y);cx.scale(s/22,s/22);cx.translate(0,-7);cx.beginPath();
  cx.moveTo(0,4);cx.bezierCurveTo(0,2.5,-2.5,-2,-6,-2);cx.bezierCurveTo(-11,-2,-11,4,-11,4);cx.bezierCurveTo(-11,7.5,-7,11,0,15);
  cx.bezierCurveTo(7,11,11,7.5,11,4);cx.bezierCurveTo(11,4,11,-2,6,-2);cx.bezierCurveTo(2.5,-2,0,2.5,0,4);cx.restore()}
function heart(x,y,s,col,al){cx.globalAlpha=al;heartPath(x,y,s);cx.fillStyle=col;cx.fill();cx.globalAlpha=al*.55;heartPath(x-s*.12,y-s*.14,s*.32);cx.fillStyle='rgba(255,255,255,.7)';cx.fill();cx.globalAlpha=1}
function crown(x,y,u){cx.beginPath();cx.moveTo(x-6*u,y);cx.lineTo(x-6.5*u,y-6*u);cx.lineTo(x-3*u,y-3*u);cx.lineTo(x,y-8*u);cx.lineTo(x+3*u,y-3*u);cx.lineTo(x+6.5*u,y-6*u);cx.lineTo(x+6*u,y);cx.closePath();
  cx.fillStyle='#ffd98e';cx.fill();cx.lineWidth=1*u;cx.strokeStyle='#b8741a';cx.stroke()}

function person(p,o,t){
  var u=G.s*o.ds,x=o.x,y=o.y,lk=p.lk;
  var raise=0,bob=0,sway=0,walk=o.state==='walk';
  if(!walk){
    sway=Math.sin(t*1.7+lk.ph)*1.2*u;
    var wave=Math.sin(t*2.4-(o.ang||0)*1.3);raise=Math.pow(Math.max(0,wave),3);
    if(o.arrived!==undefined&&o.arrived<1.6)raise=1;
    bob=raise*1.6*u;
  }else{bob=Math.abs(Math.sin(o.walk))*1.4*u}
  x+=sway;y-=bob;
  var legH=10*u,torH=15*u,torW=14*u,hr=6.6*u,hip=y-legH,sh=hip-torH,hy=sh-hr*1.02;
  cx.lineCap='round';
  // legs
  var sw=walk?Math.sin(o.walk)*3.2*u:0;cx.strokeStyle=NAVY;cx.lineWidth=3.8*u;
  seg(x-3*u,hip,x-3*u+sw,y+bob*.6);seg(x+3*u,hip,x+3*u-sw,y+bob*.6);
  // arms behind the body when facing away
  function arms(){
    cx.strokeStyle=lk.shirt;cx.lineWidth=3.5*u;
    [-1,1].forEach(function(sd){
      var r=walk?0:raise,swing=walk?Math.sin(o.walk+(sd>0?Math.PI:0))*2.5*u:0;
      var hx=x+sd*(9.5*u+2*u*r),hyy=sh+13*u-r*23*u+swing;
      seg(x+sd*5.5*u,sh+3*u,hx,hyy);
      cx.fillStyle=lk.skin;cx.beginPath();cx.arc(hx,hyy,2.1*u,0,TAU);cx.fill();
    });
  }
  if(!o.face)arms();
  // body
  cx.fillStyle=lk.shirt;rr(x-torW/2,sh,torW,torH+2*u,5*u);cx.fill();
  if(o.face)arms();
  // hair behind the head (puff or long)
  if(lk.style===1){cx.fillStyle=lk.hair;cx.beginPath();cx.arc(x,hy-1*u,hr*1.38,0,TAU);cx.fill()}
  // head
  cx.fillStyle=lk.skin;cx.beginPath();cx.arc(x,hy,hr,0,TAU);cx.fill();
  if(o.face){
    if(lk.style!==1){cx.fillStyle=lk.hair;cx.beginPath();cx.arc(x,hy,hr*1.02,Math.PI*1.08,Math.PI*1.92);cx.closePath();cx.fill()}
    if(lk.style===2){cx.fillStyle=lk.hair;cx.beginPath();cx.arc(x,hy-hr*1.05,2.8*u,0,TAU);cx.fill()}
    // happy closed eyes and a big smile
    cx.strokeStyle=FACE;cx.lineWidth=Math.max(.7,1*u);
    cx.beginPath();cx.arc(x-2.4*u,hy+.6*u,1.25*u,Math.PI*1.15,Math.PI*1.85);cx.stroke();
    cx.beginPath();cx.arc(x+2.4*u,hy+.6*u,1.25*u,Math.PI*1.15,Math.PI*1.85);cx.stroke();
    cx.beginPath();cx.arc(x,hy+1.6*u,2.5*u,Math.PI*.15,Math.PI*.85);cx.stroke();
    cx.fillStyle='rgba(255,120,140,.35)';cx.beginPath();cx.arc(x-4*u,hy+2.6*u,1.2*u,0,TAU);cx.arc(x+4*u,hy+2.6*u,1.2*u,0,TAU);cx.fill();
  }else{
    cx.fillStyle=lk.hair;cx.beginPath();cx.arc(x,hy-.3*u,hr*1.01,0,TAU);cx.fill();
    if(lk.style===2){cx.beginPath();cx.arc(x,hy-hr*1.05,2.8*u,0,TAU);cx.fill()}
  }
  // a crown pops up when a member starts a new tribe
  if(p.lead!==undefined&&o.arrived!==undefined&&o.arrived<2.6){
    var k=Math.min(1,o.arrived/.35),fade=o.arrived>2?1-(o.arrived-2)/.6:1;
    cx.globalAlpha=Math.max(0,fade);crown(x,hy-hr-4*u-k*3*u,u*(.6+.4*k));cx.globalAlpha=1;
  }
  return{hx:x,hy:hy-hr};
}

function glowGround(c,amt){
  if(amt<=0)return;var x=G.cx[c],y=G.cy,rx=G.rx[c]*1.5,ry=G.ry[c]*2.1;
  cx.save();cx.translate(x,y);cx.scale(1,ry/rx);
  var g=cx.createRadialGradient(0,0,0,0,0,rx);g.addColorStop(0,'rgba(242,173,60,'+(.22*amt)+')');g.addColorStop(1,'rgba(242,173,60,0)');
  cx.fillStyle=g;cx.beginPath();cx.arc(0,0,rx,0,TAU);cx.fill();
  cx.strokeStyle='rgba(255,217,142,'+(.28*amt)+')';cx.lineWidth=1/(ry/rx);cx.beginPath();cx.arc(0,0,rx*.72,0,TAU);cx.stroke();cx.restore();
}
function fire(c,t,amt){
  if(amt<=0)return;var x=G.cx[c],y=G.cy-G.ry[c]*.15,u=G.s*amt;
  var g=cx.createRadialGradient(x,y-8*u,0,x,y-8*u,48*u);g.addColorStop(0,'rgba(255,190,90,.38)');g.addColorStop(1,'rgba(255,190,90,0)');
  cx.fillStyle=g;cx.beginPath();cx.arc(x,y-8*u,48*u,0,TAU);cx.fill();
  cx.strokeStyle='#6b4423';cx.lineWidth=3.4*u;cx.lineCap='round';seg(x-9*u,y,x+9*u,y-4*u);seg(x+9*u,y,x-9*u,y-4*u);
  var cols=['#f97316','#f2ad3c','#fff3c4'],hs=[21,14,8],ws=[8.5,6,3.4];
  for(var k=0;k<3;k++){
    var h=hs[k]*u*(.9+.12*Math.sin(t*9+k*1.7)+.06*Math.sin(t*13.7+k*2.3)),wd=ws[k]*u,tip=Math.sin(t*3.1+k)*1.6*u,b=y-2*u;
    cx.fillStyle=cols[k];cx.beginPath();cx.moveTo(x+tip,b-h);
    cx.bezierCurveTo(x+wd,b-h*.45,x+wd*.9,b,x,b);cx.bezierCurveTo(x-wd*.9,b,x-wd,b-h*.45,x+tip,b-h);cx.fill();
  }
}

var HCOL=['#ff5d7a','#ff7f9b','#ffd98e','#f2ad3c','#ff9eb5'];
function burst(x,y,n,u){for(var i=0;i<n;i++){var a=-Math.PI/2+(i-(n-1)/2)*.5;hearts.push({x:x,y:y,vx:Math.cos(a)*28*u,vy:Math.sin(a)*42*u-10*u,age:0,life:1.6,s:(6+rnd(i+T*7)*3)*u,c:HCOL[i%HCOL.length]})}}

function frame(t,dt){
  cx.setTransform(dpr,0,0,dpr,0,0);cx.clearRect(0,0,W,H);
  var s=G.s;
  // which tribes exist yet
  var litL=clamp((t-(LEAVE_L.t0+LEAVE_L.dur))/.6,0,1),litR=clamp((t-(LEAVE_R.t0+LEAVE_R.dur))/.6,0,1);
  for(var q=soft.length-1;q>=0;q--){var sh=soft[q];sh.age+=dt;if(sh.age>sh.life){soft.splice(q,1);continue}
    sh.y+=sh.vy*dt;var sx=sh.x+Math.sin(sh.age*1.3+sh.ph)*10*s;heart(sx,sh.y,sh.s,sh.c,.2*Math.sin(Math.min(1,sh.age/sh.life)*Math.PI))}
  glowGround(1,1);glowGround(0,litL);glowGround(2,litR);
  // sort everyone and the fires by depth
  var items=[];
  people.forEach(function(p){var o=where(p,t);if(o)items.push({y:o.y,p:p,o:o})});
  items.push({y:G.cy-G.ry[1]*.15,fire:1,amt:1});items.push({y:G.cy-G.ry[0]*.15,fire:0,amt:litL});items.push({y:G.cy-G.ry[2]*.15,fire:2,amt:litR});
  items.sort(function(a,b){return a.y-b.y});
  var heads=[];
  items.forEach(function(it){
    if(it.fire!==undefined){fire(it.fire,t,it.amt);return}
    var h=person(it.p,it.o,t);if(it.o.state==='circle')heads.push(h);
    // a little burst of hearts the moment someone joins
    if(it.o.arrived!==undefined&&!it.p.popped&&dt>0){it.p.popped=true;burst(h.hx,h.hy,it.p.lead!==undefined?7:4,s)}
  });
  if(dt>0){
    // hearts float up from the circles
    nextHeart-=dt;
    if(nextHeart<=0&&heads.length){var hd=heads[Math.floor(Math.random()*heads.length)];
      hearts.push({x:hd.hx,y:hd.hy-4*s,vx:(Math.random()-.5)*18*s,vy:-(26+Math.random()*18)*s,age:0,life:2.8,s:(7+Math.random()*5)*s,c:HCOL[Math.floor(Math.random()*HCOL.length)]});
      nextHeart=.12+Math.random()*.14}
    // big soft hearts drifting up behind everyone: love all over the place
    nextSoft-=dt;
    if(nextSoft<=0){soft.push({x:Math.random()*W,y:H+20*s,vy:-(14+Math.random()*10)*s,ph:Math.random()*6.3,age:0,life:6+Math.random()*2,s:(16+Math.random()*12)*s,c:HCOL[Math.floor(Math.random()*HCOL.length)]});nextSoft=.45+Math.random()*.35}
    // once all three tribes stand, hearts travel between them
    if(t>END-1.5){nextArc-=dt;if(nextArc<=0){var pairs=[[1,0],[1,2],[0,1],[2,1],[0,2],[2,0]],pr=pairs[Math.floor(Math.random()*pairs.length)];arcs.push({a:pr[0],b:pr[1],age:0,dur:1.7});nextArc=1.1+Math.random()*.6}}
  }
  // flying hearts
  for(var i=hearts.length-1;i>=0;i--){var h2=hearts[i];h2.age+=dt;if(h2.age>h2.life){hearts.splice(i,1);continue}
    h2.x+=h2.vx*dt+Math.sin((h2.age+i)*4)*.25*s;h2.y+=h2.vy*dt;h2.vx*=.985;
    var al=Math.min(1,h2.age*5)*(1-Math.pow(h2.age/h2.life,2));heart(h2.x,h2.y,h2.s,h2.c,al)}
  for(var j=arcs.length-1;j>=0;j--){var a=arcs[j];a.age+=dt;var f=a.age/a.dur;if(f>=1){burst(G.cx[a.b],G.cy-34*s,3,s*.8);arcs.splice(j,1);continue}
    var x0=G.cx[a.a],x1=G.cx[a.b],y0=G.cy-30*s,mx=(x0+x1)/2,my=Math.min(y0-H*.42,8*s),e=ease(f);
    var bx=(1-e)*(1-e)*x0+2*(1-e)*e*mx+e*e*x1,by=(1-e)*(1-e)*y0+2*(1-e)*e*my+e*e*y0;
    heart(bx,by,13*s,'#ff6f8f',Math.sin(f*Math.PI)*.95)}
}

/* ---------- run only while visible ---------- */
function tick(now){
  if(!running)return;
  var dt=last?Math.min(.05,(now-last)/1000):0;last=now;T+=dt;
  frame(T,dt);
  if(replay)replay.hidden=T<END;
  requestAnimationFrame(tick);
}
function start(){if(running||reduce)return;running=true;last=0;requestAnimationFrame(tick)}
function stop(){running=false}
function still(){ // the finished scene, frozen, with a few hearts in the air
  people.forEach(function(p){p.popped=true});hearts=[];arcs=[];
  for(var c=0;c<3;c++)for(var k=0;k<3;k++)hearts.push({x:G.cx[c]+(k-1)*G.rx[c]*.6,y:G.cy-(70+k*16)*G.s,vx:0,vy:0,age:.6,life:3,s:(8+k*3)*G.s,c:HCOL[(c+k)%HCOL.length]});
  soft=[];for(var m=0;m<6;m++)soft.push({x:W*(.08+m*.17),y:H*(.25+(m%3)*.18),vy:0,ph:0,age:3,life:6,s:(18+(m%3)*6)*G.s,c:HCOL[m%HCOL.length]});
  frame(END+2,0);
}
function resize(){layout();if(reduce)still();else if(!running)frame(T,0)}
layout();
if(reduce){still()}else{frame(0,0)}
if('ResizeObserver'in window)new ResizeObserver(function(){resize()}).observe(cv);else window.addEventListener('resize',resize);
if(!reduce){
  if('IntersectionObserver'in window)new IntersectionObserver(function(e){visible=e[0].isIntersecting;if(visible)start();else stop()},{threshold:.25}).observe(cv);
  else start();
  document.addEventListener('visibilitychange',function(){if(document.hidden)stop();else if(visible)start()});
}
if(replay)replay.addEventListener('click',function(){T=0;hearts=[];arcs=[];soft=[];nextArc=0;people.forEach(function(p){p.popped=false});replay.hidden=true;if(!running)start()});
})();

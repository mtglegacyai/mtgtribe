/* MTG TRIBE | back-to-top button.
   A flat gold button in the bottom-right corner. It appears once you scroll down, its ring fills as you
   read, and one tap takes you back to the top. Same look and place as the Canton pages' button.
   Include on any page: <script src="/assets/tribe/to-top.js?v=1" defer></script> */
(function(){
"use strict";
if(document.getElementById('totop'))return; // the page already has one
var d=document,reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var css=d.createElement('style');
css.textContent=
'.tt{position:fixed;right:max(18px,env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:95;display:grid;place-items:center;width:56px;height:56px;padding:0;border:0;border-radius:50%;cursor:pointer;background:transparent;color:#000;-webkit-tap-highlight-color:transparent;opacity:0;visibility:hidden;transform:translateY(14px) scale(.9);transition:opacity .3s,transform .35s cubic-bezier(.16,1,.3,1),visibility 0s .35s}'+
'.tt.on{opacity:1;visibility:visible;transform:none;transition:opacity .3s,transform .35s cubic-bezier(.16,1,.3,1),visibility 0s}'+
'.tt svg.pr{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg)}'+
'.tt .tr{fill:rgba(0,0,0,.6);stroke:rgba(255,255,255,.18);stroke-width:3}'+
'.tt .bar{fill:none;stroke:#ffd98e;stroke-width:3;stroke-linecap:round;stroke-dasharray:157;stroke-dashoffset:157}'+
'.tt .core{position:relative;display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:linear-gradient(180deg,#ffd98e,#f2ad3c);box-shadow:inset 0 0 0 1px rgba(255,236,190,.6),0 8px 20px rgba(0,0,0,.4);transition:transform .2s cubic-bezier(.16,1,.3,1),filter .2s}'+
'.tt .core svg{width:19px;height:19px}'+
'.tt:hover .core{transform:translateY(-2px);filter:brightness(1.06)}'+
'.tt:active .core{transform:scale(.94)}'+
'.tt:focus-visible{outline:3px solid #ffd98e;outline-offset:3px}'+
'@media (prefers-reduced-motion:reduce){.tt,.tt.on,.tt .core{transition:none}}'+
'@media print{.tt{display:none}}';
d.head.appendChild(css);
var b=d.createElement('button');b.type='button';b.className='tt';b.id='totop';b.setAttribute('aria-label','Back to top');b.title='Back to top';
b.innerHTML='<svg class="pr" viewBox="0 0 56 56" aria-hidden="true"><circle class="tr" cx="28" cy="28" r="25"/><circle class="bar" cx="28" cy="28" r="25"/></svg>'+
 '<span class="core"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg></span>';
d.body.appendChild(b);
var bar=b.querySelector('.bar'),L=157,tick=false;
function upd(){tick=false;var y=window.scrollY||d.documentElement.scrollTop,h=d.documentElement.scrollHeight-window.innerHeight;
  b.classList.toggle('on',y>window.innerHeight*.8);bar.style.strokeDashoffset=(L-L*(h>0?Math.min(1,y/h):0)).toFixed(1)}
window.addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});
window.addEventListener('resize',upd);upd();
b.addEventListener('click',function(e){
  window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});
  // move keyboard focus to the top too, so the next Tab starts from the menu
  if(e.detail!==0)return; // mouse or touch: no visible focus jump
  var t=d.querySelector('.skip')||d.querySelector('a[href],button');if(t)setTimeout(function(){try{t.focus({preventScroll:true})}catch(e){}},reduce?0:500);
});
})();

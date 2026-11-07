/* MTG TRIBE | live CNTN (Canton Strategic Holdings, Nasdaq) price card.
   Fills every <div class="cl" data-cntn-live> with TradingView's free mini chart: price, change and a
   1 month chart in MTG gold. Loads only when the card is near the screen. If TradingView cannot load,
   the card keeps its fallback line (a link to Nasdaq.com, and on /cntn/ the weekly snapshot price).
   Other markets: add data-symbol="EXCHANGE:PAIR" to the card (e.g. the CC card on /cc/ uses KRAKEN:CCUSD).
   Cards without data-symbol show CNTN.
   Include once per page: <script src="/assets/tribe/cntn-live.js?v=2" defer></script> */
(function(){
"use strict";
var cards=document.querySelectorAll('[data-cntn-live]');if(!cards.length)return;
var css=document.createElement('style');
css.textContent=
'.cl{margin:18px 0 22px;border-radius:18px;border:1px solid rgba(242,173,60,.38);background:radial-gradient(420px circle at 0 0,rgba(242,173,60,.09),transparent 60%),rgba(255,255,255,.02);overflow:hidden}'+
'.cl-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 12px;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.08)}'+
'.cl-t{color:#fff;font-weight:800;font-size:15px;letter-spacing:.02em}.cl-t small{display:block;margin-top:2px;color:#a9afb7;font-weight:600;font-size:12.5px;letter-spacing:0}'+
'.cl-live{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;color:#9ff5c6;background:rgba(61,220,132,.1);box-shadow:inset 0 0 0 1px rgba(61,220,132,.35);font-weight:800;font-size:11px;letter-spacing:.14em;text-transform:uppercase}'+
'.cl-live i{width:7px;height:7px;border-radius:50%;background:#3ddc84;box-shadow:0 0 8px #3ddc84}'+
'.cl-body{height:0;transition:height .4s ease}.cl.cl-on .cl-body{height:210px}'+
'.cl-body .tradingview-widget-container,.cl-body .tradingview-widget-container__widget{height:100%!important}'+
'.cl iframe{color-scheme:light;background:transparent}'+
'.cl-fb{margin:0;padding:14px 16px;color:#c3c7cd;font-size:14.5px;line-height:1.55}.cl.cl-on .cl-fb{display:none}'+
'.cl-fb a,.cl-foot a{color:#e8b862;font-weight:700;text-decoration:underline;text-underline-offset:3px}'+
'.cl-foot{margin:0;padding:10px 16px 12px;border-top:1px solid rgba(255,255,255,.06);color:#8a919b;font-size:12.5px;line-height:1.5}'+
'@media (prefers-reduced-motion:no-preference){.cl-live i{animation:clp 2s ease-in-out infinite}}@keyframes clp{50%{box-shadow:0 0 0 5px rgba(61,220,132,0),0 0 8px #3ddc84}}'+
'@media (max-width:560px){.cl.cl-on .cl-body{height:190px}}';
document.head.appendChild(css);

var CFG={symbol:'NASDAQ:CNTN',width:'100%',height:'100%',locale:'en',dateRange:'1M',colorTheme:'dark',isTransparent:true,autosize:true,largeChartUrl:'',
  trendLineColor:'rgba(242, 173, 60, 1)',underLineColor:'rgba(242, 173, 60, 0.25)',underLineBottomColor:'rgba(242, 173, 60, 0)'};

function load(card){
  if(card.dataset.loaded)return;card.dataset.loaded='1';
  var body=card.querySelector('.cl-body'),fb=card.querySelector('.cl-fb');if(!body)return;
  var wrap=document.createElement('div');wrap.className='tradingview-widget-container';
  var inner=document.createElement('div');inner.className='tradingview-widget-container__widget';wrap.appendChild(inner);
  var cfg={};for(var k in CFG)cfg[k]=CFG[k];
  if(card.dataset.symbol&&/^[A-Z0-9_]+:[A-Z0-9_.]+$/.test(card.dataset.symbol))cfg.symbol=card.dataset.symbol;
  var s=document.createElement('script');s.src='https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js';s.async=true;s.text=JSON.stringify(cfg);
  var done=false;
  function ok(){if(done)return;done=true;card.classList.add('cl-on')}
  function fail(){if(done)return;done=true;if(fb){var m=fb.querySelector('.cl-msg');if(m)m.textContent='The live price could not load right now.'}}
  s.onerror=fail;
  // show the card once TradingView's frame has loaded
  if('MutationObserver'in window){new MutationObserver(function(ms,o){var f=wrap.querySelector('iframe');if(f){o.disconnect();f.addEventListener('load',ok);setTimeout(ok,2500)}}).observe(wrap,{childList:true,subtree:true})}
  setTimeout(function(){if(!wrap.querySelector('iframe'))fail()},12000);
  wrap.appendChild(s);body.appendChild(wrap);
}
Array.prototype.forEach.call(cards,function(card){
  if('IntersectionObserver'in window){var io=new IntersectionObserver(function(e){if(e[0].isIntersecting){io.disconnect();load(card)}},{rootMargin:'400px'});io.observe(card)}
  else load(card);
});
})();

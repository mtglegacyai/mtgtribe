/* MTG TRIBE Command Centre behaviour.
   Stores only on this device: menu state (mtg-side), Tribe Path ticks (tribe-path), a 2 minute price cache (tribe-mkt-*).
   No tracking, no cookies. */
(function(){
"use strict";
var d=document,w=window,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,c){return (c||d).querySelector(s)}function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}
function get(k){try{return JSON.parse(localStorage.getItem(k))}catch(e){return null}}
function put(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}

/* ---------- reveals ---------- */
if('IntersectionObserver'in w){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.08});
  $$('.rv').forEach(function(el){io.observe(el)});
}else $$('.rv').forEach(function(el){el.classList.add('in')});

/* ---------- menu follows the section you are reading ---------- */
(function(){
  var links=$$('.md-side .md-nav[href^="#"]'),map={};
  links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
  var ids=Object.keys(map).concat(['streams']);
  if(!('IntersectionObserver'in w))return;
  var so=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;var id=e.target.id;if(id==='streams')id='bellver';
    var a=map[id];if(!a)return;links.forEach(function(l){l.classList.toggle('is-on',l===a)});
    if(a.scrollIntoView&&w.matchMedia('(min-width:1061px)').matches){var side=$('.md-side'),r=a.getBoundingClientRect(),sr=side.getBoundingClientRect();if(r.top<sr.top+60||r.bottom>sr.bottom-160)side.scrollTo({top:a.offsetTop-sr.height/3,behavior:reduce?'auto':'smooth'})}
  })},{rootMargin:'-35% 0px -55% 0px'});
  ids.forEach(function(id){var s=d.getElementById(id);if(s)so.observe(s)});
})();

/* ---------- engine track: a spark travels the five moves ---------- */
(function(){
  var sp=$('#track .spark');if(!sp||reduce||!sp.animate)return;
  sp.animate([{left:'6%',opacity:0},{opacity:1,offset:.08},{opacity:1,offset:.92},{left:'94%',opacity:0}],{duration:5200,iterations:Infinity,easing:'cubic-bezier(.45,0,.55,1)'});
})();

/* ---------- live market: crypto from CoinGecko, then CNTN (Nasdaq stock) from TradingView ---------- */
var COINS=[['bitcoin','Bitcoin','BTC','₿'],['ethereum','Ethereum','ETH','Ξ'],['binancecoin','BNB','BNB','BNB'],['solana','Solana','SOL','SOL'],['canton-network','Canton Coin','CC','CC']];
var grid=$('#mgrid'),cur='usd',busy=false;
function money(n,c){
  var dp=n>=100?0:n>=1?2:4;
  return new Intl.NumberFormat(c==='zar'?'en-ZA':'en-US',{style:'currency',currency:c.toUpperCase(),minimumFractionDigits:dp,maximumFractionDigits:dp}).format(n);
}
var stock=null;
/* CNTN tile: built once and never redrawn, so switching USD and ZAR does not reload it */
function stockTile(){
  var el=d.createElement('div');el.className='coin stock';el.id='coin-cntn';
  el.innerHTML='<div class="st-w"></div><p class="st-fb"><b>CNTN</b> <span>Canton Strategic Holdings</span><span class="st-msg">Loading the live price.</span> <a href="https://www.nasdaq.com/market-activity/stocks/cntn" target="_blank" rel="noopener">See CNTN on Nasdaq.com</a></p>'+
    '<span class="st-foot">Nasdaq stock, priced in USD · 1 month chart · <a href="https://www.tradingview.com/symbols/NASDAQ-CNTN/" target="_blank" rel="noopener nofollow">TradingView</a>, may be delayed</span>';
  var box=$('.st-w',el),wrap=d.createElement('div');wrap.className='tradingview-widget-container';
  var inner=d.createElement('div');inner.className='tradingview-widget-container__widget';wrap.appendChild(inner);
  var s=d.createElement('script');s.src='https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js';s.async=true;
  s.text=JSON.stringify({symbol:'NASDAQ:CNTN',width:'100%',height:'100%',locale:'en',dateRange:'1M',colorTheme:'dark',isTransparent:true,autosize:true,largeChartUrl:'',
    trendLineColor:'rgba(242, 173, 60, 1)',underLineColor:'rgba(242, 173, 60, 0.25)',underLineBottomColor:'rgba(242, 173, 60, 0)'});
  var done=false;function ok(){if(!done){done=true;el.classList.add('st-on')}}
  function fail(){if(!done){done=true;$('.st-msg',el).textContent='The live price could not load right now.'}}
  s.onerror=fail;
  if('MutationObserver'in w)new MutationObserver(function(m,o){var f=wrap.querySelector('iframe');if(f){o.disconnect();f.addEventListener('load',ok);setTimeout(ok,2500)}}).observe(wrap,{childList:true,subtree:true});
  setTimeout(function(){if(!wrap.querySelector('iframe'))fail()},12000);
  wrap.appendChild(s);box.appendChild(wrap);
  return el;
}
function tiles(){
  $$('.coin:not(.stock)',grid).forEach(function(el){grid.removeChild(el)});
  if(!stock){stock=stockTile();grid.appendChild(stock)}
  COINS.forEach(function(c){
    var el=d.createElement('div');el.className='coin sk';el.id='coin-'+c[0];
    el.innerHTML='<span class="sym" aria-hidden="true">'+c[3]+'</span><span class="nm">'+c[1]+'<small>'+c[2]+'</small></span><span class="ch">+0.00%</span><span class="px">$00,000</span>'+
      '<svg class="spark" viewBox="0 0 100 40" preserveAspectRatio="none" role="img" aria-label="'+c[1]+' price over the last 7 days"></svg><span class="r7"><span class="lo"></span><span class="hi"></span></span><span class="tip" aria-hidden="true"></span>';
    grid.insertBefore(el,stock);
  });
}
function draw(el,c,data){
  el.classList.remove('sk');
  var p=data.current_price,ch=data.price_change_percentage_24h||0,up=ch>=0;
  $('.px',el).textContent=money(p,cur);
  var chEl=$('.ch',el);chEl.className='ch '+(up?'up':'dn');chEl.textContent=(up?'▲ ':'▼ ')+Math.abs(ch).toFixed(2)+'%';
  chEl.setAttribute('aria-label',(up?'up ':'down ')+Math.abs(ch).toFixed(2)+' percent in 24 hours');
  var pts=(data.sparkline_in_7d&&data.sparkline_in_7d.price)||[];var svg=$('svg.spark',el);
  if(pts.length<2){svg.innerHTML='';return}
  var lo=Math.min.apply(null,pts),hi=Math.max.apply(null,pts),rng=hi-lo||1,n=pts.length;
  function X(i){return i/(n-1)*100}function Y(v){return 36-(v-lo)/rng*32}
  var dl='';for(var i=0;i<n;i++)dl+=(i?'L':'M')+X(i).toFixed(2)+','+Y(pts[i]).toFixed(2);
  svg.innerHTML='<path class="a" d="'+dl+'L100,40L0,40Z"/><path class="l" d="'+dl+'"/><line x1="0" x2="0" y1="0" y2="40" style="opacity:0"/><circle r="0" cx="0" cy="0"/>';
  // CoinGecko always returns the 7 day chart in US dollars, whatever currency is chosen, so it is labelled USD
  $('.lo',el).textContent='7d low '+money(lo,'usd');$('.hi',el).textContent='7d high '+money(hi,'usd')+(cur!=='usd'?' (USD)':'');
  var line=$('line',svg),dot=$('circle',svg),tip=$('.tip',el);
  function at(clientX){
    var r=svg.getBoundingClientRect(),f=Math.max(0,Math.min(1,(clientX-r.left)/r.width)),i=Math.round(f*(n-1));
    var hrs=Math.round((n-1-i)*(168/(n-1)));
    line.setAttribute('x1',X(i));line.setAttribute('x2',X(i));line.style.opacity='1';
    dot.setAttribute('cx',X(i));dot.setAttribute('cy',Y(pts[i]));dot.setAttribute('r','1.6');
    tip.textContent=money(pts[i],'usd')+' · '+(hrs===0?'now':hrs<24?hrs+'h ago':Math.round(hrs/24)+'d ago');el.classList.add('hov');
  }
  function off(){line.style.opacity='0';dot.setAttribute('r','0');el.classList.remove('hov')}
  svg.onpointermove=function(e){at(e.clientX)};svg.onpointerdown=function(e){at(e.clientX)};svg.onpointerleave=off;
}
function stamp(t,cached){var dt=new Date(t);$('#m-time').textContent=(cached?'Updated ':'Live · ')+('0'+dt.getHours()).slice(-2)+':'+('0'+dt.getMinutes()).slice(-2)}
function render(list,t,cached){
  var byId={};list.forEach(function(x){byId[x.id]=x});
  COINS.forEach(function(c){var el=$('#coin-'+c[0]);if(byId[c[0]])draw(el,c,byId[c[0]]);else{el.classList.remove('sk');$('.px',el).textContent='Not available';$('.ch',el).textContent=''}});
  stamp(t,cached);$('#m-err').classList.remove('on');
}
function loadMarket(force){
  if(busy||!grid)return;var key='tribe-mkt-'+cur,c=get(key),now=Date.now();
  if(!force&&c&&now-c.t<120000&&c.list){render(c.list,c.t,true);return}
  busy=true;$('#m-ref').classList.add('spin');
  var url='https://api.coingecko.com/api/v3/coins/markets?vs_currency='+cur+'&ids='+COINS.map(function(x){return x[0]}).join(',')+'&sparkline=true&price_change_percentage=24h';
  fetch(url,{cache:'no-store'}).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(list){
    if(!Array.isArray(list)||!list.length)throw new Error('empty');
    put(key,{t:now,list:list});render(list,now,false);
  }).catch(function(){
    if(c&&c.list){render(c.list,c.t,true)}
    else{$$('.coin:not(.stock)',grid).forEach(function(el){el.classList.remove('sk');$('.px',el).textContent='-';$('.ch',el).textContent=''});$('#m-time').textContent='Prices unavailable'}
    $('#m-err').classList.add('on');
  }).then(function(){busy=false;$('#m-ref').classList.remove('spin')});
}
if(grid){
  tiles();
  $$('.seg button').forEach(function(b){b.addEventListener('click',function(){
    if(b.getAttribute('data-cur')===cur)return;cur=b.getAttribute('data-cur');
    $$('.seg button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});tiles();loadMarket(false);
  })});
  $('#m-ref').addEventListener('click',function(){loadMarket(true)});
  var started=false;
  if('IntersectionObserver'in w)new IntersectionObserver(function(e){if(e[0].isIntersecting&&!started){started=true;loadMarket(false)}},{rootMargin:'300px'}).observe(grid);else loadMarket(false);
  setInterval(function(){if(started&&!d.hidden)loadMarket(false)},125000);
}

/* ---------- Tribe Path: learning missions only, never money ---------- */
var LEVELS=[
  {name:'Find the tribe',rank:'Initiate',m:[
    ['Watch MTG\'s 2 minute 40 invite video','/#invite','Watch it'],
    ['Join the MTG TRIBE WhatsApp group','/group/','Join'],
    ['Follow @mtgtribe on YouTube and @joinmtgtribe on TikTok','https://www.youtube.com/@mtgtribe','Open YouTube']]},
  {name:'Learn the streams',rank:'Action Taker',m:[
    ['Read the stream #1 guide: the Bellver Card','https://bellveraffiliates.com/learn/','Open the guide'],
    ['Watch the ClickBaitPays quick guide (about 10 minutes)','https://clickbaitpaysus.com/mtg/','Open it'],
    ['Read the risks: the disclaimer and the safety centre','/altruva/dashboard/safety/','Safety centre']]},
  {name:'Own your keys',rank:'Builder',m:[
    ['Set up a self-custody wallet and write your recovery phrase on paper, offline','/altruva/dashboard/tutorials/','Wallet tutorial'],
    ['Try the Bitcoin DCA Calculator to see how regular buying works','https://www.musathegiant.com/dca/','Open the calculator'],
    ['Write down your own portfolio plan: which coins, how much, and when you take profit','','']]},
  {name:'Create with AI',rank:'Architect',m:[
    ['Watch one explainer and one tutorial from start to finish','/altruva/dashboard/explainers/','Explainers'],
    ['Make your first short tutorial or explainer with an AI tool','',''],
    ['Share one tutorial with someone who needs it','','']]},
  {name:'Branch out',rank:'Tribe Leader',m:[
    ['Teach one person a full step, from start to finish','',''],
    ['Start your own tribe group and welcome your first members','',''],
    ['Come back and help a new member in the MTG TRIBE','/group/','Open the group']]}
];
var RANKS=['Explorer'].concat(LEVELS.map(function(l){return l.rank})),XP=100,TOTAL=1500;
var host=$('#levels');
function state(){return get('tribe-path')||{}}
function levelsDone(s){var n=0;for(var i=0;i<LEVELS.length;i++){if(LEVELS[i].m.every(function(_,k){return s['m'+i+'-'+k]}))n=i+1;else break}return n}
function count(s){var n=0;Object.keys(s).forEach(function(k){if(s[k])n++});return n}
function paint(s,celebrate){
  var done=count(s),xp=done*XP,lv=levelsDone(s),rank=RANKS[lv];
  $('#xp-val').textContent=xp.toLocaleString('en-ZA')+' XP';
  $('#xp-bar').style.width=(xp/TOTAL*100).toFixed(1)+'%';
  $('#xp-ring').style.strokeDashoffset=(427.3*(1-xp/TOTAL)).toFixed(1);
  $('#xp-lv').textContent='Level '+lv+' of 5';$('#xp-rank').textContent=rank;$('#st-rank').textContent=rank;
  $('#xp-next').textContent=lv<5?'Next rank: '+RANKS[lv+1]+'. Finish level '+(lv+1)+' to unlock it.':'You reached the top rank. Now help someone else climb.';
  $$('.level',host).forEach(function(el,i){var all=LEVELS[i].m.every(function(_,k){return s['m'+i+'-'+k]});el.classList.toggle('done',all);
    $('small',el).textContent=LEVELS[i].m.filter(function(_,k){return s['m'+i+'-'+k]}).length+' / 3 · '+(all?'Unlocked ':'Unlocks ')+LEVELS[i].rank});
  if(celebrate)levelUp(rank);
}
function levelUp(rank){var t=$('#lvup');$('#lvup-t').textContent=rank;t.classList.add('show');clearTimeout(levelUp.t);levelUp.t=setTimeout(function(){t.classList.remove('show')},3200)}
if(host){
  LEVELS.forEach(function(L,i){
    var box=d.createElement('div');box.className='level glass';
    var h='<header><span class="lvn">'+(i+1)+'</span><b>'+L.name+'</b><small></small></header>';
    L.m.forEach(function(m,k){
      var id='m'+i+'-'+k,ext=/^https?:/.test(m[1]);
      h+='<div class="mission"><input type="checkbox" id="'+id+'"><label for="'+id+'"><span class="box"><svg aria-hidden="true"><use href="#i-check"/></svg></span><span class="t">'+m[0]+'</span><span class="xpv">+'+XP+' XP</span></label>'+
        (m[1]?'<a class="go link" href="'+m[1]+'"'+(ext?' target="_blank" rel="noopener"':'')+'>'+m[2]+'<svg class="ic arrow" aria-hidden="true"><use href="#'+(ext?'i-ext':'i-arrow')+'"/></svg>'+(ext?'<span class="sr">(opens in a new tab)</span>':'')+'</a>':'')+'</div>';
    });
    box.innerHTML=h;host.appendChild(box);
  });
  var s=state();
  $$('.mission input',host).forEach(function(cb){cb.checked=!!s[cb.id];cb.addEventListener('change',function(){
    var st=state(),before=levelsDone(st);st[cb.id]=cb.checked;put('tribe-path',st);paint(st,levelsDone(st)>before);
  })});
  paint(s,false);
  // two taps to reset, so nobody loses progress by accident (no browser pop-up needed)
  var rb=$('#xp-reset'),armed=0;
  rb.addEventListener('click',function(){
    if(!armed){armed=setTimeout(function(){armed=0;rb.textContent='Reset my progress'},4000);rb.textContent='Tap again to reset everything';return}
    clearTimeout(armed);armed=0;rb.textContent='Progress reset';put('tribe-path',{});$$('.mission input',host).forEach(function(cb){cb.checked=false});paint({},false);
    setTimeout(function(){rb.textContent='Reset my progress'},2500);
  });
}
})();

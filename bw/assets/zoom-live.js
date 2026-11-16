/* Bitcoin Wealth live on Zoom, /bw/dashboard/live-on-zoom/ (MTG, 16 Nov 2026): the next session, the countdown,
   this week's calendar dates and the time zone table. The sessions come from the page (#zl-data, built from ZOOM in
   config.py). The schedule maths between core:start and core:end is the tested JetUP /jetup/zoom/ maths, made to take
   the session list (Node: require() this file, then make(sessions)). Menu, reveal and back to top: bw.js. */
(function(){
"use strict";
/*core:start  the schedule maths, pure functions (tested in Node) */
var SA='Africa/Johannesburg', ON_MS=90*60000, DAY=86400000;
var DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
/* minutes a time zone is ahead of UTC at instant t (Intl, so daylight saving is always right) */
function offMin(tz,t){
  try{
    var o={},p=new Intl.DateTimeFormat('en-US',{timeZone:tz==='local'?undefined:tz,hourCycle:'h23',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'}).formatToParts(new Date(t));
    for(var i=0;i<p.length;i++)o[p[i].type]=p[i].value;
    var u=Date.UTC(+o.year,+o.month-1,+o.day,(+o.hour)%24,+o.minute,+o.second);
    return Math.round((u-Math.floor(t/1000)*1000)/60000);
  }catch(e){return tz===SA?120:-new Date(t).getTimezoneOffset()}
}
/* wall clock in a zone: {dow, h, m, y, mo, d} */
function wall(tz,t){var w=new Date(t+offMin(tz,t)*60000);return {dow:w.getUTCDay(),h:w.getUTCHours(),m:w.getUTCMinutes(),y:w.getUTCFullYear(),mo:w.getUTCMonth(),d:w.getUTCDate()}}
/* the UTC instant of a South African wall time */
function saInstant(y,mo,d,h,m){var guess=Date.UTC(y,mo,d,h,m);return guess-offMin(SA,guess-120*60000)*60000}
/* "14:00", 24 hour clock like the rest of the Bitcoin Wealth guide */
function hm(h,m){return (h<10?'0':'')+h+':'+(m<10?'0':'')+m}
/* a session start in any zone: time, day, and whether the day differs from South Africa */
function inZone(t,tz){var z=wall(tz,t),s=wall(SA,t);return {time:hm(z.h,z.m),day:DAYS[z.dow],short:DAYS[z.dow].slice(0,3),dow:z.dow,dayDiff:z.dow!==s.dow,shift:(z.dow-s.dow+7)%7,off:offMin(tz,t)}}
function utcLabel(min){if(!min)return 'UTC+0';var s=min<0?'-':'+',a=Math.abs(min),h=Math.floor(a/60),m=a%60;return 'UTC'+s+h+(m?':'+(m<10?'0':'')+m:'')}
function countdown(ms){ms=Math.max(0,ms);var mins=Math.ceil(ms/60000);return {d:Math.floor(mins/1440),h:Math.floor(mins%1440/60),m:mins%60}}
/* days of a group of sessions, shifted when the day differs there: "Tue to Sat", "Wed and Thu", "Tue" */
function daysLabel(dows,shift){
  var n=dows.map(function(d){return (d+shift)%7}),nm=function(d){return DAYS[d].slice(0,3)};
  if(n.length===1)return nm(n[0]);
  var run=true;for(var i=1;i<dows.length;i++)if(dows[i]!==dows[i-1]+1)run=false;
  if(run&&n.length>2)return nm(n[0])+' to '+nm(n[n.length-1]);
  return n.slice(0,-1).map(nm).join(', ')+' and '+nm(n[n.length-1]);
}
/* S: [{d: weekday 0=Sunday, h, m, l: language, e: 1 for an evening}] in South African time */
function make(S){
  /* every session start from yesterday to 8 days ahead, sorted; keep the ones not yet over (still "on" for 90 minutes) */
  function upcoming(now){
    var w=wall(SA,now),out=[];
    for(var k=-1;k<=8;k++){
      var day=new Date(Date.UTC(w.y,w.mo,w.d+k)),dow=day.getUTCDay();
      for(var i=0;i<S.length;i++)if(S[i].d===dow){
        var st=saInstant(day.getUTCFullYear(),day.getUTCMonth(),day.getUTCDate(),S[i].h,S[i].m);
        if(st+ON_MS>now)out.push({i:i,s:S[i],start:st,on:st<=now});
      }
    }
    out.sort(function(a,b){return a.start-b.start});
    return out;
  }
  /* the next start of each session (the reference for the time zone table and the calendar's "Your time") */
  function nextOfEach(now){var up=upcoming(now),r=[];for(var i=0;i<up.length;i++)if(!r[up[i].i])r[up[i].i]=up[i];return r}
  return {S:S,upcoming:upcoming,nextOfEach:nextOfEach};
}
var CORE={make:make,inZone:inZone,hm:hm,utcLabel:utcLabel,countdown:countdown,daysLabel:daysLabel,offMin:offMin,wall:wall,saInstant:saInstant,DAYS:DAYS};
/*core:end*/
if(typeof document==='undefined'){if(typeof module!=='undefined')module.exports=CORE;return}

var d=document,$=function(s,c){return (c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
var data;try{data=JSON.parse($('#zl-data').textContent)}catch(e){return}
var Z=make(data.s);
var LOCAL=(function(){try{return Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){return ''}})();
var zoneName=LOCAL?LOCAL.split('/').pop().replace(/_/g,' '):'';
function sameAsSA(t){return offMin('local',t)===offMin(SA,t)}
function txt(el,v){if(el&&el.textContent!==v)el.textContent=v}
function code(l){return {English:'en',isiXhosa:'xh',isiZulu:'zu',Sesotho:'st'}[l]||'en'}
function name(s){return s.l+' session'}
function meta(s){
  return '<span class="lg l-'+code(s.l)+'">'+s.l+'</span><span class="pt"><span class="e" aria-hidden="true">'+(s.e?'🌙':'☀️')+'</span>'+(s.e?'Evening':'Afternoon')+'</span>'
    +(!s.e&&s.l==='English'?'<span class="any">Questions welcome in any language</span>':'');
}

function renderNext(now){
  var up=Z.upcoming(now),cur=up[0],nx=up[1];
  if(!cur)return;
  var sa=inZone(cur.start,SA),lo=inZone(cur.start,'local');
  txt($('#nx-name'),name(cur.s));
  var m=$('#nx-meta'),mh=meta(cur.s);if(m.innerHTML!==mh)m.innerHTML=mh;
  var lab=$('#nx-lab');
  if(cur.on){
    if(!$('.onnow',lab))lab.innerHTML='<span class="onnow"><span class="dot" aria-hidden="true"></span>On now</span>';
    txt($('#nx-when'),'Started '+sa.day+' at '+sa.time+' SAST. Get the Zoom link in the WhatsApp group, or message MTG.');
    $('#nx-cd').hidden=true;
  }else{
    if(lab.textContent!=='Next live session')lab.textContent='Next live session';
    var w=wall(SA,now),today=w.dow===wall(SA,cur.start).dow&&cur.start-now<DAY;
    var tom=!today&&(wall(SA,now+DAY).dow===wall(SA,cur.start).dow)&&cur.start-now<2*DAY;
    txt($('#nx-when'),(today?'Today':tom?'Tomorrow':sa.day)+' at '+sa.time+' SAST (South African time)');
    var c=countdown(cur.start-now);$('#nx-cd').hidden=false;
    txt($('#cd-d'),String(c.d));txt($('#cd-h'),String(c.h));txt($('#cd-m'),String(c.m));
    $('#nx-cd').setAttribute('aria-label','Starts in '+c.d+' days, '+c.h+' hours and '+c.m+' minutes');
  }
  var loc=$('#nx-local'),lh;
  if(sameAsSA(cur.start))lh='Your device is on South African time, so <b>'+lo.day+' '+lo.time+'</b> is your time too.';
  else lh=(cur.on?'It started at <b>':'That’s <b>')+lo.day+' '+lo.time+'</b> your time'+(zoneName?' ('+zoneName+')':'')+'.';
  if(loc.innerHTML!==lh)loc.innerHTML=lh;
  if(nx){var n2=inZone(nx.start,SA);txt($('#nx-after'),'After that: '+n2.day+' '+n2.time+' SAST, '+nx.s.l+(nx.s.e?' evening':' afternoon')+'.')}
}

function renderTable(now){
  var ref=Z.nextOfEach(now);
  $$('.tzt tbody tr').forEach(function(tr){
    var ids=tr.getAttribute('data-s').split(',').map(Number),r=null;
    ids.forEach(function(i){if(ref[i]&&(!r||ref[i].start<r.start))r=ref[i]});
    if(!r)return;
    var dows=ids.map(function(i){return data.s[i].d});
    $$('td',tr).forEach(function(td){
      var tz=td.getAttribute('data-tz'),z=inZone(r.start,tz),tt=$('.tt',td),dy=$('.dy',td);
      txt(tt,z.time);
      if(z.dayDiff){if(!dy){dy=d.createElement('span');dy.className='dy';td.appendChild(dy)}txt(dy,daysLabel(dows,z.shift));}
      else if(dy)dy.remove();
    });
  });
  var r0=Z.upcoming(now)[0];
  if(!r0)return;
  $$('.zl .off[data-tz]').forEach(function(el){txt(el,utcLabel(offMin(el.getAttribute('data-tz'),r0.start)))});
  txt($('#you-zone'),(zoneName||'your device')+', '+utcLabel(offMin('local',r0.start)));
}

function renderCalendar(now){
  var w=wall(SA,now),mon=Date.UTC(w.y,w.mo,w.d-((w.dow+6)%7));
  var fmt;try{fmt=new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'short',timeZone:'UTC'})}catch(e){}
  $$('.zl .day').forEach(function(el){
    var dow=+el.getAttribute('data-dow'),idx=(dow+6)%7,dt=new Date(mon+idx*DAY);
    if(fmt)txt($('.dt',el),fmt.format(dt));
    el.classList.toggle('today',dow===w.dow);
    if(dow===w.dow)el.setAttribute('aria-current','date');else el.removeAttribute('aria-current');
  });
  if(fmt)txt($('#cal-week'),' · Week of '+fmt.format(new Date(mon)));
  var ref=Z.nextOfEach(now),local=!sameAsSA(now);
  $$('.zl .ev[data-s]').forEach(function(ev){
    var r=ref[+ev.getAttribute('data-s')],yt=$('.yt',ev);if(!r||!yt)return;
    var z=inZone(r.start,'local');
    txt(yt,local?'Your time: '+z.short+' '+z.time:'');
  });
  $$('.zl .ev.on').forEach(function(ev){ev.classList.remove('on')});
  var up=Z.upcoming(now)[0];
  if(up){   /* mark the next session only when it falls in the week on show */
    var u=wall(SA,up.start),ud=Date.UTC(u.y,u.mo,u.d),el=$('.zl .ev[data-s="'+up.i+'"]');
    if(el&&ud>=mon&&ud<mon+7*DAY)el.classList.add('on');
  }
}

function tick(){var now=Date.now();renderNext(now);renderTable(now);renderCalendar(now)}
tick();
setInterval(tick,15000);
d.addEventListener('visibilitychange',function(){if(!d.hidden)tick()});

})();

/* JetUP live on Zoom, /jetup/zoom/ (MTG, 16 Nov 2026): the next session, the countdown, this week's calendar dates
   and the time zone table. The schedule maths between core:start and core:end is unchanged from the tested
   /jetuplive/ page (Node: require() this file to get the pure functions). Reveal, menu and back to top: jetup.js. */
(function(){
"use strict";
/*core:start  the schedule maths, pure functions (tested in Node) */
var SA='Africa/Johannesburg', ON_MS=90*60000, DAY=86400000;
var S=[
 {d:2,h:20,m:0,name:'Presentation'},
 {d:4,h:20,m:0,name:'Presentation'},
 {d:6,h:20,m:0,name:'Presentation'},
 {d:0,h:15,m:0,name:'International presentation'},
 {d:0,h:20,m:0,name:'Training night'}
];
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
/* "8pm", "7:30am", "12 midnight", "12 noon" */
function hm(h,m){if(h===0&&m===0)return '12 midnight';if(h===12&&m===0)return '12 noon';var ap=h<12?'am':'pm',h12=h%12||12;return h12+(m?':'+(m<10?'0':'')+m:'')+ap}
/* a session start in any zone: time, day, and whether the day differs from South Africa */
function inZone(t,tz){var z=wall(tz,t),s=wall(SA,t);return {time:hm(z.h,z.m),day:DAYS[z.dow],short:DAYS[z.dow].slice(0,3),dayDiff:z.dow!==s.dow,off:offMin(tz,t)}}
function utcLabel(min){if(!min)return 'UTC+0';var s=min<0?'-':'+',a=Math.abs(min),h=Math.floor(a/60),m=a%60;return 'UTC'+s+h+(m?':'+(m<10?'0':'')+m:'')}
function countdown(ms){ms=Math.max(0,ms);var mins=Math.ceil(ms/60000);return {d:Math.floor(mins/1440),h:Math.floor(mins%1440/60),m:mins%60}}
/* the next start of each of the five sessions (the reference for the time zone table) */
function nextOfEach(now){var up=upcoming(now),r=[];for(var i=0;i<up.length;i++)if(!r[up[i].i])r[up[i].i]=up[i];return r}
var CORE={S:S,upcoming:upcoming,inZone:inZone,hm:hm,utcLabel:utcLabel,countdown:countdown,nextOfEach:nextOfEach,offMin:offMin,wall:wall,saInstant:saInstant};
/*core:end*/
if(typeof document==='undefined'){if(typeof module!=='undefined')module.exports=CORE;return}

var d=document,$=function(s,c){return (c||d).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
var LOCAL=(function(){try{return Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){return ''}})();
var zoneName=LOCAL?LOCAL.split('/').pop().replace(/_/g,' '):'';
function sameAsSA(t){return offMin('local',t)===offMin(SA,t)}
function txt(el,v){if(el&&el.textContent!==v)el.textContent=v}

function renderNext(now){
  var up=upcoming(now),cur=up[0],nx=up[1];
  if(!cur)return;
  var sa=inZone(cur.start,SA),lo=inZone(cur.start,'local');
  var name=cur.s.name+(cur.i===4?' (back office training)':'');
  txt($('#nx-name'),name);
  var lab=$('#nx-lab');
  if(cur.on){
    lab.innerHTML='<span class="onnow"><span class="dot" aria-hidden="true"></span>On now</span>';
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
  var loc=$('#nx-local');
  if(sameAsSA(cur.start))loc.innerHTML='Your device is on South African time, so <b>'+lo.day+' '+lo.time+'</b> is your time too.';
  else loc.innerHTML=(cur.on?'It started at <b>':'That’s <b>')+lo.day+' '+lo.time+'</b> your time'+(zoneName?' ('+zoneName+')':'')+'.';
  if(nx){var n2=inZone(nx.start,SA);txt($('#nx-after'),'After that: '+n2.day+' '+n2.time+' SAST, '+nx.s.name+(nx.i===4?' (back office training)':'')+'.')}
}

function renderTable(now){
  var ref=nextOfEach(now);
  $$('.tzt tbody tr').forEach(function(tr){
    var r=ref[+tr.getAttribute('data-s')];if(!r)return;
    $$('td',tr).forEach(function(td){
      var tz=td.getAttribute('data-tz'),z=inZone(r.start,tz),tt=$('.tt',td),dy=$('.dy',td);
      txt(tt,z.time);
      if(z.dayDiff){if(!dy){dy=d.createElement('span');dy.className='dy';td.appendChild(dy)}txt(dy,z.short);dy.title=z.day}
      else if(dy)dy.remove();
    });
  });
  $$('.off[data-tz]').forEach(function(el){var r=ref[0];if(r)txt(el,utcLabel(offMin(el.getAttribute('data-tz'),r.start)))});
  var r0=ref[0];
  if(r0)txt($('#you-zone'),(zoneName||'your device')+', '+utcLabel(offMin('local',r0.start)));
}

function renderCalendar(now){
  var w=wall(SA,now),mon=Date.UTC(w.y,w.mo,w.d-((w.dow+6)%7));
  var fmt;try{fmt=new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'short',timeZone:'UTC'})}catch(e){}
  $$('.day').forEach(function(el){
    var dow=+el.getAttribute('data-dow'),idx=(dow+6)%7,dt=new Date(mon+idx*DAY);
    if(fmt)txt($('.dt',el),fmt.format(dt));
    el.classList.toggle('today',dow===w.dow);
    if(dow===w.dow)el.setAttribute('aria-current','date');else el.removeAttribute('aria-current');
  });
  var ref=nextOfEach(now),local=!sameAsSA(now);
  $$('.ev[data-s]').forEach(function(ev){
    var r=ref[+ev.getAttribute('data-s')],yt=$('.yt',ev);if(!r||!yt)return;
    var z=inZone(r.start,'local');
    txt(yt,local?'Your time: '+z.short+' '+z.time:'');
  });
}

function tick(){var now=Date.now();renderNext(now);renderTable(now);renderCalendar(now)}
tick();
setInterval(tick,15000);
d.addEventListener('visibilitychange',function(){if(!d.hidden)tick()});

})();

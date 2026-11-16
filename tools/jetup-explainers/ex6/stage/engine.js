/* JetUP explainer #6 ("The partner plan: the rule most people miss"), 16:9. Every visual is a pure function of time t.
   The picture: a building with ten glass floors (the levels) and an access card. $250 of active trading opens floors 1 to 3;
   from the 4th direct partner each new one opens the next floor; 10 direct partners open all 10 (JetUP's business plan).
   The signature ending (the 9:09 sign-up training's) is composited on top after the stage render (tools/video-signature). */
(function () {
'use strict';
const TL = window.TL, S = TL.scenes, C = TL.cues;
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const ez = { out: x => 1 - Math.pow(1 - x, 3), inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.6, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); } };
function st(el, o, x = 0, y = 0, s = 1) {
  el.style.opacity = o.toFixed(3); el.style.visibility = o <= .002 ? 'hidden' : 'visible';
  el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)})`;
}
function vis(t, a, b, fi = .35, fo = .3) {
  if (t < a || t > b) return 0;
  return Math.min(fi <= 0 ? 1 : ez.out(lin(t, a, a + fi)), fo <= 0 ? 1 : 1 - ez.inOut(lin(t, b - fo, b)));
}
const rise = (t, a, b, d = 40, fi = .4, fo = .3) => { const v = vis(t, a, b, fi, fo); return { o: v, y: d * (1 - v) }; };
const pop = (t, a, b, fi = .35, fo = .3) => { const v = vis(t, a, b, fi, fo); return { o: v, s: .7 + .3 * ez.back(lin(t, a, a + .45)) }; };
const mk = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };

/* ---------- the glass floors: ten isometric plates, floor 1 at the bottom, a flat label at each right corner ---------- */
function makeStack(host, cx, cy1, pw, sp) {
  const P = [], Lb = [];
  for (let i = 0; i < 10; i++) {
    const p = mk('div', 'pl', '<span class="on"></span>'); const cy = cy1 - i * sp;
    p.style.cssText = `left:${cx - pw / 2}px;top:${cy - pw / 2}px;width:${pw}px;height:${pw}px;z-index:${10 + i}`;
    const l = mk('div', 'fl', `<b>${i + 1}</b><i>🔒</i>`); l.style.cssText = `left:${cx + pw * .7071 + 6}px;top:${cy}px;z-index:30`;
    host.appendChild(p); host.appendChild(l); P.push(p); Lb.push(l);
  }
  return { P, Lb };
}
function paint(stk, lit) {          // lit[i]: 0..1 for each floor
  stk.P.forEach((p, i) => {
    const k = lit[i], lift = 10 * Math.sin(Math.PI * clamp(k * 1.6));
    p.firstChild.style.opacity = k.toFixed(3);
    p.style.transform = `translateY(${(-lift).toFixed(1)}px) rotateX(60deg) rotateZ(-45deg)`;
    const l = stk.Lb[i]; l.className = k > .5 ? 'fl lit' : 'fl'; l.lastChild.style.opacity = (1 - k).toFixed(3);
  });
}
const H = makeStack($('hiso'), 560, 800, 230, 44);
const B = makeStack($('biso'), 1000, 780, 250, 46);
const on = (t, c) => ez.out(lin(t, c - .05, c + .3));

/* ---------- hook: ten levels, only three open ---------- */
function hook(t) {
  const [a, b] = S.hook;
  const s = rise(t, a + .05, b, 30, .5, .3); st($('hiso'), s.o, 0, s.y);
  paint(H, Array.from({ length: 10 }, (_, i) => i < 3 ? on(t, C.h_only + i * .22) : 0));
  const e = rise(t, a + .15, b, 24); st($('hkE'), e.o, 0, e.y);
  const p = pop(t, a + .3, b, .45, .3); st($('hk10'), p.o, 0, 0, p.s);
  const k = pop(t, C.h_only - .1, b, .4, .3); st($('hk3'), k.o, 0, 0, k.s);
  const r = rise(t, C.h_rule - .15, b, 30); st($('hkR'), r.o, 0, r.y, 1 + .05 * Math.sin(Math.PI * lin(t, C.h_rule, C.h_rule + .5)));
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .25, b, 30), r = rise(t, a + .6, b, 24); st($('hhi'), h.o, 0, h.y); st($('harch'), r.o, 0, r.y);
}

/* ---------- what's a level: you, your direct partners (level 1), the people they invite (level 2), ten levels deep ---------- */
const YOU = [960, 295], L1X = [560, 960, 1360], L1Y = 495, L2Y = 646, NS = 'http://www.w3.org/2000/svg';
const n1 = L1X.map((x, i) => { const n = mk('div', 'ab node n1', '🧑'); n.style.left = (x - 55) + 'px'; $('l1nodes').appendChild(n); return n; });
const n2 = []; L1X.forEach(x => [-130, 130].forEach(dx => { const n = mk('div', 'ab node n2', '🧑'); n.style.left = (x + dx - 38) + 'px'; $('l2nodes').appendChild(n); n2.push([n, x, x + dx]); }));
const ln1 = L1X.map(x => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', YOU[0]); l.setAttribute('y1', YOU[1] + 108); l.setAttribute('x2', x); l.setAttribute('y2', L1Y - 55); $('lines1').appendChild(l); return l; });
const ln2 = n2.map(([n, x0, x1]) => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', x0); l.setAttribute('y1', L1Y + 55); l.setAttribute('x2', x1); l.setAttribute('y2', L2Y - 38); $('lines2').appendChild(l); return l; });
const deep = []; for (let j = 0; j < 8; j++) { const y = 712 + j * 20; const r = mk('div', 'ab dr'); r.style.top = y + 'px'; const d = mk('div', 'ab dl', 'L' + (j + 3)); d.style.top = (y - 9) + 'px'; $('ldeeprows').appendChild(r); $('ldeeprows').appendChild(d); deep.push([r, d]); }
function seg(l, k) { const x1 = +l.getAttribute('x1'), y1 = +l.getAttribute('y1'), x2 = +l.getAttribute('x2'), y2 = +l.getAttribute('y2'), len = Math.hypot(x2 - x1, y2 - y1);
  l.style.strokeDasharray = len.toFixed(1); l.style.strokeDashoffset = (len * (1 - k)).toFixed(1); }
function level(t) {
  const [a, b] = S.level;
  const ti = rise(t, a + .05, b, 30); st($('ltt'), ti.o, 0, ti.y);
  st($('lsvg'), vis(t, a + .2, b, .3, .3));
  const y = pop(t, a + .25, b, .45, .3); st($('lyou'), y.o, 0, 0, y.s); st($('lyouT'), vis(t, a + .4, b, .3, .3));
  n1.forEach((n, i) => { const c = C.l_direct - .1 + i * .14, p = pop(t, c, b, .4, .3); st(n, p.o, 0, 0, p.s); seg(ln1[i], ez.out(lin(t, c - .3, c + .1))); });
  const g1 = rise(t, C.l_one - .25, b, 20); st($('lt1'), g1.o, 0, g1.y);
  n2.forEach(([n], i) => { const c = C.l_they - .05 + i * .09, p = pop(t, c, b, .4, .3); st(n, p.o, 0, 0, p.s); seg(ln2[i], ez.out(lin(t, c - .3, c + .1))); });
  const g2 = rise(t, C.l_two - .25, b, 20); st($('lt2'), g2.o, 0, g2.y);
  deep.forEach(([r, d], j) => { const v = vis(t, C.l_ten - .35 + j * .09, b, .3, .3); st(r, v * (1 - j * .06)); st(d, v); });
  const dp = rise(t, C.l_deep - .2, b, 0); st($('ldeep'), dp.o, 30 * (1 - dp.o), 0);
}

/* ---------- the building: the access card, $250 opens floors 1 to 3, the 4th direct partner opens floor 4 ... 10 open all 10 ---------- */
const FL = [C.q_one, (C.q_one + C.q_three) / 2, C.q_three].concat(C.f_cnt.slice(3));   // when each floor lights
function build(t) {
  const [a, b] = S.build;
  const ti = rise(t, a + .05, b, 30); st($('btt'), ti.o, 0, ti.y);
  const sk = rise(t, C.b_ten - .25, b, 30, .5, .3); st($('biso'), sk.o, 0, sk.y);
  const lit = FL.map(c => on(t, c));
  if (t >= C.f_all) { const pz = Math.sin(Math.PI * lin(t, C.f_all, C.f_all + .7)); lit.forEach((v, i) => lit[i] = Math.min(1, v) * (1 + .0 * pz)); }
  paint(B, lit);
  const cd = pop(t, C.b_card - .15, b, .4, .3), dock = ez.inOut(lin(t, C.b_opens - .2, C.b_opens + .35));
  st($('bcard'), cd.o, 60 * dock, 0, cd.s);
  st($('brd'), vis(t, C.b_card - .1, b, .35, .3));
  const tap = C.b_opens + .35, tk = lin(t, tap, tap + .6);
  $('brdl').style.background = t >= tap && t < tap + .7 ? '#cbfb61' : (t >= C.q_one ? 'rgba(203,251,97,.75)' : '#3a3150');
  $('brdl').style.boxShadow = t >= tap ? '0 0 22px rgba(203,251,97,.8)' : 'none';
  st($('brdring'), t >= tap && t <= tap + .6 ? .9 * (1 - tk) : 0, 0, 0, .5 + 1.2 * ez.out(tk));
  const q = pop(t, C.q_250 - .1, b, .4, .3); st($('bq'), q.o, 0, 0, q.s);
  const ok = pop(t, C.q_qual - .05, b, .35, .3); st($('bqok'), ok.o, 0, 0, ok.s);
  const n = C.f_cnt.filter(c => t >= c).length;
  $('bn').textContent = n; $('bo').textContent = Math.max(3, n);
  const cn = pop(t, C.f_1 - .25, b, .4, .3), bump = n ? 1 + .06 * Math.sin(Math.PI * lin(t, C.f_cnt[n - 1], C.f_cnt[n - 1] + .3)) : 1;
  st($('bcnt'), cn.o, 0, 0, cn.s * bump);
  const sl = rise(t, C.f_still - .1, C.f_fourth + .1, 16, .3, .25); st($('bstill'), sl.o, 0, sl.y);
  const al = pop(t, C.f_all - .1, b, .4, .3); st($('ball'), al.o, 0, 0, al.s * (1 + .05 * Math.sin(Math.PI * lin(t, C.f_all, C.f_all + .6))));
  const fg = rise(t, C.q_250, b, 10); st($('bfig'), fg.o, 0, fg.y);
}

/* ---------- what open floors pay: lot commission bars, $2 / $1 / $0.50, up to $8.00 per lot ---------- */
const BARS = []; [2, 1, 1, 1, .5, .5, .5, .5, .5, .5].forEach((v, i) => {
  const h = v * 160, x = i * 132, cls = v === 2 ? 'bar' : v === 1 ? 'bar m' : 'bar s';
  const br = mk('div', cls); br.style.cssText = `left:${x}px;height:${h}px`;
  const vl = mk('div', 'bv', '$' + v.toFixed(2)); vl.style.cssText = `left:${x}px;top:${340 - h - 42}px;color:${v === 2 ? '#cbfb61' : '#d9ccff'}`;
  const lb = mk('div', 'bl', 'L' + (i + 1)); lb.style.left = x + 'px';
  $('bars').append(br, vl, lb);
  const c = i === 0 ? C.p_l1 - .15 : i < 4 ? C.p_l24 - .15 + (i - 1) * .12 : C.p_l510 - .15 + (i - 4) * .1;
  BARS.push([br, vl, lb, c]);
});
function lots(t) {
  const [a, b] = S.lots;
  const ti = rise(t, a + .05, b, 30); st($('ptt'), ti.o, 0, ti.y);
  const ch = rise(t, C.p_lot - .25, b, 16); st($('pchip'), ch.o, 0, ch.y);
  st($('pbase'), vis(t, a + .3, b, .4, .3));
  const fade = vis(t, a, b, .01, .3);
  BARS.forEach(([br, vl, lb, c]) => {
    const g = ez.back(lin(t, c, c + .5)), seen = t >= c ? fade : 0;
    br.style.transform = `scaleY(${Math.max(0, g).toFixed(3)})`; br.style.opacity = seen.toFixed(3); br.style.visibility = seen > 0 ? 'visible' : 'hidden';
    const lv = vis(t, c + .25, b, .3, .3); vl.style.opacity = lv.toFixed(3); lb.style.opacity = (t >= c ? fade : 0).toFixed(3);
  });
  const tt = pop(t, C.p_eight - .12, b, .4, .3); st($('ptot'), tt.o, 0, 0, tt.s * (1 + .05 * Math.sin(Math.PI * lin(t, C.p_eight, C.p_eight + .5))));
  const r = rise(t, C.p_real - .12, b, 20); st($('preal'), r.o, 0, r.y);
  const fg = rise(t, C.p_lot, b, 10); st($('pfig'), fg.o, 0, fg.y);
}

/* ---------- profit share: 1.5% on every open level, paid from the 30% share ---------- */
const CH = []; for (let i = 0; i < 10; i++) { const c = mk('div', 'sc glass', `<b>1.5%</b><small>L${i + 1}</small>`); c.style.left = (i * 144) + 'px'; c.style.visibility = 'hidden'; $('chips').appendChild(c); CH.push(c); }
function share(t) {
  const [a, b] = S.share;
  const ti = rise(t, a + .05, b, 30); st($('stt'), ti.o, 0, ti.y);
  const ch = rise(t, C.s_profit - .2, b, 16); st($('schip'), ch.o, 0, ch.y);
  CH.forEach((c, i) => { const p = pop(t, C.s_one - .1 + i * .09, b, .35, .3); st(c, p.o, 0, 14 * (1 - p.o), p.s); });
  const sb = rise(t, C.s_paid - .25, b, 30); st($('sbar'), sb.o, 0, sb.y);
  const ar = vis(t, C.s_thirty - .1, b, .3, .3); st($('sarr'), ar, 0, 20 * (1 - ar));
  st($('sring'), vis(t, C.s_thirty - .05, C.s_never + .2, .25, .3) * (.7 + .3 * Math.sin(t * 6)));
  const nv = rise(t, C.s_never - .12, b, 24); st($('snever'), nv.o, 0, nv.y);
  const fg = rise(t, C.s_profit, b, 10); st($('sfig'), fg.o, 0, fg.y);
}

/* ---------- client or partner ---------- */
function client(t) {
  const [a, b] = S.client;
  const ti = rise(t, a + .05, b, 30); st($('ctt'), ti.o, 0, ti.y);
  const x = pop(t, C.c_train - .15, b, .45, .3); st($('cA'), x.o, 0, 0, x.s * (1 + .04 * Math.sin(Math.PI * lin(t, C.c_155, C.c_155 + .5))));
  const y = pop(t, C.c_earn - .15, b, .45, .3); st($('cB'), y.o, 0, 0, y.s);
  const k = rise(t, C.c_check - .12, b, 26); st($('cchk'), k.o, 0, k.y);
}

/* ---------- so that's the rule ---------- */
function recap(t) {
  const [a, b] = S.recap;
  const ti = rise(t, a + .05, b, 30); st($('rtt'), ti.o, 0, ti.y);
  [['rr1', C.r_250 - .25], ['rr2', C.r_fourth - .35], ['rr3', C.r_fourth + .9]].forEach(([id, c]) => { const r = rise(t, c, b, 30); st($(id), r.o, 0, r.y); });
}

/* ---------- now it's your turn: tap any Join JetUP button ---------- */
function turn(t) {
  const [a, b] = S.turn, tt = C.i_join + .55;
  const h = rise(t, a + .05, b, 40); st($('ut'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, a + .05, a + .5)));
  const se = pop(t, C.u_turn - .15, b, .4, .3); st($('useat'), se.o, 0, 8 * Math.sin(t * 2), se.s * (1 + .08 * Math.sin(Math.PI * lin(t, C.u_turn, C.u_turn + .5))));
  const u = rise(t, C.i_url - .3, b, 30); st($('uurl'), u.o, 0, u.y, 1 + .04 * Math.sin(Math.PI * lin(t, C.i_url, C.i_url + .6)));
  const j = pop(t, C.i_go - .1, b, .4, .3); const press = t > tt - .04 && t < tt + .16 ? .95 : 1;
  st($('ujoin'), j.o, 0, 0, j.s * press * (1 + .02 * Math.sin(t * 4)));
  const hk = ez.out(lin(t, C.i_join - .45, tt)), hv = vis(t, C.i_join - .45, b, .25, .3);
  st($('uhand'), hv, 260 * (1 - hk), 220 * (1 - hk) + (t > tt - .04 && t < tt + .16 ? 10 : 0));
  const rk = lin(t, tt, tt + .65); $('uring').style.opacity = (t >= tt && t <= tt + .65 ? .9 * (1 - rk) : 0).toFixed(3);
  $('uring').style.visibility = t >= tt && t <= tt + .65 ? 'visible' : 'hidden'; $('uring').style.transform = `scale(${(.4 + 1.6 * ez.out(rk)).toFixed(3)})`;
}

function scenes(t) { st($('top'), vis(t, S.hi[0], TL.T + 1, .5, 0)); hook(t); hi(t); level(t); build(t); lots(t); share(t); client(t); recap(t); turn(t); }

/* ---------- captions: the current line, the spoken word lit ---------- */
const capbox = $('capbox'); let lastCap = null;
function captions(t) {
  const c = TL.caps.find(c => t >= c.a && t < c.b);
  if (!c || (TL.capoff && t >= TL.capoff)) { capbox.style.visibility = 'hidden'; lastCap = null; return; }
  if (c !== lastCap) { capbox.innerHTML = c.w.map(w => `<span>${w.w}</span>`).join(' '); lastCap = c; }
  const sp = capbox.children;
  c.w.forEach((w, i) => { const end = c.w[i + 1] ? c.w[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  capbox.style.visibility = 'visible'; capbox.style.opacity = Math.min(lin(t, c.a, c.a + .12), 1 - lin(t, c.b - .12, c.b)).toFixed(3);
}

/* ---------- emoji pops on key words, as in the sign-up training ---------- */
const emoEl = document.createElement('div'); emoEl.id = 'emo';
emoEl.style.cssText = 'position:absolute;left:0;top:0;width:96px;height:96px;font:84px/96px "Noto Color Emoji";text-align:center;visibility:hidden;transform-origin:100% 100%;z-index:60';
document.body.appendChild(emoEl);
function emojis(t) {
  const E = (TL.emos || []).filter(([t0]) => t >= t0 && t <= t0 + 2).pop();
  if (!E || capbox.style.visibility !== 'visible' || (TL.kit && t >= TL.kit[0])) { emoEl.style.visibility = 'hidden'; return; }
  const age = t - E[0]; if (emoEl.textContent !== E[1]) emoEl.textContent = E[1];
  const a = Math.min(1, age / .15) * Math.min(1, (2 - age) / .3), s = .4 + .6 * ez.back(clamp(age / .4)); const r = capbox.getBoundingClientRect();
  emoEl.style.left = (r.right + 6 - 96).toFixed(1) + 'px'; emoEl.style.top = (r.top - 96 - 14 - 8 * ez.out(clamp(age / 2))).toFixed(1) + 'px';
  emoEl.style.transform = `scale(${s.toFixed(3)})`; emoEl.style.opacity = a.toFixed(3); emoEl.style.visibility = 'visible';
}

window.R = function (t) { scenes(t); captions(t); emojis(t); return Promise.all([...document.images].map(i => i.decode().catch(() => {}))); };
})();

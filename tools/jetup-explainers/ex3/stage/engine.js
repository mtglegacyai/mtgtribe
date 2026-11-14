/* JetUP explainer #3 ("Amplify 24x: the size you trade with", the market stall), 16:9. Every visual is a pure function of time t.
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
const mix = (p, q, k) => p + (q - p) * k;
const bump = (t, c, amt = .05, d = .6) => 1 + amt * Math.sin(Math.PI * lin(t, c, c + d));
const title = (id, t, a, b) => { const r = rise(t, a + .05, b, 30); st($(id), r.o, 0, r.y); };

/* the 24 stalls: 6 across, 4 down. Stall 1 is yours (lime); the other 23 are the size Amplify adds (dashed) */
function grid(el, skipFirst) {
  const out = [];
  for (let i = 0; i < 24; i++) {
    if (i === 0 && skipFirst) { out.push(null); continue; }
    const d = document.createElement('div'); d.className = 'gst' + (i === 0 ? ' mine' : '');
    d.style.left = (i % 6) * 166 + 'px'; d.style.top = Math.floor(i / 6) * 132 + 'px'; d.innerHTML = '<b>' + (i + 1) + '</b>';
    el.appendChild(d); out.push(d);
  }
  return out;
}
const SG = grid($('sgrid'), true); grid($('egrid'), false);
if (C.new) $('mr1t').textContent = 'Start small, and learn how it moves';

/* ---------- hook: $50 trades like $1,200. One word: Amplify 24x ---------- */
function hook(t) {
  const [a, b] = S.hook;
  const e = rise(t, a + .05, b, 24); st($('hkE'), e.o, 0, e.y);
  const p5 = pop(t, C.h_50, b, .45, .3); st($('h50'), p5.o, -40 * (1 - ez.out(lin(t, C.h_50, C.h_50 + .55))), 0, p5.s);
  const lk = rise(t, C.h_like, b, 20); st($('hlk'), lk.o, 0, lk.y);
  const p12 = pop(t, C.h_12, b, .45, .3); st($('h12'), p12.o, 40 * (1 - ez.out(lin(t, C.h_12, C.h_12 + .55))), 0, p12.s * bump(t, C.h_12 + .45, .04, .55));
  const k = rise(t, C.h_word, b, 34); st($('hkB'), k.o, 0, k.y);
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .25, b, 30), r = rise(t, a + .6, b, 24); st($('hhi'), h.o, 0, h.y); st($('harch'), r.o, 0, r.y);
}

/* ---------- the market stall: your one stall, then it takes its place as stall 1 of 24 ---------- */
function stall(t) {
  const [a, b] = S.stall;
  title('att', t, a, b);
  const hv = vis(t, C.a_pop, b, .4, .3), pp = .8 + .2 * ez.back(lin(t, C.a_pop, C.a_pop + .5)), k = ez.inOut(lin(t, C.a_shrink, C.a_shrink + .7));
  st($('stH'), hv, mix(705 + 255 * (1 - pp), 110, k), mix(290 + 197 * (1 - pp), 270, k), mix(pp, 150 / 510, k));
  const c1 = pop(t, C.a_one, C.a_shrink + .15, .35, .25); st($('s1chip'), c1.o, 0, 0, c1.s);
  for (let i = 1; i < 24; i++) { const p = pop(t, C.a_shrink + .55 + i * .045, b, .3, .3); st(SG[i], p.o, 0, 0, p.s); }
  const c24 = pop(t, C.a_24, b, .45, .3); st($('s24'), c24.o, 0, 0, c24.s * bump(t, C.a_24 + .45, .03, .55));
  const l1 = rise(t, C.a_leg, b, 24), l2 = rise(t, C.a_leg + .35, b, 24); st($('sl1'), l1.o, 0, l1.y); st($('sl2'), l2.o, 0, l2.y);
}

/* ---------- the money plan: $155 in, $50 to Sonic, $100 + $100 promo, a few dollars spare ---------- */
function plan(t) {
  const [a, b] = S.plan;
  title('ptt', t, a, b);
  const d = pop(t, C.p_dep - .1, b, .45, .3); st($('pdep'), d.o, 0, 0, d.s);
  [['pr1', C.p_sonic], ['pr2', C.p_bal], ['pr3', C.p_bonus], ['pr4', C.p_spare]].forEach(([id, c]) => { const r = rise(t, c - .1, b, 24); st($(id), r.o, 0, r.y); });
  const p2 = pop(t, C.p_200, b, .4, .3); st($('p200'), p2.o, 0, 0, p2.s * bump(t, C.p_200 + .4, .05));
}

/* ---------- amplify 24x: $50 x 24 = $1,200, $200 x 24 = $4,800, $6,000 of exposure ---------- */
function result(id, t, c) {
  const el = $(id); el.style.opacity = lin(t, c - .05, c + .2).toFixed(3);
  el.style.transform = `scale(${(.6 + .4 * ez.back(lin(t, c - .05, c + .4))).toFixed(3)})`;
}
function amp(t) {
  const [a, b] = S.amp;
  title('mtt', t, a, b);
  $('m24').style.transform = `scale(${bump(t, C.m_24, .18).toFixed(3)})`;
  const r1 = pop(t, C.m_24 + .45, b, .4, .3); st($('e1'), r1.o, 0, 0, r1.s); result('e1r', t, C.m_12);
  const r2 = pop(t, C.m_200 - .15, b, .4, .3); st($('e2'), r2.o, 0, 0, r2.s); result('e2r', t, C.m_48);
  const tt = pop(t, C.m_six, b, .45, .3); st($('etot'), tt.o, 0, 0, tt.s * bump(t, C.m_six + .45, .04));
}

/* ---------- what is exposure: the size you trade with, not money you own ---------- */
function expo(t) {
  const [a, b] = S.expo;
  title('xtt', t, a, b);
  const g = vis(t, a + .15, b, .45, .3); st($('egrid'), g, 0, 24 * (1 - g), .8);
  const lg = rise(t, a + .5, b, 20); st($('eleg'), lg.o, 0, lg.y);
  const ec = pop(t, C.e_expo - .05, b, .45, .3); st($('ecard'), ec.o, 0, 0, ec.s);
  $('esub').style.opacity = lin(t, C.e_size - .1, C.e_size + .25).toFixed(3);
  const en = pop(t, C.e_not, b, .4, .3); st($('enot'), en.o, 0, 0, en.s * bump(t, C.e_not + .4, .05));
  const eo = rise(t, C.e_not + .5, b, 20); st($('eown'), eo.o, 0, eo.y);
}

/* ---------- try your own numbers: the real Exposure Calculator, tap by tap ---------- */
const LX = 470, LY = 260;                                   // the laptop screen's corner on the stage; shots are 980 x 552 css px
const TAPS = { sonic: [297, 171], training: [143, 171] }, EX = [478, 163, 470, 67];
function calc(t) {
  const [a, b] = S.calc;
  title('ctt', t, a, b);
  const lp = vis(t, a + .15, b, .45, .3); st($('lap'), lp, 0, 30 * (1 - lp), .97 + .03 * lp);
  const k = t < C.d1 + .15 ? 0 : t < C.d3 + .15 ? 1 : 2;
  for (let i = 0; i < 3; i++) $('k' + i).style.opacity = i === k ? '1' : '0';
  const tap = [[C.d1, TAPS.sonic], [C.d3, TAPS.training]].find(([c]) => t >= c - .05 && t <= c + .6);
  if (tap) { const u = lin(t, tap[0] - .05, tap[0] + .6), x = LX + tap[1][0], y = LY + tap[1][1];
    $('ctap').style.left = (x - 45).toFixed(1) + 'px'; $('ctap').style.top = (y - 45).toFixed(1) + 'px';
    st($('ctap'), .9 * (1 - u), 0, 0, .4 + 1.1 * ez.out(u)); } else st($('ctap'), 0);
  // the "Trading exposure" row, ringed once an example is tapped; the note beside it says what the number means
  const rv = vis(t, C.d2, b, .3, .3); const rg = $('cring');
  rg.style.left = (LX + EX[0]) + 'px'; rg.style.top = (LY + EX[1]) + 'px'; rg.style.width = EX[2] + 'px'; rg.style.height = EX[3] + 'px';
  st(rg, rv * (.75 + .25 * Math.sin(t * 5)));
  const nv = vis(t, C.d2, b, .3, .3); st($('cnote'), nv, 0, 16 * (1 - nv));
  const sw = lin(t, C.d4 - .1, C.d4 + .15); $('cnA').style.opacity = (1 - sw).toFixed(3); $('cnB').style.opacity = sw.toFixed(3);
  st($('ccap'), C.new ? 0 : vis(t, a + .6, b, .4, .3));
}

/* ---------- bigger size, bigger moves: the same 1% move, without and with Amplify ---------- */
const UB = [...document.querySelectorAll('.wcard .ub')], DB = [...document.querySelectorAll('.wcard .db')];
const UL = [...document.querySelectorAll('.wcard .ul')], DL = [...document.querySelectorAll('.wcard .dl')];
function swings(t) {
  const [a, b] = S.swings;
  title('wtt', t, a, b);
  const A = pop(t, a + .2, b, .45, .3); st($('wA'), A.o, 0, 0, A.s);
  const B = pop(t, C.w_big - .1, b, .45, .3); st($('wB'), B.o, 0, 0, B.s);
  const u = ez.out(lin(t, C.w_up - .1, C.w_up + .5)), d = ez.out(lin(t, C.w_down - .1, C.w_down + .5));
  UB.forEach(e => { e.style.transform = `scaleY(${u.toFixed(3)})`; }); DB.forEach(e => { e.style.transform = `scaleY(${d.toFixed(3)})`; });
  UL.forEach(e => { e.style.opacity = u.toFixed(3); }); DL.forEach(e => { e.style.opacity = d.toFixed(3); });
}

/* ---------- the loss limit is written down ---------- */
function limit(t) {
  const [a, b] = S.limit;
  title('ltt', t, a, b);
  const s = rise(t, a + .3, b, 20); st($('lsub'), s.o, 0, s.y);
  const t1 = pop(t, C.l_ten - .1, b, .45, .3); st($('lt1'), t1.o, 0, 0, t1.s);
  const t2 = pop(t, C.l_five - .1, b, .45, .3); st($('lt2'), t2.o, 0, 0, t2.s);
  const f = rise(t, C.l_five + .6, b, 20); st($('lfoot'), f.o, 0, f.y);
}

/* ---------- a bigger size, not extra money: start small, let it prove itself ---------- */
function small(t) {
  const [a, b] = S.small;
  title('rtt', t, a, b);
  const d = pop(t, C.r_0, b, .45, .3); st($('rdisc'), d.o, 0, 6 * Math.sin(t * 2), d.s);
  const r1 = rise(t, C.r_small - .1, b, 24); st($('mr1'), r1.o, 0, r1.y);
  const r2 = rise(t, C.r_prove - .1, b, 24); st($('mr2'), r2.o, 0, r2.y);
}

/* ---------- now it's your turn: claim yours, tap any Join JetUP button ---------- */
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

function scenes(t) { st($('top'), vis(t, S.hi[0], TL.T + 1, .5, 0)); hook(t); hi(t); stall(t); plan(t); amp(t); expo(t); calc(t); swings(t); limit(t); small(t); turn(t); }

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

const pend = [];
window.R = function (t) { pend.length = 0; scenes(t); captions(t); emojis(t); return Promise.all([...document.images].map(i => i.decode().catch(() => {}))); };
})();

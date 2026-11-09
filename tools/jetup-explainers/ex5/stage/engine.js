/* JetUP explainer #5 ("The $100 Fast Start Promo"), 16:9. Every visual is a pure function of time t.
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

/* ---------- hook: the $100 promo, with confetti ---------- */
const conf = $('conf'), CF = [];
for (let i = 0; i < 28; i++) { const d = document.createElement('div'); d.className = 'cf'; d.style.background = ['#cbfb61', '#e8c25a', '#e371fc', '#9b7cff', '#ffffff'][i % 5]; conf.appendChild(d);
  CF.push({ el: d, x: 120 + (i * 977) % 1680, d: .25 + (i * 37 % 100) / 180, s: 520 + (i * 53 % 300), r: (i * 71 % 360), w: (i % 3) - 1 }); }
function hook(t) {
  const [a, b] = S.hook;
  const g = pop(t, .05, b, .45, .3); st($('gift'), g.o, 0, 10 * Math.sin(t * 3), g.s * (1 + .03 * Math.sin(t * 6)));
  const h1 = rise(t, .35, b, 40), h2 = rise(t, .75, b, 40); st($('hkA'), h1.o, 0, h1.y, .9 + .1 * ez.back(lin(t, .35, .8))); st($('hkB'), h2.o, 0, h2.y);
  ['sp1', 'sp2', 'sp3'].forEach((id, i) => { const v = vis(t, .5 + .2 * i, b, .3, .3), tw = .6 + .4 * Math.sin(t * 7 + i * 2); st($(id), v * tw, 0, 0, .8 + .2 * tw); });
  CF.forEach(c => { const u = t - c.d; if (u < 0 || t > b) { c.el.style.visibility = 'hidden'; return; }
    c.el.style.visibility = 'visible'; c.el.style.opacity = clamp(1.6 - u * .5).toFixed(3);
    c.el.style.transform = `translate(${(c.x + 60 * Math.sin(u * 3 + c.r) + c.w * 40 * u).toFixed(1)}px,${(-60 + c.s * u).toFixed(1)}px) rotate(${(c.r + 220 * u).toFixed(1)}deg)`; });
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .25, b, 30), r = rise(t, a + .6, b, 24); st($('hhi'), h.o, 0, h.y); st($('harch'), r.o, 0, r.y);
}

/* ---------- the money plan: $155 in, $50 Sonic account, $100 + $100 promo ---------- */
function money(t) {
  const [a, b] = S.money;
  const ti = rise(t, a + .05, b, 30); st($('mt'), ti.o, 0, ti.y);
  const co = pop(t, a + .3, b, .45, .3); st($('coin'), co.o, 0, 6 * Math.sin(t * 2), co.s);
  const n = '$' + Math.round(155 * ez.inOut(lin(t, a + .4, C.m_dep + 1.6))); if ($('coinN').textContent !== n) $('coinN').textContent = n;
  [['m1', C.m_fifty], ['m2', C.m_hund], ['m3', C.m_spare]].forEach(([id, c]) => { const r = vis(t, c - .15, b, .35, .3); st($(id), r, 50 * (1 - ez.out(lin(t, c - .15, c + .3))), 0, .96 + .04 * ez.back(lin(t, c - .15, c + .35))); });
  const r2 = vis(t, C.m_adds - .1, b, .35, .3); st($('m2r'), r2, 0, 24 * (1 - r2), (.85 + .15 * ez.back(lin(t, C.m_adds - .1, C.m_adds + .4))) * (1 + .03 * Math.sin(Math.PI * lin(t, C.m_adds + .9, C.m_adds + 1.5))));
}

/* ---------- claim it in 4 steps ---------- */
function claim(t) {
  const [a, b] = S.claim;
  const ti = rise(t, a + .05, b, 30); st($('ctt'), ti.o, 0, ti.y);
  [['k1', C.c_cu, C.c_tile], ['k2', C.c_tile, C.c_form], ['k3', C.c_form, C.c_mail], ['k4', C.c_mail, C.c_two]].forEach(([id, c0, c1]) => {
    const p = pop(t, c0 - .15, b, .4, .3); st($(id), p.o, 0, 0, p.s); $(id).classList.toggle('on', t >= c0 - .1 && t < c1 - .15); });
  const tt = C.c_join + .45, tk = $('tapk'), jb = $('jbtn'), rk = lin(t, tt, tt + .6), on = t >= tt && t <= tt + .6;
  jb.style.transform = t > tt - .05 && t < tt + .15 ? 'scale(.94)' : 'none';
  if (on) { const jr = jb.getBoundingClientRect(); tk.style.left = (jr.left + jr.width / 2 - 55).toFixed(1) + 'px'; tk.style.top = (jr.top + jr.height / 2 - 55).toFixed(1) + 'px'; }
  tk.style.visibility = on ? 'visible' : 'hidden'; tk.style.opacity = (on ? .9 * (1 - rk) : 0).toFixed(3); tk.style.transform = `scale(${(.3 + 1.3 * ez.out(rk)).toFixed(3)})`;
  const rv = pop(t, C.c_recv - .1, C.c_two - .2, .35, .3); st($('recv'), rv.o, 0, 0, rv.s);
  const p5 = pop(t, C.c_50 - .2, b, .4, .3); st($('a50'), p5.o, 0, 0, p5.s);
  const p2 = pop(t, C.c_200 - .2, b, .4, .3); st($('a200'), p2.o, 0, 0, p2.s * (1 + .04 * Math.sin(Math.PI * lin(t, C.c_200 + .3, C.c_200 + .9))));
}

/* ---------- the promo rules, in plain words ---------- */
function rules(t) {
  const [a, b] = S.rules;
  const ti = rise(t, a + .05, b, 30); st($('rtt'), ti.o, 0, ti.y);
  [['r1', C.r_any], ['r2', C.r_bonus], ['r3', C.r_ends], ['r4', C.r_change]].forEach(([id, c]) => { const r = vis(t, c - .15, b, .35, .3); st($(id), r, 40 * (1 - ez.out(lin(t, c - .15, c + .3))), 0); });
}

/* ---------- a promo is a promo: start while it is still on ---------- */
function promo(t) {
  const [a, b] = S.promo;
  const h = pop(t, a + .05, b, .45, .3); st($('hour'), h.o, 0, 0, h.s); $('hour').style.transform += ` rotate(${(12 * Math.sin(t * 2.4)).toFixed(2)}deg)`;
  const p1 = rise(t, a + .2, b, 40), p2 = rise(t, a + .55, b, 40); st($('pA'), p1.o, 0, p1.y); st($('pB'), p2.o, 0, p2.y);
  const c = rise(t, C.p_start - .1, b, 30); st($('pC'), c.o, 0, c.y, 1 + .03 * Math.sin(Math.PI * lin(t, C.p_still - .1, C.p_still + .5)));
  const d = rise(t, C.p_confirm - .2, b, 30); st($('pD'), d.o, 0, d.y);
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

function scenes(t) { st($('top'), vis(t, S.hi[0], TL.T + 1, .5, 0)); hook(t); hi(t); money(t); claim(t); rules(t); promo(t); turn(t); }

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

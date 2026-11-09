/* JetUP explainer #4 ("The 70/30 split: where every profit goes"), 16:9. Every visual is a pure function of time t.
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

/* ---------- hook: 70 / 30 ---------- */
function hook(t) {
  const [a, b] = S.hook;
  const e = rise(t, a + .05, b, 24); st($('hkE'), e.o, 0, e.y);
  const p7 = pop(t, a + .15, b, .45, .3), p3 = pop(t, a + .45, b, .45, .3), sl = vis(t, a + .3, b, .3, .3);
  st($('h70'), p7.o, -40 * (1 - ez.out(lin(t, a + .15, a + .7))), 0, p7.s); st($('h30'), p3.o, 40 * (1 - ez.out(lin(t, a + .45, a + 1))), 0, p3.s); st($('hsl'), sl * .9);
  const k = rise(t, a + .8, b, 34); st($('hkB'), k.o, 0, k.y);
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .25, b, 30), r = rise(t, a + .6, b, 24); st($('hhi'), h.o, 0, h.y); st($('harch'), r.o, 0, r.y);
}

/* ---------- where every profit goes: the bar splits 70 / 30, the 30% fans out, then $10 becomes $7 + $3 ---------- */
function split(t) {
  const [a, b] = S.split;
  const ti = rise(t, a + .05, b, 30); st($('stt'), ti.o, 0, ti.y);
  const br = pop(t, a + .15, b, .45, .3); st($('bar'), br.o, 0, 0, .96 + .04 * ez.back(lin(t, a + .15, a + .6)));
  const sp = ez.inOut(lin(t, C.s_seventy - .2, C.s_seventy + .7));
  $('b70').style.transform = `translateX(${(-100 * (1 - sp)).toFixed(2)}%)`; $('b30').style.transform = `translateX(${(100 * (1 - lin(t, C.s_thirty - .3, C.s_thirty + .5) * 1)).toFixed(2)}%)`;
  $('b70').style.opacity = (sp).toFixed(3); $('b30').style.opacity = lin(t, C.s_thirty - .3, C.s_thirty + .3).toFixed(3);
  $('bpf').style.opacity = (1 - sp).toFixed(3);
  $('bar').style.boxShadow = t > C.s_yours - .1 && t < C.s_yours + .8 ? '0 26px 70px rgba(0,0,0,.45),0 0 0 6px rgba(203,251,97,.5)' : '0 26px 70px rgba(0,0,0,.45)';
  const fan = C.s_ten - .3;
  st($('tline'), vis(t, C.s_broker - .3, fan, .3, .3));
  [['w1', C.s_broker], ['w2', C.s_strat], ['w3', C.s_partner]].forEach(([id, c]) => { const p = pop(t, c - .15, fan, .4, .3); st($(id), p.o, 0, 20 * (1 - p.o), p.s); });
  const c10 = pop(t, C.s_ten - .1, b, .4, .3); st($('ex10'), c10.o, 0, 0, c10.s * (1 + .03 * Math.sin(t * 3)));
  st($('exar'), vis(t, C.s_seven - .5, b, .3, .3), 30 * (1 - ez.out(lin(t, C.s_seven - .5, C.s_seven))));
  const s7 = pop(t, C.s_seven - .2, b, .4, .3); st($('ex7'), s7.o, 0, 0, s7.s);
  const s3 = pop(t, C.s_seven + .15, b, .4, .3); st($('ex3'), s3.o, 0, 0, s3.s);
}

/* ---------- only on profit ---------- */
function fees(t) {
  const [a, b] = S.fees;
  const ti = rise(t, a + .05, b, 30); st($('ftt'), ti.o, 0, ti.y);
  const fa = pop(t, a + .2, b, .45, .3); st($('fA'), fa.o, 0, 0, fa.s * (1 + .03 * Math.sin(Math.PI * lin(t, C.f_profits, C.f_profits + .6))));
  const fb = pop(t, C.f_nofee - .1, b, .45, .3); st($('fB'), fb.o, 0, 0, fb.s);
  const ok = pop(t, C.f_nobody + .3, b, .35, .3); st($('fBok'), ok.o, 0, 0, ok.s * (1 + .08 * Math.sin(Math.PI * lin(t, C.f_nobody + .3, C.f_nobody + .9))));
  [['q1', C.f_mgmt], ['q2', C.f_join], ['q3', C.f_month], ['q4', C.f_amp]].forEach(([id, c]) => { const p = pop(t, c - .15, b, .4, .3); st($(id), p.o, 0, 16 * (1 - p.o), p.s); });
}

/* ---------- check the record: the line draws forward, +30.1%, then 30.1% x 70% = about 21% ---------- */
const RP = (() => { const pts = []; for (let i = 0; i <= 46; i++) { const u = i / 46; pts.push([u * 940, 300 - 210 * (u * .92 + .06 * Math.sin(u * 17) + .03 * Math.sin(u * 41))]); } return pts; })();
$('rline').setAttribute('d', 'M' + RP.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' L'));
$('rarea').setAttribute('d', 'M0,330 L' + RP.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' L') + ' L940,330 Z');
function record(t) {
  const [a, b] = S.record, eq = C.r_times - .25;
  const ti = rise(t, a + .05, b, 30); st($('rtt'), ti.o, 0, ti.y);
  const rc = vis(t, a + .2, eq, .45, .35); st($('rcard'), rc, 0, 24 * (1 - rc));
  $('rcr').setAttribute('width', (940 * ez.inOut(lin(t, a + .5, C.r_plus + .6))).toFixed(1));
  const p = pop(t, C.r_plus - .1, eq, .45, .35); st($('rplus'), p.o, 0, 0, p.s);
  const d = rise(t, C.r_nov - .15, eq, 20); st($('rdates'), d.o, 0, d.y);
  const bf = rise(t, C.r_before - .1, eq, 20); st($('rbefore'), bf.o, 0, bf.y);
  const q = pop(t, eq + .1, b, .45, .3); st($('req'), q.o, 0, 0, q.s);
  $('req').querySelector('.y').style.transform = `scale(${(1 + .08 * Math.sin(Math.PI * lin(t, C.r_21 - .1, C.r_21 + .5))).toFixed(3)})`;
  const m = rise(t, C.r_months - .3, b, 20); st($('rmo'), m.o, 0, m.y);
  const f = rise(t, C.r_fixed - .1, b, 24); st($('rfix'), f.o, 0, f.y);
}

/* ---------- try your own numbers: the real Profit Split Calculator, tap by tap ---------- */
const SX = 980 / 1280, SY = 552 / 720, LX = 470, LY = 260;   // screenshot css px -> stage px (inside the laptop screen)
const TAPS = { ten: [277, 181], myfx: [153, 181], amt: [337, 290] };
function calc(t) {
  const [a, b] = S.calc;
  const ti = rise(t, a + .05, b, 30); st($('ctt'), ti.o, 0, ti.y);
  const lp = vis(t, a + .15, b, .45, .3); st($('lap'), lp, 0, 30 * (1 - lp), .97 + .03 * lp);
  const k = t < C.d1 + .15 ? 0 : t < C.d2 + .15 ? 1 : t < C.d3 + .1 ? 2 : t < C.d3 + .45 ? 3 : t < C.d3 + .75 ? 4 : t < C.d3 + 1.05 ? 5 : 6;
  for (let i = 0; i < 7; i++) $('k' + i).style.opacity = i === k ? '1' : '0';
  const tap = [[C.d1, TAPS.ten], [C.d2, TAPS.myfx], [C.d3, TAPS.amt]].find(([c]) => t >= c - .05 && t <= c + .6);
  if (tap) { const u = lin(t, tap[0] - .05, tap[0] + .6), x = LX + tap[1][0] * SX, y = LY + tap[1][1] * SY;
    $('ctap').style.left = (x - 45).toFixed(1) + 'px'; $('ctap').style.top = (y - 45).toFixed(1) + 'px';
    st($('ctap'), .9 * (1 - u), 0, 0, .4 + 1.1 * ez.out(u)); } else st($('ctap'), 0);
  // the result row "Your share", ringed once the amount is typed
  const rv = vis(t, C.d4, b, .3, .3); const rg = $('cring'); rg.style.left = (LX + 615 * SX).toFixed(1) + 'px'; rg.style.top = (LY + 164 * SY).toFixed(1) + 'px';
  rg.style.width = (620 * SX).toFixed(1) + 'px'; rg.style.height = (76 * SY).toFixed(1) + 'px'; st(rg, rv * (.75 + .25 * Math.sin(t * 5)));
  st($('ccap'), C.new ? 0 : vis(t, a + .6, b, .4, .3));
}

/* ---------- your money, your pace ---------- */
function money(t) {
  const [a, b] = S.money;
  const ti = rise(t, a + .05, b, 30); st($('mtt'), ti.o, 0, ti.y);
  const ac = pop(t, a + .2, b, .45, .3); st($('acct'), ac.o, 0, 0, ac.s);
  const wl = pop(t, C.m_any + .3, b, .45, .3); st($('wal'), wl.o, 0, 0, wl.s);
  st($('mpath'), vis(t, C.m_any, b, .4, .3));
  const u = ez.inOut(lin(t, C.m_any + .2, C.m_any + 1.6)), cv = vis(t, C.m_any + .1, C.m_any + 1.9, .2, .3);
  $('mcoin').style.left = (690 + 480 * u).toFixed(1) + 'px'; $('mcoin').style.top = (370 - 50 * Math.sin(Math.PI * u)).toFixed(1) + 'px'; st($('mcoin'), cv);
  const r1 = rise(t, C.m_small - .1, b, 24); st($('mr1'), r1.o, 0, r1.y);
  const r2 = rise(t, C.m_prove - .1, b, 24); st($('mr2'), r2.o, 0, r2.y);
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

function scenes(t) { st($('top'), vis(t, S.hi[0], TL.T + 1, .5, 0)); hook(t); hi(t); split(t); fees(t); record(t); calc(t); money(t); turn(t); }

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

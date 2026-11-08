/* JetUP explainer #2 ("Five names. One simple picture.", the minibus taxi), 16:9. Every visual is a pure function of time t.
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

/* ---------- hook: five names, mixed up, then one picture ---------- */
const CH = ['c1', 'c2', 'c3', 'c4', 'c5'], CUE = ['h_jet', 'h_tag', 'h_copy', 'h_sonic', 'h_you'];
const P0 = [[430, 300, -7], [1330, 290, 5], [840, 520, -3], [1440, 600, 8], [460, 700, 4]];
const P1 = [[1390, 640, 7], [600, 560, -8], [1330, 300, 6], [480, 300, -9], [960, 720, 3]];
let P2 = null;
function rowTargets() {
  const s = .78, gap = 34, ws = CH.map(id => $(id).offsetWidth * s); const tot = ws.reduce((a, b) => a + b, 0) + gap * 4;
  let x = (1920 - tot) / 2; return ws.map(w => { const c = x + w / 2; x += w + gap; return [c, 560, 0]; });
}
function hook(t) {
  const [a, b] = S.hook; if (!P2) P2 = rowTargets();
  const km = ez.inOut(lin(t, C.h_mix - .1, C.h_mix + .8)), kr = ez.inOut(lin(t, C.h_one - .25, C.h_one + .5));
  CH.forEach((id, i) => {
    const el = $(id), t0 = C[CUE[i]] - .12, v = vis(t, t0, b, .3, .3);
    const k = ez.back(lin(t, t0, t0 + .45)), wob = Math.sin(Math.PI * km) * 10 * (i % 2 ? 1 : -1);
    let x = mix(mix(P0[i][0], P1[i][0], km), P2[i][0], kr), y = mix(mix(P0[i][1], P1[i][1], km), P2[i][1], kr), r = mix(mix(P0[i][2], P1[i][2], km) + wob, 0, kr);
    const s = (.6 + .4 * k) * mix(1, .78, kr);
    el.style.opacity = v.toFixed(3); el.style.visibility = v > .002 ? 'visible' : 'hidden';
    el.style.transform = `translate(${(x - el.offsetWidth / 2).toFixed(1)}px,${(y - el.offsetHeight / 2).toFixed(1)}px) rotate(${r.toFixed(2)}deg) scale(${s.toFixed(4)})`;
  });
  ['q1', 'q2', 'q3'].forEach((id, i) => { const p = pop(t, C.h_sense + .12 * i, C.h_one - .1, .3, .25); st($(id), p.o, 0, 6 * Math.sin(t * 5 + i), p.s); });
  const ti = rise(t, C.h_one - .15, b, 40, .4, .3); st($('hkT'), ti.o, 0, ti.y);
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .25, b, 30), r = rise(t, a + .6, b, 24); st($('hhi'), h.o, 0, h.y); st($('harch'), r.o, 0, r.y);
}

/* ---------- the minibus taxi: the picture builds line by line ---------- */
const CHIPS = () => [[C.t_drive - .1, C.t_copy - .1, '<span class="em">✋</span>You don\'t drive', ''],
  [C.t_copy - .1, C.d_sonic - .25, '<span class="em">🔁</span>Copy trading works the same way', ''],
  [C.k_track - .05, C.s_seat - .25, '<span class="em">📊</span>Track record public on Myfxbook', 'gold'],
  [C.g_login - .1, C.b_board - .25, '<span class="em">🔐</span>Log in yourself: see your own balance', ''],
  [C.a_no1 - .1, C.y_you - .25, '<span class="em">❌</span>Does not trade · <span class="em">❌</span>Does not take your money', 'red']];
function taxi(t) {
  const [a, b] = S.taxi;
  const v = vis(t, a, b, .45, .35);
  st($('skyline'), v * .5); st($('road'), v);
  const th = rise(t, a + .05, b, 30); st($('thead'), th.o, 0, th.y);
  // drive in from the left, wheels turning, then idle
  const kd = ez.out(lin(t, C.t_taxi - .35, C.t_taxi + 1.15)), dist = 1100 * kd, dx = -1100 + dist;
  const tv = Math.min(vis(t, C.t_taxi - .35, b, .05, .35), v); const bob = kd >= 1 ? 1.6 * Math.sin(t * 9) : 2.5 * Math.sin(t * 22);
  st($('taxi'), tv, dx, bob);
  const ang = (dist / 44) * 180 / Math.PI;
  $('w1').setAttribute('transform', `rotate(${ang.toFixed(1)} 160 236)`); $('w2').setAttribute('transform', `rotate(${ang.toFixed(1)} 560 236)`);
  $('dash').style.transform = `translateX(${(-(dist % 120)).toFixed(1)}px)`;
  // the top-left chip: one short fact at a time
  const ch = CHIPS().find(([x, y]) => t >= x && t < y), tc = $('tchip');
  if (ch) {
    if (tc.dataset.k !== ch[2]) { tc.innerHTML = ch[2]; tc.className = 'ab ' + ch[3]; tc.dataset.k = ch[2]; }
    const r = rise(t, ch[0], ch[1], 24, .3, .25); st(tc, Math.min(r.o, v), 0, r.y, .94 + .06 * ez.back(lin(t, ch[0], ch[0] + .4)));
  } else st(tc, 0);
  // the driver
  const dp = pop(t, C.d_sonic - .05, b, .35, .35); st($('drv'), Math.min(dp.o, v), 0, bob, dp.s);
  const dl = rise(t, C.d_sonic + .15, b, 24); st($('drvL'), Math.min(dl.o, v), 0, dl.y + bob);
  // your seat, in your name; later you sit in it
  const sp = pop(t, C.s_seat - .05, b, .35, .35); st($('seat'), Math.min(sp.o, v), 0, bob, sp.s * (1 + .06 * Math.sin(Math.PI * lin(t, C.y_you - .05, C.y_you + .5))));
  const seatTxt = t >= C.y_you - .05 ? '🙋' : '💺'; if ($('seat').textContent !== seatTxt) $('seat').textContent = seatTxt;
  const pl = rise(t, C.s_name - .2, b, 20); st($('plate'), Math.min(pl.o, v), 0, pl.y + bob, 1 + .05 * Math.sin(Math.PI * lin(t, C.s_tag - .1, C.s_tag + .5)));
  const ptxt = t >= C.s_tag - .1 ? 'Your <b>TAG Markets</b> account' : 'Booked in <b>your name</b>';
  if ($('plateT').innerHTML !== ptxt) $('plateT').innerHTML = ptxt;
  // CopyX, the route board, and its route to the driver
  const bo = rise(t, C.b_board - .1, b, -40, .45); st($('board'), Math.min(bo.o, v), 0, bo.y);
  const po = vis(t, C.b_board - .1, b, .45, .35); $('pole').style.opacity = po.toFixed(3); $('pole').style.visibility = po > .002 ? 'visible' : 'hidden';
  $('pole').style.transform = `scaleY(${ez.out(lin(t, C.b_board - .1, C.b_board + .5)).toFixed(3)})`; $('pole').style.transformOrigin = '50% 0';
  const ro = vis(t, C.b_puts - .1, b, .4, .35); $('route').style.opacity = ro.toFixed(3); $('route').style.visibility = ro > .002 ? 'visible' : 'hidden';
  $('routeP').style.strokeDashoffset = (-t * 60).toFixed(1);
  // JetUP, the association
  const of = vis(t, C.a_jet - .1, b, .45, .35); st($('office'), Math.min(of, v), 0, 30 * (1 - of), .9 + .1 * ez.back(lin(t, C.a_jet - .1, C.a_jet + .4)));
  [['o1', C.a_trains - .05], ['o2', C.a_trains + .3]].forEach(([id, c]) => { const k = ez.back(lin(t, c, c + .4)); $(id).style.display = 'inline-block'; $(id).style.opacity = lin(t, c, c + .15).toFixed(3); $(id).style.transform = `scale(${(.4 + .6 * k).toFixed(3)})`; });
  // you decide
  [['th1', C.y_which - .1], ['th2', C.y_much - .1]].forEach(([id, c]) => { const k = ez.out(lin(t, c, c + .35)); $(id).style.opacity = k.toFixed(3); $(id).style.transform = `translateX(${(-30 * (1 - k)).toFixed(1)}px)`; });
  st($('think'), Math.min(vis(t, C.y_you - .1, b, .2, .35), v));
  // the picture, row by row
  const pv = Math.min(vis(t, C.d_sonic - .35, b, .45, .35), v); st($('panel'), pv, 0, 30 * (1 - pv));
  const R = [['pr1', C.d_sonic, C.s_seat], ['pr2', C.s_seat, C.b_board], ['pr3', C.b_board, C.a_jet], ['pr4', C.a_jet, C.y_you], ['pr5', C.y_you, b + 1]];
  R.forEach(([id, c0, c1]) => {
    const el = $(id), k = ez.out(lin(t, c0 - .15, c0 + .3)); el.style.opacity = k.toFixed(3); el.style.transform = `translateX(${(36 * (1 - k)).toFixed(1)}px)`;
    el.classList.toggle('on', t >= c0 - .1 && t < c1 - .15);
  });
  const s1 = t >= C.k_track - .05 ? 'The driver · track record on Myfxbook' : 'The driver: it does the trading';
  if ($('pr1s').textContent !== s1) $('pr1s').textContent = s1;
  const s2 = t >= C.g_broker - .05 ? 'The broker: your seat, in your name' : 'Your seat, booked in your name';
  if ($('pr2s').textContent !== s2) $('pr2s').textContent = s2;
}

/* ---------- where the picture stops ---------- */
function stops(t) {
  const [a, b] = S.stops, mid = C.r88 - .3;
  const h = rise(t, a + .05, b, 30); st($('sh'), h.o, 0, h.y);
  const g = pop(t, a + .15, mid, .45, .3); st($('sign'), g.o, 0, 0, g.s * (1 + .02 * Math.sin(t * 3)));
  [['sa', C.p_taxi], ['sb', C.p_lose], ['sc', C.p_trip]].forEach(([id, c]) => { const r = rise(t, c - .15, mid, 0, .35, .3); st($(id), r.o, 40 * (1 - ez.out(lin(t, c - .15, c + .25))), 0); });
  const r2 = rise(t, mid, b, 30); st($('rk88'), r2.o, 0, r2.y);
  $('n88').textContent = Math.round(88 * ez.out(lin(t, C.r88 - .1, C.r88 + 1.0))) + '%';
  const r3 = rise(t, C.r_learn - .2, b, 30); st($('rk3'), r3.o, 0, r3.y);
}

/* ---------- let's verify, together (the signature ending takes over at "Everything I showed you") ---------- */
function next(t) {
  const [a, b] = S.next;
  const h = rise(t, a + .05, b, 40); st($('nx1'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, a + .05, a + .5)));
  const s1 = rise(t, a + .55, b, 40), s2 = rise(t, a + .95, b, 40); st($('st1'), s1.o, 0, s1.y); st($('st2'), s2.o, 0, s2.y);
}

function scenes(t) { st($('top'), vis(t, S.hi[0], TL.T + 1, .5, 0)); hook(t); hi(t); taxi(t); stops(t); next(t); }

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

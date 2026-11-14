/* JetUP explainer #10 ("Know your numbers: the Exposure Calculator"), 16:9. Every visual is a pure function of time t.
   The picture: a road map (checking the map before a road trip) that pulls back into MTG's real Exposure Calculator in a
   slim laptop; then the real page, tap by tap, with a camera (translate + scale of #cam) that frames one part at a time,
   a soft spotlight and a gold or lime box on the exact target, and big callout chips beside the screen for the key numbers.
   The screens are real screenshots (calc_shots.js), placed on one document: every shot is the same page at its own scroll,
   so a scroll is the camera moving over one page. A loss is shown the same size as the gain, in calm colours.
   The signature ending (the 9:09 sign-up training's) is composited on top after the stage render (tools/video-signature). */
(function () {
'use strict';
const TL = window.TL, S = TL.scenes, C = TL.cues, BX = window.BOXES.shots;
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const mix = (a, b, k) => a + (b - a) * k;
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
const pulse = (t, c, d = .6) => t >= c && t <= c + d ? Math.sin(Math.PI * (t - c) / d) : 0;
const NS = 'http://www.w3.org/2000/svg';
const sv = (tag, at, parent) => { const e = document.createElementNS(NS, tag); for (const k in at) e.setAttribute(k, at[k]); if (parent) parent.appendChild(e); return e; };
const sa = (e, at) => { for (const k in at) e.setAttribute(k, typeof at[k] === 'number' ? at[k].toFixed(3) : at[k]); };
function place(id, x, y) { const e = $(id); e.style.left = x + 'px'; e.style.top = y + 'px'; }
// a chip that is no longer the focal point steps back (dimmer), so one thing reads at a time
const dim = (t, later) => later.reduce((m, c) => m * (1 - .5 * ez.out(lin(t, c - .1, c + .3))), 1);
function foc(id, d) { $(id).style.filter = d > .995 ? 'none' : `brightness(${(.45 + .55 * d).toFixed(3)}) saturate(${(.55 + .45 * d).toFixed(3)})`; }

/* ---------- the document: every shot is the same page at its own scroll (page px of the 1280x800 viewport) ---------- */
const OFF = {}; for (const k in BX) OFF[k] = BX.calc.form[1] - BX[k].form[1];    // top -292, lines +263, the rest 0
const R = (shot, key, pad = 0) => { const b = BX[shot][key]; return [b[0] - pad, b[1] + OFF[shot] - pad, b[2] + 2 * pad, b[3] + 2 * pad]; };
const field = (k, pad) => { const f = R('calc', k), bx = R('calc', k + 'Box'); return [f[0] - pad, f[1] - pad, f[2] + 2 * pad, bx[1] + bx[3] - f[1] + 2 * pad]; };
const T_ = {   // tap and highlight targets in document px
  training: R('calc', 'training', 5), presets: R('calc', 'presets', 8),
  own: field('own', 10), bonus: field('bonus', 10), mult: field('mult', 10),
  slider: [BX.calc.slider[0] - 10, BX.calc.slider[1] - 62, BX.calc.slider[2] + 20, BX.calc.moveOut[1] + BX.calc.moveOut[3] - BX.calc.slider[1] + 76],
  bal: R('calc', 'bal', 4), ex: R('calc', 'ex', 4), balex: [BX.calc.bal[0] - 6, BX.calc.bal[1] - 6, BX.calc.bal[2] + 12, BX.calc.ex[1] + BX.calc.ex[3] - BX.calc.bal[1] + 12],
  pl: R('calc', 'pl', 4), eqown: R('lines', 'eqown', 4), eqbal: R('lines', 'eqbal', 4),
  two: [BX.lines.eqown[0] - 6, BX.lines.eqown[1] + OFF.lines - 6, BX.lines.eqown[2] + 12, BX.lines.eqbal[1] + BX.lines.eqbal[3] - BX.lines.eqown[1] + 12],
  note: R('note', 'note', 6), n10: R('note', 'n10', 4), n5: R('note', 'n5', 4), nLimit: R('note', 'nLimit', 4)
};
const ctr = r => [r[0] + r[2] / 2, r[1] + r[3] / 2];

/* the shots, one <img> each (a src swap could show a frame before it decodes) */
const NAMES = Object.keys(BX), IMG = {};
NAMES.forEach(n => { const i = document.createElement('img'); i.className = 'shot'; i.src = `calc/${n}.jpg`; i.alt = ''; $('shots').appendChild(i); IMG[n] = i; });

/* ---------- the scroll and the screen state ---------- */
// the page as it opens, scrolled to the calculator on "Step one", a little further for the price move (the slider mid-screen),
// then to the last two results and the loss limit note; the turn scene shows the page as it opens (the laptop is hidden in the recap)
const SCROLL = [[C.e_step - .1, .9, 0], [S.step3[0], .7, OFF.m00], [C.n_scroll, .85, OFF.lines], [C.m_scroll, .8, OFF.note], [S.recap[0] + .5, 0, OFF.top]];
function scrollAt(t) {
  let v = OFF.top;
  for (const [a, d, to] of SCROLL) { if (t < a) break; v = d ? mix(v, to, ez.inOut(lin(t, a, a + d))) : to; }
  return v;
}
// the price move slider: 0 until "One percent", +1% by "six thousand", -1% on "either direction", up on "swings",
// down on "down", then it settles back to no move before the page scrolls (all values the page itself shows)
function moveAt(t) {
  const k = [[C.d_one - .15, 0], [C.d_one + .55, 1], [C.d_either - .1, 1], [C.d_either + .75, -1], [C.s_swings - .1, -1], [C.s_swings + .45, 1],
    [C.s_down - .05, 1], [C.s_down + .5, -1], [C.n_scroll - .05, 0]];
  if (t < S.step3[0] || t >= C.n_scroll + .1 || t < k[0][0]) return 0;
  for (let i = 0; i < k.length - 1; i++) if (t < k[i + 1][0]) return mix(k[i][1], k[i + 1][1], ez.inOut(lin(t, k[i][0], k[i + 1][0])));
  return 0;
}
const moveName = v => { const q = Math.round(v * 5); return q === 0 ? 'm00' : (q > 0 ? 'mp' : 'mn') + String(Math.abs(q * 2)).padStart(2, '0'); };
// [time, shot, fade]: the shot shown from that time on (the new one under the old, the old fading out at the end of the fade)
const SEQ = [[0, 'top', 0], [C.e_step - .1, 'pre', .9], [C.e_press, 'calc', .12], [C.w_money - .12, 'f_own', .15], [C.w_bonus - .12, 'f_bonus', .15],
  [C.w_mult - .12, 'f_mult', .15], [S.step3[0], 'm00', .7], [C.n_scroll, 'lines', .85], [C.m_scroll, 'note', .8], [S.recap[0] + .5, 'top', 0]];
function shotsAt(t) {
  let cur = SEQ[0], prev = null;
  for (let i = 1; i < SEQ.length; i++) if (t >= SEQ[i][0]) { prev = SEQ[i - 1]; cur = SEQ[i]; }
  let name = cur[1];
  if (name === 'm00' && t >= S.step3[0] && t < C.n_scroll) name = moveName(moveAt(t));
  const k = prev ? lin(t, cur[0], cur[0] + cur[2]) : 1;
  let pname = prev ? prev[1] : null;
  if (pname === 'm00' && cur[1] === 'lines') pname = moveName(moveAt(cur[0]));
  return { name, pname: k < 1 ? pname : null, po: 1 - lin(k, .6, 1) };
}

/* ---------- the camera: a focal point on the screen (viewport px), a zoom (video px per page px), where it lands ---------- */
const K = .84, SX = 422.4, SY = 140, VPY = 40;                // the screen's place in the wide shot; the page starts under the address bar
const WIDE = { f: [640, 400], z: K, v: [960, SY + K * (VPY + 400)] };
const cam = (f, z, v) => ({ f, z, v });
const vpOf = (r, sc) => [r[0] + r[2] / 2, r[1] + r[3] / 2 - sc];       // a target's centre on the screen once the page is at scroll sc
const KEYS = [
  [0, 0, cam([640, 400], 1.52, [960, 540])],                                   // the map fills the frame
  [C.h_morph, 1.25, WIDE],                                                       // ... and pulls back into the laptop
  [S.step1[0] + .3, .01, WIDE],
  [C.e_step - .1, .9, cam(vpOf(T_.presets, 0), 2.6, [720, 430])],              // Step 1: the examples
  [C.e_150 - .4, .6, cam(vpOf(T_.own, 0), 2.6, [720, 470])],                   // your own $150
  [C.e_plus - .2, .6, cam(vpOf(T_.bonus, 0), 2.6, [720, 470])],               // plus the $100 bonus
  [C.x_thats - .4, .7, cam(vpOf(T_.balex, 0), 2.1, [1180, 400])],             // the balance and the exposure (chips on the left)
  [C.w_or - .2, .7, cam([325, 412], 1.75, [700, 500])],                        // Step 2: the three fields
  [C.w_money - .25, .5, cam(vpOf(T_.own, 0), 2.5, [690, 470])],
  [C.w_bonus - .25, .5, cam(vpOf(T_.bonus, 0), 2.5, [690, 470])],
  [C.w_mult - .25, .5, cam(vpOf(T_.mult, 0), 2.5, [690, 470])],
  [S.step3[0], .7, cam(vpOf(T_.slider, OFF.m00), 2.3, [650, 590])],          // Step 3: the price move (the page scrolls with it)
  [C.n_scroll, .9, cam(vpOf(T_.two, OFF.lines), 2.15, [1180, 420])],           // your lines to know (chips on the left)
  [C.m_scroll, .8, cam(vpOf(T_.note, OFF.note), 2.6, [1010, 400])],           // the loss limit note
  [S.recap[0], .01, cam(vpOf(T_.note, OFF.note), 2.6, [1010, 400])],
  [C.u_now - .3, .01, cam([640, 400], K * .58, [500, 520])]                    // your turn: the calculator, small, on the left
];
function camAt(t) {
  let c = KEYS[0][2];
  for (const [kt, d, k] of KEYS) {
    if (t < kt) break;
    const p = ez.inOut(d <= .01 ? 1 : lin(t, kt, kt + d));
    const lz = Math.exp(mix(Math.log(c.z), Math.log(k.z), p));
    c = { f: [mix(c.f[0], k.f[0], p), mix(c.f[1], k.f[1], p)], z: lz, v: [mix(c.v[0], k.v[0], p), mix(c.v[1], k.v[1], p)] };
  }
  return c;
}
let CAM = null;
// a screen point (viewport px) to video px, through the camera
function v2s(x, y) { const s = CAM.z / K, wx = SX + K * x, wy = SY + K * (VPY + y); return [CAM.tx + s * wx, CAM.ty + s * wy]; }
function scrims(t) {                                           // dark top and bottom scrims while the screen fills the frame
  const k = clamp((CAM.z - 1.1) / .6) * parseFloat($('cam').style.opacity || 0);
  ['scrimT', 'scrimB'].forEach(id => { const e = $(id); e.style.opacity = k.toFixed(3); e.style.visibility = k > .002 ? 'visible' : 'hidden'; });
}
function camera(t) {
  const c = camAt(t), s = c.z / K, wx = SX + K * c.f[0], wy = SY + K * (VPY + c.f[1]);
  CAM = { z: c.z, tx: c.v[0] - s * wx, ty: c.v[1] - s * wy };
  // the laptop leaves for Hi and the recap and returns for Step 1 and your turn
  const o = t < S.hi[0] + .45 ? 1 - ez.inOut(lin(t, S.hi[0], S.hi[0] + .45))
    : t < S.recap[0] ? ez.out(lin(t, S.step1[0], S.step1[0] + .45)) * (t < S.step1[0] ? 0 : 1)
    : t < C.u_now ? 1 - ez.inOut(lin(t, S.recap[0], S.recap[0] + .45))
    : ez.out(lin(t, C.u_now, C.u_now + .45)) * (1 - ez.inOut(lin(t, S.turn[1] - .3, S.turn[1])));
  const back = t > S.hi[0] && t < S.step1[0] + .45 ? (t < S.step1[0] ? ez.inOut(lin(t, S.hi[0], S.hi[0] + .45)) : 1 - ez.out(lin(t, S.step1[0], S.step1[0] + .45)))
    : t > S.recap[0] && t < C.u_now ? ez.inOut(lin(t, S.recap[0], S.recap[0] + .45)) : 0;
  const sb = 1 - .08 * back, cx = 960, cy = 520;              // it recedes a little as it goes
  const e = $('cam');
  e.style.opacity = o.toFixed(3); e.style.visibility = o <= .002 ? 'hidden' : 'visible';
  e.style.transform = `translate(${(cx + (CAM.tx - cx) * sb).toFixed(2)}px,${(cy + (CAM.ty - cy) * sb).toFixed(2)}px) scale(${(s * sb).toFixed(5)})`;
  CAM.tx = cx + (CAM.tx - cx) * sb; CAM.ty = cy + (CAM.ty - cy) * sb; CAM.z = CAM.z * sb;
}

/* ---------- the screen: shots, the fixed page header, the spotlight, highlight boxes, taps ---------- */
function screen(t) {
  const sc = scrollAt(t), { name, pname, po } = shotsAt(t);
  NAMES.forEach(n => {
    const i = IMG[n], on = n === name || n === pname;
    i.style.visibility = on ? 'visible' : 'hidden';
    if (!on) return;
    i.style.top = (OFF[n] - sc).toFixed(2) + 'px';
    i.style.zIndex = n === pname ? 2 : 1; i.style.opacity = n === pname ? po.toFixed(3) : '1';
  });
  return sc;
}
// the spotlight and the highlight box move from target to target: [time, target, colour, spotlight strength]
const SPOT = [
  [0, null], [C.e_tap - .1, 'training', 'lime', 1], [C.e_150 - .4, 'own', 'gold', 1], [C.e_plus - .2, 'bonus', 'gold', 1], [C.e_bonus + .6, 'bonus', 'gold', 1],
  [C.x_thats - .2, 'bal', 'lime', 1], [C.x_six - .1, 'ex', 'gold', 1], [C.o_not + 1.0, 'ex', 'gold', 1],
  [C.w_or - .2, null], [C.w_money - .15, 'own', 'lime', 1], [C.w_bonus - .15, 'bonus', 'lime', 1], [C.w_mult - .15, 'mult', 'lime', 1], [C.w_24 + 1, 'mult', 'gold', 1],
  [C.d_now - .1, null], [C.d_drag - .1, 'slider', 'lime', 1], [C.n_scroll - .1, null],
  [C.n_scroll + .3, 'two', 'lime', 1], [C.n_two - .15, 'eqown', 'gold', 1], [C.n_four - .15, 'eqbal', 'gold', 1], [C.m_scroll - .05, null],
  [C.m_loss - .15, 'note', 'lime', 1], [S.recap[0], null]];
function spotAt(t) {
  let cur = null, prev = null, i0 = -1;
  for (let i = 0; i < SPOT.length; i++) if (t >= SPOT[i][0]) { i0 = i; }
  cur = SPOT[i0]; prev = i0 > 0 ? SPOT[i0 - 1] : null;
  const k = ez.inOut(lin(t, cur[0], cur[0] + .4));
  const rc = cur[1] ? T_[cur[1]] : null, rp = prev && prev[1] ? T_[prev[1]] : null;
  if (!rc && !rp) return null;
  if (!rc) return { r: rp, col: prev[2], a: 1 - k };
  if (!rp) return { r: rc, col: cur[2], a: k };
  return { r: rc.map((v, j) => mix(rp[j], v, k)), col: k > .5 ? cur[2] : prev[2], a: 1 };
}
function overlays(t, sc) {
  const sp = spotAt(t), spot = $('spot'), hl = $('hl');
  if (sp && sp.a > .002 && t >= S.step1[0] && t < S.recap[0] + .3) {
    const [x, y, w, h] = sp.r;
    [spot, hl].forEach(e => { e.style.left = x + 'px'; e.style.top = (y - sc) + 'px'; e.style.width = w + 'px'; e.style.height = h + 'px'; e.style.visibility = 'visible'; });
    spot.style.opacity = (sp.a * .95).toFixed(3); hl.style.opacity = sp.a.toFixed(3); hl.className = sp.col === 'lime' ? 'lime' : '';
  } else { spot.style.visibility = hl.style.visibility = 'hidden'; }
  // the two figures in the loss limit note, each boxed on its word
  const h2 = $('hl2'); let r2 = null, a2 = 0;
  if (t >= C.m_ten - .1 && t < S.recap[0]) { const k = ez.inOut(lin(t, C.m_five - .1, C.m_five + .3)); r2 = T_.n10.map((v, j) => mix(v, T_.n5[j], k)); a2 = ez.out(lin(t, C.m_ten - .1, C.m_ten + .2)) * (1 - lin(t, S.recap[0] - .3, S.recap[0])); }
  if (r2) { h2.style.left = r2[0] + 'px'; h2.style.top = (r2[1] - sc) + 'px'; h2.style.width = r2[2] + 'px'; h2.style.height = r2[3] + 'px'; h2.style.opacity = a2.toFixed(3); h2.style.visibility = 'visible'; }
  else h2.style.visibility = 'hidden';
  // the tap on "Training: $150 + $100" (hand and ring), on "tap an example"
  // the tap lands on the right of the button, so "$150 + $100" stays readable under the finger
  const tp = [T_.training[0] + T_.training[2] * .8, T_.training[1] + T_.training[3] * .62], hand = $('hand'), ring = $('ring');
  const sl = BX.calc.slider, mv = moveAt(t), th = [sl[0] + 8 + (sl[2] - 16) * (mv + 10) / 20, sl[1] + sl[3] / 2];
  if (t < S.step3[0]) {
    const hk = ez.out(lin(t, C.e_tap - .25, C.e_press)), hv = vis(t, C.e_tap - .25, C.e_press + .7, .2, .3);
    hand.style.left = (tp[0] - 18) + 'px'; hand.style.top = (tp[1] - 3 - sc) + 'px';
    hand.style.opacity = hv.toFixed(3); hand.style.visibility = hv > .002 ? 'visible' : 'hidden';
    hand.style.transform = `translate(${(90 * (1 - hk)).toFixed(1)}px,${(t > C.e_press - .04 && t < C.e_press + .14 ? 4 : 60 * (1 - hk)).toFixed(1)}px)`;
  } else {                                                      // the finger holds the thumb from "drag" until the slider settles
    const hk = ez.out(lin(t, C.d_drag - .3, C.d_drag + .1)), hv = vis(t, C.d_drag - .3, C.n_scroll - .1, .2, .3);
    hand.style.left = (th[0] - 18) + 'px'; hand.style.top = (th[1] + 12 - sc) + 'px';
    hand.style.opacity = hv.toFixed(3); hand.style.visibility = hv > .002 ? 'visible' : 'hidden';
    hand.style.transform = `translate(${(40 * (1 - hk)).toFixed(1)}px,${(60 * (1 - hk)).toFixed(1)}px)`;
  }
  const rk = lin(t, C.e_press, C.e_press + .6);
  ring.style.left = tp[0] + 'px'; ring.style.top = (tp[1] - sc) + 'px';
  ring.style.visibility = t >= C.e_press && rk < 1 ? 'visible' : 'hidden'; ring.style.opacity = (.95 * (1 - rk)).toFixed(3);
  ring.style.transform = `scale(${(.4 + 1.4 * ez.out(rk)).toFixed(3)})`;
  // the slider's thumb: a lime ring while it is dragged
  const tr = $('thumbRing');
  const tv = vis(t, C.d_drag, C.n_scroll - .05, .3, .25);
  tr.style.left = th[0] + 'px'; tr.style.top = (th[1] - sc) + 'px';
  tr.style.opacity = tv.toFixed(3); tr.style.visibility = tv > .002 ? 'visible' : 'hidden';
  tr.style.transform = `scale(${(1 + .25 * pulse(t, C.d_drag + .1, .5)).toFixed(3)})`;
}

/* ---------- hook: the road map, the glowing route, the pin "Your numbers" ---------- */
const MAP = $('mapSvg');
MAP.innerHTML = `<defs>
 <radialGradient id="mBg" cx=".55" cy=".45" r=".8"><stop offset="0" stop-color="#21173d"/><stop offset=".6" stop-color="#160f2b"/><stop offset="1" stop-color="#0c0819"/></radialGradient>
 <linearGradient id="mWater" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1f2a5c"/><stop offset="1" stop-color="#16204a"/></linearGradient>
 <radialGradient id="mPark" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#2c4a2a"/><stop offset="1" stop-color="#1c3220"/></radialGradient>
 <linearGradient id="mGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1bf"/><stop offset=".45" stop-color="#e8c25a"/><stop offset="1" stop-color="#a8792a"/></linearGradient>
 <radialGradient id="mGlow"><stop offset="0" stop-color="#ffe08f" stop-opacity=".8"/><stop offset=".5" stop-color="#e8c25a" stop-opacity=".25"/><stop offset="1" stop-color="#e8c25a" stop-opacity="0"/></radialGradient>
 <radialGradient id="mLimeGlow"><stop offset="0" stop-color="#cbfb61" stop-opacity=".85"/><stop offset=".5" stop-color="#cbfb61" stop-opacity=".25"/><stop offset="1" stop-color="#cbfb61" stop-opacity="0"/></radialGradient>
 <filter id="mBlur6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
 <filter id="mShadow" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity=".5"/></filter>
 <pattern id="mGrid" width="46" height="46" patternUnits="userSpaceOnUse" patternTransform="rotate(-14)"><path d="M 46 0 L 0 0 0 46" fill="none" stroke="rgba(255,255,255,.055)" stroke-width="2"/></pattern></defs>
 <rect width="1280" height="800" fill="url(#mBg)"/>
 <path d="M -20 610 C 160 560 260 640 420 600 S 640 470 760 520 S 980 640 1300 560 L 1300 820 L -20 820 Z" fill="url(#mWater)" opacity=".75"/>
 <path d="M -20 640 C 160 590 260 670 420 630 S 640 500 760 550 S 980 670 1300 590" fill="none" stroke="rgba(150,170,255,.18)" stroke-width="3"/>
 <rect width="1280" height="800" fill="url(#mGrid)"/>
 <ellipse cx="300" cy="300" rx="130" ry="80" fill="url(#mPark)" opacity=".7" transform="rotate(-14 300 300)"/>
 <ellipse cx="960" cy="180" rx="110" ry="64" fill="url(#mPark)" opacity=".6" transform="rotate(-14 960 180)"/>
 <ellipse cx="760" cy="380" rx="70" ry="44" fill="url(#mPark)" opacity=".55" transform="rotate(-14 760 380)"/>
 <g id="mRoads" fill="none" stroke-linecap="round" stroke-linejoin="round"></g>
 <g id="mRoute"></g><g id="mMarks"></g><g id="mPins"></g>
 <g id="mCompass" transform="translate(1196 548)"></g>`;
const ROADS = ['M -20 470 C 200 450 330 520 520 500 S 860 380 1300 400', 'M 120 820 C 160 640 120 470 210 330 S 260 120 230 -20',
  'M 560 820 C 540 660 600 560 640 420 S 700 200 760 -20', 'M -20 210 C 260 230 480 160 720 190 S 1060 280 1300 240',
  'M 980 820 C 1000 680 940 560 1000 440 S 1100 260 1120 -20', 'M 330 820 C 420 700 520 690 600 600'];
ROADS.forEach((d, i) => { sv('path', { d, stroke: 'rgba(10,6,22,.9)', 'stroke-width': i < 5 ? 22 : 16 }, $('mRoads')); sv('path', { d, stroke: 'rgba(214,204,246,.30)', 'stroke-width': i < 5 ? 14 : 9 }, $('mRoads')); });
const ROUTE = 'M 230 640 C 300 590 340 560 460 540 S 640 520 700 450 S 800 345 900 348 S 985 352 1000 336';
const rGlow = sv('path', { d: ROUTE, fill: 'none', stroke: '#cbfb61', 'stroke-width': 26, 'stroke-linecap': 'round', opacity: .35, filter: 'url(#mBlur6)' }, $('mRoute'));
const rDark = sv('path', { d: ROUTE, fill: 'none', stroke: '#14190a', 'stroke-width': 15, 'stroke-linecap': 'round', opacity: .7 }, $('mRoute'));
const rLine = sv('path', { d: ROUTE, fill: 'none', stroke: '#cbfb61', 'stroke-width': 9, 'stroke-linecap': 'round' }, $('mRoute'));
const RLEN = rLine.getTotalLength();
[rGlow, rDark, rLine].forEach(p => sa(p, { 'stroke-dasharray': `${RLEN} ${RLEN}` }));
const marks = [.25, .5, .75].map(f => { const p = rLine.getPointAtLength(RLEN * f); const g = sv('g', { transform: `translate(${p.x} ${p.y})`, opacity: 0 }, $('mMarks'));
  sv('circle', { r: 11, fill: '#14190a', stroke: '#cbfb61', 'stroke-width': 4 }, g); return { g, f }; });
// the start (you) and the pin: your numbers
const startG = sv('g', { transform: 'translate(230 640)', opacity: 0 }, $('mPins'));
sv('circle', { r: 40, fill: 'url(#mLimeGlow)' }, startG); sv('circle', { r: 17, fill: '#cbfb61', stroke: '#14190a', 'stroke-width': 5 }, startG);
const pinG = sv('g', { opacity: 0 }, $('mPins'));
const pinGlow = sv('ellipse', { cx: 0, cy: 0, rx: 70, ry: 26, fill: 'url(#mGlow)' }, pinG);
const pinBody = sv('g', { filter: 'url(#mShadow)' }, pinG);
sv('path', { d: 'M 0 0 C -10 -26 -44 -50 -44 -86 A 44 44 0 1 1 44 -86 C 44 -50 10 -26 0 0 Z', fill: 'url(#mGold)', stroke: '#8e6420', 'stroke-width': 3 }, pinBody);
sv('circle', { cx: 0, cy: -88, r: 18, fill: '#1a1405' }, pinBody);
const pinCard = sv('g', { opacity: 0 }, pinG);
sv('rect', { x: -168, y: -224, width: 336, height: 76, rx: 38, fill: 'rgba(21,17,42,.95)', stroke: '#ffe08f', 'stroke-width': 3 }, pinCard);
sv('text', { x: 0, y: -173, 'text-anchor': 'middle', fill: '#fff', style: 'font:800 38px Manrope' }, pinCard).textContent = 'Your numbers';
const PIN = [1000, 336];                                      // under the top bar and its chip, clear of the title
// a small gold compass, the map's own
(() => { const g = $('mCompass'); sv('circle', { r: 48, fill: 'rgba(21,17,42,.85)', stroke: 'rgba(255,224,143,.6)', 'stroke-width': 3 }, g);
  sv('path', { d: 'M 0 -38 L 9 0 L 0 38 L -9 0 Z', fill: 'url(#mGold)' }, g); sv('path', { d: 'M -38 0 L 0 -7 L 38 0 L 0 7 Z', fill: 'rgba(214,204,246,.55)' }, g);
  sv('text', { x: 0, y: -54, 'text-anchor': 'middle', fill: '#ffe08f', style: 'font:800 22px Manrope' }, g).textContent = 'N'; })();
const HKW = [...$('hkT').querySelectorAll('span')];
function hook(t) {
  const [a, b] = S.hook;
  // the map: the route draws from you to the pin on "checking the map before a road trip"; the pin drops on "road trip"
  const mapO = 1 - ez.inOut(lin(t, C.h_morph + .35, C.h_morph + 1.15));
  const m = $('map'); m.style.opacity = mapO.toFixed(3); m.style.visibility = mapO > .002 && t < S.hi[1] ? 'visible' : 'hidden';
  op(startG, 1);
  const dr = ez.inOut(lin(t, C.h_like, C.h_trip_end - .1));
  [rGlow, rDark, rLine].forEach(p => sa(p, { 'stroke-dashoffset': RLEN * (1 - dr) }));
  sa(rGlow, { opacity: .35 + .2 * Math.sin(t * 3) });
  marks.forEach(mk => op(mk.g, ez.out(lin(t, C.h_like + mk.f * (C.h_trip_end - .1 - C.h_like), C.h_like + mk.f * (C.h_trip_end - .1 - C.h_like) + .2))));
  const pk = lin(t, C.h_road - .15, C.h_road + .35);
  op(pinG, ez.out(lin(t, C.h_road - .15, C.h_road)));
  sa(pinBody, { transform: `translate(0 ${(-120 * (1 - ez.back(pk))).toFixed(1)}) scale(${(.6 + .4 * ez.back(pk)).toFixed(3)})` });
  sa(pinG, { transform: `translate(${PIN[0]} ${PIN[1]})` });
  sa(pinGlow, { rx: 70 + 10 * Math.sin(t * 3), opacity: .6 + .4 * pulse(t, C.h_trip_end, .8) });
  op(pinCard, ez.out(lin(t, C.h_trip_end - .1, C.h_trip_end + .3)));
  sa(pinCard, { transform: `translate(0 ${(16 * (1 - ez.out(lin(t, C.h_trip_end - .1, C.h_trip_end + .3)))).toFixed(1)})` });
  // the title lights word by word on "know your numbers"; it leaves as the map pulls back into the laptop
  const v = t < C.h_morph + .5 ? 1 - ez.inOut(lin(t, C.h_morph + .05, C.h_morph + .5)) : 0;
  st($('hkT'), v, 0, -30 * ez.inOut(lin(t, C.h_morph, C.h_morph + .5)));
  [C.h_know, C.h_your, C.h_numbers].forEach((c, i) => {
    const w = HKW[i]; w.classList.toggle('lit', t >= c - .04);
    w.style.transform = `translateY(${(-10 * pulse(t, c - .04, .3)).toFixed(1)}px) scale(${(1 + .05 * pulse(t, c - .04, .3)).toFixed(3)})`;
  });
}
const op = (e, o) => e.setAttribute('opacity', clamp(o).toFixed(3));

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi, e = b - .3;
  const d = pop(t, a + .15, e, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .4, e, 24), r = rise(t, a + .65, e, 30); st($('hwho'), h.o, 0, h.y); st($('httl'), r.o, 0, r.y);
}

/* ---------- the step pill, in the top bar ---------- */
function steps(t) {
  [['st1', S.step1], ['stR', S.read], ['st2', S.step2], ['st3', S.step3], ['stL', S.lines]].forEach(([id, [a, b]]) => {
    const k = pop(t, a + .25, b + .15, .35, .25); st($(id), k.o, 0, 0, k.s);
  });
}

/* ---------- the callout chips ---------- */
function chips(t) {
  // step 1: $150 your own, + $100 bonus
  place('c150', 1390, 330); const a = pop(t, C.e_150 - .05, S.step1[1] + .1); st($('c150'), a.o, 0, 0, a.s); foc('c150', dim(t, [C.e_100]));
  place('c100', 1390, 530); const b = pop(t, C.e_100 - .05, S.step1[1] + .1); st($('c100'), b.o, 0, 0, b.s);
  // read your exposure: $250, $6,000; the size you trade with, not money you own
  place('cBal', 90, 236); const c = pop(t, C.x_thats - .05, S.read[1] + .1); st($('cBal'), c.o, 0, 0, c.s); foc('cBal', dim(t, [C.x_six]));
  place('cEx', 90, 430); const d = pop(t, C.x_six - .05, S.read[1] + .1); st($('cEx'), d.o, 0, 0, d.s * (1 + .03 * pulse(t, C.x_six + .3, .5)));
  place('cExpo', 560, 596); const e = rise(t, C.o_exposure - .05, S.read[1] + .1, 24); st($('cExpo'), e.o, 0, e.y);
  const sm = $('cExpo').querySelector('small'), smk = ez.out(lin(t, C.o_not - .1, C.o_not + .3));
  sm.style.opacity = smk.toFixed(3); sm.style.maxHeight = (46 * smk).toFixed(1) + 'px'; sm.style.marginTop = (-8 * (1 - smk)).toFixed(1) + 'px';
  // step 2: your own numbers, ticked on his words
  const o = rise(t, C.w_type - .1, S.step2[1] + .1, 30); st($('own3'), o.o, 0, o.y);
  [['o1', C.w_money], ['o2', C.w_bonus], ['o3', C.w_mult]].forEach(([id, cc]) => {
    const el = $(id), k = ez.out(lin(t, cc - .15, cc + .3));
    el.style.opacity = (.22 + .78 * k).toFixed(3); el.querySelector('.ok').style.transform = `scale(${ez.back(lin(t, cc, cc + .35)).toFixed(3)})`;
  });
  const x = ez.out(lin(t, C.w_24 - .1, C.w_24 + .3)); $('x24').style.opacity = x.toFixed(3);
  $('o3').style.transform = `scale(${(1 + .04 * pulse(t, C.w_24, .5)).toFixed(3)})`; $('o3').style.transformOrigin = '0 50%';
  // step 3: the profit or loss row, magnified, under the top bar; $60; same size, both ways
  lens(t);
  place('c60', 1250, 400); const f = pop(t, C.d_sixty - .1, S.step3[1] + .1); st($('c60'), f.o, 0, 0, f.s); foc('c60', dim(t, [C.d_either]));
  place('both', 1250, 590); const g = rise(t, C.d_either - .1, S.step3[1] + .1, 30); st($('both'), g.o, 0, g.y);
  const up = ez.inOut(lin(t, C.d_either - .05, C.d_either + .5)), dn = ez.inOut(lin(t, C.d_either + .25, C.d_either + .8));
  $('barUp').querySelector('i').style.width = (100 * up).toFixed(1) + '%'; $('barDn').querySelector('i').style.width = (100 * dn).toFixed(1) + '%';
  const mv = moveAt(t);                                         // the bar that matches the slider's side glows while it is there
  $('barUp').style.filter = mv > .5 && t > C.s_bigger ? 'drop-shadow(0 0 14px rgba(203,251,97,.8))' : 'none';
  $('barDn').style.filter = mv < -.5 && t > C.s_bigger ? 'drop-shadow(0 0 14px rgba(201,184,255,.8))' : 'none';
  // your lines to know: 2.5%, 4.17%; then the loss limit note: 10%, 5%
  place('c25', 80, 262); const h = pop(t, C.n_two - .1, C.m_scroll + .2); st($('c25'), h.o, 0, 0, h.s); foc('c25', dim(t, [C.n_four]));
  place('c417', 80, 446); const i = pop(t, C.n_four - .1, C.m_scroll + .2); st($('c417'), i.o, 0, 0, i.s);
  place('c10', 330, 600); const j = pop(t, C.m_ten - .1, S.lines[1] + .1); st($('c10'), j.o, 0, 0, j.s); foc('c10', dim(t, [C.m_five]));
  place('c5', 1010, 600); const k = pop(t, C.m_five - .1, S.lines[1] + .1); st($('c5'), k.o, 0, 0, k.s);
}
// the lens: the same real screen (whichever slider frame is showing), the profit or loss row magnified, linked to its row
const LZ = 2.3, LENS = $('lens'), LIMG = {};
['m00', 'mp02', 'mp04', 'mp06', 'mp08', 'mp10', 'mn02', 'mn04', 'mn06', 'mn08', 'mn10'].forEach(n => {
  const i = document.createElement('img'); i.src = `calc/${n}.jpg`; i.alt = ''; i.style.width = (1280 * LZ) + 'px'; i.style.height = (800 * LZ) + 'px';
  i.style.left = (-(T_.pl[0]) * LZ) + 'px'; i.style.top = (-(T_.pl[1] - OFF[n]) * LZ) + 'px'; LENS.appendChild(i); LIMG[n] = i; });
const LL = $('lensLead'), llP = sv('path', { fill: 'none', stroke: '#ffe08f', 'stroke-width': 3, 'stroke-dasharray': '2 9', 'stroke-linecap': 'round' }, LL);
function lens(t) {
  const v = rise(t, C.d_drag + .2, C.n_scroll + .1, 24, .4, .3);
  LENS.style.width = (T_.pl[2] * LZ) + 'px'; LENS.style.height = (T_.pl[3] * LZ) + 'px';
  st(LENS, v.o, 0, v.y);
  const n = moveName(moveAt(t)); Object.entries(LIMG).forEach(([k, i]) => i.style.visibility = k === n && v.o > .002 ? 'visible' : 'hidden');
  LENS.style.boxShadow = `0 0 0 3px #ffe08f,0 0 ${(40 + 30 * pulse(t, C.d_sixty, .7)).toFixed(0)}px rgba(232,194,90,${(.45 + .3 * pulse(t, C.d_sixty, .7)).toFixed(2)}),0 24px 60px rgba(0,0,0,.6)`;
}

/* ---------- recap: four ticked cards, on his words ---------- */
function recap(t) {
  const [a, b] = S.recap;
  const ti = rise(t, C.rc_so - .1, b, 30, .45, .3); st($('rtt'), ti.o, 0, ti.y);
  [['rc1', C.rc_tap], ['rc2', C.rc_read], ['rc3', C.rc_drag], ['rc4', C.rc_know]].forEach(([id, c], i) => {
    const v = rise(t, C.rc_so + .1 + i * .08, b, 40, .45, .3), k = ez.out(lin(t, c - .15, c + .3));
    st($(id), v.o * (.35 + .65 * k), 0, v.y, 1 + .03 * pulse(t, c, .45));
    $(id).querySelector('.ok').style.transform = `scale(${ez.back(lin(t, c, c + .35)).toFixed(3)})`;
    $(id).querySelector('.ok').style.opacity = (t >= c ? 1 : 0).toString();
  });
}

/* ---------- now it's your turn: open the calculator, tap any Join JetUP button ---------- */
function turn(t) {
  const [a, b] = S.turn, tt = C.i_press;
  const h = rise(t, C.u_now - .02, b, 40); st($('ut'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, C.u_now - .02, C.u_now + .45)));   // once the recap has gone
  const o = pop(t, C.u_turn - .1, b, .4, .3); st($('uopen'), o.o, 0, 0, o.s * (1 + .015 * Math.sin(t * 4)));
  const press = t > tt - .04 && t < tt + .16 ? .95 : 1;
  const j = pop(t, C.u_turn + .1, b, .4, .3); st($('ujoin'), j.o, 0, 0, j.s * press * (1 + .02 * Math.sin(t * 4 + 1)));
  const u = rise(t, C.i_url - .3, b, 30); st($('uurl'), u.o, 0, u.y, 1 + .04 * pulse(t, C.i_url, .6));
  const hk = ez.out(lin(t, C.i_join - .45, tt)), hv = vis(t, C.i_join - .45, b, .25, .3);
  st($('uhand'), hv, 320 * (1 - hk), (t > tt - .04 && t < tt + .16 ? 10 : 0));
  const rk = lin(t, tt, tt + .65); $('uring').style.opacity = (t >= tt && t <= tt + .65 ? .9 * (1 - rk) : 0).toFixed(3);
  $('uring').style.visibility = t >= tt && t <= tt + .65 ? 'visible' : 'hidden'; $('uring').style.transform = `scale(${(.4 + 1.6 * ez.out(rk)).toFixed(3)})`;
}

function scenes(t) {
  st($('top'), vis(t, 0, TL.T + 1, 0, 0));
  camera(t); scrims(t); const sc = screen(t); overlays(t, sc);
  hook(t); hi(t); steps(t); chips(t); recap(t); turn(t);
}

/* ---------- captions: the current line, the spoken word lit ---------- */
const capbox = $('capbox'); let lastCap = null;
const capHTML = c => c.w.map((w, i) => `<span>${w.w}</span>` + (i === c.w.length - 1 ? '' : i === c.br ? '<br>' : ' ')).join('');
function captions(t) {
  const c = TL.caps.find(c => t >= c.a && t < c.b);
  if (!c || (TL.capoff && t >= TL.capoff)) { capbox.style.visibility = 'hidden'; lastCap = null; return; }
  if (c !== lastCap) { capbox.innerHTML = capHTML(c); lastCap = c; }
  const sp = capbox.querySelectorAll('span');
  c.w.forEach((w, i) => { const end = c.w[i + 1] ? c.w[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  capbox.style.visibility = 'visible'; capbox.style.opacity = Math.min(lin(t, c.a, c.a + .12), 1 - lin(t, c.b - .12, c.b)).toFixed(3);
}

/* ---------- emoji pops on key words, as in the sign-up training ---------- */
const emoEl = document.createElement('div'); emoEl.id = 'emo';
emoEl.style.cssText = 'position:absolute;left:0;top:0;width:112px;height:112px;border-radius:50%;font:66px/112px "Noto Color Emoji";text-align:center;visibility:hidden;transform-origin:100% 100%;z-index:60;background:#15112a;box-shadow:inset 0 0 0 2.5px rgba(203,251,97,.85),0 0 30px rgba(203,251,97,.28),0 16px 34px rgba(0,0,0,.5)';
document.body.appendChild(emoEl);
function emojis(t) {
  let E = null, end = 0;
  for (const e of (TL.emos || [])) {
    const c = TL.caps.find(c => e[0] >= c.a && e[0] < c.b), en = Math.min(e[0] + 2, c ? c.b : e[0] + 2);
    if (t >= e[0] && t < en) { E = e; end = en; }
  }
  if (!E || capbox.style.visibility !== 'visible' || (TL.kit && t >= TL.kit[0])) { emoEl.style.visibility = 'hidden'; return; }
  const age = t - E[0]; if (emoEl.textContent !== E[1]) emoEl.textContent = E[1];
  const a = Math.min(1, age / .15) * Math.min(1, (end - t) / .3), s = .4 + .6 * ez.back(clamp(age / .4)); const r = capbox.getBoundingClientRect();
  emoEl.style.left = (r.right - 112).toFixed(1) + 'px'; emoEl.style.top = (r.top - 112 - 8 - 8 * ez.out(clamp(age / 2))).toFixed(1) + 'px';
  emoEl.style.transform = `scale(${s.toFixed(3)})`; emoEl.style.opacity = a.toFixed(3); emoEl.style.visibility = 'visible';
}

/* QA helper: every caption on the lines it was planned for (one, or two at its break), never more than two */
window.capLines = function () {
  const out = []; const lh = parseFloat(getComputedStyle(capbox).lineHeight);
  capbox.style.visibility = 'hidden';
  TL.caps.forEach(c => { capbox.innerHTML = capHTML(c); const n = Math.round((capbox.clientHeight - 30) / lh), want = c.br === undefined ? 1 : 2;
    if (n !== want) out.push([c.a, n, want, c.w.map(w => w.w).join(' ')]); });
  lastCap = null; return out;
};
window.R = function (t) { scenes(t); captions(t); emojis(t); return Promise.all([...document.images].map(i => i.decode().catch(() => {}))); };
})();

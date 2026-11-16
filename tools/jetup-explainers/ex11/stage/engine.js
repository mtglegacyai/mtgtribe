/* JetUP explainer #11 ("The Infinity Bonus: two strong wheels"), 16:9. Every visual is a pure function of time t.
   The picture: explainer #6's ten glass floors light and the top opens upward to an infinity sign; ten 1.5% Profit Share
   level bars with a lime Infinity layer settling on top and running past level 10; then ONE bicycle that stays and grows:
   its gear cassette is JetUP's Infinity scale (the chain climbs a gear on each number), its handlebar trip meter counts the
   month's new volume and resets on a calendar flip, its two wheels are two lines (the strongest capped at half: the 50%
   rule), and a partner in your line rides their own bicycle in a lower gear (the difference rule). JetUP's figures only:
   no example incomes, no promises, no warnings. The signature ending is composited on top after the stage render. */
(function () {
'use strict';
const TL = window.TL, S = TL.scenes, C = TL.cues;
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
const op = (e, o) => { const v = clamp(o); e.setAttribute('opacity', v.toFixed(3)); e.style.visibility = v <= .002 ? 'hidden' : 'visible'; };
const mk = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
function place(id, x, y) { const e = $(id); e.style.left = x.toFixed(1) + 'px'; e.style.top = y.toFixed(1) + 'px'; }
function foc(el, d) { el.style.filter = d > .995 ? 'none' : `brightness(${(.45 + .55 * d).toFixed(3)}) saturate(${(.55 + .45 * d).toFixed(3)})`; }

/* ---------- JetUP's Infinity scale (business plan, Oct 2026): the team's new volume in a calendar month sets the rate ---------- */
const THR = [50e3, 200e3, 500e3, 1e6, 3e6, 7.5e6, 15e6, 25e6, 40e6];
const THL = ['$50K', '$200K', '$500K', '$1M', '$3M', '$7.5M', '$15M', '$25M', '$40M'];
const RATE = ['1.5%', '3%', '4%', '5%', '5.5%', '6%', '6.5%', '7%', '7.5%'];
const fmt = v => v < 500 ? '$0' : v < 1e6 ? '$' + Math.round(v / 1e3) + 'K' : '$' + (v < 1e7 ? (Math.round(v / 1e5) / 10).toString() : Math.round(v / 1e6).toString()) + 'M';
const gearOf = v => { let g = -1; THR.forEach((x, i) => { if (v >= x - 1) g = i; }); return g; };
const geo = (a, b, k) => Math.exp(mix(Math.log(Math.max(a, 1)), Math.log(Math.max(b, 1)), k));

/* the fills of the two wheels in Rule 1 (fractions of the $1M example's ring): the strongest line fills past half, only
   half of it counts (the rest turns grey on "at most half"); all other lines fill the other half, in full */
const rearFill = t => .8 * ez.inOut(lin(t, C.f_strongest - .1, C.f_counts + .45));
const frontFill = t => .5 * ez.inOut(lin(t, C.f_two - .15, C.f_wheels + .4));
const capK = t => ez.out(lin(t, C.f_most - .1, C.f_half + .2));          // the part past half greys out, the cap lights
/* the trip meter: the team's new volume this month (counted volume) */
function meter(t) {
  if (t < S.month[0] + .2) {
    if (t < C.b_team - .1) return 0;
    if (t < C.b_climb[0] + .05) return 50e3 * ez.out(lin(t, C.b_team - .1, C.b_climb[0] + .05));
    let v = THR[0];
    for (let i = 1; i < 9; i++) { if (t < C.b_climb[i]) break; v = THR[i]; }      // one gear, one threshold at a time
    return v;
  }
  if (t < C.m_resets + .5) return t < C.m_resets - .05 ? THR[8] : geo(THR[8], 1, ez.inOut(lin(t, C.m_resets - .05, C.m_resets + .45))) * (t > C.m_resets + .4 ? 0 : 1);
  if (t < S.fifty[0]) return 0;
  return 1e6 * (Math.min(rearFill(t), .5) + frontFill(t));
}
// the gear is the meter's (labels and meter always agree); only the chain ring glides to a new gear in 0.1 s
const gearAt = t => gearOf(meter(t));
const chainAt = t => {
  const g = gearAt(t);
  for (let k = 1; k <= 5; k++) { const gp = gearAt(t - k * .02); if (gp !== g) return gp < 0 || g < 0 ? g : mix(gp, g, ez.out((k - .5) / 5.5)); }
  return g;
};

/* ---------- defs: the materials ---------- */
const ART = $('art');
ART.innerHTML = `<defs>
 <linearGradient id="gFrame" gradientUnits="userSpaceOnUse" x1="0" y1="-270" x2="40" y2="40"><stop offset="0" stop-color="#d9ccff"/><stop offset=".35" stop-color="#9b7cff"/><stop offset=".75" stop-color="#5b3cd0"/><stop offset="1" stop-color="#3a2490"/></linearGradient>
 <linearGradient id="gFrame2" gradientUnits="userSpaceOnUse" x1="0" y1="-270" x2="40" y2="40"><stop offset="0" stop-color="#fff1bf"/><stop offset=".4" stop-color="#e8c25a"/><stop offset=".8" stop-color="#a8792a"/><stop offset="1" stop-color="#7d5a1d"/></linearGradient>
 <linearGradient id="gRider" gradientUnits="userSpaceOnUse" x1="0" y1="-620" x2="120" y2="40"><stop offset="0" stop-color="#efe8ff"/><stop offset=".5" stop-color="#c9b8ff"/><stop offset="1" stop-color="#8f78e6"/></linearGradient>
 <linearGradient id="gRiderD" gradientUnits="userSpaceOnUse" x1="0" y1="-400" x2="0" y2="40"><stop offset="0" stop-color="#8a74d8"/><stop offset="1" stop-color="#5a46a8"/></linearGradient>
 <linearGradient id="gRider2" gradientUnits="userSpaceOnUse" x1="0" y1="-620" x2="120" y2="40"><stop offset="0" stop-color="#f3ffd8"/><stop offset=".5" stop-color="#d8f59a"/><stop offset="1" stop-color="#9fcf45"/></linearGradient>
 <linearGradient id="gRider2D" gradientUnits="userSpaceOnUse" x1="0" y1="-400" x2="0" y2="40"><stop offset="0" stop-color="#93b84a"/><stop offset="1" stop-color="#5f7f25"/></linearGradient>
 <linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1bf"/><stop offset=".45" stop-color="#e8c25a"/><stop offset="1" stop-color="#a8792a"/></linearGradient>
 <linearGradient id="gGoldU" gradientUnits="userSpaceOnUse" x1="0" y1="-200" x2="0" y2="200"><stop offset="0" stop-color="#fff1bf"/><stop offset=".5" stop-color="#e8c25a"/><stop offset="1" stop-color="#a8792a"/></linearGradient>
 <linearGradient id="gChrome" gradientUnits="userSpaceOnUse" x1="-50" y1="-50" x2="50" y2="50"><stop offset="0" stop-color="#f4f1ff"/><stop offset=".5" stop-color="#9c95b8"/><stop offset="1" stop-color="#e2ddf4"/></linearGradient>
 <linearGradient id="gTire" gradientUnits="userSpaceOnUse" x1="0" y1="-200" x2="0" y2="200"><stop offset="0" stop-color="#3a3452"/><stop offset=".5" stop-color="#16121f"/><stop offset="1" stop-color="#2b2640"/></linearGradient>
 <linearGradient id="gSaddle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4166"/><stop offset="1" stop-color="#15111f"/></linearGradient>
 <radialGradient id="gShadow"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
 <radialGradient id="gHalo"><stop offset="0" stop-color="#ffe08f" stop-opacity=".45"/><stop offset=".6" stop-color="#e8c25a" stop-opacity=".12"/><stop offset="1" stop-color="#e8c25a" stop-opacity="0"/></radialGradient>
 <linearGradient id="gBar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f74f0" stop-opacity=".75"/><stop offset=".55" stop-color="#4a33a8" stop-opacity=".7"/><stop offset="1" stop-color="#231a4a" stop-opacity=".85"/></linearGradient>
 <linearGradient id="gBand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e4ff9a"/><stop offset=".8" stop-color="#cbfb61"/><stop offset="1" stop-color="#cbfb61" stop-opacity="0"/></linearGradient>
 <linearGradient id="gBeam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffe08f" stop-opacity=".0"/><stop offset=".35" stop-color="#ffe08f" stop-opacity=".45"/><stop offset="1" stop-color="#cbfb61" stop-opacity=".0"/></linearGradient>
 <linearGradient id="gInf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cbfb61"/><stop offset=".5" stop-color="#fff1bf"/><stop offset="1" stop-color="#e8c25a"/></linearGradient>
 <linearGradient id="gSprk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f1ff"/><stop offset=".5" stop-color="#a59ec2"/><stop offset="1" stop-color="#5e5878"/></linearGradient>
 <filter id="fGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="fGlowS" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="fDrop" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="16" stdDeviation="14" flood-color="#000" flood-opacity=".5"/></filter>
</defs><g id="gHook"></g><g id="gPS"></g><g id="gLinks"></g><g id="gBikes"></g>`;

/* ---------- hook: ten glass floors (explainer #6), the top opens upward to an infinity sign ---------- */
function makeStack(host, cx, cy1, pw, sp) {
  const P = [], Lb = [], G = [];
  for (let i = 0; i < 10; i++) {
    const p = mk('div', 'pl', '<span class="on"></span>'); const cy = cy1 - i * sp;
    p.style.cssText = `left:${cx - pw / 2}px;top:${cy - pw / 2}px;width:${pw}px;height:${pw}px;z-index:${10 + i}`;
    const l = mk('div', 'fl', `<b>${i + 1}</b>`); l.style.cssText = `left:${cx + pw * .7071 + 6}px;top:${cy}px;z-index:30`;
    host.appendChild(p); host.appendChild(l); P.push(p); Lb.push(l);
  }
  for (let j = 0; j < 3; j++) {                                  // the floors above the top: no ceiling
    const p = mk('div', 'pl gh'); p.style.cssText = `left:${cx - pw / 2}px;top:${cy1 - 9 * sp - pw / 2}px;width:${pw}px;height:${pw}px;z-index:${20 + j}`;
    host.appendChild(p); G.push(p);
  }
  return { P, Lb, G };
}
const HX = 520, HY1 = 800, HSP = 38, HTOP = HY1 - 9 * HSP;
const H = makeStack($('hiso'), HX, HY1, 200, HSP);
const INF = [520, 232], INFA = 190;
const lem = (() => { let d = ''; for (let k = 0; k <= 160; k++) { const u = Math.PI / 2 + 2 * Math.PI * k / 160, s = Math.sin(u), c = Math.cos(u), q = 1 + s * s;
  d += (k ? ' L ' : 'M ') + (INF[0] + INFA * c / q).toFixed(1) + ' ' + (INF[1] + INFA * 1.05 * s * c / q).toFixed(1); } return d; })();
const hG = $('gHook');
const beam = sv('rect', { x: HX - 70, y: INF[1] + 30, width: 140, height: HTOP - INF[1] - 30, fill: 'url(#gBeam)', filter: 'url(#fGlowS)' }, hG);
const infGlow = sv('path', { d: lem, fill: 'none', stroke: '#cbfb61', 'stroke-width': 30, 'stroke-linecap': 'round', opacity: 0, filter: 'url(#fGlow)' }, hG);
const infDark = sv('path', { d: lem, fill: 'none', stroke: '#14110b', 'stroke-width': 26, 'stroke-linecap': 'round', opacity: 0 }, hG);
const infLine = sv('path', { d: lem, fill: 'none', stroke: 'url(#gInf)', 'stroke-width': 16, 'stroke-linecap': 'round', opacity: 0 }, hG);
const ILEN = infLine.getTotalLength();
[infGlow, infDark, infLine].forEach(p => sa(p, { 'stroke-dasharray': `${ILEN} ${ILEN}` }));
const HKW = [...$('hkT').querySelectorAll('span')];
function hook(t) {
  const [a, b] = S.hook;
  // the first frame reads on its own: the ten floors and the title are there, dimmed, from t = 0; they light on his words
  st($('hiso'), vis(t, a, b, 0, .35));
  // the floors light one by one on "Ten levels"; the top opens on "the limit": the top plate lifts, three ghost floors rise
  // above it and fade, a beam climbs to the infinity sign, which draws itself as he says "Infinity"
  H.P.forEach((p, i) => {
    const k = ez.out(lin(t, C.h_ten - .05 + i * .07, C.h_ten + .25 + i * .07)), lift = 10 * Math.sin(Math.PI * clamp(k * 1.6));
    const up = i === 9 ? 46 * ez.back(lin(t, C.h_open, C.h_open + .5)) : 0;
    p.firstChild.style.opacity = k.toFixed(3);
    p.style.transform = `translateY(${(-lift - up).toFixed(1)}px) rotateX(60deg) rotateZ(-45deg)`;
    const l = H.Lb[i]; l.className = k > .5 ? 'fl lit' : 'fl'; l.style.transform = `translateY(calc(-50% - ${up.toFixed(1)}px))`;
  });
  H.G.forEach((p, j) => {
    const k = lin(t, C.h_open + .1 + j * .12, C.h_open + .9 + j * .12), y = (HSP + 8) * (j + 1) * ez.out(k) + (j + 1) * 12;
    p.style.opacity = (k <= 0 ? 0 : (1 - .25 * j) * Math.min(1, k * 4) * (1 - .8 * lin(t, C.h_meet, C.h_meet + .6))).toFixed(3);
    p.style.transform = `translateY(${(-46 - y).toFixed(1)}px) rotateX(60deg) rotateZ(-45deg)`;
  });
  const bk = ez.out(lin(t, C.h_open + .1, C.h_open + .8)); op(beam, bk * (.75 + .25 * Math.sin(t * 4)));
  sa(beam, { y: INF[1] + 30 + (HTOP - INF[1] - 30) * (1 - bk), height: (HTOP - INF[1] - 30) * bk });
  const dr = ez.inOut(lin(t, C.h_open + .45, C.h_infinity + .35));
  [infGlow, infDark, infLine].forEach(p => sa(p, { 'stroke-dashoffset': ILEN * (1 - dr) }));
  op(infLine, dr > 0 ? 1 : 0); op(infDark, dr > 0 ? .6 : 0); op(infGlow, dr > 0 ? .35 + .25 * Math.sin(t * 3) + .4 * pulse(t, C.h_infinity + .3, .7) : 0);
  // "10 levels" on "Ten levels"; it gives way to the title on "Meet the Infinity Bonus"; "No depth limit" on its words
  const k10 = pop(t, C.h_ten - .1, C.h_no - .1, .35, .25); st($('hk10'), k10.o, 0, 0, k10.s);
  st($('hkT'), vis(t, a, b, 0, .35));
  [C.h_meet, C.h_infinity, C.h_bonus].forEach((c, i) => {
    const w = HKW[i]; w.style.opacity = (.35 + .65 * ez.out(lin(t, c - .06, c + .15))).toFixed(3);
    w.style.transform = `translateY(${(-10 * pulse(t, c - .04, .3)).toFixed(1)}px) scale(${(1 + .05 * pulse(t, c - .04, .3)).toFixed(3)})`;
  });
  const n = pop(t, C.h_no - .1, b, .4, .35); st($('hkNo'), n.o, 0, 0, n.s);
  op(hG, t < S.hi[0] + .4 ? 1 - ez.inOut(lin(t, b - .35, b)) : 0);
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi, e = b + .05;                               // it hands over to Profit Share without an empty frame
  const d = pop(t, a + .15, e, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .4, e, 24), r = rise(t, a + .65, e, 30); st($('hwho'), h.o, 0, h.y); st($('httl'), r.o, 0, r.y);
}

/* ---------- Profit Share: ten 1.5% level bars; the lime Infinity layer on top, from level 1, past level 10 ---------- */
const PS = $('gPS'), PX0 = 150, PP = 140, PW = 118, PY0 = 492, PY1 = 700;
const bars = [];
for (let i = 0; i < 13; i++) {
  const g = sv('g', { opacity: 0 }, PS), x = PX0 + i * PP, real = i < 10;
  const r = sv('rect', { x, y: PY0, width: PW, height: PY1 - PY0, rx: 16, fill: real ? 'url(#gBar)' : 'none', stroke: real ? 'rgba(155,124,255,.85)' : 'rgba(203,251,97,.4)',
    'stroke-width': real ? 2.5 : 2.5, 'stroke-dasharray': real ? 'none' : '10 9' }, g);
  if (real) { sv('rect', { x: x + 8, y: PY0 + 8, width: PW - 16, height: 26, rx: 10, fill: 'rgba(255,255,255,.10)' }, g);
    sv('text', { x: x + PW / 2, y: PY0 + 128, 'text-anchor': 'middle', fill: '#f6f3ff', style: 'font:800 40px Manrope' }, g).textContent = '1.5%'; }
  const cg = sv('g', {}, g);
  const chip = sv('rect', { x: x + PW / 2 - 34, y: 716, width: 68, height: 52, rx: 16, fill: 'rgba(20,16,34,.92)', stroke: real ? 'rgba(155,124,255,.6)' : 'rgba(203,251,97,.45)', 'stroke-width': 2 }, cg);
  const tx = sv('text', { x: x + PW / 2, y: 754, 'text-anchor': 'middle', fill: real ? '#cfc8e6' : '#cbfb61', style: 'font:800 32px Manrope' }, cg); tx.textContent = String(i + 1);
  bars.push({ g, r, chip, tx, x, real });
}
const band = sv('g', { opacity: 0 }, PS);
const bandGlow = sv('rect', { x: PX0, y: 404, width: 100, height: 72, rx: 24, fill: '#cbfb61', opacity: .35, filter: 'url(#fGlow)' }, band);
const bandR = sv('rect', { x: PX0, y: 404, width: 100, height: 72, rx: 24, fill: 'url(#gBand)' }, band);
const bandShine = sv('rect', { x: PX0, y: 410, width: 160, height: 18, rx: 9, fill: 'rgba(255,255,255,.45)' }, band);
const bandT = sv('text', { x: PX0 + 28, y: 456, fill: '#14190a', style: 'font:400 46px Anton;letter-spacing:.04em' }, band); bandT.textContent = 'INFINITY';
function share(t) {
  const [a, b] = S.share, on = t > a && t < b + .5;
  const ti = rise(t, a + .1, b, 30); st($('psT'), ti.o, 0, ti.y);
  const pl = ez.out(lin(t, C.p_leadership - .15, C.p_leadership + .3)); $('psPlus').style.opacity = pl.toFixed(3);
  $('psPlus').style.transform = `translateX(${(30 * (1 - pl)).toFixed(1)}px)`;
  const su = rise(t, C.s_one - .15, b, 20); st($('psSub'), su.o, 0, su.y);
  const fo = 1 - ez.inOut(lin(t, b - .35, b));
  bars.forEach((B, i) => {
    let k;
    if (B.real) k = ez.out(lin(t, (i === 0 ? C.s_one - .1 : C.s_every - .15 + i * .08), (i === 0 ? C.s_one + .35 : C.s_every + .25 + i * .08)));
    else k = ez.out(lin(t, C.p_all - .1 + (i - 10) * .15, C.p_all + .35 + (i - 10) * .15)) * [1, .7, .4][i - 10];
    op(B.g, on ? k * fo : 0);
    const h = (PY1 - PY0) * (B.real ? ez.out(clamp(k * 1.2)) : 1);
    sa(B.r, { y: PY1 - h, height: h });
    const l1 = i === 0 && t > C.p_level - .1;                    // "from level 1": its chip turns lime
    sa(B.chip, { fill: l1 ? '#cbfb61' : 'rgba(20,16,34,.92)' }); sa(B.tx, { fill: l1 ? '#14190a' : (B.real ? '#cfc8e6' : '#cbfb61') });
    B.chip.parentNode.setAttribute('transform', l1 ? `translate(${B.x + PW / 2} 742) scale(${(1 + .25 * pulse(t, C.p_level - .1, .5)).toFixed(3)}) translate(${-(B.x + PW / 2)} -742)` : '');
  });
  // the Infinity layer settles on top on "on top of the Profit Share" (levels 1 to 10), then runs on past level 10 on "all the way down"
  const dk = ez.back(lin(t, C.p_top - .25, C.p_top + .3)), ex = ez.inOut(lin(t, C.p_all - .1, C.p_down_end + .2));
  const w = mix(10 * PP - (PP - PW), 1920 + 200 - PX0, ex);
  op(band, on && t > C.p_top - .25 ? Math.min(1, lin(t, C.p_top - .25, C.p_top)) * fo : 0);
  band.setAttribute('transform', `translate(0 ${(-70 * (1 - dk)).toFixed(1)})`);
  [bandGlow, bandR].forEach(r => sa(r, { width: w }));
  sa(bandGlow, { opacity: .3 + .15 * Math.sin(t * 3) + .3 * pulse(t, C.p_top, .6) });
  sa(bandShine, { x: PX0 + 20 + ((t * 420) % Math.max(200, w - 180)), opacity: .35 });
  const pi = rise(t, C.s_paid - .15, C.p_from - .15, 24); st($('psPaid'), pi.o * fo, 0, pi.y);
  const pf = rise(t, C.p_from - .1, b, 24); st($('psInf'), pf.o * fo, 0, pf.y);
}

/* ---------- the bicycle (one SVG drawing, used twice: yours and a partner's) ---------- */
function makeBike(par, o) {
  const g = sv('g', { opacity: 0 }, par), R = { g };
  sv('ellipse', { cx: 280, cy: 204, rx: 470, ry: 22, fill: 'url(#gShadow)' }, g);
  R.halo = sv('ellipse', { cx: 280, cy: 150, rx: 520, ry: 230, fill: 'url(#gHalo)', opacity: 0 }, g);
  R.road = sv('line', { x1: -230, y1: 196, x2: 800, y2: 196, stroke: 'rgba(214,204,246,.22)', 'stroke-width': 4, 'stroke-dasharray': '34 26', 'stroke-linecap': 'round' }, g);
  const legFar = sv('path', { fill: 'none', stroke: `url(#${o.rider}D)`, 'stroke-width': 34, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  R.wheels = [0, 560].map(cx => {
    const w = sv('g', { transform: `translate(${cx} 0)` }, g), W = { w };
    W.track = sv('circle', { r: 214, fill: 'none', stroke: 'rgba(255,255,255,.08)', 'stroke-width': 18, opacity: 0 }, w);
    W.extra = sv('circle', { r: 214, fill: 'none', stroke: '#cbfb61', 'stroke-width': 18, 'stroke-linecap': 'round', transform: 'rotate(-90)', opacity: 0 }, w);
    W.glow = sv('circle', { r: 214, fill: 'none', stroke: '#cbfb61', 'stroke-width': 30, transform: 'rotate(-90)', opacity: 0, filter: 'url(#fGlowS)' }, w);
    W.fill = sv('circle', { r: 214, fill: 'none', stroke: '#cbfb61', 'stroke-width': 18, 'stroke-linecap': 'round', transform: 'rotate(-90)', opacity: 0 }, w);
    W.cap = sv('g', { opacity: 0 }, w);
    sv('rect', { x: -9, y: 194, width: 18, height: 40, rx: 6, fill: 'url(#gGold)', stroke: '#14110b', 'stroke-width': 3 }, W.cap);
    sv('circle', { r: 182, fill: 'rgba(12,9,20,.55)' }, w);
    sv('circle', { r: 182, fill: 'none', stroke: 'url(#gTire)', 'stroke-width': 26 }, w);
    sv('circle', { r: 194, fill: 'none', stroke: 'rgba(255,255,255,.10)', 'stroke-width': 2 }, w);
    sv('circle', { r: 166, fill: 'none', stroke: 'url(#gGoldU)', 'stroke-width': 7 }, w);
    sv('circle', { r: 158, fill: 'none', stroke: 'rgba(255,224,143,.22)', 'stroke-width': 2 }, w);
    W.sp = sv('g', {}, w);
    for (let k = 0; k < 18; k++) { const an = k * Math.PI / 9, an2 = an + .22 * (k % 2 ? 1 : -1);
      sv('line', { x1: 15 * Math.cos(an2), y1: 15 * Math.sin(an2), x2: 158 * Math.cos(an), y2: 158 * Math.sin(an), stroke: 'rgba(214,204,246,.55)', 'stroke-width': 2.2 }, W.sp); }
    sv('circle', { r: 20, fill: 'url(#gChrome)' }, w); sv('circle', { r: 7, fill: '#0b0912' }, w);
    return W;
  });
  // the rear cassette: nine sprockets, the biggest is the 1.5% gear, the smallest the 7.5% gear (a real bike's top gear)
  R.lens = sv('circle', { r: 64, fill: 'none', stroke: '#ffe08f', 'stroke-width': 5, opacity: 0 }, g);
  sv('circle', { r: 50, fill: 'rgba(12,9,20,.85)' }, g);
  R.spr = [];
  for (let i = 0; i < 9; i++) R.spr.push(sv('circle', { r: 46 - i * 3.6, fill: 'none', stroke: 'url(#gChrome)', 'stroke-width': 2.6 }, g));
  sv('circle', { r: 9, fill: 'url(#gChrome)' }, g);
  const BB = [235, 25];
  R.chainT = sv('line', { 'stroke-width': 6, 'stroke-dasharray': '8 5', 'stroke-linecap': 'round' }, g);
  R.chainB = sv('line', { 'stroke-width': 6, 'stroke-dasharray': '8 5', 'stroke-linecap': 'round' }, g);
  R.ring = sv('circle', { r: 0, fill: 'none', 'stroke-width': 6 }, g);
  const crankFar = sv('line', { stroke: '#4a4166', 'stroke-width': 12, 'stroke-linecap': 'round' }, g);
  // the frame
  const fr = `url(#${o.frame})`;
  const tube = (d, w) => { sv('path', { d, fill: 'none', stroke: fr, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', filter: 'url(#fDrop)' }, g);
    sv('path', { d, fill: 'none', stroke: 'rgba(255,255,255,.38)', 'stroke-width': Math.max(3, w * .22), 'stroke-linecap': 'round', transform: 'translate(0 -4)' }, g); };
  tube('M 0 0 L 235 25', 14); tube('M 0 0 L 178 -238', 12); tube('M 235 25 L 494 -178', 22); tube('M 235 25 L 178 -250', 20);
  tube('M 178 -250 L 480 -238', 18); tube('M 496 -176 C 512 -100 526 -40 560 0', 14); tube('M 476 -256 L 498 -168', 26);
  sv('path', { d: 'M 178 -250 L 164 -318', stroke: 'url(#gChrome)', 'stroke-width': 11, 'stroke-linecap': 'round' }, g);
  sv('path', { d: 'M 104 -332 C 130 -350 200 -348 228 -332 C 214 -318 160 -314 104 -332 Z', fill: 'url(#gSaddle)', stroke: 'rgba(255,224,143,.55)', 'stroke-width': 2.5 }, g);
  sv('path', { d: 'M 478 -256 L 486 -294 L 534 -302', fill: 'none', stroke: 'url(#gChrome)', 'stroke-width': 12, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  sv('path', { d: 'M 530 -302 C 566 -306 580 -284 572 -258 C 568 -244 556 -240 546 -246', fill: 'none', stroke: '#2a2540', 'stroke-width': 13, 'stroke-linecap': 'round' }, g);
  sv('path', { d: 'M 530 -302 C 566 -306 580 -284 572 -258', fill: 'none', stroke: 'rgba(255,224,143,.5)', 'stroke-width': 3, 'stroke-linecap': 'round', transform: 'translate(0 -4)' }, g);
  // the trip meter on the stem
  R.tm = sv('g', { transform: 'translate(500 -324)' }, g);
  sv('rect', { x: -30, y: -16, width: 60, height: 32, rx: 8, fill: '#0b0912', stroke: 'url(#gGold)', 'stroke-width': 3.5 }, R.tm);
  R.tmS = sv('rect', { x: -22, y: -9, width: 44, height: 18, rx: 4, fill: '#cbfb61', opacity: .25 }, R.tm);
  // the chainring and the crank
  const crg = sv('g', { transform: `translate(${BB[0]} ${BB[1]})` }, g);
  sv('circle', { r: 60, fill: 'none', stroke: 'url(#gGold)', 'stroke-width': 9, 'stroke-dasharray': '6 4.5' }, crg);
  sv('circle', { r: 50, fill: 'rgba(12,9,20,.7)', stroke: 'rgba(255,224,143,.6)', 'stroke-width': 3 }, crg);
  R.spider = sv('g', {}, crg);
  for (let k = 0; k < 5; k++) { const an = k * 2 * Math.PI / 5; sv('line', { x1: 0, y1: 0, x2: 46 * Math.cos(an), y2: 46 * Math.sin(an), stroke: 'url(#gGold)', 'stroke-width': 8, 'stroke-linecap': 'round' }, R.spider); }
  sv('circle', { r: 12, fill: 'url(#gChrome)' }, crg);
  const crankNear = sv('line', { stroke: 'url(#gChrome)', 'stroke-width': 13, 'stroke-linecap': 'round' }, g);
  const pedal = sv('rect', { width: 46, height: 14, rx: 5, fill: '#2a2540', stroke: 'rgba(255,224,143,.6)', 'stroke-width': 2 }, g);
  // the rider: a clean pictogram (no face, no photo), a gold helmet
  const legNear = sv('path', { fill: 'none', stroke: `url(#${o.rider})`, 'stroke-width': 38, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  sv('path', { d: 'M 168 -356 C 230 -450 300 -500 390 -508', fill: 'none', stroke: `url(#${o.rider})`, 'stroke-width': 48, 'stroke-linecap': 'round' }, g);
  sv('path', { d: 'M 392 -506 L 468 -420 L 548 -300', fill: 'none', stroke: `url(#${o.rider})`, 'stroke-width': 26, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  sv('circle', { cx: 446, cy: -560, r: 42, fill: `url(#${o.rider})` }, g);
  sv('path', { d: 'M 398 -562 C 396 -622 492 -634 502 -568 C 486 -556 428 -552 398 -562 Z', fill: 'url(#gGold)', stroke: '#8e6420', 'stroke-width': 2.5 }, g);
  sv('path', { d: 'M 428 -604 L 446 -584 M 452 -610 L 466 -588 M 476 -606 L 484 -586', stroke: 'rgba(26,20,5,.55)', 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
  const HIP = [168, -352], LA = 232, LB = 228;
  function leg(P) {
    const dx = P[0] - HIP[0], dy = P[1] - HIP[1], d = Math.min(Math.hypot(dx, dy), LA + LB - 1), ph = Math.atan2(dy, dx);
    const al = Math.acos(clamp((LA * LA + d * d - LB * LB) / (2 * LA * d), -1, 1)), K = [HIP[0] + LA * Math.cos(ph - al), HIP[1] + LA * Math.sin(ph - al)];
    return `M ${HIP[0]} ${HIP[1]} L ${K[0].toFixed(1)} ${K[1].toFixed(1)} L ${P[0].toFixed(1)} ${P[1].toFixed(1)} L ${(P[0] + 30).toFixed(1)} ${(P[1] + 4).toFixed(1)}`;
  }
  R.set = s => {
    g.setAttribute('transform', `translate(${s.x.toFixed(1)} ${s.y.toFixed(1)}) scale(${s.s.toFixed(4)})`); op(g, s.o);
    if (s.o <= .002) return;
    R.wheels.forEach(W => W.sp.setAttribute('transform', `rotate(${(s.ang % 360).toFixed(2)})`));
    sa(R.road, { 'stroke-dashoffset': (s.ang * Math.PI / 180 * 190).toFixed(1) });
    const th = s.ang * Math.PI / 180 * .55, p1 = [BB[0] + 88 * Math.cos(th), BB[1] + 88 * Math.sin(th)], p2 = [BB[0] - 88 * Math.cos(th), BB[1] - 88 * Math.sin(th)];
    R.spider.setAttribute('transform', `rotate(${(th * 180 / Math.PI).toFixed(2)})`);
    sa(crankNear, { x1: BB[0], y1: BB[1], x2: p1[0], y2: p1[1] }); sa(crankFar, { x1: BB[0], y1: BB[1], x2: p2[0], y2: p2[1] });
    sa(pedal, { x: p1[0] - 23, y: p1[1] - 7 });
    legNear.setAttribute('d', leg([p1[0], p1[1] - 6])); legFar.setAttribute('d', leg([p2[0], p2[1] - 6]));
    // the chain on the active sprocket (lime once there is a gear); a little dimmer and on the 1.5% sprocket with none
    const gf = s.gear, on = gf >= -.001, gi = Math.max(0, gf), r = 46 - gi * 3.6, col = on ? '#cbfb61' : 'rgba(214,204,246,.45)';
    R.spr.forEach((c, i) => sa(c, { stroke: on && Math.abs(i - gi) < .5 ? '#cbfb61' : 'url(#gChrome)', 'stroke-width': on && Math.abs(i - gi) < .5 ? 4.5 : 2.6 }));
    sa(R.chainT, { x1: 0, y1: -r, x2: BB[0], y2: BB[1] - 60, stroke: col, 'stroke-dashoffset': (-s.ang * 2).toFixed(1) });
    sa(R.chainB, { x1: 0, y1: r, x2: BB[0], y2: BB[1] + 60, stroke: col, 'stroke-dashoffset': (s.ang * 2).toFixed(1) });
    sa(R.ring, { r, stroke: col });
    op(R.lens, s.lens || 0); sa(R.lens, { r: 64 + 6 * Math.sin(s.ang / 40) });
    sa(R.tmS, { opacity: s.tm != null ? .25 + .75 * s.tm : .25 });
    op(R.halo, s.halo || 0);
    // the two wheels as two lines (Rule 1)
    const rg = s.rings, L2 = 2 * Math.PI * 214;
    R.wheels.forEach((W, j) => {
      if (!rg) { [W.track, W.fill, W.extra, W.glow, W.cap].forEach(e => op(e, 0)); return; }
      const f = rg.f[j], cnt = j === 0 ? Math.min(f, .5) : f, ext = j === 0 ? Math.max(0, f - .5) : 0;
      op(W.track, rg.o); op(W.fill, rg.o * (cnt > .001 ? 1 : 0)); sa(W.fill, { 'stroke-dasharray': `${(L2 * cnt).toFixed(1)} ${L2}` });
      op(W.glow, rg.o * (cnt > .001 ? rg.glow[j] : 0)); sa(W.glow, { 'stroke-dasharray': `${(L2 * cnt).toFixed(1)} ${L2}` });
      op(W.extra, rg.o * (ext > .001 ? 1 : 0)); sa(W.extra, { 'stroke-dasharray': `0 ${(L2 * .5).toFixed(1)} ${(L2 * ext).toFixed(1)} ${L2}`, stroke: rg.capk > 0 ? `rgba(${Math.round(mix(203, 120, rg.capk))},${Math.round(mix(251, 110, rg.capk))},${Math.round(mix(97, 150, rg.capk))},${mix(1, .55, rg.capk).toFixed(2)})` : '#cbfb61' });
      op(W.cap, j === 0 ? rg.o * rg.capk : 0);
      W.cap.setAttribute('transform', `scale(${(1 + .3 * (rg.capPulse || 0)).toFixed(3)})`);
    });
  };
  return R;
}
const BIKE = makeBike($('gBikes'), { frame: 'gFrame', rider: 'gRider' });
const PAR = makeBike($('gBikes'), { frame: 'gFrame2', rider: 'gRider2' });
$('gBikes').insertBefore(PAR.g, BIKE.g);                         // the partner rides behind yours

// where your bicycle is: [time, ease duration, {x, y (rear hub), s}]
const BK = [[0, 0, { x: 1170, y: 615, s: .8 }], [C.b_think - .25, .75, { x: 1050, y: 615, s: .8 }], [S.diff[0] + .05, .8, { x: 1290, y: 440, s: .55 }],
  [S.recap[0] - .05, .75, { x: 1460, y: 560, s: .5 }], [C.u_now - .25, .75, { x: 330, y: 650, s: .55 }]];
function keyAt(K, t) {
  let c = K[0][2];
  for (const [kt, d, k] of K) { if (t < kt) break; const p = ez.inOut(d <= .01 ? 1 : lin(t, kt, kt + d)); c = { x: mix(c.x, k.x, p), y: mix(c.y, k.y, p), s: mix(c.s, k.s, p) }; }
  return c;
}
const bikeO = t => vis(t, C.b_think - .25, S.turn[1], .6, .3);
const hubAt = (b, lx, ly) => [b.x + b.s * lx, b.y + b.s * ly];

/* ---------- the side panel: the cassette (the scale), the month, Rule 1, Rule 2 ---------- */
const CAS = $('cas'), CX = 400, rowY = i => 650 - i * 66, rowRx = i => 150 - i * 13;
sv('rect', { x: CX - 9, y: 112, width: 18, height: 560, rx: 9, fill: 'url(#gSprk)', opacity: .55 }, CAS);
const crow = [];
for (let i = 0; i < 9; i++) {
  const y = rowY(i), rx = rowRx(i), ry = rx * .2 + 4, g = sv('g', { opacity: 0 }, CAS);
  sv('ellipse', { cx: CX, cy: y + 7, rx, ry, fill: '#2a2540' }, g);
  const face = sv('ellipse', { cx: CX, cy: y, rx, ry, fill: 'url(#gSprk)', stroke: 'rgba(255,255,255,.55)', 'stroke-width': 2 }, g);
  const teeth = sv('ellipse', { cx: CX, cy: y, rx: rx + 4, ry: ry + 2, fill: 'none', stroke: 'rgba(214,204,246,.7)', 'stroke-width': 4, 'stroke-dasharray': '5 6' }, g);
  sv('ellipse', { cx: CX, cy: y, rx: rx * .32, ry: ry * .32, fill: '#15112a', stroke: 'rgba(255,255,255,.35)', 'stroke-width': 1.5 }, g);
  const th = sv('text', { x: 222, y: y + 14, 'text-anchor': 'end', fill: '#cfc8e6', style: 'font:800 40px Manrope' }, g); th.textContent = THL[i];
  const rt = sv('text', { x: 582, y: y + 16, 'text-anchor': 'start', fill: '#cfc8e6', style: 'font:400 48px Anton;letter-spacing:.02em' }, g); rt.textContent = RATE[i];
  crow.push({ g, face, teeth, th, rt, y, rx, ry });
}
const cGlow = sv('ellipse', { cx: CX, fill: 'none', stroke: '#cbfb61', 'stroke-width': 18, opacity: 0, filter: 'url(#fGlowS)' }, CAS);
const cRing = sv('ellipse', { cx: CX, fill: 'none', stroke: '#cbfb61', 'stroke-width': 8, 'stroke-dasharray': '11 6', opacity: 0 }, CAS);
const PC = ['pcGear', 'pcMonth', 'pcR1', 'pcR2'].map($);
const LEAD = sv('path', { fill: 'none', stroke: '#ffe08f', 'stroke-width': 3.5, 'stroke-dasharray': '2 10', 'stroke-linecap': 'round', opacity: 0 }, $('gLinks'));
const TMLEAD = sv('path', { fill: 'none', stroke: '#ffe08f', 'stroke-width': 3.5, 'stroke-dasharray': '2 10', 'stroke-linecap': 'round', opacity: 0 }, $('gLinks'));
const TEAM = sv('path', { fill: 'none', stroke: '#cbfb61', 'stroke-width': 5, 'stroke-dasharray': '3 12', 'stroke-linecap': 'round', opacity: 0 }, $('gLinks'));
const PANW = [[C.b_gears - .25, C.m_resets + .4], [C.m_resets + .4, S.month[1] + .05], [S.fifty[0] + .05, S.fifty[1] + .05], [S.diff[0] + .05, S.diff[1] + .1]];
function panel(t) {
  const po = vis(t, PANW[0][0], PANW[3][1], .45, .35); st($('pan'), po, -30 * (1 - po), 0);
  PC.forEach((e, i) => { const [a, b] = PANW[i], v = vis(t, a, b, i ? .35 : .01, i < 3 ? .25 : .01); e.style.opacity = v.toFixed(3); e.style.visibility = v > .002 ? 'visible' : 'hidden'; });
  // the cassette: the sprockets appear bottom to top on "with gears"; the chain climbs with the trip meter
  const cf = chainAt(t), on = cf > -.5 && t < C.m_resets + .1;
  crow.forEach((R, i) => {
    op(R.g, ez.out(lin(t, C.b_gears - .1 + i * .06, C.b_gears + .25 + i * .06)));
    const ga = gearAt(t), act = on && i === ga, past = on && i < ga;
    sa(R.th, { fill: act ? '#ffe08f' : past ? '#f6f3ff' : '#9c95b8' }); sa(R.rt, { fill: act ? '#cbfb61' : past ? '#f6f3ff' : '#9c95b8' });
    const sc = act ? 1.12 : 1, ax = 222;
    R.th.setAttribute('transform', `translate(${ax} ${R.y}) scale(${sc}) translate(${-ax} ${-R.y})`);
    R.rt.setAttribute('transform', `translate(582 ${R.y}) scale(${sc}) translate(-582 ${-R.y})`);
    sa(R.teeth, { stroke: act ? '#cbfb61' : 'rgba(214,204,246,.7)' });
  });
  // "$50K" glows on "fifty thousand dollars", "$40M" on "forty million"
  [[0, C.b_fifty], [8, C.b_forty]].forEach(([i, c]) => { const p = pulse(t, c - .05, .6); if (p > 0) crow[i].th.setAttribute('transform', `translate(222 ${crow[i].y}) scale(${1.12 + .1 * p}) translate(-222 ${-crow[i].y})`); });
  const ci = clamp(cf, 0, 8), cy = mix(rowY(Math.floor(ci)), rowY(Math.min(8, Math.floor(ci) + 1)), ci - Math.floor(ci)), crx = mix(rowRx(Math.floor(ci)), rowRx(Math.min(8, Math.floor(ci) + 1)), ci - Math.floor(ci));
  const ro = on ? 1 : 1 - lin(t, C.m_resets - .05, C.m_resets + .25);
  [cRing, cGlow].forEach(e => sa(e, { cy, rx: crx + 16, ry: crx * .2 + 14 }));
  op(cRing, cf > -.5 || t > C.m_resets ? ro * (cf > -.5 || t > C.m_resets - .05 ? 1 : 0) : 0); op(cGlow, (cf > -.5 ? ro : 0) * (.5 + .3 * Math.sin(t * 4)));
  sa(cRing, { 'stroke-dashoffset': (-t * 40).toFixed(1) });
  // the month: the big calendar flips on "every month"; the two rules tick on their words
  flip($('calA'), $('calB'), t, C.m_month - .1);
  [['mr1', C.m_only], ['mr2', C.m_paid]].forEach(([id, c]) => { const r = rise(t, c - .15, PANW[1][1] + .2, 26); st($(id), r.o, 0, r.y);
    $(id).querySelector('.ok').style.transform = `scale(${ez.back(lin(t, c, c + .35)).toFixed(3)})`; });
  // Rule 1
  [['r1big', C.f_fifty - .15], ['r1a', C.f_strongest - .1], ['r1b', C.f_half - .05], ['r1c', C.f_bike - .1]].forEach(([id, c]) => {
    const r = rise(t, c, S.fifty[1] + .2, 26); st($(id), r.o, 0, r.y, 1 + .03 * pulse(t, c + .1, .45)); });
  foc($('r1a'), 1 - .45 * ez.out(lin(t, C.f_bike - .1, C.f_bike + .3)) + .45 * ez.out(lin(t, C.f_wheels, C.f_wheels + .3)));
  // Rule 2: on their structure; your rate 3%, their rate 1.5%, you earn 1.5%; all your other lines: your full rate
  const on2 = ez.out(lin(t, C.d_structure - .15, C.d_structure + .3)); $('r2on').style.opacity = on2.toFixed(3); $('r2on').style.transform = `translateY(${(16 * (1 - on2)).toFixed(1)}px)`;
  [['r2big', C.d_difference - .15], ['eq1', C.d_three - .1], ['eq2', C.d_one - .15], ['eq3', C.d_one2 - .1], ['r2c', C.d_one2 + .35]].forEach(([id, c]) => {
    const p = id === 'eq3' ? pop(t, c, S.diff[1] + .2, .35, .3) : rise(t, c, S.diff[1] + .2, 26);
    st($(id), p.o, 0, p.y || 0, p.s || 1); });
  const ln = ez.inOut(lin(t, C.d_leaves - .15, C.d_leaves + .3)); $('eqLine').style.transform = `scaleX(${ln.toFixed(3)})`; $('eqLine').style.opacity = ln > 0 ? 1 : 0;
  $('eqLine').style.transformOrigin = '0 50%';
}
function flip(A, B, t, c) {                                     // a calendar page turns over: 1 folds away, 2 is under it
  const k = ez.inOut(lin(t, c, c + .45));
  A.style.transform = `rotateX(${(-100 * k).toFixed(1)}deg)`; A.style.opacity = (1 - lin(k, .6, 1)).toFixed(3); A.style.zIndex = 2; B.style.zIndex = 1;
}

/* ---------- the bicycle scenes: your bike, the trip meter, the wheels (Rule 1), a partner in your line (Rule 2) ---------- */
function bikes(t) {
  const b = keyAt(BK, t), o = bikeO(t), ang = t * 95;
  const g = t < S.diff[0] ? chainAt(t) : 1;                        // Rule 2 onwards: your gear is 3%, the example's
  const rings = t > S.fifty[0] && t < S.diff[0] + .4 ? {
    o: vis(t, S.fifty[0] + .1, S.diff[0] + .4, .4, .35), f: [rearFill(t), frontFill(t)], capk: capK(t), capPulse: pulse(t, C.f_half - .05, .5),
    glow: [.4 + .6 * pulse(t, C.f_wheels, .8), .4 + .6 * pulse(t, C.f_wheels, .8)] } : null;
  const lensO = vis(t, C.b_gears - .1, C.m_resets + .4, .3, .3);
  BIKE.set({ x: b.x, y: b.y, s: b.s, o, ang, gear: g, lens: lensO, tm: vis(t, C.b_set - .1, S.fifty[1], .3, .3), rings });
  // the lead from the bike's cassette to the panel's cassette
  const hub = [b.x, b.y], cf = clamp(chainAt(t), 0, 8), py = 150 + mix(rowY(Math.floor(cf)), rowY(Math.min(8, Math.floor(cf) + 1)), cf - Math.floor(cf));
  LEAD.setAttribute('d', `M 806 ${py.toFixed(1)} C 900 ${py.toFixed(1)} ${(hub[0] - 150).toFixed(1)} ${hub[1]} ${(hub[0] - 64 * b.s).toFixed(1)} ${hub[1]}`);
  op(LEAD, lensO * .9);
  // the trip meter, magnified: the month's new volume; resets to $0 on "resets", the calendar flips on "every month"
  const tmv = rise(t, C.b_set - .1, S.fifty[1], 20, .35, .3); st($('tm'), tmv.o, 0, tmv.y, 1 + .05 * pulse(t, C.m_trip - .05, .5) + .04 * pulse(t, C.m_resets, .45));
  $('tmV').textContent = fmt(meter(t));
  flip($('tmA'), $('tmB'), t, C.m_every - .1);
  const tp = hubAt(b, 500, -324);
  TMLEAD.setAttribute('d', `M ${(tp[0] + 22).toFixed(1)} ${(tp[1] - 12).toFixed(1)} C ${(tp[0] + 40).toFixed(1)} ${(tp[1] - 40).toFixed(1)} 1560 340 1580 ${306 + tmv.y}`);
  op(TMLEAD, tmv.o * .9);
  // Rule 1: the wheel labels, your gear from the counted volume
  const wr = rise(t, C.f_strongest - .05, S.fifty[1] + .1, 20), wf = rise(t, C.f_bike - .1, S.fifty[1] + .1, 20);
  const rh = hubAt(b, 0, 0), fh = hubAt(b, 560, 0);
  place('wRear', rh[0] - 150, rh[1] + b.s * 214 + 22); st($('wRear'), wr.o, 0, wr.y);
  place('wFront', fh[0] - 90, fh[1] + b.s * 214 + 22); st($('wFront'), wf.o, 0, wf.y);
  const gv = gearOf(meter(t)), gy = pop(t, C.f_strongest + .3, S.fifty[1] + .1, .35, .3);
  const gEl = $('gYou'); if (gv >= 0) gEl.lastChild.textContent = RATE[gv];
  place('gYou', b.x - b.s * 265, b.y - b.s * 310); st(gEl, gv >= 0 ? gy.o : 0, 0, 0, gy.s * (1 + .08 * pulse(t, C.f_wheels + .2, .5)));
  // Rule 2: a partner in your line rides in on their own bike, in a lower gear (1.5%); the difference on their structure
  const pk = ez.out(lin(t, C.d_partner - .3, C.d_partner + .6)), po = vis(t, C.d_partner - .3, S.recap[0] + .3, .45, .35);
  PAR.set({ x: mix(760, 960, pk), y: 792, s: .45, o: po, ang: t * 80 + 40, gear: 0, halo: ez.out(lin(t, C.d_structure - .1, C.d_structure + .4)) * po });
  // the labels say each rate on its word: yours on "Three percent", theirs on "their own rate"
  const ly = rise(t, S.diff[0] + .5, S.diff[1] + .1, 20); place('lbYou', 846, 166); st($('lbYou'), ly.o, 0, ly.y);
  const lyr = ez.out(lin(t, C.d_three - .1, C.d_three + .25)); $('lbYouR').style.opacity = lyr.toFixed(3); $('lbYouR').style.maxHeight = (34 * lyr).toFixed(1) + 'px'; $('lbYouR').style.marginTop = (-8 * (1 - lyr)).toFixed(1) + 'px';
  const lp = rise(t, C.d_partner - .1, S.diff[1] + .1, 20); place('lbPar', 1330, 680); st($('lbPar'), lp.o, 0, lp.y);
  const lpr = ez.out(lin(t, C.d_own - .1, C.d_own + .25)); $('lbParR').style.opacity = lpr.toFixed(3); $('lbParR').style.maxHeight = (34 * lpr).toFixed(1) + 'px'; $('lbParR').style.marginTop = (-8 * (1 - lpr)).toFixed(1) + 'px';
  $('lbPar').classList.toggle('g', t > C.d_structure - .1);
  TEAM.setAttribute('d', `M ${(b.x + b.s * 300).toFixed(1)} ${(b.y + b.s * 214).toFixed(1)} C ${(b.x + b.s * 280).toFixed(1)} ${(b.y + b.s * 330).toFixed(1)} 1300 600 1250 640`);
  op(TEAM, vis(t, C.d_line - .2, S.diff[1] + .1, .4, .3)); sa(TEAM, { 'stroke-dashoffset': (-t * 30).toFixed(1) });
}

/* ---------- recap: three ticked cards, on his words; your bike rolls on beside them ---------- */
function recap(t) {
  const [a, b] = S.recap;
  const ti = rise(t, C.rc_so - .1, b, 30, .45, .3); st($('rtt'), ti.o, 0, ti.y);
  [['rc1', C.rc_gear], ['rc2', C.rc_two], ['rc3', C.rc_diff]].forEach(([id, c], i) => {
    const v = rise(t, C.rc_so + .1 + i * .08, b, 40, .45, .3), k = ez.out(lin(t, c - .15, c + .3));
    st($(id), v.o * (.35 + .65 * k), 0, v.y, 1 + .03 * pulse(t, c, .45));
    $(id).querySelector('.ok').style.transform = `scale(${ez.back(lin(t, c, c + .35)).toFixed(3)})`;
    $(id).querySelector('.ok').style.opacity = (t >= c ? 1 : 0).toString();
  });
  const ch = rise(t, C.rc_infinity, b, 16); st($('rcChip'), ch.o, 0, ch.y);
}

/* ---------- now it's your turn: see the partner plan, tap any Join JetUP button ---------- */
function turn(t) {
  const [a, b] = S.turn, tt = C.i_press;
  const h = rise(t, C.u_now - .02, b, 40); st($('ut'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, C.u_now - .02, C.u_now + .45)));
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
  hook(t); hi(t); share(t); panel(t); bikes(t); recap(t); turn(t);
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

/* JetUP Zoom invitation promo v2: every visual is a pure function of time t (seconds). */
(function () {
'use strict';
const TL = window.TL, C = TL.cues, T = TL.T;
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const ez = {
  out: x => 1 - Math.pow(1 - x, 3), inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.7, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
};
function st(el, o, x = 0, y = 0, s = 1, r = 0) {
  el.style.opacity = o.toFixed(3);
  el.style.visibility = o <= .002 ? 'hidden' : 'visible';
  el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)}) rotate(${r.toFixed(2)}deg)`;
}
function scene(t, a, b, fi = .22, fo = .2) {
  if (t < a || t > b) return { v: 0, y: 0 };
  const i = fi <= 0 ? 1 : ez.out(lin(t, a, a + fi)), o = ez.inOut(lin(t, b - fo, b));
  return { v: Math.min(i, 1 - o), y: 30 * (1 - i) - 40 * o };
}
function pop(t, t0, d = .38) { const k = lin(t, t0, t0 + d); return { o: ez.out(lin(t, t0, t0 + .12)), s: .5 + .5 * ez.back(k) }; }
function rise(t, t0, d = .32, dist = 46) { const k = ez.out(lin(t, t0, t0 + d)); return { o: k, y: dist * (1 - k) }; }
function slide(t, t0, dx, d = .32) { const k = ez.out(lin(t, t0, t0 + d)); return { o: k, x: dx * (1 - k) }; }

/* ---------- captions (numbers and the web address shown the way people read them) ---------- */
const RAW = TL.words, W = [];
for (let i = 0; i < RAW.length; i++) {
  const w = RAW[i], nx = k => (RAW[i + k] || {}).w || '';
  const merge = (n, text) => { W.push({ w: text, a: w.a, b: RAW[i + n - 1].b }); i += n - 1; };
  if (w.w === 'MTG' && nx(1) === 'tribe') { merge(8, 'mtgtribe.com/JetUpZoom,'); continue; }
  if (w.w === 'one' && nx(1) === 'hundred' && nx(2) === 'dollar') { merge(3, '$100'); continue; }
  if (w.w === 'Eleven' && nx(1) === 'thirty') { merge(2, '11:30'); continue; }
  if (w.w === 'Jet' && /^Up/.test(nx(1))) { merge(2, 'JetUP' + nx(1).slice(2)); continue; }
  if (w.w === 'P' && nx(1) === 'M') { merge(2, 'PM'); continue; }
  const num = { Eight: '8', Seven: '7', ten: '10' }[w.w];
  W.push({ w: num || w.w, a: w.a, b: w.b });
}
const PH = [];
{ let cur = [];
  W.forEach((w, i) => {
    cur.push(w);
    const nx = W[i + 1], end = /[.!?:]$/.test(w.w) || (/,$/.test(w.w) && cur.length >= 3) || cur.length >= 6 || !nx || nx.a - w.b > .6;
    if (end) { PH.push(cur); cur = []; }
  });
}
const capbox = $('capbox'); let lastPh = -1;
function captions(t) {
  let idx = -1;
  for (let i = 0; i < PH.length; i++) {
    const p = PH[i], a = p[0].a - .12, nxt = PH[i + 1] ? PH[i + 1][0].a - .12 : 1e9, b = Math.min(p[p.length - 1].b + .35, nxt);
    if (t >= a && t < b) { idx = i; break; }
  }
  if (idx < 0) { capbox.style.opacity = 0; capbox.style.visibility = 'hidden'; return; }
  const p = PH[idx];
  if (idx !== lastPh) { capbox.innerHTML = p.map(w => `<span>${w.w}</span>`).join(' '); lastPh = idx; }
  const sp = capbox.children;
  p.forEach((w, i) => { const end = p[i + 1] ? p[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  const a = p[0].a - .12, b = p[p.length - 1].b + .35;
  capbox.style.visibility = 'visible';
  capbox.style.opacity = Math.min(lin(t, a, a + .12), 1 - lin(t, b - .12, b)).toFixed(3);
}

/* ---------- scenes ---------- */
const S = {
  s0: [0, C.hi - .25], s1: [C.hi - .45, C.eight - .2], s2: [C.eight - .4, C.curious - .15], s3: [C.curious - .35, C.learn3 - .15],
  s4: [C.learn3 - .35, C.trading - .15], s5: [C.trading - .35, C.join - .15], s6: [C.join - .35, C.see - .12], s7: [C.see - .3, T + .5]
};
const URL = [[C.mtgU, 'mtg'], [C.tribe, 'mtgtribe'], [C.dot, 'mtgtribe.'], [C.com, 'mtgtribe.com'], [C.slash, 'mtgtribe.com/'],
  [C.jet, 'mtgtribe.com/<i>JetUp</i>'], [C.zoomU, 'mtgtribe.com/<i>JetUpZoom</i>']];
let lastUrl = null;

const PUNCH = [C.gold0, C.tonight, C.eight, C.seven, C.eleven, C.burned, C.one, C.two, C.threeP, C.risk, C.zoomU + .55, C.see, C.lgtc];
const FLASH = [S.s1[0], S.s2[0], S.s3[0], S.s4[0], S.s5[0], S.s6[0], S.s7[0]].map(x => x + .12);
window.R = function (t) {
  let pz = 0; PUNCH.forEach(p => { if (t >= p - .04) pz += .03 * Math.exp(-(t - p + .04) / .16); });
  st($('sc'), 1, 0, 0, 1 + pz);
  let fl = 0; FLASH.forEach(f => { if (t >= f) fl = Math.max(fl, .13 * Math.exp(-(t - f) / .07)); });
  st($('flash'), fl);
  st($('bgc'), 1, 0, -t * 5);
  st($('g1'), 1, 40 * Math.sin(t * .25), 30 * Math.cos(t * .2));
  st($('g2'), 1, -40 * Math.sin(t * .22), 0);
  st($('top'), 1);
  $('dot').style.opacity = (.55 + .45 * Math.sin(t * 6)).toFixed(3);

  /* S0 hook: the first frame already reads AUTOMATED GOLD TRADING (WhatsApp preview) */
  { const e = scene(t, ...S.s0, 0, .3);
    st($('h1'), e.v, 0, e.y, 1.07 - .07 * ez.out(lin(t, .2, .5)));
    st($('h2'), e.v, 0, e.y, 1.07 - .07 * ez.out(lin(t, C.gold0 - .05, C.gold0 + .25)));
    const g = lin(t, C.gold0 - .1, C.gold0 + .5);
    st($('hbar'), e.v * ez.out(lin(t, C.gold0 - .1, C.gold0 + .08)), 0, e.y - 420 * (1 - ez.back(g)), 1 + .02 * Math.sin(t * 2));
    const h = rise(t, C.works0 - .5); st($('hsub'), e.v * h.o, 0, e.y + h.y);
    const p = pop(t, C.before0 - .05, .5); st($('hpill'), e.v * p.o, 0, e.y, p.s * (1 + .02 * Math.sin(Math.PI * lin(t, C.cent, C.cent + .4)))); }

  /* S1 the invitation */
  { const e = scene(t, ...S.s1); const cr = pop(t, C.hi - .2), m = pop(t, C.mtg - .25), ar = rise(t, C.arch - .35);
    st($('crown1'), e.v * cr.o, 0, e.y, cr.s);
    st($('mono1'), e.v * m.o, 0, e.y, m.s);
    st($('arch1'), e.v * ar.o, 0, e.y + ar.y);
    const k = rise(t, C.inviting - .25, .6, 140);
    st($('tk'), e.v * k.o, 0, e.y + k.y, .94 + .06 * k.o);
    const t1 = pop(t, C.inviting - .05, .55); st($('tk1'), t1.o, 0, 0, t1.s);
    const t2 = rise(t, C.live0 - .1); st($('tk2'), t2.o, 0, t2.y);
    const t3 = pop(t, C.zoom - .15); st($('tk3'), t3.o, 0, 0, t3.s);
    const d = ez.out(lin(t, C.zoom, C.zoom + .5)); st($('tkd'), d, 0, 0, 1); $('tkd').style.clipPath = `inset(0 ${(100 * (1 - d)).toFixed(1)}% 0 0)`;
    const sk = lin(t, C.tonight - .05, C.tonight + .3);
    st($('tk4'), ez.out(lin(t, C.tonight - .05, C.tonight + .08)), 0, 0, 1.8 - .8 * ez.out(sk), -6 * ez.out(sk)); }

  /* S2 the times */
  { const e = scene(t, ...S.s2); const k = rise(t, S.s2[0] + .05), d = rise(t, S.s2[0] + .15);
    st($('k2'), e.v * k.o, 0, e.y + k.y);
    st($('dt2'), e.v * d.o, 0, e.y + d.y);
    st($('tc'), e.v * ez.out(lin(t, C.eight - .35, C.eight - .1)), 0, e.y);
    const at = [C.eight, C.seven, C.eleven];
    at.forEach((a, i) => {
      const s = slide(t, a - .2, -90); st($('tr' + (i + 1)), s.o, s.x, 0);
      $('tr' + (i + 1)).classList.toggle('on', t >= a - .1 && (i === 2 || t < at[i + 1] - .1));
    }); }

  /* S3 why come */
  { const e = scene(t, ...S.s3);
    const b1 = slide(t, C.curious - .1, -120), b2 = slide(t, C.burned - .4, -120), w = rise(t, C.come - .3), a1 = slide(t, C.come - .05, 120), a2 = slide(t, C.ask - .15, 120);
    st($('b1'), e.v * b1.o, b1.x, e.y); st($('b2'), e.v * b2.o, b2.x, e.y);
    st($('why'), e.v * w.o, 0, e.y + w.y);
    st($('a1'), e.v * a1.o, a1.x, e.y); st($('a2'), e.v * a2.o, a2.x, e.y); }

  /* S4 three things you'll learn */
  { const e = scene(t, ...S.s4); const h = pop(t, C.learn3 - .1, .55);
    st($('lh'), e.v * h.o, 0, e.y, h.s * (1 + .04 * Math.sin(Math.PI * lin(t, C.three, C.three + .4))));
    const at = [C.one, C.two, C.threeP], end = S.s4[1];
    at.forEach((a, i) => {
      const s = slide(t, a - .12, -100), nxt = i < 2 ? at[i + 1] - .12 : end + 1, dim = 1 - .35 * ez.out(lin(t, nxt, nxt + .35));
      st($('l' + (i + 1)), e.v * s.o * dim, s.x, e.y, .97 + .03 * s.o);
      $('l' + (i + 1)).classList.toggle('foc', t >= a - .12 && t < nxt);
    }); }

  /* S5 learn first, then decide */
  { const e = scene(t, ...S.s5);
    const d1 = pop(t, C.trading - .1), a1 = rise(t, C.learnF - .4, .3, -20), d2 = pop(t, C.learnF - .2), a2 = rise(t, C.decide - .5, .3, -20), d3 = pop(t, C.decide - .35);
    st($('d1'), e.v * d1.o, 0, e.y, d1.s); st($('da1'), e.v * a1.o, 0, e.y + a1.y);
    st($('d2'), e.v * d2.o, 0, e.y, d2.s); st($('da2'), e.v * a2.o, 0, e.y + a2.y);
    st($('d3'), e.v * d3.o, 0, e.y, d3.s); }

  /* S6 join the call, then share */
  { const e = scene(t, ...S.s6); const j = pop(t, C.join - .1), u = pop(t, C.join + .1, .5);
    st($('j1'), e.v * j.o, 0, e.y, j.s);
    let txt = ''; URL.forEach(([a, s]) => { if (t >= a - .03) txt = s; });
    if (txt !== lastUrl) { $('ut').innerHTML = txt; lastUrl = txt; }
    $('ucur').style.opacity = t < C.zoomU + .8 && Math.floor(t * 3) % 2 === 0 ? 1 : 0;
    const tapT = C.zoomU + .55, press = 1 - .035 * Math.sin(Math.PI * lin(t, tapT - .05, tapT + .25));
    st($('u6'), e.v * u.o, 0, e.y, u.s * press);
    const hin = ez.inOut(lin(t, C.zoomU, tapT - .05)), hout = lin(t, tapT + .5, tapT + .85), hs = 1 - .12 * Math.sin(Math.PI * lin(t, tapT - .08, tapT + .22));
    st($('hand'), e.v * Math.min(lin(t, C.zoomU, C.zoomU + .2), 1 - hout), 260 * (1 - hin) - 90, e.y + 380 * (1 - hin) - 40, hs, -12 * (1 - hin));
    const rp = lin(t, tapT, tapT + .65); st($('rip'), e.v * (rp > 0 && rp < 1 ? 1 - rp : 0), 0, e.y, 1 + 9 * ez.out(rp));
    const ea = pop(t, C.logIn - .1); st($('early'), e.v * ea.o, 0, e.y, ea.s * (1 + .03 * Math.sin(Math.PI * lin(t, C.ten, C.ten + .4))));
    const sh = rise(t, C.send - .15, .5, 60); st($('share'), e.v * sh.o, 0, e.y + sh.y);
    const pl = lin(t, C.someone - .1, C.someone + .9);
    st($('plane'), e.v * (pl > 0 && pl < 1 ? Math.sin(Math.PI * pl) : 0), 760 * ez.inOut(pl), e.y - 140 * Math.sin(Math.PI * pl * .9), .8 + .4 * pl, -20 + 30 * pl); }

  /* S7 see you tonight */
  { const e = scene(t, ...S.s7, .3, .01); const h = pop(t, C.see - .1, .55);
    st($('e1'), e.v * h.o, 0, e.y, h.s);
    [.35, .5, .65].forEach((d, i) => { const c = pop(t, C.see + d, .45); st($('ch' + (i + 1)), e.v * c.o, 0, e.y, c.s); });
    const u = rise(t, C.see + .7, .5, 50); st($('u7'), e.v * u.o, 0, e.y + u.y, 1 + .012 * Math.sin(Math.max(0, t - C.see - 1.2) * 3.2));
    const b = rise(t, C.lgtc - .45), s = pop(t, C.lgtc - .05, .6), d = rise(t, C.lgtc + .6);
    st($('e2'), e.v * b.o, 0, e.y + b.y); st($('e3'), e.v * s.o, 0, e.y, s.s); st($('disc'), e.v * d.o, 0, e.y + d.y); }

  captions(t);
  st($('fade'), lin(t, T - .2, T));
};
window.READY = true;
})();

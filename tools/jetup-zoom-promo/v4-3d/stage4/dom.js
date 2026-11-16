/* JetUP Zoom invitation v4: the HTML layer (headlines, labels, captions), a pure function of time t. */
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
  el.style.opacity = o.toFixed(3); el.style.visibility = o <= .002 ? 'hidden' : 'visible';
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

/* captions */
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
  W.forEach((w, i) => { cur.push(w); const nx = W[i + 1], end = /[.!?:]$/.test(w.w) || (/,$/.test(w.w) && cur.length >= 3) || cur.length >= 6 || !nx || nx.a - w.b > .6; if (end) { PH.push(cur); cur = []; } });
}
const capbox = $('capbox'); let lastPh = -1;
function captions(t) {
  let idx = -1;
  for (let i = 0; i < PH.length; i++) { const p = PH[i], a = p[0].a - .12, nxt = PH[i + 1] ? PH[i + 1][0].a - .12 : 1e9, b = Math.min(p[p.length - 1].b + .35, nxt); if (t >= a && t < b) { idx = i; break; } }
  if (idx < 0) { capbox.style.opacity = 0; capbox.style.visibility = 'hidden'; return; }
  const p = PH[idx]; if (idx !== lastPh) { capbox.innerHTML = p.map(w => `<span>${w.w}</span>`).join(' '); lastPh = idx; }
  const sp = capbox.children; p.forEach((w, i) => { const end = p[i + 1] ? p[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  const a = p[0].a - .12, b = p[p.length - 1].b + .35; capbox.style.visibility = 'visible'; capbox.style.opacity = Math.min(lin(t, a, a + .12), 1 - lin(t, b - .12, b)).toFixed(3);
}

/* scenes (shared with the 3D layer) */
const S = window.SCENES = {
  s0: [0, C.hi - .25], s1: [C.hi - .45, C.eight - .2], s2: [C.eight - .4, C.curious - .15], s3: [C.curious - .35, C.learn3 - .15],
  s4: [C.learn3 - .35, C.trading - .15], s5: [C.trading - .35, C.join - .15], s6: [C.join - .35, C.see - .12], s7: [C.see - .3, T + .5]
};
const PUNCH = [C.gold0, C.tonight, C.eight, C.seven, C.eleven, C.burned, C.one, C.two, C.threeP, C.risk, C.zoomU + .55, C.see, C.lgtc];
const FLASH = ['s1', 's2', 's3', 's4', 's5', 's6', 's7'].map(k => S[k][0] + .12);

window.RD = function (t) {
  let pz = 0; PUNCH.forEach(p => { if (t >= p - .04) pz += .03 * Math.exp(-(t - p + .04) / .16); });
  $('wrap').style.transform = `scale(${(1 + pz).toFixed(4)})`;
  let fl = 0; FLASH.forEach(f => { if (t >= f) fl = Math.max(fl, .12 * Math.exp(-(t - f) / .07)); }); st($('flash'), fl);
  st($('bgc'), 1, 0, -t * 5); st($('g1'), 1, 40 * Math.sin(t * .25), 30 * Math.cos(t * .2)); st($('g2'), 1, -40 * Math.sin(t * .22), 0);
  st($('top'), 1); $('dot').style.opacity = (.55 + .45 * Math.sin(t * 6)).toFixed(3);

  { const e = scene(t, ...S.s0, 0, .2);
    st($('h1'), e.v, 0, e.y, 1.07 - .07 * ez.out(lin(t, .2, .5)));
    st($('h2'), e.v, 0, e.y, 1.07 - .07 * ez.out(lin(t, C.gold0 - .05, C.gold0 + .25)));
    const h = rise(t, C.works0 - .45); st($('hsub'), e.v * h.o, 0, e.y + h.y);
    const p = pop(t, C.before0 - .05); st($('hpill'), e.v * p.o, 0, e.y, p.s * (1 + .03 * Math.sin(Math.PI * lin(t, C.cent, C.cent + .4)))); }

  { const e = scene(t, ...S.s1); const m = pop(t, C.mtg - .25), ar = rise(t, C.arch - .35);
    st($('mono1'), e.v * m.o, 0, e.y, m.s); st($('arch1'), e.v * ar.o, 0, e.y + ar.y); }

  { const e = scene(t, ...S.s2); const k = rise(t, S.s2[0] + .05), d = rise(t, S.s2[0] + .15);
    st($('k2'), e.v * k.o, 0, e.y + k.y); st($('dt2'), e.v * d.o, 0, e.y + d.y);
    [C.eight, C.seven, C.eleven].forEach((a, i) => { const s = slide(t, a - .2, 120); st($('tr' + (i + 1)), e.v * s.o, s.x, e.y); }); }

  { const e = scene(t, ...S.s3);
    const b1 = slide(t, C.curious - .1, -140), b2 = slide(t, C.burned - .4, -140), a1 = slide(t, C.come - .05, 140), a2 = slide(t, C.ask - .15, 140);
    st($('b1'), e.v * b1.o, b1.x, e.y); st($('b2'), e.v * b2.o, b2.x, e.y); st($('a1'), e.v * a1.o, a1.x, e.y); st($('a2'), e.v * a2.o, a2.x, e.y); }

  { const e = scene(t, ...S.s4); const h = pop(t, C.learn3 - .1);
    st($('lh'), e.v * h.o, 0, e.y, h.s * (1 + .04 * Math.sin(Math.PI * lin(t, C.three, C.three + .4))));
    const at = [C.one, C.two, C.threeP];
    st($('pc'), e.v * ez.out(lin(t, C.one - .3, C.one)), 0, e.y);
    at.forEach((a, i) => {
      const nxt = i < 2 ? at[i + 1] - .2 : 1e9, on = t >= a - .12 && t < nxt;
      $('pc' + (i + 1)).className = 'pc' + (on ? ' on' : t >= nxt ? ' done' : '');
      const r = rise(t, a - .05, .32, 50), out = lin(t, nxt, nxt + .2);
      st($('lt' + (i + 1)), e.v * r.o * (1 - out), 0, e.y + r.y - 30 * out);
    }); }

  { const e = scene(t, ...S.s5);
    [[C.trading - .1, 'd1'], [C.learnF - .2, 'd2'], [C.decide - .35, 'd3']].forEach(([a, id]) => { const s = slide(t, a, 120); st($(id), e.v * s.o, s.x, e.y); }); }

  { const e = scene(t, ...S.s6); const j = pop(t, C.join - .1);
    st($('j1'), e.v * j.o, 0, e.y, j.s);
    const ea = pop(t, C.logIn - .1); st($('early'), e.v * ea.o, 0, e.y, ea.s * (1 + .03 * Math.sin(Math.PI * lin(t, C.ten, C.ten + .4))));
    const sh = slide(t, C.send - .1, 160, .36); st($('share'), e.v * sh.o, sh.x, e.y); }

  { const e = scene(t, ...S.s7, .3, .01);
    [.35, .5, .65].forEach((d, i) => { const c = pop(t, C.see + d); st($('ch' + (i + 1)), e.v * c.o, 0, e.y, c.s); });
    const u = rise(t, C.see + .7, .4, 50); st($('u7'), e.v * u.o, 0, e.y + u.y, 1 + .012 * Math.sin(Math.max(0, t - C.see - 1.2) * 3.2));
    const b = rise(t, C.lgtc - .45), s = pop(t, C.lgtc - .05, .5), d = rise(t, C.lgtc + .6);
    st($('e2'), e.v * b.o, 0, e.y + b.y); st($('e3'), e.v * s.o, 0, e.y, s.s); st($('disc'), e.v * d.o, 0, e.y + d.y); }

  captions(t);
  st($('fade'), lin(t, T - .2, T));
};
})();

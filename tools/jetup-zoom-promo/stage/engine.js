/* JetUP Zoom promo: every visual is a pure function of time t (seconds), so any frame renders on its own. */
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
// scene envelope: {v: visibility, y: drift}
function scene(t, a, b, fi = .32, fo = .3) {
  if (t < a || t > b) return { v: 0, y: 0 };
  const i = fi <= 0 ? 1 : ez.out(lin(t, a, a + fi)), o = ez.inOut(lin(t, b - fo, b));
  return { v: Math.min(i, 1 - o), y: 30 * (1 - i) - 40 * o };
}
function pop(t, t0, d = .5) { const k = lin(t, t0, t0 + d); return { o: ez.out(lin(t, t0, t0 + .18)), s: .55 + .45 * ez.back(k), k }; }
function rise(t, t0, d = .45, dist = 36) { const k = ez.out(lin(t, t0, t0 + d)); return { o: k, y: dist * (1 - k) }; }
function slam(t, t0, d = .38, from = 1.45) { const k = ez.out(lin(t, t0, t0 + d)); return { o: lin(t, t0, t0 + .1), s: from + (1 - from) * k }; }

/* ---------- words for captions and cues ---------- */
const W = [];
for (let i = 0; i < TL.words.length; i++) {           // X A U, U S D.  ->  XAU/USD.
  const w = TL.words[i];
  if (w.w === 'X' && TL.words[i + 5] && TL.words[i + 5].w.startsWith('D')) {
    W.push({ w: 'XAU/USD.', a: w.a, b: TL.words[i + 5].b, c: w.c, parts: TL.words.slice(i, i + 6).map(x => x.a) }); i += 5; continue;
  }
  W.push(Object.assign({}, w));
}
const XT = W.find(w => w.w === 'XAU/USD.').parts;   // times of X, A, U, U, S, D
const PH = [];
{ let cur = [];
  W.forEach((w, i) => {
    cur.push(w);
    const nx = W[i + 1], end = /[.!?:]$/.test(w.w) || (/,$/.test(w.w) && cur.length >= 3) || cur.length >= 6 || !nx || nx.c !== w.c || nx.a - w.b > .6;
    if (end) { PH.push(cur); cur = []; }
  });
}
const capbox = $('capbox');
let lastPh = -1;
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
  p.forEach((w, i) => {
    const end = p[i + 1] ? p[i + 1].a : w.b + .25;
    sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? 'done' : 'todo';
  });
  const a = p[0].a - .12, b = p[p.length - 1].b + .35;
  capbox.style.visibility = 'visible';
  capbox.style.opacity = Math.min(lin(t, a, a + .12), 1 - lin(t, b - .12, b)).toFixed(3);
}

/* ---------- scene times ---------- */
const S = { s0: [0, 2.82], s1: [2.6, 6.72], s2: [6.5, 21.52], s3: [21.3, 31.4], s4: [31.18, 36.28], s5: [36.06, 43.68], s6: [43.46, T + .5] };
const tMain = 13.51;   // "The main one"

window.R = function (t) {
  /* background */
  st($('bgc'), 1, 0, -t * 3);
  st($('g1'), 1, 40 * Math.sin(t * .25), 30 * Math.cos(t * .2));
  st($('g2'), 1, -40 * Math.sin(t * .22), 0);
  const tb = 1;
  st($('top'), tb, 0, -20 * (1 - tb));
  $('dot').style.opacity = (.55 + .45 * Math.sin(t * 6)).toFixed(3);

  /* S0 hook */
  { const e = scene(t, ...S.s0, 0, .3);
    const a = slam(t, .22), b = slam(t, .55), g = lin(t, 1.12, 1.72), h = rise(t, 1.78);
    // the first frame already shows the hook (WhatsApp uses it as the preview), then each line punches in on its hit
    st($('h1'), e.v, 0, e.y, 1.07 - .07 * ez.out(lin(t, .22, .5)));
    st($('h2'), e.v, 0, e.y, 1.07 - .07 * ez.out(lin(t, .55, .83)));
    st($('hbar'), e.v * ez.out(lin(t, 1.12, 1.3)), 0, e.y - 420 * (1 - ez.back(g)), 1 + .02 * Math.sin(t * 2));
    st($('hsub'), e.v * h.o, 0, e.y + h.y); }

  /* S1 intro */
  { const e = scene(t, ...S.s1); const p = pop(t, 2.68, .6), n1 = pop(t, C.mtg1 - .12), n2 = rise(t, C.arch1 - .42);
    st($('pc'), e.v * p.o, 0, e.y, p.s * (1 + .025 * lin(t, 2.68, 6.7)));
    st($('n1'), e.v * n1.o, 0, e.y, n1.s);
    st($('n2'), e.v * n2.o, 0, e.y + n2.y); }

  /* S2 the simple picture */
  { const e = scene(t, ...S.s2); const k = rise(t, 6.52);
    st($('k2'), e.v * k.o, 0, e.y + k.y);
    const at = [C.tag - .08, C.account - .45, C.connect - .25, tMain + .04], hl = [C.broker, C.name, C.copyx, C.gold1];
    const gz = C.gold1 - .1;
    for (let i = 0; i < 4; i++) {
      const s = ez.out(lin(t, at[i], at[i] + .45)), n = $('nd' + (i + 1));
      const newer = i < 3 ? at[i + 1] : gz, dim = 1 - .5 * ez.out(lin(t, newer, newer + .4));
      st(n, e.v * s * dim, -70 * (1 - s), e.y, .96 + .04 * s);
      n.classList.toggle('foc', t >= at[i] && t < newer);
      $('nd' + (i + 1) + 's').classList.toggle('hl', t >= hl[i]);
      if (i < 3) { const a = ez.out(lin(t, at[i + 1] - .12, at[i + 1] + .2)); st($('ar' + (i + 1)), e.v * a * dim, 0, e.y - 14 * (1 - a)); }
    }
    const g = lin(t, gz, gz + .6);
    st($('gz'), e.v * ez.out(lin(t, gz, gz + .2)), 0, e.y);
    st($('gbar'), 1, 0, -260 * (1 - ez.back(g)), 1 + .015 * Math.sin(t * 2.2));
    // XAU/USD types in on the spoken letters
    const txt = ['X', 'XA', 'XAU', 'XAU/U', 'XAU/US', 'XAU/USD'];
    let n = 0; XT.forEach((x, i) => { if (t >= x - .02) n = i + 1; });
    $('tickt').textContent = n ? txt[n - 1] : '';
    const tk = ez.out(lin(t, XT[0] - .25, XT[0]));
    st($('tick'), tk, 18 * (1 - tk), 0);
    $('tcur').style.opacity = (n < 6 || t < XT[5] + .6) && Math.floor(t * 3) % 2 === 0 ? 1 : 0;
    const gl = rise(t, C.gold2 - .1);
    st($('gl'), gl.o, 0, gl.y);
    const tg = t - C.dollars, sw = tg < 0 ? 0 : 28 * Math.exp(-2.6 * tg) * Math.cos(9 * tg);
    const tp = pop(t, C.dollars - .08, .45);
    st($('tag'), tp.o, 0, 0, tp.s, sw); }

  /* S3 promo */
  { const e = scene(t, ...S.s3); const k = rise(t, 21.33);
    st($('k3'), e.v * k.o, 0, e.y + k.y);
    const g = pop(t, C.promo - .2, .55), open = lin(t, C.hundred - .32, C.hundred + .2), mv = ez.inOut(lin(t, C.rules - .2, C.rules + .45));
    const wob = t < C.hundred - .32 ? 4 * Math.sin((t - C.promo) * 22) * lin(t, C.promo + .2, C.promo + .5) : 0;
    st($('gift'), e.v * g.o, -240 * mv, e.y - 20 * mv, g.s * (1 - .5 * mv), wob);
    const lid = document.querySelector('.glid');
    lid.style.transform = `translate(${(-24 * ez.out(open)).toFixed(1)}px,${(-80 * ez.out(open)).toFixed(1)}px) rotate(${(-18 * ez.out(open)).toFixed(1)}deg)`;
    lid.style.transformOrigin = '150px 115px'; lid.style.opacity = (1 - lin(t, C.hundred - .05, C.hundred + .25)).toFixed(3);
    const a = pop(t, C.hundred - .25, .5);
    $('amtn').textContent = Math.round(100 * ez.out(lin(t, C.hundred - .25, C.hundred + .35)));
    st($('amt'), e.v * a.o, 150 * mv, e.y - 330 * mv, a.s * (1 - .38 * mv));
    const al = rise(t, C.hundred + .25);
    st($('amtl'), e.v * al.o, 150 * mv, e.y + al.y - 395 * mv, 1 - .2 * mv);
    const r = rise(t, C.rules - .05, .5, 80);
    st($('rules'), e.v * r.o, 0, e.y + r.y);
    const r1 = ez.out(lin(t, C.twelve - .6, C.twelve - .2)), r2 = ez.out(lin(t, C.taking - .45, C.taking - .05));
    st($('rr1'), r1, 60 * (1 - r1), 0);
    st($('rr2'), r2, 60 * (1 - r2), 0, 1 + .02 * Math.sin(Math.PI * lin(t, C.ends, C.ends + .5)));
    $('rr2').classList.toggle('warn', t >= C.ends - .05); }

  /* S4 tonight, the times */
  { const e = scene(t, ...S.s4); const k = rise(t, 31.22), n = slam(t, 31.32, .4, 1.5), d = rise(t, 31.75);
    st($('k4'), e.v * k.o, 0, e.y + k.y);
    st($('tn'), e.v * n.o, 0, e.y, n.s);
    st($('dt'), e.v * d.o, 0, e.y + d.y);
    st($('tc'), e.v * ez.out(lin(t, 32.1, 32.3)), 0, e.y);
    [32.25, 32.7, 33.15].forEach((a, i) => { const s = ez.out(lin(t, a, a + .4)); st($('tr' + (i + 1)), s, -80 * (1 - s), 0); });
    const el = pop(t, 33.75); st($('early'), e.v * el.o, 0, e.y, el.s); }

  /* S5 call to action */
  { const e = scene(t, ...S.s5); const a = rise(t, 36.1), b = pop(t, 36.2), u = pop(t, 36.36, .55);
    st($('c5a'), e.v * a.o, 0, e.y + a.y);
    st($('c5b'), e.v * b.o, 0, e.y, b.s);
    const tapT = C.action, press = 1 - .035 * Math.sin(Math.PI * lin(t, tapT - .05, tapT + .25));
    st($('u5'), e.v * u.o, 0, e.y, u.s * press);
    const hin = ez.inOut(lin(t, 37.15, tapT - .05)), hout = lin(t, tapT + .6, tapT + .95);
    const hs = 1 - .12 * Math.sin(Math.PI * lin(t, tapT - .08, tapT + .22));
    st($('hand'), e.v * Math.min(lin(t, 37.15, 37.35), 1 - hout), 260 * (1 - hin) - 90, e.y + 380 * (1 - hin) - 40, hs, -12 * (1 - hin));
    const rp = lin(t, tapT, tapT + .65);
    st($('rip'), e.v * (rp > 0 && rp < 1 ? 1 - rp : 0), 0, e.y, 1 + 9 * ez.out(rp));
    [38.7, 38.85, 39.0].forEach((c, i) => { const s = pop(t, c, .45); st($('ch' + (i + 1)), e.v * s.o, 0, e.y, s.s); });
    const el = rise(t, 39.25); st($('early5'), e.v * el.o, 0, e.y + el.y);
    const nf = pop(t, C.advice - .45); st($('nfa'), e.v * nf.o, 0, e.y, nf.s); }

  /* S6 end card */
  { const e = scene(t, ...S.s6, .35, .01); const p = pop(t, 43.5, .6), e1 = rise(t, C.me - .05), e2 = pop(t, C.lgtc - .08, .6), u = rise(t, 44.6, .5, 50), d = rise(t, 45.2);
    st($('pc6'), e.v * p.o, 0, e.y, p.s * (1 + .02 * lin(t, 43.5, T)));
    st($('e1'), e.v * e1.o, 0, e.y + e1.y);
    st($('e2'), e.v * e2.o, 0, e.y, e2.s);
    st($('u6'), e.v * u.o, 0, e.y + u.y, 1 + .012 * Math.sin(Math.max(0, t - 45.1) * 3.2));
    st($('disc'), e.v * d.o, 0, e.y + d.y); }

  captions(t);
  st($('fade'), lin(t, T - .2, T));
};
window.READY = true;
})();

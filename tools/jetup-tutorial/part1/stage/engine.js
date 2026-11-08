/* JetUP tutorial part 1: every visual is a pure function of time t (seconds). R(t) resolves when the frame is ready. */
(function () {
'use strict';
const TL = window.TL;
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const ez = {
  out: x => 1 - Math.pow(1 - x, 3), inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.6, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
};
function st(el, o, x = 0, y = 0, s = 1) {
  el.style.opacity = o.toFixed(3);
  el.style.visibility = o <= .002 ? 'hidden' : 'visible';
  el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)})`;
}
function vis(t, a, b, fi = .3, fo = .3) {
  if (t < a || t > b) return 0;
  return Math.min(fi <= 0 ? 1 : ez.out(lin(t, a, a + fi)), fo <= 0 ? 1 : 1 - ez.inOut(lin(t, b - fo, b)));
}
function rise(t, a, b, d = 46, fi = .35, fo = .3) { const v = vis(t, a, b, fi, fo); return { o: v, y: d * (1 - v) }; }

/* ---------- step card ---------- */
let lastStep = null;
function steps(t) {
  const s = TL.steps.find(s => t >= s.t0 && t < s.t1);
  const el = $('step');
  if (!s) { st(el, 0); lastStep = null; return; }
  if (s !== lastStep) {
    $('snum').textContent = s.n; $('st1').innerHTML = s.title; $('st2').innerHTML = s.sub;
    $('sof').textContent = s.n ? `STEP ${s.n} OF ${TL.nsteps}` : '';
    $('snum').style.display = s.n ? '' : 'none';
    lastStep = s;
  }
  const v = vis(t, s.t0, s.t1, .38, .25);
  st(el, v, 60 * (1 - v), 0);
  const k = ez.back(lin(t, s.t0 + .05, s.t0 + .5));
  $('snum').style.transform = `scale(${(.4 + .6 * k).toFixed(3)})`;
  // progress
  const bars = $('prog').children;
  for (let i = 0; i < bars.length; i++) {
    const S = TL.steps.filter(x => x.n === i + 1);
    let f = 0;
    if (S.length) { const a = Math.min(...S.map(x => x.t0)), b = Math.max(...S.map(x => x.t1)); f = lin(t, a, b); }
    bars[i].firstChild.style.transform = `scaleX(${f.toFixed(4)})`;
  }
}

/* ---------- screen window, shots, camera ---------- */
const imA = $('imA'), imB = $('imB'), ov = $('ov');
const VW = 930, VH = 1212;
function camAt(sh, t) {
  const K = sh.cam;
  if (t <= K[0][0]) return K[0].slice(1);
  for (let i = 0; i < K.length - 1; i++) {
    const a = K[i], b = K[i + 1];
    if (t <= b[0]) { const k = ez.inOut(lin(t, a[0], b[0])); return [a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k, a[3] + (b[3] - a[3]) * k]; }
  }
  return K[K.length - 1].slice(1);
}
function view(sh, t) {
  const [cx, cy, s] = camAt(sh, t);
  let X = VW / 2 - cx * s, Y = VH / 2 - cy * s;
  X = clamp(X, VW - 720 * s, 0); Y = clamp(Y, VH - 1562 * s, 0);
  return { X, Y, s };
}
function frameSrc(sh, t) {
  const local = (t - sh.t0) * sh.speed + (sh.src0 - sh.cstart);
  const k = clamp(Math.round(local * TL.fps), 0, sh.n - 1);
  return `../../clips/${sh.clip}/${String(k).padStart(5, '0')}.jpg`;
}
const pend = [];
function setImg(img, src) {
  if (img.dataset.src !== src) { img.dataset.src = src; img.src = src; pend.push(img.decode().catch(() => {})); }
}
function shots(t) {
  const w = TL.win.find(w => t >= w[0] && t <= w[1]);
  const win = $('win');
  if (!w) { st(win, 0); return null; }
  const v = vis(t, w[0], w[1], .45, .35);
  st(win, v, 0, 120 * (1 - v), .94 + .06 * v);
  const i = TL.shots.findIndex(s => t >= s.t0 && t < s.t1);
  if (i < 0) return null;
  const sh = TL.shots[i], prev = TL.shots[i - 1];
  const V = view(sh, t);
  setImg(imA, frameSrc(sh, t));
  imA.style.transform = `translate(${V.X.toFixed(1)}px,${V.Y.toFixed(1)}px) scale(${V.s.toFixed(4)})`;
  const xf = prev && Math.abs(prev.t1 - sh.t0) < .01 && sh.xfade ? lin(t, sh.t0, sh.t0 + sh.xfade) : 1;
  imA.style.opacity = xf.toFixed(3);
  if (xf < 1) {
    const P = view(prev, t);
    setImg(imB, frameSrc(prev, Math.min(t, prev.t1 - .001)));
    imB.style.transform = `translate(${P.X.toFixed(1)}px,${P.Y.toFixed(1)}px) scale(${P.s.toFixed(4)})`;
    imB.style.opacity = 1; imB.style.visibility = 'visible';
  } else { imB.style.visibility = 'hidden'; }
  // flash on a hard cut between different clips
  $('flash').style.opacity = (sh.flash ? .35 * (1 - lin(t, sh.t0, sh.t0 + .25)) : 0).toFixed(3);
  return { sh, V };
}

/* rings, taps and chips live inside the window, in screen-recording coordinates */
const pool = { ring: [], tap: [], chip: [] };
function get(kind, i) {
  while (pool[kind].length <= i) {
    const d = document.createElement('div');
    d.className = kind; if (kind === 'tap') d.innerHTML = '<i></i><b></b>';
    ov.appendChild(d); pool[kind].push(d);
  }
  return pool[kind][i];
}
function overlays(t, cur) {
  let nr = 0, nt = 0, nc = 0;
  if (cur) {
    const { V } = cur;
    for (const r of TL.rings) {
      if (t < r.t0 || t > r.t1) continue;
      const el = get('ring', nr++), v = vis(t, r.t0, r.t1, .3, .25);
      const pad = 10;
      el.className = 'ring' + (r.gold ? ' gold' : '');
      el.style.left = (V.X + r.x0 * V.s - pad) + 'px'; el.style.top = (V.Y + r.y0 * V.s - pad) + 'px';
      el.style.width = ((r.x1 - r.x0) * V.s + 2 * pad) + 'px'; el.style.height = ((r.y1 - r.y0) * V.s + 2 * pad) + 'px';
      const k = ez.back(lin(t, r.t0, r.t0 + .4));
      el.style.opacity = v.toFixed(3); el.style.visibility = 'visible';
      el.style.transform = `scale(${(1.12 - .12 * k).toFixed(3)})`;
    }
    for (const p of TL.taps) {
      if (t < p.t - .35 || t > p.t + .7) continue;
      const el = get('tap', nt++);
      el.style.left = (V.X + p.x * V.s) + 'px'; el.style.top = (V.Y + p.y * V.s) + 'px';
      el.style.visibility = 'visible'; el.style.opacity = 1;
      const pre = lin(t, p.t - .35, p.t), post = lin(t, p.t, p.t + .7);
      const dot = el.children[1], ring = el.children[0];
      dot.style.opacity = (t < p.t ? ez.out(pre) : 1 - post).toFixed(3);
      dot.style.transform = `scale(${(t < p.t ? 1.25 - .25 * ez.out(pre) : 1 - .3 * post).toFixed(3)})`;
      ring.style.opacity = (t < p.t ? 0 : .9 * (1 - post)).toFixed(3);
      ring.style.transform = `scale(${(.3 + 1.1 * ez.out(post)).toFixed(3)})`;
    }
  }
  for (const c of TL.chips) {
    if (t < c.t0 || t > c.t1) continue;
    const el = get('chip', nc++), v = vis(t, c.t0, c.t1, .32, .25);
    el.className = 'chip' + (c.gold ? ' gold' : '');
    if (el.dataset.txt !== c.text) { el.innerHTML = c.text; el.dataset.txt = c.text; }
    el.style.top = c.y + 'px';
    const k = ez.back(lin(t, c.t0, c.t0 + .4));
    el.style.opacity = v.toFixed(3); el.style.visibility = 'visible';
    el.style.transform = `translate(-50%,${(30 * (1 - v)).toFixed(1)}px) scale(${(.7 + .3 * k).toFixed(3)})`;
  }
  for (let i = nr; i < pool.ring.length; i++) pool.ring[i].style.visibility = 'hidden';
  for (let i = nt; i < pool.tap.length; i++) pool.tap[i].style.visibility = 'hidden';
  for (let i = nc; i < pool.chip.length; i++) pool.chip[i].style.visibility = 'hidden';
}

/* ---------- cards ---------- */
const PH_SMALL = { dx: 170 - 540, dy: 250 - 708, s: 200 / 576 };   // the intro photo shrinks to the top left
function cards(t) {
  const S = TL.scenes, C = TL.cues;
  // ----- intro, overview, recap and next video share MTG's photo (large in the greeting, small afterwards) -----
  { const [a, b] = S.intro, [ra, rb] = S.recap, [na, nb] = S.next;
    const inIntro = t >= a && t <= b, inRec = t >= ra && t <= rb, inNext = t >= na && t <= nb;
    const v = Math.max(vis(t, a, b, 0, .35), vis(t, ra, nb, .45, .35));
    const k = inIntro ? ez.inOut(lin(t, C.inthis - .1, C.inthis + .6)) : 1;
    const breathe = 1 + .012 * Math.sin(t * 1.6);
    const sc = (1 - k) * breathe + k * PH_SMALL.s;
    st($('iph'), v, k * PH_SMALL.dx, k * PH_SMALL.dy + (1 - k) * 20 * (1 - ez.out(lin(t, 0, .8))), sc);
    const nm = Math.max(inIntro ? lin(t, C.inthis + .3, C.inthis + .7) : 0, vis(t, ra, nb, .45, .35));
    st($('iname'), Math.min(nm, v), 30 * (1 - nm), 0);
    const g = vis(t, a, C.inthis + .1, 0, .3);
    st($('ipart'), g, 0, 0); st($('ititle'), g, 0, 0);
    const h = rise(t, .3, C.inthis + .1, 40, .4, .3), h2 = rise(t, .7, C.inthis + .1, 30, .4, .3);
    st($('ihi'), h.o, 0, h.y); st($('iarch'), h2.o, 0, h2.y);
    // plan panel: overview (rows pop in as named) and recap (rows tick as named)
    const ov = inIntro ? vis(t, C.inthis + .3, b, .45, .3) : 0, rc = inRec ? vis(t, ra, rb, .45, .35) : 0;
    const pv = Math.max(ov, rc);
    st($('plan'), pv, 0, 50 * (1 - pv));
    if (pv > 0) {
      const head = inRec ? 'WHAT WE COVERED<small>In this video, you learned to:</small>' : 'IN THIS VIDEO<small>Create your JetUP account, step by step</small>';
      if ($('plh').dataset.h !== head) { $('plh').innerHTML = head; $('plh').dataset.h = head; }
      for (let i = 0; i < 9; i++) {
        const row = $('pr' + i);
        if (row.dataset.txt !== TL.plan[i]) { row.lastChild.innerHTML = TL.plan[i]; row.dataset.txt = TL.plan[i]; }
        if (inRec) {
          const tk = C.plan_tick[i], on = t >= tk - .05;
          row.className = 'pr' + (on ? ' ok' : '');
          const p = ez.back(lin(t, tk - .05, tk + .3));
          row.style.opacity = on ? 1 : .45; row.style.visibility = 'visible';
          row.firstChild.style.transform = `scale(${on ? (.6 + .4 * p).toFixed(3) : 1})`;
          row.style.transform = 'none';
        } else {
          const r = rise(t, C.plan_in[i] - .15, b, 30, .3, 0);
          row.className = 'pr'; row.style.opacity = r.o.toFixed(3); row.style.visibility = r.o > .002 ? 'visible' : 'hidden';
          row.style.transform = `translateX(${(40 * (1 - r.o)).toFixed(1)}px)`; row.firstChild.style.transform = 'none';
        }
      }
    }
    const pz = inIntro ? rise(t, C.pause - .2, b, 40, .4, .3) : { o: 0, y: 0 };
    st($('pz'), pz.o, 0, pz.y); }
  // ----- step 1: the Partner link -----
  { const [a, b] = S.link;
    const v1 = rise(t, a + .1, b, 50), v2 = rise(t, C.client - .3, b, 50);
    st($('lk1'), v1.o, 0, v1.y, 1 + .03 * Math.sin(Math.PI * lin(t, C.partner, C.partner + .5)));
    st($('lk2'), v2.o * .92, 0, v2.y);
    const q = rise(t, C.ifme - .2, b, 40), u = rise(t, (C.lk_url || C.ifme + .25) - .3, b, 40), bt = rise(t, (C.lk_btn || C.ifme + .9) - .4, b, 40), n = rise(t, (C.lk_other || C.ifme + 1.4) - .2, b, 30);
    st($('lkq'), q.o, 0, q.y); st($('lku'), u.o, 0, u.y);
    const press = t > C.linktap - .05 && t < C.linktap + .18 ? .95 : 1;
    st($('lkb'), bt.o, 0, bt.y, press); st($('lkn'), n.o, 0, n.y);
    tapAt($('lktap'), t, C.linktap); }
  // ----- tip -----
  { const [a, b] = S.tip; const r = rise(t, a, b, 70, .4, .3); st($('tip'), r.o, 0, r.y); }
  // ----- email -----
  { const [a, b] = S.mail; const r = rise(t, a, b, 70, .4, .3); st($('mail'), r.o, 0, r.y);
    tapAt($('mtap'), t, C.mailtap); }
  // ----- next video -----
  { const [a, b] = S.next;
    const n = rise(t, C.next - .3, b, 60, .4, .35); st($('nx'), n.o, 0, n.y, .92 + .08 * ez.back(lin(t, C.next - .3, C.next + .2)));
    for (let i = 0; i < 3; i++) { const r = rise(t, C.nb[i] - .2, b, 0, .35, .35); st($('nb' + i), r.o, 50 * (1 - r.o), 0); }
    const q = rise(t, C.links_url - .9, b, 30, .4, .35); st($('euq'), q.o, 0, q.y);
    const u = rise(t, C.links_url - .3, b, 40, .4, .35); st($('eu'), u.o, 0, u.y, 1 + .04 * Math.sin(Math.PI * lin(t, C.links_url, C.links_url + .6)));
    { const r = rise(t, (C.every || 1e9) - .2, b, 30, .4, .35); st($('einv'), r.o, 0, r.y); }
    const txt = t < C.share - .2 ? 'Save this video, so it is here when you need it.' : 'Share it with someone who is ready to start.';
    if ($('esv').dataset.t !== txt) { $('esv').textContent = txt; $('esv').dataset.t = txt; }
    const sv = Math.min(rise(t, C.save - .2, b, 30, .35, .35).o, 1);
    const sw = t > C.share - .45 && t < C.share - .2 ? lin(t, C.share - .2, C.share - .45) : 1;
    st($('esv'), sv * (t < C.share - .2 ? sw : vis(t, C.share - .2, b, .25, .35)), 0, 0); }
  // ----- outro -----
  { const [a, b] = S.outro;
    const p = rise(t, a, b, 40, .5, 0); st($('oph'), p.o, 0, p.y, 1 + .012 * Math.sin(t * 1.6));
    const M = [[a, C.o_thanks - .15, 'None of this is financial advice.<br>Always do your own research.'],
               [C.o_thanks - .15, C.o_massive - .15, 'SOC'],
               [C.o_massive - .15, C.o_best - .15, 'Thank yourself for taking<br>massive action today!'],
               [C.o_best - .15, C.o_im - .15, '<div><div style="font:800 46px/1.2 var(--f-b)">I wish you nothing but the best,</div><div class="big goldtxt" style="margin-top:14px">BECAUSE YOU ARE THE BEST</div></div>']];
    const om = $('omsg'); let shown = false;
    for (const [m0, m1, html] of M) {
      if (t >= m0 && t < m1) {
        const key = String(m0);
        if (om.dataset.k !== key) { om.innerHTML = html === 'SOC' ? $('t_soc').innerHTML : html; om.dataset.k = key; }
        const v = vis(t, m0, m1, .3, .25); st(om, v, 0, 24 * (1 - v)); shown = true;
        if (html === 'SOC') {
          [['s_like', C.o_like], ['s_share', C.o_share], ['s_comm', C.o_comment]].forEach(([id, tt]) => {
            const e = document.getElementById(id); if (!e) return;
            const k = ez.back(lin(t, tt - .2, tt + .25)); e.style.opacity = lin(t, tt - .2, tt).toFixed(3); e.style.transform = `scale(${(.5 + .5 * k).toFixed(3)})`;
          });
        }
      }
    }
    if (!shown) st(om, 0);
    const br = rise(t, C.o_im - .2, b, 30, .4, 0); st($('ebrand'), br.o, 0, br.y);
    const ur = rise(t, C.o_im - .1, b, 30, .45, 0); st($('eurl'), ur.o, 0, ur.y, 1 + .04 * Math.sin(Math.PI * lin(t, C.o_im + .2, C.o_im + .9)));
    const sl = rise(t, C.o_lgtc - .25, b, 40, .45, 0); st($('eslog'), sl.o, 0, sl.y, .9 + .1 * ez.back(lin(t, C.o_lgtc - .25, C.o_lgtc + .25)));
    const rk = rise(t, C.o_lgtc + .5, b, 20, .4, 0); st($('erisk'), rk.o, 0, rk.y); }
}
function tapAt(el, t, tt) {
  if (t < tt - .35 || t > tt + .7) { el.style.visibility = 'hidden'; return; }
  el.style.visibility = 'visible'; el.style.opacity = 1;
  const pre = lin(t, tt - .35, tt), post = lin(t, tt, tt + .7);
  el.children[1].style.opacity = (t < tt ? ez.out(pre) : 1 - post).toFixed(3);
  el.children[0].style.opacity = (t < tt ? 0 : .9 * (1 - post)).toFixed(3);
  el.children[0].style.transform = `scale(${(.3 + 1.1 * ez.out(post)).toFixed(3)})`;
}

/* ---------- captions ---------- */
const PH = [];
{ let cur = [];
  TL.words.forEach((w, i) => {
    cur.push(w);
    const nx = TL.words[i + 1], end = /[.!?]$/.test(w.w) || (/[,:]$/.test(w.w) && cur.length >= 4) || cur.length >= 7 || !nx || nx.a - w.b > .5;
    if (end) { PH.push(cur); cur = []; }
  });
}
const capbox = $('capbox'); let lastPh = -1;
function captions(t) {
  let idx = -1;
  for (let i = 0; i < PH.length; i++) {
    const p = PH[i], a = p[0].a - .1, nxt = PH[i + 1] ? PH[i + 1][0].a - .1 : 1e9, b = Math.min(p[p.length - 1].b + .35, nxt);
    if (t >= a && t < b) { idx = i; break; }
  }
  if (idx < 0 || !TL.capOn(t)) { capbox.style.opacity = 0; capbox.style.visibility = 'hidden'; return; }
  const p = PH[idx];
  if (idx !== lastPh) { capbox.innerHTML = p.map(w => `<span>${w.w}</span>`).join(' '); lastPh = idx; }
  const sp = capbox.children;
  p.forEach((w, i) => { const end = p[i + 1] ? p[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  capbox.style.visibility = 'visible';
  capbox.style.opacity = Math.min(lin(t, p[0].a - .1, p[0].a + .05), 1).toFixed(3);
}
TL.capOn = t => !TL.nocap.some(([a, b]) => t >= a && t < b);

/* progress bar segments */
for (let i = 0; i < TL.nsteps; i++) { const d = document.createElement('i'); d.innerHTML = '<b></b>'; $('prog').appendChild(d); }

window.R = function (t) {
  pend.length = 0;
  steps(t);
  const cur = shots(t);
  overlays(t, cur);
  cards(t);
  captions(t);
  const pv = vis(t, TL.scenes.link[0], TL.scenes.recap[0] + .3, .4, .3);
  st($('prog'), pv);
  return Promise.all(pend);
};
})();

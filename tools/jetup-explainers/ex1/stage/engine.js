/* JetUP explainer #1 ("the simple picture"), 16:9. Every visual is a pure function of time t. R(t) resolves when ready. */
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
function rowIn(el, t, a) { const k = ez.out(lin(t, a - .1, a + .3)); el.style.opacity = k.toFixed(3); el.style.transform = `translateX(${(24 * (1 - k)).toFixed(1)}px)`; }

function scenes(t) {
  st($('top'), vis(t, S.hi[0], TL.T + 1, .5, 0));
  // hook
  { const [a, b] = S.hook;
    const r1 = rise(t, 0, b, 30, 0), r2 = rise(t, 0, b, 40, 0), r3 = rise(t, C.h2 - .15, b, 40), r4 = rise(t, C.h3 - .15, b, 30);
    st($('hk1'), r1.o, 0, r1.y); st($('hk2'), r2.o, 0, r2.y, 1 + .04 * Math.sin(Math.PI * lin(t, C.h1 - .05, C.h1 + .6)));
    st($('hk3'), r3.o, 0, r3.y); st($('hk4'), r4.o, 0, r4.y);
    const g = vis(t, 0, b, 0, .3); st($('hbar'), g, 0, 14 * Math.sin(t * 2.2)); }
  // hi
  { const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
    const h = rise(t, a + .25, b, 30), r = rise(t, a + .6, b, 24); st($('hhi'), h.o, 0, h.y); st($('harch'), r.o, 0, r.y); }
  // the simple picture
  { const [a, b] = S.pic;
    const ti = rise(t, a, b, 30); st($('ptitle'), ti.o, 0, ti.y);
    const nodes = [['nJ', C.j_card - .25, C.t_card - .1], ['nT', C.t_card - .25, C.c_copy - .1], ['nX', C.c_copy - .2, C.s_card - .1], ['nS', C.s_card - .25, b]];
    nodes.forEach(([id, t0, tf]) => { const r = pop(t, t0, b, .4, .3); st($(id), r.o, 0, 0, r.s); $(id).classList.toggle('on', t >= t0 + .1 && t < tf); });
    [['rJ1', C.j_comm], ['rJ2', C.j_train], ['rJ3', C.j_ai], ['rJ4', C.j_x1], ['rJ5', C.j_x2], ['rT1', C.t_acc], ['rT2', C.t_name],
     ['rX1', C.c_copy + .3], ['rX2', C.c_cx + .2], ['rS1', C.s_gold]].forEach(([id, c]) => rowIn($(id), t, c));
    const sb = ez.out(lin(t, C.s_gold, C.s_gold + .4)); $('sbar').style.opacity = sb.toFixed(3); $('sbar').style.transform = `scale(${(.6 + .4 * ez.back(lin(t, C.s_gold, C.s_gold + .45))).toFixed(3)})`;
    [['l1', C.t_card - .2], ['l2', C.c_copy - .15], ['l3', C.s_card - .2]].forEach(([id, c]) => {
      const k = ez.out(lin(t, c, c + .45)); st($(id), vis(t, c, b, .05, .3)); $(id).style.transform = `scaleX(${k.toFixed(3)})`; });
    const ac = rise(t, C.t_name + .2, b, 30); st($('acc'), ac.o, 0, ac.y);
    const xu = rise(t, C.s_xau - .1, b, 30); st($('xau'), xu.o, 0, xu.y); }
  // the split
  { const [a, b] = S.split;
    const co = pop(t, a + .05, b, .45, .3); st($('scoin'), co.o, 0, 10 * Math.sin(t * 2), co.s);
    const b7 = rise(t, C.p70 - .2, b, 30), b3 = rise(t, C.p30 - .2, b, 30); st($('b70'), b7.o, 0, b7.y); st($('b30'), b3.o, 0, b3.y);
    $('b70').querySelector('.fill').style.transform = `scaleX(${ez.out(lin(t, C.p70, C.p70 + .8)).toFixed(3)})`;
    $('b30').querySelector('.fill').style.transform = `scaleX(${ez.out(lin(t, C.p30, C.p30 + .8)).toFixed(3)})`;
    [['pb1', C.p_broker], ['pb2', C.p_strat], ['pb3', C.p_partner]].forEach(([id, c]) => {
      const k = ez.out(lin(t, c - .1, c + .3)); $(id).style.opacity = k.toFixed(3); $(id).style.transform = `scale(${(.8 + .2 * ez.back(lin(t, c - .1, c + .35))).toFixed(3)})`; });
    const nf = rise(t, C.p_loss - .2, b, 30); st($('nofee'), nf.o, 0, nf.y); }
  // risk
  { const [a, b] = S.risk;
    const r1 = rise(t, a + .05, b, 30); st($('rk1'), r1.o, 0, r1.y);
    const r2 = rise(t, C.r88 - .3, b, 30); st($('rk88'), r2.o, 0, r2.y);
    $('n88').textContent = Math.round(88 * ez.out(lin(t, C.r88 - .1, C.r88 + 1.0))) + '%';
    const r3 = rise(t, C.r_learn - .2, b, 30); st($('rk3'), r3.o, 0, r3.y); }
  // next
  { const [a, b] = S.next;
    const h = rise(t, a + .05, b, 40); st($('nx1'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, a + .05, a + .5)));
    const s1 = rise(t, a + .55, b, 40), s2 = rise(t, a + .95, b, 40), u = rise(t, a + 1.35, b, 30), n = rise(t, C.n_every - .2, b, 30);
    st($('st1'), s1.o, 0, s1.y); st($('st2'), s2.o, 0, s2.y); st($('nurl'), u.o, 0, u.y, 1 + .03 * Math.sin(Math.PI * lin(t, a + 1.4, a + 2))); st($('ninv'), n.o, 0, n.y); }
  // outro
  { const [a, b] = S.outro;
    const d = pop(t, a + .05, b, .45, .01); st($('odisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
    const M = [[a, C.o_thanks - .15, 'None of this is financial advice.<br>Always do your own research.'],
               [C.o_thanks - .15, C.o_massive - .15, 'SOC'],
               [C.o_massive - .15, C.o_best - .15, 'Thank yourself for taking<br>massive action today!'],
               [C.o_best - .15, C.o_im - .2, '<div><div style="font:800 46px/1.2 var(--f-b)">I wish you nothing but the best,</div><div class="big goldtxt" style="margin-top:16px">because YOU are the best</div></div>']];
    const m = M.find(([x, y]) => t >= x && t < y), om = $('omsg');
    if (m) {
      if (om.dataset.k !== m[2]) { om.innerHTML = m[2] === 'SOC' ? $('t_soc').innerHTML : m[2]; om.dataset.k = m[2]; }
      const v = vis(t, m[0], m[1], .35, .25); st(om, v, 0, 20 * (1 - v));
      if (m[2] === 'SOC') [['s_like', C.o_like], ['s_share', C.o_share], ['s_comm', C.o_comment]].forEach(([id, tt]) => {
        const el = $(id); if (!el) return; const k = lin(t, tt - .15, tt + .2); el.style.opacity = (.25 + .75 * k).toFixed(3);
        el.style.transform = `scale(${(1 + .18 * Math.sin(Math.PI * lin(t, tt - .15, tt + .35))).toFixed(3)})`; });
    } else st(om, 0);
    const br = rise(t, C.o_im - .2, b, 30, .4, .01); st($('obrand'), br.o, 0, br.y);
    const sl = rise(t, C.o_lgtc - .25, b, 40, .45, .01); st($('oslog'), sl.o, 0, sl.y, .9 + .1 * ez.back(lin(t, C.o_lgtc - .25, C.o_lgtc + .25)));
    const ur = rise(t, C.o_im - .1, b, 30, .45, .01); st($('ourl'), ur.o, 0, ur.y, 1 + .04 * Math.sin(Math.PI * lin(t, C.o_im + .2, C.o_im + .9)));
    const rk = rise(t, C.o_lgtc + .5, b, 20, .4, .01); st($('orisk'), rk.o, 0, rk.y); }
}

/* captions: the current line, the spoken word lit */
const capbox = $('capbox');
let lastCap = null;
function captions(t) {
  const c = TL.caps.find(c => t >= c.a && t < c.b);
  if (!c || (TL.capoff && t >= TL.capoff)) { capbox.style.visibility = 'hidden'; lastCap = null; return; }
  if (c !== lastCap) { capbox.innerHTML = c.w.map(w => `<span>${w.w}</span>`).join(' '); lastCap = c; }
  const sp = capbox.children;
  c.w.forEach((w, i) => { const end = c.w[i + 1] ? c.w[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  capbox.style.visibility = 'visible';
  capbox.style.opacity = Math.min(lin(t, c.a, c.a + .12), 1 - lin(t, c.b - .12, c.b)).toFixed(3);
}


/* emoji pops on key words, as in the sign-up training: above the caption box, at its right edge, for 2 s */
const emoEl = document.createElement('div'); emoEl.id = 'emo';
emoEl.style.cssText = 'position:absolute;left:0;top:0;width:96px;height:96px;font:84px/96px "Noto Color Emoji";text-align:center;visibility:hidden;transform-origin:100% 100%;z-index:60';
document.body.appendChild(emoEl);
function emojis(t) {
  const E = (TL.emos || []).filter(([t0]) => t >= t0 && t <= t0 + 2).pop();
  if (!E || capbox.style.visibility !== 'visible' || (TL.kit && t >= TL.kit[0])) { emoEl.style.visibility = 'hidden'; return; }
  const age = t - E[0];
  if (emoEl.textContent !== E[1]) emoEl.textContent = E[1];
  const a = Math.min(1, age / .15) * Math.min(1, (2 - age) / .3), s = .4 + .6 * ez.back(clamp(age / .4));
  const r = capbox.getBoundingClientRect();
  emoEl.style.left = (r.right + 6 - 96).toFixed(1) + 'px';
  emoEl.style.top = (r.top - 96 - 14 - 8 * ez.out(clamp(age / 2))).toFixed(1) + 'px';
  emoEl.style.transform = `scale(${s.toFixed(3)})`; emoEl.style.opacity = a.toFixed(3); emoEl.style.visibility = 'visible';
}
const pend = [];
window.R = function (t) {
  pend.length = 0; scenes(t); captions(t); emojis(t);
  return Promise.all([...document.images].map(i => i.decode().catch(() => {})));
};
})();

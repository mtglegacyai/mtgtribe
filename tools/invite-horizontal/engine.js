/* MTG TRIBE invite, horizontal: deterministic frame engine.
   Every visual is a pure function of time t (seconds), so any frame can be rendered on its own. */
(function () {
'use strict';
const TM = window.TIMING, CO = TM.CO, TOTAL = TM.TOTAL, V = window.ORIENT === 'v', W = V ? 1080 : 1920, H = V ? 1920 : 1080;
const E = window.E = {}; E.V = V; E.W = W; E.H = H;

/* ---------- time maps ---------- */
E.S = function (s) {               // source voice time -> output time
  for (const g of TM.SEG) { if (s < g.a) return g.o; if (s <= g.b) return g.o + s - g.a; }
  return TOTAL;
};
E.src = function (t) {             // output time -> source time (null in the cold open)
  if (t < CO) return null;
  for (const g of TM.SEG) { const e = g.o + (g.b - g.a); if (t >= g.o && t < e + 1e-6) return g.a + t - g.o; }
  return null;
};
E.CO = CO; E.TOTAL = TOTAL;

/* ---------- maths ---------- */
const clamp = E.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = E.lin = (t, a, b) => clamp((t - a) / (b - a));
const mix = E.mix = (a, b, k) => a + (b - a) * k;
const ez = E.ez = {
  out: x => 1 - Math.pow(1 - x, 3), in: x => x * x * x, inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  expo: x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x), sine: x => .5 - Math.cos(Math.PI * x) / 2,
  elastic: x => x === 0 ? 0 : x >= 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI) / 3) + 1
};
E.win = function (t, t0, t1, fi = .45, fo = .4) {   // 0..1 visibility of a window with fades
  if (t < t0 - .001 || t > t1 + fo) return 0;
  return Math.min(ez.out(lin(t, t0, t0 + fi)), 1 - ez.inOut(lin(t, t1, t1 + fo)));
};
E.pop = function (t, t0, d = .5) {                   // spring pop-in: {o, s}
  const k = lin(t, t0, t0 + d);
  return { o: ez.out(lin(t, t0, t0 + .16)), s: k <= 0 ? .4 : .4 + .6 * ez.back(k), k };
};
let seed = 1;
E.rng = function (s) { let a = s >>> 0; return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; };

/* ---------- DOM helpers ---------- */
E.el = function (parent, cls, html, css) {
  const d = document.createElement('div'); d.className = 'a ' + (cls || '');
  if (html != null) d.innerHTML = html;
  if (css) d.style.cssText += css;
  parent.appendChild(d); return d;
};
E.ic = function (name, cls, extra) {
  const i = window.ICONS[name]; if (!i) return '';
  if (i.t === 's') return `<svg class="ic ${cls || ''}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" ${extra || ''}><path d="${i.d}"/></svg>`;
  return `<svg class="ic ${cls || ''}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" ${extra || ''}>${i.d}</svg>`;
};
E.set = function (el, o) {        // x,y translate; s scale; r rotate; ry rotateY; o opacity; b blur
  let tr = '';
  if (o.p) tr += `perspective(${o.p}px) `;
  tr += `translate(${(o.x || 0).toFixed(2)}px,${(o.y || 0).toFixed(2)}px)`;
  if (o.s != null) tr += ` scale(${o.s.toFixed(4)})`;
  if (o.sx != null) tr += ` scale(${o.sx.toFixed(4)},${(o.sy == null ? 1 : o.sy).toFixed(4)})`;
  if (o.r) tr += ` rotate(${o.r.toFixed(3)}deg)`;
  if (o.ry) tr += ` rotateY(${o.ry.toFixed(3)}deg)`;
  if (o.rx) tr += ` rotateX(${o.rx.toFixed(3)}deg)`;
  el.style.transform = tr;
  if (o.o != null) { el.style.opacity = clamp(o.o).toFixed(3); el.style.visibility = o.o <= .002 ? 'hidden' : 'visible'; }
  if (o.b != null) el.style.filter = o.b > .05 ? `blur(${o.b.toFixed(2)}px)` : '';
};
E.shine = function (el, t, t0, d = 1.1) {      // gold light sweep across .gt/.st text
  const k = lin(t, t0, t0 + d);
  el.style.backgroundPosition = `${(150 - 200 * ez.inOut(k)).toFixed(1)}% 0,0 0`;
};
E.words = function (el, text, cls) {           // split into word spans for kinetic type
  el.innerHTML = '<span>' + text.split(' ').map(w => `<span class="w ${cls || ''}" style="display:inline-block">${w}</span>`).join(' ') + '</span>';
  return Array.from(el.querySelectorAll('.w'));
};

/* ---------- registries ---------- */
const SCENES = E.SCENES = [];
E.scene = function (name, t0, t1, build, update) { SCENES.push({ name, t0, t1, build, update, el: null, built: false }); };
const SFX = window.SFX = [];
E.cue = function (name, t, gain = 1, extra) { SFX.push(Object.assign({ name, t: +t.toFixed(3), gain }, extra || {})); };
const HITS = [];                                   // camera shake impulses
E.shake = function (t, amp = 10) { HITS.push({ t, amp }); };
const FLASH = [];
E.flash = function (t, dur = .5, peak = .6, color = '255,214,140') { FLASH.push({ t, dur, peak, color }); };
const CHAP = [];
E.chapter = function (t, text) { CHAP.push({ t, text }); };

/* ---------- avatar ---------- */
// frames: 1000x564 upscale of the original avatar panel, 30 fps, index = round(source*30)
const AVL = { // target rect and source viewport (in 1000x564 frame space)
  hidden: null,
  hero: { x: 370, y: 132, w: 1180, h: 666, r: 30, v: [0, 0, 1000, 564] },
  split: { x: 96, y: 176, w: 1000, h: 564, r: 30, v: [0, 0, 1000, 564] },
  pip: { x: 84, y: 760, w: 236, h: 236, r: 118, v: [352, 44, 356, 356] }
};
if (V) Object.assign(AVL, {   // phone: MTG big on top, the host bubble sits above the captions
  hero: { x: 40, y: 330, w: 1000, h: 760, r: 36, v: [143, 0, 742, 564] },
  split: { x: 40, y: 180, w: 1000, h: 564, r: 30, v: [0, 0, 1000, 564] },
  pip: { x: 440, y: 1186, w: 200, h: 200, r: 100, v: [352, 44, 356, 356] }
});
const AVK = E.AVK = [];   // keyframes {t, mode, d}
E.av = function (t, mode, d = .55) { AVK.push({ t, mode, d }); };
const avEl = document.getElementById('av'), avImg = document.getElementById('avimg'), avRing = document.getElementById('avring');
let lastSrc = '';
function lerpLayout(A, B, k) {
  return { x: mix(A.x, B.x, k), y: mix(A.y, B.y, k), w: mix(A.w, B.w, k), h: mix(A.h, B.h, k), r: mix(A.r, B.r, k), v: A.v.map((q, i) => mix(q, B.v[i], k)) };
}
function avState(t) {
  const ks = AVK; let prevMode = 'hidden', prevLay = AVL.split, cur = null;
  let L = null, vis = 0;
  for (let i = 0; i < ks.length; i++) {
    const k = ks[i]; if (t < k.t) break;
    const fromMode = prevMode, fromLay = prevLay;
    const toMode = k.mode, toLay = AVL[toMode] || fromLay;
    const p = ez.inOut(lin(t, k.t, k.t + k.d));
    if (fromMode === 'hidden' && toMode !== 'hidden') { L = toLay; vis = p; }
    else if (toMode === 'hidden') { L = fromLay; vis = 1 - p; }
    else { L = lerpLayout(fromLay, toLay, p); vis = 1; }
    prevMode = toMode; prevLay = toLay; cur = { from: fromMode, to: toMode, p };
  }
  return { L: L || AVL.split, vis, cur };
}
E.avatarAt = function (t) {
  const s = E.src(t);
  const st = avState(t);
  let vis = st.vis;
  if (s == null || s < .78 || s > 154.40) vis = 0;
  if (vis <= .003) { avEl.style.visibility = 'hidden'; avRing.style.visibility = 'hidden'; return Promise.resolve(); }
  const L = st.L, cur = st.cur || {};
  // entering/leaving: scale + blur from the centre
  const sc = .9 + .1 * vis, cx = L.x + L.w / 2, cy = L.y + L.h / 2;
  const w = L.w * sc, h = L.h * sc, x = cx - w / 2, y = cy - h / 2;
  avEl.style.visibility = 'visible';
  avEl.style.left = x.toFixed(1) + 'px'; avEl.style.top = y.toFixed(1) + 'px';
  avEl.style.width = w.toFixed(1) + 'px'; avEl.style.height = h.toFixed(1) + 'px';
  avEl.style.borderRadius = (L.r * sc).toFixed(1) + 'px';
  avEl.style.opacity = vis.toFixed(3);
  avEl.style.filter = vis < .98 ? `blur(${((1 - vis) * 14).toFixed(1)}px)` : '';
  const [vx, vy, vw, vh] = L.v, kx = w / vw, ky = h / vh;
  avImg.style.width = (1000 * kx).toFixed(1) + 'px'; avImg.style.height = (564 * ky).toFixed(1) + 'px';
  avImg.style.left = (-vx * kx).toFixed(1) + 'px'; avImg.style.top = (-vy * ky).toFixed(1) + 'px';
  // gold frame + glow
  const rr = L.r * sc;
  avRing.style.visibility = 'visible'; avRing.style.opacity = vis.toFixed(3);
  avRing.innerHTML = `<defs><linearGradient id="avg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe7b0"/><stop offset=".5" stop-color="#f2ad3c"/><stop offset="1" stop-color="#8a5a18"/></linearGradient>
    <filter id="avf" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter></defs>
    <rect x="${x - 1}" y="${y - 1}" width="${w + 2}" height="${h + 2}" rx="${rr + 1}" fill="none" stroke="#f2ad3c" stroke-opacity=".45" stroke-width="10" filter="url(#avf)"/>
    <rect x="${x - 1.5}" y="${y - 1.5}" width="${w + 3}" height="${h + 3}" rx="${rr + 1.5}" fill="none" stroke="url(#avg)" stroke-width="3"/>`;
  const idx = Math.max(23, Math.min(4632, Math.round(s * 30)));
  const srcp = 'av/' + String(idx).padStart(5, '0') + '.jpg';
  if (srcp === lastSrc) return Promise.resolve();
  lastSrc = srcp; avImg.src = srcp;
  return avImg.decode().catch(() => {});
};

/* ---------- background ---------- */
const bg = document.getElementById('bg').getContext('2d');
const dust = []; { const r = E.rng(7); for (let i = 0; i < 150; i++) dust.push({ x: r() * W, y: r() * H, z: .3 + r() * .9, ph: r() * 6.28, sp: .4 + r() * 1.2 }); }
E.bgParams = function () { return { warm: 1, cool: 0, grid: .5, dust: 1 }; };
function drawBg(t) {
  const P = E.bgParams(t);
  bg.globalCompositeOperation = 'source-over'; bg.globalAlpha = 1;
  const g = bg.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, `rgb(${Math.round(mix(12, 10, P.cool))},${Math.round(mix(9, 11, P.cool))},${Math.round(mix(6, 14, P.cool))})`);
  g.addColorStop(1, '#040302');
  bg.fillStyle = g; bg.fillRect(0, 0, W, H);
  // drifting light pools
  const pools = [[.72 + .06 * Math.sin(t * .11), .22 + .05 * Math.cos(t * .13), 760, .2], [.2 + .05 * Math.cos(t * .09), .78 + .04 * Math.sin(t * .1), 640, .1], [.5 + .2 * Math.sin(t * .05), .5, 900, .06]];
  for (const [px, py, rad, al] of pools) {
    const rg = bg.createRadialGradient(px * W, py * H, 0, px * W, py * H, rad);
    const a = al * P.warm;
    rg.addColorStop(0, `rgba(242,173,60,${a})`); rg.addColorStop(1, 'rgba(242,173,60,0)');
    bg.fillStyle = rg; bg.fillRect(0, 0, W, H);
    if (P.cool > 0) { const cg = bg.createRadialGradient(px * W, py * H, 0, px * W, py * H, rad); cg.addColorStop(0, `rgba(120,140,170,${al * .5 * P.cool})`); cg.addColorStop(1, 'rgba(120,140,170,0)'); bg.fillStyle = cg; bg.fillRect(0, 0, W, H); }
  }
  // blueprint grid
  if (P.grid > 0) {
    bg.strokeStyle = `rgba(255,236,200,${.035 * P.grid})`; bg.lineWidth = 1; bg.beginPath();
    const off = (t * 6) % 64;
    for (let x = -64 + off; x < W; x += 64) { bg.moveTo(x, 0); bg.lineTo(x, H); }
    for (let y = 0; y < H; y += 64) { bg.moveTo(0, y); bg.lineTo(W, y); }
    bg.stroke();
    const m = bg.createRadialGradient(W / 2, H * .45, 200, W / 2, H * .45, V ? 1250 : 1100); m.addColorStop(0, 'rgba(5,4,3,0)'); m.addColorStop(1, 'rgba(5,4,3,.95)');
    bg.fillStyle = m; bg.fillRect(0, 0, W, H);
  }
  // gold dust
  if (P.dust > 0) for (const d of dust) {
    const y = ((d.y - t * 14 * d.sp * d.z) % H + H) % H, x = d.x + Math.sin(t * .3 + d.ph) * 18 * d.z;
    const a = (.25 + .45 * (.5 + .5 * Math.sin(t * 1.3 * d.sp + d.ph))) * P.dust * d.z;
    bg.fillStyle = `rgba(255,217,142,${(a * .6).toFixed(3)})`; bg.beginPath(); bg.arc(x, y, 1.1 + 1.5 * d.z, 0, 6.283); bg.fill();
  }
}

/* ---------- fx: grain, vignette, flashes ---------- */
const fx = document.getElementById('fx').getContext('2d');
const grain = []; { const r = E.rng(11); for (let k = 0; k < 6; k++) { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); const id = g.createImageData(256, 256); for (let i = 0; i < id.data.length; i += 4) { const v = r() * 255; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; } g.putImageData(id, 0, 0); grain.push(fx.createPattern(c, 'repeat')); } }
function drawFx(t) {
  fx.clearRect(0, 0, W, H);
  const v = V ? fx.createRadialGradient(W / 2, H / 2, 520, W / 2, H / 2, 1250) : fx.createRadialGradient(W / 2, H / 2, 420, W / 2, H / 2, 1180); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.62)');
  fx.fillStyle = v; fx.fillRect(0, 0, W, H);
  // caption bed
  if (t > CO - .2) { const y0 = V ? 1330 : 840; const b = fx.createLinearGradient(0, y0, 0, H); b.addColorStop(0, 'rgba(0,0,0,0)'); b.addColorStop(V ? .5 : 1, 'rgba(0,0,0,.55)'); if (V) b.addColorStop(1, 'rgba(0,0,0,.35)'); fx.fillStyle = b; fx.fillRect(0, y0, W, H - y0); }
  for (const f of FLASH) {
    const k = (t - f.t) / f.dur; if (k < -.08 || k > 1) continue;
    const a = k < 0 ? f.peak * (1 + k / .08) : f.peak * Math.pow(1 - k, 2);
    fx.fillStyle = `rgba(${f.color},${a.toFixed(3)})`; fx.fillRect(0, 0, W, H);
  }
  const endK = clamp((t - (TOTAL - .75)) / .7); if (endK > 0) { fx.fillStyle = `rgba(0,0,0,${endK.toFixed(3)})`; fx.fillRect(0, 0, W, H); }
  fx.globalAlpha = .035; fx.globalCompositeOperation = 'overlay';
  fx.fillStyle = grain[Math.floor(t * 12) % grain.length]; fx.fillRect(0, 0, W, H);
  fx.globalAlpha = 1; fx.globalCompositeOperation = 'source-over';
}

/* ---------- captions ---------- */
const capEl = document.getElementById('cap');
let capIdx = -2;
E.capHide = []; // [t0,t1] windows with no captions
function drawCaps(t) {
  const C = TM.CHUNKS; let idx = -1;
  for (let i = 0; i < C.length; i++) { const nx = C[i + 1]; const end = nx ? Math.min(nx.s - .02, C[i].e + .9) : C[i].e + 1.2; if (t >= C[i].s - .08 && t < end) { idx = i; break; } }
  for (const [a, b] of E.capHide) if (t >= a && t < b) idx = -1;
  if (idx !== capIdx) {
    capIdx = idx;
    capEl.innerHTML = idx < 0 ? '' : '<div class="ln">' + C[idx].w.map(w => `<span class="w">${w.w}</span>`).join('') + '</div>';
  }
  if (idx < 0) return;
  const c = C[idx], ln = capEl.firstChild, spans = ln.children;
  const k = ez.out(lin(t, c.s - .08, c.s + .14));
  ln.style.opacity = k.toFixed(3); ln.style.transform = `translateY(${(1 - k) * 14}px)`;
  for (let i = 0; i < c.w.length; i++) {
    const w = c.w[i], sp = spans[i];
    const on = t >= w.s - .03, cur = on && (i === c.w.length - 1 ? t < w.e + .25 : t < c.w[i + 1].s - .03);
    sp.style.color = cur ? '#ffd98e' : on ? '#ffffff' : 'rgba(255,255,255,.5)';
    const pk = cur ? Math.sin(Math.PI * clamp((t - w.s) / Math.max(.12, w.e - w.s))) : 0;
    sp.style.transform = `translateY(${(-4 * pk).toFixed(2)}px)`;
  }
}

/* ---------- hud ---------- */
const hud = { brand: document.getElementById('brand'), chap: document.getElementById('chap'), chapt: document.getElementById('chapt'), url: document.getElementById('url'), prog: document.getElementById('prog') };
hud.url.innerHTML = E.ic('whatsapp') + '<span>mtgtribe.com/group</span>';
let chapNow = null;
function drawHud(t) {
  const on = E.win(t, CO + .4, TOTAL - 6.6, .8, .6);
  E.set(hud.brand, { o: on, x: (1 - on) * -20 });
  E.set(hud.url, { o: on * .95 });
  hud.prog.style.width = (W * clamp(t / TOTAL)).toFixed(1) + 'px'; hud.prog.style.opacity = t > CO ? .9 : 0;
  let c = null; for (const ch of CHAP) if (t >= ch.t) c = ch;
  if (c && c.text !== chapNow) { chapNow = c.text; hud.chapt.textContent = c.text; }
  if (c) { const k = ez.out(lin(t, c.t, c.t + .5)); E.set(hud.chap, { o: on * k, x: (1 - k) * 30 }); } else E.set(hud.chap, { o: 0 });
}

/* ---------- frame ---------- */
const root = document.getElementById('scenes');
E.renderAt = async function (t) {
  E.lastT = t;
  drawBg(t);
  // camera shake from impacts
  let sx = 0, sy = 0;
  for (const h of HITS) { const d = t - h.t; if (d < 0 || d > .6) continue; const a = h.amp * Math.exp(-d * 9); sx += a * Math.sin(d * 63); sy += a * .6 * Math.cos(d * 51); }
  root.style.transform = (sx || sy) ? `translate(${sx.toFixed(2)}px,${sy.toFixed(2)}px)` : '';
  for (const s of SCENES) {
    const on = t >= s.t0 - .8 && t <= s.t1 + .9;
    if (on && !s.built) { s.el = document.createElement('div'); s.el.className = 'sc'; root.appendChild(s.el); s.build(s.el, s); s.built = true; }
    if (!s.built) continue;
    s.el.style.display = on ? 'block' : 'none';
    if (on) s.update(t, s.el, s);
    else if (s.overlays) s.overlays.forEach(o => { o.style.visibility = 'hidden'; });
  }
  const p = E.avatarAt(t);
  drawCaps(t); drawHud(t); drawFx(t);
  await p;
  await new Promise(r => requestAnimationFrame(() => r()));
};
E.ready = function () { return document.fonts.ready; };
E.prebuild = function () { for (const s of SCENES) if (!s.built) { s.el = document.createElement('div'); s.el.className = 'sc'; root.appendChild(s.el); s.build(s.el, s); s.built = true; s.el.style.display = 'none'; } };
window.renderAt = E.renderAt;
})();

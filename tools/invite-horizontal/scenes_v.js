/* MTG TRIBE invite, VERTICAL 1080x1920: the same scenes and timing as scenes.js, laid out for a phone.
   The soundtrack is the same mix as the horizontal cut, so no sound cues are registered here. */
(function () {
'use strict';
const { S, el, ic, set, win, pop, lin, ez, mix, clamp, shine, words, shake, flash, chapter, av, CO, TOTAL } = E;
const RV = { x: 40, y: 790, w: 1000, h: 590, cx: 540 };          // stage under the avatar when MTG is on top

/* ---------- helpers ---------- */
function box(p, cx, cy, w, h, cls, html, css) { return el(p, 'cx ' + (cls || ''), html, `left:${cx - w / 2}px;top:${cy - h / 2}px;width:${w}px;height:${h}px;` + (css || '')); }
function up(e, t, t0, d = .4, dist = 26) { const k = ez.out(lin(t, t0, t0 + d)); set(e, { o: k, y: (1 - k) * dist, b: (1 - k) * 8 }); return k; }
function slam(e, t, t0, from = 1.7, extra) { const k = lin(t, t0, t0 + .22); const s = from - (from - 1) * ez.out(k); set(e, Object.assign({ o: lin(t, t0 - .01, t0 + .07), s: k <= 0 ? from : s, b: (1 - ez.out(k)) * 6 }, extra || {})); return k; }
function pp(e, t, t0, extra) { const p = pop(t, t0); set(e, Object.assign({ o: p.o, s: p.s }, extra || {})); return p.k; }
const out = (t, t1, d = .3) => 1 - ez.inOut(lin(t, t1, t1 + d));
function svgLayer(p, css) { const d = el(p, '', '<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;overflow:visible"></svg>', 'width:1080px;height:1920px;' + (css || '')); return d.firstChild; }
const NS = 'http://www.w3.org/2000/svg';
function sv(parent, tag, attrs) { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); parent.appendChild(n); return n; }
function defs(svg, html) { const d = sv(svg, 'defs', {}); d.innerHTML = html; return d; }
const GOLD_DEFS = `<linearGradient id="gg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe7b0"/><stop offset=".55" stop-color="#f2ad3c"/><stop offset="1" stop-color="#a8681a"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>`;
const capHide = E.capHide;
const cardCss = 'border-radius:28px;background:linear-gradient(160deg,rgba(52,42,26,.92),rgba(16,13,9,.95));box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.4),0 18px 40px rgba(0,0,0,.5)';

E.bgParams = function (t) {
  if (t < CO + .3) { const w = lin(t, 3.6, 5.4); return { warm: .25 + .75 * w, cool: 1 - w, grid: 0, dust: .25 + .75 * w }; }
  if (t > S(49.8) && t < S(58.0)) return { warm: 1, cool: 0, grid: 0, dust: .5 };
  if (t > S(63.0) && t < S(71.6)) return { warm: 1, cool: 0, grid: 1, dust: .8 };
  return { warm: 1, cool: 0, grid: .45, dust: 1 };
};

/* ===================== 0. COLD OPEN ===================== */
E.scene('cold', 0, CO + .2, (r, s) => {
  s.cv = el(r, '', '<canvas width="1080" height="1920"></canvas>', 'width:1080px;height:1920px').firstChild;
  s.b1 = box(r, 540, 900, 960, 220, '', '', 'font:700 80px/1.15 var(--f-b);color:#e9e4dc;letter-spacing:-.01em');
  s.b1w = words(s.b1, "Maybe you've been burned before.");
  s.b2 = ['LOST MONEY.', 'LOST TRUST.', 'EVEN GOT BANNED.'].map((x, i) => box(r, 540, 730 + i * 190, 1060, 180, 'disp', x, 'font-size:128px;color:#9a938a;letter-spacing:.02em'));
  s.k2 = s.b2.map((b, i) => box(r, 540, 730 + i * 190, 10, 12, '', '', 'background:linear-gradient(90deg,#ff6a3d,#ffb36b);border-radius:6px;box-shadow:0 0 24px rgba(255,90,40,.8)'));
  s.b3a = box(r, 540, 790, 1000, 100, '', 'But here you are.', 'font:700 82px/1 var(--f-b);color:#fff');
  s.b3b = box(r, 540, 1000, 1060, 320, 'disp gt', '<span>Still<br>watching.</span>', 'font-size:176px;line-height:.92');
  s.b4a = box(r, 540, 680, 1000, 70, '', 'That means you', 'font:600 60px/1 var(--f-b);color:#d9d2c6');
  s.b4b = box(r, 540, 910, 1060, 380, 'disp gt', "<span>Haven't<br>given up</span>", 'font-size:200px;line-height:.9');
  s.b4c = box(r, 540, 1150, 1000, 70, '', 'on yourself.', 'font:600 60px/1 var(--f-b);color:#d9d2c6');
  s.b5 = box(r, 540, 920, 1060, 460, 'disp st', "<span>You're<br>not done.</span>", 'font-size:228px;line-height:.9');
  s.b6a = box(r, 540, 850, 1060, 110, '', "It's not over", 'font:800 98px/1 var(--f-b);color:#fff');
  s.b6b = box(r, 540, 980, 1060, 110, '', "until it's over.", 'font:800 98px/1 var(--f-b);color:#ffd98e;text-shadow:0 0 40px rgba(242,173,60,.45)');
  s.b7 = box(r, 540, 850, 960, 190, '', '<span>The best time to start was <span class="yd" style="position:relative;display:inline-block">yesterday<i style="position:absolute;left:-4px;right:-4px;top:52%;height:6px;border-radius:3px;background:#ffb36b;transform-origin:0 50%;transform:scaleX(0)"></i></span>.</span>', 'font:600 70px/1.2 var(--f-b);color:#bdb5a8');
  s.yd = s.b7.querySelector('.yd'); s.ydl = s.b7.querySelector('.yd i');
  s.b8 = box(r, 540, 1070, 1060, 100, '', 'The next best time?', 'font:800 86px/1 var(--f-b);color:#fff');
  s.b9 = box(r, 540, 940, 1080, 560, 'disp gt', 'NOW.', 'font-size:440px;line-height:1');
  [2.05, 2.5, 2.95].forEach((x, i) => shake(x, 5 + i * 2));
  shake(7.15, 14); flash(7.15, .25, .18, '255,255,255');
  shake(12.45, 24); flash(12.45, .7, .55);
}, (t, r, s) => {
  const c = s.cv.getContext('2d'); c.clearRect(0, 0, 1080, 1920);
  const ea = 1 - lin(t, 3.4, 4.4);
  if (ea > 0) {
    const rnd = E.rng(5);
    for (let i = 0; i < 90; i++) {
      const sp = .06 + rnd() * .1, off = rnd(), x0 = rnd() * 1080, ph = rnd() * 6.28, sz = .9 + rnd() * 2.8;
      const k = (t * sp + off) % 1, y = 1960 - k * 1650, x = x0 + Math.sin(t * 1.2 + ph) * 30 + k * 60;
      const a = ea * Math.sin(Math.PI * k) * (.5 + .5 * Math.sin(t * 9 + ph));
      c.fillStyle = `rgba(255,${Math.round(120 + 80 * (1 - k))},60,${(a * .8).toFixed(3)})`; c.beginPath(); c.arc(x, y, sz, 0, 6.283); c.fill();
    }
  }
  s.b1w.forEach((w, i) => { const t0 = .3 + i * .13, k = ez.out(lin(t, t0, t0 + .3)), g = out(t, 1.8, .25); set(w, { o: k * g, y: (1 - k) * 18 - (1 - g) * 14, b: (1 - k) * 8 + (1 - g) * 10 }); });
  s.b2.forEach((b, i) => {
    const t0 = 2.05 + i * .45, k = slam(b, t, t0, 1.45), f = lin(t, 3.62 + i * .04, 3.95);
    set(b, { o: lin(t, t0, t0 + .06) * (1 - f), s: k <= 0 ? 1.45 : 1.45 - .45 * ez.out(k), y: f * f * 140, r: f * (i - 1) * 6, b: f * 6 });
    const sk = ez.out(lin(t, 3.32 + i * .06, 3.5 + i * .06)), w = (b.textContent.length * 57 + 40) * sk;
    s.k2[i].style.width = w + 'px'; s.k2[i].style.left = (540 - w / 2) + 'px';
    set(s.k2[i], { o: sk > 0 ? 1 - f : 0, y: f * f * 140, r: f * (i - 1) * 6 });
  });
  { const g = out(t, 5.15, .25); up(s.b3a, t, 3.9, .45); s.b3a.style.opacity *= g;
    const k = ez.out(lin(t, 4.42, 4.9)); set(s.b3b, { o: k * g, s: .9 + .1 * k, b: (1 - k) * 10 }); shine(s.b3b, t, 4.55, 1.2); }
  { const g = out(t, 6.95, .22); up(s.b4a, t, 5.35); s.b4a.style.opacity *= g;
    const k = ez.out(lin(t, 5.62, 6.0)); set(s.b4b, { o: k * g, s: 1.08 - .08 * k, b: (1 - k) * 10 }); shine(s.b4b, t, 5.75, 1.1);
    up(s.b4c, t, 6.05); s.b4c.style.opacity *= g; }
  { const g = out(t, 8.22, .25); const k = slam(s.b5, t, 7.15, 1.6); set(s.b5, { o: lin(t, 7.14, 7.2) * g, s: (k <= 0 ? 1.6 : 1.6 - .6 * ez.out(k)) * (1 + (1 - g) * .25), b: (1 - g) * 12 }); shine(s.b5, t, 7.4, .9); }
  { const g = out(t, 9.85, .22); up(s.b6a, t, 8.45); s.b6a.style.opacity *= g; up(s.b6b, t, 8.95); s.b6b.style.opacity *= g; }
  { const g = out(t, 11.55, .2); up(s.b7, t, 10.08, .45); s.b7.style.opacity *= g;
    const k = ez.out(lin(t, 10.95, 11.25)); s.ydl.style.transform = `scaleX(${k})`; s.yd.style.opacity = 1 - .55 * k;
    const g8 = out(t, 12.35, .12); const k8 = ez.out(lin(t, 11.62, 12.0)); set(s.b8, { o: k8 * g8, s: .96 + .04 * k8 + .05 * lin(t, 11.6, 12.4), b: (1 - k8) * 8 }); }
  { const k = lin(t, 12.45, 12.68), f = ez.in(lin(t, 13.05, 13.5));
    set(s.b9, { o: lin(t, 12.44, 12.5) * (1 - f), s: (k <= 0 ? 2.4 : 2.4 - 1.4 * ez.out(k)) * (1 + f * 2.6), b: f * 16 }); shine(s.b9, t, 12.6, .9); }
});

/* ===================== 1. WELCOME ===================== */
chapter(CO + .5, 'Welcome');
av(S(.82), 'hero', .6); av(S(3.0), 'hidden', .32);
function namePlate() {
  return el(document.getElementById('over'), 'glass', `<div style="display:flex;align-items:center;gap:20px;height:100%;padding:0 30px">
     <span class="disp gt" style="font-size:60px">MTG</span><span style="font-size:46px">👑</span>
     <i style="width:2px;height:54px;background:rgba(255,217,142,.45)"></i>
     <span style="font:700 32px/1.1 var(--f-b);color:#f7e6bf">Your Digital Architect</span></div>`, 'left:70px;top:1000px;height:104px;border-radius:22px;width:660px;overflow:hidden;visibility:hidden;opacity:0');
}
E.scene('welcome', CO - .3, S(3.4), (r, s) => {
  s.logo = box(r, 540, 840, 1060, 280, '', '<span class="disp gt" style="font-size:250px;line-height:1">MTG</span><span style="font-size:160px;margin-left:14px;filter:drop-shadow(0 0 30px rgba(242,173,60,.5))">👑</span>');
  s.sub = box(r, 540, 1030, 1060, 40, 'mono', 'Your Digital Architect', 'font-size:27px;color:#ffd98e;letter-spacing:.4em');
  s.np = namePlate(); s.overlays = [s.np];
}, (t, r, s) => {
  const k = ez.out(lin(t, CO - .15, CO + .45)), g = ez.inOut(lin(t, S(.7), S(1.15)));
  set(s.logo, { o: k * (1 - g), s: (1.15 - .15 * k) * (1 - .25 * g), y: -g * 140, b: (1 - k) * 14 + g * 8 }); shine(s.logo.firstChild, t, CO + .2, 1.2);
  const k2 = ez.out(lin(t, CO + .25, CO + .7)); set(s.sub, { o: k2 * (1 - g), y: (1 - k2) * 16 - g * 140 });
  const n = ez.out(lin(t, S(2.1), S(2.55))), ng = out(t, S(3.0), .25);
  set(s.np, { o: n * ng, x: (1 - n) * -60 }); s.np.style.clipPath = `inset(0 ${((1 - n) * 100).toFixed(1)}% 0 0 round 22px)`;
  shine(s.np.querySelector('.gt'), t, S(2.4), 1);
});

/* ===================== 2. EVERY STEP: a zig-zag path up to the door ===================== */
av(S(6.5), 'pip', .5); av(S(19.85), 'hidden', .35);
function smoothPath(P) {   // Catmull-Rom through points, as cubic Beziers
  let d = `M ${P[0][0]} ${P[0][1]}`;
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    d += ` C ${p1[0] + (p2[0] - p0[0]) / 6} ${p1[1] + (p2[1] - p0[1]) / 6}, ${p2[0] - (p3[0] - p1[0]) / 6} ${p2[1] - (p3[1] - p1[1]) / 6}, ${p2[0]} ${p2[1]}`;
  }
  return d;
}
E.scene('steps', S(3.2), S(20.25), (r, s) => {
  s.world = el(r, '', '', 'width:1080px;height:1920px;transform-origin:540px 520px');
  const svg = svgLayer(s.world); defs(svg, GOLD_DEFS + `<radialGradient id="dl"><stop offset="0" stop-color="#fff6dc"/><stop offset=".35" stop-color="#ffd98e" stop-opacity=".85"/><stop offset="1" stop-color="#f2ad3c" stop-opacity="0"/></radialGradient>`);
  const NODES = [[230, 1100], [850, 980], [230, 860], [850, 745]];
  s.path = sv(svg, 'path', { d: smoothPath([[120, 1150], ...NODES, [540, 700]]), fill: 'none', stroke: 'rgba(255,217,142,.16)', 'stroke-width': 3, 'stroke-dasharray': '4 12' });
  s.len = s.path.getTotalLength();
  const near = (x, y) => { let best = 0, bd = 1e9; for (let L = 0; L <= s.len; L += 3) { const p = s.path.getPointAtLength(L), d = (p.x - x) ** 2 + (p.y - y) ** 2; if (d < bd) { bd = d; best = L; } } return best; };
  s.glowDoor = sv(svg, 'ellipse', { cx: 540, cy: 520, rx: 10, ry: 10, fill: 'url(#dl)' });
  s.door = el(s.world, '', `<div style="position:absolute;inset:0;border-radius:130px 130px 10px 10px;box-shadow:inset 0 0 0 4px #f2ad3c,0 0 60px rgba(242,173,60,.4);background:radial-gradient(circle at 50% 45%,#fff6dc,#ffd98e 30%,#f2ad3c 60%,#7a4a16)"></div>
    <div class="dl" style="position:absolute;left:8px;top:8px;width:122px;height:384px;border-radius:122px 0 0 4px;transform-origin:0 50%;background:linear-gradient(160deg,#2c2216,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.55)"><i style="position:absolute;right:14px;top:206px;width:10px;height:10px;border-radius:50%;background:#ffd98e;box-shadow:0 0 12px #f2ad3c"></i></div>
    <div class="dr" style="position:absolute;right:8px;top:8px;width:122px;height:384px;border-radius:0 122px 4px 0;transform-origin:100% 50%;background:linear-gradient(200deg,#2c2216,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.55)"><i style="position:absolute;left:14px;top:206px;width:10px;height:10px;border-radius:50%;background:#ffd98e;box-shadow:0 0 12px #f2ad3c"></i></div>`,
    'left:410px;top:300px;width:260px;height:400px;perspective:900px');
  s.dl = s.door.querySelector('.dl'); s.dr = s.door.querySelector('.dr');
  s.rays = el(s.world, '', '', 'left:240px;top:200px;width:600px;height:600px;border-radius:50%;background:repeating-conic-gradient(from 0deg,rgba(255,217,142,.22) 0 6deg,rgba(255,217,142,0) 6deg 18deg);-webkit-mask-image:radial-gradient(circle,#000 10%,transparent 68%);mask-image:radial-gradient(circle,#000 10%,transparent 68%)');
  s.fp = []; const n = Math.floor(s.len / 46);
  for (let i = 1; i < n; i++) {
    const L = i * 46, p = s.path.getPointAtLength(L), q = s.path.getPointAtLength(Math.min(s.len, L + 2));
    const ang = Math.atan2(q.y - p.y, q.x - p.x), side = i % 2 ? 1 : -1, nx = -Math.sin(ang) * 13 * side, ny = Math.cos(ang) * 13 * side;
    const f = el(s.world, '', ic('footprints', '', 'style="width:36px;height:36px"'), `left:${p.x + nx - 18}px;top:${p.y + ny - 18}px;width:36px;height:36px;color:#ffd98e`);
    f.style.transform = `rotate(${ang * 57.3 + 90}deg)`; s.fp.push({ el: f, L });
  }
  const ms = [['circle-play', 'Tutorials', 7.08], ['lightbulb', 'Explainers', 7.94], ['globe', 'Websites', 9.6], ['tiktok', 'TikTok lives', 11.44]];
  s.ms = ms.map(([icn, lb, ts], i) => {
    const [x, y] = NODES[i], left = x < 540;
    const dot = el(s.world, '', '', `left:${x - 12}px;top:${y - 12}px;width:24px;height:24px;border-radius:50%;background:#ffd98e;box-shadow:0 0 0 6px rgba(242,173,60,.25),0 0 26px #f2ad3c`);
    const card = el(s.world, 'glass', `<div style="display:flex;align-items:center;gap:18px;height:100%;padding:0 22px">${ic(icn, '', 'style="width:52px;height:52px;color:#ffd98e;flex:none"')}<b style="font:800 34px/1 var(--f-b);white-space:nowrap">${lb}</b></div>`,
      `left:${left ? x + 54 : x - 54 - 300}px;top:${y - 50}px;width:300px;height:100px;transform-origin:${left ? '0' : '100%'} 50%`);
    const stem = el(s.world, '', '', `left:${left ? x + 12 : x - 54}px;top:${y - 1}px;width:42px;height:2px;background:#f2ad3c`);
    return { dot, card, stem, L: near(x, y), t: S(ts) };
  });
  s.lab0 = box(r, 540, 205, 1040, 100, 'disp st', "You've already started.", 'font-size:88px');
  s.lab = box(r, 540, 205, 1040, 110, 'disp gt', 'Every step counts', 'font-size:110px');
  s.inv = el(r, 'glass', `<div style="position:absolute;inset:18px;border-radius:18px;box-shadow:inset 0 0 0 1px rgba(255,217,142,.35)"></div>
    <div class="cx" style="flex-direction:column;height:100%;gap:22px">
      <span class="mono" style="font-size:26px;color:#ffd98e;letter-spacing:.5em">You're invited</span>
      <span class="disp gt inv-t" style="font-size:160px">MTG TRIBE</span>
      <span style="font:600 34px/1 var(--f-b);color:#d9d2c6">A community of action takers</span></div>
    <div class="cx" style="position:absolute;right:-30px;bottom:-34px;width:130px;height:130px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd98e,#c17a1e 60%,#7a4a16);box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 4px rgba(255,236,200,.35);font-size:60px">👑</div>`,
    'left:90px;top:560px;width:900px;height:480px');
  s.invT = s.inv.querySelector('.inv-t');
  flash(S(20.05), .45, .55);
}, (t, r, s) => {
  const vin = ez.out(lin(t, S(3.2), S(3.385) + .35)), vout = out(t, S(19.95), .3);
  const kts = [[S(6.2), 0], [S(7.08), s.ms[0].L], [S(7.94), s.ms[1].L], [S(9.6), s.ms[2].L], [S(11.44), s.ms[3].L], [S(12.5), s.len]];
  let walk = 0; for (let i = 0; i < kts.length - 1; i++) { const [a, la] = kts[i], [b, lb] = kts[i + 1]; if (t >= a) walk = mix(la, lb, ez.sine(lin(t, a, b))); }
  const wave = mix(-200, s.len + 200, lin(t, S(13.4), S(15.2)));
  s.path.style.opacity = vin;
  s.fp.forEach(f => {
    const k = clamp((walk - f.L + 30) / 30), hot = Math.exp(-Math.pow((f.L - wave) / 120, 2));
    f.el.style.opacity = (k * (.55 + .45 * hot) * vin).toFixed(3);
    f.el.style.filter = hot > .05 ? `drop-shadow(0 0 ${(14 * hot).toFixed(1)}px #f2ad3c)` : '';
    f.el.style.color = hot > .3 ? '#fff6dc' : '#ffd98e';
  });
  s.ms.forEach(m => { pp(m.card, t, m.t); m.card.style.opacity *= vin; set(m.dot, { o: lin(t, m.t - .2, m.t) * vin, s: .6 + .4 * ez.back(lin(t, m.t - .2, m.t + .2)) }); m.stem.style.opacity = (lin(t, m.t, m.t + .2) * vin).toFixed(3); });
  { const k = ez.out(lin(t, S(6.6), S(7.1))), g = out(t, S(13.05), .3); set(s.lab0, { o: k * g, y: (1 - k) * 20 }); shine(s.lab0, t, S(7.0), 1.2); }
  { const k = ez.out(lin(t, S(13.4), S(13.9))), g = out(t, S(15.9), .3); set(s.lab, { o: k * g, y: (1 - k) * 20, s: .94 + .06 * k }); shine(s.lab, t, S(13.7), 1.3); }
  const push = ez.inOut(lin(t, S(15.9), S(17.6)));
  s.world.style.transform = `scale(${(1 + .5 * push).toFixed(4)})`; s.world.style.opacity = (vin * vout * (1 - .7 * ez.out(lin(t, S(17.9), S(18.5))))).toFixed(3);
  const op = ez.inOut(lin(t, S(16.9), S(17.9)));
  s.dl.style.transform = `rotateY(${(-82 * op).toFixed(2)}deg)`; s.dr.style.transform = `rotateY(${(82 * op).toFixed(2)}deg)`;
  s.glowDoor.setAttribute('rx', 120 + 420 * op); s.glowDoor.setAttribute('ry', 190 + 520 * op); s.glowDoor.setAttribute('opacity', ((.25 + op * 1.2) * .6).toFixed(3));
  set(s.rays, { o: op * .9, s: .6 + .9 * op, r: t * 8 });
  set(s.door, { o: lin(t, S(3.4), S(4.2)) });
  const fly = ez.out(lin(t, S(17.85), S(18.65)));
  set(s.inv, { o: lin(t, S(17.85), S(18.0)) * vout, y: (1 - fly) * -260, s: .15 + .85 * fly, rx: (1 - fly) * 40, p: 1400 });
  shine(s.invT, t, S(18.9), 1.0);
});

/* ===================== 3. WHAT IT IS (MTG on top) ===================== */
chapter(S(21.6), 'What it is');
av(S(21.6), 'split', .6); av(S(35.55), 'hidden', .4);
E.scene('what', S(21.565), S(36.0), (r, s) => {
  s.q1 = box(r, 540, 818, 1000, 30, 'mono', 'So what is the', 'font-size:22px;color:#ffd98e;letter-spacing:.4em');
  s.q2 = box(r, 540, 892, 1000, 110, 'disp gt', 'MTG TRIBE?', 'font-size:118px');
  s.row = el(r, '', '', `left:40px;top:960px;width:1000px;height:70px;display:flex;justify-content:center;gap:14px;align-items:center`);
  s.chips = [['book-open', 'Learn', 25.78], ['zap', 'Take action', 26.44], ['sprout', 'Grow', 27.4]].map(([icn, lb, ts], i) => {
    const c = document.createElement('div'); c.className = 'chip'; c.style.fontSize = '28px'; c.style.padding = '14px 22px'; c.innerHTML = ic(icn) + lb; s.row.appendChild(c);
    if (i < 2) { const a = document.createElement('div'); a.innerHTML = ic('send', '', 'style="width:24px;height:24px;color:#f2ad3c"'); a.style.display = 'flex'; a.className = 'arw'; s.row.appendChild(a); }
    return { c, t: S(ts) };
  });
  s.arws = Array.from(s.row.querySelectorAll('.arw'));
  s.chat = el(r, '', `<div style="height:80px;display:flex;align-items:center;gap:16px;padding:0 24px;background:linear-gradient(90deg,#0f5e3a,#128c4e);border-radius:26px 26px 0 0">
      <span class="cx" style="width:54px;height:54px;border-radius:50%;background:#1b140c;box-shadow:inset 0 0 0 2px #f2ad3c;font-size:28px">👑</span>
      <span style="display:flex;flex-direction:column;gap:6px"><b style="font:800 30px/1 var(--f-b);color:#fff">MTG TRIBE</b><small style="font:600 19px/1 var(--f-b);color:#c9f5d9">WhatsApp community</small></span>
      <span style="margin-left:auto;color:#fff">${ic('whatsapp', '', 'style="width:40px;height:40px"')}</span></div>
    <div class="msgs" style="position:absolute;left:0;right:0;top:80px;bottom:0;padding:18px 24px;display:flex;flex-direction:column;gap:12px;background:linear-gradient(180deg,#14100b,#0c0a07);border-radius:0 0 26px 26px"></div>`,
    'left:90px;top:1046px;width:900px;height:334px;border-radius:26px;box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.35),0 30px 70px rgba(0,0,0,.6)');
  const msgs = s.chat.querySelector('.msgs');
  s.msgs = [['circle-play', 'New tutorial: step by step', 30.06], ['lightbulb', 'New explainer', 30.94], ['zap', 'Tip of the day', 31.82], ['target', 'Strategy session', 32.2]].map(([icn, lb, ts]) => {
    const m = document.createElement('div');
    m.style.cssText = 'align-self:flex-start;display:flex;align-items:center;gap:12px;padding:9px 18px;border-radius:4px 18px 18px 18px;background:#2a2116;box-shadow:inset 0 0 0 1px rgba(255,217,142,.25);font:700 25px/1 var(--f-b);transform-origin:0 50%';
    m.innerHTML = ic(icn, '', 'style="width:28px;height:28px;color:#ffd98e"') + lb; msgs.appendChild(m); return { m, t: S(ts) };
  });
  s.fan = ['coins', 'rocket', 'globe', 'chart-line', 'briefcase'].map(icn => el(r, 'glass', `<div class="cx" style="height:100%">${ic(icn, '', 'style="width:76px;height:76px;color:#ffd98e"')}</div>`, `left:450px;top:1070px;width:180px;height:240px;transform-origin:50% 140%`));
  s.stamp = box(r, 540, 890, 1000, 130, 'disp gt', 'Not just one.', 'font-size:120px');
  shake(S(34.94), 7);
}, (t, r, s) => {
  const g = out(t, S(35.65), .32);
  up(s.q1, t, S(21.62)); s.q1.style.opacity *= g;
  const qo = out(t, S(34.6), .3); s.q1.style.opacity *= qo;
  const k = ez.out(lin(t, S(22.2), S(22.6))); set(s.q2, { o: k * g * qo, s: 1.15 - .15 * k, b: (1 - k) * 8 }); shine(s.q2, t, S(22.6), 1.1);
  const cout = ez.inOut(lin(t, S(32.75), S(33.25)));
  s.chips.forEach((c, i) => { const p = pop(t, c.t); set(c.c, { o: p.o * g * (1 - cout), s: p.s }); const tog = Math.exp(-Math.pow((t - S(27.9) - i * .1) / .18, 2)); c.c.style.boxShadow = `inset 0 0 0 1.5px rgba(255,217,142,${(.4 + .6 * tog).toFixed(2)}),0 0 ${(40 * tog).toFixed(0)}px rgba(242,173,60,${(.8 * tog).toFixed(2)}),0 18px 40px rgba(0,0,0,.5)`; });
  s.arws.forEach((a, i) => { a.style.opacity = (lin(t, s.chips[i + 1].t - .1, s.chips[i + 1].t + .15) * g * (1 - cout)).toFixed(3); });
  const cin = ez.out(lin(t, S(23.8), S(24.35)));
  set(s.chat, { o: cin * (1 - cout) * g, y: (1 - cin) * 60 + cout * 80, s: .96 + .04 * cin, b: cout * 8 });
  s.msgs.forEach(m => { const p = pop(t, m.t, .45); set(m.m, { o: p.o, s: p.s }); });
  const fo = ez.out(lin(t, S(33.0), S(34.2)));
  s.fan.forEach((f, i) => { set(f, { o: lin(t, S(32.95), S(33.2)) * g, r: (i - 2) * 15 * fo, y: (1 - fo) * 40, s: .9 + .1 * fo }); f.style.boxShadow = `inset 0 0 0 1.5px rgba(255,217,142,.4),0 0 ${(30 * fo).toFixed(0)}px rgba(242,173,60,.25),0 20px 50px rgba(0,0,0,.6)`; });
  slam(s.stamp, t, S(34.94), 1.7, { r: -4 }); s.stamp.style.opacity *= g; shine(s.stamp, t, S(35.1), .8);
});

/* ===================== 4. UPFRONT ===================== */
chapter(S(36.5), 'Let me be upfront');
av(S(36.6), 'pip', .5);
E.scene('upfront', S(36.37), S(49.75), (r, s) => {
  s.head = el(r, '', `<div style="display:flex;flex-direction:column;align-items:center;gap:26px"><span class="ibox" style="width:140px;height:140px;display:grid">${ic('shield-check', '', 'style="width:72px;height:72px"')}</span><span class="disp st up-t" style="font-size:116px">Let me be upfront</span></div>`,
    'left:0;top:500px;width:1080px;height:300px;display:flex;justify-content:center;align-items:center;transform-origin:540px 150px');
  s.headT = s.head.querySelector('.up-t');
  s.one = box(r, 540, 660, 880, 220, 'glass', `<div style="display:flex;align-items:center;gap:26px">${ic('ticket', '', 'style="width:84px;height:84px;color:#ffd98e"')}<span class="disp" style="font-size:100px;color:#efe9df">One program</span></div>`);
  s.x = box(r, 540, 660, 300, 300, '', `<svg width="300" height="300" viewBox="0 0 300 300"><path d="M40 40 L260 260 M260 40 L40 260" stroke="#ff7a4d" stroke-width="22" stroke-linecap="round" style="filter:drop-shadow(0 0 18px rgba(255,90,40,.8))"/></svg>`);
  s.shards = []; { const rnd = E.rng(3); for (let i = 0; i < 16; i++) s.shards.push({ e: el(r, '', '', `left:${520 + rnd() * 40}px;top:${640 + rnd() * 40}px;width:${10 + rnd() * 26}px;height:${8 + rnd() * 18}px;background:linear-gradient(135deg,#ffd98e,#a8681a);border-radius:3px`), vx: (rnd() - .5) * 1100, vy: (rnd() - .7) * 1100, vr: (rnd() - .5) * 900 }); }
  const pos = [[300, 520], [780, 520], [300, 790], [780, 790]];
  s.tiles = [['rocket', 'Projects', 40.52], ['wrench', 'Tools', 41.32], ['target', 'Strategies', 41.86], ['coins', 'Coins & tokens', 43.72]].map(([icn, lb, ts], i) => {
    const [cx, cy] = pos[i];
    const e = el(r, 'glass', `<div class="cx" style="flex-direction:column;gap:18px;height:100%"><span class="ibox" style="width:100px;height:100px;display:grid">${ic(icn, '', 'style="width:52px;height:52px"')}</span><span class="disp" style="font-size:56px;color:#f5efe6">${lb}</span></div>`, `left:${cx - 215}px;top:${cy - 120}px;width:430px;height:240px`);
    return { e, cx, cy, t: S(ts) };
  });
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  s.streams = [200, 420, 660, 880].map(x => sv(svg, 'path', { d: `M ${x} 918 C ${x} 990, 540 960, 540 1040`, fill: 'none', stroke: 'url(#gg)', 'stroke-width': 7, 'stroke-linecap': 'round', filter: 'url(#glow)' }));
  s.flow = [200, 420, 660, 880].map(x => sv(svg, 'path', { d: `M ${x} 918 C ${x} 990, 540 960, 540 1040`, fill: 'none', stroke: '#fff6dc', 'stroke-width': 3, 'stroke-dasharray': '6 26', 'stroke-linecap': 'round' }));
  s.pool = sv(svg, 'ellipse', { cx: 540, cy: 1048, rx: 200, ry: 30, fill: 'rgba(242,173,60,.35)', filter: 'url(#glow2)' });
  s.lab1 = box(r, 540, 1128, 1040, 74, 'disp gt', 'Multiple streams of income', 'font-size:68px');
  s.lab2 = box(r, 540, 1128, 1040, 80, '', `<span style="display:flex;align-items:center;gap:20px">${ic('infinity', '', 'style="width:84px;height:84px;color:#ffd98e"')}<span class="disp gt" style="font-size:72px">Never stop learning</span></span>`);
  shake(S(38.76), 8);
}, (t, r, s) => {
  const g = out(t, S(49.55), .35);
  const hk = ez.out(lin(t, S(36.45), S(36.9))), hm = ez.inOut(lin(t, S(37.55), S(38.05)));
  set(s.head, { o: hk * g, s: (1.1 - .1 * hk) * (1 - .5 * hm), y: -hm * 400, b: (1 - hk) * 10 }); shine(s.headT, t, S(36.8), 1.1);
  pp(s.one, t, S(38.05)); const shat = lin(t, S(39.22), S(39.4));
  s.one.style.opacity = (lin(t, S(38.05), S(38.2)) * (1 - shat)).toFixed(3);
  slam(s.x, t, S(38.72), 1.8); s.x.style.opacity = (lin(t, S(38.7), S(38.78)) * (1 - shat)).toFixed(3);
  s.shards.forEach(h => { const d = t - S(39.22); if (d < 0 || d > 1.2) { h.e.style.opacity = 0; return; } set(h.e, { o: 1 - d / 1.2, x: h.vx * d, y: h.vy * d + 900 * d * d, r: h.vr * d }); });
  s.tiles.forEach(ti => { const k = ez.back(lin(t, ti.t - .1, ti.t + .45)), o = lin(t, ti.t - .1, ti.t + .05); set(ti.e, { o: o * g, x: (1 - k) * (540 - ti.cx), y: (1 - k) * (660 - ti.cy), s: .5 + .5 * clamp(k, 0, 1.2) }); });
  const sd = ez.inOut(lin(t, S(46.3), S(47.3)));
  s.streams.forEach(p => { const L = p.getTotalLength() + 2; p.setAttribute('stroke-dasharray', L); p.setAttribute('stroke-dashoffset', (L * (1 - sd)).toFixed(1)); p.setAttribute('opacity', g.toFixed(3)); });
  s.flow.forEach(p => { p.setAttribute('stroke-dashoffset', (-t * 120).toFixed(1)); p.setAttribute('opacity', (lin(t, S(46.9), S(47.3)) * g).toFixed(3)); });
  s.pool.setAttribute('opacity', (ez.out(lin(t, S(46.9), S(47.6))) * g).toFixed(3)); s.pool.setAttribute('rx', 140 + 90 * lin(t, S(46.9), S(48.5)));
  const l1 = ez.out(lin(t, S(46.6), S(47.0))), l1o = out(t, S(48.1), .25); set(s.lab1, { o: l1 * l1o * g, y: (1 - l1) * 18 }); shine(s.lab1, t, S(47.0), 1);
  const l2 = ez.out(lin(t, S(48.25), S(48.65))); set(s.lab2, { o: l2 * g, y: (1 - l2) * 18 });
  const inf = s.lab2.querySelector('svg'); inf.style.strokeDasharray = 60; inf.style.strokeDashoffset = (60 * (1 - ez.inOut(lin(t, S(48.25), S(49.1))))).toFixed(1);
  shine(s.lab2.querySelector('.gt'), t, S(48.6), 1);
});

/* ===================== 5. THE FARMER ===================== */
chapter(S(50.0), 'Spread the risk');
E.scene('farm', S(49.75), S(63.0), (r, s) => {
  s.wrap = el(r, '', '<canvas width="1080" height="1920"></canvas>', 'width:1080px;height:1920px;transform-origin:540px 760px');
  s.cv = s.wrap.firstChild;
  s.lab = box(r, 540, 300, 1040, 200, 'disp gt', '<span>One bad season.<br>Still a full table.</span>', 'font-size:92px;line-height:1');
  s.pause = box(r, 540, 720, 230, 230, '', `<svg width="230" height="230" viewBox="0 0 220 220"><circle cx="110" cy="110" r="100" fill="rgba(0,0,0,.45)" stroke="#ffd98e" stroke-width="5"/><rect x="78" y="62" width="22" height="96" rx="6" fill="#ffd98e"/><rect x="120" y="62" width="22" height="96" rx="6" fill="#ffd98e"/></svg>`);
  s.stop = box(r, 540, 910, 820, 84, 'glass', '<span class="mono" style="font-size:28px;color:#ffd98e">Where the analogy stops</span>', 'border-radius:18px');
  s.frame = el(r, '', '', 'left:50px;top:190px;width:980px;height:960px;border-radius:24px;box-shadow:inset 0 0 0 3px rgba(255,217,142,.75);outline:2px dashed rgba(255,217,142,.35);outline-offset:14px');
  s.gauge = el(r, '', `<svg width="900" height="520" viewBox="0 0 760 440" style="overflow:visible">
    <defs><linearGradient id="gz" x1="0" x2="1"><stop offset="0" stop-color="#c9d66b"/><stop offset=".5" stop-color="#f2ad3c"/><stop offset="1" stop-color="#e2553a"/></linearGradient></defs>
    <path d="M 60 380 A 320 320 0 0 1 700 380" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="46" stroke-linecap="round"/>
    <path d="M 60 380 A 320 320 0 0 1 700 380" fill="none" stroke="url(#gz)" stroke-width="40" stroke-linecap="round" style="filter:drop-shadow(0 0 16px rgba(242,173,60,.4))"/>
    <text x="60" y="438" fill="#c9d66b" font-family="JetBrains Mono" font-weight="700" font-size="22" text-anchor="middle" letter-spacing="4">LOW</text>
    <text x="700" y="438" fill="#ff8a6b" font-family="JetBrains Mono" font-weight="700" font-size="22" text-anchor="middle" letter-spacing="4">HIGH</text>
    <text x="380" y="300" fill="#ffd98e" font-family="JetBrains Mono" font-weight="700" font-size="24" text-anchor="middle" letter-spacing="8">RISK</text>
    <g class="needle"><path d="M 380 380 L 372 380 L 380 100 L 388 380 Z" fill="#fff6dc" style="filter:drop-shadow(0 0 10px rgba(255,217,142,.9))"/></g>
    <circle cx="380" cy="380" r="24" fill="#1b140c" stroke="#ffd98e" stroke-width="5"/></svg>`, 'left:90px;top:360px;width:900px;height:520px');
  s.needle = s.gauge.querySelector('.needle');
  s.zero = box(r, 250, 960, 290, 70, 'chip', ic('lock') + 'Never zero', 'font-size:28px;justify-content:center');
  s.risk = box(r, 540, 1080, 1040, 100, 'disp gt', 'Lower risk, not no risk.', 'font-size:84px');
  s.table = el(r, '', '', 'left:240px;top:580px;width:600px;height:240px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,rgba(255,217,142,.2),rgba(30,24,15,.95) 70%);box-shadow:inset 0 0 0 3px rgba(255,217,142,.6),0 0 60px rgba(242,173,60,.25),0 30px 60px rgba(0,0,0,.6)');
  const seatIcons = ['coins', 'globe', 'rocket', 'chart-line', 'wallet', 'store', 'megaphone', null];
  s.seats = seatIcons.map((icn, i) => {
    const a = Math.PI / 2 + i * (Math.PI * 2 / 8) + Math.PI / 4, cx = 540 + Math.cos(a) * 400, cy = 700 + Math.sin(a) * 240;
    const empty = !icn;
    const e = box(r, cx, cy, 110, 110, '', empty ? `<div class="cx" style="width:110px;height:110px;border-radius:50%;border:3px dashed #ffd98e;color:#ffd98e">${ic('armchair', '', 'style="width:54px;height:54px"')}</div>`
      : `<div class="cx" style="width:100px;height:100px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#3a2e1f,#16110b);box-shadow:inset 0 0 0 2px rgba(255,217,142,.45);color:#ffd98e">${ic(icn, '', 'style="width:46px;height:46px"')}</div>`);
    return { e, empty, i, cx, cy };
  });
  const es = s.seats[7];
  s.yours = box(r, es.cx, es.cy + 100, 260, 60, 'chip', ic('crown') + 'Your seat', 'font-size:26px;justify-content:center');
  s.seatLab = box(r, 540, 330, 1040, 200, 'disp gt', "<span>There's a seat<br>for you.</span>", 'font-size:96px;line-height:1');
  flash(S(53.32), .3, .35, '255,255,255'); shake(S(59.76), 6);
}, (t, r, s) => {
  const vin = ez.out(lin(t, S(49.75), S(50.4))), g = out(t, S(62.55), .4);
  const freeze = ez.out(lin(t, S(55.5), S(55.9))), sink = ez.inOut(lin(t, S(57.9), S(58.5)));
  drawFarmV(s.cv.getContext('2d'), t);
  s.wrap.style.opacity = (vin * g * (1 - .62 * sink)).toFixed(3);
  s.wrap.style.filter = `grayscale(${(freeze * .9).toFixed(2)}) brightness(${(1 - .35 * freeze).toFixed(2)})` + (sink > .01 ? ` blur(${(sink * 10).toFixed(1)}px)` : '');
  s.wrap.style.transform = `scale(${(1.02 + .03 * lin(t, S(49.8), S(55.5)) - .06 * sink).toFixed(4)})`;
  { const k = ez.out(lin(t, S(54.3), S(54.8))), o = out(t, S(55.45), .2); set(s.lab, { o: k * o, y: (1 - k) * 20 }); shine(s.lab, t, S(54.7), 1); }
  { const k = pop(t, S(55.55)), o = out(t, S(57.85), .3); set(s.pause, { o: k.o * o, s: k.s }); const k2 = ez.out(lin(t, S(56.3), S(56.7))); set(s.stop, { o: k2 * o, y: (1 - k2) * 20 }); set(s.frame, { o: freeze * o * .9, s: 1.03 - .03 * freeze }); }
  const gin = ez.out(lin(t, S(58.0), S(58.45))), gout = out(t, S(60.35), .35);
  set(s.gauge, { o: gin * gout, s: .9 + .1 * gin, y: (1 - gin) * 30 });
  const sw = ez.back(lin(t, S(58.4), S(59.2))), wob = Math.sin((t - S(59.6)) * 14) * Math.exp(-Math.max(0, t - S(59.6)) * 3) * (t > S(59.6) ? 4 : 0);
  s.needle.setAttribute('transform', `rotate(${(mix(62, -48, sw) + wob).toFixed(2)} 380 380)`);
  { const k = pop(t, S(59.52)); set(s.zero, { o: k.o * gout, s: k.s }); }
  { slam(s.risk, t, S(59.76), 1.5); s.risk.style.opacity *= gout; shine(s.risk, t, S(59.9), .9); }
  const tin = ez.out(lin(t, S(60.4), S(60.9)));
  set(s.table, { o: tin * g, s: .85 + .15 * tin });
  s.seats.forEach(st => {
    const t0 = st.empty ? S(61.9) : S(60.76) + st.i * .1, p = pop(t, t0);
    set(st.e, { o: p.o * g, s: p.s * (st.empty ? 1 + .06 * Math.sin((t - t0) * 6) * lin(t, t0, t0 + .5) : 1) });
    if (st.empty) st.e.firstChild.style.boxShadow = `0 0 ${(20 + 30 * (.5 + .5 * Math.sin(t * 6))).toFixed(0)}px rgba(242,173,60,${(.8 * lin(t, t0, t0 + .4)).toFixed(2)})`;
  });
  { const k = pop(t, S(62.05)); set(s.yours, { o: k.o * g, s: k.s }); }
  { const k = ez.out(lin(t, S(61.85), S(62.3))); set(s.seatLab, { o: k * g, y: (1 - k) * 20 }); shine(s.seatLab, t, S(62.2), 1); }
});
function drawFarmV(c, t) {
  const W = 1080, H = 1920; c.clearRect(0, 0, W, H);
  const sky = c.createLinearGradient(0, 160, 0, 760); sky.addColorStop(0, '#120c06'); sky.addColorStop(.6, '#4a2c10'); sky.addColorStop(1, '#8a5418');
  c.fillStyle = sky; c.fillRect(0, 0, W, 780);
  const sun = c.createRadialGradient(760, 600, 10, 760, 600, 380); sun.addColorStop(0, 'rgba(255,236,190,.95)'); sun.addColorStop(.12, 'rgba(255,210,120,.7)'); sun.addColorStop(1, 'rgba(242,173,60,0)');
  c.fillStyle = sun; c.fillRect(0, 160, W, 760);
  const hill = (y0, amp, f, ph, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(0, H); for (let x = 0; x <= W; x += 20) c.lineTo(x, y0 + Math.sin(x * f + ph) * amp + Math.sin(x * f * 2.3 + ph) * amp * .4); c.lineTo(W, H); c.fill(); };
  hill(650, 22, .006, 1, '#3a240f'); hill(700, 16, .009, 3, '#24170b');
  c.fillStyle = '#140d06'; c.beginPath(); c.moveTo(810, 660); c.lineTo(890, 606); c.lineTo(970, 660); c.lineTo(970, 730); c.lineTo(810, 730); c.fill();
  const wl = c.createRadialGradient(890, 682, 2, 890, 682, 55); wl.addColorStop(0, 'rgba(255,217,142,1)'); wl.addColorStop(1, 'rgba(255,217,142,0)');
  c.fillStyle = wl; c.fillRect(835, 640, 110, 85); c.fillStyle = '#ffd98e'; c.fillRect(877, 670, 26, 22);
  const fy = 740; const field = c.createLinearGradient(0, fy, 0, 1200); field.addColorStop(0, '#2a1a0b'); field.addColorStop(1, '#120b05'); c.fillStyle = field; c.fillRect(0, fy, W, 1200 - fy);
  const fade = c.createLinearGradient(0, 1100, 0, 1260); fade.addColorStop(0, 'rgba(5,4,3,0)'); fade.addColorStop(1, 'rgba(5,4,3,1)'); c.fillStyle = fade; c.fillRect(0, 1100, W, 160);
  const plots = [{ x: 150, type: 'maize' }, { x: 400, type: 'wheat' }, { x: 650, type: 'sun' }, { x: 900, type: 'leaf' }];
  const storm = lin(t, S(52.45), S(52.95)), wilt = ez.inOut(lin(t, S(53.35), S(54.1))), stormOut = lin(t, S(54.6), S(55.3));
  const glow = ez.out(lin(t, S(54.1), S(54.6)));
  plots.forEach((p, i) => {
    c.fillStyle = 'rgba(255,217,142,.05)'; c.fillRect(p.x - 112, fy + 24, 224, 340);
    for (let row = 0; row < 3; row++) for (let col = 0; col < 3; col++) {
      const px = p.x - 66 + col * 66 + (row % 2) * 12, py = fy + 120 + row * 105, sc = 1.0 + row * .2;
      const gT = S(50.85) + i * .28 + row * .06, grow = ez.out(lin(t, gT, gT + .7));
      if (grow <= 0) continue;
      drawPlantV(c, p.type, px, py, sc * grow, i === 1 ? wilt : 0, glow * (i !== 1 ? 1 : 0), t + i + row, t);
    }
  });
  if (storm > 0 && stormOut < 1) {
    const cx = mix(-120, 400, ez.out(storm)) + stormOut * -560, cy = 640;
    c.globalAlpha = 1 - stormOut;
    if (t > S(52.6)) { c.strokeStyle = 'rgba(180,200,230,.55)'; c.lineWidth = 2; c.beginPath(); const rnd = E.rng(Math.floor(t * 30)); for (let i = 0; i < 40; i++) { const x = cx - 120 + rnd() * 240, y = cy + 40 + rnd() * 420; c.moveTo(x, y); c.lineTo(x - 8, y + 30); } c.stroke(); }
    c.fillStyle = '#2b2e36'; [[-95, 10, 60], [-35, -18, 78], [45, -4, 70], [105, 14, 52], [0, 28, 78]].forEach(([dx, dy, rr]) => { c.beginPath(); c.arc(cx + dx, cy + dy, rr, 0, 6.283); c.fill(); });
    if (Math.abs(t - S(53.32)) < .12) { c.strokeStyle = '#fff6dc'; c.lineWidth = 5; c.shadowColor = '#fff'; c.shadowBlur = 30; c.beginPath(); c.moveTo(cx + 10, cy + 60); c.lineTo(cx - 20, cy + 160); c.lineTo(cx + 15, cy + 170); c.lineTo(cx - 25, cy + 300); c.stroke(); c.shadowBlur = 0; }
    c.globalAlpha = 1;
  }
  const fam = ez.out(lin(t, S(54.8), S(55.3)));
  if (fam > 0) {
    c.globalAlpha = fam; c.fillStyle = '#ffd98e'; c.shadowColor = 'rgba(242,173,60,.9)'; c.shadowBlur = 20;
    [[840, 1.2], [886, 1.35], [930, .9]].forEach(([x, k]) => { c.beginPath(); c.arc(x, 726 - 46 * k, 10 * k, 0, 6.283); c.fill(); c.beginPath(); c.roundRect(x - 11 * k, 738 - 46 * k, 22 * k, 40 * k, 8 * k); c.fill(); });
    c.shadowBlur = 0; c.globalAlpha = 1;
  }
}
function drawPlantV(c, type, x, y, s, bad, glow, ph, t) {
  const sway = Math.sin(ph * 1.7 + t * 1.6) * 2;
  c.save(); c.translate(x, y); c.scale(s, s); c.rotate(bad * .5 + sway * .01);
  const green = bad > 0 ? `rgb(${Math.round(mix(96, 110, bad))},${Math.round(mix(150, 80, bad))},${Math.round(mix(70, 40, bad))})` : '#6aa04a';
  if (glow > 0) { c.shadowColor = `rgba(255,217,142,${glow})`; c.shadowBlur = 18 * glow; }
  c.strokeStyle = green; c.lineWidth = 5; c.lineCap = 'round';
  if (type === 'maize') { c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -90); c.stroke(); c.beginPath(); c.moveTo(0, -40); c.quadraticCurveTo(-30, -60, -40, -40); c.moveTo(0, -60); c.quadraticCurveTo(30, -80, 40, -60); c.stroke(); c.fillStyle = '#f2c14e'; c.beginPath(); c.ellipse(8, -70, 7, 18, .3, 0, 6.283); c.fill(); }
  if (type === 'wheat') { c.strokeStyle = bad > 0 ? '#7a5a30' : '#d9a441'; c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -80); c.stroke(); c.fillStyle = bad > 0 ? '#6a4a25' : '#f2c14e'; for (let k = 0; k < 5; k++) { c.beginPath(); c.ellipse(-6, -78 + k * 9, 5, 8, -.5, 0, 6.283); c.ellipse(6, -78 + k * 9, 5, 8, .5, 0, 6.283); c.fill(); } }
  if (type === 'sun') { c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -85); c.stroke(); c.fillStyle = '#f2ad3c'; for (let k = 0; k < 10; k++) { c.beginPath(); c.ellipse(Math.cos(k * .628) * 16, -92 + Math.sin(k * .628) * 16, 9, 5, k * .628, 0, 6.283); c.fill(); } c.fillStyle = '#4a2a10'; c.beginPath(); c.arc(0, -92, 11, 0, 6.283); c.fill(); }
  if (type === 'leaf') { c.fillStyle = green; for (let k = 0; k < 5; k++) { c.beginPath(); c.ellipse(Math.cos(k * 1.256) * 14, -22 + Math.sin(k * 1.256) * 8, 20, 12, k * 1.256, 0, 6.283); c.fill(); } c.fillStyle = '#8cc46a'; c.beginPath(); c.arc(0, -24, 14, 0, 6.283); c.fill(); }
  c.restore();
}

/* ===================== 6. SERVICES ===================== */
chapter(S(63.0), 'Services');
av(S(62.8), 'split', .6); av(S(71.55), 'pip', .55);
E.scene('services', S(62.75), S(76.45), (r, s) => {
  s.bp = el(r, '', '', `left:40px;top:784px;width:1000px;height:600px;border-radius:26px;background:repeating-linear-gradient(0deg,rgba(255,217,142,.07) 0 1px,transparent 1px 32px),repeating-linear-gradient(90deg,rgba(255,217,142,.07) 0 1px,transparent 1px 32px),linear-gradient(160deg,rgba(30,24,15,.7),rgba(10,8,6,.85));box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.3)`);
  s.title = el(r, '', `<div style="display:flex;align-items:center;gap:18px">${ic('pencil-ruler', '', 'style="width:56px;height:56px;color:#ffd98e"')}<span class="disp gt sv-t" style="font-size:78px">MTG Services</span></div><div style="margin-top:10px;font:600 24px/1 var(--f-b);color:#bdb5a8">Built by your Digital Architect</div>`, 'left:84px;top:806px;width:900px;height:120px');
  s.svT = s.title.querySelector('.sv-t');
  const mkWin = (img, url) => el(r, '', `<div style="height:44px;display:flex;align-items:center;gap:8px;padding:0 16px;background:#1b150e;border-radius:16px 16px 0 0;box-shadow:inset 0 -1px 0 rgba(255,217,142,.2)">
      <i style="width:11px;height:11px;border-radius:50%;background:#ff6b5b"></i><i style="width:11px;height:11px;border-radius:50%;background:#f7c14b"></i><i style="width:11px;height:11px;border-radius:50%;background:#43c46a"></i>
      <span style="margin-left:14px;padding:6px 14px;border-radius:999px;background:#0b0907;font:700 15px/1 var(--f-m);color:#ffd98e;letter-spacing:.04em">${url}</span></div>
    <div class="shot" style="position:absolute;left:0;right:0;top:44px;bottom:0;background:url(${img}) center top/cover;border-radius:0 0 16px 16px"></div>
    <svg class="wire" width="560" height="306" viewBox="0 0 560 306" style="position:absolute;left:0;top:44px" fill="none" stroke="#ffd98e" stroke-width="2.5">
      <rect x="24" y="18" width="120" height="16" rx="4"/><rect x="420" y="16" width="112" height="22" rx="11"/>
      <rect x="120" y="70" width="320" height="26" rx="6"/><rect x="90" y="106" width="380" height="26" rx="6"/><rect x="160" y="150" width="240" height="12" rx="6"/>
      <rect x="140" y="180" width="110" height="30" rx="15"/><rect x="262" y="180" width="160" height="30" rx="15"/><rect x="60" y="232" width="440" height="66" rx="12"/></svg>
    <div class="lnk" style="position:absolute;right:-18px;top:-22px;opacity:0"><span class="chip" style="font-size:20px;padding:10px 16px;background:linear-gradient(180deg,#ffd98e,#f2ad3c);color:#1b140c;box-shadow:0 10px 30px rgba(0,0,0,.5)">${ic('link', '', 'style="width:22px;height:22px;color:#1b140c"')}Your link ✓</span></div>`,
    'left:260px;top:944px;width:560px;height:350px;border-radius:16px;background:#0e0b08;box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.4),0 30px 70px rgba(0,0,0,.65)');
  s.copies = [mkWin('site-tribe.jpg', 'yoursite.com'), mkWin('site-dash.jpg', 'yoursite.com')];
  s.main = mkWin('site-altruva.jpg', 'mtgtribe.com/altruva');
  [s.main, ...s.copies].forEach(w => { w.querySelectorAll('.wire rect').forEach(rc => { const L = 2 * (+rc.getAttribute('width') + +rc.getAttribute('height')); rc.setAttribute('stroke-dasharray', L); rc.dataset.l = L; }); });
  s.links = box(r, 540, 1342, 1000, 70, 'disp gt', 'Your links. Built in.', 'font-size:66px');
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  s.src = [['tiktok', 210, 330], ['whatsapp', 870, 330], ['facebook', 210, 960], ['youtube', 870, 960]].map(([icn, x, y]) => {
    const d = `M ${x} ${y} C ${x} ${mix(y, 640, .5)}, ${mix(x, 540, .5)} 640, 540 640`;
    const road = sv(svg, 'path', { d, fill: 'none', stroke: 'rgba(255,217,142,.18)', 'stroke-width': 26, 'stroke-linecap': 'round' });
    const lane = sv(svg, 'path', { d, fill: 'none', stroke: 'rgba(255,217,142,.6)', 'stroke-width': 2.5, 'stroke-dasharray': '14 16' });
    const e = box(r, x, y, 130, 130, '', `<div class="cx" style="width:130px;height:130px;border-radius:34px;background:#120e09;box-shadow:inset 0 0 0 2px rgba(255,217,142,.5),0 0 40px rgba(242,173,60,.25);color:#fff">${ic(icn, '', 'style="width:64px;height:64px"')}</div>`);
    const dots = []; for (let k = 0; k < 7; k++) dots.push(sv(svg, 'circle', { r: 8, fill: '#ffd98e', filter: 'url(#glow)' }));
    return { road, lane, e, dots, len: road.getTotalLength() };
  });
  s.site = box(r, 540, 640, 380, 260, 'glass', `<div style="position:absolute;inset:14px;border-radius:14px;background:url(site-tribe.jpg) center top/cover"></div><div class="cx" style="position:absolute;left:50%;bottom:-32px;transform:translateX(-50%);width:68px;height:68px;border-radius:50%;background:linear-gradient(180deg,#ffd98e,#f2ad3c);color:#1b140c">${ic('store', '', 'style="width:36px;height:36px"')}</div>`);
  s.ring = box(r, 540, 640, 440, 440, '', '', 'border-radius:50%;box-shadow:0 0 0 3px rgba(255,217,142,.8),0 0 50px rgba(242,173,60,.6)');
  s.find = box(r, 540, 1110, 1040, 90, 'disp gt', 'The right people find you.', 'font-size:76px');
  s.bbr = box(r, 540, 200, 1000, 34, 'mono', 'Blueprint. Build. Roads.', 'font-size:22px;color:#ffd98e;letter-spacing:.4em');
}, (t, r, s) => {
  const A = out(t, S(71.45), .3), B = ez.out(lin(t, S(71.6), S(72.1))), g = out(t, S(76.15), .35);
  const bpk = ez.out(lin(t, S(62.85), S(63.4))); set(s.bp, { o: bpk * A, s: .97 + .03 * bpk });
  { const k = ez.out(lin(t, S(64.4), S(64.85))); set(s.title, { o: k * A, y: (1 - k) * 18 }); shine(s.svT, t, S(64.8), 1); }
  const wk = lin(t, S(65.85), S(65.95));
  const draw = ez.inOut(lin(t, S(65.9), S(67.1))), reveal = ez.inOut(lin(t, S(67.34), S(67.95)));
  const dup = ez.back(lin(t, S(68.8), S(69.5)));
  [s.main, ...s.copies].forEach((w, i) => {
    const isMain = i === 0, side = i === 1 ? -1 : 1;
    set(w, { o: (isMain ? wk : lin(t, S(68.75), S(68.95))) * A, x: isMain ? 0 : side * 150 * dup, y: isMain ? -10 * dup : 30 * dup, r: isMain ? 0 : side * 7 * dup, s: isMain ? 1 - .1 * dup : .9 });
    w.querySelectorAll('.wire rect').forEach(rc => rc.setAttribute('stroke-dashoffset', (+rc.dataset.l * (1 - (isMain ? draw : 1))).toFixed(1)));
    const sh = w.querySelector('.shot'); sh.style.clipPath = `inset(0 0 ${(isMain ? (1 - reveal) * 100 : 0).toFixed(1)}% 0)`; sh.style.opacity = isMain ? (reveal > 0 ? 1 : 0) : 1;
    w.querySelector('.wire').style.opacity = isMain ? (1 - reveal) : 0;
    const lk = w.querySelector('.lnk'), p = pop(t, S(70.38) + [.12, 0, .24][i]); set(lk, { o: p.o, s: p.s });
  });
  { slam(s.links, t, S(70.82), 1.35); s.links.style.opacity *= A; shine(s.links, t, S(71.0), .8); }
  const rd = ez.inOut(lin(t, S(72.5), S(73.3)));
  s.src.forEach((q, i) => {
    q.road.setAttribute('stroke-dasharray', q.len); q.road.setAttribute('stroke-dashoffset', (q.len * (1 - rd)).toFixed(1)); q.road.setAttribute('opacity', (B * g).toFixed(3));
    q.lane.setAttribute('opacity', (rd * B * g).toFixed(3)); q.lane.setAttribute('stroke-dashoffset', (-t * 60).toFixed(1));
    const p = pop(t, S(73.6) + i * .1); set(q.e, { o: p.o * B * g, s: p.s });
    const fast = 1 + 1.4 * lin(t, S(74.7), S(75.2));
    q.dots.forEach((d, k) => {
      if (t < S(73.0)) { d.setAttribute('opacity', 0); return; }
      const ph = ((t - S(73.0)) * .32 * fast + k / q.dots.length) % 1, pt = q.road.getPointAtLength(q.len * ph);
      d.setAttribute('cx', pt.x.toFixed(1)); d.setAttribute('cy', pt.y.toFixed(1)); d.setAttribute('opacity', (Math.sin(Math.PI * ph) * B * g * lin(t, S(73.0), S(73.4))).toFixed(3));
    });
  });
  { const p = pop(t, S(71.75)); set(s.site, { o: p.o * B * g, s: p.s }); }
  { const k = lin(t, S(74.7), S(75.6)); set(s.ring, { o: (1 - k) * (k > 0 ? 1 : 0) * g, s: .6 + k * .9 }); }
  { const k = ez.out(lin(t, S(75.55), S(75.95))); set(s.find, { o: k * g, y: (1 - k) * 20 }); shine(s.find, t, S(75.9), 1); }
  { const k = ez.out(lin(t, S(72.2), S(72.6))); set(s.bbr, { o: k * g * B }); }
});

/* ===================== 7. STAND ON YOUR OWN FEET ===================== */
chapter(S(76.8), 'Stand on your own feet');
av(S(76.5), 'split', .55); av(S(85.55), 'hidden', .35);
E.scene('stand', S(76.45), S(86.0), (r, s) => {
  s.title = box(r, 540, 830, 1000, 80, 'disp st', 'Stand on your own feet', 'font-size:70px');
  s.ground = el(r, '', '', 'left:140px;top:1300px;width:300px;height:4px;border-radius:2px;background:linear-gradient(90deg,transparent,#f2ad3c,transparent);box-shadow:0 0 20px #f2ad3c');
  s.fig = box(r, 290, 1110, 300, 380, '', `<svg width="300" height="380" viewBox="0 0 300 380" fill="none" stroke="#ffd98e" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 16px rgba(242,173,60,.6))">
     <circle cx="150" cy="70" r="46"/><path d="M150 120 L150 250"/><path d="M150 150 L80 210"/><path d="M150 150 L220 210"/><path d="M150 250 L100 360"/><path d="M150 250 L200 360"/></svg>`, 'transform-origin:50% 100%');
  s.rows = [['wallet', 'Create your wallet', 79.58], ['lock', 'Secure it yourself', 80.04], ['users', 'Join by yourself', 81.88], ['send', 'Transact by yourself', 82.34]].map(([icn, lb, ts], i) => {
    const e = el(r, '', `<div style="display:flex;align-items:center;gap:14px;height:100%"><span class="ck cx" style="width:48px;height:48px;border-radius:12px;box-shadow:inset 0 0 0 2px rgba(255,217,142,.6);color:#1b140c;flex:none">${ic('check', '', 'style="width:30px;height:30px;stroke-width:3.4"')}</span>${ic(icn, '', 'style="width:32px;height:32px;color:#ffd98e"')}<b style="font:800 30px/1 var(--f-b);white-space:nowrap">${lb}</b></div>`, `left:500px;top:${930 + i * 92}px;width:520px;height:66px`);
    return { e, t: S(ts), ck: e.querySelector('.ck') };
  });
  const svg = svgLayer(r);
  s.strings = [[210, 930, 219, 1061], [290, 910, 290, 1005], [370, 930, 361, 1061]].map(([x1, y1, x2, y2]) => ({ top: sv(svg, 'line', { x1, y1, x2: x1, y2: y1, stroke: '#e9e4dc', 'stroke-width': 2.5 }), bot: sv(svg, 'line', { x1: x2, y1: y2, x2, y2, stroke: '#e9e4dc', 'stroke-width': 2.5 }), x1, y1, x2, y2 }));
  s.bar = box(r, 290, 916, 360, 60, '', `<div style="position:absolute;left:0;right:0;top:20px;height:20px;border-radius:10px;background:linear-gradient(180deg,#6b6157,#3a332b);box-shadow:0 8px 20px rgba(0,0,0,.6)"></div><div style="position:absolute;left:170px;top:-40px;width:20px;height:110px;border-radius:10px;background:linear-gradient(90deg,#6b6157,#3a332b)"></div><span class="mono" style="position:absolute;left:0;right:0;top:-74px;font-size:18px;color:#bdb5a8">So-called leader</span>`);
  s.sc = box(r, 140, 990, 84, 84, '', ic('scissors', '', 'style="width:74px;height:74px;color:#fff6dc;filter:drop-shadow(0 0 12px #f2ad3c)"'));
  s.free = box(r, 690, 1110, 640, 220, 'disp gt', '<span>No strings<br>attached.</span>', 'font-size:110px;line-height:.95');
}, (t, r, s) => {
  const g = out(t, S(85.6), .3);
  { const k = ez.out(lin(t, S(77.85), S(78.3))); set(s.title, { o: k * g * out(t, S(83.2), .3), y: (1 - k) * 18 }); shine(s.title, t, S(78.2), 1); }
  const rise = ez.back(lin(t, S(77.9), S(78.6))), fin = ez.out(lin(t, S(76.85), S(77.3)));
  set(s.fig, { o: fin * g, sy: .62 + .38 * clamp(rise, 0, 1.1), sx: 1, x: -10 * (1 - fin) });
  set(s.ground, { o: fin * g * (.4 + .6 * rise) });
  const ckOut = out(t, S(83.25), .35);
  s.rows.forEach(rw => { const k = ez.out(lin(t, rw.t - .25, rw.t + .1)); set(rw.e, { o: k * ckOut * g, x: (1 - k) * 30 }); const c = lin(t, rw.t, rw.t + .15); rw.ck.style.background = c > 0 ? `rgba(242,173,60,${c})` : 'transparent'; rw.ck.firstChild.style.opacity = c; });
  const down = ez.out(lin(t, S(83.4), S(84.1))), barFly = ez.in(lin(t, S(85.1), S(85.6)));
  set(s.bar, { o: down * g, y: (1 - down) * -220 - barFly * 400, r: barFly * -12 });
  s.strings.forEach((q, i) => {
    const ci = clamp((t - S(85.06) - i * .06) / .3), mid = mix(q.y1, q.y2, .45), yTop = q.y1 + (1 - down) * -220 - barFly * 400;
    q.top.setAttribute('y1', yTop);
    if (ci <= 0) { q.top.setAttribute('x2', q.x2); q.top.setAttribute('y2', q.y2); q.bot.setAttribute('opacity', 0); }
    else { q.top.setAttribute('x2', mix(q.x1, q.x2, .45)); q.top.setAttribute('y2', mix(mid, yTop, ci)); q.bot.setAttribute('x1', mix(q.x1, q.x2, .45)); q.bot.setAttribute('y1', mix(mid, q.y2, ci) + ci * ci * 60); q.bot.setAttribute('opacity', (down * g * (1 - ci)).toFixed(3)); }
    q.top.setAttribute('opacity', (down * g * (1 - ci * .6)).toFixed(3));
  });
  { const k = lin(t, S(84.75), S(85.15)); set(s.sc, { o: (k > 0 && k < 1 ? 1 : 0) * g, x: k * 420, r: Math.sin(t * 40) * 14 }); }
  { slam(s.free, t, S(85.15), 1.5); s.free.style.opacity *= g; shine(s.free, t, S(85.3), .7); }
});
E.scene('keys', S(85.75), S(88.405), (r, s) => {
  s.rows = [['wallet', 'Wallet', 85.86], ['key-round', 'Keys', 86.70], ['compass', 'Decisions', 87.46]].map(([icn, w, ts], i) => {
    const e = el(r, '', `<div style="display:flex;flex-direction:column;align-items:center;gap:18px"><span class="ibox" style="width:130px;height:130px;display:grid">${ic(icn, '', 'style="width:70px;height:70px"')}</span><span style="display:flex;gap:28px;align-items:baseline"><span class="disp st" style="font-size:126px">Your</span><span class="disp gt kw" style="font-size:126px">${w}</span></span></div>`, `left:0;top:${300 + i * 330}px;width:1080px;height:300px;display:flex;justify-content:center`);
    shake(S(ts), 9); return { e, t: S(ts), kw: e.querySelector('.kw') };
  });
  flash(S(88.36), .3, .4);
}, (t, r, s) => {
  const gk = lin(t, S(88.1), S(88.405));
  s.rows.forEach(rw => { const k = lin(t, rw.t, rw.t + .2); set(rw.e, { o: lin(t, rw.t - .01, rw.t + .06) * (1 - gk), s: (k <= 0 ? 1.5 : 1.5 - .5 * ez.out(k)) * (1 + gk * .2), b: (1 - ez.out(k)) * 6 + gk * 8 }); shine(rw.kw, t, rw.t + .15, .7); });
});

/* ===================== 8. YOUR OWN TRIBE ===================== */
chapter(S(89.0), 'Your own tribe');
av(S(88.85), 'split', .5); av(S(91.5), 'pip', .5);
E.scene('tribe', S(88.79), S(103.05), (r, s) => {
  s.ch1 = el(r, '', `<div style="display:flex;align-items:center;gap:24px;justify-content:center">${ic('flag', '', 'style="width:92px;height:92px;color:#ffd98e"')}<span class="disp gt ch-t" style="font-size:96px">MTG's challenge</span></div>`, 'left:40px;top:880px;width:1000px;height:110px');
  s.chT = s.ch1.querySelector('.ch-t');
  s.ch2 = box(r, 540, 1110, 1000, 200, 'disp st', '<span>Start your<br>own tribe.</span>', 'font-size:104px;line-height:.95');
  s.shoutLab = box(r, 540, 300, 1040, 200, 'disp st', "<span>Shouting isn't<br>leading.</span>", 'font-size:100px;line-height:.98');
  s.mega = box(r, 270, 780, 260, 260, '', ic('megaphone', '', 'style="width:220px;height:220px;color:#bdb5a8"'));
  s.shouts = ['JOIN!', 'JOIN NOW!', 'JOIN!!'].map((x, i) => box(r, 560, 680 + i * 100, 300, 70, 'disp', x, 'font-size:60px;color:#bdb5a8'));
  s.crowd = [0, 1, 2, 3].map(i => box(r, 780 + (i % 2) * 150, 700 + Math.floor(i / 2) * 160, 120, 120, '', ic('user', '', 'style="width:96px;height:96px;color:#8d877e"')));
  s.megaX = box(r, 270, 780, 320, 320, '', `<svg width="320" height="320" viewBox="0 0 320 320"><path d="M50 50 L270 270 M270 50 L50 270" stroke="#f2ad3c" stroke-width="20" stroke-linecap="round" style="filter:drop-shadow(0 0 14px rgba(242,173,60,.8))"/></svg>`);
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  const C = { x: 540, y: 615 };
  const L1 = [-150, -30, 90].map(a => ({ x: C.x + Math.cos(a * Math.PI / 180) * 300, y: C.y + Math.sin(a * Math.PI / 180) * 215 }));
  const L2 = [-170, -125, -55, -10, 40, 140, 115].map(a => ({ x: C.x + Math.cos(a * Math.PI / 180) * 440, y: C.y + Math.sin(a * Math.PI / 180) * 345 }));
  const par = [0, 0, 1, 1, 2, 0, 2];
  const crown = [[0, -250], [-360, -160], [-170, 0], [170, 0], [360, -160], [-360, 20], [360, 20], [-360, 190], [-120, 190], [120, 190], [360, 190]].map(([x, y]) => ({ x: C.x + x, y: C.y + y }));
  s.nodes = [{ p: C, lit: S(94.22), par: null, lab: 'You', ci: 0 }]
    .concat(L1.map((p, i) => ({ p, lit: S([95.16, 95.84, 96.54][i]) + .3, par: 0, lab: ['Teach', 'Train', 'Coach'][i], ci: [1, 4, 9][i] })))
    .concat(L2.map((p, i) => ({ p, lit: S(97.1) + i * .18, par: 1 + par[i], lab: null, ci: [5, 2, 3, 6, 10, 7, 8][i] })));
  s.nodes.forEach(n => { n.c = crown[n.ci]; }); s.byCrown = []; s.nodes.forEach((n, i) => { s.byCrown[n.ci] = i; });
  s.lines = s.nodes.map(n => n.par == null ? null : sv(svg, 'line', { stroke: 'url(#gg)', 'stroke-width': 4, 'stroke-linecap': 'round', filter: 'url(#glow)' }));
  s.crownPath = sv(svg, 'path', { fill: 'none', stroke: '#ffd98e', 'stroke-width': 5, 'stroke-linejoin': 'round', filter: 'url(#glow2)' });
  s.crownOrder = [7, 5, 1, 2, 0, 3, 4, 6, 10, 9, 8, 7];
  s.nodeEls = s.nodes.map((n, i) => {
    const sz = i === 0 ? 124 : 90;
    const e = box(r, 0, 0, sz, sz, '', `<div class="cx nd" style="width:${sz}px;height:${sz}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#3a2e1f,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.35)">
       <span class="fl" style="color:#ffd98e">${ic('flame', '', `style="width:${sz * .55}px;height:${sz * .55}px"`)}</span></div>
       ${n.lab ? `<span class="mono nl" style="position:absolute;left:50%;top:${sz + 10}px;transform:translateX(-50%);font-size:${i === 0 ? 24 : 20}px;color:#ffd98e;white-space:nowrap">${n.lab}</span>` : ''}`);
    return { e, nd: e.querySelector('.nd'), fl: e.querySelector('.fl'), nl: e.querySelector('.nl'), sz };
  });
  s.lead = box(r, 540, 1110, 1040, 100, 'disp gt', 'Lead with value', 'font-size:96px');
  s.candle = box(r, 540, 1112, 980, 120, '', 'A candle loses nothing by lighting another.', 'font:italic 600 52px/1.18 var(--f-b);color:#f7e6bf');
  s.bnb = box(r, 540, 1110, 1040, 100, 'disp gt', 'Built, not bought.', 'font-size:96px');
  shake(S(90.64), 7);
}, (t, r, s) => {
  const A = out(t, S(91.4), .3), g = out(t, S(102.85), .3);
  { const k = ez.out(lin(t, S(89.35), S(89.8))); set(s.ch1, { o: k * A, y: (1 - k) * 20 }); shine(s.chT, t, S(89.7), 1); }
  { slam(s.ch2, t, S(90.64), 1.5); s.ch2.style.opacity *= A; shine(s.ch2, t, S(90.8), .8); }
  const M = ez.out(lin(t, S(91.7), S(92.1))), Mo = out(t, S(93.55), .3);
  set(s.mega, { o: M * Mo, r: Math.sin(t * 30) * 2 * M, x: (1 - M) * -40 });
  s.shouts.forEach((e, i) => { const t0 = S([92.1, 92.4, 92.7][i]), k = lin(t, t0, t0 + .6); set(e, { o: (k > 0 ? 1 - k * .7 : 0) * Mo, x: k * 160, s: .7 + .5 * k }); });
  s.crowd.forEach((e, i) => { const k = ez.inOut(lin(t, S(92.6) + i * .08, S(93.3) + i * .08)); set(e, { o: M * Mo * (1 - k * .8), x: k * 120, s: 1 - .2 * k }); });
  { slam(s.megaX, t, S(93.1), 1.6); s.megaX.style.opacity *= Mo; }
  { const k = ez.out(lin(t, S(92.85), S(93.25))); set(s.shoutLab, { o: k * Mo, y: (1 - k) * 18 }); shine(s.shoutLab, t, S(93.1), .8); }
  const form = ez.inOut(lin(t, S(101.15), S(102.1)));
  const P = s.nodes.map(n => ({ x: mix(n.p.x, n.c.x, form), y: mix(n.p.y, n.c.y, form) }));
  s.nodes.forEach((n, i) => {
    const ne = s.nodeEls[i], appear = i === 0 ? S(93.85) : (n.par === 0 ? n.lit - .45 : n.lit - .35);
    const p = pop(t, appear);
    ne.e.style.left = (P[i].x - ne.sz / 2) + 'px'; ne.e.style.top = (P[i].y - ne.sz / 2) + 'px';
    set(ne.e, { o: p.o * g, s: p.s });
    const lit = lin(t, n.lit, n.lit + .2), fl = 1 + .08 * Math.sin(t * 17 + i * 2.1) * lit;
    ne.fl.style.opacity = (.25 + .75 * lit).toFixed(3); ne.fl.style.transform = `scale(${(.8 + .2 * lit) * fl})`; ne.fl.style.color = lit > .5 ? '#fff1c9' : '#8d877e';
    ne.nd.style.boxShadow = `inset 0 0 0 2px rgba(255,217,142,${(.35 + .5 * lit).toFixed(2)}),0 0 ${(50 * lit).toFixed(0)}px rgba(242,173,60,${(.7 * lit).toFixed(2)})`;
    if (ne.nl) ne.nl.style.opacity = (lin(t, n.lit, n.lit + .25) * (1 - form)).toFixed(3);
    const ln = s.lines[i];
    if (ln) { const a = P[n.par], b = P[i], k = ez.out(lin(t, n.lit - .32, n.lit)); ln.setAttribute('x1', a.x); ln.setAttribute('y1', a.y); ln.setAttribute('x2', mix(a.x, b.x, k)); ln.setAttribute('y2', mix(a.y, b.y, k)); ln.setAttribute('opacity', ((k > 0 ? 1 : 0) * g * (1 - form)).toFixed(3)); }
  });
  const cp = s.crownOrder.map(ci => P[s.byCrown[ci]]); s.crownPath.setAttribute('d', 'M ' + cp.map(p => `${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(' L ') + ' Z');
  s.crownPath.setAttribute('opacity', (lin(t, S(101.7), S(102.2)) * g).toFixed(3));
  { const k = ez.out(lin(t, S(94.15), S(94.55))), o = out(t, S(98.6), .3); set(s.lead, { o: k * o * g, y: (1 - k) * 18 }); shine(s.lead, t, S(94.5), 1); }
  { const k = ez.out(lin(t, S(98.85), S(99.4))), o = out(t, S(101.0), .3); set(s.candle, { o: k * o * g, y: (1 - k) * 14 }); }
  { slam(s.bnb, t, S(102.2), 1.4); s.bnb.style.opacity *= g; shine(s.bnb, t, S(102.35), .8); }
});

/* ===================== 9. ACTION TAKERS ===================== */
chapter(S(103.1), 'Action takers');
av(S(102.95), 'split', .5); av(S(105.45), 'pip', .5);
E.scene('action', S(102.9), S(116.3), (r, s) => {
  s.a1 = box(r, 540, 850, 1000, 34, 'mono', 'The MTG TRIBE is', 'font-size:24px;color:#ffd98e;letter-spacing:.4em');
  s.a2 = box(r, 540, 950, 1000, 100, 'disp st', 'A tribe of', 'font-size:104px');
  s.a3 = el(r, '', `<div style="display:flex;align-items:center;justify-content:center;gap:16px">${ic('zap', '', 'style="width:110px;height:110px;color:#ffd98e;filter:drop-shadow(0 0 16px #f2ad3c)"')}<span class="disp gt a3t" style="font-size:134px">Action takers</span></div>`, 'left:0;top:1030px;width:1080px;height:160px');
  s.a3t = s.a3.querySelector('.a3t');
  s.card = el(r, 'glass', `<div style="padding:34px 38px;display:flex;flex-direction:column;gap:20px;height:100%">
     <span class="mono" style="font-size:20px;color:#ffd98e">Gym membership</span>
     <span class="disp" style="font-size:80px;color:#efe9df">Member</span>
     <div style="height:56px;background:repeating-linear-gradient(90deg,#efe9df 0 3px,transparent 3px 7px,#efe9df 7px 8px,transparent 8px 13px);opacity:.7;border-radius:4px"></div></div>`, 'left:280px;top:230px;width:520px;height:300px');
  s.cardX = box(r, 540, 380, 270, 270, '', `<svg width="270" height="270" viewBox="0 0 260 260"><path d="M40 40 L220 220 M220 40 L40 220" stroke="#ff7a4d" stroke-width="18" stroke-linecap="round" style="filter:drop-shadow(0 0 14px rgba(255,90,40,.7))"/></svg>`);
  s.cardLab = box(r, 540, 570, 600, 50, 'mono', 'Joining', 'font-size:28px;color:#ff9a7a');
  s.dumb = box(r, 540, 660, 130, 130, '', ic('dumbbell', '', 'style="width:116px;height:116px;color:#ffd98e;filter:drop-shadow(0 0 14px #f2ad3c)"'));
  s.cells = []; for (let i = 0; i < 30; i++) { const cx = 350 + (i % 6) * 76, cy = 770 + Math.floor(i / 6) * 58; s.cells.push(box(r, cx, cy, 62, 46, '', ic('check', '', 'style="width:26px;height:26px;stroke-width:3.4;opacity:0"'), 'border-radius:10px;box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.3);color:#1b140c')); }
  s.day = box(r, 540, 1048, 600, 50, 'mono', 'Day 0', 'font-size:30px;color:#ffd98e');
  s.showLab = box(r, 540, 1120, 900, 70, 'disp gt', 'Showing up ✓', 'font-size:72px');
  const pos = [[540, 380], [310, 770], [770, 770]];
  s.loop = [['circle-play', 'Watch', 109.98], ['hammer', 'Do the work', 111.14], ['graduation-cap', 'Teach', 112.28]].map(([icn, lb, ts], i) => {
    const e = box(r, pos[i][0], pos[i][1], 230, 230, '', `<div class="cx lp" style="width:230px;height:230px;border-radius:50%;flex-direction:column;gap:10px;background:radial-gradient(circle at 35% 30%,#3a2e1f,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.4)">${ic(icn, '', 'style="width:88px;height:88px;color:#ffd98e"')}<b class="mono" style="font-size:19px;color:#f7e6bf;letter-spacing:.2em">${lb}</b></div>`);
    return { e, lp: e.querySelector('.lp'), t: S(ts) };
  });
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  s.arc = sv(svg, 'circle', { cx: 540, cy: 640, r: 270, fill: 'none', stroke: 'url(#gg)', 'stroke-width': 4, 'stroke-dasharray': '20 22', filter: 'url(#glow)' });
  s.house = el(r, '', `<svg width="620" height="560" viewBox="0 0 620 560" fill="none" stroke="#ffd98e" stroke-width="8" stroke-linejoin="round" stroke-linecap="round" style="filter:drop-shadow(0 0 14px rgba(242,173,60,.6))">
    <path class="hp" d="M40 260 L310 40 L580 260"/><path class="hp" d="M90 220 L90 520 L530 520 L530 220"/><path class="hp" d="M250 520 L250 360 L370 360 L370 520"/>
    <rect class="hw" x="130" y="290" width="90" height="80" rx="8" fill="rgba(255,217,142,0)"/><rect class="hw" x="400" y="290" width="90" height="80" rx="8" fill="rgba(255,217,142,0)"/>
    <rect class="hd" x="256" y="366" width="108" height="150" fill="rgba(255,217,142,0)" stroke="none"/></svg>`, 'left:230px;top:330px;width:620px;height:560px');
  s.hp = Array.from(s.house.querySelectorAll('.hp')); s.hp.forEach(p => { const L = p.getTotalLength(); p.style.strokeDasharray = L; p.dataset.l = L; });
  s.hw = Array.from(s.house.querySelectorAll('.hw')); s.hd = s.house.querySelector('.hd');
  s.chair = box(r, 540, 780, 80, 80, '', ic('armchair', '', 'style="width:64px;height:64px;color:#1b140c"'));
  s.seat = box(r, 540, 1060, 1040, 200, 'disp gt', '<span>Your seat<br>is waiting.</span>', 'font-size:100px;line-height:.98');
  shake(S(104.9), 8);
}, (t, r, s) => {
  const A = out(t, S(105.35), .3), G = out(t, S(109.6), .3), L = out(t, S(113.25), .3), g = out(t, S(116.1), .35);
  up(s.a1, t, S(103.2)); s.a1.style.opacity *= A;
  up(s.a2, t, S(104.2)); s.a2.style.opacity *= A;
  { slam(s.a3, t, S(104.9), 1.5); s.a3.style.opacity *= A; shine(s.a3t, t, S(105.05), .9); }
  const gi = ez.out(lin(t, S(106.2), S(106.7)));
  set(s.card, { o: gi * G * (1 - .45 * lin(t, S(107.4), S(107.7))), y: (1 - gi) * -40, r: -3 });
  { slam(s.cardX, t, S(107.4), 1.7); s.cardX.style.opacity *= G; }
  { const k = ez.out(lin(t, S(107.5), S(107.8))); set(s.cardLab, { o: k * G }); }
  const di = ez.out(lin(t, S(106.4), S(106.9))), rep = Math.max(0, Math.sin((t - S(108.6)) * 14)) * lin(t, S(108.6), S(108.8)) * (1 - lin(t, S(109.3), S(109.5)));
  set(s.dumb, { o: di * G, y: -rep * 22 });
  let n = 0; s.cells.forEach((c, i) => { const t0 = S(108.62) + i * .024, k = lin(t, t0, t0 + .08); if (k > 0) n = i + 1; set(c, { o: di * G, s: 1 + .15 * Math.sin(Math.PI * k) }); c.style.background = k > 0 ? `rgba(242,173,60,${(.9 * k).toFixed(2)})` : 'transparent'; c.firstChild.style.opacity = k; });
  s.day.textContent = 'Day ' + n; set(s.day, { o: di * G });
  { slam(s.showLab, t, S(109.04), 1.4); s.showLab.style.opacity *= G; }
  const li = ez.out(lin(t, S(109.75), S(110.1)));
  s.arc.setAttribute('opacity', (li * L).toFixed(3)); s.arc.setAttribute('transform', `rotate(${(t * 40).toFixed(1)} 540 640)`);
  s.loop.forEach(q => { const p = pop(t, q.t - .25), lit = lin(t, q.t, q.t + .25); set(q.e, { o: p.o * L, s: p.s * (1 + .06 * Math.exp(-Math.pow((t - q.t - .15) / .12, 2))) }); q.lp.style.boxShadow = `inset 0 0 0 2px rgba(255,217,142,${(.4 + .5 * lit).toFixed(2)}),0 0 ${(60 * lit).toFixed(0)}px rgba(242,173,60,${(.6 * lit).toFixed(2)})`; });
  const hd = ez.inOut(lin(t, S(113.6), S(114.7)));
  s.hp.forEach((p, i) => p.style.strokeDashoffset = (+p.dataset.l * (1 - clamp(hd * 1.4 - i * .2))).toFixed(1));
  set(s.house, { o: lin(t, S(113.5), S(113.7)) * g });
  const wl = ez.out(lin(t, S(115.1), S(115.5)));
  s.hw.forEach(w => w.setAttribute('fill', `rgba(255,217,142,${(.85 * wl).toFixed(2)})`)); s.hd.setAttribute('fill', `rgba(255,236,190,${(.95 * wl).toFixed(2)})`);
  { const p = pop(t, S(115.3)); set(s.chair, { o: p.o * g, s: p.s }); }
  { const k = ez.out(lin(t, S(115.3), S(115.7))); set(s.seat, { o: k * g, y: (1 - k) * 18 }); shine(s.seat, t, S(115.6), 1); }
});

/* ===================== 10. YOUR ONE STEP ===================== */
chapter(S(116.4), 'Your one step');
av(S(116.15), 'split', .5); av(S(131.95), 'pip', .5);
E.scene('cta', S(116.1), S(132.4), (r, s) => {
  s.one = box(r, 540, 1050, 320, 320, '', `<div class="cx" style="width:300px;height:300px;border-radius:50%;box-shadow:inset 0 0 0 4px #f2ad3c,0 0 60px rgba(242,173,60,.4);background:radial-gradient(circle at 40% 30%,rgba(255,217,142,.15),rgba(0,0,0,.4))"><span class="disp gt one-t" style="font-size:236px;line-height:1">1</span></div>`);
  s.oneT = s.one.querySelector('.one-t');
  s.oneL = box(r, 540, 1250, 800, 40, 'mono', 'One step', 'font-size:30px;color:#ffd98e;letter-spacing:.5em');
  s.hdr = box(r, 540, 808, 1000, 30, 'mono', 'Your one step', 'font-size:22px;color:#ffd98e;letter-spacing:.42em');
  s.btn = el(r, '', `<div style="display:flex;align-items:center;justify-content:center;gap:22px;height:100%;padding:0 34px">${ic('whatsapp', '', 'style="width:64px;height:64px;color:#fff;flex:none"')}<span class="ty" style="font:800 54px/1 var(--f-b);color:#fff;letter-spacing:-.01em;white-space:nowrap"></span><span class="cur" style="width:4px;height:54px;background:#fff"></span></div>`,
    'left:80px;top:834px;width:920px;height:126px;border-radius:63px;background:linear-gradient(180deg,#34e07a,#14a34f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.25),0 20px 50px rgba(20,163,79,.35)');
  s.ty = s.btn.querySelector('.ty'); s.cur = s.btn.querySelector('.cur');
  s.ripple = box(r, 800, 897, 110, 110, '', '', 'border-radius:50%;box-shadow:0 0 0 4px rgba(255,255,255,.8)');
  s.ptr = box(r, 0, 0, 76, 76, '', ic('mouse-pointer-click', '', 'style="width:70px;height:70px;color:#fff;filter:drop-shadow(0 4px 10px rgba(0,0,0,.8))"'));
  s.join = box(r, 540, 1000, 1000, 64, '', `<span class="chip" style="font-size:28px">${ic('users')}Join the WhatsApp tribe</span>`);
  s.tt = el(r, '', `<div style="display:flex;align-items:center;gap:22px;height:100%;padding:0 30px">${ic('tiktok', '', 'style="width:52px;height:52px;color:#fff"')}<span style="display:flex;flex-direction:column;gap:8px"><b style="font:800 42px/1 var(--f-b)">@joinmtgtribe</b><small class="mono" style="font-size:16px;color:#ffd98e">Follow us on TikTok</small></span></div>`, 'left:80px;top:1052px;width:920px;height:96px;' + cardCss);
  s.wa = el(r, '', `<div style="display:flex;align-items:center;gap:22px;height:100%;padding:0 30px">${ic('whatsapp', '', 'style="width:52px;height:52px;color:#25d366"')}<span style="display:flex;flex-direction:column;gap:8px"><b style="font:800 40px/1 var(--f-b);white-space:nowrap">WhatsApp MTG: 072 171 4626</b><small class="mono" style="font-size:16px;color:#ffd98e">Talk to me directly</small></span></div>`, 'left:80px;top:1160px;width:920px;height:96px;' + cardCss);
  s.vn = el(r, '', `<div style="display:flex;align-items:center;gap:14px;height:100%;padding:0 22px">${ic('mic', '', 'style="width:32px;height:32px;color:#ffd98e"')}<span class="bars" style="display:flex;align-items:center;gap:5px;height:40px"></span><b class="mono" style="font-size:16px;color:#f7e6bf">Voice note</b></div>`, 'left:80px;top:1268px;width:420px;height:56px;border-radius:28px;background:rgba(20,16,10,.9);box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.35)');
  s.bars = []; const bw = s.vn.querySelector('.bars'); for (let i = 0; i < 16; i++) { const b = document.createElement('i'); b.style.cssText = 'display:block;width:5px;border-radius:3px;background:#ffd98e;height:10px'; bw.appendChild(b); s.bars.push(b); }
  s.pay = box(r, 540, 1352, 1000, 64, 'disp gt', 'Pay attention. Take action.', 'font-size:60px');
  s.text = 'mtgtribe.com/group';
  shake(S(131.58), 6);
}, (t, r, s) => {
  const g = out(t, S(131.95), .35);
  { const p = pop(t, S(116.45)), o = out(t, S(117.6), .3); set(s.one, { o: p.o * o, s: p.s * (1 + .06 * Math.exp(-Math.pow((t - S(116.9)) / .1, 2))) }); shine(s.oneT, t, S(116.7), .9);
    const k = ez.out(lin(t, S(116.84), S(117.1))); set(s.oneL, { o: k * o }); }
  { const k = ez.out(lin(t, S(117.6), S(118.0))); set(s.hdr, { o: k * g }); }
  const bi = ez.back(lin(t, S(117.75), S(118.2))), press = Math.exp(-Math.pow((t - S(120.88)) / .07, 2));
  set(s.btn, { o: lin(t, S(117.75), S(117.9)) * g, s: (.8 + .2 * clamp(bi, 0, 1.1)) * (1 - .05 * press) });
  s.ty.textContent = s.text.slice(0, Math.round(s.text.length * lin(t, S(118.08), S(120.16))));
  s.cur.style.opacity = (t < S(120.5) && Math.floor(t * 3) % 2 === 0) || (t > S(118.0) && t < S(120.2)) ? 1 : 0;
  const pk = ez.inOut(lin(t, S(120.15), S(120.75)));
  s.ptr.style.left = mix(980, 790, pk) + 'px'; s.ptr.style.top = mix(1180, 900, pk) + 'px';
  set(s.ptr, { o: lin(t, S(120.1), S(120.25)) * (1 - lin(t, S(121.6), S(121.9))) * g, s: 1 - .15 * press });
  { const k = lin(t, S(120.84), S(121.5)); set(s.ripple, { o: k > 0 ? (1 - k) * g : 0, s: .5 + 2.2 * k }); }
  { const p = pop(t, S(121.0)); set(s.join, { o: p.o * g, s: p.s }); }
  { const k = ez.out(lin(t, S(122.6), S(123.0))); set(s.tt, { o: k * g, x: (1 - k) * 40 }); }
  { const k = ez.out(lin(t, S(126.8), S(127.2))); set(s.wa, { o: k * g, x: (1 - k) * 40 }); }
  { const k = ez.out(lin(t, S(129.2), S(129.55))); set(s.vn, { o: k * g, x: (1 - k) * 40 }); s.bars.forEach((b, i) => { b.style.height = (8 + 30 * Math.abs(Math.sin(t * 7 + i * .9) * Math.sin(t * 3.1 + i * .37))).toFixed(1) + 'px'; }); }
  { slam(s.pay, t, S(131.58), 1.4); s.pay.style.opacity *= g; shine(s.pay, t, S(131.7), .8); }
});

/* ===================== 11. THANK YOU ===================== */
chapter(S(132.2), 'Thank you');
av(S(150.2), 'hero', .6); av(S(153.95), 'hidden', .45);
E.scene('thanks', S(132.1), S(150.7), (r, s) => {
  s.nfa = box(r, 540, 640, 960, 480, 'glass', `<div style="display:flex;flex-direction:column;align-items:center;gap:26px;padding:0 40px"><span class="ibox" style="width:150px;height:150px;display:grid">${ic('shield-check', '', 'style="width:80px;height:80px"')}</span>
    <span class="disp st nfa1" style="font-size:90px">Not financial advice</span><span class="nfa2" style="font:700 44px/1 var(--f-b);color:#f7e6bf">Always do your own research.</span></div>`);
  s.nfa1 = s.nfa.querySelector('.nfa1'); s.nfa2 = s.nfa.querySelector('.nfa2');
  s.heart = box(r, 540, 640, 640, 640, '', ic('heart', '', 'style="width:600px;height:600px;color:rgba(242,173,60,.18);fill:rgba(242,173,60,.12)"'));
  s.soc = [['thumbs-up', 'Like', 139.06], ['share-2', 'Share', 139.62], ['message-circle', 'Comment', 140.16]].map(([icn, lb, ts], i) => {
    const x = 230 + i * 310;
    const e = box(r, x, 640, 220, 280, '', `<div class="cx" style="width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd98e,#c17a1e);box-shadow:0 0 50px rgba(242,173,60,.45),inset 0 0 0 3px rgba(255,246,220,.5);color:#1b140c">${ic(icn, '', 'style="width:92px;height:92px;stroke-width:2.4"')}</div><b class="mono" style="position:absolute;bottom:-8px;font-size:24px;color:#ffd98e">${lb}</b>`, 'flex-direction:column');
    const hearts = []; const rnd = E.rng(20 + i); for (let k = 0; k < 6; k++) hearts.push({ h: box(r, x, 580, 44, 44, '', ic('heart', '', 'style="width:38px;height:38px;color:#ffd98e;fill:#f2ad3c"')), vx: (rnd() - .5) * 220, vy: -220 - rnd() * 280, d: rnd() * .15 });
    return { e, t: S(ts), hearts };
  });
  s.card = el(r, '', `<div style="position:absolute;inset:0;border-radius:34px;background:linear-gradient(135deg,#2a2218 0%,#0d0b08 45%,#1d170f 100%);box-shadow:inset 0 0 0 2px rgba(255,217,142,.6),0 40px 100px rgba(0,0,0,.7),0 0 80px rgba(242,173,60,.2)"></div>
    <div class="sheen" style="position:absolute;inset:0;border-radius:34px;background:linear-gradient(110deg,transparent 35%,rgba(255,236,190,.22) 50%,transparent 65%);background-size:300% 100%"></div>
    <div style="position:absolute;left:46px;top:40px;display:flex;align-items:center;gap:14px"><span style="font-size:44px">👑</span><span class="disp gt" style="font-size:52px">MTG TRIBE</span></div>
    <span class="mono" style="position:absolute;right:46px;top:56px;font-size:18px;color:#bdb5a8">Tribe member</span>
    <div style="position:absolute;right:52px;top:120px;width:96px;height:72px;border-radius:14px;background:linear-gradient(135deg,#ffe7b0,#c17a1e);box-shadow:inset 0 0 0 2px rgba(0,0,0,.25)"><i style="position:absolute;left:0;right:0;top:35px;height:2px;background:rgba(0,0,0,.25)"></i><i style="position:absolute;top:0;bottom:0;left:47px;width:2px;background:rgba(0,0,0,.25)"></i></div>
    <span class="disp gt you" style="position:absolute;left:46px;top:236px;font-size:170px;line-height:1">You</span>
    <div style="position:absolute;left:52px;right:46px;bottom:38px;display:flex;justify-content:space-between">
      <span class="fld st1" style="display:flex;flex-direction:column;gap:8px"><small class="mono" style="font-size:14px;color:#bdb5a8">Status</small><b style="font:800 30px/1 var(--f-b);color:#ffd98e">Action Taker</b></span>
      <span class="fld" style="display:flex;flex-direction:column;gap:8px"><small class="mono" style="font-size:14px;color:#bdb5a8">Since</small><b style="font:800 30px/1 var(--f-b)">Today</b></span>
      <span class="fld" style="display:flex;flex-direction:column;gap:8px"><small class="mono" style="font-size:14px;color:#bdb5a8">Seat</small><b style="font:800 30px/1 var(--f-b)">Reserved</b></span></div>
    <span class="crown" style="position:absolute;left:58px;top:150px;font-size:100px;filter:drop-shadow(0 0 20px rgba(242,173,60,.8))">👑</span>`, 'left:120px;top:400px;width:840px;height:520px');
  s.sheen = s.card.querySelector('.sheen'); s.you = s.card.querySelector('.you'); s.crown = s.card.querySelector('.crown'); s.st1 = s.card.querySelector('.st1');
  flash(S(149.66), .4, .3);
}, (t, r, s) => {
  { const k = ez.out(lin(t, S(132.3), S(132.75))), o = out(t, S(136.85), .3); set(s.nfa, { o: k * o, s: .95 + .05 * k });
    const k1 = ez.out(lin(t, S(134.1), S(134.5))); set(s.nfa1, { o: .35 + .65 * k1 }); shine(s.nfa1, t, S(134.4), 1); const k2 = ez.out(lin(t, S(135.4), S(135.8))); set(s.nfa2, { o: k2, y: (1 - k2) * 12 }); }
  const so = out(t, S(142.7), .3);
  { const k = ez.out(lin(t, S(138.8), S(139.4))), beat = 1 + .05 * Math.max(0, Math.sin((t - S(141.04)) * 9)) * lin(t, S(141.0), S(141.2)); set(s.heart, { o: k * so, s: (.85 + .15 * k) * beat }); }
  s.soc.forEach(q => { const p = pop(t, q.t); set(q.e, { o: p.o * so, s: p.s });
    q.hearts.forEach(h => { const d = t - q.t - .1 - h.d; if (d < 0 || d > 1.1) { h.h.style.opacity = 0; return; } set(h.h, { o: (1 - d / 1.1) * so, x: h.vx * d, y: h.vy * d + 260 * d * d, s: .6 + .6 * d }); }); });
  const fl = ez.out(lin(t, S(143.05), S(143.85))), co = ez.in(lin(t, S(150.15), S(150.6)));
  set(s.card, { o: lin(t, S(143.05), S(143.25)) * (1 - co), ry: (1 - fl) * 88, p: 1600, s: (.92 + .08 * fl) * (1 - .3 * co), y: -co * 300 });
  s.sheen.style.backgroundPosition = `${(150 - 200 * ez.inOut(lin(t, S(144.1), S(145.3)))).toFixed(1)}% 0`;
  shine(s.you, t, S(145.4), 1.1);
  const gl = Math.exp(-Math.pow((t - S(144.6)) / .45, 2)); s.st1.style.filter = gl > .02 ? `drop-shadow(0 0 ${(18 * gl).toFixed(1)}px #f2ad3c)` : '';
  const cd = ez.out(lin(t, S(148.75), S(149.66)));
  set(s.crown, { o: lin(t, S(148.7), S(148.9)), y: (1 - cd) * -260, r: (1 - cd) * -25, s: 1 + .25 * Math.exp(-Math.pow((t - S(149.7)) / .12, 2)) });
});

/* ===================== 12. CRYPTO REGARDS ===================== */
chapter(S(150.5), 'Crypto regards');
capHide.push([S(153.85), TOTAL + 1]);
E.scene('end', S(150.3), TOTAL, (r, s) => {
  s.np = namePlate(); s.overlays = [s.np];
  s.cr = box(r, 540, 400, 1040, 160, 'gt', 'Crypto Regards,', 'font:400 128px/1.1 "Great Vibes",cursive;filter:drop-shadow(0 0 24px rgba(242,173,60,.35))');
  s.mtg = box(r, 540, 580, 1000, 200, '', '<span class="disp gt" style="font-size:190px;line-height:1">MTG</span><span style="font-size:130px;margin-left:10px">👑</span>');
  s.arch = box(r, 540, 712, 1000, 40, 'mono', 'Your Digital Architect', 'font-size:28px;color:#ffd98e;letter-spacing:.4em');
  s.seat = box(r, 540, 780, 1000, 34, 'mono', 'Your seat is waiting', 'font-size:22px;color:#f7e6bf;letter-spacing:.42em');
  s.btn = box(r, 540, 890, 920, 124, '', `<div class="cx" style="gap:22px;width:920px;height:124px;border-radius:62px;background:linear-gradient(180deg,#34e07a,#14a34f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.25),0 20px 60px rgba(20,163,79,.4)">${ic('whatsapp', '', 'style="width:62px;height:62px;color:#fff"')}<b style="font:800 56px/1 var(--f-b);color:#fff">mtgtribe.com/group</b></div>`);
  s.c1 = box(r, 540, 1030, 1000, 76, '', `<span class="chip" style="font-size:32px;padding:16px 28px">${ic('tiktok', '', 'style="color:#fff"')}@joinmtgtribe on TikTok</span>`);
  s.c2 = box(r, 540, 1124, 1000, 76, '', `<span class="chip" style="font-size:32px;padding:16px 28px">${ic('whatsapp', '', 'style="color:#25d366"')}WhatsApp MTG: 072 171 4626</span>`);
  s.slog = box(r, 540, 1290, 1060, 110, '', '', 'font:400 88px/1 var(--f-d);letter-spacing:.01em');
  s.slog.innerHTML = '<span>' + ["Let's", 'Get', 'This', 'Crypto!', '💪'].map((w, i) => `<span class="${i < 4 ? 'gt' : ''}" style="display:inline-block;margin:0 .12em">${w}</span>`).join('') + '</span>';
  s.sw = Array.from(s.slog.firstChild.children); s.swt = [154.04, 154.24, 154.32, 154.52, 154.68].map(S);
}, (t, r, s) => {
  const n = ez.out(lin(t, S(150.62), S(151.05))), ng = out(t, S(153.75), .25);
  set(s.np, { o: n * ng, x: (1 - n) * -60 }); s.np.style.clipPath = `inset(0 ${((1 - n) * 100).toFixed(1)}% 0 0 round 22px)`; shine(s.np.querySelector('.gt'), t, S(150.9), 1);
  const items = [[s.cr, 153.98], [s.mtg, 154.2], [s.arch, 154.42], [s.seat, 154.62], [s.btn, 154.8], [s.c1, 155.0], [s.c2, 155.12]];
  items.forEach(([e, ts]) => { const k = ez.out(lin(t, S(ts), S(ts) + .45)); set(e, { o: k, y: (1 - k) * 22, b: (1 - k) * 6 }); });
  shine(s.mtg.firstChild, t, S(154.5), 1.2);
  const br = 1 + .025 * Math.sin((t - S(155)) * 3) * lin(t, S(155.2), S(155.6)); s.btn.style.transform += ` scale(${br.toFixed(4)})`;
  s.sw.forEach((w, i) => { const k = lin(t, s.swt[i] - .02, s.swt[i] + .16); set(w, { o: lin(t, s.swt[i] - .02, s.swt[i] + .05), s: k <= 0 ? 1.5 : 1.5 - .5 * ez.out(k) }); });
  shine(s.sw[3], t, S(155.3), 1.2);
});
})();

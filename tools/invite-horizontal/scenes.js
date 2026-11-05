/* MTG TRIBE invite, horizontal: the scenes. Times in S(...) are the source voice times from the transcript. */
(function () {
'use strict';
const { S, el, ic, set, win, pop, lin, ez, mix, clamp, shine, words, cue, shake, flash, chapter, av, CO, TOTAL } = E;
const R = { x: 1150, y: 176, w: 674, h: 564, cx: 1487 };          // right-hand stage when the avatar is on the left

/* ---------- helpers ---------- */
function box(p, cx, cy, w, h, cls, html, css) { return el(p, 'cx ' + (cls || ''), html, `left:${cx - w / 2}px;top:${cy - h / 2}px;width:${w}px;height:${h}px;` + (css || '')); }
function up(e, t, t0, d = .4, dist = 26) { const k = ez.out(lin(t, t0, t0 + d)); set(e, { o: k, y: (1 - k) * dist, b: (1 - k) * 8 }); return k; }
function slam(e, t, t0, from = 1.7, extra) { const k = lin(t, t0, t0 + .22); const s = from - (from - 1) * ez.out(k); set(e, Object.assign({ o: lin(t, t0 - .01, t0 + .07), s: k <= 0 ? from : s, b: (1 - ez.out(k)) * 6 }, extra || {})); return k; }
function pp(e, t, t0, extra) { const p = pop(t, t0); set(e, Object.assign({ o: p.o, s: p.s }, extra || {})); return p.k; }
const out = (t, t1, d = .3) => 1 - ez.inOut(lin(t, t1, t1 + d));
function svgLayer(p, css) { const d = el(p, '', '<svg width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0;overflow:visible"></svg>', 'width:1920px;height:1080px;' + (css || '')); return d.firstChild; }
const NS = 'http://www.w3.org/2000/svg';
function sv(parent, tag, attrs) { const n = document.createElementNS(NS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); parent.appendChild(n); return n; }
function defs(svg, html) { const d = sv(svg, 'defs', {}); d.innerHTML = html; return d; }
const GOLD_DEFS = `<linearGradient id="gg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe7b0"/><stop offset=".55" stop-color="#f2ad3c"/><stop offset="1" stop-color="#a8681a"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>`;
function ibox(p, cx, cy, size, name, css) { return box(p, cx, cy, size, size, 'ibox', ic(name, '', `style="width:${Math.round(size * .5)}px;height:${Math.round(size * .5)}px"`), css); }
const capHide = E.capHide;

/* ---------- background mood ---------- */
E.bgParams = function (t) {
  if (t < CO + .3) { const w = lin(t, 3.6, 5.4); return { warm: .25 + .75 * w, cool: 1 - w, grid: 0, dust: .25 + .75 * w }; }
  if (t > S(49.8) && t < S(58.0)) return { warm: 1, cool: 0, grid: 0, dust: .5 };
  if (t > S(63.0) && t < S(71.6)) return { warm: 1, cool: 0, grid: 1, dust: .8 };
  return { warm: 1, cool: 0, grid: .45, dust: 1 };
};

/* =====================================================================
   0. COLD OPEN (no voice): the pain, the turn, NOW.
   ===================================================================== */
E.scene('cold', 0, CO + .2, (r, s) => {
  s.cv = el(r, '', '<canvas width="1920" height="1080"></canvas>', 'width:1920px;height:1080px').firstChild;
  s.b1 = box(r, 960, 520, 1700, 130, '', '', 'font:700 70px/1.1 var(--f-b);color:#e9e4dc;letter-spacing:-.01em');
  s.b1w = words(s.b1, "Maybe you've been burned before.");
  s.b2 = ['LOST MONEY.', 'LOST TRUST.', 'EVEN GOT BANNED.'].map((x, i) => box(r, 960, 360 + i * 170, 1500, 160, 'disp', x, 'font-size:150px;color:#9a938a;letter-spacing:.02em'));
  s.k2 = s.b2.map((b, i) => box(r, 960, 360 + i * 170, 10, 12, '', '', 'background:linear-gradient(90deg,#ff6a3d,#ffb36b);border-radius:6px;box-shadow:0 0 24px rgba(255,90,40,.8)'));
  s.b3a = box(r, 960, 430, 1500, 100, '', 'But here you are.', 'font:700 76px/1 var(--f-b);color:#fff');
  s.b3b = box(r, 960, 590, 1700, 190, 'disp gt', 'STILL WATCHING.', 'font-size:190px');
  s.b4a = box(r, 960, 330, 1400, 70, '', 'That means you', 'font:600 54px/1 var(--f-b);color:#d9d2c6');
  s.b4b = box(r, 960, 500, 1800, 210, 'disp gt', "HAVEN'T GIVEN UP", 'font-size:210px');
  s.b4c = box(r, 960, 680, 1400, 70, '', 'on yourself.', 'font:600 54px/1 var(--f-b);color:#d9d2c6');
  s.b5 = box(r, 960, 530, 1880, 260, 'disp st', "YOU'RE NOT DONE.", 'font-size:250px');
  s.b6a = box(r, 960, 450, 1600, 110, '', "It's not over", 'font:800 100px/1 var(--f-b);color:#fff');
  s.b6b = box(r, 960, 590, 1600, 110, '', "until it's over.", 'font:800 100px/1 var(--f-b);color:#ffd98e;text-shadow:0 0 40px rgba(242,173,60,.45)');
  s.b7 = box(r, 960, 470, 1700, 90, '', '<span>The best time to start was <span class="yd" style="position:relative;display:inline-block">yesterday<i style="position:absolute;left:-4px;right:-4px;top:52%;height:6px;border-radius:3px;background:#ffb36b;transform-origin:0 50%;transform:scaleX(0)"></i></span>.</span>', 'font:600 64px/1 var(--f-b);color:#bdb5a8');
  s.yd = s.b7.querySelector('.yd'); s.ydl = s.b7.querySelector('.yd i');
  s.b8 = box(r, 960, 610, 1600, 100, '', 'The next best time?', 'font:800 84px/1 var(--f-b);color:#fff');
  s.b9 = box(r, 960, 540, 1900, 520, 'disp gt', 'NOW.', 'font-size:500px;line-height:1');
  // sound design
  cue('drone', 0, 1, { dur: 12.5 });
  [0.35, 1.45, 2.5].forEach(x => cue('heart', x, .9));
  [2.05, 2.5, 2.95].forEach((x, i) => { cue('hit', x, .55 + i * .1); shake(x, 5 + i * 2); });
  cue('scrape', 3.35, .6);
  cue('swell', 3.75, .8, { dur: 3.2 });
  [5.4, 6.35].forEach(x => cue('heart', x, .55));
  cue('hit', 7.15, 1); shake(7.15, 14); flash(7.15, .25, .18, '255,255,255');
  cue('swell', 8.35, .85, { dur: 2.6 }); [8.45, 9.45, 10.4].forEach(x => cue('heart', x, .6));
  cue('riser', 10.55, .9, { dur: 1.9 });
  cue('boom', 12.45, 1); shake(12.45, 24); flash(12.45, .7, .55);
  cue('whoosh', 13.0, .8); cue('shimmer', 13.15, .7);
}, (t, r, s) => {
  // embers in the first beats, they cool and die as the light turns warm
  const c = s.cv.getContext('2d'); c.clearRect(0, 0, 1920, 1080);
  const ea = 1 - lin(t, 3.4, 4.4);
  if (ea > 0) {
    const rnd = E.rng(5);
    for (let i = 0; i < 90; i++) {
      const sp = .08 + rnd() * .14, off = rnd(), x0 = rnd() * 1920, ph = rnd() * 6.28, sz = .8 + rnd() * 2.6;
      const k = (t * sp + off) % 1, y = 1100 - k * 900, x = x0 + Math.sin(t * 1.2 + ph) * 30 + k * 80;
      const a = ea * Math.sin(Math.PI * k) * (.5 + .5 * Math.sin(t * 9 + ph));
      c.fillStyle = `rgba(255,${Math.round(120 + 80 * (1 - k))},60,${(a * .8).toFixed(3)})`; c.beginPath(); c.arc(x, y, sz, 0, 6.283); c.fill();
    }
  }
  // B1
  s.b1w.forEach((w, i) => { const t0 = .3 + i * .13, k = ez.out(lin(t, t0, t0 + .3)), g = out(t, 1.8, .25); set(w, { o: k * g, y: (1 - k) * 18 - (1 - g) * 14, b: (1 - k) * 8 + (1 - g) * 10 }); });
  // B2: three slams, then a burning strike and they fall away
  s.b2.forEach((b, i) => {
    const t0 = 2.05 + i * .45, k = slam(b, t, t0, 1.45), f = lin(t, 3.62 + i * .04, 3.95);
    set(b, { o: lin(t, t0, t0 + .06) * (1 - f), s: k <= 0 ? 1.45 : 1.45 - .45 * ez.out(k), y: f * f * 120, r: f * (i - 1) * 6, b: f * 6 });
    const sk = ez.out(lin(t, 3.32 + i * .06, 3.5 + i * .06)), w = (b.textContent.length * 66 + 40) * sk;
    s.k2[i].style.width = w + 'px'; s.k2[i].style.left = (960 - w / 2) + 'px';
    set(s.k2[i], { o: sk > 0 ? 1 - f : 0, y: f * f * 120, r: f * (i - 1) * 6 });
  });
  // B3
  { const g = out(t, 5.15, .25); up(s.b3a, t, 3.9, .45); s.b3a.style.opacity *= g;
    const k = ez.out(lin(t, 4.42, 4.9)); set(s.b3b, { o: k * g, s: .9 + .1 * k, b: (1 - k) * 10 }); shine(s.b3b, t, 4.55, 1.2); }
  // B4
  { const g = out(t, 6.95, .22); up(s.b4a, t, 5.35); s.b4a.style.opacity *= g;
    const k = ez.out(lin(t, 5.62, 6.0)); set(s.b4b, { o: k * g, s: 1.08 - .08 * k, b: (1 - k) * 10 }); shine(s.b4b, t, 5.75, 1.1);
    up(s.b4c, t, 6.05); s.b4c.style.opacity *= g; }
  // B5
  { const g = out(t, 8.22, .25); const k = slam(s.b5, t, 7.15, 1.6); set(s.b5, { o: lin(t, 7.14, 7.2) * g, s: (k <= 0 ? 1.6 : 1.6 - .6 * ez.out(k)) * (1 + (1 - g) * .25), b: (1 - g) * 12 }); shine(s.b5, t, 7.4, .9); }
  // B6
  { const g = out(t, 9.85, .22); up(s.b6a, t, 8.45); s.b6a.style.opacity *= g; up(s.b6b, t, 8.95); s.b6b.style.opacity *= g; }
  // B7, B8
  { const g = out(t, 11.55, .2); up(s.b7, t, 10.08, .45); s.b7.style.opacity *= g;
    const k = ez.out(lin(t, 10.95, 11.25)); s.ydl.style.transform = `scaleX(${k})`; s.yd.style.opacity = 1 - .55 * k;
    const g8 = out(t, 12.35, .12); const k8 = ez.out(lin(t, 11.62, 12.0)); set(s.b8, { o: k8 * g8, s: .96 + .04 * k8 + .05 * lin(t, 11.6, 12.4), b: (1 - k8) * 8 }); }
  // B9: NOW.
  { const k = lin(t, 12.45, 12.68), f = ez.in(lin(t, 13.05, 13.5));
    set(s.b9, { o: lin(t, 12.44, 12.5) * (1 - f), s: (k <= 0 ? 2.4 : 2.4 - 1.4 * ez.out(k)) * (1 + f * 2.6), b: f * 16 }); shine(s.b9, t, 12.6, .9); }
});

/* =====================================================================
   1. WELCOME: logo, then MTG in his office
   ===================================================================== */
chapter(CO + .5, 'Welcome');
av(S(.82), 'hero', .6); av(S(3.0), 'hidden', .32);
function namePlate(r) {
  const n = el(document.getElementById('over'), 'glass', `<div style="display:flex;align-items:center;gap:22px;height:100%;padding:0 30px">
     <span class="disp gt" style="font-size:58px">MTG</span><span style="font-size:44px">👑</span>
     <i style="width:2px;height:52px;background:rgba(255,217,142,.45)"></i>
     <span style="font:700 30px/1.1 var(--f-b);color:#f7e6bf">Your Digital Architect</span></div>`, 'left:420px;top:676px;height:100px;border-radius:22px;width:640px;overflow:hidden;visibility:hidden;opacity:0');
  return n;
}
E.scene('welcome', CO - .3, S(3.4), (r, s) => {
  s.logo = box(r, 960, 470, 1200, 260, '', '<span class="disp gt" style="font-size:250px;line-height:1">MTG</span><span style="font-size:160px;margin-left:14px;filter:drop-shadow(0 0 30px rgba(242,173,60,.5))">👑</span>');
  s.sub = box(r, 960, 650, 1000, 40, 'mono', 'Your Digital Architect', 'font-size:28px;color:#ffd98e;letter-spacing:.42em');
  s.np = namePlate(r); s.overlays = [s.np];
  cue('chime', CO + .05, .8); cue('whoosh', S(.8), .45); cue('whoosh', S(3.05), .7);
}, (t, r, s) => {
  const k = ez.out(lin(t, CO - .15, CO + .45)), g = ez.inOut(lin(t, S(.7), S(1.15)));
  set(s.logo, { o: k * (1 - g), s: (1.15 - .15 * k) * (1 - .25 * g), y: -g * 120, b: (1 - k) * 14 + g * 8 }); shine(s.logo.firstChild, t, CO + .2, 1.2);
  const k2 = ez.out(lin(t, CO + .25, CO + .7)); set(s.sub, { o: k2 * (1 - g), y: (1 - k2) * 16 - g * 120 });
  const n = ez.out(lin(t, S(2.1), S(2.55))), ng = out(t, S(3.0), .25);
  set(s.np, { o: n * ng, x: (1 - n) * -60 }); s.np.style.clipPath = `inset(0 ${((1 - n) * 100).toFixed(1)}% 0 0 round 22px)`;
  shine(s.np.querySelector('.gt'), t, S(2.4), 1);
});

/* =====================================================================
   2. EVERY STEP: footprints on a golden path to a door that opens
   ===================================================================== */
av(S(6.5), 'pip', .5); av(S(19.85), 'hidden', .35);
E.scene('steps', S(3.2), S(20.25), (r, s) => {
  s.world = el(r, '', '', 'width:1920px;height:1080px;transform-origin:1630px 480px');
  const svg = svgLayer(s.world); defs(svg, GOLD_DEFS + `<radialGradient id="dl"><stop offset="0" stop-color="#fff6dc"/><stop offset=".35" stop-color="#ffd98e" stop-opacity=".85"/><stop offset="1" stop-color="#f2ad3c" stop-opacity="0"/></radialGradient>`);
  s.path = sv(svg, 'path', { d: 'M 430 770 C 700 830, 860 520, 1100 560 S 1330 690, 1470 700', fill: 'none', stroke: 'rgba(255,217,142,.16)', 'stroke-width': 3, 'stroke-dasharray': '4 12' });
  s.len = s.path.getTotalLength();
  // door
  s.glowDoor = sv(svg, 'ellipse', { cx: 1630, cy: 480, rx: 10, ry: 10, fill: 'url(#dl)' });
  s.door = el(s.world, '', `<div style="position:absolute;inset:0;border-radius:150px 150px 10px 10px;box-shadow:inset 0 0 0 4px #f2ad3c,0 0 60px rgba(242,173,60,.4);background:radial-gradient(circle at 50% 45%,#fff6dc,#ffd98e 30%,#f2ad3c 60%,#7a4a16)"></div>
    <div class="dl" style="position:absolute;left:8px;top:8px;width:142px;height:450px;border-radius:142px 0 0 4px;transform-origin:0 50%;background:linear-gradient(160deg,#2c2216,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.55)"><i style="position:absolute;right:16px;top:240px;width:10px;height:10px;border-radius:50%;background:#ffd98e;box-shadow:0 0 12px #f2ad3c"></i></div>
    <div class="dr" style="position:absolute;right:8px;top:8px;width:142px;height:450px;border-radius:0 142px 4px 0;transform-origin:100% 50%;background:linear-gradient(200deg,#2c2216,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.55)"><i style="position:absolute;left:16px;top:240px;width:10px;height:10px;border-radius:50%;background:#ffd98e;box-shadow:0 0 12px #f2ad3c"></i></div>`,
    'left:1481px;top:246px;width:300px;height:466px;perspective:900px');
  s.dl = s.door.querySelector('.dl'); s.dr = s.door.querySelector('.dr');
  s.rays = el(s.world, '', '', 'left:1330px;top:180px;width:600px;height:600px;border-radius:50%;background:repeating-conic-gradient(from 0deg,rgba(255,217,142,.22) 0 6deg,rgba(255,217,142,0) 6deg 18deg);-webkit-mask-image:radial-gradient(circle,#000 10%,transparent 68%);mask-image:radial-gradient(circle,#000 10%,transparent 68%)');
  // footprints
  s.fp = []; const n = Math.floor(s.len / 50);
  for (let i = 1; i < n; i++) {
    const L = i * 50, p = s.path.getPointAtLength(L), q = s.path.getPointAtLength(Math.min(s.len, L + 2));
    const ang = Math.atan2(q.y - p.y, q.x - p.x), side = i % 2 ? 1 : -1, nx = -Math.sin(ang) * 13 * side, ny = Math.cos(ang) * 13 * side;
    const f = el(s.world, '', ic('footprints', '', 'style="width:36px;height:36px"'), `left:${p.x + nx - 18}px;top:${p.y + ny - 18}px;width:36px;height:36px;color:#ffd98e`);
    f.style.transform = `rotate(${ang * 57.3 + 90}deg)`; s.fp.push({ el: f, L, ang });
  }
  // milestones
  const ms = [['circle-play', 'Tutorials', .14, 7.08], ['lightbulb', 'Explainers', .38, 7.94], ['globe', 'Websites', .62, 9.6], ['tiktok', 'TikTok lives', .86, 11.44]];
  s.ms = ms.map(([icn, lb, f, ts]) => {
    const p = s.path.getPointAtLength(s.len * f);
    const dot = el(s.world, '', '', `left:${p.x - 11}px;top:${p.y - 11}px;width:22px;height:22px;border-radius:50%;background:#ffd98e;box-shadow:0 0 0 6px rgba(242,173,60,.25),0 0 26px #f2ad3c`);
    const card = el(s.world, 'glass', `<div class="cx" style="flex-direction:column;gap:14px;height:100%">${ic(icn, '', 'style="width:64px;height:64px;color:#ffd98e"')}<b style="font:800 32px/1 var(--f-b)">${lb}</b></div>`, `left:${p.x - 130}px;top:${p.y - 268}px;width:260px;height:184px;transform-origin:50% 100%`);
    const stem = el(s.world, '', '', `left:${p.x - 1}px;top:${p.y - 84}px;width:2px;height:72px;background:linear-gradient(#f2ad3c,rgba(242,173,60,0))`);
    cue('pop', S(ts), .6);
    return { dot, card, stem, L: s.len * f, t: S(ts) };
  });
  s.lab = box(r, 960, 205, 1400, 110, 'disp gt', 'Every step counts', 'font-size:104px');
  s.lab0 = box(r, 900, 205, 1300, 100, 'disp st', "You've already started.", 'font-size:96px');
  // invitation
  s.inv = el(r, 'glass', `<div style="position:absolute;inset:18px;border-radius:18px;box-shadow:inset 0 0 0 1px rgba(255,217,142,.35)"></div>
    <div class="cx" style="flex-direction:column;height:100%;gap:18px">
      <span class="mono" style="font-size:24px;color:#ffd98e;letter-spacing:.5em">You're invited</span>
      <span class="disp gt inv-t" style="font-size:150px">MTG TRIBE</span>
      <span style="font:600 30px/1 var(--f-b);color:#d9d2c6">A community of action takers</span></div>
    <div class="cx" style="position:absolute;right:-34px;bottom:-34px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd98e,#c17a1e 60%,#7a4a16);box-shadow:0 10px 30px rgba(0,0,0,.6),inset 0 0 0 4px rgba(255,236,200,.35);font-size:56px">👑</div>`,
    'left:560px;top:250px;width:800px;height:440px');
  s.invT = s.inv.querySelector('.inv-t');
  cue('whoosh', S(16.0), .5); cue('door', S(16.98), .9); cue('shimmer', S(17.3), .6); cue('whoosh', S(17.9), .7); cue('chime', S(18.6), .7); flash(S(20.05), .45, .55); cue('whoosh', S(19.95), .6);
}, (t, r, s) => {
  const vin = ez.out(lin(t, S(3.2), S(3.385) + .35)), vout = out(t, S(19.95), .3);
  // how far the steps have walked
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
  s.ms.forEach(m => { const k = pp(m.card, t, m.t); set(m.dot, { o: lin(t, m.t - .2, m.t) * vin, s: .6 + .4 * ez.back(lin(t, m.t - .2, m.t + .2)) }); m.card.style.opacity *= vin; m.stem.style.opacity = (k * vin).toFixed(3); });
  { const k = ez.out(lin(t, S(6.6), S(7.1))), g = out(t, S(13.05), .3); set(s.lab0, { o: k * g, y: (1 - k) * 20 }); shine(s.lab0, t, S(7.0), 1.2); }
  { const k = ez.out(lin(t, S(13.4), S(13.9))), g = out(t, S(15.9), .3); set(s.lab, { o: k * g, y: (1 - k) * 20, s: .94 + .06 * k }); shine(s.lab, t, S(13.7), 1.3); }
  // camera push to the door, door opens, light pours out
  const push = ez.inOut(lin(t, S(15.9), S(17.6)));
  s.world.style.transform = `scale(${(1 + .45 * push).toFixed(4)})`; s.world.style.opacity = (vin * vout * (1 - .7 * ez.out(lin(t, S(17.9), S(18.5))))).toFixed(3);
  const op = ez.inOut(lin(t, S(16.9), S(17.9)));
  s.dl.style.transform = `rotateY(${(-82 * op).toFixed(2)}deg)`; s.dr.style.transform = `rotateY(${(82 * op).toFixed(2)}deg)`;
  const lg = .25 + op * 1.2;
  s.glowDoor.setAttribute('rx', 140 + 520 * op); s.glowDoor.setAttribute('ry', 220 + 420 * op); s.glowDoor.setAttribute('opacity', (lg * .6).toFixed(3));
  set(s.rays, { o: op * .9, s: .6 + .9 * op, r: t * 8 });
  set(s.door, { o: lin(t, S(3.4), S(4.2)) });
  // the invitation flies out of the door
  const fly = ez.out(lin(t, S(17.85), S(18.65)));
  set(s.inv, { o: lin(t, S(17.85), S(18.0)) * vout, x: (1 - fly) * 520, y: (1 - fly) * 40, s: .15 + .85 * fly, ry: (1 - fly) * -40, p: 1400 });
  shine(s.invT, t, S(18.9), 1.0);
});

/* =====================================================================
   3. WHAT IT IS: WhatsApp community, learn, take action, grow
   ===================================================================== */
chapter(S(21.6), 'What it is');
av(S(21.6), 'split', .6); av(S(35.55), 'hidden', .4);
E.scene('what', S(21.565), S(36.0), (r, s) => {
  s.q1 = box(r, R.cx, 214, 640, 30, 'mono', 'So what is the', 'font-size:20px;color:#ffd98e;letter-spacing:.4em');
  s.q2 = box(r, R.cx, 282, 674, 100, 'disp gt', 'MTG TRIBE?', 'font-size:104px');
  const chips = [['book-open', 'Learn', 25.78], ['zap', 'Take action', 26.44], ['sprout', 'Grow', 27.4]];
  s.row = el(r, '', '', `left:${R.x}px;top:356px;width:${R.w}px;height:60px;display:flex;justify-content:center;gap:12px;align-items:center`);
  s.chips = chips.map(([icn, lb, ts], i) => {
    const c = document.createElement('div'); c.className = 'chip'; c.style.fontSize = '24px'; c.style.padding = '12px 20px'; c.innerHTML = ic(icn) + lb;
    s.row.appendChild(c);
    if (i < 2) { const a = document.createElement('div'); a.innerHTML = ic('send', '', 'style="width:22px;height:22px;color:#f2ad3c"'); a.style.display = 'flex'; a.className = 'arw'; s.row.appendChild(a); }
    cue('pop', S(ts), .5); return { c, t: S(ts) };
  });
  s.arws = Array.from(s.row.querySelectorAll('.arw'));
  s.chat = el(r, '', `<div style="height:76px;display:flex;align-items:center;gap:16px;padding:0 22px;background:linear-gradient(90deg,#0f5e3a,#128c4e);border-radius:24px 24px 0 0">
      <span class="cx" style="width:50px;height:50px;border-radius:50%;background:#1b140c;box-shadow:inset 0 0 0 2px #f2ad3c;font-size:26px">👑</span>
      <span style="display:flex;flex-direction:column;gap:5px"><b style="font:800 26px/1 var(--f-b);color:#fff">MTG TRIBE</b><small style="font:600 17px/1 var(--f-b);color:#c9f5d9">WhatsApp community</small></span>
      <span style="margin-left:auto;color:#fff">${ic('whatsapp', '', 'style="width:36px;height:36px"')}</span></div>
    <div class="msgs" style="position:absolute;left:0;right:0;top:76px;bottom:0;padding:18px 22px;display:flex;flex-direction:column;gap:12px;background:linear-gradient(180deg,#14100b,#0c0a07);border-radius:0 0 24px 24px"></div>`,
    `left:${R.x + 20}px;top:440px;width:${R.w - 40}px;height:330px;border-radius:24px;box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.35),0 30px 70px rgba(0,0,0,.6)`);
  const msgs = s.chat.querySelector('.msgs');
  s.msgs = [['circle-play', 'New tutorial: step by step', 30.06], ['lightbulb', 'New explainer', 30.94], ['zap', 'Tip of the day', 31.82], ['target', 'Strategy session', 32.2]].map(([icn, lb, ts]) => {
    const m = document.createElement('div');
    m.style.cssText = 'align-self:flex-start;display:flex;align-items:center;gap:12px;padding:10px 18px;border-radius:4px 18px 18px 18px;background:#2a2116;box-shadow:inset 0 0 0 1px rgba(255,217,142,.25);font:700 23px/1 var(--f-b);transform-origin:0 50%';
    m.innerHTML = ic(icn, '', 'style="width:26px;height:26px;color:#ffd98e"') + lb; msgs.appendChild(m); cue('pop', S(ts), .45); return { m, t: S(ts) };
  });
  // a fan of different opportunities
  s.fan = ['coins', 'rocket', 'globe', 'chart-line', 'briefcase'].map((icn, i) => el(r, 'glass', `<div class="cx" style="height:100%">${ic(icn, '', 'style="width:70px;height:70px;color:#ffd98e"')}</div>`,
    `left:${R.cx - 85}px;top:420px;width:170px;height:230px;transform-origin:50% 140%`));
  s.stamp = box(r, R.cx, 690, 674, 110, 'disp gt', 'Not just one.', 'font-size:96px');
  cue('whoosh', S(23.7), .4); cue('whoosh', S(32.9), .5); cue('hit', S(34.94), .7); shake(S(34.94), 7); cue('whoosh', S(35.7), .55);
}, (t, r, s) => {
  const g = out(t, S(35.65), .32);
  up(s.q1, t, S(21.62)); s.q1.style.opacity *= g;
  const k = ez.out(lin(t, S(22.2), S(22.6))); set(s.q2, { o: k * g, s: 1.15 - .15 * k, b: (1 - k) * 8 }); shine(s.q2, t, S(22.6), 1.1);
  s.chips.forEach((c, i) => { const p = pop(t, c.t); set(c.c, { o: p.o * g, s: p.s }); const tog = Math.exp(-Math.pow((t - S(27.9) - i * .1) / .18, 2)); c.c.style.boxShadow = `inset 0 0 0 1.5px rgba(255,217,142,${(.4 + .6 * tog).toFixed(2)}),0 0 ${(40 * tog).toFixed(0)}px rgba(242,173,60,${(.8 * tog).toFixed(2)}),0 18px 40px rgba(0,0,0,.5)`; });
  s.arws.forEach((a, i) => { a.style.opacity = (lin(t, s.chips[i + 1].t - .1, s.chips[i + 1].t + .15) * g).toFixed(3); });
  const cin = ez.out(lin(t, S(23.8), S(24.35))), cout = ez.inOut(lin(t, S(32.75), S(33.25)));
  set(s.chat, { o: cin * (1 - cout) * g, y: (1 - cin) * 60 + cout * 80, s: .96 + .04 * cin, b: cout * 8 });
  s.msgs.forEach(m => { const p = pop(t, m.t, .45); set(m.m, { o: p.o, s: p.s }); });
  const fo = ez.out(lin(t, S(33.0), S(34.2)));
  s.fan.forEach((f, i) => { const a = (i - 2) * 15 * fo; set(f, { o: lin(t, S(32.95), S(33.2)) * g, r: a, y: (1 - fo) * 40 - 30, s: .9 + .1 * fo }); f.style.boxShadow = `inset 0 0 0 1.5px rgba(255,217,142,.4),0 0 ${(30 * fo).toFixed(0)}px rgba(242,173,60,.25),0 20px 50px rgba(0,0,0,.6)`; });
  const sk = slam(s.stamp, t, S(34.94), 1.7, { r: -4 }); s.stamp.style.opacity *= g; shine(s.stamp, t, S(35.1), .8);
});

/* =====================================================================
   4. UPFRONT: not one program, many streams, never stop learning
   ===================================================================== */
chapter(S(36.5), 'Let me be upfront');
av(S(36.6), 'pip', .5);
E.scene('upfront', S(36.37), S(49.75), (r, s) => {
  s.head = el(r, '', `<div style="display:flex;align-items:center;gap:30px">${'<span class="ibox" style="width:130px;height:130px;display:grid">' + ic('shield-check', '', 'style="width:68px;height:68px"') + '</span>'}<span class="disp st up-t" style="font-size:130px">Let me be upfront</span></div>`,
    'left:0;top:395px;width:1920px;height:150px;display:flex;justify-content:center;align-items:center;transform-origin:960px 75px');
  s.headT = s.head.querySelector('.up-t');
  s.one = box(r, 960, 470, 800, 220, 'glass', `<div style="display:flex;align-items:center;gap:26px">${ic('ticket', '', 'style="width:80px;height:80px;color:#ffd98e"')}<span class="disp" style="font-size:96px;color:#efe9df">One program</span></div>`);
  s.x = box(r, 960, 470, 300, 300, '', `<svg width="300" height="300" viewBox="0 0 300 300"><path d="M40 40 L260 260 M260 40 L40 260" stroke="#ff7a4d" stroke-width="22" stroke-linecap="round" style="filter:drop-shadow(0 0 18px rgba(255,90,40,.8))"/></svg>`);
  s.shards = []; { const rnd = E.rng(3); for (let i = 0; i < 16; i++) s.shards.push({ e: el(r, '', '', `left:${940 + rnd() * 40}px;top:${450 + rnd() * 40}px;width:${10 + rnd() * 26}px;height:${8 + rnd() * 18}px;background:linear-gradient(135deg,#ffd98e,#a8681a);border-radius:3px`), vx: (rnd() - .5) * 1600, vy: (rnd() - .7) * 1000, vr: (rnd() - .5) * 900 }); }
  const tiles = [['rocket', 'Projects', 40.52], ['wrench', 'Tools', 41.32], ['target', 'Strategies', 41.86], ['coins', 'Coins & tokens', 43.72]];
  s.tiles = tiles.map(([icn, lb, ts], i) => {
    const cx = 960 + (i - 1.5) * 390;
    const e = el(r, 'glass', `<div class="cx" style="flex-direction:column;gap:18px;height:100%"><span class="ibox" style="width:96px;height:96px;display:grid">${ic(icn, '', 'style="width:50px;height:50px"')}</span><span class="disp" style="font-size:52px;color:#f5efe6">${lb}</span></div>`, `left:${cx - 170}px;top:300px;width:340px;height:240px`);
    cue('pop', S(ts), .6); return { e, cx, t: S(ts) };
  });
  const svg = svgLayer(r); defs(svg, GOLD_DEFS + '<linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd98e" stop-opacity=".2"/><stop offset="1" stop-color="#ffd98e"/></linearGradient>');
  s.streams = s.tiles.map(ti => sv(svg, 'path', { d: `M ${ti.cx} 545 C ${ti.cx} 640, 960 600, 960 690`, fill: 'none', stroke: 'url(#gg)', 'stroke-width': 7, 'stroke-linecap': 'round', filter: 'url(#glow)' }));
  s.flow = s.tiles.map(ti => sv(svg, 'path', { d: `M ${ti.cx} 545 C ${ti.cx} 640, 960 600, 960 690`, fill: 'none', stroke: '#fff6dc', 'stroke-width': 3, 'stroke-dasharray': '6 26', 'stroke-linecap': 'round' }));
  s.pool = sv(svg, 'ellipse', { cx: 960, cy: 700, rx: 230, ry: 34, fill: 'rgba(242,173,60,.35)', filter: 'url(#glow2)' });
  s.lab1 = box(r, 960, 776, 1400, 74, 'disp gt', 'Multiple streams of income', 'font-size:70px');
  s.lab2 = box(r, 960, 776, 1400, 74, '', `<span style="display:flex;align-items:center;gap:22px">${ic('infinity', '', 'style="width:84px;height:84px;color:#ffd98e"')}<span class="disp gt" style="font-size:70px">Never stop learning</span></span>`);
  cue('whoosh', S(36.5), .5); cue('hit', S(38.76), .7); shake(S(38.76), 8); cue('shatter', S(39.25), .8); cue('flow', S(46.3), .6, { dur: 3.2 }); cue('chime', S(48.3), .5); cue('whoosh', S(49.6), .5);
}, (t, r, s) => {
  const g = out(t, S(49.55), .35);
  const hk = ez.out(lin(t, S(36.45), S(36.9))), hm = ez.inOut(lin(t, S(37.55), S(38.05)));
  set(s.head, { o: hk * g, s: (1.1 - .1 * hk) * (1 - .5 * hm), y: -hm * 260, b: (1 - hk) * 10 }); shine(s.headT, t, S(36.8), 1.1);
  const ok = pp(s.one, t, S(38.05)); const shat = lin(t, S(39.22), S(39.4));
  s.one.style.opacity = (lin(t, S(38.05), S(38.2)) * (1 - shat)).toFixed(3);
  const xk = slam(s.x, t, S(38.72), 1.8); s.x.style.opacity = (lin(t, S(38.7), S(38.78)) * (1 - shat)).toFixed(3);
  s.shards.forEach(h => { const d = t - S(39.22); if (d < 0 || d > 1.2) { h.e.style.opacity = 0; return; } set(h.e, { o: 1 - d / 1.2, x: h.vx * d, y: h.vy * d + 900 * d * d, r: h.vr * d }); });
  s.tiles.forEach(ti => { const k = ez.back(lin(t, ti.t - .1, ti.t + .45)), o = lin(t, ti.t - .1, ti.t + .05); set(ti.e, { o: o * g, x: (1 - k) * (960 - ti.cx), y: (1 - k) * 170, s: .5 + .5 * clamp(k, 0, 1.2) }); });
  const sd = ez.inOut(lin(t, S(46.3), S(47.3)));
  s.streams.forEach((p, i) => { const L = p.getTotalLength() + 2; p.setAttribute('stroke-dasharray', L); p.setAttribute('stroke-dashoffset', (L * (1 - sd)).toFixed(1)); p.setAttribute('opacity', g.toFixed(3)); });
  s.flow.forEach(p => { p.setAttribute('stroke-dashoffset', (-t * 120).toFixed(1)); p.setAttribute('opacity', (lin(t, S(46.9), S(47.3)) * g).toFixed(3)); });
  s.pool.setAttribute('opacity', (ez.out(lin(t, S(46.9), S(47.6))) * g).toFixed(3)); s.pool.setAttribute('rx', 160 + 90 * lin(t, S(46.9), S(48.5)));
  const l1 = ez.out(lin(t, S(46.6), S(47.0))), l1o = out(t, S(48.1), .25); set(s.lab1, { o: l1 * l1o * g, y: (1 - l1) * 18 }); shine(s.lab1, t, S(47.0), 1);
  const l2 = ez.out(lin(t, S(48.25), S(48.65))); set(s.lab2, { o: l2 * g, y: (1 - l2) * 18 });
  const inf = s.lab2.querySelector('svg'); inf.style.strokeDasharray = 60; inf.style.strokeDashoffset = (60 * (1 - ez.inOut(lin(t, S(48.25), S(49.1))))).toFixed(1);
  shine(s.lab2.querySelector('.gt'), t, S(48.6), 1);
});

/* =====================================================================
   5. THE FARMER: one storm, still a full table, then where the analogy stops
   ===================================================================== */
chapter(S(50.0), 'Spread the risk');
E.scene('farm', S(49.75), S(63.0), (r, s) => {
  s.wrap = el(r, '', '<canvas width="1920" height="1080"></canvas>', 'width:1920px;height:1080px;transform-origin:960px 560px');
  s.cv = s.wrap.firstChild;
  s.lab = box(r, 960, 170, 1700, 90, 'disp gt', 'One bad season. Still a full table.', 'font-size:84px');
  s.pause = box(r, 960, 470, 220, 220, '', `<svg width="220" height="220" viewBox="0 0 220 220"><circle cx="110" cy="110" r="100" fill="rgba(0,0,0,.45)" stroke="#ffd98e" stroke-width="5"/><rect x="78" y="62" width="22" height="96" rx="6" fill="#ffd98e"/><rect x="120" y="62" width="22" height="96" rx="6" fill="#ffd98e"/></svg>`);
  s.stop = box(r, 960, 650, 760, 76, 'glass', '<span class="mono" style="font-size:26px;color:#ffd98e">Where the analogy stops</span>', 'border-radius:18px');
  s.frame = el(r, '', '', 'left:130px;top:150px;width:1660px;height:720px;border-radius:24px;box-shadow:inset 0 0 0 3px rgba(255,217,142,.75);outline:2px dashed rgba(255,217,142,.35);outline-offset:14px');
  // risk gauge
  s.gauge = el(r, '', `<svg width="760" height="440" viewBox="0 0 760 440" style="overflow:visible">
    <defs><linearGradient id="gz" x1="0" x2="1"><stop offset="0" stop-color="#c9d66b"/><stop offset=".5" stop-color="#f2ad3c"/><stop offset="1" stop-color="#e2553a"/></linearGradient></defs>
    <path d="M 60 380 A 320 320 0 0 1 700 380" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="46" stroke-linecap="round"/>
    <path d="M 60 380 A 320 320 0 0 1 700 380" fill="none" stroke="url(#gz)" stroke-width="40" stroke-linecap="round" style="filter:drop-shadow(0 0 16px rgba(242,173,60,.4))"/>
    <text x="60" y="438" fill="#c9d66b" font-family="JetBrains Mono" font-weight="700" font-size="22" text-anchor="middle" letter-spacing="4">LOW</text>
    <text x="700" y="438" fill="#ff8a6b" font-family="JetBrains Mono" font-weight="700" font-size="22" text-anchor="middle" letter-spacing="4">HIGH</text>
    <text x="380" y="300" fill="#ffd98e" font-family="JetBrains Mono" font-weight="700" font-size="24" text-anchor="middle" letter-spacing="8">RISK</text>
    <g class="needle"><path d="M 380 380 L 372 380 L 380 100 L 388 380 Z" fill="#fff6dc" style="filter:drop-shadow(0 0 10px rgba(255,217,142,.9))"/></g>
    <circle cx="380" cy="380" r="24" fill="#1b140c" stroke="#ffd98e" stroke-width="5"/></svg>`, 'left:580px;top:250px;width:760px;height:440px');
  s.needle = s.gauge.querySelector('.needle');
  s.zero = box(r, 470, 610, 270, 64, 'chip', ic('lock') + 'Never zero', 'font-size:24px;justify-content:center');
  s.risk = box(r, 960, 790, 1500, 90, 'disp gt', 'Lower risk, not no risk.', 'font-size:88px');
  // the round table
  s.table = el(r, '', '', 'left:660px;top:385px;width:600px;height:230px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,rgba(255,217,142,.2),rgba(30,24,15,.95) 70%);box-shadow:inset 0 0 0 3px rgba(255,217,142,.6),0 0 60px rgba(242,173,60,.25),0 30px 60px rgba(0,0,0,.6)');
  const seatIcons = ['coins', 'globe', 'rocket', 'chart-line', 'wallet', 'store', 'megaphone', null];
  s.seats = seatIcons.map((icn, i) => {
    const a = -Math.PI / 2 + (i - 0) * (Math.PI * 2 / 8) + Math.PI, cx = 960 + Math.cos(a) * 420, cy = 500 + Math.sin(a) * 215;
    const empty = !icn;
    const e = box(r, cx, cy, 104, 104, '', empty ? `<div class="cx" style="width:104px;height:104px;border-radius:50%;border:3px dashed #ffd98e;color:#ffd98e">${ic('armchair', '', 'style="width:50px;height:50px"')}</div>`
      : `<div class="cx" style="width:96px;height:96px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#3a2e1f,#16110b);box-shadow:inset 0 0 0 2px rgba(255,217,142,.45);color:#ffd98e">${ic(icn, '', 'style="width:44px;height:44px"')}</div>`);
    return { e, empty, i };
  });
  s.yours = box(r, 960, 790, 300, 56, 'chip', ic('crown') + 'Your seat', 'font-size:24px;justify-content:center');
  s.seatLab = box(r, 960, 205, 1500, 90, 'disp gt', "There's a seat for you.", 'font-size:86px');
  cue('grow', S(50.85), .5, { dur: 1.4 }); cue('rain', S(52.5), .55, { dur: 1.9 }); cue('thunder', S(53.3), .9); flash(S(53.32), .3, .35, '255,255,255');
  cue('chime', S(54.3), .45); cue('stop', S(55.55), .8); cue('whoosh', S(57.9), .4); cue('swing', S(58.4), .6); cue('hit', S(59.76), .6); shake(S(59.76), 6);
  cue('whoosh', S(60.4), .4); for (let i = 0; i < 7; i++) cue('pop', S(60.76) + i * .1, .3); cue('chime', S(61.95), .6); cue('whoosh', S(62.6), .5);
}, (t, r, s) => {
  const vin = ez.out(lin(t, S(49.75), S(50.4))), g = out(t, S(62.55), .4);
  const freeze = ez.out(lin(t, S(55.5), S(55.9))), sink = ez.inOut(lin(t, S(57.9), S(58.5)));
  drawFarm(s.cv.getContext('2d'), t, freeze);
  s.wrap.style.opacity = (vin * g * (1 - .62 * sink)).toFixed(3);
  s.wrap.style.filter = `grayscale(${(freeze * .9).toFixed(2)}) brightness(${(1 - .35 * freeze).toFixed(2)})` + (sink > .01 ? ` blur(${(sink * 10).toFixed(1)}px)` : '');
  s.wrap.style.transform = `scale(${(1.02 + .03 * lin(t, S(49.8), S(55.5)) - .06 * sink).toFixed(4)})`;
  { const k = ez.out(lin(t, S(54.3), S(54.8))), o = out(t, S(55.45), .2); set(s.lab, { o: k * o, y: (1 - k) * 20 }); shine(s.lab, t, S(54.7), 1); }
  { const k = pop(t, S(55.55)), o = out(t, S(57.85), .3); set(s.pause, { o: k.o * o, s: k.s }); const k2 = ez.out(lin(t, S(56.3), S(56.7))); set(s.stop, { o: k2 * o, y: (1 - k2) * 20 }); set(s.frame, { o: freeze * o * .9, s: 1.03 - .03 * freeze }); }
  // gauge
  const gin = ez.out(lin(t, S(58.0), S(58.45))), gout = out(t, S(60.35), .35);
  set(s.gauge, { o: gin * gout, s: .9 + .1 * gin, y: (1 - gin) * 30 });
  const sw = ez.back(lin(t, S(58.4), S(59.2))), wob = Math.sin((t - S(59.6)) * 14) * Math.exp(-Math.max(0, t - S(59.6)) * 3) * (t > S(59.6) ? 4 : 0);
  const ang = mix(62, -48, sw) + wob; s.needle.setAttribute('transform', `rotate(${ang.toFixed(2)} 380 380)`);
  { const k = pop(t, S(59.52)); set(s.zero, { o: k.o * gout, s: k.s }); }
  { const k = slam(s.risk, t, S(59.76), 1.5); s.risk.style.opacity *= gout; shine(s.risk, t, S(59.9), .9); }
  // table
  const tin = ez.out(lin(t, S(60.4), S(60.9)));
  set(s.table, { o: tin * g, s: .85 + .15 * tin, ry: 0 });
  s.seats.forEach(st => {
    const t0 = st.empty ? S(61.9) : S(60.76) + st.i * .1, p = pop(t, t0);
    set(st.e, { o: p.o * g, s: p.s * (st.empty ? 1 + .06 * Math.sin((t - t0) * 6) * lin(t, t0, t0 + .5) : 1) });
    if (st.empty) st.e.firstChild.style.boxShadow = `0 0 ${(20 + 30 * (.5 + .5 * Math.sin(t * 6))).toFixed(0)}px rgba(242,173,60,${(.8 * lin(t, t0, t0 + .4)).toFixed(2)})`;
  });
  { const k = pop(t, S(62.05)); set(s.yours, { o: k.o * g, s: k.s }); }
  { const k = ez.out(lin(t, S(61.85), S(62.3))); set(s.seatLab, { o: k * g, y: (1 - k) * 20 }); shine(s.seatLab, t, S(62.2), 1); }
});
// painted farm: four plots, a storm over one, the others still feed the family
function drawFarm(c, t, freeze) {
  const W = 1920, H = 1080; c.clearRect(0, 0, W, H);
  const sky = c.createLinearGradient(0, 0, 0, 480); sky.addColorStop(0, '#120c06'); sky.addColorStop(.6, '#4a2c10'); sky.addColorStop(1, '#8a5418');
  c.fillStyle = sky; c.fillRect(0, 0, W, 500);
  const sun = c.createRadialGradient(1380, 360, 10, 1380, 360, 380); sun.addColorStop(0, 'rgba(255,236,190,.95)'); sun.addColorStop(.12, 'rgba(255,210,120,.7)'); sun.addColorStop(1, 'rgba(242,173,60,0)');
  c.fillStyle = sun; c.fillRect(0, 0, W, 700);
  const hill = (y0, amp, f, ph, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(0, H); for (let x = 0; x <= W; x += 20) c.lineTo(x, y0 + Math.sin(x * f + ph) * amp + Math.sin(x * f * 2.3 + ph) * amp * .4); c.lineTo(W, H); c.fill(); };
  hill(400, 22, .004, 1, '#3a240f'); hill(440, 16, .006, 3, '#24170b');
  // farmhouse with a warm window
  c.fillStyle = '#140d06'; c.beginPath(); c.moveTo(1560, 420); c.lineTo(1650, 360); c.lineTo(1740, 420); c.lineTo(1740, 500); c.lineTo(1560, 500); c.fill();
  const win = c.createRadialGradient(1650, 445, 2, 1650, 445, 60); win.addColorStop(0, 'rgba(255,217,142,1)'); win.addColorStop(1, 'rgba(255,217,142,0)');
  c.fillStyle = win; c.fillRect(1590, 400, 120, 90); c.fillStyle = '#ffd98e'; c.fillRect(1635, 432, 30, 26);
  // field
  const fy = 500; const field = c.createLinearGradient(0, fy, 0, H); field.addColorStop(0, '#2a1a0b'); field.addColorStop(1, '#120b05'); c.fillStyle = field; c.fillRect(0, fy, W, H - fy);
  const plots = [{ x: 540, type: 'maize' }, { x: 870, type: 'wheat' }, { x: 1200, type: 'sun' }, { x: 1530, type: 'leaf' }];
  const storm = lin(t, S(52.45), S(52.95)), wilt = ez.inOut(lin(t, S(53.35), S(54.1))), stormOut = lin(t, S(54.6), S(55.3));
  const glow = ez.out(lin(t, S(54.1), S(54.6)));
  plots.forEach((p, i) => {
    c.fillStyle = 'rgba(255,217,142,.05)'; c.fillRect(p.x - 150, fy + 20, 300, 330);
    for (let row = 0; row < 3; row++) for (let col = 0; col < 4; col++) {
      const px = p.x - 108 + col * 72 + (row % 2) * 16, py = fy + 120 + row * 100, sc = 1.05 + row * .22;
      const gT = S(50.85) + i * .28 + row * .06, grow = ez.out(lin(t, gT, gT + .7));
      if (grow <= 0) continue;
      const bad = i === 1 ? wilt : 0;
      drawPlant(c, p.type, px, py, sc * grow, bad, glow * (i !== 1 ? 1 : 0), t + i + row);
    }
  });
  // storm cloud over plot 2
  if (storm > 0 && stormOut < 1) {
    const cx = mix(300, 870, ez.out(storm)) + stormOut * -600, cy = 400, a = (1 - stormOut);
    c.globalAlpha = a;
    if (t > S(52.6)) { c.strokeStyle = 'rgba(180,200,230,.55)'; c.lineWidth = 2; c.beginPath(); const rnd = E.rng(Math.floor(t * 30)); for (let i = 0; i < 46; i++) { const x = cx - 150 + rnd() * 300, y = cy + 40 + rnd() * 400; c.moveTo(x, y); c.lineTo(x - 8, y + 30); } c.stroke(); }
    c.fillStyle = '#2b2e36'; [[-110, 10, 70], [-40, -20, 90], [50, -5, 80], [120, 15, 60], [0, 30, 90]].forEach(([dx, dy, rr]) => { c.beginPath(); c.arc(cx + dx, cy + dy, rr, 0, 6.283); c.fill(); });
    if (Math.abs(t - S(53.32)) < .12) { c.strokeStyle = '#fff6dc'; c.lineWidth = 5; c.shadowColor = '#fff'; c.shadowBlur = 30; c.beginPath(); c.moveTo(cx + 10, cy + 60); c.lineTo(cx - 20, cy + 160); c.lineTo(cx + 15, cy + 170); c.lineTo(cx - 25, cy + 300); c.stroke(); c.shadowBlur = 0; }
    c.globalAlpha = 1;
  }
  // the family at the farmhouse, fed
  const fam = ez.out(lin(t, S(54.8), S(55.3)));
  if (fam > 0) {
    c.globalAlpha = fam; c.fillStyle = '#ffd98e'; c.shadowColor = 'rgba(242,173,60,.9)'; c.shadowBlur = 20;
    [[1590, 1.3], [1640, 1.45], [1690, .95]].forEach(([x, k]) => { c.beginPath(); c.arc(x, 495 - 46 * k, 10 * k, 0, 6.283); c.fill(); c.beginPath(); c.roundRect(x - 11 * k, 507 - 46 * k, 22 * k, 40 * k, 8 * k); c.fill(); });
    c.shadowBlur = 0; c.globalAlpha = 1;
  }
}
function drawPlant(c, type, x, y, s, bad, glow, ph) {
  const sway = Math.sin(ph * 1.7 + E.lastT * 1.6) * 2;
  c.save(); c.translate(x, y); c.scale(s, s); c.rotate((bad * .5 + sway * .01));
  const green = bad > 0 ? `rgb(${Math.round(mix(96, 110, bad))},${Math.round(mix(150, 80, bad))},${Math.round(mix(70, 40, bad))})` : '#6aa04a';
  if (glow > 0) { c.shadowColor = `rgba(255,217,142,${glow})`; c.shadowBlur = 18 * glow; }
  c.strokeStyle = green; c.lineWidth = 5; c.lineCap = 'round';
  if (type === 'maize') { c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -90); c.stroke(); c.beginPath(); c.moveTo(0, -40); c.quadraticCurveTo(-30, -60, -40, -40); c.moveTo(0, -60); c.quadraticCurveTo(30, -80, 40, -60); c.stroke(); c.fillStyle = bad > 0 ? '#8a6a3a' : '#f2c14e'; c.beginPath(); c.ellipse(8, -70, 7, 18, .3, 0, 6.283); c.fill(); }
  if (type === 'wheat') { c.strokeStyle = bad > 0 ? '#7a5a30' : '#d9a441'; c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -80); c.stroke(); c.fillStyle = bad > 0 ? '#6a4a25' : '#f2c14e'; for (let k = 0; k < 5; k++) { c.beginPath(); c.ellipse(-6, -78 + k * 9, 5, 8, -.5, 0, 6.283); c.ellipse(6, -78 + k * 9, 5, 8, .5, 0, 6.283); c.fill(); } }
  if (type === 'sun') { c.beginPath(); c.moveTo(0, 0); c.lineTo(0, -85); c.stroke(); c.fillStyle = '#f2ad3c'; for (let k = 0; k < 10; k++) { c.beginPath(); c.ellipse(Math.cos(k * .628) * 16, -92 + Math.sin(k * .628) * 16, 9, 5, k * .628, 0, 6.283); c.fill(); } c.fillStyle = '#4a2a10'; c.beginPath(); c.arc(0, -92, 11, 0, 6.283); c.fill(); }
  if (type === 'leaf') { c.fillStyle = green; for (let k = 0; k < 5; k++) { c.beginPath(); c.ellipse(Math.cos(k * 1.256) * 14, -22 + Math.sin(k * 1.256) * 8, 20, 12, k * 1.256, 0, 6.283); c.fill(); } c.fillStyle = '#8cc46a'; c.beginPath(); c.arc(0, -24, 14, 0, 6.283); c.fill(); }
  c.restore();
}

/* =====================================================================
   6. SERVICES: blueprint, build, duplicate with your links, then the roads (traffic)
   ===================================================================== */
chapter(S(63.0), 'Services');
av(S(62.8), 'split', .6); av(S(71.55), 'pip', .55);
E.scene('services', S(62.75), S(76.45), (r, s) => {
  s.bp = el(r, '', '', `left:${R.x}px;top:${R.y}px;width:${R.w}px;height:${R.h + 80}px;border-radius:26px;background:repeating-linear-gradient(0deg,rgba(255,217,142,.07) 0 1px,transparent 1px 32px),repeating-linear-gradient(90deg,rgba(255,217,142,.07) 0 1px,transparent 1px 32px),linear-gradient(160deg,rgba(30,24,15,.7),rgba(10,8,6,.85));box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.3)`);
  s.title = el(r, '', `<div style="display:flex;align-items:center;gap:18px">${ic('pencil-ruler', '', 'style="width:54px;height:54px;color:#ffd98e"')}<span class="disp gt sv-t" style="font-size:76px">MTG Services</span></div><div style="margin-top:10px;font:600 22px/1 var(--f-b);color:#bdb5a8">Built by your Digital Architect</div>`, `left:${R.x + 40}px;top:204px;width:600px;height:120px`);
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
    `left:${R.x + 57}px;top:340px;width:560px;height:350px;border-radius:16px;background:#0e0b08;box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.4),0 30px 70px rgba(0,0,0,.65)`);
  s.copies = [mkWin('site-tribe.jpg', 'yoursite.com'), mkWin('site-dash.jpg', 'yoursite.com')];
  s.main = mkWin('site-altruva.jpg', 'mtgtribe.com/altruva');
  [s.main, ...s.copies].forEach(w => { w.querySelectorAll('.wire rect').forEach(rc => { const L = 2 * (+rc.getAttribute('width') + +rc.getAttribute('height')); rc.setAttribute('stroke-dasharray', L); rc.dataset.l = L; }); });
  s.links = box(r, R.cx, 726, 674, 70, 'disp gt', 'Your links. Built in.', 'font-size:64px');
  // traffic: roads to your site
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  s.center = { x: 960, y: 470 };
  s.src = [['tiktok', 560, 270], ['whatsapp', 1360, 270], ['facebook', 560, 690], ['youtube', 1360, 690]].map(([icn, x, y]) => {
    const d = `M ${x} ${y} C ${mix(x, 960, .5)} ${y}, ${mix(x, 960, .5)} 470, 960 470`;
    const road = sv(svg, 'path', { d, fill: 'none', stroke: 'rgba(255,217,142,.18)', 'stroke-width': 26, 'stroke-linecap': 'round' });
    const lane = sv(svg, 'path', { d, fill: 'none', stroke: 'rgba(255,217,142,.6)', 'stroke-width': 2.5, 'stroke-dasharray': '14 16' });
    const e = box(r, x, y, 120, 120, '', `<div class="cx" style="width:120px;height:120px;border-radius:32px;background:#120e09;box-shadow:inset 0 0 0 2px rgba(255,217,142,.5),0 0 40px rgba(242,173,60,.25);color:#fff">${ic(icn, '', 'style="width:58px;height:58px"')}</div>`);
    const dots = []; for (let k = 0; k < 7; k++) dots.push(sv(svg, 'circle', { r: 7, fill: '#ffd98e', filter: 'url(#glow)' }));
    return { road, lane, e, dots, len: road.getTotalLength() };
  });
  s.site = box(r, 960, 470, 330, 230, 'glass', `<div style="position:absolute;inset:14px;border-radius:14px;background:url(site-tribe.jpg) center top/cover"></div><div class="cx" style="position:absolute;left:50%;bottom:-30px;transform:translateX(-50%);width:64px;height:64px;border-radius:50%;background:linear-gradient(180deg,#ffd98e,#f2ad3c);color:#1b140c">${ic('store', '', 'style="width:34px;height:34px"')}</div>`);
  s.ring = box(r, 960, 470, 400, 400, '', '', 'border-radius:50%;box-shadow:0 0 0 3px rgba(255,217,142,.8),0 0 50px rgba(242,173,60,.6)');
  s.find = box(r, 960, 836, 1500, 80, 'disp gt', 'The right people find you.', 'font-size:74px');
  s.bbr = box(r, 960, 150, 900, 30, 'mono', 'Blueprint. Build. Roads.', 'font-size:20px;color:#ffd98e;letter-spacing:.42em');
  cue('whoosh', S(62.8), .5); cue('draw', S(65.9), .5, { dur: 1.2 }); cue('scan', S(67.34), .6); cue('whoosh', S(68.8), .5); [0, .12, .24].forEach(d => cue('pop', S(70.38) + d, .5)); cue('hit', S(70.82), .45);
  cue('whoosh', S(71.6), .55); cue('draw', S(72.58), .4, { dur: .8 }); [0, .1, .2, .3].forEach(d => cue('pop', S(73.6) + d, .4)); cue('flow', S(73.0), .45, { dur: 3.2 }); cue('chime', S(74.74), .5); cue('whoosh', S(76.2), .5);
}, (t, r, s) => {
  const A = out(t, S(71.45), .3), B = ez.out(lin(t, S(71.6), S(72.1))), g = out(t, S(76.15), .35);
  const bpk = ez.out(lin(t, S(62.85), S(63.4))); set(s.bp, { o: bpk * A, s: .97 + .03 * bpk });
  { const k = ez.out(lin(t, S(64.4), S(64.85))); set(s.title, { o: k * A, y: (1 - k) * 18 }); shine(s.svT, t, S(64.8), 1); }
  const wk = lin(t, S(65.85), S(65.95));
  const draw = ez.inOut(lin(t, S(65.9), S(67.1))), reveal = ez.inOut(lin(t, S(67.34), S(67.95)));
  const dup = ez.back(lin(t, S(68.8), S(69.5)));
  [s.main, ...s.copies].forEach((w, i) => {
    const isMain = i === 0, side = i === 1 ? -1 : 1;
    const ox = isMain ? 0 : side * 120 * dup, oy = isMain ? -10 * dup : 30 * dup, rr = isMain ? 0 : side * 7 * dup;
    set(w, { o: (isMain ? wk : lin(t, S(68.75), S(68.95))) * A, x: ox, y: oy, r: rr, s: isMain ? 1 - .1 * dup : .9 });
    w.querySelectorAll('.wire rect').forEach(rc => rc.setAttribute('stroke-dashoffset', (+rc.dataset.l * (1 - (isMain ? draw : 1))).toFixed(1)));
    const sh = w.querySelector('.shot'), cut = isMain ? (1 - reveal) * 100 : 0; sh.style.clipPath = `inset(0 0 ${cut.toFixed(1)}% 0)`; sh.style.opacity = isMain ? (reveal > 0 ? 1 : 0) : 1;
    w.querySelector('.wire').style.opacity = isMain ? (1 - reveal) : 0;
    const lk = w.querySelector('.lnk'), p = pop(t, S(70.38) + [.12, 0, .24][i]); set(lk, { o: p.o, s: p.s });
  });
  { const k = slam(s.links, t, S(70.82), 1.35); s.links.style.opacity *= A; shine(s.links, t, S(71.0), .8); }
  // traffic
  const rd = ez.inOut(lin(t, S(72.5), S(73.3)));
  s.src.forEach((q, i) => {
    q.road.setAttribute('stroke-dasharray', q.len); q.road.setAttribute('stroke-dashoffset', (q.len * (1 - rd)).toFixed(1)); q.road.setAttribute('opacity', (B * g).toFixed(3));
    q.lane.setAttribute('opacity', (rd * B * g).toFixed(3)); q.lane.setAttribute('stroke-dashoffset', (-t * 60).toFixed(1));
    const p = pop(t, S(73.6) + i * .1); set(q.e, { o: p.o * B * g, s: p.s });
    const fast = 1 + 1.4 * lin(t, S(74.7), S(75.2));
    q.dots.forEach((d, k) => {
      const ph = ((t - S(73.0)) * .32 * fast + k / q.dots.length) % 1;
      if (t < S(73.0)) { d.setAttribute('opacity', 0); return; }
      const pt = q.road.getPointAtLength(q.len * ph); d.setAttribute('cx', pt.x.toFixed(1)); d.setAttribute('cy', pt.y.toFixed(1));
      d.setAttribute('opacity', (Math.sin(Math.PI * ph) * B * g * lin(t, S(73.0), S(73.4))).toFixed(3));
    });
  });
  { const p = pop(t, S(71.75)); set(s.site, { o: p.o * B * g, s: p.s }); }
  { const k = lin(t, S(74.7), S(75.6)); set(s.ring, { o: (1 - k) * (k > 0 ? 1 : 0) * g, s: .6 + k * .9 }); }
  { const k = ez.out(lin(t, S(75.55), S(75.95))); set(s.find, { o: k * g, y: (1 - k) * 20 }); shine(s.find, t, S(75.9), 1); }
  { const k = ez.out(lin(t, S(72.2), S(72.6))); set(s.bbr, { o: k * g * B }); }
});

/* =====================================================================
   7. STAND ON YOUR OWN FEET: wallet steps, the strings snap
   ===================================================================== */
chapter(S(76.8), 'Stand on your own feet');
av(S(76.5), 'split', .55); av(S(85.55), 'hidden', .35);
E.scene('stand', S(76.45), S(86.0), (r, s) => {
  s.title = box(r, R.cx, 218, 760, 76, 'disp st', 'Stand on your own feet', 'font-size:62px');
  s.ground = el(r, '', '', `left:${R.x + 30}px;top:668px;width:300px;height:4px;border-radius:2px;background:linear-gradient(90deg,transparent,#f2ad3c,transparent);box-shadow:0 0 20px #f2ad3c`);
  s.fig = box(r, 1330, 480, 300, 380, '', `<svg width="300" height="380" viewBox="0 0 300 380" fill="none" stroke="#ffd98e" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 16px rgba(242,173,60,.6))">
     <circle cx="150" cy="70" r="46"/><path d="M150 120 L150 250"/><path d="M150 150 L80 210"/><path d="M150 150 L220 210"/><path d="M150 250 L100 360"/><path d="M150 250 L200 360"/></svg>`, 'transform-origin:50% 100%');
  const rows = [['wallet', 'Create your wallet', 79.58], ['lock', 'Secure it yourself', 80.04], ['users', 'Join by yourself', 81.88], ['send', 'Transact by yourself', 82.34]];
  s.rows = rows.map(([icn, lb, ts], i) => {
    const e = el(r, '', `<div style="display:flex;align-items:center;gap:14px;height:100%"><span class="ck cx" style="width:44px;height:44px;border-radius:12px;box-shadow:inset 0 0 0 2px rgba(255,217,142,.6);color:#1b140c;flex:none">${ic('check', '', 'style="width:28px;height:28px;stroke-width:3.4"')}</span>${ic(icn, '', 'style="width:30px;height:30px;color:#ffd98e"')}<b style="font:800 27px/1 var(--f-b);white-space:nowrap">${lb}</b></div>`, `left:1480px;top:${320 + i * 92}px;width:340px;height:64px`);
    cue('tick', S(ts), .7); return { e, t: S(ts), ck: e.querySelector('.ck') };
  });
  const svg = svgLayer(r);
  s.strings = [[1250, 300, 1259, 431], [1330, 280, 1330, 375], [1410, 300, 1401, 431]].map(([x1, y1, x2, y2]) => ({ top: sv(svg, 'line', { x1, y1, x2: x1, y2: y1, stroke: '#e9e4dc', 'stroke-width': 2.5 }), bot: sv(svg, 'line', { x1: x2, y1: y2, x2, y2, stroke: '#e9e4dc', 'stroke-width': 2.5 }), x1, y1, x2, y2 }));
  s.bar = box(r, 1330, 286, 360, 60, '', `<div style="position:absolute;left:0;right:0;top:20px;height:20px;border-radius:10px;background:linear-gradient(180deg,#6b6157,#3a332b);box-shadow:0 8px 20px rgba(0,0,0,.6)"></div><div style="position:absolute;left:170px;top:-40px;width:20px;height:110px;border-radius:10px;background:linear-gradient(90deg,#6b6157,#3a332b)"></div><span class="mono" style="position:absolute;left:0;right:0;top:-74px;font-size:17px;color:#bdb5a8">So-called leader</span>`);
  s.sc = box(r, 1100, 360, 80, 80, '', ic('scissors', '', 'style="width:70px;height:70px;color:#fff6dc;filter:drop-shadow(0 0 12px #f2ad3c)"'));
  s.free = box(r, R.cx, 724, 700, 80, 'disp gt', 'No strings attached.', 'font-size:72px');
  cue('whoosh', S(76.5), .5); cue('rise', S(77.9), .5); cue('whoosh', S(83.4), .4); cue('snip', S(85.0), .8); [0, .06, .12].forEach(d => cue('snap', S(85.06) + d, .7)); cue('hit', S(85.2), .5);
}, (t, r, s) => {
  const g = out(t, S(85.6), .3);
  { const k = ez.out(lin(t, S(77.85), S(78.3))); set(s.title, { o: k * g * out(t, S(83.2), .3), y: (1 - k) * 18 }); shine(s.title, t, S(78.2), 1); }
  const rise = ez.back(lin(t, S(77.9), S(78.6))), fin = ez.out(lin(t, S(76.85), S(77.3)));
  set(s.fig, { o: fin * g, sy: .62 + .38 * clamp(rise, 0, 1.1), sx: 1, x: -10 * (1 - fin) });
  set(s.ground, { o: fin * g * (.4 + .6 * rise) });
  const ckOut = out(t, S(83.25), .35);
  s.rows.forEach(rw => { const k = ez.out(lin(t, rw.t - .25, rw.t + .1)); set(rw.e, { o: k * ckOut * g, x: (1 - k) * 30 }); const c = lin(t, rw.t, rw.t + .15); rw.ck.style.background = c > 0 ? `rgba(242,173,60,${c})` : 'transparent'; rw.ck.firstChild.style.opacity = c; });
  // the strings: down they come, then snip
  const down = ez.out(lin(t, S(83.4), S(84.1))), cut = lin(t, S(85.06), S(85.5)), barFly = ez.in(lin(t, S(85.1), S(85.6)));
  set(s.bar, { o: down * g, y: (1 - down) * -220 - barFly * 400, r: barFly * -12 });
  s.strings.forEach((q, i) => {
    const ci = clamp((t - S(85.06) - i * .06) / .3), mid = mix(q.y1, q.y2, .45);
    const yTop = q.y1 + (1 - down) * -220 - barFly * 400;
    q.top.setAttribute('y1', yTop); q.top.setAttribute('x2', mix(q.x1, q.x2, .45)); q.top.setAttribute('y2', ci > 0 ? mix(mid, yTop, ci) : mix(yTop, q.y2, 1) );
    q.top.setAttribute('opacity', (down * g * (1 - ci * .6)).toFixed(3));
    q.bot.setAttribute('x1', mix(q.x1, q.x2, .45)); q.bot.setAttribute('y1', ci > 0 ? mix(mid, q.y2, ci) + ci * ci * 60 : mid);
    q.bot.setAttribute('opacity', (down * g * (1 - ci)).toFixed(3));
    if (ci <= 0) { q.top.setAttribute('x2', q.x2); q.top.setAttribute('y2', q.y2); q.bot.setAttribute('opacity', 0); }
  });
  { const k = lin(t, S(84.75), S(85.15)); set(s.sc, { o: (k > 0 && k < 1 ? 1 : 0) * g, x: k * 460, r: Math.sin(t * 40) * 14 }); }
  { const k = slam(s.free, t, S(85.15), 1.5); s.free.style.opacity *= g; shine(s.free, t, S(85.3), .7); }
});

/* your wallet, your keys, your decisions */
E.scene('keys', S(85.75), S(88.405), (r, s) => {
  s.rows = [['wallet', 'Wallet', 85.86], ['key-round', 'Keys', 86.70], ['compass', 'Decisions', 87.46]].map(([icn, w, ts], i) => {
    const e = el(r, '', `<div style="display:flex;align-items:center;gap:40px;height:100%"><span class="ibox" style="width:150px;height:150px;display:grid;flex:none">${ic(icn, '', 'style="width:80px;height:80px"')}</span><span class="disp st" style="font-size:150px">Your</span><span class="disp gt kw" style="font-size:150px">${w}</span></div>`, `left:420px;top:${150 + i * 220}px;width:1300px;height:170px;transform-origin:30% 50%`);
    cue('hit', S(ts), .85); shake(S(ts), 9); return { e, t: S(ts), kw: e.querySelector('.kw') };
  });
  flash(S(88.36), .3, .4); cue('whoosh', S(88.2), .6);
}, (t, r, s) => {
  const gk = lin(t, S(88.1), S(88.405));
  s.rows.forEach(rw => { const k = lin(t, rw.t, rw.t + .2); set(rw.e, { o: lin(t, rw.t - .01, rw.t + .06) * (1 - gk), s: (k <= 0 ? 1.5 : 1.5 - .5 * ez.out(k)) * (1 + gk * .2), b: (1 - ez.out(k)) * 6 + gk * 8 }); shine(rw.kw, t, rw.t + .15, .7); });
});

/* =====================================================================
   8. YOUR OWN TRIBE: the challenge, lead with value, candles become a crown
   ===================================================================== */
chapter(S(89.0), 'Your own tribe');
av(S(88.85), 'split', .5); av(S(91.5), 'pip', .5);
E.scene('tribe', S(88.79), S(103.05), (r, s) => {
  s.ch1 = el(r, '', `<div style="display:flex;align-items:center;gap:24px;justify-content:center">${ic('flag', '', 'style="width:84px;height:84px;color:#ffd98e"')}<span class="disp gt ch-t" style="font-size:78px">MTG's challenge</span></div>`, `left:${R.x}px;top:290px;width:${R.w}px;height:100px`);
  s.chT = s.ch1.querySelector('.ch-t');
  s.ch2 = box(r, R.cx, 470, 700, 90, 'disp st', 'Start your own tribe.', 'font-size:66px');
  // shouting is not leading
  s.mega = box(r, 640, 480, 260, 260, '', ic('megaphone', '', 'style="width:220px;height:220px;color:#bdb5a8"'));
  s.shouts = ['JOIN!', 'JOIN NOW!', 'JOIN!!'].map((x, i) => box(r, 900, 380 + i * 100, 300, 70, 'disp', x, 'font-size:60px;color:#bdb5a8'));
  s.crowd = [0, 1, 2, 3].map(i => box(r, 1250 + (i % 2) * 140, 400 + Math.floor(i / 2) * 150, 110, 110, '', ic('user', '', 'style="width:90px;height:90px;color:#8d877e"')));
  s.megaX = box(r, 640, 480, 320, 320, '', `<svg width="320" height="320" viewBox="0 0 320 320"><path d="M50 50 L270 270 M270 50 L50 270" stroke="#f2ad3c" stroke-width="20" stroke-linecap="round" style="filter:drop-shadow(0 0 14px rgba(242,173,60,.8))"/></svg>`);
  s.shoutLab = box(r, 960, 210, 1500, 90, 'disp st', "Shouting isn't leading.", 'font-size:86px');
  // candle network
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  const C = { x: 960, y: 445 };
  const L1 = [-150, -30, 90].map(a => ({ x: C.x + Math.cos(a * Math.PI / 180) * 280, y: C.y + Math.sin(a * Math.PI / 180) * 190 }));
  const L2a = [-170, -125, -55, -10, 40, 140, 115];
  const L2 = L2a.map(a => ({ x: C.x + Math.cos(a * Math.PI / 180) * 560, y: C.y + Math.sin(a * Math.PI / 180) * 285 }));
  const par = [0, 0, 1, 1, 2, 0, 2];
  // crown points: 11 nodes, YOU on the middle peak
  const crown = [[0, -250], [-320, -160], [-150, 0], [150, 0], [320, -160], [-320, 20], [320, 20], [-320, 190], [-107, 190], [107, 190], [320, 190]].map(([x, y]) => ({ x: C.x + x, y: C.y + y }));
  s.nodes = [{ p: C, lit: S(94.22), par: null, lab: 'You', ci: 0 }]
    .concat(L1.map((p, i) => ({ p, lit: S([95.16, 95.84, 96.54][i]) + .3, par: 0, lab: ['Teach', 'Train', 'Coach'][i], ci: [1, 4, 9][i] })))
    .concat(L2.map((p, i) => ({ p, lit: S(97.1) + i * .18, par: 1 + par[i], lab: null, ci: [5, 2, 3, 6, 10, 7, 8][i] })));
  s.nodes.forEach(n => { n.c = crown[n.ci]; }); s.byCrown = []; s.nodes.forEach((n, i) => { s.byCrown[n.ci] = i; });
  s.lines = s.nodes.map((n, i) => n.par == null ? null : sv(svg, 'line', { stroke: 'url(#gg)', 'stroke-width': 4, 'stroke-linecap': 'round', filter: 'url(#glow)' }));
  s.crownPath = sv(svg, 'path', { fill: 'none', stroke: '#ffd98e', 'stroke-width': 5, 'stroke-linejoin': 'round', filter: 'url(#glow2)' });
  s.crownOrder = [7, 5, 1, 2, 0, 3, 4, 6, 10, 9, 8, 7];
  s.nodeEls = s.nodes.map((n, i) => {
    const big = i === 0, sz = big ? 120 : 84;
    const e = box(r, 0, 0, sz, sz, '', `<div class="cx nd" style="width:${sz}px;height:${sz}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#3a2e1f,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.35)">
       <span class="fl" style="color:#ffd98e">${ic('flame', '', `style="width:${sz * .55}px;height:${sz * .55}px"`)}</span></div>
       ${n.lab ? `<span class="mono nl" style="position:absolute;left:50%;top:${sz + 10}px;transform:translateX(-50%);font-size:${big ? 22 : 18}px;color:#ffd98e;white-space:nowrap">${n.lab}</span>` : ''}`);
    return { e, nd: e.querySelector('.nd'), fl: e.querySelector('.fl'), nl: e.querySelector('.nl'), sz };
  });
  s.lead = box(r, 960, 836, 1400, 90, 'disp gt', 'Lead with value', 'font-size:84px');
  s.candle = box(r, 960, 836, 1700, 70, '', 'A candle loses nothing by lighting another.', 'font:italic 600 52px/1 var(--f-b);color:#f7e6bf');
  s.bnb = box(r, 960, 836, 1400, 84, 'disp gt', 'Built, not bought.', 'font-size:84px');
  cue('whoosh', S(88.85), .5); cue('chime', S(89.42), .5); cue('hit', S(90.64), .7); shake(S(90.64), 7); cue('whoosh', S(91.55), .5);
  [92.1, 92.4, 92.7].forEach(x => cue('shout', S(x), .45)); cue('hit', S(93.1), .55);
  cue('whoosh', S(93.7), .4); cue('ignite', S(94.22), .8); [95.16, 95.84, 96.54].forEach(x => cue('ignite', S(x) + .3, .55)); for (let i = 0; i < 7; i++) cue('ignite', S(97.1) + i * .18, .3);
  cue('swell', S(98.8), .45, { dur: 2.4 }); cue('rise', S(101.2), .6); cue('chime', S(102.0), .7); cue('hit', S(102.2), .5);
}, (t, r, s) => {
  const A = out(t, S(91.4), .3), g = out(t, S(102.85), .3);
  { const k = ez.out(lin(t, S(89.35), S(89.8))); set(s.ch1, { o: k * A, y: (1 - k) * 20 }); shine(s.chT, t, S(89.7), 1); }
  { const k = slam(s.ch2, t, S(90.64), 1.5); s.ch2.style.opacity *= A; shine(s.ch2, t, S(90.8), .8); }
  // megaphone beat
  const M = ez.out(lin(t, S(91.7), S(92.1))), Mo = out(t, S(93.55), .3);
  set(s.mega, { o: M * Mo, r: Math.sin(t * 30) * 2 * M, x: (1 - M) * -40 });
  s.shouts.forEach((e, i) => { const t0 = S([92.1, 92.4, 92.7][i]), k = lin(t, t0, t0 + .6); set(e, { o: (k > 0 ? 1 - k * .7 : 0) * Mo, x: k * 260, s: .7 + .5 * k }); });
  s.crowd.forEach((e, i) => { const k = ez.inOut(lin(t, S(92.6) + i * .08, S(93.3) + i * .08)); set(e, { o: M * Mo * (1 - k * .8), x: k * 140, s: 1 - .2 * k }); });
  { const k = slam(s.megaX, t, S(93.1), 1.6); s.megaX.style.opacity *= Mo; }
  { const k = ez.out(lin(t, S(92.85), S(93.25))); set(s.shoutLab, { o: k * Mo, y: (1 - k) * 18 }); shine(s.shoutLab, t, S(93.1), .8); }
  // network, then the crown
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
    if (ln) {
      const a = P[n.par], b = P[i], k = ez.out(lin(t, n.lit - .32, n.lit));
      ln.setAttribute('x1', a.x); ln.setAttribute('y1', a.y); ln.setAttribute('x2', mix(a.x, b.x, k)); ln.setAttribute('y2', mix(a.y, b.y, k));
      ln.setAttribute('opacity', ((k > 0 ? 1 : 0) * g * (1 - form)).toFixed(3));
    }
  });
  const cp = s.crownOrder.map(ci => P[s.byCrown[ci]]); s.crownPath.setAttribute('d', 'M ' + cp.map(p => `${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(' L ') + ' Z');
  s.crownPath.setAttribute('opacity', (lin(t, S(101.7), S(102.2)) * g).toFixed(3));
  { const k = ez.out(lin(t, S(94.15), S(94.55))), o = out(t, S(98.6), .3); set(s.lead, { o: k * o * g, y: (1 - k) * 18 }); shine(s.lead, t, S(94.5), 1); }
  { const k = ez.out(lin(t, S(98.85), S(99.4))), o = out(t, S(101.0), .3); set(s.candle, { o: k * o * g, y: (1 - k) * 14 }); }
  { const k = slam(s.bnb, t, S(102.2), 1.4); s.bnb.style.opacity *= g; shine(s.bnb, t, S(102.35), .8); }
});

/* =====================================================================
   9. ACTION TAKERS: the gym, watch, do, teach, then home
   ===================================================================== */
chapter(S(103.1), 'Action takers');
av(S(102.95), 'split', .5); av(S(105.45), 'pip', .5);
E.scene('action', S(102.9), S(116.3), (r, s) => {
  s.a1 = box(r, R.cx, 300, 674, 34, 'mono', 'The MTG TRIBE is', 'font-size:22px;color:#ffd98e;letter-spacing:.4em');
  s.a2 = box(r, R.cx, 384, 674, 90, 'disp st', 'A tribe of', 'font-size:92px');
  s.a3 = el(r, '', `<div style="display:flex;align-items:center;justify-content:center;gap:16px">${ic('zap', '', 'style="width:90px;height:90px;color:#ffd98e;filter:drop-shadow(0 0 16px #f2ad3c)"')}<span class="disp gt a3t" style="font-size:118px">Action takers</span></div>`, `left:${R.x - 40}px;top:440px;width:${R.w + 80}px;height:130px`);
  s.a3t = s.a3.querySelector('.a3t');
  // gym
  s.card = el(r, 'glass', `<div style="padding:34px 38px;display:flex;flex-direction:column;gap:20px;height:100%">
     <span class="mono" style="font-size:18px;color:#ffd98e">Gym membership</span>
     <span class="disp" style="font-size:72px;color:#efe9df">Member</span>
     <div style="height:56px;background:repeating-linear-gradient(90deg,#efe9df 0 3px,transparent 3px 7px,#efe9df 7px 8px,transparent 8px 13px);opacity:.7;border-radius:4px"></div></div>`, 'left:400px;top:300px;width:480px;height:300px');
  s.cardX = box(r, 640, 450, 260, 260, '', `<svg width="260" height="260" viewBox="0 0 260 260"><path d="M40 40 L220 220 M220 40 L40 220" stroke="#ff7a4d" stroke-width="18" stroke-linecap="round" style="filter:drop-shadow(0 0 14px rgba(255,90,40,.7))"/></svg>`);
  s.cardLab = box(r, 640, 660, 480, 50, 'mono', 'Joining', 'font-size:26px;color:#ff9a7a');
  s.dumb = box(r, 1300, 270, 140, 140, '', ic('dumbbell', '', 'style="width:120px;height:120px;color:#ffd98e;filter:drop-shadow(0 0 14px #f2ad3c)"'));
  s.cells = []; for (let i = 0; i < 30; i++) { const cx = 1110 + (i % 6) * 76, cy = 380 + Math.floor(i / 6) * 58; s.cells.push(box(r, cx, cy, 62, 46, '', ic('check', '', 'style="width:26px;height:26px;stroke-width:3.4;opacity:0"'), 'border-radius:10px;box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.3);color:#1b140c')); }
  s.day = box(r, 1300, 690, 480, 50, 'mono', 'Day 0', 'font-size:28px;color:#ffd98e');
  s.showLab = box(r, 1300, 760, 480, 56, 'disp gt', 'Showing up ✓', 'font-size:58px');
  // watch, do, teach loop
  const pos = [[960, 290], [740, 640], [1180, 640]];
  s.loop = [['circle-play', 'Watch', 109.98], ['hammer', 'Do the work', 111.14], ['graduation-cap', 'Teach', 112.28]].map(([icn, lb, ts], i) => {
    const e = box(r, pos[i][0], pos[i][1], 210, 210, '', `<div class="cx lp" style="width:210px;height:210px;border-radius:50%;flex-direction:column;gap:10px;background:radial-gradient(circle at 35% 30%,#3a2e1f,#120e09);box-shadow:inset 0 0 0 2px rgba(255,217,142,.4)">${ic(icn, '', 'style="width:80px;height:80px;color:#ffd98e"')}<b class="mono" style="font-size:17px;color:#f7e6bf;letter-spacing:.2em">${lb}</b></div>`);
    cue('pop', S(ts), .6); return { e, lp: e.querySelector('.lp'), t: S(ts) };
  });
  const svg = svgLayer(r); defs(svg, GOLD_DEFS);
  s.arc = sv(svg, 'circle', { cx: 960, cy: 523, r: 250, fill: 'none', stroke: 'url(#gg)', 'stroke-width': 4, 'stroke-dasharray': '20 22', filter: 'url(#glow)' });
  // home
  s.house = el(r, '', `<svg width="620" height="560" viewBox="0 0 620 560" fill="none" stroke="#ffd98e" stroke-width="8" stroke-linejoin="round" stroke-linecap="round" style="filter:drop-shadow(0 0 14px rgba(242,173,60,.6))">
    <path class="hp" d="M40 260 L310 40 L580 260"/><path class="hp" d="M90 220 L90 520 L530 520 L530 220"/><path class="hp" d="M250 520 L250 360 L370 360 L370 520"/>
    <rect class="hw" x="130" y="290" width="90" height="80" rx="8" fill="rgba(255,217,142,0)"/><rect class="hw" x="400" y="290" width="90" height="80" rx="8" fill="rgba(255,217,142,0)"/>
    <rect class="hd" x="256" y="366" width="108" height="150" fill="rgba(255,217,142,0)" stroke="none"/></svg>`, 'left:650px;top:170px;width:620px;height:560px');
  s.hp = Array.from(s.house.querySelectorAll('.hp')); s.hp.forEach(p => { const L = p.getTotalLength(); p.style.strokeDasharray = L; p.dataset.l = L; });
  s.hw = Array.from(s.house.querySelectorAll('.hw')); s.hd = s.house.querySelector('.hd');
  s.chair = box(r, 960, 620, 80, 80, '', ic('armchair', '', 'style="width:64px;height:64px;color:#1b140c"'));
  s.seat = box(r, 960, 806, 1400, 80, 'disp gt', 'Your seat is waiting.', 'font-size:80px');
  cue('whoosh', S(103.0), .45); cue('hit', S(104.9), .75); shake(S(104.9), 8); cue('whoosh', S(105.5), .5); cue('stamp', S(107.4), .7);
  for (let i = 0; i < 30; i++) cue('tick', S(108.62) + i * .024, .22); cue('hit', S(109.04), .5); cue('whoosh', S(109.7), .45); cue('draw', S(113.6), .4, { dur: 1 }); cue('chime', S(115.14), .6);
}, (t, r, s) => {
  const A = out(t, S(105.35), .3), G = out(t, S(109.6), .3), L = out(t, S(113.25), .3), g = out(t, S(116.1), .35);
  up(s.a1, t, S(103.2)); s.a1.style.opacity *= A;
  up(s.a2, t, S(104.2)); s.a2.style.opacity *= A;
  { const k = slam(s.a3, t, S(104.9), 1.5); s.a3.style.opacity *= A; shine(s.a3t, t, S(105.05), .9); }
  // gym
  const gi = ez.out(lin(t, S(106.2), S(106.7)));
  set(s.card, { o: gi * G * (1 - .45 * lin(t, S(107.4), S(107.7))), x: (1 - gi) * -40, r: -3 });
  { const k = slam(s.cardX, t, S(107.4), 1.7); s.cardX.style.opacity *= G; }
  { const k = ez.out(lin(t, S(107.5), S(107.8))); set(s.cardLab, { o: k * G }); }
  const di = ez.out(lin(t, S(106.4), S(106.9))), rep = Math.max(0, Math.sin((t - S(108.6)) * 14)) * lin(t, S(108.6), S(108.8)) * (1 - lin(t, S(109.3), S(109.5)));
  set(s.dumb, { o: di * G, y: -rep * 26 });
  let n = 0; s.cells.forEach((c, i) => { const t0 = S(108.62) + i * .024, k = lin(t, t0, t0 + .08); if (k > 0) n = i + 1; set(c, { o: di * G, s: 1 + .15 * Math.sin(Math.PI * k) }); c.style.background = k > 0 ? `rgba(242,173,60,${(.9 * k).toFixed(2)})` : 'transparent'; c.firstChild.style.opacity = k; });
  s.day.textContent = 'Day ' + n; set(s.day, { o: di * G });
  { const k = slam(s.showLab, t, S(109.04), 1.4); s.showLab.style.opacity *= G; }
  // loop
  const li = ez.out(lin(t, S(109.75), S(110.1)));
  s.arc.setAttribute('opacity', (li * L).toFixed(3)); s.arc.setAttribute('transform', `rotate(${(t * 40).toFixed(1)} 960 523)`);
  s.loop.forEach(q => { const p = pop(t, q.t - .25), lit = lin(t, q.t, q.t + .25); set(q.e, { o: p.o * L, s: p.s * (1 + .06 * Math.exp(-Math.pow((t - q.t - .15) / .12, 2))) }); q.lp.style.boxShadow = `inset 0 0 0 2px rgba(255,217,142,${(.4 + .5 * lit).toFixed(2)}),0 0 ${(60 * lit).toFixed(0)}px rgba(242,173,60,${(.6 * lit).toFixed(2)})`; });
  // home
  const hd = ez.inOut(lin(t, S(113.6), S(114.7)));
  s.hp.forEach((p, i) => p.style.strokeDashoffset = (+p.dataset.l * (1 - clamp(hd * 1.4 - i * .2))).toFixed(1));
  set(s.house, { o: lin(t, S(113.5), S(113.7)) * g });
  const wl = ez.out(lin(t, S(115.1), S(115.5)));
  s.hw.forEach(w => w.setAttribute('fill', `rgba(255,217,142,${(.85 * wl).toFixed(2)})`)); s.hd.setAttribute('fill', `rgba(255,236,190,${(.95 * wl).toFixed(2)})`);
  { const p = pop(t, S(115.3)); set(s.chair, { o: p.o * g, s: p.s }); }
  { const k = ez.out(lin(t, S(115.3), S(115.7))); set(s.seat, { o: k * g, y: (1 - k) * 18 }); shine(s.seat, t, S(115.6), 1); }
});

/* =====================================================================
   10. YOUR ONE STEP: the links, exactly as in the original
   ===================================================================== */
chapter(S(116.4), 'Your one step');
av(S(116.15), 'split', .5); av(S(131.95), 'pip', .5);
E.scene('cta', S(116.1), S(132.4), (r, s) => {
  s.one = box(r, R.cx, 420, 300, 300, '', `<div class="cx" style="width:280px;height:280px;border-radius:50%;box-shadow:inset 0 0 0 4px #f2ad3c,0 0 60px rgba(242,173,60,.4);background:radial-gradient(circle at 40% 30%,rgba(255,217,142,.15),rgba(0,0,0,.4))"><span class="disp gt one-t" style="font-size:220px;line-height:1">1</span></div>`);
  s.oneT = s.one.querySelector('.one-t');
  s.oneL = box(r, R.cx, 610, 600, 40, 'mono', 'One step', 'font-size:26px;color:#ffd98e;letter-spacing:.5em');
  s.hdr = box(r, R.cx, 214, 674, 30, 'mono', 'Your one step', 'font-size:20px;color:#ffd98e;letter-spacing:.42em');
  s.btn = el(r, '', `<div style="display:flex;align-items:center;gap:20px;height:100%;padding:0 34px">${ic('whatsapp', '', 'style="width:60px;height:60px;color:#fff"')}<span class="ty" style="font:800 46px/1 var(--f-b);color:#fff;letter-spacing:-.01em;white-space:nowrap"></span><span class="cur" style="width:4px;height:48px;background:#fff"></span></div>`,
    `left:${R.x + 20}px;top:252px;width:${R.w - 40}px;height:124px;border-radius:62px;background:linear-gradient(180deg,#34e07a,#14a34f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.25),0 20px 50px rgba(20,163,79,.35),0 0 0 rgba(0,0,0,0)`);
  s.ty = s.btn.querySelector('.ty'); s.cur = s.btn.querySelector('.cur');
  s.ripple = box(r, 1640, 314, 100, 100, '', '', 'border-radius:50%;box-shadow:0 0 0 4px rgba(255,255,255,.8)');
  s.ptr = box(r, 0, 0, 70, 70, '', ic('mouse-pointer-click', '', 'style="width:64px;height:64px;color:#fff;filter:drop-shadow(0 4px 10px rgba(0,0,0,.8))"'));
  s.join = box(r, R.cx, 418, 674, 60, '', `<span class="chip" style="font-size:24px">${ic('users')}Join the WhatsApp tribe</span>`);
  s.tt = el(r, '', `<div style="display:flex;align-items:center;gap:20px;height:100%;padding:0 30px">${ic('tiktok', '', 'style="width:50px;height:50px;color:#fff"')}<span style="display:flex;flex-direction:column;gap:8px"><b style="font:800 40px/1 var(--f-b)">@joinmtgtribe</b><small class="mono" style="font-size:15px;color:#ffd98e">Follow us on TikTok</small></span></div>`,
    `left:${R.x + 20}px;top:478px;width:${R.w - 40}px;height:100px;border-radius:28px;background:linear-gradient(160deg,rgba(52,42,26,.92),rgba(16,13,9,.95));box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.4),0 18px 40px rgba(0,0,0,.5)`);
  s.wa = el(r, '', `<div style="display:flex;align-items:center;gap:20px;height:100%;padding:0 30px">${ic('whatsapp', '', 'style="width:50px;height:50px;color:#25d366"')}<span style="display:flex;flex-direction:column;gap:8px"><b style="font:800 36px/1 var(--f-b);white-space:nowrap">WhatsApp MTG: 072 171 4626</b><small class="mono" style="font-size:15px;color:#ffd98e">Talk to me directly</small></span></div>`,
    `left:${R.x + 20}px;top:596px;width:${R.w - 40}px;height:100px;border-radius:28px;background:linear-gradient(160deg,rgba(52,42,26,.92),rgba(16,13,9,.95));box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.4),0 18px 40px rgba(0,0,0,.5)`);
  s.vn = el(r, '', `<div style="display:flex;align-items:center;gap:14px;height:100%;padding:0 22px">${ic('mic', '', 'style="width:32px;height:32px;color:#ffd98e"')}<span class="bars" style="display:flex;align-items:center;gap:5px;height:40px"></span><b class="mono" style="font-size:16px;color:#f7e6bf">Voice note</b></div>`,
    `left:${R.x + 20}px;top:712px;width:420px;height:58px;border-radius:29px;background:rgba(20,16,10,.9);box-shadow:inset 0 0 0 1.5px rgba(255,217,142,.35)`);
  s.bars = []; const bw = s.vn.querySelector('.bars'); for (let i = 0; i < 16; i++) { const b = document.createElement('i'); b.style.cssText = 'display:block;width:5px;border-radius:3px;background:#ffd98e;height:10px'; bw.appendChild(b); s.bars.push(b); }
  s.pay = box(r, R.cx, 818, 760, 80, 'disp gt', 'Pay attention. Take action.', 'font-size:56px');
  s.text = 'mtgtribe.com/group';
  cue('whoosh', S(116.2), .45); cue('hit', S(116.84), .55); cue('whoosh', S(117.7), .45);
  for (let i = 0; i < s.text.length; i++) cue('type', S(118.08) + (S(120.16) - S(118.08)) * i / s.text.length, .35);
  cue('click', S(120.84), .8); cue('pop', S(121.0), .5); cue('pop', S(122.62), .55); cue('pop', S(126.86), .55); cue('pop', S(129.26), .4); cue('hit', S(131.58), .6); shake(S(131.58), 6); cue('whoosh', S(131.95), .5);
}, (t, r, s) => {
  const g = out(t, S(131.95), .35);
  { const p = pop(t, S(116.45)), o = out(t, S(117.6), .3); set(s.one, { o: p.o * o, s: p.s * (1 + .06 * Math.exp(-Math.pow((t - S(116.9)) / .1, 2))) }); shine(s.oneT, t, S(116.7), .9);
    const k = ez.out(lin(t, S(116.84), S(117.1))); set(s.oneL, { o: k * o }); }
  { const k = ez.out(lin(t, S(117.6), S(118.0))); set(s.hdr, { o: k * g }); }
  const bi = ez.back(lin(t, S(117.75), S(118.2))), press = Math.exp(-Math.pow((t - S(120.88)) / .07, 2));
  set(s.btn, { o: lin(t, S(117.75), S(117.9)) * g, s: (.8 + .2 * clamp(bi, 0, 1.1)) * (1 - .05 * press) });
  const n = Math.round(s.text.length * lin(t, S(118.08), S(120.16))); s.ty.textContent = s.text.slice(0, n);
  s.cur.style.opacity = (t < S(120.5) && Math.floor(t * 3) % 2 === 0) || (t > S(118.0) && t < S(120.2)) ? 1 : 0;
  // pointer glides in and clicks
  const pk = ez.inOut(lin(t, S(120.15), S(120.75)));
  s.ptr.style.left = mix(1760, 1630, pk) + 'px'; s.ptr.style.top = mix(560, 320, pk) + 'px';
  set(s.ptr, { o: lin(t, S(120.1), S(120.25)) * (1 - lin(t, S(121.6), S(121.9))) * g, s: 1 - .15 * press });
  { const k = lin(t, S(120.84), S(121.5)); set(s.ripple, { o: k > 0 ? (1 - k) * g : 0, s: .5 + 2.2 * k }); }
  { const p = pop(t, S(121.0)); set(s.join, { o: p.o * g, s: p.s }); }
  { const k = ez.out(lin(t, S(122.6), S(123.0))); set(s.tt, { o: k * g, x: (1 - k) * 40 }); }
  { const k = ez.out(lin(t, S(126.8), S(127.2))); set(s.wa, { o: k * g, x: (1 - k) * 40 }); }
  { const k = ez.out(lin(t, S(129.2), S(129.55))); set(s.vn, { o: k * g, x: (1 - k) * 40 }); s.bars.forEach((b, i) => { b.style.height = (8 + 30 * Math.abs(Math.sin(t * 7 + i * .9) * Math.sin(t * 3.1 + i * .37))).toFixed(1) + 'px'; }); }
  { const k = slam(s.pay, t, S(131.58), 1.4); s.pay.style.opacity *= g; shine(s.pay, t, S(131.7), .8); }
});

/* =====================================================================
   11. THANK YOU: not financial advice, like share comment, your member card, crowned
   ===================================================================== */
chapter(S(132.2), 'Thank you');
av(S(150.2), 'hero', .6); av(S(153.95), 'hidden', .45);
E.scene('thanks', S(132.1), S(150.7), (r, s) => {
  s.nfa = box(r, 960, 450, 1080, 260, 'glass', `<div style="display:flex;align-items:center;gap:40px;padding:0 50px;height:100%"><span class="ibox" style="width:150px;height:150px;display:grid;flex:none">${ic('shield-check', '', 'style="width:80px;height:80px"')}</span>
    <span style="display:flex;flex-direction:column;gap:20px;text-align:left"><span class="disp st nfa1" style="font-size:86px">Not financial advice</span><span class="nfa2" style="font:700 40px/1 var(--f-b);color:#f7e6bf">Always do your own research.</span></span></div>`);
  s.nfa1 = s.nfa.querySelector('.nfa1'); s.nfa2 = s.nfa.querySelector('.nfa2');
  s.heart = box(r, 960, 450, 520, 520, '', ic('heart', '', 'style="width:480px;height:480px;color:rgba(242,173,60,.18);fill:rgba(242,173,60,.12)"'));
  s.soc = [['thumbs-up', 'Like', 139.06], ['share-2', 'Share', 139.62], ['message-circle', 'Comment', 140.16]].map(([icn, lb, ts], i) => {
    const e = box(r, 640 + i * 320, 430, 200, 250, '', `<div class="cx" style="width:180px;height:180px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd98e,#c17a1e);box-shadow:0 0 50px rgba(242,173,60,.45),inset 0 0 0 3px rgba(255,246,220,.5);color:#1b140c">${ic(icn, '', 'style="width:84px;height:84px;stroke-width:2.4"')}</div><b class="mono" style="position:absolute;bottom:-6px;font-size:22px;color:#ffd98e">${lb}</b>`, 'flex-direction:column');
    const hearts = []; const rnd = E.rng(20 + i); for (let k = 0; k < 6; k++) hearts.push({ h: box(r, 640 + i * 320, 380, 40, 40, '', ic('heart', '', 'style="width:34px;height:34px;color:#ffd98e;fill:#f2ad3c"')), vx: (rnd() - .5) * 260, vy: -200 - rnd() * 260, d: rnd() * .15 });
    cue('pop', S(ts), .7); return { e, t: S(ts), hearts };
  });
  // the member card
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
    <span class="crown" style="position:absolute;left:58px;top:150px;font-size:100px;filter:drop-shadow(0 0 20px rgba(242,173,60,.8))">👑</span>`, 'left:540px;top:200px;width:840px;height:520px');
  s.sheen = s.card.querySelector('.sheen'); s.you = s.card.querySelector('.you'); s.crown = s.card.querySelector('.crown'); s.st1 = s.card.querySelector('.st1');
  cue('whoosh', S(132.3), .45); cue('hit', S(134.16), .45); cue('whoosh', S(136.9), .4); cue('swell', S(141.0), .4, { dur: 2 });
  cue('flip', S(143.1), .8); cue('shimmer', S(144.14), .6); cue('whoosh', S(148.7), .4); cue('chime', S(149.66), 1); flash(S(149.66), .4, .3); cue('whoosh', S(150.2), .55);
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

/* =====================================================================
   12. CRYPTO REGARDS: end card with every CTA from the original
   ===================================================================== */
chapter(S(150.5), 'Crypto regards');
capHide.push([S(153.85), TOTAL + 1]);
E.scene('end', S(150.3), TOTAL, (r, s) => {
  s.np = namePlate(r); s.overlays = [s.np];
  s.cr = box(r, 960, 160, 1200, 150, 'gt', 'Crypto Regards,', 'font:400 120px/1.1 "Great Vibes",cursive;filter:drop-shadow(0 0 24px rgba(242,173,60,.35))');
  s.mtg = box(r, 960, 318, 1000, 180, '', '<span class="disp gt" style="font-size:176px;line-height:1">MTG</span><span style="font-size:120px;margin-left:10px">👑</span>');
  s.arch = box(r, 960, 432, 1000, 40, 'mono', 'Your Digital Architect', 'font-size:26px;color:#ffd98e;letter-spacing:.42em');
  s.seat = box(r, 960, 505, 1000, 34, 'mono', 'Your seat is waiting', 'font-size:20px;color:#f7e6bf;letter-spacing:.42em');
  s.btn = box(r, 960, 590, 720, 112, '', `<div class="cx" style="gap:20px;width:720px;height:112px;border-radius:56px;background:linear-gradient(180deg,#34e07a,#14a34f);box-shadow:inset 0 0 0 2px rgba(255,255,255,.25),0 20px 60px rgba(20,163,79,.4)">${ic('whatsapp', '', 'style="width:56px;height:56px;color:#fff"')}<b style="font:800 48px/1 var(--f-b);color:#fff">mtgtribe.com/group</b></div>`);
  s.c1 = box(r, 700, 712, 480, 70, '', `<span class="chip" style="font-size:26px">${ic('tiktok', '', 'style="color:#fff"')}@joinmtgtribe on TikTok</span>`);
  s.c2 = box(r, 1220, 712, 520, 70, '', `<span class="chip" style="font-size:26px">${ic('whatsapp', '', 'style="color:#25d366"')}WhatsApp MTG: 072 171 4626</span>`);
  s.slog = box(r, 960, 852, 1400, 96, '', '', 'font:400 84px/1 var(--f-d);text-transform:none;letter-spacing:.01em');
  s.slog.innerHTML = ["Let's", 'Get', 'This', 'Crypto!', '💪'].map((w, i) => `<span class="${i < 4 ? 'gt' : ''}" style="display:inline-block;margin:0 .14em">${w}</span>`).join('');
  s.sw = Array.from(s.slog.children); s.swt = [154.04, 154.24, 154.32, 154.52, 154.68].map(S);
  cue('whoosh', S(150.25), .5); cue('whoosh', S(153.95), .6); cue('shimmer', S(154.05), .6); s.swt.forEach((x, i) => cue('hit', x, i === 4 ? .6 : .3)); cue('chime', S(154.8), .6);
}, (t, r, s) => {
  const n = ez.out(lin(t, S(150.62), S(151.05))), ng = out(t, S(153.75), .25);
  set(s.np, { o: n * ng, x: (1 - n) * -60 }); s.np.style.clipPath = `inset(0 ${((1 - n) * 100).toFixed(1)}% 0 0 round 22px)`; shine(s.np.querySelector('.gt'), t, S(150.9), 1);
  const fade = 1 - lin(t, TOTAL - .7, TOTAL - .05);
  const items = [[s.cr, 153.98], [s.mtg, 154.2], [s.arch, 154.42], [s.seat, 154.62], [s.btn, 154.8], [s.c1, 155.0], [s.c2, 155.12]];
  items.forEach(([e, ts]) => { const k = ez.out(lin(t, S(ts), S(ts) + .45)); set(e, { o: k * fade, y: (1 - k) * 22, b: (1 - k) * 6 }); });
  shine(s.mtg.firstChild, t, S(154.5), 1.2);
  const br = 1 + .025 * Math.sin((t - S(155)) * 3) * lin(t, S(155.2), S(155.6)); s.btn.style.transform += ` scale(${br.toFixed(4)})`;
  s.sw.forEach((w, i) => { const k = lin(t, s.swt[i] - .02, s.swt[i] + .16); set(w, { o: lin(t, s.swt[i] - .02, s.swt[i] + .05) * fade, s: k <= 0 ? 1.5 : 1.5 - .5 * ez.out(k) }); });
  shine(s.sw[3], t, S(155.3), 1.2);
  E.lastFade = fade;
});
})();

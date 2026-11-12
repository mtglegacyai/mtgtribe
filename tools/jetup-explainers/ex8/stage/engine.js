/* JetUP explainer #8 ("Getting your money out"), 16:9. Every visual is a pure function of time t.
   The picture: a fruit tree in your own backyard, one illustration that persists and grows across the scenes, with a camera
   (translate + scale of #world) that frames one focal point at a time. The backyard behind its gate ("TAG Markets · the
   broker") is your account at TAG Markets in your own name (the name plate); the tree is your own money; the fruit is your
   profit when the strategy makes one; the lime-ribboned gift branch is the promo; the basket outside the gate is your
   crypto wallet; the path through the gate is how withdrawals go (a labelled illustration). Nothing is picked before
   "My advice?": then the small mango from the hook makes the first trip. Labels live in screen space (never scaled).
   The signature ending (the 9:09 sign-up training's) is composited on top after the stage render (tools/video-signature). */
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
let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;

/* ---------- world coordinates (the picture at scale 1) ---------- */
const TX = 700, TB = 664;                                  // trunk centre x, trunk base y (on the lawn, just behind the fence)
const CR = { x: 690, y: 320, rx: 285, ry: 172 };            // the crown
const GX = 1218, POSTL = [GX - 148, GX - 118], POSTR = [GX + 118, GX + 148]; // gate centre, posts
const FT = 680, FB = 770;                                   // fence tips, fence base (the ground line)
const PLATE = [GX + 160, 700, 92, 56];                      // name plate x, y, w, h (on the pickets right of the gate)
const BK = { x: 1620, y: 772, rx: 112, ry: 25, by: 866, brx: 88 }; // the basket: rim centre, rim radii, bottom
const MANGO = 'M0 -27 C 15 -27 24 -12 23 6 C 22 22 10 31 -3 30 C -15 29 -23 18 -21 3 C -19 -12 -13 -27 0 -27 Z';
const RIPE = [[548, 474, 1], [790, 488, 1.02], [866, 404, .96]];   // the two or three mangoes (x, y, size)
const MS = [1012, 614, .74];                               // the small mango from the hook (behind the fence, beside the gate)
const GIFT = { bx: 478, by: 600, w: 72, h: 66 };            // the gift box hanging from the gift branch
const PATHD = 'M 722 664 C 860 668 1040 672 1160 690 C 1200 697 1218 722 1222 770 C 1227 815 1310 842 1400 838 C 1480 834 1530 815 1560 792';

const G = { ground: $('wGround'), tree: $('wTree'), fence: $('wFence'), front: $('wFront') };

/* ground: the lawn of your backyard behind the fence, the ground outside it */
const lawn = sv('g', {}, G.ground);
sv('rect', { x: -3000, y: 500, width: 8000, height: 280, fill: 'url(#gLawn)' }, lawn);
sv('ellipse', { cx: 760, cy: 640, rx: 620, ry: 70, fill: 'url(#gYard)' }, lawn);
const yardGlow = sv('ellipse', { cx: 740, cy: 650, rx: 520, ry: 90, fill: 'url(#gGlowLime)', opacity: 0 }, lawn);
for (let i = 0; i < 70; i++) {                              // grass tufts on the lawn
  const x = -300 + rnd() * 2500, y = 600 + rnd() * 80, h = 6 + rnd() * 9;
  sv('path', { d: `M${x} ${y} l -3 ${-h} M${x + 3} ${y} l 2 ${-h * 1.2} M${x + 6} ${y} l 5 ${-h * .8}`, stroke: rnd() < .5 ? '#2f6e33' : '#3f8a3c', 'stroke-width': 2, 'stroke-linecap': 'round', opacity: .55 }, lawn);
}
const outside = sv('g', {}, G.ground);
sv('rect', { x: -3000, y: FB - 2, width: 8000, height: 520, fill: 'url(#gGround)' }, outside);
sv('ellipse', { cx: GX + 40, cy: FB + 46, rx: 420, ry: 80, fill: 'url(#gGlowVio)', opacity: .55 }, outside);
sv('rect', { x: -3000, y: FB - 2, width: 8000, height: 3, fill: '#cbfb61', opacity: .12 }, outside);
for (let i = 0; i < 90; i++) {                              // grass along the outside of the fence
  const x = -300 + i * 30 + rnd() * 14, y = FB + 4 + rnd() * 6, h = 7 + rnd() * 9;
  sv('path', { d: `M${x} ${y} l -3 ${-h} M${x + 3} ${y} l 2 ${-h * 1.2} M${x + 6} ${y} l 5 ${-h * .8}`, stroke: rnd() < .5 ? '#2c5e33' : '#3a7a3b', 'stroke-width': 2.2, 'stroke-linecap': 'round', opacity: .7 }, outside);
}
const stoneD = [[1236, 794, 40, 11], [1300, 822, 46, 12], [1384, 834, 50, 13], [1468, 826, 46, 12]];
stoneD.forEach(([x, y, rx, ry]) => {                        // stepping stones from the gate towards the basket
  sv('ellipse', { cx: x + 3, cy: y + 4, rx, ry, fill: '#000', opacity: .35 }, outside);
  sv('ellipse', { cx: x, cy: y, rx, ry, fill: '#3b3355' }, outside);
  sv('ellipse', { cx: x - 6, cy: y - 3, rx: rx * .7, ry: ry * .5, fill: '#5a5178', opacity: .55 }, outside);
});

/* the tree: trunk (your own money), crown, the mangoes, the small mango's stalk, the gift branch */
const treeG = sv('g', {}, G.tree);
const trunkG = sv('g', { 'clip-path': 'url(#cTrunk)' }, treeG);
const TRUNK = 'M 652 668 C 672 650 676 612 676 572 C 676 536 670 502 660 474 C 640 444 600 410 552 372 L 566 360 C 606 392 646 418 680 444 ' +
  'C 684 404 690 362 694 300 L 712 300 C 716 362 718 404 722 444 C 756 414 800 384 846 352 L 858 366 C 816 398 772 436 744 476 ' +
  'C 734 514 728 548 728 584 C 728 620 738 650 760 668 Z';
sv('ellipse', { cx: TX + 4, cy: TB + 2, rx: 92, ry: 12, fill: '#000', opacity: .35, filter: 'url(#fBlur3)' }, trunkG);
const trunkP = sv('path', { d: TRUNK, fill: 'url(#gTrunk)' }, trunkG);
[['M 668 650 C 676 610 674 560 666 520', .35], ['M 702 656 C 708 610 706 560 700 500', .3], ['M 716 640 C 722 600 722 556 716 520', .25],
 ['M 690 600 C 694 580 694 560 690 540', .3]].forEach(([d, o]) => sv('path', { d, fill: 'none', stroke: '#2a180c', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: o }, trunkG));
sv('path', { d: 'M 726 660 C 722 620 724 560 734 500', fill: 'none', stroke: '#ffd98a', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: .35 }, trunkG);
const trunkLit = sv('path', { d: TRUNK, fill: '#cbfb61', opacity: 0 }, trunkG);
const trunkGlow = sv('ellipse', { cx: TX, cy: 570, rx: 90, ry: 130, fill: 'url(#gGlowLime)', opacity: 0 }, treeG);
treeG.insertBefore(trunkGlow, trunkG);

// the gift branch (the promo), tied onto the trunk with a lime ribbon; hidden until "gift branch"
const giftG = sv('g', { opacity: 0 }, treeG);
const branchP = sv('path', { d: 'M 676 520 C 620 532 552 548 478 584', fill: 'none', stroke: 'url(#gBranch)', 'stroke-width': 15, 'stroke-linecap': 'round' }, giftG);
const BRL = branchP.getTotalLength();
const bleaves = [];
[[600, 538, -150], [560, 548, -30], [526, 560, -160], [500, 574, -20], [640, 528, -40]].forEach(([x, y, r]) => {
  bleaves.push(sv('ellipse', { cx: x, cy: y, rx: 24, ry: 8, fill: '#2f7d34', transform: `rotate(${r} ${x} ${y})` }, giftG)); });
const giftString = sv('line', { x1: 480, y1: 584, x2: 478, y2: 600, stroke: '#e8c25a', 'stroke-width': 2.5 }, giftG);
const giftBox = sv('g', {}, giftG);
sv('rect', { x: GIFT.bx - GIFT.w / 2, y: GIFT.by, width: GIFT.w, height: GIFT.h, rx: 8, fill: 'url(#gGift)', filter: 'url(#fSoft)' }, giftBox);
sv('rect', { x: GIFT.bx - GIFT.w / 2 - 4, y: GIFT.by, width: GIFT.w + 8, height: 18, rx: 5, fill: '#b9a3ff' }, giftBox);
sv('rect', { x: GIFT.bx - 7, y: GIFT.by, width: 14, height: GIFT.h, fill: 'url(#gRibbon)' }, giftBox);
sv('rect', { x: GIFT.bx - GIFT.w / 2 - 4, y: GIFT.by + 7, width: GIFT.w + 8, height: 10, fill: 'url(#gRibbon)' }, giftBox);
sv('path', { d: `M ${GIFT.bx} ${GIFT.by + 2} C ${GIFT.bx - 30} ${GIFT.by - 22} ${GIFT.bx - 34} ${GIFT.by + 8} ${GIFT.bx} ${GIFT.by + 2} M ${GIFT.bx} ${GIFT.by + 2} C ${GIFT.bx + 30} ${GIFT.by - 22} ${GIFT.bx + 34} ${GIFT.by + 8} ${GIFT.bx} ${GIFT.by + 2}`, fill: '#d8ff7a', stroke: '#8fcf2a', 'stroke-width': 2 }, giftBox);
const ribbonGlow = sv('ellipse', { cx: 676, cy: 516, rx: 70, ry: 54, fill: 'url(#gGlowLime)', opacity: 0 }, giftG);
const bow = sv('g', {}, giftG);
sv('path', { d: 'M 664 506 l 26 -4 l 2 12 l -26 5 Z M 664 524 l 26 -4 l 2 10 l -26 5 Z', fill: 'url(#gRibbon)' }, bow);
sv('path', { d: 'M 678 512 C 650 486 636 500 650 516 C 660 526 672 520 678 512 Z M 678 512 C 706 484 722 498 708 516 C 698 526 686 520 678 512 Z', fill: '#d8ff7a', stroke: '#8fcf2a', 'stroke-width': 2 }, bow);
sv('path', { d: 'M 674 516 l -12 34 l 10 -4 l 6 8 l 4 -36 Z M 684 516 l 14 32 l -10 -2 l -4 9 l -6 -36 Z', fill: '#b8ec4c' }, bow);
sv('circle', { cx: 678, cy: 513, r: 7, fill: '#e9ff9e' }, bow);
const ring = sv('g', {}, giftG), dots = [];
for (let i = 0; i < 12; i++) {
  const a = -Math.PI / 2 + i * Math.PI / 6, x = GIFT.bx + 84 * Math.cos(a), y = GIFT.by + GIFT.h / 2 + 84 * Math.sin(a);
  dots.push([sv('circle', { cx: x, cy: y, r: 9, fill: 'rgba(255,255,255,.14)', stroke: 'rgba(255,255,255,.35)', 'stroke-width': 2 }, ring),
             sv('circle', { cx: x, cy: y, r: 9, fill: '#cbfb61', opacity: 0 }, ring)]);
}

// the crown: back masses, mid masses, light masses, then mango leaves (procedural, seeded), all revealed from the trunk top
const crownG = sv('g', { 'clip-path': 'url(#cCrown)' }, treeG);
const msStalk = sv('path', { d: 'M 924 470 C 958 506 990 548 1008 588', fill: 'none', stroke: '#5a3a22', 'stroke-width': 4, 'stroke-linecap': 'round' }, crownG);
sv('ellipse', { cx: 958, cy: 510, rx: 18, ry: 6, fill: '#2f7d34', transform: 'rotate(55 958 510)' }, crownG);
sv('ellipse', { cx: 984, cy: 546, rx: 16, ry: 5, fill: '#3f9440', transform: 'rotate(-30 984 546)' }, crownG);
const blobs = [];
for (let i = 0; i < 11; i++) {                              // the dome: masses round the upper half and the sides
  const a = Math.PI * (1.0 + i / 10);
  blobs.push([CR.x + .7 * CR.rx * Math.cos(a), CR.y + .55 * CR.ry * Math.sin(a), 74 + 12 * rnd(), 'url(#gBlobD)']);
}
[[-205, 62, 80], [-110, 104, 86], [0, 112, 88], [110, 104, 86], [205, 58, 78]].forEach(([x, y, r]) => blobs.push([CR.x + x, CR.y + y, r, 'url(#gBlobD)']));
[[-120, -6, 112], [0, -36, 118], [124, 0, 110], [0, 46, 118], [-86, 50, 96], [96, 56, 98]].forEach(([x, y, r]) => blobs.push([CR.x + x, CR.y + y, r, 'url(#gBlobM)']));
[[-120, -78, 76], [-20, -98, 74], [92, -86, 72], [-196, -26, 64], [-64, -40, 70], [176, -36, 62]].forEach(([x, y, r]) => blobs.push([CR.x + x, CR.y + y, r, 'url(#gBlobL)']));
const blobEls = blobs.map(([x, y, r, f]) => [sv('circle', { cx: x, cy: y, r, fill: f }, crownG), x, y, r]);
const leafG = sv('g', {}, crownG);
for (let i = 0; i < 260; i++) {
  const a = rnd() * Math.PI * 2, rf = .62 + .44 * Math.sqrt(rnd());
  const x = CR.x + CR.rx * rf * Math.cos(a), y = CR.y + CR.ry * rf * Math.sin(a) * (Math.sin(a) > 0 ? .86 : 1);
  if (y > CR.y + CR.ry - 2 || y < CR.y - CR.ry + 6) continue;
  const top = clamp((CR.y + CR.ry - y) / (2 * CR.ry)), lit = rnd() < .06 * top;
  const col = lit ? '#8fca52' : ['#14421f', '#1b5427', '#24692f', '#317d38', '#42953f'][Math.min(4, Math.floor(top * 3.6 + rnd() * 1.4))];
  const rot = a * 180 / Math.PI + 90 + (rnd() - .5) * 70;
  sv('ellipse', { cx: x, cy: y, rx: 23 + rnd() * 9, ry: 6.5 + rnd() * 2, fill: col, opacity: .92, transform: `rotate(${rot.toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})` }, leafG);
}
sv('ellipse', { cx: CR.x, cy: CR.y + 150, rx: 260, ry: 60, fill: '#06140a', opacity: .28, filter: 'url(#fBlur)' }, crownG);   // shade under the crown
// the ripe mangoes (hidden until "bears fruit")
function mango(parent, x, y, k, withStalk = true) {
  const g = sv('g', { transform: `translate(${x} ${y}) scale(${k})` }, parent);
  if (withStalk) sv('path', { d: 'M 0 -26 C 1 -36 -2 -44 -6 -52', fill: 'none', stroke: '#5a3a22', 'stroke-width': 3.5, 'stroke-linecap': 'round' }, g);
  const glow = sv('circle', { cx: 0, cy: 2, r: 58, fill: 'url(#gGlowGold)', opacity: 0 }, g);
  const raw = sv('path', { d: MANGO, fill: 'url(#gRaw)' }, g);
  const ripe = sv('path', { d: MANGO, fill: 'url(#gRipe)', opacity: 0 }, g);
  const blush = sv('path', { d: MANGO, fill: 'url(#gBlush)', opacity: 0 }, g);
  sv('ellipse', { cx: -8, cy: -12, rx: 5, ry: 9, fill: '#fff', opacity: .38, transform: 'rotate(18 -8 -12)' }, g);
  return { g, glow, raw, ripe, blush, x, y, k };
}
const fruitG = sv('g', {}, treeG);
const ripe = RIPE.map(([x, y, k]) => mango(fruitG, x, y, k));
const msG = sv('g', {}, G.tree);                            // the small mango: on screen from the hook (behind the fence)
const small = mango(msG, MS[0], MS[1], MS[2], false);

/* the fence: pickets that grow outward from the gate, rails, the gate's posts, beam and sign, the name plate */
const railG = sv('g', {}, G.fence);
const pickets = [];
for (let x = 40; x < 1880; x += 38) {
  if (x + 24 > POSTL[0] - 10 && x < POSTR[1] + 10) continue;
  const g = sv('g', {}, G.fence);
  sv('path', { d: `M${x} ${FT + 10} L${x + 12} ${FT} L${x + 24} ${FT + 10} L${x + 24} ${FB} L${x} ${FB} Z`, fill: 'url(#gPicket)' }, g);
  sv('path', { d: `M${x} ${FT + 10} L${x + 12} ${FT} L${x + 24} ${FT + 10} L${x + 24} ${FB} L${x} ${FB} Z`, fill: 'url(#gPicketS)' }, g);
  pickets.push([g, x + 12]);
}
[[FT + 26, 9], [FB - 26, 9]].forEach(([y, h]) => {
  sv('rect', { x: 30, y, width: POSTL[0] - 30, height: h, fill: 'url(#gRail)' }, railG);
  sv('rect', { x: POSTR[1], y, width: 1870 - POSTR[1], height: h, fill: 'url(#gRail)' }, railG);
});
const gateG = sv('g', {}, G.fence);
const postEls = [POSTL, POSTR].map(([a, b]) => {
  const g = sv('g', {}, gateG);
  sv('rect', { x: a, y: 575, width: b - a, height: FB - 575, fill: 'url(#gPost)' }, g);
  sv('path', { d: `M${a - 5} 575 L${(a + b) / 2} 550 L${b + 5} 575 Z`, fill: 'url(#gGoldH)' }, g);
  sv('rect', { x: a - 5, y: 575, width: b - a + 10, height: 8, rx: 2, fill: '#c39437' }, g);
  return g;
});
const beamG = sv('g', {}, gateG);
sv('rect', { x: GX - 168, y: 548, width: 336, height: 14, rx: 4, fill: 'url(#gPost)' }, beamG);
sv('rect', { x: GX - 168, y: 548, width: 336, height: 3, fill: '#ffd98a', opacity: .5 }, beamG);
const signG = sv('g', {}, gateG);
[[GX - 102, GX - 92], [GX + 92, GX + 102]].forEach(([a, b]) => sv('rect', { x: a, y: 538, width: b - a, height: 12, fill: '#c39437' }, signG));
const signGlow = sv('rect', { x: GX - 242, y: 466, width: 484, height: 90, rx: 26, fill: '#e8c25a', opacity: 0, filter: 'url(#fBlur)' }, signG);
sv('rect', { x: GX - 228, y: 480, width: 456, height: 62, rx: 14, fill: 'url(#gSign)', stroke: 'url(#gGoldH)', 'stroke-width': 3, filter: 'url(#fSoft)' }, signG);
sv('rect', { x: GX - 221, y: 487, width: 442, height: 48, rx: 10, fill: 'none', stroke: 'rgba(255,224,143,.28)', 'stroke-width': 1.2 }, signG);
const signT = sv('text', { x: GX, y: 523, 'text-anchor': 'middle', 'font-family': 'Manrope', 'font-weight': 800, 'font-size': 33, fill: '#fff' }, signG);
signT.innerHTML = 'TAG Markets <tspan fill="#e8c25a" font-weight="700">· the broker</tspan>';
const plateG = sv('g', {}, G.fence);
const [PX, PY, PW, PH] = PLATE;
const plateGlow = sv('rect', { x: PX - 22, y: PY - 22, width: PW + 44, height: PH + 44, rx: 26, fill: '#b39cff', opacity: 0, filter: 'url(#fBlur)' }, plateG);
sv('rect', { x: PX, y: PY, width: PW, height: PH, rx: 9, fill: 'url(#gGoldH)', filter: 'url(#fSoft)' }, plateG);
sv('rect', { x: PX + 5, y: PY + 5, width: PW - 10, height: PH - 10, rx: 6, fill: 'none', stroke: 'rgba(90,60,20,.55)', 'stroke-width': 1.5 }, plateG);
sv('circle', { cx: PX + 26, cy: PY + 21, r: 8, fill: '#6b4a1c' }, plateG);
sv('path', { d: `M${PX + 12} ${PY + 46} C ${PX + 12} ${PY + 32} ${PX + 40} ${PY + 32} ${PX + 40} ${PY + 46} Z`, fill: '#6b4a1c' }, plateG);
sv('circle', { cx: PX + 66, cy: PY + 24, r: 7, fill: '#2a1a08' }, plateG);
sv('path', { d: `M${PX + 62} ${PY + 26} L${PX + 70} ${PY + 26} L${PX + 72} ${PY + 42} L${PX + 60} ${PY + 42} Z`, fill: '#2a1a08' }, plateG);

/* the gate leaves (HTML, swung open in 3D) */
function leafSVG(mirror) {
  let s = `<svg viewBox="0 0 118 130"${mirror ? ' style="transform:scaleX(-1)"' : ''}><defs><linearGradient id="gB${mirror ? 'r' : 'l'}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d0a271"/><stop offset=".18" stop-color="#a87648"/><stop offset="1" stop-color="#5e3d25"/></linearGradient></defs>`;
  for (let i = 0; i < 5; i++) {
    const x0 = i * 23.6, x1 = x0 + 21.6, y0 = 18 * Math.pow(x0 / 118, 1.6), y1 = 18 * Math.pow(x1 / 118, 1.6);
    s += `<path d="M${x0} ${y0 + 4} Q${x0 + 10.8} ${y0 - 3} ${x1} ${y1 + 2} L${x1} 130 L${x0} 130 Z" fill="url(#gB${mirror ? 'r' : 'l'})"/>`;
    s += `<rect x="${x0 + 2}" y="${y0 + 8}" width="2" height="${118 - y0}" fill="#fff" opacity=".12"/>`;
  }
  s += '<rect x="0" y="32" width="118" height="11" fill="#4d311d"/><rect x="0" y="100" width="118" height="11" fill="#4d311d"/>';
  s += '<path d="M8 100 L110 43 L110 56 L22 104 Z" fill="#5a3a22"/>';
  s += '<rect x="-4" y="33" width="44" height="9" rx="3" fill="#e8c25a"/><rect x="-4" y="101" width="44" height="9" rx="3" fill="#e8c25a"/>';
  s += '<circle cx="2" cy="37.5" r="4" fill="#fff1bf"/><circle cx="2" cy="105.5" r="4" fill="#fff1bf"/>';
  s += '<rect x="100" y="64" width="18" height="10" rx="3" fill="#e8c25a"/><circle cx="104" cy="69" r="2.5" fill="#7a5520"/>';
  return s + '</svg>';
}
const glL = $('glL'), glR = $('glR');
glL.innerHTML = leafSVG(false); glR.innerHTML = leafSVG(true);
glL.style.left = POSTL[1] + 'px'; glR.style.left = (POSTR[0] - 118) + 'px';
glL.style.transformOrigin = '0% 50%'; glR.style.transformOrigin = '100% 50%';

/* the front layer: the path through the gate, the basket, the small mango's trip, the tick seal, the key */
const pathG = sv('g', {}, G.front);
const pathGlow = sv('path', { d: PATHD, fill: 'none', stroke: '#cbfb61', 'stroke-width': 18, 'stroke-linecap': 'round', opacity: 0, filter: 'url(#fBlur)' }, pathG);
const pathBase = sv('path', { d: PATHD, fill: 'none', stroke: 'rgba(255,255,255,.55)', 'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-dasharray': '1 17', opacity: 0 }, pathG);
const pathLit = sv('path', { d: PATHD, fill: 'none', stroke: '#cbfb61', 'stroke-width': 9, 'stroke-linecap': 'round', 'stroke-dasharray': '1 17', mask: 'url(#mPath)', opacity: 0 }, pathG);
$('mPathP').setAttribute('d', PATHD);
const PL = pathBase.getTotalLength();
const basketG = sv('g', {}, G.front);
sv('ellipse', { cx: BK.x + 6, cy: BK.by + 6, rx: 128, ry: 15, fill: '#000', opacity: .5, filter: 'url(#fBlur3)' }, basketG);
const bkHandleBack = sv('path', { d: `M ${BK.x - 98} ${BK.y} C ${BK.x - 96} ${BK.y - 112} ${BK.x + 96} ${BK.y - 112} ${BK.x + 98} ${BK.y}`, fill: 'none', stroke: '#9a6a30', 'stroke-width': 13, 'stroke-linecap': 'round' }, basketG);
sv('path', { d: `M ${BK.x - 98} ${BK.y} C ${BK.x - 96} ${BK.y - 112} ${BK.x + 96} ${BK.y - 112} ${BK.x + 98} ${BK.y}`, fill: 'none', stroke: '#f3cf86', 'stroke-width': 5, 'stroke-dasharray': '9 7', 'stroke-linecap': 'round', opacity: .8 }, basketG);
sv('ellipse', { cx: BK.x, cy: BK.y, rx: BK.rx, ry: BK.ry, fill: 'url(#gBasketIn)' }, basketG);
const inMango = mango(basketG, BK.x, BK.y - 4, MS[2], false);
inMango.g.setAttribute('opacity', 0);
const bodyD = `M ${BK.x - BK.rx} ${BK.y} C ${BK.x - BK.rx + 2} ${BK.y + 50} ${BK.x - BK.brx - 4} ${BK.by - 10} ${BK.x - BK.brx} ${BK.by} ` +
  `C ${BK.x - 40} ${BK.by + 12} ${BK.x + 40} ${BK.by + 12} ${BK.x + BK.brx} ${BK.by} C ${BK.x + BK.brx + 4} ${BK.by - 10} ${BK.x + BK.rx - 2} ${BK.y + 50} ${BK.x + BK.rx} ${BK.y} ` +
  `A ${BK.rx} ${BK.ry} 0 0 1 ${BK.x - BK.rx} ${BK.y} Z`;
sv('path', { d: bodyD, fill: 'url(#gStraw)' }, basketG);
const weave = sv('g', { 'clip-path': 'url(#cBasket)' }, basketG);
const cb = sv('clipPath', { id: 'cBasket' }, $('wback').querySelector('defs'));
sv('path', { d: bodyD }, cb);
for (let r = 0; r < 6; r++) {
  const y = BK.y + 14 + r * 15, w = BK.rx - (BK.rx - BK.brx) * (r / 6), sag = 22 - r * 2;
  sv('path', { d: `M ${BK.x - w - 10} ${y} Q ${BK.x} ${y + sag} ${BK.x + w + 10} ${y}`, fill: 'none', stroke: r % 2 ? '#b77a35' : '#e2b064', 'stroke-width': 11 }, weave);
  sv('path', { d: `M ${BK.x - w - 10} ${y} Q ${BK.x} ${y + sag} ${BK.x + w + 10} ${y}`, fill: 'none', stroke: r % 2 ? '#e9bf74' : '#9a6428', 'stroke-width': 11, 'stroke-dasharray': '13 13', 'stroke-dashoffset': r % 2 ? 0 : 13 }, weave);
}
sv('path', { d: bodyD, fill: 'url(#gStrawS)' }, basketG);
sv('path', { d: `M ${BK.x - BK.rx} ${BK.y} A ${BK.rx} ${BK.ry} 0 0 0 ${BK.x + BK.rx} ${BK.y}`, fill: 'none', stroke: '#f6d48e', 'stroke-width': 10, 'stroke-linecap': 'round' }, basketG);
sv('path', { d: `M ${BK.x - BK.rx} ${BK.y} A ${BK.rx} ${BK.ry} 0 0 0 ${BK.x + BK.rx} ${BK.y}`, fill: 'none', stroke: '#a8702e', 'stroke-width': 4, 'stroke-dasharray': '7 6' }, basketG);
sv('path', { d: `M ${BK.x - BK.rx} ${BK.y} A ${BK.rx} ${BK.ry} 0 0 1 ${BK.x + BK.rx} ${BK.y}`, fill: 'none', stroke: '#d9a95c', 'stroke-width': 7, opacity: .9 }, basketG);
const seal = sv('g', { opacity: 0 }, basketG);
sv('circle', { cx: 0, cy: 0, r: 40, fill: '#cbfb61', stroke: '#14190a', 'stroke-width': 3 }, seal);
sv('circle', { cx: 0, cy: 0, r: 31, fill: 'none', stroke: '#14190a', 'stroke-width': 2, 'stroke-dasharray': '4 4' }, seal);
sv('path', { d: 'M -16 1 L -5 13 L 18 -12', fill: 'none', stroke: '#14190a', 'stroke-width': 7, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, seal);
const flyG = sv('g', {}, G.front);                          // the small mango on its first trip (in front of everything)
const fly = mango(flyG, 0, 0, MS[2], false);
fly.ripe.setAttribute('opacity', 1); fly.raw.setAttribute('opacity', 0); fly.blush.setAttribute('opacity', .8);
const burstG = sv('g', { opacity: 0 }, G.front);         // the first pick: a soft lime burst
const burstC = sv('circle', { cx: MS[0], cy: MS[1], r: 30, fill: 'none', stroke: '#cbfb61', 'stroke-width': 5 }, burstG);
const burstS = [0, 1, 2, 3, 4, 5].map(i => sv('line', { stroke: '#e9ff9e', 'stroke-width': 4, 'stroke-linecap': 'round' }, burstG));
const keyG = sv('g', { opacity: 0 }, G.front);              // the key that turns in your name plate
sv('circle', { cx: 0, cy: 0, r: 15, fill: 'none', stroke: 'url(#gGoldH)', 'stroke-width': 8 }, keyG);
sv('rect', { x: 13, y: -4, width: 44, height: 8, rx: 3, fill: 'url(#gGoldH)' }, keyG);
sv('path', { d: 'M 44 4 l 0 10 l 6 0 l 0 -10 Z M 52 4 l 0 7 l 5 0 l 0 -7 Z', fill: '#e8c25a' }, keyG);
const hand = $('hand');

/* ---------- the camera ---------- */
const CAM = { hook: [887, 640, 1.3], tree: [1381, 554, .907], gift: [478, 560, .95], basket: [1400, 556, .9], key: [1586, 690, 1.6], turn: [1700, 505, .7] };
const CK = [[0, 'hook'], [S.tree[0] + .05, 'hook'], [S.tree[0] + 1.1, 'tree'], [S.gift[0] + .1, 'tree'], [S.gift[0] + 1.1, 'gift'],
  [S.basket[0] + .05, 'gift'], [S.basket[0] + 1.15, 'basket'], [C.w_dont - .1, 'basket'], [C.w_dont + .65, 'key'], [S.recap[0] + .05, 'key'],
  [S.recap[0] + 1.05, 'turn'], [1e9, 'turn']];
let CM = [0, 0, 1];
function camera(t) {
  let i = 0; while (i < CK.length - 2 && t >= CK[i + 1][0]) i++;
  const [t0, a] = CK[i], [t1, b] = CK[i + 1], k = a === b ? 0 : ez.inOut(lin(t, t0, t1));
  const A = CAM[a], B = CAM[b];
  const s = Math.exp(mix(Math.log(A[2]), Math.log(B[2]), k));            // zoom in log space, and keep the move smooth
  CM = [mix(A[0], B[0], k), mix(A[1], B[1], k), s];
  $('world').style.transform = `translate(${(960 - CM[0] * s).toFixed(2)}px,${(540 - CM[1] * s).toFixed(2)}px) scale(${s.toFixed(5)})`;
}
const w2s = (x, y) => [(x - CM[0]) * CM[2] + 960, (y - CM[1]) * CM[2] + 540];

/* ---------- leader lines (screen space, from a label to the part it names) ---------- */
const LEAD = $('lead'); const leads = {};
function leader(id, o, from, to, col) {
  let L = leads[id];
  if (!L) { L = leads[id] = [sv('path', { fill: 'none', 'stroke-width': 3, 'stroke-dasharray': '2 9', 'stroke-linecap': 'round' }, LEAD), sv('circle', { r: 7 }, LEAD), sv('circle', { r: 16, fill: 'none', 'stroke-width': 2 }, LEAD)]; }
  const [p, d, r] = L; const vis_ = o > .01;
  [p, d, r].forEach(e => e.style.display = vis_ ? '' : 'none'); if (!vis_) return;
  const mx = (from[0] + to[0]) / 2;
  sa(p, { d: `M ${from[0].toFixed(1)} ${from[1].toFixed(1)} C ${mx.toFixed(1)} ${from[1].toFixed(1)} ${mx.toFixed(1)} ${to[1].toFixed(1)} ${to[0].toFixed(1)} ${to[1].toFixed(1)}`, stroke: col, opacity: o });
  sa(d, { cx: to[0], cy: to[1], fill: col, opacity: o }); sa(r, { cx: to[0], cy: to[1], stroke: col, opacity: o * .55 });
}
function box(id) { const e = $(id); const x = parseFloat(e.style.left), y = parseFloat(e.style.top); return [x, y, e.offsetWidth, e.offsetHeight]; }
function place(id, x, y) { const e = $(id); e.style.left = x + 'px'; e.style.top = y + 'px'; }
// focus: the newest label is bright, older ones in the scene step back (darker, never see-through)
const dim = (t, later) => later.reduce((m, c) => m * (1 - .55 * ez.out(lin(t, c - .1, c + .3))), 1);
function foc(id, d) { $(id).style.filter = d > .995 ? 'none' : `brightness(${(.42 + .58 * d).toFixed(3)}) saturate(${(.55 + .45 * d).toFixed(3)})`; }

/* ---------- hook: the visitor's own question, the door becomes your backyard gate ---------- */
const QW = [...$('hkQ').children].filter(e => e.tagName === 'SPAN');
function hook(t) {
  const [a, b] = S.hook, e = b + .2;
  st($('hkQ'), vis(t, a, e, 0, .35));
  QW.forEach((w, i) => {
    const c = C.h_words[i], k = ez.out(lin(t, c - .04, c + .14));
    w.classList.toggle('lit', t >= c - .04);
    w.style.transform = `translateY(${(-10 * pulse(t, c - .04, .3)).toFixed(1)}px) scale(${(1 + .04 * pulse(t, c - .04, .3)).toFixed(3)})`;
  });
  st($('hkE'), vis(t, a, e, 0, .35));
  const dv = t < C.h_back - .15 ? 1 : 1 - ez.inOut(lin(t, C.h_back - .15, C.h_back + .25));
  st($('door'), dv * vis(t, a, e, 0, .3), 0, -30 * (1 - dv), 1 - .25 * (1 - dv));
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi; const d = pop(t, a + .05, b, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .3, b, 24), r = rise(t, a + .55, b, 30); st($('hwho'), h.o, 0, h.y); st($('httl'), r.o, 0, r.y);
}

/* ---------- the world, one function of t across every scene ---------- */
function world(t) {
  camera(t);
  const out = Math.max(vis(t, S.hi[0], S.hi[1], .35, .35), t > S.turn[1] - .3 ? lin(t, S.turn[1] - .3, S.turn[1]) : 0);
  const dimR = 1 - .9 * vis(t, S.recap[0] + .2, C.u_now + .25, .6, .55);           // the recap cards stand in front
  const wo = (1 - out) * dimR;
  $('world').style.opacity = wo.toFixed(3); $('world').style.visibility = wo < .002 || t < C.h_back - .3 ? 'hidden' : 'visible';
  const gb = C.h_back;                                     // the gate and the low fence arrive on "backyard"
  // ground and lawn
  const gk = ez.out(lin(t, gb - .1, gb + .5)); lawn.setAttribute('opacity', (gk * (.55 + .45 * ez.out(lin(t, S.tree[0], S.tree[0] + 1)))).toFixed(3));
  outside.setAttribute('opacity', gk.toFixed(3));
  yardGlow.setAttribute('opacity', (.9 * pulse(t, C.y_back - .1, 1.2)).toFixed(3));
  // pickets: near the gate on "backyard", the rest grow outward when the gate opens
  pickets.forEach(([g, x]) => {
    const d = Math.abs(x - GX), near = d < 330, c = near ? gb + d / 330 * .35 : C.g_open + (d - 330) / 900 * .9;
    const k = ez.back(lin(t, c, c + .35));
    g.setAttribute('transform', `translate(0 ${FB}) scale(1 ${Math.max(0, k).toFixed(3)}) translate(0 ${-FB})`);
    g.setAttribute('opacity', clamp(k * 3).toFixed(3));
  });
  railG.setAttribute('opacity', ez.out(lin(t, C.g_open, C.g_open + .8)).toFixed(3));
  postEls.forEach((g, i) => { const k = ez.back(lin(t, gb - .12 + i * .05, gb + .3)); g.setAttribute('transform', `translate(0 ${FB}) scale(1 ${Math.max(0, k).toFixed(3)}) translate(0 ${-FB})`); g.setAttribute('opacity', clamp(k * 3).toFixed(3)); });
  const bk = ez.out(lin(t, gb + .1, gb + .45)); beamG.setAttribute('opacity', bk.toFixed(3));
  const sk = ez.back(lin(t, gb + .15, gb + .6)); signG.setAttribute('opacity', clamp(sk * 2).toFixed(3));
  signG.setAttribute('transform', `translate(${GX} 510) scale(${(.6 + .4 * sk).toFixed(3)}) translate(${-GX} -510)`);
  signGlow.setAttribute('opacity', (.55 * Math.max(pulse(t, C.y_tag - .1, .9), pulse(t, C.r_broker - .1, 1.1))).toFixed(3));
  const pk = ez.out(lin(t, gb + .2, gb + .55)); plateG.setAttribute('opacity', pk.toFixed(3));
  plateGlow.setAttribute('opacity', (.85 * Math.max(vis(t, C.y_account - .1, S.tree[1] - .2, .3, .5) * (.75 + .25 * Math.sin(t * 4)), pulse(t, C.w_key, 1))).toFixed(3));
  // the gate leaves: closed in the hook, swung open in 3D as the tree scene starts
  const lk = ez.out(lin(t, gb - .05, gb + .4)), open = ez.inOut(lin(t, C.g_open + .05, C.g_open + 1.0));
  const ang = 84 * open - 4 * Math.sin(Math.PI * clamp((open - .85) / .15));
  [[glL, 1], [glR, -1]].forEach(([el, sg]) => {
    el.style.opacity = lk.toFixed(3); el.style.visibility = lk > .002 ? 'visible' : 'hidden';
    el.style.transform = `translateY(${(30 * (1 - lk)).toFixed(1)}px) rotateY(${(sg * ang).toFixed(2)}deg)`;
  });
  // the small mango, glowing behind the fence from the hook until it is picked
  const sm = ez.back(lin(t, gb + .3, gb + .8));
  small.ripe.setAttribute('opacity', 1); small.raw.setAttribute('opacity', 0); small.blush.setAttribute('opacity', .8);
  small.glow.setAttribute('opacity', (sm * (.75 + .25 * Math.sin(t * 3.2)) * (1 - lin(t, C.s_pick - .05, C.s_pick + .1))).toFixed(3));
  small.g.setAttribute('transform', `translate(${MS[0]} ${MS[1] + 3 * Math.sin(t * 1.7)}) scale(${(MS[2] * Math.max(0, sm)).toFixed(3)})`);
  small.g.setAttribute('opacity', (t < C.s_pick ? clamp(sm * 2) : 0).toFixed(3));
  // the tree draws in: trunk (bottom up), then the crown from the trunk top
  const tk = ez.inOut(lin(t, C.t_think + .1, C.t_fruit + .3));
  trunkG.setAttribute('transform', `translate(${TX} ${TB}) scale(${(.5 + .5 * tk).toFixed(3)} ${Math.max(.001, tk).toFixed(3)}) translate(${-TX} ${-TB})`);   // grows from its base
  treeG.setAttribute('opacity', (t > C.t_think ? 1 : 0).toFixed(3));
  const ck = ez.out(lin(t, C.t_fruit + .1, C.t_tree + .9));
  sa($('cCrownC'), { r: 620 * ck, cy: 430 - 60 * ck });
  blobEls.forEach(([e, x, y, r]) => { const d = Math.hypot(x - TX, y - 430) / 420, k = ez.back(lin(t, C.t_fruit + .05 + d * .55, C.t_fruit + .5 + d * .55));
    e.setAttribute('r', (r * Math.max(0, k)).toFixed(1)); });
  leafG.setAttribute('opacity', ez.out(lin(t, C.t_tree + .1, C.t_tree + .7)).toFixed(3));
  // trunk lights lime on "your own money" (and again when the promo asks you to keep it in)
  const lit = Math.max(vis(t, C.m_own - .1, S.tree[1] - .1, .35, .5), vis(t, C.e_own - .1, S.gift[1] - .1, .4, .5));
  trunkLit.setAttribute('opacity', (.32 * lit).toFixed(3)); trunkGlow.setAttribute('opacity', (.95 * lit).toFixed(3));
  // the mangoes ripen on "bears fruit" (two or three, never a laden tree); one is cupped, ready to pick
  ripe.forEach((m, i) => {
    const c = C.f_bears - .15 + i * .14, g = ez.back(lin(t, c, c + .5)), rk = ez.inOut(lin(t, c + .15, c + .9));
    const cup = i === 2 ? ez.out(lin(t, C.a_with - .05, C.a_with + .3)) * (t < S.gift[0] + .4 ? 1 : 1 - lin(t, S.gift[0] + .4, S.gift[0] + .9)) : 0;
    m.g.setAttribute('transform', `translate(${m.x} ${(m.y - 6 * cup).toFixed(1)}) scale(${(m.k * Math.max(0, .55 + .45 * g)).toFixed(3)})`);
    m.g.setAttribute('opacity', clamp(g * 3).toFixed(3));
    m.raw.setAttribute('opacity', (1 - rk).toFixed(3)); m.ripe.setAttribute('opacity', rk.toFixed(3)); m.blush.setAttribute('opacity', (.8 * rk).toFixed(3));
    const hl = Math.max(pulse(t, c + .4, .8), vis(t, C.k_where - .1, C.k_into, .3, .3), i === 2 ? .8 * cup : 0);
    m.glow.setAttribute('opacity', (.9 * hl).toFixed(3));
  });
  // the hand: reaches up and cups a ripe mango on "Profits can be withdrawn any time" (nothing is picked yet)
  const hv = vis(t, C.a_prof - .1, S.gift[0] + .9, .35, .4), hk = ez.out(lin(t, C.a_prof - .1, C.a_with));
  if (hv > .002) {
    const [mx, my] = [RIPE[2][0], RIPE[2][1]];
    hand.style.visibility = 'visible'; hand.style.opacity = hv.toFixed(3);
    hand.style.transform = `translate(${(mx - 64).toFixed(1)}px,${(my - 30 + 90 * (1 - hk)).toFixed(1)}px) rotate(${(-8 * (1 - hk)).toFixed(1)}deg)`;
  } else hand.style.visibility = 'hidden';
  // the gift branch, tied onto your tree with a lime ribbon; twelve month dots round the gift
  const gv = t >= C.g_gift - .2 ? 1 : 0; giftG.setAttribute('opacity', gv);
  const bl = ez.out(lin(t, C.g_gift - .15, C.g_gift + .45));
  sa(branchP, { 'stroke-dasharray': `${BRL * bl} ${BRL}` });
  bleaves.forEach((l, i) => l.setAttribute('opacity', ez.out(lin(t, C.g_gift + .1 + i * .06, C.g_gift + .4 + i * .06)).toFixed(3)));
  const gk2 = ez.back(lin(t, C.g_gift + .3, C.g_gift + .75));
  giftBox.setAttribute('transform', `translate(${GIFT.bx} ${GIFT.by}) rotate(${(6 * Math.sin(t * 2.2) * (1 - lin(t, C.g_gift + .3, C.g_gift + 2))).toFixed(2)}) scale(${Math.max(0, gk2).toFixed(3)}) translate(${-GIFT.bx} ${-GIFT.by})`);
  giftString.setAttribute('opacity', clamp(gk2 * 2).toFixed(3));
  const bw = ez.back(lin(t, C.g_tied - .05, C.g_tied + .4));
  bow.setAttribute('transform', `translate(678 513) scale(${Math.max(0, bw).toFixed(3)}) translate(-678 -513)`);
  ribbonGlow.setAttribute('opacity', (Math.max(vis(t, C.e_own - .1, S.gift[1] - .1, .4, .5) * (.8 + .2 * Math.sin(t * 4)), .7 * pulse(t, C.g_tied, .8))).toFixed(3));
  const rv = vis(t, C.g_tied, S.gift[1] + .2, .4, .5); ring.setAttribute('opacity', rv.toFixed(3));
  dots.forEach(([o, on], i) => { const c = mix(C.b_rel - .05, C.b_months, i / 11); on.setAttribute('opacity', ez.out(lin(t, c, c + .12)).toFixed(3));
    on.setAttribute('r', (9 * (1 + .45 * pulse(t, c, .3))).toFixed(2)); });
  const allLit = pulse(t, C.b_months + .05, .7); ring.setAttribute('transform', `translate(${GIFT.bx} ${GIFT.by + 33}) scale(${(1 + .06 * allLit).toFixed(3)}) translate(${-GIFT.bx} ${-GIFT.by - 33})`);
  // the basket outside the gate: appears on "Into your own basket", empty and waiting
  const bb = lin(t, C.k_into - .05, C.k_into + .55), bsy = ez.back(bb), bsx = .7 + .3 * ez.out(bb);
  basketG.setAttribute('opacity', clamp(bb * 4).toFixed(3));
  basketG.setAttribute('transform', `translate(${BK.x} ${BK.by}) scale(${bsx.toFixed(3)} ${Math.max(.05, bsy).toFixed(3)}) translate(${-BK.x} ${-BK.by})`);
  // the path: faint on "Withdrawals", lights up dotted to the basket on "arrive safely"
  const pf = vis(t, C.r_with - .1, S.small[1] - .3, .5, .4);
  pathBase.setAttribute('opacity', (.5 * pf).toFixed(3));
  const pk2 = ez.inOut(lin(t, C.r_arrive - .5, C.r_safely + .05));
  $('mPathP').setAttribute('stroke-dasharray', `${(PL * pk2).toFixed(1)} ${PL + 10}`);
  pathLit.setAttribute('opacity', (pf * (pk2 > 0 ? 1 : 0)).toFixed(3));
  pathGlow.setAttribute('opacity', (.35 * pf * pk2 * (1 + .3 * pulse(t, C.r_safely, .8))).toFixed(3));
  // the first trip: the small mango is picked on "Start small" and travels the path into the basket by "early"
  let fv = 0;
  if (t >= C.s_pick && t < C.s_land + .1) {
    fv = 1; const lift = ez.out(lin(t, C.s_pick, C.s_pick + .3));
    let x, y;
    const j0 = C.s_pick + .3, j1 = C.s_pick + .95, j2 = C.s_land - .3;
    const P0 = pathBase.getPointAtLength(PL * .4);
    if (t < j0) { x = MS[0]; y = MS[1] - 16 * lift; }
    else if (t < j1) { const k = ez.inOut(lin(t, j0, j1)), cx = MS[0] + 60, cy = MS[1] - 60;
      x = (1 - k) * (1 - k) * MS[0] + 2 * k * (1 - k) * cx + k * k * P0.x; y = (1 - k) * (1 - k) * (MS[1] - 16) + 2 * k * (1 - k) * cy + k * k * (P0.y - 26); }
    else if (t < j2) { const k = ez.inOut(lin(t, j1, j2)), p = pathBase.getPointAtLength(PL * mix(.4, 1, k)); x = p.x; y = p.y - 26; }
    else { const k = ez.inOut(lin(t, j2, C.s_land)), p = pathBase.getPointAtLength(PL); x = mix(p.x, BK.x, k); y = mix(p.y - 26, BK.y - 40, k); }
    fly.g.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(10 * Math.sin((t - C.s_pick) * 7)).toFixed(1)}) scale(${(MS[2] * (1 + .1 * lift)).toFixed(3)})`);
    fly.glow.setAttribute('opacity', '.9');
  }
  fly.g.setAttribute('opacity', fv); flyG.setAttribute('opacity', fv);
  const ink = ez.out(lin(t, C.s_land - .05, C.s_land + .3));
  inMango.g.setAttribute('opacity', (t >= C.s_land ? 1 : 0)); inMango.ripe.setAttribute('opacity', 1); inMango.raw.setAttribute('opacity', 0); inMango.blush.setAttribute('opacity', .8);
  inMango.glow.setAttribute('opacity', (.9 * (1 - .4 * lin(t, C.s_land + .3, C.s_land + 1.5))).toFixed(3));
  inMango.g.setAttribute('transform', `translate(${BK.x} ${(BK.y - 40 + 34 * ink).toFixed(1)}) scale(${MS[2]})`);
  const bk2 = lin(t, C.s_pick - .02, C.s_pick + .5);
  burstG.setAttribute('opacity', (t >= C.s_pick - .02 && bk2 < 1 ? 1 - ez.inOut(bk2) : 0).toFixed(3));
  burstC.setAttribute('r', (26 + 40 * ez.out(bk2)).toFixed(1));
  burstS.forEach((l, i) => { const a = i * Math.PI / 3 - Math.PI / 2, r0 = 36 + 30 * ez.out(bk2), r1 = r0 + 16;
    sa(l, { x1: MS[0] + r0 * Math.cos(a), y1: MS[1] - 14 + r0 * Math.sin(a), x2: MS[0] + r1 * Math.cos(a), y2: MS[1] - 14 + r1 * Math.sin(a) }); });
  // the tick seal stamps the basket on "prove"
  const sl = lin(t, C.p_prove - .12, C.p_prove + .3);
  seal.setAttribute('opacity', (t >= C.p_prove - .12 ? clamp(sl * 3) : 0).toFixed(3));
  seal.setAttribute('transform', `translate(${BK.x + 86} ${BK.y + 44}) scale(${(2.2 - 1.2 * ez.back(sl)).toFixed(3)}) rotate(${(-14 * (1 - ez.out(sl))).toFixed(1)})`);
  // the key turns in your own name plate on "Don't take my word for it"
  const ki = ez.out(lin(t, C.w_dont + .2, C.w_key - .05)), kt = ez.inOut(lin(t, C.w_key, C.w_key + .35));
  keyG.setAttribute('opacity', vis(t, C.w_dont + .2, S.small[1] + .2, .3, .4).toFixed(3));
  keyG.setAttribute('transform', `translate(${(PX + 66 + 70 * (1 - ki)).toFixed(1)} ${PY + 26}) rotate(${(180 - 90 * kt).toFixed(1)}) scale(.9) translate(-57 0)`);   // the tip in the keyhole, the bow turns
}

/* ---------- labels: the fruit tree ---------- */
function treeLabels(t) {
  const [a, b] = S.tree;
  place('Lplate', 1090, 616); place('Ltrunk', 168, 770); place('Lprofit', 1110, 168); place('Lany', 1110, 352);
  const d1 = dim(t, [C.m_own, C.f_bears, C.a_with]), d2 = dim(t, [C.f_bears, C.a_with]), d3 = dim(t, [C.a_with]);
  const p = rise(t, C.y_account - .1, b, 24); st($('Lplate'), p.o, 0, p.y); foc('Lplate', d1);
  const r = rise(t, C.m_own - .12, b, 24); st($('Ltrunk'), r.o, 0, r.y); foc('Ltrunk', d2);
  const f = rise(t, C.f_bears - .05, b, 24); st($('Lprofit'), f.o, 0, f.y); foc('Lprofit', d3);
  const n = pop(t, C.a_any - .12, b, .35, .3); st($('Lany'), n.o, 0, 0, n.s);
  const [px, py, pw, ph] = box('Lplate'); leader('plate', p.o * d1, [px, py + ph / 2 + p.y], w2s(PX + PW, PY + PH / 2), '#b39cff');
  const [tx_, ty_, tw] = box('Ltrunk'); leader('trunk', r.o * d2, [tx_ + tw / 2, ty_ + r.y], w2s(TX, 640), '#cbfb61');
  const [fx, fy, , fh] = box('Lprofit'); leader('profit', f.o * d3, [fx, fy + fh / 2 + f.y], w2s(RIPE[1][0] + 18, RIPE[1][1] - 20), '#ffe08f');
  const [nx, ny, , nh] = box('Lany'); leader('any', n.o, [nx, ny + nh / 2], w2s(RIPE[2][0] + 24, RIPE[2][1] + 10), '#ffe08f');
}

/* ---------- labels: the gift branch (the promo) ---------- */
function giftLabels(t) {
  const [a, b] = S.gift;
  place('Gq', 76, 150); place('Gtag', 66, 246); place('Grel', 66, 408); place('Gkeep', 66, 514); place('Gphone', 66, 684);
  const q = rise(t, C.g_promo - .15, C.g_tied + .2, 20); st($('Gq'), q.o, 0, q.y);
  const dT = dim(t, [C.e_own, C.c_check]), dK = dim(t, [C.c_check]);
  const g = rise(t, C.g_tied - .1, b, 24); st($('Gtag'), g.o, 0, g.y); foc('Gtag', dT);
  const r = pop(t, C.b_months - .05, b, .35, .3); st($('Grel'), r.o, 0, 0, r.s); foc('Grel', dT);
  const k = rise(t, C.e_own - .12, b, 24); st($('Gkeep'), k.o, 0, k.y); foc('Gkeep', dK);
  const ph = vis(t, C.c_check - .15, b, .45, .3); st($('Gphone'), ph, -120 * (1 - ez.out(lin(t, C.c_check - .15, C.c_check + .35))), 0);
  const [gx, gy, gw, gh] = box('Gtag'); leader('tag', g.o * dT, [gx + gw, gy + gh / 2 + g.y], w2s(GIFT.bx - GIFT.w / 2 + 6, GIFT.by + 20), '#cbfb61');
}

/* ---------- labels: into your basket, the way out (an illustration), the 48 hours ---------- */
function basketLabels(t) {
  const [a, b] = S.basket;
  place('Bbasket', 1296, 700); place('illus', 1560, 136); place('Bacct', 56, 748); place('Bwal', 1176, 296); place('Bsafe', 1316, 556);
  place('Bclock', 1176, 250); place('Bfees', 1086, 452);
  const route = C.n_jet - .1;                              // the route labels step aside for the 48 hours
  const k = rise(t, C.k_crypto - .12, C.r_with + .1, 20); st($('Bbasket'), k.o, 0, k.y);
  const il = vis(t, C.r_with - .1, C.w_dont + .1, .4, .35); st($('illus'), il);
  const ac = rise(t, C.r_with - .05, route + .4, 24, .4, .4); st($('Bacct'), ac.o, 0, ac.y);
  const wl = rise(t, C.r_address - .15, route + .4, 24, .4, .4); st($('Bwal'), wl.o, 0, wl.y);
  $('net1').classList.toggle('on', t >= C.r_network); $('net2').classList.toggle('on', t >= C.r_sides);
  $('net1').style.transform = `scale(${(1 + .12 * pulse(t, C.r_network, .4)).toFixed(3)})`; $('net2').style.transform = `scale(${(1 + .12 * pulse(t, C.r_sides, .4)).toFixed(3)})`;
  const sf = pop(t, C.r_safely - .1, route + .4, .35, .4); st($('Bsafe'), sf.o, 0, 0, sf.s);
  const cl = pop(t, C.n_48 - .12, b + .1, .4, .35); st($('Bclock'), cl.o, 0, 0, cl.s);
  const fe = rise(t, C.n_on - .05, b + .1, 20, .4, .35); st($('Bfees'), fe.o, 0, fe.y);
  const [kx, ky, , kh] = box('Bbasket'); leader('basket', k.o, [kx, ky + kh / 2 + k.y], w2s(BK.x + BK.rx - 8, BK.y + 20), '#ffe08f');
  const [wx, wy, ww, wh] = box('Bwal'); leader('wal', wl.o, [wx + 40, wy + wh + wl.y], w2s(BK.x + 30, BK.y - 30), '#ffe08f');
  const [ax, ay, aw] = box('Bacct'); leader('acct', ac.o, [ax + 260, ay + ac.y], w2s(TX + 20, TB + 2), '#b39cff');
}

/* ---------- labels: one small fruit first, the key, your own balance ---------- */
function smallLabels(t) {
  const [a, b] = S.small;
  place('Stest', 1110, 372); place('Sprove', 1012, 482); place('Ssee', 742, 420); place('adv', 1250, 210);
  const off = C.w_dont - .1;
  const ad = pop(t, C.s_advice - .12, off + .3, .35, .35); st($('adv'), ad.o, 0, 0, ad.s);
  const ts = pop(t, C.s_land - .05, off + .3, .35, .35); st($('Stest'), ts.o, 0, 0, ts.s); foc('Stest', dim(t, [C.p_prove]));
  const pr = rise(t, C.p_prove - .1, off + .3, 24, .35, .35); st($('Sprove'), pr.o, 0, pr.y);
  const ph = vis(t, C.l_log - .05, b, .15, .35), pk = ez.out(lin(t, C.l_log - .05, C.l_log + .6));
  $('phone').style.opacity = ph.toFixed(3); $('phone').style.visibility = ph > .002 ? 'visible' : 'hidden';
  $('phone').style.transform = `perspective(1600px) translateX(${(720 * (1 - pk)).toFixed(1)}px) rotateY(${(-18 + 12 * pk).toFixed(2)}deg)`;
  const se = pop(t, C.l_see - .12, b, .35, .35); st($('Ssee'), se.o, 0, 0, se.s);
}

/* ---------- recap: three cards, picture first, meaning under it; then they fold back into the tree ---------- */
function recap(t) {
  const [a, b] = S.recap, fold = C.u_now;
  const ti = rise(t, a + .25, fold + .25, 30, .45, .3); st($('rtt'), ti.o, 0, ti.y);
  const [tx_, ty_] = w2s(TX, 330);
  [['rc1', C.rc_pick - .25], ['rc2', C.rc_let - .25], ['rc3', C.rc_start - .25]].forEach(([id, c], i) => {
    const e = $(id), v = rise(t, c, b, 40, .45, .01), fk = ez.inOut(lin(t, fold - .05, fold + .55));
    const [x0, y0, w, h] = [parseFloat(getComputedStyle(e).left), 282, 520, 470];
    const dx = (tx_ - (x0 + w / 2)) * fk, dy = (ty_ - (y0 + h / 2)) * fk;
    const o = v.o * (1 - ez.inOut(lin(t, fold + .2, fold + .55)));
    e.style.opacity = o.toFixed(3); e.style.visibility = o > .002 ? 'visible' : 'hidden';
    e.style.transform = `perspective(1400px) translate(${dx.toFixed(1)}px,${(v.y + dy).toFixed(1)}px) rotateY(${(70 * fk).toFixed(1)}deg) scale(${(1 - .82 * fk).toFixed(3)})`;
    e.querySelector('.ok').style.transform = `scale(${(ez.back(lin(t, c + .3, c + .65))).toFixed(3)})`;
  });
}

/* ---------- now it's your turn: tap any Join JetUP button ---------- */
function turn(t) {
  const [a, b] = S.turn, tt = C.i_press;
  const h = rise(t, C.u_now + .3, b, 40); st($('ut'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, C.u_now + .3, C.u_now + .8)));
  const j = pop(t, C.u_turn - .12, b, .4, .3); const press = t > tt - .04 && t < tt + .16 ? .95 : 1;
  st($('ujoin'), j.o, 0, 0, j.s * press * (1 + .02 * Math.sin(t * 4)));
  const u = rise(t, C.i_url - .3, b, 30); st($('uurl'), u.o, 0, u.y, 1 + .04 * pulse(t, C.i_url, .6));
  const hk = ez.out(lin(t, C.i_join - .45, tt)), hv = vis(t, C.i_join - .45, b, .25, .3);
  st($('uhand'), hv, 260 * (1 - hk), 220 * (1 - hk) + (t > tt - .04 && t < tt + .16 ? 10 : 0));
  const rk = lin(t, tt, tt + .65); $('uring').style.opacity = (t >= tt && t <= tt + .65 ? .9 * (1 - rk) : 0).toFixed(3);
  $('uring').style.visibility = t >= tt && t <= tt + .65 ? 'visible' : 'hidden'; $('uring').style.transform = `scale(${(.4 + 1.6 * ez.out(rk)).toFixed(3)})`;
}

function scenes(t) {
  st($('top'), vis(t, 0, TL.T + 1, 0, 0));
  world(t); hook(t); hi(t); treeLabels(t); giftLabels(t); basketLabels(t); smallLabels(t); recap(t); turn(t);
}

/* ---------- captions: the current line, the spoken word lit ---------- */
const capbox = $('capbox'); let lastCap = null;
function captions(t) {
  const c = TL.caps.find(c => t >= c.a && t < c.b);
  if (!c || (TL.capoff && t >= TL.capoff)) { capbox.style.visibility = 'hidden'; lastCap = null; return; }
  if (c !== lastCap) { capbox.innerHTML = c.w.map(w => `<span>${w.w}</span>`).join(' '); lastCap = c; }
  const sp = capbox.children;
  c.w.forEach((w, i) => { const end = c.w[i + 1] ? c.w[i + 1].a : w.b + .25; sp[i].className = t >= w.a && t < end ? 'on' : t >= end ? '' : 'todo'; });
  capbox.style.visibility = 'visible'; capbox.style.opacity = Math.min(lin(t, c.a, c.a + .12), 1 - lin(t, c.b - .12, c.b)).toFixed(3);
}

/* ---------- emoji pops on key words, as in the sign-up training ---------- */
const emoEl = document.createElement('div'); emoEl.id = 'emo';
emoEl.style.cssText = 'position:absolute;left:0;top:0;width:96px;height:96px;font:84px/96px "Noto Color Emoji";text-align:center;visibility:hidden;transform-origin:100% 100%;z-index:60';
document.body.appendChild(emoEl);
function emojis(t) {
  const E = (TL.emos || []).filter(([t0]) => t >= t0 && t <= t0 + 2).pop();
  if (!E || capbox.style.visibility !== 'visible' || (TL.kit && t >= TL.kit[0])) { emoEl.style.visibility = 'hidden'; return; }
  const age = t - E[0]; if (emoEl.textContent !== E[1]) emoEl.textContent = E[1];
  const a = Math.min(1, age / .15) * Math.min(1, (2 - age) / .3), s = .4 + .6 * ez.back(clamp(age / .4)); const r = capbox.getBoundingClientRect();
  emoEl.style.left = (r.right + 6 - 96).toFixed(1) + 'px'; emoEl.style.top = (r.top - 96 - 14 - 8 * ez.out(clamp(age / 2))).toFixed(1) + 'px';
  emoEl.style.transform = `scale(${s.toFixed(3)})`; emoEl.style.opacity = a.toFixed(3); emoEl.style.visibility = 'visible';
}

/* QA helper: how many lines each caption takes (never more than two) */
window.capLines = function () {
  const out = []; const lh = parseFloat(getComputedStyle(capbox).lineHeight);
  capbox.style.visibility = 'hidden';
  TL.caps.forEach(c => { capbox.innerHTML = c.w.map(w => `<span>${w.w}</span>`).join(' '); const n = Math.round((capbox.clientHeight - 30) / lh); if (n > 2) out.push([c.a, n, c.w.map(w => w.w).join(' ')]); });
  lastCap = null; return out;
};
window.R = function (t) { scenes(t); captions(t); emojis(t); return Promise.all([...document.images].map(i => i.decode().catch(() => {}))); };
})();

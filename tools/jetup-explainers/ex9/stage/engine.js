/* JetUP explainer #9 ("What copying really means"), 16:9. Every visual is a pure function of time t.
   The picture: a community-hall cooking class, one illustration that persists and grows across the scenes, with a camera
   (translate + scale of #world) that frames one focal point at a time. The chef at the front is Sonic AI, the strategy (his
   hat badge); each stir is a trade. Your own enamel pot on your own table, with its lime name plate, is your own account (an
   MT5 account at TAG Markets, in your name); the ingredients in it are your money. Every other table has its own pot and its
   own name plate (names blurred): no shared pot. The lime CopyX line carries the chef's stir into your pot (and, fainter,
   into every other pot); your wooden spoon rests on its rest from "lift the spoon" on: you don't pick the trades. The glass
   lid is the MetaTrader 5 app: watch every trade, read only. Colours never change: the chef and his counter gold; your pot,
   its plate and the CopyX line lime; the lid clear glass. Never drawn: amounts or markings in any pot, a stir bigger or
   smaller than another (every stir arrow is the same size, in screen space), two pots side by side, a clock, a knob, flames,
   a finished dish, nonstop stirring (the chef stirs once, then rests). Labels live in screen space (never scaled).
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
const op = (e, o) => e.setAttribute('opacity', clamp(o).toFixed(3));
let seed = 9; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
function defsOf(el) {                   // a clipPath lives in its own svg's <defs>: one inside the hidden #world clips the hook's pot to nothing
  const svg = el.tagName.toLowerCase() === 'svg' ? el : el.ownerSVGElement;
  let d = svg.querySelector(':scope > defs');
  if (!d) { d = document.createElementNS(NS, 'defs'); svg.insertBefore(d, svg.firstChild); }
  return d;
}

/* ---------- gradients and filters (shared by every svg on the page: the world, the hook's pot, the recap's spoon) ---------- */
$('defs').innerHTML = `
 <linearGradient id="gWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#110a20"/><stop offset=".55" stop-color="#1d1330"/><stop offset="1" stop-color="#2b1c33"/></linearGradient>
 <linearGradient id="gWains" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2530"/><stop offset="1" stop-color="#1e121a"/></linearGradient>
 <linearGradient id="gFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a2f1d"/><stop offset=".35" stop-color="#3a2416"/><stop offset=".75" stop-color="#22150e"/><stop offset="1" stop-color="#0e0908"/></linearGradient>
 <radialGradient id="gPool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffcf87" stop-opacity=".30"/><stop offset=".6" stop-color="#ffb35c" stop-opacity=".10"/><stop offset="1" stop-color="#ffb35c" stop-opacity="0"/></radialGradient>
 <radialGradient id="gVig" cx=".5" cy=".42" r=".75"><stop offset=".55" stop-color="#05030a" stop-opacity="0"/><stop offset="1" stop-color="#05030a" stop-opacity=".75"/></radialGradient>
 <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#171338"/><stop offset=".6" stop-color="#33275e"/><stop offset="1" stop-color="#6d4672"/></linearGradient>
 <linearGradient id="gFrame" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1a14"/><stop offset=".5" stop-color="#4a3022"/><stop offset="1" stop-color="#24160f"/></linearGradient>
 <linearGradient id="gShade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8e6420"/><stop offset=".35" stop-color="#ffe08f"/><stop offset=".6" stop-color="#e8c25a"/><stop offset="1" stop-color="#7a5418"/></linearGradient>
 <radialGradient id="gBulb" cx=".5" cy=".3" r=".7"><stop offset="0" stop-color="#fffbe8"/><stop offset=".6" stop-color="#ffe3a0"/><stop offset="1" stop-color="#ffc35c"/></radialGradient>
 <radialGradient id="gLampGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd590" stop-opacity=".55"/><stop offset=".4" stop-color="#ffb55c" stop-opacity=".16"/><stop offset="1" stop-color="#ffb55c" stop-opacity="0"/></radialGradient>
 <linearGradient id="gCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd590" stop-opacity=".22"/><stop offset="1" stop-color="#ffd590" stop-opacity="0"/></linearGradient>
 <linearGradient id="gGoldH" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff4cc"/><stop offset=".4" stop-color="#ecc865"/><stop offset=".75" stop-color="#c39437"/><stop offset="1" stop-color="#8e6420"/></linearGradient>
 <linearGradient id="gGoldV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1bf"/><stop offset=".45" stop-color="#e8c25a"/><stop offset="1" stop-color="#a8792a"/></linearGradient>
 <linearGradient id="gCtrFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d2718"/><stop offset="1" stop-color="#1f130b"/></linearGradient>
 <linearGradient id="gCtrTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e3f27"/><stop offset="1" stop-color="#3b2516"/></linearGradient>
 <linearGradient id="gApron" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b98a35"/><stop offset=".3" stop-color="#ffe7a6"/><stop offset=".6" stop-color="#e8c25a"/><stop offset="1" stop-color="#9c7027"/></linearGradient>
 <linearGradient id="gShirt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#211a3d"/><stop offset=".4" stop-color="#3a3068"/><stop offset="1" stop-color="#1a1430"/></linearGradient>
 <radialGradient id="gSkin" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#c58a5c"/><stop offset=".6" stop-color="#94603a"/><stop offset="1" stop-color="#6a4126"/></radialGradient>
 <radialGradient id="gHat" cx=".38" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#eeeaf6"/><stop offset="1" stop-color="#c3bbd6"/></radialGradient>
 <linearGradient id="gHatBand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#cfc8de"/><stop offset=".35" stop-color="#ffffff"/><stop offset="1" stop-color="#bdb4d0"/></linearGradient>
 <linearGradient id="gTopW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b98654"/><stop offset="1" stop-color="#d9a873"/></linearGradient>
 <linearGradient id="gEdgeW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2b37c"/><stop offset=".25" stop-color="#a87445"/><stop offset="1" stop-color="#7a4f2b"/></linearGradient>
 <linearGradient id="gApronW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6e4628"/><stop offset="1" stop-color="#4b2f1a"/></linearGradient>
 <linearGradient id="gLeg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a2f1a"/><stop offset=".4" stop-color="#8d6140"/><stop offset="1" stop-color="#3a2414"/></linearGradient>
 <linearGradient id="gStoveTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9d4e4"/><stop offset="1" stop-color="#f4f1f8"/></linearGradient>
 <linearGradient id="gStoveFront" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cdc6da"/><stop offset=".2" stop-color="#9c94b0"/><stop offset="1" stop-color="#6c6482"/></linearGradient>
 <radialGradient id="gHotplate" cx=".45" cy=".4" r=".6"><stop offset="0" stop-color="#4a4752"/><stop offset=".7" stop-color="#25232b"/><stop offset="1" stop-color="#121116"/></radialGradient>
 <linearGradient id="gEnLime" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7fb024"/><stop offset=".14" stop-color="#d9ff8a"/><stop offset=".3" stop-color="#c4f25a"/><stop offset=".72" stop-color="#93c731"/><stop offset="1" stop-color="#557f12"/></linearGradient>
 <linearGradient id="gEnCream" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b9b0c4"/><stop offset=".14" stop-color="#ffffff"/><stop offset=".32" stop-color="#f4f0f8"/><stop offset=".75" stop-color="#cfc7dc"/><stop offset="1" stop-color="#8f86a3"/></linearGradient>
 <linearGradient id="gEnShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".6" stop-color="#000" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
 <radialGradient id="gInside" cx=".5" cy=".2" r=".9"><stop offset="0" stop-color="#2a1c14"/><stop offset="1" stop-color="#0d0806"/></radialGradient>
 <radialGradient id="gStew" cx=".42" cy=".38" r=".75"><stop offset="0" stop-color="#e99a48"/><stop offset=".6" stop-color="#c2652a"/><stop offset="1" stop-color="#8a3f18"/></radialGradient>
 <radialGradient id="gGlowLime"><stop offset="0" stop-color="#cbfb61" stop-opacity=".75"/><stop offset=".5" stop-color="#cbfb61" stop-opacity=".25"/><stop offset="1" stop-color="#cbfb61" stop-opacity="0"/></radialGradient>
 <radialGradient id="gGlowGold"><stop offset="0" stop-color="#ffe08f" stop-opacity=".75"/><stop offset=".45" stop-color="#e8c25a" stop-opacity=".28"/><stop offset="1" stop-color="#e8c25a" stop-opacity="0"/></radialGradient>
 <linearGradient id="gWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d39c"/><stop offset=".5" stop-color="#cf9a5c"/><stop offset="1" stop-color="#92602f"/></linearGradient>
 <linearGradient id="gRest" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#e9e3f2"/><stop offset="1" stop-color="#b3aac6"/></linearGradient>
 <linearGradient id="gSleeve" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a3f80"/><stop offset=".5" stop-color="#352c63"/><stop offset="1" stop-color="#1f1940"/></linearGradient>
 <linearGradient id="gHandSkin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c48a5d"/><stop offset=".55" stop-color="#9b6440"/><stop offset="1" stop-color="#6d4227"/></linearGradient>
 <linearGradient id="gLidGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".32"/><stop offset=".45" stop-color="#e8f0ff" stop-opacity=".08"/><stop offset="1" stop-color="#ffffff" stop-opacity=".18"/></linearGradient>
 <linearGradient id="gKnob" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a3550"/><stop offset=".45" stop-color="#8d86a6"/><stop offset="1" stop-color="#2a2540"/></linearGradient>
 <linearGradient id="gGlint" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
 <filter id="fBlur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="fBlur4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="fBlur2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>
 <filter id="fName" x="-25%" y="-90%" width="150%" height="280%"><feGaussianBlur stdDeviation="2.6"/></filter>
 <filter id="fSoft" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="#000" flood-opacity=".45"/></filter>`;

/* ---------- world coordinates (the wide shot at scale 1) ---------- */
const FY = 388;                                             // where the back wall meets the floor
const CTR = { x0: 676, x1: 1244, top: 334, front: 350, base: 444 };   // the chef's counter
const CHEF = { x: 936 };                                     // the chef, behind his counter
const CPOT = { x: 1056, y: 320, rx: 60, ry: 13 };            // the chef's pot: only its rim shows above the counter
const ROWS = [[498, 522, .6], [1422, 522, .6], [246, 662, .78], [1674, 662, .78]];   // every other table: x, front edge y, scale
const YT = { x: 960, y: 790, s: 1 };                         // your table, in front (wider and deeper: the spoon rests in front of the stove)

const G = { hall: $('wHall'), chef: $('wChef'), rows: $('wRows'), lines: $('wLines'), yours: $('wYours'), front: $('wFront') };

/* the hall: back wall, tall windows, two brass pendant lamps, the wainscot, the wooden floor */
const hall = sv('g', {}, G.hall);
sv('rect', { x: -1400, y: -700, width: 4720, height: FY + 700, fill: 'url(#gWall)' }, hall);
const winG = sv('g', {}, hall);
[[150, 1], [452, .95], [1468, .95], [1770, 1]].forEach(([x, k]) => {
  const w = 168 * k, top = -10, bot = 238;
  const arch = `M ${x - w / 2} ${bot} L ${x - w / 2} ${top + w / 2} A ${w / 2} ${w / 2} 0 0 1 ${x + w / 2} ${top + w / 2} L ${x + w / 2} ${bot} Z`;
  sv('path', { d: arch, fill: 'url(#gFrame)', transform: `translate(0 0) scale(1)`, stroke: '#1a100b', 'stroke-width': 14 }, winG);
  sv('path', { d: arch, fill: 'url(#gSky)' }, winG);
  for (let i = 0; i < 7; i++) sv('circle', { cx: x - w / 2 + 14 + rnd() * (w - 28), cy: top + 30 + rnd() * 120, r: .8 + rnd() * 1.4, fill: '#fff', opacity: .25 + rnd() * .5 }, winG);
  sv('rect', { x: x - 4, y: top + 6, width: 8, height: bot - top - 6, fill: '#2a1a12' }, winG);
  sv('rect', { x: x - w / 2, y: 120, width: w, height: 8, fill: '#2a1a12' }, winG);
  sv('rect', { x: x - w / 2 - 14, y: bot - 2, width: w + 28, height: 14, rx: 3, fill: '#4a3022' }, winG);
  sv('path', { d: arch, fill: 'none', stroke: 'rgba(255,214,150,.18)', 'stroke-width': 2 }, winG);
});
const wains = sv('g', {}, hall);
sv('rect', { x: -1400, y: FY - 96, width: 4720, height: 96, fill: 'url(#gWains)' }, wains);
for (let x = -1400; x < 3320; x += 120) sv('rect', { x: x + 12, y: FY - 84, width: 96, height: 72, rx: 4, fill: 'none', stroke: 'rgba(255,220,170,.10)', 'stroke-width': 2 }, wains);
sv('rect', { x: -1400, y: FY - 102, width: 4720, height: 8, fill: '#6b4a2c' }, wains);
sv('rect', { x: -1400, y: FY - 102, width: 4720, height: 2, fill: '#c8955a', opacity: .55 }, wains);
const floor = sv('g', {}, hall);
sv('rect', { x: -1400, y: FY, width: 4720, height: 1400, fill: 'url(#gFloor)' }, floor);
const VP = [960, 120];
for (let i = -40; i <= 40; i++) {                            // plank joints run to the vanishing point
  const xb = 960 + i * 118, k = (FY - VP[1]) / (1500 - VP[1]);
  sv('line', { x1: VP[0] + (xb - VP[0]) * k, y1: FY, x2: xb, y2: 1500, stroke: '#000', 'stroke-opacity': .28, 'stroke-width': 2 }, floor);
}
for (let j = 0; j < 14; j++) {                              // board ends: a butt joint straight across one plank, from joint line to
  const y = FY + 14 + Math.pow(j / 13, 1.7) * 1000, k = (y - VP[1]) / (1500 - VP[1]);   // joint line, closer together towards the back
  for (let i = -40; i < 40; i++) {
    if ((((i * 7 + j * 3) % 5) + 5) % 5) continue;           // one plank in five, staggered from row to row
    sv('line', { x1: VP[0] + (960 + i * 118 - VP[0]) * k, y1: y, x2: VP[0] + (960 + (i + 1) * 118 - VP[0]) * k, y2: y, stroke: '#000', 'stroke-opacity': .22, 'stroke-width': 1.4 + j * .08 }, floor);
  }
}
const pools = sv('g', {}, floor);                            // warm light pools under the lamps
sv('ellipse', { cx: 960, cy: 560, rx: 900, ry: 260, fill: 'url(#gPool)' }, pools);
sv('ellipse', { cx: 960, cy: 820, rx: 620, ry: 170, fill: 'url(#gPool)' }, pools);
const lamps = [];
[[672, 82], [1248, 82]].forEach(([x, y]) => {                // brass pendant lamps: cord, dome shade, bulb, warm glow (a little cord shows above
  // each shade in the wide shot)
  const g = sv('g', {}, hall);
  const glow = sv('ellipse', { cx: x, cy: y + 30, rx: 230, ry: 190, fill: 'url(#gLampGlow)' }, g);
  const cone = sv('path', { d: `M ${x - 52} ${y + 6} L ${x - 270} ${FY + 40} L ${x + 270} ${FY + 40} L ${x + 52} ${y + 6} Z`, fill: 'url(#gCone)', opacity: .6 }, g);
  sv('line', { x1: x, y1: -700, x2: x, y2: y - 46, stroke: '#0b0710', 'stroke-width': 3 }, g);
  sv('path', { d: `M ${x - 10} ${y - 48} L ${x + 10} ${y - 48} L ${x + 12} ${y - 36} L ${x - 12} ${y - 36} Z`, fill: '#8e6420' }, g);
  const bulb = sv('ellipse', { cx: x, cy: y + 2, rx: 26, ry: 14, fill: 'url(#gBulb)' }, g);
  sv('path', { d: `M ${x - 62} ${y + 4} C ${x - 58} ${y - 36} ${x - 30} ${y - 42} ${x} ${y - 42} C ${x + 30} ${y - 42} ${x + 58} ${y - 36} ${x + 62} ${y + 4} Z`, fill: 'url(#gShade)' }, g);
  sv('path', { d: `M ${x - 62} ${y + 4} Q ${x} ${y + 14} ${x + 62} ${y + 4}`, fill: 'none', stroke: '#fff1bf', 'stroke-width': 2.5, opacity: .8 }, g);
  lamps.push({ g, glow, cone, bulb });
});
const vig = sv('rect', { x: -1400, y: -700, width: 4720, height: 2300, fill: 'url(#gVig)', 'pointer-events': 'none' }, G.front);

/* the chef at the front: plain apron, white hat with a badge; his counter (gold trim); his pot behind it, only its rim */
const chefG = sv('g', {}, G.chef);
const ctrGlow = sv('ellipse', { cx: 960, cy: 300, rx: 430, ry: 190, fill: 'url(#gGlowGold)', opacity: 0 }, chefG);
const chefBody = sv('g', {}, chefG);
const X = CHEF.x;
// torso (dark shirt), apron bib and straps, neck, head (no face: simple and dignified), the hat with its badge
sv('path', { d: `M ${X - 104} ${CTR.top + 4} C ${X - 106} 300 ${X - 96} 276 ${X - 58} 266 L ${X + 58} 266 C ${X + 96} 276 ${X + 106} 300 ${X + 104} ${CTR.top + 4} Z`, fill: 'url(#gShirt)' }, chefBody);
sv('path', { d: `M ${X - 46} 282 L ${X + 46} 282 L ${X + 62} ${CTR.top + 4} L ${X - 62} ${CTR.top + 4} Z`, fill: 'url(#gApron)' }, chefBody);
sv('path', { d: `M ${X - 46} 282 L ${X + 46} 282`, stroke: '#fff4cc', 'stroke-width': 2.5, opacity: .8 }, chefBody);
sv('path', { d: `M ${X - 42} 284 C ${X - 34} 262 ${X - 22} 252 ${X - 14} 250 M ${X + 42} 284 C ${X + 34} 262 ${X + 22} 252 ${X + 14} 250`, fill: 'none', stroke: '#e8c25a', 'stroke-width': 6, 'stroke-linecap': 'round' }, chefBody);
sv('rect', { x: X - 26, y: 304, width: 52, height: 26, rx: 6, fill: 'none', stroke: 'rgba(120,80,20,.45)', 'stroke-width': 2.5 }, chefBody);   // the apron's pocket
sv('path', { d: `M ${X - 15} 236 L ${X + 15} 236 L ${X + 17} 262 L ${X - 17} 262 Z`, fill: '#7a4a2c' }, chefBody);
const head = sv('g', {}, chefBody);
sv('ellipse', { cx: X, cy: 206, rx: 33, ry: 39, fill: 'url(#gSkin)' }, head);
sv('ellipse', { cx: X - 31, cy: 210, rx: 6, ry: 10, fill: '#7a4a2c' }, head);
sv('ellipse', { cx: X + 31, cy: 210, rx: 6, ry: 10, fill: '#6a4126' }, head);
sv('path', { d: `M ${X - 30} 196 C ${X - 30} 230 ${X - 12} 246 ${X} 246 C ${X + 12} 246 ${X + 30} 230 ${X + 30} 196`, fill: 'none', stroke: '#5a361f', 'stroke-width': 2, opacity: .35 }, head);
const hat = sv('g', {}, chefBody);
[[-30, 132, 30], [30, 132, 30], [-14, 116, 32], [16, 114, 32], [0, 140, 36]].forEach(([dx, y, r]) => sv('circle', { cx: X + dx, cy: y, r, fill: 'url(#gHat)' }, hat));
sv('path', { d: `M ${X - 40} 150 C ${X - 30} 160 ${X + 30} 160 ${X + 40} 150 L ${X + 38} 180 C ${X + 20} 186 ${X - 20} 186 ${X - 38} 180 Z`, fill: 'url(#gHatBand)' }, hat);
sv('path', { d: `M ${X - 38} 178 C ${X - 20} 184 ${X + 20} 184 ${X + 38} 178`, fill: 'none', stroke: '#a59cbc', 'stroke-width': 2 }, hat);
const badgeGlow = sv('circle', { cx: X, cy: 166, r: 34, fill: 'url(#gGlowGold)', opacity: 0 }, hat);
const BADGE = [X, 166];
sv('path', { d: `M ${X} 154 L ${X + 11} 159 L ${X + 10} 170 Q ${X} 180 ${X} 180 Q ${X} 180 ${X - 10} 170 L ${X - 11} 159 Z`, fill: 'url(#gGoldH)', stroke: '#8e6420', 'stroke-width': 1.5 }, hat);
sv('path', { d: `M ${X} 160 l 2.6 5.2 5.6 .8 -4 4 1 5.6 -5.2 -2.8 -5.2 2.8 1 -5.6 -4 -4 5.6 -.8 Z`, fill: '#fff8de', opacity: .9 }, hat);
// his right arm rests on the counter's edge; his left hand holds his wooden spoon in his pot
sv('path', { d: `M ${X - 90} 288 C ${X - 126} 304 ${X - 130} 324 ${X - 108} ${CTR.top - 2}`, fill: 'none', stroke: '#2b2350', 'stroke-width': 30, 'stroke-linecap': 'round' }, chefBody);
sv('ellipse', { cx: X - 96, cy: CTR.top - 3, rx: 19, ry: 10, fill: 'url(#gSkin)' }, chefBody);
// his pot behind the counter: only the rim (and a sliver of the gold pot) shows above it
const cpG = sv('g', {}, chefG);
sv('path', { d: `M ${CPOT.x - CPOT.rx} ${CPOT.y} L ${CPOT.x - CPOT.rx + 2} ${CTR.top + 2} L ${CPOT.x + CPOT.rx - 2} ${CTR.top + 2} L ${CPOT.x + CPOT.rx} ${CPOT.y} Z`, fill: 'url(#gApron)' }, cpG);
sv('ellipse', { cx: CPOT.x, cy: CPOT.y, rx: CPOT.rx + 4, ry: CPOT.ry + 3, fill: '#8e6420' }, cpG);
sv('ellipse', { cx: CPOT.x, cy: CPOT.y, rx: CPOT.rx, ry: CPOT.ry, fill: 'url(#gInside)' }, cpG);
sv('ellipse', { cx: CPOT.x, cy: CPOT.y + 2, rx: CPOT.rx * .82, ry: CPOT.ry * .62, fill: 'url(#gStew)', opacity: .9 }, cpG);
sv('ellipse', { cx: CPOT.x, cy: CPOT.y, rx: CPOT.rx + 4, ry: CPOT.ry + 3, fill: 'none', stroke: 'url(#gGoldH)', 'stroke-width': 4 }, cpG);
const chefFront = sv('g', {}, chefG);                      // his left arm, his spoon and his hand: in front of his pot's far rim
const chefSpoon = sv('line', { stroke: 'url(#gWood)', 'stroke-width': 9, 'stroke-linecap': 'round' }, chefFront);
const chefArm = sv('path', { fill: 'none', stroke: '#2b2350', 'stroke-width': 28, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, chefFront);
const chefHand = sv('ellipse', { rx: 15, ry: 13, fill: 'url(#gSkin)' }, chefFront);
// the counter (in front of him and his pot)
const ctr = sv('g', {}, chefG);
sv('ellipse', { cx: 960, cy: CTR.base + 6, rx: 330, ry: 16, fill: '#000', opacity: .4, filter: 'url(#fBlur4)' }, ctr);
sv('rect', { x: CTR.x0 + 10, y: CTR.front, width: CTR.x1 - CTR.x0 - 20, height: CTR.base - CTR.front, fill: 'url(#gCtrFront)' }, ctr);
for (let x = CTR.x0 + 30; x < CTR.x1 - 20; x += 46) sv('rect', { x, y: CTR.front + 8, width: 3, height: CTR.base - CTR.front - 14, fill: '#000', opacity: .28 }, ctr);
sv('rect', { x: CTR.x0 + 10, y: CTR.base - 10, width: CTR.x1 - CTR.x0 - 20, height: 10, fill: 'url(#gGoldV)', opacity: .8 }, ctr);
const ctrTrim = sv('rect', { x: CTR.x0, y: CTR.top, width: CTR.x1 - CTR.x0, height: CTR.front - CTR.top, rx: 4, fill: 'url(#gGoldH)' }, ctr);
sv('rect', { x: CTR.x0, y: CTR.top, width: CTR.x1 - CTR.x0, height: 3, fill: '#fff4cc', opacity: .85 }, ctr);
sv('rect', { x: CTR.x0 + 10, y: CTR.front, width: CTR.x1 - CTR.x0 - 20, height: 6, fill: '#000', opacity: .35 }, ctr);

/* a table: wooden top, apron, legs, a two-plate stove (no knobs, nothing glowing), an enamel pot on the left plate */
function drawPot(parent, bx, by, s, kind) {
  const g = sv('g', {}, parent), rx = 84 * s, ry = 24 * s, H = 112 * s, y0 = by - H;
  const body = `M ${bx - rx} ${y0} L ${bx - rx * .97} ${by - ry * .7} A ${rx * .97} ${ry * 1.05} 0 0 0 ${bx + rx * .97} ${by - ry * .7} L ${bx + rx} ${y0} Z`;
  const enamel = kind === 'mine' ? 'url(#gEnLime)' : 'url(#gEnCream)', rimC = kind === 'mine' ? '#5d8a19' : '#5b4b9a';
  sv('ellipse', { cx: bx + 6 * s, cy: by + 2 * s, rx: rx * 1.02, ry: ry * .9, fill: '#000', opacity: .45, filter: 'url(#fBlur4)' }, g);
  [[-1, 1], [1, 1]].forEach(([sg]) => sv('path', { d: `M ${bx + sg * rx * .98} ${y0 + 16 * s} C ${bx + sg * (rx + 26 * s)} ${y0 + 12 * s} ${bx + sg * (rx + 28 * s)} ${y0 + 34 * s} ${bx + sg * rx * .99} ${y0 + 34 * s}`, fill: 'none', stroke: rimC, 'stroke-width': 7 * s, 'stroke-linecap': 'round' }, g));
  sv('path', { d: body, fill: enamel }, g);
  sv('path', { d: body, fill: 'url(#gEnShade)' }, g);
  sv('path', { d: `M ${bx - rx * .62} ${y0 + 12 * s} L ${bx - rx * .6} ${by - ry * 1.1}`, stroke: '#fff', 'stroke-opacity': .55, 'stroke-width': 7 * s, 'stroke-linecap': 'round' }, g);
  sv('path', { d: `M ${bx - rx * .47} ${y0 + 16 * s} L ${bx - rx * .46} ${y0 + 46 * s}`, stroke: '#fff', 'stroke-opacity': .35, 'stroke-width': 3 * s, 'stroke-linecap': 'round' }, g);
  sv('path', { d: `M ${bx - rx * .97} ${by - ry * .7} A ${rx * .97} ${ry * 1.05} 0 0 0 ${bx + rx * .97} ${by - ry * .7}`, fill: 'none', stroke: rimC, 'stroke-width': 3 * s, opacity: .7 }, g);
  sv('ellipse', { cx: bx, cy: y0, rx: rx + 2 * s, ry: ry + 2 * s, fill: rimC }, g);                    // the rolled rim
  sv('ellipse', { cx: bx, cy: y0 + 1 * s, rx: rx - 3 * s, ry: ry - 2.5 * s, fill: 'url(#gInside)' }, g);
  const sc = [bx, y0 + 6 * s], srx = rx * .84, sry = ry * .7;                                         // the stew's surface (no level marks)
  const stew = sv('g', {}, g);
  sv('ellipse', { cx: sc[0], cy: sc[1], rx: srx, ry: sry, fill: 'url(#gStew)' }, stew);
  const cid = 'cS' + Math.round(bx) + '_' + Math.round(by); const cp = sv('clipPath', { id: cid }, defsOf(parent));
  sv('ellipse', { cx: sc[0], cy: sc[1], rx: srx, ry: sry }, cp);
  const chunks = sv('g', { 'clip-path': `url(#${cid})` }, stew);
  const swirl = sv('g', {}, chunks);                         // everything that turns when the pot stirs
  let s2 = Math.round(bx * 7 + by) % 2147483646 + 1; const r2 = () => (s2 = (s2 * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 16; i++) {
    const a = r2() * Math.PI * 2, rr = Math.sqrt(r2()) * .85, x = Math.cos(a) * rr * srx, y = Math.sin(a) * rr * sry;
    const col = ['#ff9b3d', '#ffb347', '#86c443', '#f1d08a', '#e2763a'][i % 5], w = (i % 5 === 2 ? 6 : 9) * s;
    sv('ellipse', { cx: x, cy: y, rx: w, ry: w * .55, fill: col, opacity: .95, transform: `rotate(${(r2() * 60 - 30).toFixed(0)} ${x.toFixed(1)} ${y.toFixed(1)})` }, swirl);
  }
  const swirlLine = sv('path', { d: `M ${-srx * .7} 0 A ${srx * .7} ${sry * .7} 0 0 1 ${srx * .5} ${-sry * .3} M ${srx * .62} ${sry * .2} A ${srx * .55} ${sry * .55} 0 0 1 ${-srx * .3} ${sry * .45}`, fill: 'none', stroke: kind === 'mine' ? '#eaffb0' : '#ffe2b8', 'stroke-width': 3.5 * s, 'stroke-linecap': 'round', opacity: 0 }, swirl);
  sv('ellipse', { cx: sc[0] - srx * .25, cy: sc[1] - sry * .3, rx: srx * .45, ry: sry * .3, fill: '#fff', opacity: .12 }, stew);
  const glow = sv('ellipse', { cx: sc[0], cy: sc[1], rx: srx * 1.05, ry: sry * 1.15, fill: '#cbfb61', opacity: 0 }, g);
  const ring = sv('ellipse', { cx: sc[0], cy: sc[1], rx: srx * .4, ry: sry * .4, fill: 'none', stroke: kind === 'mine' ? '#eaffb0' : '#fff1d6', 'stroke-width': 2.5 * s, opacity: 0 }, g);
  sv('path', { d: `M ${bx - rx - 2 * s} ${y0} A ${rx + 2 * s} ${ry + 2 * s} 0 0 0 ${bx + rx + 2 * s} ${y0}`, fill: 'none', stroke: kind === 'mine' ? '#e6ff9c' : '#8f80c8', 'stroke-width': 2 * s, opacity: .8 }, g);
  return { g, swirl, swirlLine, glow, ring, sc, srx, sry, bx, by, y0, rx, ry, s };
}
function setSwirl(p, ang, k) {          // the pot's contents turn (one stir = one turn), seen in the plane of the surface
  sa(p.swirl, { transform: `translate(${p.sc[0]} ${p.sc[1]}) scale(1 ${(p.sry / p.srx).toFixed(4)}) rotate(${ang.toFixed(2)}) scale(1 ${(p.srx / p.sry).toFixed(4)})` });
  op(p.swirlLine, k);
}
function drawTable(parent, cx, cy, s, mine) {
  const g = sv('g', {}, parent), W = (mine ? 560 : 470) * s, Wb = (mine ? 508 : 432) * s, Dp = (mine ? 128 : 78) * s;
  sv('ellipse', { cx, cy: cy + 162 * s, rx: W * .56, ry: 20 * s, fill: '#000', opacity: .45, filter: 'url(#fBlur4)' }, g);
  [[cx - Wb / 2 + 22 * s], [cx + Wb / 2 - 44 * s]].forEach(([x]) => sv('rect', { x, y: cy + 10 * s, width: 20 * s, height: 128 * s, fill: '#3a2414' }, g));   // back legs
  [[cx - W / 2 + 18 * s], [cx + W / 2 - 44 * s]].forEach(([x]) => sv('rect', { x, y: cy + 14 * s, width: 26 * s, height: 148 * s, rx: 3 * s, fill: 'url(#gLeg)' }, g));
  sv('rect', { x: cx - W / 2 + 14 * s, y: cy + 14 * s, width: W - 28 * s, height: 46 * s, fill: 'url(#gApronW)' }, g);
  sv('rect', { x: cx - W / 2 + 14 * s, y: cy + 14 * s, width: W - 28 * s, height: 5 * s, fill: '#000', opacity: .3 }, g);
  sv('path', { d: `M ${cx - Wb / 2} ${cy - Dp} L ${cx + Wb / 2} ${cy - Dp} L ${cx + W / 2} ${cy} L ${cx - W / 2} ${cy} Z`, fill: 'url(#gTopW)' }, g);
  sv('rect', { x: cx - W / 2, y: cy, width: W, height: 16 * s, rx: 3 * s, fill: 'url(#gEdgeW)' }, g);
  for (let i = 1; i < 5; i++) { const k = i / 5; sv('line', { x1: cx - Wb / 2 + Wb * k, y1: cy - Dp, x2: cx - W / 2 + W * k, y2: cy, stroke: '#7a4f2b', 'stroke-opacity': .3, 'stroke-width': 1.5 * s }, g); }
  // the two-plate stove (a low box; no knobs, no flames)
  const sx0 = cx + (mine ? -190 : -200) * s, sx1 = cx + (mine ? 150 : 112) * s, sy0 = cy - (mine ? 106 : 64) * s, sy1 = cy - (mine ? 58 : 18) * s, sk = 10 * s;
  sv('path', { d: `M ${sx0 + sk} ${sy0} L ${sx1 - sk} ${sy0} L ${sx1} ${sy1} L ${sx0} ${sy1} Z`, fill: 'url(#gStoveTop)' }, g);
  sv('rect', { x: sx0, y: sy1, width: sx1 - sx0, height: 14 * s, rx: 2 * s, fill: 'url(#gStoveFront)' }, g);
  sv('ellipse', { cx: (sx0 + sx1) / 2, cy: sy1 + 16 * s, rx: (sx1 - sx0) * .52, ry: 5 * s, fill: '#000', opacity: .3, filter: 'url(#fBlur2)' }, g);
  const plates = mine ? [[cx - 100 * s, cy - 83 * s], [cx + 58 * s, cy - 83 * s]] : [[cx - 112 * s, cy - 41 * s], [cx + 26 * s, cy - 41 * s]];
  plates.forEach(([x, y]) => { sv('ellipse', { cx: x, cy: y, rx: 60 * s, ry: 15 * s, fill: '#1b1a20' }, g); sv('ellipse', { cx: x, cy: y - 1 * s, rx: 54 * s, ry: 12.5 * s, fill: 'url(#gHotplate)' }, g);
    sv('ellipse', { cx: x, cy: y - 1 * s, rx: 36 * s, ry: 8.4 * s, fill: 'none', stroke: '#5b5866', 'stroke-width': 1.4 * s, opacity: .6 }, g); });
  const pot = drawPot(g, plates[0][0], plates[0][1] + 2 * s, s, mine ? 'mine' : 'other');
  let plate = null;
  if (!mine) {                                                // its own name plate, the name blurred
    plate = sv('g', {}, g);
    sv('rect', { x: cx - 78 * s, y: cy + 19 * s, width: 156 * s, height: 36 * s, rx: 7 * s, fill: '#efeaf8' }, plate);
    sv('rect', { x: cx - 78 * s, y: cy + 19 * s, width: 156 * s, height: 36 * s, rx: 7 * s, fill: 'none', stroke: '#8f84ad', 'stroke-width': 2 * s }, plate);
    // two soft name strokes, as filled shapes: a stroked line has a zero-height box, so its blur filter drew nothing
    const nm = sv('g', { opacity: .8, filter: 'url(#fName)' }, plate);
    [[-60, 56], [-2, 62]].forEach(([x, w]) => sv('rect', { x: cx + x * s, y: cy + 31 * s, width: w * s, height: 12 * s, rx: 6 * s, fill: '#3b3356' }, nm));
  }
  return { g, pot, plate, cx, cy, s };
}
const rowT = ROWS.map(([x, y, s]) => drawTable(G.rows, x, y, s, false));

/* the CopyX lines: from the chef's pot into yours (lime), and fainter into every other table's own pot */
const lineG = sv('g', {}, G.lines);
const yt = drawTable(G.yours, YT.x, YT.y, YT.s, true);
const YP = yt.pot;
const LSRC = [CPOT.x, CPOT.y + 1];
function flowPath(a, b, front) {        // out of the chef's pot, down over his counter, then into the other pot from above
  // a front-row pot's line arcs over the back row and pours into its own pot from above (never through another member's pot); the
  // longer left-hand arc rides higher (24 px over its back-row pot), the right-hand one lower (17 px over its back-row pot and 17 px
  // under the "Sonic AI's trades" label, never touching it)
  const hi = b[0] < a[0];
  const c1 = front ? [a[0] + (b[0] - a[0]) * (hi ? .35 : .4), a[1] + (hi ? 40 : 70)] : [a[0] + (b[0] - a[0]) * .12, a[1] + 120],
        c2 = front ? [b[0] + (a[0] - b[0]) * .08, b[1] - (hi ? 230 : 190)] : [b[0] + (a[0] - b[0]) * .3, b[1] - 110];
  return `M ${a[0]} ${a[1]} C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${b[0].toFixed(1)} ${b[1].toFixed(1)}`;
}
const mainD = `M ${LSRC[0]} ${LSRC[1]} C ${LSRC[0] + 40} ${LSRC[1] + 150} ${YP.sc[0] + 150} ${YP.sc[1] - 160} ${YP.sc[0] + 6} ${YP.sc[1] - 4}`;
const mainGlow = sv('path', { d: mainD, fill: 'none', stroke: '#cbfb61', 'stroke-width': 22, 'stroke-linecap': 'round', opacity: 0, filter: 'url(#fBlur)' }, lineG);
const mainLine = sv('path', { d: mainD, fill: 'none', stroke: '#cbfb61', 'stroke-width': 7, 'stroke-linecap': 'round', opacity: 0 }, lineG);
const ML = mainLine.getTotalLength();
const faint = rowT.map(r => {
  const p = sv('path', { d: flowPath(LSRC, [r.pot.sc[0], r.pot.sc[1] - 2], r.s > .7), fill: 'none', stroke: '#cbfb61', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: 0 }, lineG);
  return { p, L: p.getTotalLength(), r };
});
const srcGlow = sv('ellipse', { cx: CPOT.x, cy: CPOT.y, rx: 74, ry: 24, fill: 'url(#gGlowLime)', opacity: 0 }, lineG);

/* your table: the lime pot, the spoon rest in front of the stove, your wooden spoon (and your hand), the glass lid */
const RX = YT.x - 116, RY = YT.y - 22;                       // the spoon rest
const restG = sv('g', {}, G.yours);
sv('ellipse', { cx: RX + 4, cy: RY + 7, rx: 48, ry: 10, fill: '#000', opacity: .4, filter: 'url(#fBlur2)' }, restG);
sv('path', { d: `M ${RX - 46} ${RY - 4} C ${RX - 46} ${RY + 10} ${RX + 46} ${RY + 10} ${RX + 46} ${RY - 4} L ${RX + 42} ${RY - 9} L ${RX - 42} ${RY - 9} Z`, fill: 'url(#gRest)' }, restG);
sv('ellipse', { cx: RX, cy: RY - 8, rx: 42, ry: 9, fill: '#d8d1e6' }, restG);
sv('ellipse', { cx: RX - 6, cy: RY - 7.5, rx: 26, ry: 6, fill: '#bfb6d3' }, restG);
const SPOON_REST = { x: RX - 4, y: RY - 13, a: 2.5 };          // where the spoon lies on its rest (the bowl in the rest's cup)
const spoonGlow = sv('ellipse', { cx: RX + 108, cy: RY - 12, rx: 180, ry: 40, fill: 'url(#gGlowLime)', opacity: 0 }, G.yours);
function spoonShape(parent) {           // a wooden spoon along +x: the bowl at the origin, the handle's end at x 236
  const g = sv('g', {}, parent);
  sv('path', { d: 'M 18 -4 C 60 -6 150 -7 232 -6 C 238 -6 240 6 232 6 C 150 7 60 6 18 4 Z', fill: 'url(#gWood)' }, g);
  sv('ellipse', { cx: 0, cy: 0, rx: 30, ry: 19, fill: 'url(#gWood)' }, g);
  sv('ellipse', { cx: -2, cy: -1, rx: 22, ry: 13, fill: '#b9844c', opacity: .55 }, g);
  sv('path', { d: 'M 40 -2 C 100 -3 170 -3 226 -3', stroke: '#fff3d6', 'stroke-width': 2, opacity: .55, fill: 'none' }, g);
  return g;
}
function handShape(parent) {            // your hand round the spoon's handle near its end, and the cuff (the forearm is drawn by drawArm)
  const g = sv('g', {}, parent);
  sv('path', { d: 'M 226 -34 C 238 -10 238 22 232 44 L 262 46 C 268 22 268 -12 258 -36 Z', fill: '#5b4fa0' }, g);   // the cuff
  sv('path', { d: 'M 230 -31 C 240 -10 240 20 235 41', fill: 'none', stroke: '#8f84d8', 'stroke-width': 2.5, opacity: .6, 'stroke-linecap': 'round' }, g);
  sv('path', { d: 'M 168 -26 C 186 -38 214 -38 230 -30 C 240 -10 240 18 230 34 C 214 44 184 44 168 34 C 156 24 154 -14 168 -26 Z', fill: 'url(#gHandSkin)' }, g);
  [[-18], [-4], [10], [24]].forEach(([y]) => sv('path', { d: `M 166 ${y} C 158 ${y - 7} 150 ${y - 2} 152 ${y + 6} C 154 ${y + 12} 162 ${y + 12} 168 ${y + 9}`, fill: '#a56c46', stroke: '#6d4227', 'stroke-width': 1.5 }, g));
  sv('path', { d: 'M 196 -32 C 178 -40 160 -30 156 -16 C 168 -18 182 -20 198 -18 Z', fill: '#b47a50', stroke: '#6d4227', 'stroke-width': 1.5 }, g);
  sv('path', { d: 'M 186 -26 C 204 -30 220 -26 228 -20', fill: 'none', stroke: '#e0a87c', 'stroke-width': 3, opacity: .6 }, g);
  return g;
}
// the spoon (and the hand) move as one group; a clip hides the bowl while it is under the stew
const SG = sv('g', {}, G.yours);
const spoonShadow = sv('ellipse', { rx: 120, ry: 9, fill: '#000', opacity: 0, filter: 'url(#fBlur2)' }, SG);
const spoonMove = sv('g', {}, SG);
const spoonClipId = 'cSpoon'; const spoonClip = sv('clipPath', { id: spoonClipId }, $('defs'));
const spoonClipR = sv('rect', { x: -60, y: -80, width: 800, height: 160 }, spoonClip);
const spoonG = sv('g', { 'clip-path': `url(#${spoonClipId})` }, spoonMove);
spoonShape(spoonG);
const handG = handShape(spoonMove);
// your forearm, seen from your seat: its base is fixed to you, the viewer (screen space, past the picture's bottom-right
// corner, right of every caption box), so it reaches in from the lower right in every framing; nearly straight (a forearm), the
// wrist flexing a little towards it; it tapers towards the cuff (foreshortened), is shaded across its width (lamp-lit top, darker
// underside), has a few short sleeve creases (no rings), falls darker towards you, and drops a soft shadow on your table; only
// the hand and about 320 world px of sleeve show (the rest fades out), so it never crosses the hall as one long tube
const ARM = { base: [2100, 1080], bend: 18, flex: .25, k0: .3, k1: .45, w0: 78, w1: 200 };   // base and w1 in screen px
const armG = sv('g', {}); SG.insertBefore(armG, spoonMove);
{ const tc = sv('clipPath', { id: 'cTableTop' }, $('defs')); sv('path', { d: `M ${YT.x - 254} ${YT.y - 128} L ${YT.x + 254} ${YT.y - 128} L ${YT.x + 280} ${YT.y + 16} L ${YT.x - 280} ${YT.y + 16} Z` }, tc); }
const gArmDepth = sv('linearGradient', { id: 'gArmDepth', gradientUnits: 'userSpaceOnUse' }, $('defs'));
[[0, 0], [.4, 0], [1, .6]].forEach(([o, a]) => sv('stop', { offset: o, 'stop-color': '#0a0814', 'stop-opacity': a }, gArmDepth));
// a forearm of believable length: the hand and about 320 world px of sleeve show, then the sleeve fades into the dark towards you
// (the mask runs from the wrist along the arm; past its end nothing of the arm or its shadow is drawn)
const gArmFade = sv('linearGradient', { id: 'gArmFade', gradientUnits: 'userSpaceOnUse' }, $('defs'));
[[0, 1], [.5, 1], [1, 0]].forEach(([o, a]) => sv('stop', { offset: o, 'stop-color': '#fff', 'stop-opacity': a }, gArmFade));
const mArm = sv('mask', { id: 'mArm', maskUnits: 'userSpaceOnUse', x: -4000, y: -4000, width: 10000, height: 10000 }, $('defs'));
sv('rect', { x: -4000, y: -4000, width: 10000, height: 10000, fill: 'url(#gArmFade)' }, mArm);
armG.setAttribute('mask', 'url(#mArm)');
const armShadow = sv('path', { fill: '#05030a', opacity: .34, filter: 'url(#fBlur)', 'clip-path': 'url(#cTableTop)' }, armG);
const armClipP = sv('path', {}, sv('clipPath', { id: 'cArm' }, $('defs')));
const armBody = sv('path', { fill: '#393070' }, armG);
const armShade = sv('g', { 'clip-path': 'url(#cArm)' }, armG);
const armDark = sv('path', { fill: '#140f2c', opacity: .8, filter: 'url(#fBlur4)' }, armShade);
const armLight = sv('path', { fill: '#6d5fc6', opacity: .5, filter: 'url(#fBlur4)' }, armShade);
const armFolds = sv('path', { fill: 'none', stroke: '#140f2c', 'stroke-width': 3, 'stroke-linecap': 'round', opacity: .5 }, armShade);
const armFoldL = sv('path', { fill: 'none', stroke: '#8a7ee0', 'stroke-width': 2, 'stroke-linecap': 'round', opacity: .35 }, armShade);
const armDepth = sv('path', { fill: 'url(#gArmDepth)' }, armShade);
const armRim = sv('path', { fill: 'none', stroke: '#a99ef0', 'stroke-width': 2.4, 'stroke-linecap': 'round', opacity: .5 }, armG);
function drawArm(W, hd, sc, o) {        // W: the wrist (world), hd: the hand's direction, sc: the spoon's 3D scale, o: opacity
  op(armG, o); if (o <= .002) return;
  const z = CM[2], B = [(ARM.base[0] - 960) / z + CM[0], (ARM.base[1] - 540) / z + CM[1]], L = Math.hypot(B[0] - W[0], B[1] - W[1]);
  const ca = Math.atan2(B[1] - W[1], B[0] - W[0]), ha = Math.atan2(hd[1], hd[0]);
  const Lv = Math.min(L, 320 * sc); sa(gArmFade, { x1: W[0], y1: W[1], x2: W[0] + (B[0] - W[0]) / L * Lv, y2: W[1] + (B[1] - W[1]) / L * Lv });
  const a0 = ha + (ca - ha) * ARM.flex, a1 = ca + ARM.bend * Math.PI / 180;      // the wrist flexes a little; the arm sags a little
  const P = [W, [W[0] + Math.cos(a0) * L * ARM.k0, W[1] + Math.sin(a0) * L * ARM.k0], [B[0] - Math.cos(a1) * L * ARM.k1, B[1] - Math.sin(a1) * L * ARM.k1], B];
  const w0 = ARM.w0 * sc, w1 = ARM.w1 / z, n = 30, pts = [];
  for (let i = 0; i <= n; i++) {
    const u = i / n, v = 1 - u;
    const c = [0, 1].map(k => v * v * v * P[0][k] + 3 * v * v * u * P[1][k] + 3 * v * u * u * P[2][k] + u * u * u * P[3][k]);
    const d = [0, 1].map(k => 3 * v * v * (P[1][k] - P[0][k]) + 6 * v * u * (P[2][k] - P[1][k]) + 3 * u * u * (P[3][k] - P[2][k]));
    const m = Math.hypot(d[0], d[1]) || 1;
    pts.push({ c, t: [d[0] / m, d[1] / m], n: [-d[1] / m, d[0] / m], w: w0 + (w1 - w0) * Math.pow(u, 1.35) });   // n: towards the underside
  }
  const at = (p, f, g = 0) => [p.c[0] + p.n[0] * p.w * f + p.t[0] * p.w * g, p.c[1] + p.n[1] * p.w * f + p.t[1] * p.w * g];
  const xy = q => q[0].toFixed(1) + ' ' + q[1].toFixed(1);
  const band = (f0, f1, dx = 0, dy = 0) => 'M ' + pts.map(p => { const q = at(p, f0); return xy([q[0] + dx, q[1] + dy]); }).join(' L ') + ' L ' +
    pts.slice().reverse().map(p => { const q = at(p, f1); return xy([q[0] + dx, q[1] + dy]); }).join(' L ') + ' Z';
  const outline = band(-.5, .5);
  armBody.setAttribute('d', outline); armClipP.setAttribute('d', outline); armDepth.setAttribute('d', outline);
  sa(gArmDepth, { x1: W[0], y1: W[1], x2: W[0] + (B[0] - W[0]) / L * Lv, y2: W[1] + (B[1] - W[1]) / L * Lv });   // darker as it fades: into shadow, not a ghost
  armDark.setAttribute('d', band(.12, .8));                  // the underside in shadow
  armLight.setAttribute('d', band(-.36, -.12));              // the lamp-lit top of the sleeve
  armRim.setAttribute('d', 'M ' + pts.slice(1, 24).map(p => xy(at(p, -.47))).join(' L '));
  // short creases: the sleeve bunching under the cuff (underside), one on top, one soft pull across the forearm, two at the elbow side
  const cr = (i, f0, f1, g) => { const p = pts[i]; return `M ${xy(at(p, f0))} Q ${xy(at(p, (f0 + f1) / 2, g * .55))} ${xy(at(p, f1, g))}`; };
  armFolds.setAttribute('d', [cr(1, .5, .12, .3), cr(3, .5, .2, .24), cr(2, -.5, -.3, .22), cr(8, .5, .26, .2), cr(16, .5, .28, -.2), cr(18, .5, .32, -.16)].join(' '));
  armFoldL.setAttribute('d', [cr(1, .42, .08, .3), cr(16, .42, .22, -.2)].join(' '));   // a faint lit edge beside two of them
  armShadow.setAttribute('d', band(-.42, .42, 16, 70));      // on the table top under the forearm (clipped to the table)
}
const dipRing = sv('ellipse', { rx: 16, ry: 5, fill: 'none', stroke: '#ffe2b8', 'stroke-width': 2.5, opacity: 0 }, G.yours);
// the glass lid (clear glass, a dark knob): it glints in the hook, settles onto your pot on "glass lid"
function lidShape(parent, rx, ry, h) {
  const g = sv('g', {}, parent);
  sv('ellipse', { cx: 0, cy: 0, rx: rx + 4, ry: ry + 3, fill: 'none', stroke: '#e9eef8', 'stroke-width': 5, opacity: .85 }, g);
  sv('path', { d: `M ${-rx} 0 C ${-rx} ${-h * 1.05} ${rx} ${-h * 1.05} ${rx} 0 A ${rx} ${ry} 0 0 1 ${-rx} 0 Z`, fill: 'url(#gLidGlass)' }, g);
  sv('path', { d: `M ${-rx} 0 C ${-rx} ${-h * 1.05} ${rx} ${-h * 1.05} ${rx} 0`, fill: 'none', stroke: '#ffffff', 'stroke-width': 2.5, opacity: .7 }, g);
  sv('path', { d: `M ${-rx * .72} ${-h * .3} C ${-rx * .62} ${-h * .7} ${-rx * .3} ${-h * .8} ${-rx * .08} ${-h * .8}`, fill: 'none', stroke: '#fff', 'stroke-width': 5, 'stroke-linecap': 'round', opacity: .75 }, g);
  sv('path', { d: `M ${rx * .55} ${-h * .5} C ${rx * .62} ${-h * .4} ${rx * .68} ${-h * .3} ${rx * .72} ${-h * .18}`, fill: 'none', stroke: '#fff', 'stroke-width': 3.5, 'stroke-linecap': 'round', opacity: .5 }, g);
  sv('path', { d: `M ${-24} ${-h * .8 + 2} C ${-22} ${-h * .8 - 26} ${22} ${-h * .8 - 26} ${24} ${-h * .8 + 2}`, fill: 'none', stroke: 'url(#gKnob)', 'stroke-width': 9, 'stroke-linecap': 'round' }, g);
  sv('ellipse', { cx: 0, cy: -h * .8 + 2, rx: 30, ry: 6, fill: '#a49cc0', opacity: .55 }, g);
  const glint = sv('rect', { x: -rx, y: -h * 1.1, width: rx * .5, height: h * 1.4, fill: 'url(#gGlint)', opacity: 0 }, g);
  const gid = 'cLid' + Math.round(rx); const cp = sv('clipPath', { id: gid }, defsOf(parent));
  sv('path', { d: `M ${-rx} 0 C ${-rx} ${-h * 1.05} ${rx} ${-h * 1.05} ${rx} 0 A ${rx} ${ry} 0 0 1 ${-rx} 0 Z` }, cp);
  glint.setAttribute('clip-path', `url(#${gid})`);
  return { g, glint, rx, h };
}
const lidG = sv('g', {}, G.front);
const lidShadow = sv('ellipse', { cx: 0, cy: 0, rx: YP.rx * 1.05, ry: YP.ry * 1.1, fill: '#000', opacity: 0, filter: 'url(#fBlur4)' }, lidG);
const lidMove = sv('g', {}, lidG);
const lid = lidShape(lidMove, YP.rx + 6, YP.ry + 5, 74);

/* the hook's small pot under its glass lid, and the recap's resting spoon (the same drawings, in their own svgs) */
const hkSvg = $('hkPotSvg');
const hkPot = drawPot(hkSvg, 0, 92, 1.55, 'mine');
setSwirl(hkPot, 0, 0);                  // the ingredients sit in the stew, as in your pot later
const hkLid = lidShape(hkSvg, 84 * 1.55 + 8, 24 * 1.55 + 6, 112);
hkLid.g.setAttribute('transform', `translate(0 ${92 - 112 * 1.55 - 2})`);
sv('ellipse', { cx: 0, cy: 118, rx: 170, ry: 22, fill: 'url(#gGlowLime)', opacity: .5 }, hkSvg).parentNode.insertBefore(hkSvg.lastChild, hkSvg.firstChild);
const rcSvg = $('rcSpoon');
{ const g = sv('g', { transform: 'translate(75 120)' }, rcSvg);                   // centred in its column
  sv('ellipse', { cx: 165, cy: 22, rx: 135, ry: 12, fill: '#000', opacity: .4, filter: 'url(#fBlur2)' }, g);   // the shadow under the rest and the spoon
  sv('path', { d: 'M 50 6 C 50 26 250 26 250 6 L 244 -4 L 56 -4 Z', fill: 'url(#gRest)' }, g);
  sv('ellipse', { cx: 150, cy: -2, rx: 94, ry: 14, fill: '#d8d1e6' }, g);
  const sp = spoonShape(g); sp.setAttribute('transform', 'translate(92 -14) rotate(-4) scale(1.05)');
  sv('ellipse', { cx: 200, cy: -10, rx: 210, ry: 50, fill: 'url(#gGlowLime)', opacity: .35 }, g).parentNode.insertBefore(g.lastChild, g.firstChild); }

/* ---------- the camera ---------- */
// wide: the lamps and the chef's hat in, your plate clear of the captions; the close shots (twist, pot, yours, lid) frame below the
// counter's gold top, so the chef is out of shot (never cut at the neck) and the top bar sits over the dark counter panel;
// turn: the chef's hat stays whole, your plate clear of the captions
const CAM = { wide: [960, 570, 1], hall: [960, 500, 1.16], twist: [1000, 732, 1.42], pot: [1010, 700, 1.66], yours: [1290, 748, 1.36],
  lid: [1127, 712, 1.5], turn: [1380, 574, 1.06] };
// the move to your table runs in the pause after "automatically" (after your pot's copied stir), so "You don't pick the trades"
// lands on a still picture
const CK = [[0, 'hall'], [S.cook[0] + .1, 'hall'], [S.cook[0] + 1.2, 'wide'], [C.w_and - .1, 'wide'], [C.w_twist + .5, 'twist'],
  [C.w_self + .2, 'twist'], [C.p_pot + .5, 'pot'], [C.d_name + .1, 'pot'], [C.x_strategy - .25, 'wide'], [C.a_auto + .5, 'wide'],
  [C.a_dont - .05, 'yours'], [S.lid[0] + .05, 'yours'], [S.lid[0] + 1.0, 'lid'], [S.recap[0] + .05, 'lid'], [S.recap[0] + 1.0, 'turn'], [1e9, 'turn']];
let CM = [960, 500, 1];
function camAt(t) {
  let i = 0; while (i < CK.length - 2 && t >= CK[i + 1][0]) i++;
  const [t0, a] = CK[i], [t1, b] = CK[i + 1], k = a === b ? 0 : ez.inOut(lin(t, t0, t1));
  const A = CAM[a], B = CAM[b];
  return [mix(A[0], B[0], k), mix(A[1], B[1], k), Math.exp(mix(Math.log(A[2]), Math.log(B[2]), k))];
}
function camera(t) {
  CM = camAt(t); const s = CM[2];
  $('world').style.transform = `translate(${(960 - CM[0] * s).toFixed(2)}px,${(540 - CM[1] * s).toFixed(2)}px) scale(${s.toFixed(5)})`;
  const h = .25 / TL.fps, P = camAt(t - h), Q = camAt(t + h), vx = Math.abs(Q[0] - P[0]) * s, vy = Math.abs(Q[1] - P[1]) * s;   // motion blur
  if (vx + vy > 1.5) { $('fMBg').setAttribute('stdDeviation', `${(vx / 3.46 / s).toFixed(2)} ${(vy / 3.46 / s).toFixed(2)}`); return 'url(#fMB)'; }
  return '';
}
const w2s = (x, y) => [(x - CM[0]) * CM[2] + 960, (y - CM[1]) * CM[2] + 540];

/* ---------- leader lines and the stir arrows (screen space) ---------- */
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
const dim = (t, later) => later.reduce((m, c) => m * (1 - .55 * ez.out(lin(t, c - .1, c + .3))), 1);
const PILL = { lime: [[203, 251, 97], [203, 251, 97], [20, 25, 10]], gold: [[255, 241, 191], [232, 194, 90], [26, 20, 5]] };
function foc(id, d) {
  const e = $(id), b = .42 + .58 * d, fl = d > .995 ? 'none' : `brightness(${b.toFixed(3)}) saturate(${(.55 + .45 * d).toFixed(3)})`;
  if (!e.classList.contains('pill') || e.classList.contains('line') || e.classList.contains('gline')) { e.style.filter = fl; return; }
  const [top, bot, ink] = PILL[e.classList.contains('gold') ? 'gold' : 'lime'], k = clamp((1 - d) / .55), em = e.querySelector('.em');
  if (em) em.style.filter = fl;
  if (k < .005) { e.style.background = e.style.color = e.style.boxShadow = ''; return; }
  const mx = (c, q, f) => `rgb(${c.map((v, i) => Math.round(v + (q[i] - v) * f)).join(',')})`;
  e.style.background = `linear-gradient(180deg,${mx(top, [21, 17, 42], k)},${mx(bot, [21, 17, 42], k)})`;
  e.style.color = mx(ink, [246 * b, 243 * b, 255 * b], k);
  e.style.boxShadow = `inset 0 0 0 3px rgba(${bot.map(v => Math.round(v * b)).join(',')},${(.9 * k).toFixed(3)}),0 0 40px rgba(${bot.join(',')},${(.45 * (1 - k)).toFixed(3)})`;
}
// one stir = one turn of the same circular arrow, the same size for the chef, for you and for every copied stir
const FX = $('fx');
function stirGlyph(col) {
  const g = sv('g', { opacity: 0 }, FX);
  sv('circle', { cx: 0, cy: 0, r: 58, fill: col === 'gold' ? 'url(#gFxGold)' : 'url(#gFxLime)', opacity: .5 }, g);
  const rot = sv('g', {}, g);
  const c = col === 'gold' ? '#ffe08f' : '#cbfb61';
  sv('path', { d: 'M 30 0 A 30 30 0 1 1 21.2 -21.2', fill: 'none', stroke: '#14110b', 'stroke-width': 13, 'stroke-linecap': 'round', opacity: .55 }, rot);
  sv('path', { d: 'M 30 0 A 30 30 0 1 1 21.2 -21.2', fill: 'none', stroke: c, 'stroke-width': 8, 'stroke-linecap': 'round' }, rot);
  sv('path', { d: 'M 10 -30 L 26 -27 L 23 -11', fill: 'none', stroke: c, 'stroke-width': 8, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, rot);
  return { g, rot };
}
const stirChef = stirGlyph('gold'), stirYou = stirGlyph('lime'), stirFly = stirGlyph('lime');
const pulses = faint.map(f => sv('path', { d: f.p.getAttribute('d'), fill: 'none', stroke: '#f0ffc4', 'stroke-width': 6, 'stroke-linecap': 'round', 'stroke-dasharray': `46 ${(f.L + 200).toFixed(0)}`, opacity: 0, filter: 'url(#fBlur2)' }, lineG));
function showStir(sg, o, x, y, ang, s = 1) { op(sg.g, o); if (o > .002) { sa(sg.g, { transform: `translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${s.toFixed(3)})` }); sa(sg.rot, { transform: `rotate(${ang.toFixed(1)})` }); } }

/* ---------- hook: the two-part question, the small pot under its glass lid, three empty slots ---------- */
const QL = [...$('hkL').children].filter(e => e.tagName === 'SPAN'), QR = [...$('hkR').children].filter(e => e.tagName === 'SPAN');
function hook(t) {
  const [a, b] = S.hook, e = b - .05;
  const v = vis(t, a, e, 0, .2);                                  // a short fade, so the three settled slots are held before Hi
  const lt = ez.out(lin(t, C.h_copy - .05, C.h_copy + .3));       // "Copy trading" lights the title strip
  st($('hkT'), v * (.5 + .5 * lt), 0, 0, 1 + .03 * pulse(t, C.h_copy - .05, .5));
  $('hkT').style.filter = lt > .99 ? 'none' : `brightness(${(.55 + .45 * lt).toFixed(3)})`;
  st($('hkL'), v); st($('hkR'), v);
  [...QL, ...QR].forEach((w, i) => {
    const c = C.h_words[i];
    w.classList.toggle('lit', t >= c - .04);
    w.style.transform = `translateY(${(-10 * pulse(t, c - .04, .3)).toFixed(1)}px) scale(${(1 + .05 * pulse(t, c - .04, .3)).toFixed(3)})`;
  });
  const hp = pop(t, a, e, 0, .2); st($('hkPot'), hp.o, 0, 6 * Math.sin(t * 1.6), 1);
  const gl = lin(t, C.h_stays - .05, C.h_stays + .75);           // the glass lid glints on "stays yours"
  op(hkLid.glint, t > C.h_stays - .05 && gl < 1 ? Math.sin(Math.PI * gl) : 0);
  sa(hkLid.glint, { x: mix(-hkLid.rx * 1.2, hkLid.rx * .8, gl) });
  [...$('hkS').children].forEach((el, i) => {                    // three empty numbered slots slide in under "What stays yours?" (on "stays")
    const c = C.h_stays + i * .06, k = ez.back(lin(t, c, c + .36));   // all three settled about 0.35 s before the hook fades
    el.style.opacity = (clamp(lin(t, c, c + .2)) * v).toFixed(3); el.style.transform = `translateY(${(60 * (1 - k)).toFixed(1)}px)`;
  });
  st($('hkS'), t >= C.h_stays ? v : 0);
}

/* ---------- hi ---------- */
function hi(t) {
  const [a, b] = S.hi, e = b - .35;
  const d = pop(t, a + .15, e, .45, .3); st($('hdisc'), d.o, 0, 0, d.s * (1 + .01 * Math.sin(t * 1.6)));
  const h = rise(t, a + .4, e, 24), r = rise(t, a + .65, e, 30); st($('hwho'), h.o, 0, h.y); st($('httl'), r.o, 0, r.y);
}

/* ---------- the world, one function of t across every scene ---------- */
let restAt = 1e9;
function chefPose(t) {                                         // his spoon handle's top, stirring once on each of his stirs
  const st1 = [C.k_copy - .05, C.k_copy + .75], st2 = [C.a_trades - .15, C.a_trades + .65];
  let k = 0; [st1, st2].forEach(([a, b]) => { if (t >= a && t <= b) k = ez.inOut(lin(t, a, b)); });
  const ang = k * Math.PI * 2, dip = [CPOT.x - 8 + 22 * Math.sin(ang), CPOT.y + 1 + 4 * (1 - Math.cos(ang))];
  const top = [dip[0] + 42 + 8 * Math.sin(ang), dip[1] - 58];
  return { dip, top, k: k > 0 && k < 1 ? 1 : 0, ang };
}
function world(t) {
  const mb = camera(t);
  const out = Math.max(vis(t, S.hi[0], S.hi[1], .15, .35), t > S.turn[1] - .3 ? lin(t, S.turn[1] - .3, S.turn[1]) : 0);
  const dimR = 1 - .94 * vis(t, S.recap[0] + .2, C.u_now + .5, .6, .5);       // the recap columns stand in front; the picture returns as they fold away
  const dimL = 1 - .6 * vis(t, C.f_sonic - .1, S.look[1] + .15, .5, .5);     // the real screens lead in "Look before you pick"
  const wo = (1 - out) * (t < S.cook[0] ? 0 : 1) * dimR;
  $('world').style.opacity = clamp(wo).toFixed(3); $('world').style.visibility = wo < .002 ? 'hidden' : 'visible';
  const fl = (mb + (dimL < .995 ? ` brightness(${dimL.toFixed(3)}) saturate(${(.6 + .4 * dimL).toFixed(3)})` : '')).trim();
  $('world').style.filter = fl || 'none';
  // the hall builds on "Think of a cooking class"
  const hb = ez.out(lin(t, S.cook[0], C.k_cooking + .2));
  op(hall, hb);
  lamps.forEach((l, i) => { const k = ez.out(lin(t, C.k_cooking - .2 + i * .15, C.k_cooking + .5 + i * .15)); op(l.glow, k * (.9 + .1 * Math.sin(t * 2 + i))); op(l.cone, .6 * k); });
  // the tables come in, back row first
  rowT.forEach((r, i) => { const c = C.k_cooking + .05 + i * .1, k = ez.back(lin(t, c, c + .45));
    op(r.g, clamp(lin(t, c, c + .2))); sa(r.g, { transform: `translate(${r.cx} ${r.cy + 140 * r.s}) scale(${Math.max(.01, .85 + .15 * k).toFixed(3)}) translate(${-r.cx} ${-(r.cy + 140 * r.s)})` }); });
  const yk = ez.back(lin(t, C.k_class, C.k_class + .5));
  op(yt.g, clamp(lin(t, C.k_class, C.k_class + .2)));
  sa(yt.g, { transform: `translate(${YT.x} ${YT.y + 140}) scale(${Math.max(.01, .85 + .15 * yk).toFixed(3)}) translate(${-YT.x} ${-(YT.y + 140)})` });
  op(restG, clamp(lin(t, C.k_class, C.k_class + .2)));
  // the chef and his counter light on "The chef cooks at the front"
  const ck = ez.out(lin(t, C.k_chef - .15, C.k_chef + .4));
  op(chefG, clamp(lin(t, C.k_cooking, C.k_cooking + .3)));
  [chefBody, chefFront].forEach(g => { g.setAttribute('transform', `translate(0 ${(26 * (1 - ck)).toFixed(1)})`); op(g, ck); });
  op(ctrGlow, .55 * Math.max(vis(t, C.k_chef - .1, C.k_copy + .9, .4, .6), .9 * pulse(t, C.a_trades - .2, 1.0)));
  const cp = chefPose(t);
  const sh = [CHEF.x + 84, 290], el = [sh[0] + 58, sh[1] + 6];   // the elbow at shoulder height: he holds the spoon from above
  sa(chefArm, { d: `M ${sh[0]} ${sh[1]} Q ${el[0].toFixed(1)} ${el[1].toFixed(1)} ${(cp.top[0] + 4).toFixed(1)} ${(cp.top[1] + 16).toFixed(1)}` });
  sa(chefSpoon, { x1: cp.dip[0], y1: cp.dip[1], x2: cp.top[0] + 4, y2: cp.top[1] - 8 });
  sa(chefHand, { cx: cp.top[0] + 2, cy: cp.top[1] + 6, transform: `rotate(30 ${(cp.top[0] + 2).toFixed(1)} ${(cp.top[1] + 6).toFixed(1)})` });
  // the hat badge lights on "a strategy"
  op(badgeGlow, Math.max(vis(t, C.x_strategy - .1, S.acct[1] + .3, .3, .5) * (.85 + .15 * Math.sin(t * 4)), .8 * pulse(t, C.a_trades - .2, 1.0)));
  // your table lights on "in your own pot"; the others step back a little
  // (and in "Now it's your turn", so no other pot ever stands beside yours as an equal: no two pots side by side to compare)
  const turnSoft = vis(t, C.u_now - .3, S.turn[1], .6, .3);
  // the close-shot softening holds until the recap has darkened the world (S.recap[0] + .8), so nothing brightens on the scene change
  const soft = S.recap[0] + .8;
  const yl = Math.max(.25 * vis(t, C.k_own - .15, S.copied[1], .4, .6), .5 * vis(t, S.yours[0], soft, .6, .3), .45 * turnSoft);
  const dof = Math.max(3.5 * clamp((CM[2] - 1.12) / .35), 3 * turnSoft);   // close on your table: the other tables soften into the background
  rowT.forEach(r => { r.g.style.filter = yl > .01 || dof > .05 ? `brightness(${(1 - yl).toFixed(3)}) saturate(${(1 - .5 * yl).toFixed(3)}) blur(${dof.toFixed(2)}px)` : 'none'; });
  chefG.style.filter = t > S.yours[0] && t < soft + .3 ? `brightness(${(1 - .4 * vis(t, S.yours[0], soft, .6, .3)).toFixed(3)})` : 'none';
  // the CopyX line draws on "CopyX"; fainter lines into every other pot
  const lk = ez.inOut(lin(t, C.x_copyx - .05, C.x_copyx + .7));
  const lineOn = t >= C.x_copyx - .05 ? 1 : 0, lineO = lineOn * (1 - .65 * vis(t, S.yours[0], soft, .6, .4));
  sa(mainLine, { 'stroke-dasharray': `${(ML * lk).toFixed(1)} ${ML + 10}` }); op(mainLine, lineO);
  sa(mainGlow, { 'stroke-dasharray': `${(ML * lk).toFixed(1)} ${ML + 10}` });   // the glow draws with the line (never the whole path at once)
  op(mainGlow, lineO * .45 * (lk > 0 ? 1 : 0) * (1 + .5 * pulse(t, C.a_into, 1.2)));
  // the fainter lines only in the wide and turn shots (in a close shot they would lead nowhere in frame and cross the lockup); in "Now
  // it's your turn" they recede with the tables they lead to, so the Join JetUP button stays the one focal point
  const fz = 1 - clamp((CM[2] - 1.08) / .14), fl2 = fz * (1 - .7 * turnSoft);
  faint.forEach((f, i) => { const c = C.x_copyx + .25 + i * .08, k = ez.inOut(lin(t, c, c + .7));
    sa(f.p, { 'stroke-dasharray': `${(f.L * k).toFixed(1)} ${(f.L + 10).toFixed(1)}` }); op(f.p, lineO * .5 * fl2 * (k > 0 ? 1 : 0)); });   // fainter: thinner, half see-through
  op(srcGlow, lineO * .8 * vis(t, C.x_copyx - .05, S.copied[1], .3, .5));
  // your pot: the ingredients glow lime on "deposit" ("Your money"); they stay unlit under "What stays yours?"
  op(YP.glow, .42 * vis(t, C.d_deposit - .1, C.x_strategy, .4, .5));
  // stirs: your hand stirs once in your pot ("you copy each step"); your pot stirs by itself after the spoon rests;
  // the copied stir arrives along the CopyX line ("What gets copied") and is seen again through the glass lid
  const self1 = [C.w_self, C.w_self + .8], arr = C.a_into + .75, self2 = [arr, arr + .8], self3 = [C.l_watch, C.l_watch + .8];
  let ang = 0, sk = 0;
  [[C.k_step - .1, C.k_step + .7], self1, self2, self3].forEach(([a, b]) => { if (t >= a && t <= b) { ang = 360 * ez.inOut(lin(t, a, b)); sk = Math.sin(Math.PI * lin(t, a, b)); } });
  setSwirl(YP, ang, .8 * sk);
  rowT.forEach((r, i) => { const c = arr + .1 + i * .12; let a2 = 0, k2 = 0; if (t >= c && t <= c + .8) { a2 = 360 * ez.inOut(lin(t, c, c + .8)); k2 = Math.sin(Math.PI * lin(t, c, c + .8)); }
    setSwirl(r.pot, a2, 0); });
  // your spoon: in your hand from "you copy each step", stirs once; set down on its rest on "lift the spoon"; rests for good
  spoonAndHand(t);
  // the glass lid: above your pot on "Want to see it for yourself?", settles on "glass lid", stays
  glassLid(t);
}

function spoonAndHand(t) {
  // the hoist runs in the silent beat after "And the twist?" (as the camera eases in on your hand), so the spoon already lies on its
  // rest on "lift" (C.w_rest = "lift" + .05) and the hand lets go during "the spoon": never a lifted spoon on the word "lift"
  const inA = C.k_copy + .1, stirA = C.k_step - .1, stirB = C.k_step + .7, lift0 = C.w_twist + .2, setT = C.w_rest, away = C.w_rest + .6;
  const dip0 = [YP.sc[0] + 4, YP.sc[1] - 1], A0 = 20;           // while it stirs: the bowl under the stew, the handle towards you
  let bowl = dip0, ang = A0, sc = 1, clipX = 22, hv = 0, show = 0, shad = 0, leave = 0;
  if (t >= inA && t < setT) {
    show = 1; hv = 1;
    const enter = ez.out(lin(t, inA, inA + .5));
    let k = 0; if (t >= stirA && t <= stirB) k = ez.inOut(lin(t, stirA, stirB));
    const a = k * Math.PI * 2, dip = [dip0[0] + 28 * Math.sin(a), dip0[1] + 7 * (1 - Math.cos(a))];
    if (t < lift0) {                                            // in from your side, then one stir
      bowl = [dip[0] + 300 * (1 - enter), dip[1] + 80 * (1 - enter)]; ang = A0 + 4 * Math.sin(a); clipX = 22;   // in from your side (the right)
    } else {                                                    // lifted out, carried in an arc and laid down on its rest (in 3D)
      const up = ez.out(lin(t, lift0, lift0 + .25)), lk = ez.inOut(lin(t, lift0 + .2, setT));
      const p0 = [dip0[0], dip0[1] - 64 * up], p1 = [SPOON_REST.x, SPOON_REST.y];
      const ctrl = [mix(p0[0], p1[0], .5) - 40, Math.min(p0[1], p1[1]) - 30];   // a low, gentle carry
      bowl = [(1 - lk) * (1 - lk) * p0[0] + 2 * lk * (1 - lk) * ctrl[0] + lk * lk * p1[0], (1 - lk) * (1 - lk) * p0[1] + 2 * lk * (1 - lk) * ctrl[1] + lk * lk * p1[1]];
      ang = mix(A0, SPOON_REST.a, lk); sc = 1 + .14 * Math.sin(Math.PI * lk);
      clipX = mix(22, -60, up); shad = lk;
    }
  } else if (t >= setT) {
    show = 1; bowl = [SPOON_REST.x, SPOON_REST.y]; ang = SPOON_REST.a; clipX = -60; shad = 1;
    leave = ez.inOut(lin(t, setT + .05, away)); hv = 1 - leave;
  }
  op(SG, show);
  if (show) {
    sa(spoonMove, { transform: `translate(${bowl[0].toFixed(1)} ${bowl[1].toFixed(1)}) rotate(${ang.toFixed(2)}) scale(${sc.toFixed(3)})` });
    sa(spoonClipR, { x: clipX });
    sa(handG, { transform: `translate(${(200 * leave).toFixed(1)} ${(40 * leave).toFixed(1)})` }); op(handG, hv);
    op(spoonShadow, .45 * shad); sa(spoonShadow, { cx: bowl[0] + 112, cy: bowl[1] + 22 });
    const ar = ang * Math.PI / 180, ca = Math.cos(ar), sn = Math.sin(ar), lx = (246 + 200 * leave) * sc, ly = (5 + 40 * leave) * sc;   // the wrist, under the cuff
    drawArm([bowl[0] + ca * lx - sn * ly, bowl[1] + sn * lx + ca * ly], [ca, sn], sc, hv);
  } else op(armG, 0);
  const dipOn = t >= inA + .3 && t < lift0 + .1;
  op(dipRing, dipOn ? .7 : 0);
  if (dipOn) { const k = t >= stirA && t <= stirB ? ez.inOut(lin(t, stirA, stirB)) : 0, a = k * Math.PI * 2; sa(dipRing, { cx: dip0[0] + 28 * Math.sin(a), cy: dip0[1] + 7 * (1 - Math.cos(a)) }); }
  op(spoonGlow, .9 * vis(t, C.a_dont - .1, S.copied[1] + .1, .3, .5));   // it glows on "You don't pick the trades"
}
function glassLid(t) {
  const app = C.l_want - .05, land = C.l_lid - .1;
  const on = t >= app;
  op(lidG, on ? 1 : 0); if (!on) return;
  const top = [YP.sc[0], YP.y0 - 112], seat = [YP.sc[0], YP.y0 - 2];
  const k = ez.inOut(lin(t, land - .45, land));
  const tilt = 14 * (1 - k) * Math.cos(t * 2.2), hover = (1 - k) * 8 * Math.sin(t * 2.4);
  const p = [mix(top[0], seat[0], k), mix(top[1], seat[1], k) + hover];
  const sq = 1 + .05 * pulse(t, land, .3);                   // a soft settle
  sa(lidMove, { transform: `translate(${p[0].toFixed(1)} ${p[1].toFixed(1)}) rotate(${tilt.toFixed(2)}) scale(${sq.toFixed(3)} ${(2 - sq).toFixed(3)})` });
  op(lidMove, ez.out(lin(t, app, app + .35)));
  op(lidShadow, .35 * k); sa(lidShadow, { cx: seat[0], cy: seat[1] + 2 });
  const g1 = lin(t, C.l_want + .1, C.l_want + .9), g2 = lin(t, land + .05, land + .8);
  const gl = t < C.l_want + .9 ? g1 : g2;
  op(lid.glint, (t > C.l_want + .1 && g1 < 1) || (t > land + .05 && g2 < 1) ? Math.sin(Math.PI * gl) : 0);
  sa(lid.glint, { x: mix(-lid.rx * 1.2, lid.rx * .8, gl) });
}

/* ---------- labels: the cooking class, your pot, your account ---------- */
function plate(t) {                                              // your lime name plate: "Your pot", flips to "Your own account", grows
  const on = t >= C.k_pot - .15 && t < S.recap[0] + .6;
  const pv = vis(t, C.k_pot - .15, S.turn[1], .35, .4) * (t > S.recap[0] + .2 && t < C.u_now + .5 ? 1 - vis(t, S.recap[0] + .2, C.u_now + .5, .6, .5) : 1);
  const el = $('plate'); el.style.visibility = pv > .002 ? 'visible' : 'hidden'; el.style.opacity = pv.toFixed(3);
  // it steps back while the real screens lead, under the glass lid (until the recap has darkened the world), and while the Join JetUP
  // button leads in "Now it's your turn": readable, but never competing with the call to action
  const pd = 1 - .5 * vis(t, C.f_sonic - .1, S.look[1] + .15, .5, .5) - .3 * vis(t, C.l_want - .2, S.recap[0] + .8, .5, .3)
    - .35 * vis(t, C.u_turn - .1, S.turn[1] + 1, .5, .01);
  el.style.filter = pd < .995 ? `brightness(${pd.toFixed(3)}) saturate(${(.6 + .4 * pd).toFixed(3)})` : 'none';
  if (pv <= .002) return;
  const [x, y] = w2s(YT.x, YT.y + 52), s = Math.max(1, CM[2] * .8);   // never smaller than its own type (30 px and up); in front of the
  // spoon rest's saucer (never over it)
  el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)})`;
  const f1 = ez.inOut(lin(t, C.p_own - .15, C.p_own + .3)), f2 = ez.inOut(lin(t, C.d_tag - .1, C.d_tag + .35));
  const A = $('plA'), B = $('plB'), Cc = $('plC');
  const pin = ez.back(lin(t, C.k_pot - .15, C.k_pot + .3));
  [[A, 260, 74], [B, 380, 74], [Cc, 470, 116]].forEach(([e, w, h]) => { e.style.width = w + 'px'; e.style.height = h + 'px'; e.style.left = (-w / 2) + 'px'; e.style.top = (-h / 2) + 'px'; });
  A.style.transform = `rotateX(${(180 * f1).toFixed(1)}deg) scale(${(.6 + .4 * pin).toFixed(3)})`; A.style.opacity = f1 < .5 ? 1 : 0;
  B.style.transform = `rotateX(${(180 * f1 - 180 + 180 * f2).toFixed(1)}deg)`; B.style.opacity = f1 >= .5 && f2 < .5 ? 1 : 0;
  Cc.style.transform = `rotateX(${(180 * f2 - 180).toFixed(1)}deg)`; Cc.style.opacity = f2 >= .5 ? 1 : 0;
  const gl = Math.max(.9 * pulse(t, C.k_pot - .05, .8), .8 * pulse(t, C.p_own - .1, .9), .8 * pulse(t, C.d_tag, .9), vis(t, C.y_own - .1, C.y_choices + .2, .3, .5) * (.75 + .25 * Math.sin(t * 4)));
  const g = $('plateGlow'), gw = f2 >= .5 ? 600 : f1 >= .5 ? 520 : 400, gh = f2 >= .5 ? 230 : 180;
  g.style.width = gw + 'px'; g.style.height = gh + 'px'; g.style.left = (-gw / 2) + 'px'; g.style.top = (-gh / 2) + 'px';
  g.style.opacity = gl.toFixed(3); g.style.visibility = gl > .01 ? 'visible' : 'hidden';
}
function acctLabels(t) {
  const [a, b] = S.acct;
  place('Lmoney', 1280, 330);                                    // gone before the camera pulls back (it never rests on another table's pot)
  const m = rise(t, C.d_deposit - .1, C.d_name + .1, 24, .4, .3); st($('Lmoney'), m.o, 0, m.y); foc('Lmoney', dim(t, [C.d_tag]));
  const [mx_, my_, , mh] = box('Lmoney'); leader('money', m.o * dim(t, [C.d_tag]), [mx_, my_ + mh / 2 + m.y], w2s(YP.sc[0] + 30, YP.sc[1]), '#cbfb61');
  // the hat badge: "Sonic AI · the strategy" (gold, the chef's colour)
  const [bx, by] = w2s(BADGE[0], BADGE[1]);
  place('Lbadge', 1250, 150);
  const bd = rise(t, C.x_strategy - .1, C.a_trades2 - .15, 20, .35, .3); st($('Lbadge'), bd.o, 0, bd.y); foc('Lbadge', dim(t, [C.x_copyx, C.a_what]));   // "Sonic AI's trades" takes its place
  const [lx, ly, , lh] = box('Lbadge'); leader('badge', bd.o * dim(t, [C.x_copyx, C.a_what]), [lx, ly + lh / 2 + bd.y], [bx + 14, by], '#ffe08f');
  // "CopyX" on the line
  // on the floor below the counter's lower rail (never touching it); gone as the camera leaves the wide shot, so it never lands
  // beside "What gets copied?" in the close shot (where the pair would read as a question and its answer)
  const pt = mainLine.getPointAtLength(ML * .52), [cx_, cy_] = w2s(pt.x, pt.y);
  const cxk = pop(t, C.x_copyx + .35, C.a_auto + .9, .35, .4); place('Lcopyx', cx_ + 18, cy_ - 32);
  st($('Lcopyx'), cxk.o, 0, 0, cxk.s); foc('Lcopyx', dim(t, [C.a_what]));
}

/* ---------- labels: what gets copied ---------- */
function copiedLabels(t) {
  const [a, b] = S.copied;
  place('Qcopied', 80, 146);
  const q = rise(t, C.a_what - .15, b, 20); st($('Qcopied'), q.o, 0, q.y);
  place('Lauto', 1262, 146);                                     // right of the chef's stir arrow, above the right-hand tables
  // "Sonic AI's trades," lands on "trades" with the chef's one stir; its small line grows in on "into your account" as the stir travels
  // gone as the camera leaves the wide shot (it fades from 29.97 s, after "automatically."): it never rests on another table's pot
  const l = rise(t, C.a_trades2 - .1, C.a_auto + .9, 20, .4, .3); st($('Lauto'), l.o, 0, l.y); foc('Lauto', dim(t, [C.a_dont]));
  const sm = $('Lauto').querySelector('small');               // the box opens first, then its words fade in (never a half-cut line)
  sm.style.maxHeight = (ez.out(lin(t, C.a_into - .12, C.a_into + .18)) * 84).toFixed(1) + 'px';
  sm.style.opacity = ez.out(lin(t, C.a_into + .04, C.a_into + .34)).toFixed(3);
  const [rx_, ry_] = w2s(SPOON_REST.x + 232, SPOON_REST.y + 6);   // the end of the resting spoon's handle
  place('Cpick', 830, 522);                                      // level with the resting spoon's end, clear above your plate
  const c = pop(t, C.a_dont - .12, b, .35, .3); st($('Cpick'), c.o, 0, 0, c.s);
  const [px, py, , ph] = box('Cpick'); leader('pick', c.o, [px, py + ph / 2], [rx_, ry_ + 4], '#cbfb61');
  // the stirs: the chef stirs once (gold), it travels along the CopyX line into your pot, and fainter into every other pot
  const cs = w2s(CPOT.x + 106, CPOT.y - 46);                   // beside his pot, clear of his arm
  const g1 = vis(t, C.k_copy - .1, C.k_copy + 1.0, .2, .3), g2 = vis(t, C.a_trades - .25, C.a_trades + .9, .2, .3);
  const k1 = ez.inOut(lin(t, C.k_copy - .05, C.k_copy + .75)), k2 = ez.inOut(lin(t, C.a_trades - .15, C.a_trades + .65));
  showStir(stirChef, Math.max(g1, g2), cs[0], cs[1], 360 * (t < C.a_trades - .3 ? k1 : k2));
  const ys = w2s(YP.sc[0], YP.y0 - 72);
  const y1 = vis(t, C.k_step - .15, C.k_step + .9, .2, .3), y2 = vis(t, C.w_self - .05, C.w_self + 1.0, .2, .3), arr = C.a_into + .75, y3 = vis(t, arr - .05, arr + 1.0, .2, .3);
  const yk = t < C.w_self - .1 ? ez.inOut(lin(t, C.k_step - .1, C.k_step + .7)) : t < arr - .1 ? ez.inOut(lin(t, C.w_self, C.w_self + .8)) : ez.inOut(lin(t, arr, arr + .8));
  const y4 = vis(t, C.l_watch - .05, C.l_watch + 1.0, .2, .3), lidS = w2s(YP.sc[0] - 6, YP.y0 - 26);   // inside the dome: under the handle, above the stew
  if (y4 > 0) showStir(stirYou, y4, lidS[0], lidS[1], 360 * ez.inOut(lin(t, C.l_watch, C.l_watch + .8)));
  else showStir(stirYou, Math.max(y1, y2, y3), ys[0], ys[1], 360 * yk);
  // the copied stir travels: along the main line, then the fainter lines
  const f0 = C.a_into - .1, f1 = arr - .05;
  if (t >= f0 && t <= f1 + .1) {
    const k = ez.inOut(lin(t, f0, f1)), p = mainLine.getPointAtLength(ML * k), [x, y] = w2s(p.x, p.y);
    showStir(stirFly, Math.min(1, lin(t, f0, f0 + .15)) * (1 - lin(t, f1, f1 + .1)), x, y - 34, 360 * k);   // one turn, like every stir
  } else showStir(stirFly, 0, 0, 0, 0);
  pulses.forEach((pp, i) => {
    const f = faint[i], a0 = f0 + .12, a1 = f1 + .1 + i * .1, k = ez.inOut(lin(t, a0, a1));
    op(pp, t >= a0 && t <= a1 + .15 ? .9 * Math.min(1, lin(t, a0, a0 + .12)) * (1 - lin(t, a1, a1 + .15)) : 0);
    sa(pp, { 'stroke-dashoffset': (46 - k * (f.L + 46)).toFixed(1) });
  });
}

/* ---------- what stays yours: the question returns with its three slots; they move beside your table and fill ---------- */
const CHO = ['ch1', 'ch2', 'ch3'];
function yoursLabels(t) {
  const [a, b] = S.yours;
  place('Qyours', 1130, 146);
  const q = rise(t, C.y_what - .15, b + .2, 20, .4, .35); st($('Qyours'), q.o, 0, q.y);
  const fills = [C.y_strategy, C.y_how, C.y_when];
  const mv = ez.inOut(lin(t, C.y_choices - .1, C.y_choices + .7));   // gates the dashes and the words
  // each slot drops into its own row first (a staircase, never a stack), then widens into its card
  const my = ez.inOut(lin(t, C.y_choices - .1, C.y_choices + .3)), mx = ez.inOut(lin(t, C.y_choices + .15, C.y_choices + .7));
  const opened = C.f_sonic - .05;                            // slot 1 opens into the real screen; 2 and 3 step aside
  CHO.forEach((id, i) => {
    const e = $(id);
    // empty: a small tile under the question (top right); then a card beside your table
    const tx0 = 1150 + i * 172, ty0 = 252, tx1 = 858, ty1 = 250 + i * 184;
    const x = mix(tx0, tx1, mx), y = mix(ty0, ty1, my), w = mix(150, 990, mx), h = mix(150, 152, mx);
    e.style.left = x + 'px'; e.style.top = y + 'px'; e.style.width = w + 'px'; e.style.height = h + 'px';
    const v = vis(t, C.y_what - .05 + i * .1, S.look[0] + 2.2, .35, .5) * (i === 0 ? 1 - lin(t, opened, opened + .25) : 1);
    const filled = ez.out(lin(t, fills[i] - .1, fills[i] + .3));
    const words = i === 0 ? 1 - ez.inOut(lin(t, C.f_sonic - .3, C.f_sonic - .1)) : 1;   // slot 1's words leave before the screen opens over it
    e.querySelector('.tx').style.opacity = ((mv > .9 ? filled : 0) * words).toFixed(3);
    e.querySelector('.ic').style.opacity = ((mv > .9 ? filled : 0) * words).toFixed(3);
    e.querySelector('.dash').style.opacity = (mv > .5 ? 1 - filled : 0).toFixed(3);
    e.querySelector('.ic').style.transform = `scale(${(.7 + .3 * ez.back(lin(t, fills[i] - .1, fills[i] + .35))).toFixed(3)})`;
    const aside = ez.inOut(lin(t, C.f_sonic - .22, C.f_sonic + .1));   // 2 and 3 step aside before the screen grows over them
    const slideIn = ez.back(lin(t, C.y_what - .05 + i * .1, C.y_what + .4 + i * .1));
    st(e, v * (i > 0 ? 1 - aside : 1), (i > 0 ? 80 * aside : 0), 40 * (1 - slideIn), 1);
  });
}

/* ---------- look before you pick: MTG's real CopyX screens ---------- */
function lookScreens(t) {
  const [a, b] = S.look, o0 = C.f_sonic - .05, sOut = C.r_read - .32;   // the SONIC card is gone before the fee card comes in
  // slot 1 opens into the SONIC card: it grows out of slot 1's place
  const k = ez.out(lin(t, o0, o0 + .55)), ko = ez.inOut(lin(t, sOut, sOut + .4));
  place('scrS', 1030, 122);
  const v = t >= o0 && t < sOut + .4 ? clamp(lin(t, o0, o0 + .1)) * (1 - ko) : 0;   // solid at once: it covers the empty slot, never text over text
  const sx = mix(.35, 1, k), ox = mix(-220, 0, k) - 520 * ko, oy = mix(-60, 0, k);
  st($('scrS'), v, ox, oy, sx);
  $('scrS').style.transformOrigin = '0% 0%';
  const pg = pulse(t, C.f_my - .1, 1.0);                      // the Myfxbook panel lights on "Myfxbook"
  $('scrS').style.boxShadow = pg > .01 ? `inset 0 0 0 2.5px rgba(203,251,97,.85),0 0 ${(34 + 40 * pg).toFixed(0)}px rgba(203,251,97,${(.25 + .4 * pg).toFixed(2)}),inset 0 0 26px rgba(203,251,97,.12),0 30px 70px rgba(0,0,0,.5)` : '';
  // the fee card slides in on "Read the terms"; the row lights on "performance fee"; the chip on "profits only"
  place('scrF', 380, 230);
  const f = rise(t, C.r_read + .02, b, 0, .45, .35), fin = ez.out(lin(t, C.r_read + .02, C.r_read + .55));
  st($('scrF'), f.o, 300 * (1 - fin), 0, 1);
  const lit = vis(t, C.r_perf - .1, b, .3, .3);
  $('scrF').querySelector('.lit').style.opacity = (lit * (.75 + .25 * Math.sin(t * 4))).toFixed(3);
  place('Cprofit', 1010, 548);                                 // under the fee card, clear of your plate
  const cp = pop(t, C.r_profits - .1, b, .35, .3); st($('Cprofit'), cp.o, 0, 0, cp.s);
}

/* ---------- the glass lid: the re-hook, the lid settles, MetaTrader 5, the eye icon, read only ---------- */
const EYE = [.8132, .9258];                                    // the eye icon in copyx-eye.png (make_screens.py prints it)
function lidLabels(t) {
  const [a, b] = S.lid;
  place('want', 900, 156);
  const w = pop(t, C.l_want - .1, C.l_screen + .1, .4, .35); st($('want'), w.o, 0, 0, w.s); foc('want', dim(t, [C.l_lid]));
  // "MetaTrader 5 app" on the lid
  place('Lmt5', 800, 336);
  const m = rise(t, C.l_meta - .1, b, 20, .35, .35); st($('Lmt5'), m.o, 0, m.y); foc('Lmt5', dim(t, [C.l_screen, C.l_read]) / dim(t, [C.l_watch]) );
  const [mx_, my_, mw, mh] = box('Lmt5'), lp = w2s(YP.sc[0] + 50, YP.y0 - 52);
  leader('mt5', m.o * Math.min(1, dim(t, [C.l_screen]) / dim(t, [C.l_watch])), [mx_, my_ + mh / 2 + m.y], lp, '#cbfb61');
  // the real screen slides in beside your pot; the eye icon is spotlit and tapped
  const pin = ez.out(lin(t, C.l_screen, C.l_screen + .6)), pon = t >= C.l_screen && t < b;
  const ph = $('phone'); ph.style.opacity = pon ? '1' : '0'; ph.style.visibility = pon ? 'visible' : 'hidden';
  const back = ez.inOut(lin(t, C.l_watch - .1, C.l_watch + .4));   // "watch every trade": the focus moves back to your pot
  const pout = ez.inOut(lin(t, b - .5, b));                    // it slides out solid, the way it came in (never a cut)
  ph.style.transform = `perspective(1600px) translateX(${(720 * (1 - pin) + 760 * pout).toFixed(1)}px) rotateY(${(-18 + 18 * pin - 14 * pout).toFixed(2)}deg) scale(${(1 - .04 * back).toFixed(3)})`;
  ph.style.filter = back > .01 ? `brightness(${(1 - .45 * back).toFixed(3)})` : 'none';
  // the eye icon: the screen round it dims, a round loupe magnifies it in place, it is tapped
  const iw = 420, ih = iw * 1024 / 696, ex = 3 + 11 + 11 + EYE[0] * iw, ey = 3 + 11 + 60 + EYE[1] * ih;   // in the phone's own box
  // the loupe (radius 94, its lime ring 6) sits inside the screen glass (x 14..456, y 14..712), over the eye, with the eye magnified in
  // its middle: never over the phone's rim or rounded corner
  const LR = 94, lx = Math.min(ex, 456 - LR - 12), ly = Math.min(ey, 712 - LR - 12);       // 6 px of glass round its ring
  const spot = vis(t, C.l_investor - .15, b, .35, .3) * (1 - back);
  const sx = lx - 3 - 11, sy = ly - 3 - 11;                                                                 // in the screen's box
  $('eyeShade').style.opacity = (.8 * spot).toFixed(3);
  $('eyeShade').style.webkitMaskImage = $('eyeShade').style.maskImage = `radial-gradient(circle 100px at ${sx.toFixed(1)}px ${sy.toFixed(1)}px, transparent 98%, #000 100%)`;
  const lp_ = $('eyeLoupe'), lk = ez.back(lin(t, C.l_investor - .1, C.l_investor + .35)), lo = vis(t, C.l_investor - .1, b, .25, .3) * (1 - back);   // fully gone on "watch every trade"
  lp_.style.left = (lx - LR) + 'px'; lp_.style.top = (ly - LR) + 'px';
  lp_.style.opacity = lo.toFixed(3); lp_.style.visibility = lo > .002 ? 'visible' : 'hidden';
  lp_.style.transform = `scale(${(.25 + .75 * lk - .25 * back).toFixed(3)})`;
  const li = lp_.querySelector('img'), M = 1008 / iw; li.style.left = (LR - EYE[0] * 1008).toFixed(1) + 'px'; li.style.top = (LR - EYE[1] * ih * M).toFixed(1) + 'px';
  const tk = lin(t, C.l_tap, C.l_tap + .6), tp = $('eyeTap');
  tp.style.opacity = (t >= C.l_tap && tk < 1 ? .95 * (1 - tk) : 0).toFixed(3); tp.style.transform = `scale(${(.45 + 1.1 * ez.out(tk)).toFixed(3)})`;
  const hd = $('eyeHand'), hk = ez.out(lin(t, C.l_tap - .5, C.l_tap)), hvv = vis(t, C.l_tap - .5, C.l_watch, .25, .3);
  hd.style.left = (lx - 29) + 'px'; hd.style.top = (ly - 6) + 'px';                                         // it taps the magnified eye
  hd.style.opacity = hvv.toFixed(3); hd.style.visibility = hvv > .002 ? 'visible' : 'hidden';
  hd.style.transform = `translate(${(120 * (1 - hk)).toFixed(1)}px,${(t > C.l_tap - .04 && t < C.l_tap + .16 ? 8 : 70 * (1 - hk)).toFixed(1)}px)`;
  // one chip each: the investor password's path, then read only
  // the close framing puts the lid's handle at y 242: the password chip sits by the phone (above the MetaTrader 5 label), the read
  // only chip beside the lid (top left); neither covers the lid, the stove or the phone
  place('Cpass', 760, 132);
  const cpv = rise(t, C.l_password - .2, b, 20, .4, .35); st($('Cpass'), cpv.o, 0, cpv.y); foc('Cpass', 1 - .35 * back);
  place('Cread', 80, 132);
  const rd = rise(t, C.l_read - .1, b, 20, .35, .35); st($('Cread'), rd.o, 0, rd.y);
}

/* ---------- recap: the hook's two halves return as two columns and tick in on his words; then they fold into your pot ---------- */
function recap(t) {
  const [a, b] = S.recap, fold = C.u_now;
  const ti = rise(t, C.rc_so - .1, fold + .25, 30, .45, .3); st($('rtt'), ti.o, 0, ti.y);
  const [tx_, ty_] = w2s(YP.sc[0], YP.sc[1]);
  [['rcL', C.rc_so + .1, 100, 640], ['rcR', C.rc_so + .25, 780, 1040]].forEach(([id, c, x0, w]) => {
    const e = $(id), v = rise(t, c, b, 40, .45, .01), fk = ez.inOut(lin(t, fold - .05, fold + .55));
    const dx = (tx_ - (x0 + w / 2)) * fk, dy = (ty_ - (262 + 238)) * fk;
    const o = v.o * (1 - ez.inOut(lin(t, fold + .36, fold + .55)));
    e.style.opacity = o.toFixed(3); e.style.visibility = o > .002 ? 'visible' : 'hidden';
    e.style.transform = `perspective(1400px) translate(${dx.toFixed(1)}px,${(v.y + dy).toFixed(1)}px) rotateY(${(70 * fk).toFixed(1)}deg) scale(${(1 - .85 * fk).toFixed(3)})`;
  });
  [['ri1', C.rc_trades], ['ri2', C.rc_money], ['ri3', C.rc_make], ['ri4', C.rc_watch]].forEach(([id, c]) => {
    const e = $(id), k = ez.out(lin(t, c - .15, c + .3));
    e.style.opacity = k.toFixed(3); e.style.transform = `translateY(${(18 * (1 - k)).toFixed(1)}px)`;
    e.querySelector('.ok').style.transform = `scale(${ez.back(lin(t, c, c + .35)).toFixed(3)})`;
  });
  const sp = ez.out(lin(t, C.rc_trades + .2, C.rc_trades + .7)); $('rcSpoon').style.opacity = sp.toFixed(3);
}

/* ---------- now it's your turn: tap any Join JetUP button ---------- */
function turn(t) {
  const [a, b] = S.turn, tt = C.i_press;
  st($('uback'), vis(t, C.u_now, b, .6, .3));                  // a soft dark pool behind the title, the button and the address
  const h = rise(t, C.u_now + .3, b, 40); st($('ut'), h.o, 0, h.y, .94 + .06 * ez.back(lin(t, C.u_now + .3, C.u_now + .8)));
  const j = pop(t, C.u_turn - .12, b, .4, .3); const press = t > tt - .04 && t < tt + .16 ? .95 : 1;
  st($('ujoin'), j.o, 0, 0, j.s * press * (1 + .02 * Math.sin(t * 4)));
  const u = rise(t, C.i_url - .3, b, 30); st($('uurl'), u.o, 0, u.y, 1 + .04 * pulse(t, C.i_url, .6));
  const hk = ez.out(lin(t, C.i_join - .45, tt)), hv = vis(t, C.i_join - .45, b, .25, .3);
  st($('uhand'), hv, 320 * (1 - hk), (t > tt - .04 && t < tt + .16 ? 10 : 0));
  const rk = lin(t, tt, tt + .65); $('uring').style.opacity = (t >= tt && t <= tt + .65 ? .9 * (1 - rk) : 0).toFixed(3);
  $('uring').style.visibility = t >= tt && t <= tt + .65 ? 'visible' : 'hidden'; $('uring').style.transform = `scale(${(.4 + 1.6 * ez.out(rk)).toFixed(3)})`;
}

function scenes(t) {
  st($('top'), vis(t, 0, TL.T + 1, 0, 0));
  world(t); hook(t); hi(t); plate(t); acctLabels(t); copiedLabels(t); yoursLabels(t); lookScreens(t); lidLabels(t); recap(t); turn(t);
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

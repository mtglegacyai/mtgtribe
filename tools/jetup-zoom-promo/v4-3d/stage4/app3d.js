/* JetUP Zoom invitation v4: the 3D layer (three.js). Every object is a pure function of time t.
   Screen layout is in pixels of the 1080x1920 frame; P(x, y) turns a pixel position into world units at z = 0. */
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { TTFLoader } from 'three/addons/loaders/TTFLoader.js';
import { Font } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

const TL = window.TL, C = TL.cues, T = TL.T;
const W = 1080, H = 1920, FOV = 30, DIST = 20;
const U = H / (2 * DIST * Math.tan(FOV * Math.PI / 360));     // pixels per world unit at z = 0
const P = (x, y) => [(x - W / 2) / U, -(y - H / 2) / U];
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const ez = {
  out: x => 1 - Math.pow(1 - x, 3), inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  bounce: x => { const n = 7.5625, d = 2.75; if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75; if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; }
};
function rng(s) { let a = s >>> 0; return () => { a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

/* ---------- renderer, camera, light ---------- */
const R = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: true });
R.setSize(W, H); R.setPixelRatio(1); R.setClearColor(0x000000, 0);
R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.3; R.outputColorSpace = THREE.SRGBColorSpace;
R.domElement.id = 'gl'; document.getElementById('glwrap').appendChild(R.domElement);
const S = new THREE.Scene();
const pm = new THREE.PMREMGenerator(R);
S.environment = pm.fromScene(new RoomEnvironment(), 0.03).texture;
const cam = new THREE.PerspectiveCamera(FOV, W / H, .1, 200); cam.position.set(0, 0, DIST); cam.lookAt(0, 0, 0);
const key = new THREE.DirectionalLight(0xfff4e0, 2.6); key.position.set(4, 6, 9); S.add(key);
const fill = new THREE.DirectionalLight(0xffffff, .9); fill.position.set(-5, -2, 8); S.add(fill);
const rimV = new THREE.DirectionalLight(0xb56cf6, 4.5); rimV.position.set(-7, 3, -5); S.add(rimV);
const rimP = new THREE.DirectionalLight(0xe371fc, 3); rimP.position.set(7, -3, -5); S.add(rimP);
S.add(new THREE.AmbientLight(0xffffff, .25));
const front = new THREE.PointLight(0xffe2a8, 34, 60, 1.6); front.position.set(0, 2, 12); S.add(front);
const ANI = R.capabilities.getMaxAnisotropy();

/* ---------- materials ---------- */
const M = {
  gold: new THREE.MeshPhysicalMaterial({ color: 0xffc85a, metalness: .92, roughness: .2, clearcoat: .7, clearcoatRoughness: .15, envMapIntensity: 2.4, emissive: 0x5a3600, emissiveIntensity: .35 }),
  goldDark: new THREE.MeshPhysicalMaterial({ color: 0xe8b04a, metalness: .95, roughness: .26, envMapIntensity: 2, emissive: 0x3a2200, emissiveIntensity: .3 }),
  lime: new THREE.MeshPhysicalMaterial({ color: 0x6fb800, metalness: 0, roughness: .55, clearcoat: .15, clearcoatRoughness: .4, envMapIntensity: .12, emissive: 0x63a300, emissiveIntensity: .55 }),
  pink: new THREE.MeshPhysicalMaterial({ color: 0xff5f7a, metalness: .05, roughness: .25, clearcoat: 1, emissive: 0x5a0012, emissiveIntensity: .3 }),
  violet: new THREE.MeshPhysicalMaterial({ color: 0x9b7cff, metalness: .1, roughness: .22, clearcoat: 1, clearcoatRoughness: .1, emissive: 0x20104a, emissiveIntensity: .4 }),
  white: new THREE.MeshPhysicalMaterial({ color: 0xf6f3ff, metalness: 0, roughness: .35, clearcoat: .6 }),
  dark: new THREE.MeshPhysicalMaterial({ color: 0x16121f, metalness: .4, roughness: .35, clearcoat: .8 }),
  amber: new THREE.MeshPhysicalMaterial({ color: 0xffb020, metalness: .1, roughness: .25, clearcoat: 1, emissive: 0x4a2a00, emissiveIntensity: .3 }),
  blue: new THREE.MeshPhysicalMaterial({ color: 0x2d8cff, metalness: .05, roughness: .25, clearcoat: 1, emissive: 0x05204a, emissiveIntensity: .35 }),
  wa: new THREE.MeshPhysicalMaterial({ color: 0x25d366, metalness: .05, roughness: .25, clearcoat: 1 }),
};
function canvasTex(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); draw(g, w, h);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = ANI; tx.userData = { c, g, draw }; return tx;
}
function redraw(tx, draw) { const { c, g } = tx.userData; g.clearRect(0, 0, c.width, c.height); draw(g, c.width, c.height); tx.needsUpdate = true; }
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
const glowTex = canvasTex(256, 256, (g, w, h) => { const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, 'rgba(255,220,140,.9)'); gr.addColorStop(.35, 'rgba(255,200,100,.35)'); gr.addColorStop(1, 'rgba(255,200,100,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
const shadowTex = canvasTex(256, 256, (g) => { const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, 'rgba(0,0,0,.75)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256); });
function glow(size, color = 0xffd47a, op = .8) { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color, transparent: true, opacity: op, depthWrite: false, blending: THREE.AdditiveBlending })); s.scale.set(size, size, 1); return s; }
function blob(w, h) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })); return m; }
function setOp(obj, o) {   // fade a whole group (materials are cloned per group where needed)
  obj.visible = o > .003;
  obj.traverse(n => { if (!n.material) return; (Array.isArray(n.material) ? n.material : [n.material]).forEach(m => { if (m.userData.fade) m.opacity = o * m.userData.base; }); });
}
function fadeable(obj) {
  obj.traverse(n => { if (n.material) { const arr = Array.isArray(n.material) ? n.material : [n.material]; const cl = arr.map(m => { const c = m.clone(); c.transparent = true; c.userData = { fade: true, base: m.opacity }; return c; }); n.material = Array.isArray(n.material) ? cl : cl[0]; } });
  return obj;
}

/* ---------- geometry ---------- */
const ingotShape = new THREE.Shape(); ingotShape.moveTo(-1.5, -.42); ingotShape.lineTo(1.5, -.42); ingotShape.lineTo(1.18, .42); ingotShape.lineTo(-1.18, .42); ingotShape.closePath();
const G = {
  ingot: (() => { const g = new THREE.ExtrudeGeometry(ingotShape, { depth: 1.2, bevelEnabled: true, bevelThickness: .07, bevelSize: .07, bevelSegments: 4 }); g.center(); return g; })(),
  coin: new THREE.CylinderGeometry(.62, .62, .12, 64),
  candleBody: new RoundedBoxGeometry(.34, 1, .34, 3, .06),
  wick: new THREE.CylinderGeometry(.035, .035, 1, 8),
};
const coinFace = canvasTex(512, 512, (g, w, h) => {
  const gr = g.createRadialGradient(200, 180, 20, 256, 256, 260); gr.addColorStop(0, '#fff3c4'); gr.addColorStop(.55, '#f2c55a'); gr.addColorStop(1, '#b8862c');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.strokeStyle = 'rgba(120,80,10,.55)'; g.lineWidth = 18; g.beginPath(); g.arc(256, 256, 214, 0, Math.PI * 2); g.stroke();
  g.fillStyle = 'rgba(130,85,10,.75)'; g.font = '400 300px Anton'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$', 256, 270);
});
const coin100Face = canvasTex(512, 512, (g, w, h) => {
  const gr = g.createRadialGradient(200, 180, 20, 256, 256, 260); gr.addColorStop(0, '#fff3c4'); gr.addColorStop(.55, '#f2c55a'); gr.addColorStop(1, '#b8862c');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.strokeStyle = 'rgba(120,80,10,.55)'; g.lineWidth = 16; g.beginPath(); g.arc(256, 256, 220, 0, Math.PI * 2); g.stroke();
  g.fillStyle = 'rgba(110,70,5,.85)'; g.font = '400 200px Anton'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$100', 256, 268);
});
function coinMesh(face = coinFace) {
  const top = new THREE.MeshPhysicalMaterial({ map: face, metalness: .9, roughness: .25, clearcoat: .6, envMapIntensity: 1.3 });
  const m = new THREE.Mesh(G.coin, [M.gold, top, top]); return m;
}
function candle(hgt, up = true) {
  const g = new THREE.Group(); const b = new THREE.Mesh(G.candleBody, up ? M.lime : M.pink); b.scale.y = hgt; g.add(b);
  const w = new THREE.Mesh(G.wick, up ? M.lime : M.pink); w.scale.y = hgt + .7; g.add(w); return g;
}
let font;
function text3d(str, size, mat, depth = .45) {
  const g = new TextGeometry(str, { font, size, height: depth, curveSegments: 8, bevelEnabled: true, bevelThickness: .05, bevelSize: .03, bevelSegments: 3 });
  g.center(); return new THREE.Mesh(g, mat);
}

/* ---------- build every scene ---------- */
const SC = {};
function place(obj, x, y, z = 0) { const [a, b] = P(x, y); obj.position.set(a, b, z); return obj; }

async function build() {
  await document.fonts.load('400 100px Anton'); await document.fonts.load('800 60px Manrope'); await document.fonts.load('700 60px Manrope');
  redraw(coinFace, coinFace.userData.draw); redraw(coin100Face, coin100Face.userData.draw);
  [coinFace, coin100Face].forEach(tx => { tx.center.set(.5, .5); tx.rotation = Math.PI / 2; });
  font = new Font(await new Promise(r => new TTFLoader().load('Anton-Regular.ttf', r)));

  /* S0: gold stack, rising candles, coin rain */
  { const g = new THREE.Group(); S.add(g); SC.s0 = g;
    const stack = new THREE.Group(); place(stack, 540, 1020); stack.scale.setScalar(.62); g.add(stack); SC.stack = stack;
    SC.ingots = [[-1.62, -.5], [1.62, -.5], [0, .52]].map(([x, y], i) => { const m = new THREE.Mesh(G.ingot, M.gold); m.position.set(x, y, 0); m.userData.y = y; stack.add(m); return m; });
    const gl = glow(9, 0xffd47a, .55); gl.position.set(0, .1, -1.5); stack.add(gl);
    const sh = blob(7, 1.6); sh.position.set(0, -1.15, -.8); stack.add(sh);
    SC.candles = []; const hs = [.9, 1.3, 1.0, 1.7, 1.4, 2.1, 2.5];
    hs.forEach((h, i) => { const c = candle(h, i !== 2); place(c, 170 + i * 123, 1060 - h * 55, -6); c.scale.setScalar(.9); c.userData.h = h; g.add(c); SC.candles.push(c); });
    const r = rng(11); SC.rain = [];
    for (let i = 0; i < 16; i++) { const c = coinMesh(); c.userData = { x: (r() - .5) * 6.2, d: r() * .9, sp: 2 + r() * 3, z: -1 + r() * 3, ph: r() * 6 }; g.add(c); SC.rain.push(c); }
  }

  /* S1: crown, flipping invitation ticket, TONIGHT stamp */
  { const g = new THREE.Group(); S.add(g); SC.s1 = g;
    const crown = new THREE.Group(); place(crown, 540, 245, 0); g.add(crown); SC.crown = crown;
    const band = new THREE.Mesh(new THREE.CylinderGeometry(.66, .6, .42, 64, 1, false), M.gold); crown.add(band);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(.64, .06, 12, 64), M.goldDark); ring.rotation.x = Math.PI / 2; ring.position.y = -.2; crown.add(ring);
    for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; const sp = new THREE.Mesh(new THREE.ConeGeometry(.17, .55, 4), M.gold); sp.position.set(Math.sin(a) * .62, .46, Math.cos(a) * .62); sp.rotation.y = a; crown.add(sp);
      const j = new THREE.Mesh(new THREE.SphereGeometry(.085, 16, 12), i % 2 ? M.lime : M.pink); j.position.set(Math.sin(a) * .62, .78, Math.cos(a) * .62); crown.add(j);
      const gem = new THREE.Mesh(new THREE.OctahedronGeometry(.07), i % 2 ? M.pink : M.violet); gem.position.set(Math.sin(a) * .67, 0, Math.cos(a) * .67); crown.add(gem); }
    const cg = glow(3.2, 0xffd47a, .6); cg.position.z = -1; crown.add(cg);
    crown.scale.setScalar(.95);
    // ticket
    const tk = new THREE.Group(); place(tk, 540, 905); g.add(tk); SC.ticket = tk;
    const tw = 5.5, th = 3.55;
    const body = new THREE.Mesh(new RoundedBoxGeometry(tw, th, .16, 6, .22), M.gold); tk.add(body);
    SC.ticketTex = canvasTex(1650, 1065, () => {});
    const face = new THREE.Mesh(new THREE.PlaneGeometry(tw - .18, th - .18), new THREE.MeshBasicMaterial({ map: SC.ticketTex, transparent: true, toneMapped: false }));
    face.position.z = .085; tk.add(face);
    const back = new THREE.Mesh(new THREE.PlaneGeometry(tw - .18, th - .18), new THREE.MeshPhysicalMaterial({ color: 0x241a3a, roughness: .5 })); back.position.z = -.085; back.rotation.y = Math.PI; tk.add(back);
    const tglow = glow(10, 0x9b7cff, .45); tglow.position.z = -1.2; tk.add(tglow);
    const ton = text3d('TONIGHT', .78, M.lime, .36); SC.tonight = ton; place(ton, 540, 1185, .6); g.add(ton);
  }

  /* S2: three 3D clocks */
  { const g = new THREE.Group(); S.add(g); SC.s2 = g; SC.clocks = [];
    const faceTex = canvasTex(512, 512, (g2, w, h) => {
      g2.fillStyle = '#17122a'; g2.beginPath(); g2.arc(256, 256, 256, 0, Math.PI * 2); g2.fill();
      for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2, big = i % 5 === 0; g2.strokeStyle = big ? '#cbfb61' : 'rgba(255,255,255,.35)'; g2.lineWidth = big ? 12 : 4;
        g2.beginPath(); g2.moveTo(256 + Math.sin(a) * (big ? 200 : 218), 256 - Math.cos(a) * (big ? 200 : 218)); g2.lineTo(256 + Math.sin(a) * 236, 256 - Math.cos(a) * 236); g2.stroke(); }
      g2.fillStyle = '#fff'; g2.font = '400 64px Anton'; g2.textAlign = 'center'; g2.textBaseline = 'middle';
      [['12', 0], ['3', 1], ['6', 2], ['9', 3]].forEach(([s, k]) => { const a = k * Math.PI / 2; g2.fillText(s, 256 + Math.sin(a) * 150, 256 - Math.cos(a) * 150 + 4); });
    });
    [540, 880, 1220].forEach((y, i) => {
      const c = new THREE.Group(); place(c, 250, y, .2); g.add(c);
      const rim = new THREE.Mesh(new THREE.TorusGeometry(.82, .1, 24, 72), M.gold); c.add(rim);
      const face = new THREE.Mesh(new THREE.CircleGeometry(.8, 64), new THREE.MeshBasicMaterial({ map: faceTex, toneMapped: false })); face.position.z = -.02; c.add(face);
      const backD = new THREE.Mesh(new THREE.CylinderGeometry(.82, .82, .18, 64), M.dark); backD.rotation.x = Math.PI / 2; backD.position.z = -.12; c.add(backD);
      const hh = new THREE.Mesh(new RoundedBoxGeometry(.11, .5, .05, 2, .03), M.gold); hh.geometry.translate(0, .22, 0); hh.position.z = .06; c.add(hh);
      const mh = new THREE.Mesh(new RoundedBoxGeometry(.07, .72, .05, 2, .025), M.lime); mh.geometry.translate(0, .33, 0); mh.position.z = .1; c.add(mh);
      const cap = new THREE.Mesh(new THREE.SphereGeometry(.09, 20, 14), M.gold); cap.position.z = .14; c.add(cap);
      const gl = glow(3, 0xcbfb61, .25); gl.position.z = -.6; c.add(gl);
      c.userData = { hh, mh }; SC.clocks.push(c);
    });
  }

  /* S3: question mark that turns into a check, live chat bubble */
  { const g = new THREE.Group(); S.add(g); SC.s3 = g;
    const q = text3d('?', 2.4, M.violet.clone(), .6); place(q, 540, 760, 0); g.add(q); SC.q = q;
    const ck = new THREE.Shape(); ck.moveTo(-1.05, .05); ck.lineTo(-.6, .5); ck.lineTo(-.22, .12); ck.lineTo(.78, 1.12); ck.lineTo(1.23, .67); ck.lineTo(-.22, -.78); ck.closePath();
    const check = new THREE.Mesh(new THREE.ExtrudeGeometry(ck, { depth: .45, bevelEnabled: true, bevelThickness: .08, bevelSize: .07, bevelSegments: 4 }), M.lime); check.geometry.center(); place(check, 540, 760, 0); g.add(check); SC.check = check;
    const bs = new THREE.Shape(); const bw = 2.4, bh = 1.5, r0 = .45;
    bs.moveTo(-bw / 2 + r0, -bh / 2); bs.lineTo(-.2, -bh / 2); bs.lineTo(-.65, -bh / 2 - .45); bs.lineTo(-.6, -bh / 2); bs.lineTo(bw / 2 - r0, -bh / 2);
    bs.quadraticCurveTo(bw / 2, -bh / 2, bw / 2, -bh / 2 + r0); bs.lineTo(bw / 2, bh / 2 - r0); bs.quadraticCurveTo(bw / 2, bh / 2, bw / 2 - r0, bh / 2);
    bs.lineTo(-bw / 2 + r0, bh / 2); bs.quadraticCurveTo(-bw / 2, bh / 2, -bw / 2, bh / 2 - r0); bs.lineTo(-bw / 2, -bh / 2 + r0); bs.quadraticCurveTo(-bw / 2, -bh / 2, -bw / 2 + r0, -bh / 2);
    const bub = new THREE.Group(); place(bub, 760, 760, 0); g.add(bub); SC.bubble = bub;
    const bm = new THREE.Mesh(new THREE.ExtrudeGeometry(bs, { depth: .35, bevelEnabled: true, bevelThickness: .06, bevelSize: .05, bevelSegments: 3 }), M.violet); bm.position.z = -.2; bub.add(bm);
    SC.dots = [-.6, 0, .6].map(x => { const d = new THREE.Mesh(new THREE.SphereGeometry(.17, 20, 14), M.white); d.position.set(x, 0, .3); bub.add(d); return d; });
    const live = new THREE.Mesh(new THREE.SphereGeometry(.16, 20, 14), new THREE.MeshPhysicalMaterial({ color: 0xff3048, emissive: 0xff0020, emissiveIntensity: .9, roughness: .3 })); live.position.set(1.05, .62, .3); bub.add(live); SC.liveDot = live;
    const gl = glow(7, 0x9b7cff, .4); gl.position.set(0, 0, -2); g.add(gl); place(gl, 540, 760, -2);
  }

  /* S4: three things: big numbers with their objects */
  { const g = new THREE.Group(); S.add(g); SC.s4 = g; SC.items = [];
    for (let i = 0; i < 3; i++) {
      const it = new THREE.Group(); place(it, 540, 770); g.add(it);
      const n = text3d(String(i + 1), 2.6, M.lime, .7); n.position.set(-1.55, 0, 0); it.add(n);
      const obj = new THREE.Group(); obj.position.set(1.15, 0, 0); it.add(obj);
      const gl = glow(6, i === 1 ? 0xe371fc : 0xffd47a, .45); gl.position.set(1.1, 0, -1.5); it.add(gl);
      it.userData = { n, obj }; SC.items.push(it);
    }
    // 1: a small gold stack with candles
    { const o = SC.items[0].userData.obj; const s = new THREE.Group(); s.scale.setScalar(.55); o.add(s);
      [[-1.62, -.5], [1.62, -.5], [0, .52]].forEach(([x, y]) => { const m = new THREE.Mesh(G.ingot, M.gold); m.position.set(x, y - .8, 0); s.add(m); });
      [1.0, 1.6, 2.2].forEach((h, i) => { const c = candle(h); c.position.set(-1.2 + i * 1.2, 1.4 + h / 2 - .5, -1); s.add(c); });
      SC.item1 = s; }
    // 2: gift box that opens to a $100 coin
    { const o = SC.items[1].userData.obj; const gift = new THREE.Group(); o.add(gift); SC.gift = gift;
      const box = new THREE.Mesh(new RoundedBoxGeometry(1.7, 1.4, 1.7, 4, .08), M.violet); box.position.y = -.45; gift.add(box);
      const rib1 = new THREE.Mesh(new THREE.BoxGeometry(.3, 1.42, 1.72), M.gold); rib1.position.y = -.45; gift.add(rib1);
      const rib2 = new THREE.Mesh(new THREE.BoxGeometry(1.72, 1.42, .3), M.gold); rib2.position.y = -.45; gift.add(rib2);
      const lid = new THREE.Group(); lid.position.set(0, .32, 0); gift.add(lid); SC.lid = lid;
      const lb = new THREE.Mesh(new RoundedBoxGeometry(1.86, .36, 1.86, 4, .08), M.violet); lid.add(lb);
      const lr1 = new THREE.Mesh(new THREE.BoxGeometry(.3, .38, 1.88), M.gold); lid.add(lr1); const lr2 = new THREE.Mesh(new THREE.BoxGeometry(1.88, .38, .3), M.gold); lid.add(lr2);
      const bow1 = new THREE.Mesh(new THREE.TorusGeometry(.26, .09, 12, 32), M.gold); bow1.position.set(-.22, .3, 0); bow1.rotation.set(0, 0, .6); lid.add(bow1);
      const bow2 = bow1.clone(); bow2.position.x = .22; bow2.rotation.z = -.6; lid.add(bow2);
      const c100 = coinMesh(coin100Face); c100.scale.setScalar(1.25); gift.add(c100); SC.coin100 = c100; }
    // 3: a staircase being climbed
    { const o = SC.items[2].userData.obj; const st = new THREE.Group(); o.add(st); SC.stairs = st;
      for (let k = 0; k < 4; k++) { const b = new THREE.Mesh(new RoundedBoxGeometry(.7, .45 * (k + 1), 1.1, 3, .05), k === 3 ? M.lime : M.violet); b.position.set(-1.05 + k * .7, -1 + .225 * (k + 1), 0); st.add(b); }
      const ball = new THREE.Mesh(new THREE.SphereGeometry(.26, 32, 20), M.gold); st.add(ball); SC.ball = ball;
      const flag = new THREE.Group(); flag.position.set(1.05, .9, 0); st.add(flag);
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, 1, 8), M.white); pole.position.y = .5; flag.add(pole);
      const cloth = new THREE.Mesh(new THREE.PlaneGeometry(.55, .35), new THREE.MeshPhysicalMaterial({ color: 0xcbfb61, side: THREE.DoubleSide, emissive: 0x3d5a00, emissiveIntensity: .4 })); cloth.position.set(.3, .82, 0); flag.add(cloth); SC.flag = flag; }
  }

  /* S5: risk triangle, a book that opens, a check */
  { const g = new THREE.Group(); S.add(g); SC.s5 = g;
    const tri = new THREE.Shape(); tri.moveTo(0, .95); tri.lineTo(.95, -.7); tri.lineTo(-.95, -.7); tri.closePath();
    const warn = new THREE.Group(); place(warn, 250, 480, 0); g.add(warn); SC.warn = warn;
    const tm = new THREE.Mesh(new THREE.ExtrudeGeometry(tri, { depth: .35, bevelEnabled: true, bevelThickness: .08, bevelSize: .1, bevelSegments: 4 }), M.amber); tm.geometry.center(); warn.add(tm);
    const ex = text3d('!', .9, M.dark, .2); ex.position.set(0, -.08, .3); warn.add(ex);
    const book = new THREE.Group(); place(book, 250, 810, 0); g.add(book); SC.book = book;
    const cover = new THREE.Mesh(new RoundedBoxGeometry(2.3, 1.5, .08, 2, .03), M.violet); cover.position.z = -.12; book.add(cover);
    const left = new THREE.Group(); book.add(left); const lp = new THREE.Mesh(new RoundedBoxGeometry(1.08, 1.4, .1, 2, .03), M.white); lp.position.x = -.56; left.add(lp);
    const right = new THREE.Group(); book.add(right); const rp = new THREE.Mesh(new RoundedBoxGeometry(1.08, 1.4, .1, 2, .03), M.white); rp.position.x = .56; right.add(rp);
    [left, right].forEach((side, k) => { for (let j = 0; j < 4; j++) { const ln = new THREE.Mesh(new THREE.BoxGeometry(.75, .05, .02), M.violet); ln.position.set((k ? .56 : -.56), .4 - j * .25, .06); side.add(ln); } });
    SC.covers = [left, right];
    const ck = new THREE.Shape(); ck.moveTo(-1.05, .05); ck.lineTo(-.6, .5); ck.lineTo(-.22, .12); ck.lineTo(.78, 1.12); ck.lineTo(1.23, .67); ck.lineTo(-.22, -.78); ck.closePath();
    const ok = new THREE.Mesh(new THREE.ExtrudeGeometry(ck, { depth: .35, bevelEnabled: true, bevelThickness: .07, bevelSize: .06, bevelSegments: 3 }), M.lime); ok.geometry.center(); ok.scale.setScalar(.62); place(ok, 250, 1140, 0); g.add(ok); SC.ok = ok;
  }

  /* S6: a 3D phone typing the link, then a paper plane */
  { const g = new THREE.Group(); S.add(g); SC.s6 = g;
    const ph = new THREE.Group(); place(ph, 540, 840, 0); g.add(ph); SC.phone = ph;
    const pw = 2.5, phh = 5.0;
    const rim = new THREE.Mesh(new RoundedBoxGeometry(pw, phh, .26, 8, .32), M.goldDark); ph.add(rim);
    const bez = new THREE.Mesh(new RoundedBoxGeometry(pw - .08, phh - .08, .27, 8, .28), new THREE.MeshPhysicalMaterial({ color: 0x050407, roughness: .2, clearcoat: 1 })); ph.add(bez);
    SC.screenTex = canvasTex(900, 1860, () => {});
    const scr = new THREE.Mesh(new THREE.PlaneGeometry(pw - .26, phh - .26), new THREE.MeshBasicMaterial({ map: SC.screenTex, transparent: true, toneMapped: false })); scr.position.z = .14; ph.add(scr);
    const pg = glow(9, 0x9b7cff, .45); pg.position.z = -1.5; ph.add(pg);
    const btn = [[-.9, 1.1], [-.9, .55]].map(([x, y]) => { const b = new THREE.Mesh(new RoundedBoxGeometry(.06, .4, .1, 2, .02), M.goldDark); b.position.set(-pw / 2 - .02, y, 0); ph.add(b); return b; });
    // paper plane
    const pl = new THREE.Group(); g.add(pl); SC.plane = pl;
    const geo = new THREE.BufferGeometry();
    const v = [0, 0, 1.2, -.9, 0, -.6, 0, -.08, -.4,   0, 0, 1.2, 0, -.08, -.4, .9, 0, -.6,   0, 0, 1.2, 0, -.08, -.4, 0, -.35, -.5];
    geo.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); geo.computeVertexNormals();
    const pm2 = new THREE.MeshPhysicalMaterial({ color: 0xf2eeff, side: THREE.DoubleSide, roughness: .45, clearcoat: .4, envMapIntensity: .6, flatShading: true });
    const plm = new THREE.Mesh(geo, pm2); plm.scale.setScalar(.9); pl.add(plm);
    SC.trail = [0, 1, 2, 3, 4].map(k => { const sp = glow(.5 - k * .07, 0xcbfb61, .7 - k * .12); g.add(sp); return sp; });
  }

  /* S7: SEE YOU TONIGHT in gold, coin burst */
  { const g = new THREE.Group(); S.add(g); SC.s7 = g;
    const a = text3d('SEE YOU', .82, M.white, .4); place(a, 540, 300, 0); g.add(a); SC.see1 = a;
    const b = text3d('TONIGHT', 1.02, M.gold, .5); place(b, 540, 520, 0); g.add(b); SC.see2 = b;
    const gl = glow(10, 0xffd47a, .45); place(gl, 540, 430, -2); g.add(gl);
    const r = rng(5); SC.burst = [];
    for (let i = 0; i < 12; i++) { const c = coinMesh(); const side = i % 2 ? 1 : -1; c.userData = { vx: side * (2.5 + r() * 3), vy: 3 + r() * 3, vz: -2 - r() * 2, sp: 3 + r() * 5, ph: r() * 6 }; c.scale.setScalar(.5); g.add(c); SC.burst.push(c); }
  }
  [SC.s0, SC.s1, SC.s2, SC.s3, SC.s4, SC.s5, SC.s6, SC.s7].forEach(fadeable);
}

/* ---------- canvas pages: the ticket and the phone screen ---------- */
let ticketState = -1, screenState = null;
function drawTicket(stage) {
  redraw(SC.ticketTex, (g, w, h) => {
    rr(g, 0, 0, w, h, 70); g.save(); g.clip();
    const bg = g.createLinearGradient(0, 0, 0, h); bg.addColorStop(0, '#2a1f48'); bg.addColorStop(1, '#120e1d'); g.fillStyle = bg; g.fillRect(0, 0, w, h);
    const sp = g.createRadialGradient(w / 2, 0, 50, w / 2, 0, 900); sp.addColorStop(0, 'rgba(155,124,255,.45)'); sp.addColorStop(1, 'rgba(155,124,255,0)'); g.fillStyle = sp; g.fillRect(0, 0, w, h);
    g.restore();
    g.textAlign = 'center'; g.textBaseline = 'middle';
    const gold = g.createLinearGradient(0, 120, 0, 300); gold.addColorStop(0, '#fff1bf'); gold.addColorStop(.5, '#ffd47a'); gold.addColorStop(1, '#d19a32');
    g.fillStyle = gold; g.font = '400 200px Anton'; g.fillText("YOU'RE INVITED", w / 2, 215);
    if (stage >= 1) { g.fillStyle = '#fff'; g.font = '800 82px Manrope'; g.fillText('Live JetUP presentation', w / 2, 400); }
    if (stage >= 2) {
      const bw = 520, bh = 120, bx = w / 2 - bw / 2, by = 480; g.fillStyle = 'rgba(45,140,255,.18)'; rr(g, bx, by, bw, bh, 60); g.fill(); g.strokeStyle = '#2d8cff'; g.lineWidth = 6; g.stroke();
      g.fillStyle = '#2d8cff'; rr(g, bx + 18, by + 18, 84, 84, 22); g.fill(); g.fillStyle = '#fff'; rr(g, bx + 34, by + 40, 40, 40, 8); g.fill(); g.beginPath(); g.moveTo(bx + 76, by + 52); g.lineTo(bx + 92, by + 42); g.lineTo(bx + 92, by + 78); g.lineTo(bx + 76, by + 68); g.fill();
      g.fillStyle = '#fff'; g.font = '800 62px Manrope'; g.textAlign = 'left'; g.fillText('ON ZOOM', bx + 128, by + 64); g.textAlign = 'center';
    }
    g.setLineDash([26, 20]); g.strokeStyle = 'rgba(232,194,90,.55)'; g.lineWidth = 8; g.beginPath(); g.moveTo(90, 680); g.lineTo(w - 90, 680); g.stroke(); g.setLineDash([]);
    g.fillStyle = 'rgba(255,255,255,.55)'; g.font = '700 50px Manrope'; g.fillText('SATURDAY 7 NOVEMBER 2026', w / 2, 960);
  });
}
function drawScreen(url, pressed, live) {
  redraw(SC.screenTex, (g, w, h) => {
    rr(g, 0, 0, w, h, 110); g.save(); g.clip();
    const bg = g.createLinearGradient(0, 0, 0, h); bg.addColorStop(0, '#1b1530'); bg.addColorStop(1, '#0b0912'); g.fillStyle = bg; g.fillRect(0, 0, w, h);
    g.fillStyle = '#000'; rr(g, w / 2 - 130, 34, 260, 70, 35); g.fill();                          // camera island
    g.fillStyle = '#fff'; g.font = '700 40px Manrope'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText('20:00', 70, 70);
    g.fillStyle = '#2a2342'; rr(g, 50, 170, w - 100, 120, 60); g.fill();                          // address bar
    g.fillStyle = '#9c95b8'; g.font = '700 38px Manrope'; g.fillText('🔒', 90, 232);
    g.fillStyle = '#fff'; g.font = '800 54px Manrope';
    const parts = url.split('|'); let x = 150; g.fillText(parts[0], x, 232); x += g.measureText(parts[0]).width; if (parts[1]) { g.fillStyle = '#cbfb61'; g.fillText(parts[1], x, 232); x += g.measureText(parts[1]).width; }
    if (url.length && !live) { g.fillStyle = '#cbfb61'; g.fillRect(x + 6, 200, 6, 64); }
    g.textAlign = 'center';
    g.fillStyle = '#2d8cff'; rr(g, w / 2 - 120, 470, 240, 240, 64); g.fill(); g.fillStyle = '#fff'; rr(g, w / 2 - 66, 548, 92, 84, 16); g.fill();
    g.beginPath(); g.moveTo(w / 2 + 34, 572); g.lineTo(w / 2 + 74, 548); g.lineTo(w / 2 + 74, 632); g.lineTo(w / 2 + 34, 608); g.fill();
    g.fillStyle = '#fff'; g.font = '800 70px Manrope'; g.fillText('JetUP presentation', w / 2, 820);
    g.fillStyle = '#cfc8e6'; g.font = '700 46px Manrope'; g.fillText('Tonight, live on Zoom', w / 2, 900);
    const by = 1150, bh = 170; g.fillStyle = pressed ? '#1f6fd6' : '#2d8cff'; rr(g, 90, by + (pressed ? 8 : 0), w - 180, bh, 85); g.fill();
    g.fillStyle = '#fff'; g.font = '800 64px Manrope'; g.fillText(live ? 'Joining…' : 'Join the meeting', w / 2, by + bh / 2 + (pressed ? 8 : 0));
    if (live) { g.fillStyle = 'rgba(203,251,97,.9)'; g.font = '800 46px Manrope'; g.fillText('✓ Opening Zoom', w / 2, by + 280); }
    g.fillStyle = 'rgba(255,255,255,.35)'; rr(g, w / 2 - 150, h - 60, 300, 12, 6); g.fill();
    g.restore();
  });
}

/* ---------- per-frame ---------- */
const SW = window.SCENES;   // scene windows from the DOM engine
function vis(t, a, b, fi = .22, fo = .2) { if (t < a || t > b) return 0; return Math.min(fi <= 0 ? 1 : ez.out(lin(t, a, a + fi)), 1 - ez.inOut(lin(t, b - fo, b))); }
function pop(t, t0, d = .45) { const k = lin(t, t0, t0 + d); return { o: ez.out(lin(t, t0, t0 + .12)), s: Math.max(.001, .3 + .7 * ez.back(k)), k }; }
function render3d(t) {
  const v = k => vis(t, ...SW[k]);
  /* S0 */
  { const o = vis(t, ...SW.s0, 0, .2); setOp(SC.s0, o);
    if (o > 0) {
      SC.stack.rotation.y = -.35 + .5 * Math.sin(t * .9); SC.stack.rotation.x = .28;
      SC.ingots.forEach((m, i) => { const t0 = C.gold0 - .12 + i * .16, k = lin(t, t0, t0 + .55); m.position.y = m.userData.y + 7 * (1 - ez.bounce(k)); m.visible = t >= t0 - .01; });
      SC.candles.forEach((c, i) => { const g = .55 + .45 * ez.out(lin(t, C.works0 - .3 + i * .06, C.works0 + .2 + i * .06)); c.scale.set(1, g, 1); c.rotation.y = t * .6 + i; });
      SC.rain.forEach((c, i) => { const u = c.userData, tt = t - (C.cent - .45) - u.d; c.visible = tt > 0;
        c.position.set(u.x, 1.6 - tt * (3.2 + u.sp * .8), u.z - 2.5); c.rotation.set(tt * u.sp + u.ph, 0, tt * 2 + u.ph); });
    } }
  /* S1 */
  { const o = v('s1'); setOp(SC.s1, o);
    if (o > 0) {
      const cr = pop(t, C.hi - .2, .5); SC.crown.scale.setScalar(.95 * cr.s); SC.crown.rotation.y = t * 1.6; SC.crown.rotation.x = .25;
      const k = lin(t, C.inviting - .3, C.inviting + .45), e = ez.back(k);
      SC.ticket.visible = t >= C.inviting - .3; SC.ticket.rotation.set(.12 * (1 - e) + .05 * Math.sin(t * 1.3), -Math.PI * .85 * (1 - e) + .1 * Math.sin(t * .9), .04 * Math.sin(t * 1.1));
      SC.ticket.position.z = -6 * (1 - ez.out(k)); SC.ticket.scale.setScalar(.6 + .4 * ez.out(k));
      const st = t >= C.zoom - .15 ? 2 : t >= C.live0 - .1 ? 1 : 0; if (st !== ticketState) { drawTicket(st); ticketState = st; }
      const sk = lin(t, C.tonight - .06, C.tonight + .32); SC.tonight.visible = t >= C.tonight - .06;
      SC.tonight.position.z = .6 + 9 * (1 - ez.out(sk)); SC.tonight.rotation.set(0, .15 * Math.sin(t * 2), -.08 + .3 * (1 - ez.out(sk)));
      SC.tonight.scale.setScalar(1 + .25 * Math.sin(Math.PI * lin(t, C.tonight + .25, C.tonight + .5)));
    } }
  /* S2 */
  { const o = v('s2'); setOp(SC.s2, o);
    if (o > 0) {
      const at = [C.eight, C.seven, C.eleven], target = [[8, 0], [7, 0], [11, 30]];
      SC.clocks.forEach((c, i) => { const p = pop(t, at[i] - .25, .5); c.visible = t >= at[i] - .25; c.scale.setScalar(p.s); c.rotation.y = (1 - ez.out(p.k)) * Math.PI * 1.2 + .25 * Math.sin(t * 1.2 + i);
        const k = ez.out(lin(t, at[i] - .1, at[i] + .9)), [hh, mm] = target[i];
        c.userData.mh.rotation.z = -(Math.PI * 2 * (3 + mm / 60)) * k; c.userData.hh.rotation.z = -(Math.PI * 2 * ((hh + mm / 60) / 12)) * k; });
    } }
  /* S3 */
  { const o = v('s3'); setOp(SC.s3, o);
    if (o > 0) {
      const q = pop(t, C.curious - .12, .5), sw = lin(t, C.come - .15, C.come + .25);
      SC.q.visible = t >= C.curious - .12 && sw < 1; SC.q.scale.setScalar(q.s * (1 - ez.inOut(sw)) + .001);
      SC.q.rotation.set(0, t * 1.4 + Math.PI * 2 * ez.inOut(sw), 0);
      const burn = lin(t, C.burned - .45, C.burned - .15); SC.q.material.color.setRGB(.61 + .39 * burn, .49 - .1 * burn, 1 - .55 * burn);
      if (t > C.burned - .45 && t < C.come - .2) SC.q.position.x = P(540, 0)[0] + .08 * Math.sin(t * 60) * (1 - lin(t, C.burned, C.burned + .6));
      const c = pop(t, C.come - .05, .5), mv = ez.inOut(lin(t, C.ask - .3, C.ask + .1));
      SC.check.visible = t >= C.come - .05; SC.check.scale.setScalar(c.s); SC.check.rotation.set(0, (1 - ez.out(c.k)) * Math.PI + .3 * Math.sin(t * 1.3), 0);
      SC.check.position.x = P(540 - 220 * mv, 0)[0];
      const b = pop(t, C.ask - .15, .5); SC.bubble.visible = t >= C.ask - .15; SC.bubble.scale.setScalar(.85 * b.s); SC.bubble.rotation.set(.1, -.3 + .15 * Math.sin(t * 1.4), 0);
      SC.bubble.position.x = P(780, 0)[0];
      SC.dots.forEach((d, i) => { d.position.y = .12 * Math.max(0, Math.sin(t * 9 - i * .9)); });
      SC.liveDot.scale.setScalar(1 + .25 * Math.max(0, Math.sin(t * 7)));
    } }
  /* S4 */
  { const o = v('s4'); setOp(SC.s4, o);
    if (o > 0) {
      const at = [C.one, C.two, C.threeP];
      SC.items.forEach((it, i) => { const a = at[i] - .12, b = i < 2 ? at[i + 1] - .2 : 1e9, k = lin(t, a, a + .45), x = lin(t, b, b + .35);
        it.visible = t >= a && t < b + .36; const e = ez.back(k);
        it.position.x = P(540, 0)[0] + 9 * (1 - ez.out(k)) - 9 * ez.inOut(x); it.scale.setScalar(.6 + .4 * e - .3 * x);
        it.userData.n.rotation.y = (1 - ez.out(k)) * Math.PI * 2 + .25 * Math.sin(t * 1.5);
        it.userData.obj.rotation.y = -.5 + .5 * Math.sin(t * .9 + i); it.userData.obj.rotation.x = .2; });
      const op = lin(t, C.hundred - .3, C.hundred + .15); SC.lid.position.y = .32 + .75 * ez.out(op); SC.lid.rotation.set(0, 0, 1.1 * ez.out(op)); SC.lid.position.x = -1.15 * ez.out(op);
      const cu = ez.back(lin(t, C.hundred - .15, C.hundred + .45)); SC.coin100.visible = t >= C.hundred - .15; SC.coin100.position.set(0, -.4 + 1.9 * cu, .2);
      SC.coin100.rotation.set(Math.PI / 2, 0, (1 - lin(t, C.hundred - .15, C.hundred + 1.2)) * Math.PI * 4);
      const hop = lin(t, C.started - .3, C.right + .2), steps = 4, s = Math.min(steps - 1e-6, hop * steps), si = Math.floor(s), f = s - si;
      const sx = -1.05 + si * .7 + .7 * f * (si < 3 ? 1 : 0), base = (si + 1) * .45 - 1 + .26, nb = (Math.min(si + 2, 4)) * .45 - 1 + .26;
      SC.ball.position.set(hop <= 0 ? -1.05 : sx, hop <= 0 ? .45 - 1 + .26 : base + (nb - base) * f + .55 * Math.sin(Math.PI * f), 0);
      SC.flag.rotation.y = .3 * Math.sin(t * 3);
    } }
  /* S5 */
  { const o = v('s5'); setOp(SC.s5, o);
    if (o > 0) {
      const w = pop(t, C.trading - .1), b = pop(t, C.learnF - .2), c = pop(t, C.decide - .35);
      SC.warn.visible = t >= C.trading - .1; SC.warn.scale.setScalar(.75 * w.s); SC.warn.rotation.set(0, (1 - ez.out(w.k)) * Math.PI + .3 * Math.sin(t * 1.6), .05 * Math.sin(t * 8) * (1 - lin(t, C.risk, C.risk + .8)));
      SC.book.visible = t >= C.learnF - .2; SC.book.scale.setScalar(.85 * b.s); SC.book.rotation.set(.25, -.35 + .2 * Math.sin(t), 0);
      const op = ez.out(lin(t, C.learnF - .1, C.learnF + .5)); SC.covers[0].rotation.y = -.3 * op + 1.5 * (1 - op); SC.covers[1].rotation.y = .3 * op - 1.5 * (1 - op);
      SC.ok.visible = t >= C.decide - .35; SC.ok.scale.setScalar(.62 * c.s); SC.ok.rotation.set(0, (1 - ez.out(c.k)) * Math.PI * 2 + .3 * Math.sin(t * 1.5), 0);
    } }
  /* S6 */
  { const o = v('s6'); setOp(SC.s6, o);
    if (o > 0) {
      const k = pop(t, C.join - .05, .55), mv = ez.inOut(lin(t, C.send - .3, C.send + .2));
      SC.phone.scale.setScalar(.95 * k.s * (1 - .18 * mv)); SC.phone.position.x = P(540 - 250 * mv, 0)[0];
      SC.phone.rotation.set(.08 + .03 * Math.sin(t * 1.2), -.28 + .5 * (1 - ez.out(k.k)) + .08 * Math.sin(t * .9) + .15 * mv, .02 * Math.sin(t));
      const seq = [[C.mtgU, 'mtg'], [C.tribe, 'mtgtribe'], [C.dot, 'mtgtribe.'], [C.com, 'mtgtribe.com'], [C.slash, 'mtgtribe.com/'], [C.jet, 'mtgtribe.com/|JetUp'], [C.zoomU, 'mtgtribe.com/|JetUpZoom']];
      let url = ''; seq.forEach(([a, s]) => { if (t >= a - .03) url = s; });
      const tap = C.zoomU + .55, pressed = t >= tap && t < tap + .35, live = t >= tap + .35;
      const key2 = url + pressed + live + (Math.floor(t * 3) % 2); if (key2 !== screenState) { drawScreen(url, pressed, live); screenState = key2; }
      const pf = lin(t, C.someone - .3, C.someone + 1.0), [px, py] = P(330, 700), [qx, qy] = P(1180, 470);
      SC.plane.visible = pf > 0 && pf < 1; const e2 = ez.inOut(pf);
      SC.trail.forEach((sp, k) => { const q = clamp(pf - (k + 1) * .045), e3 = ez.inOut(q); sp.visible = SC.plane.visible && q > 0; sp.position.set(px + (qx - px) * e3, py + (qy - py) * e3 + .5 * Math.sin(Math.PI * q), 1.9); }); SC.plane.position.set(px + (qx - px) * e2, py + (qy - py) * e2 + .5 * Math.sin(Math.PI * pf), 2);
      SC.plane.rotation.set(.75 + .2 * Math.sin(pf * 7), Math.PI / 2 - .55, .55 + .12 * Math.sin(pf * 9)); SC.plane.scale.setScalar(.72);
    } }
  /* S7 */
  { const o = v('s7', .3, .01); setOp(SC.s7, o);
    if (o > 0) {
      const a = pop(t, C.see - .12, .55), b = pop(t, C.see + .05, .6);
      SC.see1.scale.setScalar(a.s); SC.see1.rotation.set(.1 * Math.sin(t), (1 - ez.out(a.k)) * Math.PI + .12 * Math.sin(t * 1.1), 0);
      SC.see2.scale.setScalar(b.s); SC.see2.rotation.set(.12 * Math.sin(t * .8), (1 - ez.out(b.k)) * -Math.PI + .15 * Math.sin(t * .9 + 1), 0);
      SC.burst.forEach(c => { const u = c.userData, tt = t - C.see - .05; c.visible = tt > 0 && tt < 1.2; c.scale.setScalar(.5 * (1 - lin(tt, .8, 1.2))); const [x0, y0] = P(540, 430);
        c.position.set(x0 + u.vx * tt, y0 + u.vy * tt - 9 * tt * tt, u.vz); c.rotation.set(tt * u.sp + u.ph, tt * 2, 0); });
    } }
  R.render(S, cam);
}

await build();
window.R = function (t) { window.RD(t); render3d(t); };
window.READY = true;

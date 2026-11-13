// OlyLife THz Tera-P90, modelled in three.js for MTG's survey video (our own 3D illustration, no third-party photos).
// White rounded body, champagne-bronze base band, two brushed metal foot plates, dark display strip "30  01".
import * as THREE from 'three';
import { RoundedBoxGeometry } from '../node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from '../node_modules/three/examples/jsm/environments/RoomEnvironment.js';

function roundedRectShape(w, d, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -d / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + d - r); s.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
  s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s;
}
function brushedTexture() {
  const c = document.createElement('canvas'); c.width = 512; c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#8a8a8a'; g.fillRect(0, 0, 512, 512);
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 2600; i++) {
    const y = rnd() * 512, v = 110 + rnd() * 70; g.strokeStyle = `rgba(${v},${v},${v},${0.10 + rnd() * 0.18})`;
    g.lineWidth = 0.5 + rnd() * 1.4; g.beginPath(); g.moveTo(0, y); g.lineTo(512, y + (rnd() - 0.5) * 3); g.stroke();
  }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(1, 1); return t;
}
function displayTexture() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 200; const g = c.getContext('2d');
  const grd = g.createLinearGradient(0, 0, 0, 200); grd.addColorStop(0, '#1b1f22'); grd.addColorStop(1, '#070909');
  g.fillStyle = grd; g.fillRect(0, 0, 1024, 200);
  g.fillStyle = 'rgba(255,255,255,0.06)'; g.fillRect(0, 0, 1024, 70);
  g.font = 'bold 120px "Oswald", sans-serif'; g.textBaseline = 'middle'; g.textAlign = 'center';
  g.shadowColor = 'rgba(190,255,220,0.9)'; g.shadowBlur = 22; g.fillStyle = '#f2fff7';
  g.fillText('30', 300, 104); g.fillText('01', 720, 104);
  g.font = 'bold 34px "Montserrat", sans-serif'; g.shadowBlur = 10; g.fillStyle = '#cfeee0';
  g.fillText('MIN', 300, 178); g.fillText('LEVEL', 720, 178);
  g.lineWidth = 6; g.strokeStyle = '#e8fff2'; g.shadowBlur = 12;
  g.beginPath(); g.arc(120, 100, 30, 0, Math.PI * 2); g.stroke(); g.fillStyle = '#e8fff2'; g.fillRect(105, 97, 30, 6);
  g.beginPath(); g.arc(510, 100, 26, 0, Math.PI * 2); g.stroke(); g.fillRect(498, 97, 24, 6);
  g.strokeStyle = '#3ddc84'; g.shadowColor = '#3ddc84'; g.shadowBlur = 26; g.lineWidth = 8;
  g.beginPath(); g.arc(905, 100, 34, -Math.PI / 2 + 0.6, Math.PI * 1.5 - 0.6); g.stroke();
  g.beginPath(); g.moveTo(905, 58); g.lineTo(905, 98); g.stroke();
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function shadowTexture() {
  const c = document.createElement('canvas'); c.width = 256; c.height = 256; const g = c.getContext('2d');
  const grd = g.createRadialGradient(128, 128, 10, 128, 128, 128);
  grd.addColorStop(0, 'rgba(0,0,0,0.75)'); grd.addColorStop(0.55, 'rgba(0,0,0,0.35)'); grd.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256); return new THREE.CanvasTexture(c);
}

export function makeDevice(canvas, W, H) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const camera = new THREE.PerspectiveCamera(30, W / H, 0.1, 100);

  const dev = new THREE.Group(); scene.add(dev);
  const white = new THREE.MeshPhysicalMaterial({ color: 0xf7f8f6, roughness: 0.28, clearcoat: 0.8, clearcoatRoughness: 0.12 });
  const bronze = new THREE.MeshPhysicalMaterial({ color: 0xa98063, metalness: 0.7, roughness: 0.4, clearcoat: 0.3 });
  const bt = brushedTexture();
  const plateMat = new THREE.MeshPhysicalMaterial({ color: 0xa39386, metalness: 0.5, roughness: 0.6, roughnessMap: bt,
    anisotropy: 0.7, envMapIntensity: 0.4 });
  const trayMat = new THREE.MeshPhysicalMaterial({ color: 0xdedfdc, roughness: 0.45, clearcoat: 0.4 });

  const body = new THREE.Mesh(new RoundedBoxGeometry(3.8, 0.95, 3.7, 8, 0.42), white); body.position.y = 0.62; dev.add(body);
  const band = new THREE.Mesh(new RoundedBoxGeometry(3.86, 0.28, 3.76, 8, 0.14), bronze); band.position.y = 0.16; dev.add(band);
  // shallow tray on top
  const trayG = new THREE.ExtrudeGeometry(roundedRectShape(3.3, 2.95, 0.55), { depth: 0.03, bevelEnabled: true, bevelThickness: 0.02, bevelSize: 0.03, bevelSegments: 4, curveSegments: 24 });
  trayG.rotateX(-Math.PI / 2); const tray = new THREE.Mesh(trayG, trayMat); tray.position.set(0, 1.08, -0.22); dev.add(tray);
  // two plates (slightly foot shaped: rounded, narrower at the heel)
  const plateG = new THREE.ExtrudeGeometry(roundedRectShape(1.38, 2.62, 0.5), { depth: 0.035, bevelEnabled: true, bevelThickness: 0.025, bevelSize: 0.03, bevelSegments: 5, curveSegments: 28 });
  plateG.rotateX(-Math.PI / 2);
  for (const sx of [-1, 1]) { const p = new THREE.Mesh(plateG, plateMat); p.position.set(sx * 0.78, 1.12, -0.24); dev.add(p); }
  // centre ridge
  const ridge = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.08, 2.4, 4, 0.04), white); ridge.position.set(0, 1.15, -0.24); dev.add(ridge);
  // display strip at the front of the top
  const dispTex = displayTexture();
  const disp = new THREE.Mesh(new RoundedBoxGeometry(1.9, 0.05, 0.42, 4, 0.02),
    [trayMat, trayMat, new THREE.MeshPhysicalMaterial({ map: dispTex, emissiveMap: dispTex, emissive: 0xffffff, emissiveIntensity: 0.55, roughness: 0.15, clearcoat: 1 }), trayMat, trayMat, trayMat]);
  disp.position.set(0, 1.115, 1.5); dev.add(disp);
  // contact shadow
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(6.4, 6.0), new THREE.MeshBasicMaterial({ map: shadowTexture(), transparent: true, depthWrite: false }));
  sh.rotation.x = -Math.PI / 2; sh.position.y = 0.005; dev.add(sh);

  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(4, 8, 6); scene.add(key);
  const rim = new THREE.DirectionalLight(0x5dff9a, 1.5); rim.position.set(-6, 3, -6); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xd8ffe9, 0.6); fill.position.set(-5, 2, 5); scene.add(fill);
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));

  // pose: {cx, cy} centre on the frame (px), {size} width in px, {yaw, pitch} in radians, {a} opacity (canvas css)
  function render(pose) {
    const { cx, cy, size, yaw, pitch } = pose;
    const dist = 16; camera.position.set(0, Math.sin(pitch) * dist, Math.cos(pitch) * dist); camera.lookAt(0, 0.6, 0);
    // place the device so that its centre lands on (cx, cy): shift the camera's view via setViewOffset
    const fh = 2 * dist * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)); // world height at the target
    const worldPerPx = fh / H; const s = (size * worldPerPx) / 4.4; dev.scale.setScalar(s); dev.rotation.y = yaw;
    camera.setViewOffset(W, H, -(cx - W / 2), -(cy - H / 2), W, H); camera.updateProjectionMatrix();
    renderer.render(scene, camera);
  }
  return { render };
}

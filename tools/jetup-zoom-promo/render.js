// Render frames of the JetUP Zoom promo. Usage: node render.js test t1,t2,...   |   node render.js range <from> <to> <outDir>
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const STAGE = 'file://' + path.join(__dirname, 'stage', 'stage.html');
(async () => {
  const mode = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto(STAGE, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const ok = await p.evaluate(() => ['400 40px Anton', '800 40px Manrope', '40px "Noto Color Emoji"'].map(f => document.fonts.check(f)));
  if (ok.includes(false)) { console.error('FONTS MISSING', ok); process.exit(2); }
  // warm up every image so no frame shows a half-decoded picture
  await p.evaluate(async () => { await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  const fps = await p.evaluate(() => window.TL.fps), T = await p.evaluate(() => window.TL.T);
  if (mode === 'test') {
    const ts = process.argv[3].split(',').map(Number), out = process.argv[4] || path.join(__dirname, 'test');
    fs.mkdirSync(out, { recursive: true });
    for (const t of ts) { await p.evaluate(t => window.R(t), t); await p.screenshot({ path: path.join(out, `t${t.toFixed(2)}.jpg`), type: 'jpeg', quality: 90 }); }
  } else {
    const from = +process.argv[3], to = Math.min(+process.argv[4], Math.round(T * fps)), out = process.argv[5];
    fs.mkdirSync(out, { recursive: true });
    for (let f = from; f < to; f++) {
      await p.evaluate(t => window.R(t), f / fps);
      await p.screenshot({ path: path.join(out, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 95 });
    }
    console.log('done', from, to);
  }
  await b.close();
})();

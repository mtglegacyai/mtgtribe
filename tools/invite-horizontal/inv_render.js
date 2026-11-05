// usage: node inv_render.js <fromFrame> <toFrame> <outDir> [step]
const { chromium } = require('playwright');
const [from, to, outDir, step] = [+process.argv[2], +process.argv[3], process.argv[4], +(process.argv[5] || 1)];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://localhost:8790/stage.html', { waitUntil: 'load' });
  await p.evaluate(async () => {
    await Promise.all(['400 40px Anton', '400 40px Manrope', '600 40px Manrope', '700 40px Manrope', '800 40px Manrope', 'italic 600 40px Manrope', '500 40px "JetBrains Mono"', '700 40px "JetBrains Mono"', '400 40px "Great Vibes"'].map(f => document.fonts.load(f)));
    await Promise.all(['site-altruva.jpg', 'site-tribe.jpg', 'site-dash.jpg'].map(u => { const i = new Image(); i.src = u; return i.decode(); }));
    E.prebuild();
  });
  const t0 = Date.now(); let n = 0;
  for (let f = from; f < to; f += step) {
    await p.evaluate(t => window.renderAt(t), f / 30);
    await p.screenshot({ path: `${outDir}/${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 93 });
    n++;
  }
  if (errs.length) console.log('ERRORS', errs.slice(0, 5));
  console.log(`rendered ${n} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  await b.close();
})();

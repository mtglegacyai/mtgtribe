// usage: node inv_test.js outDir "o:1.2,s:7.5,..."   (o = output time, s = source voice time)
const { chromium } = require('playwright');
const [outDir, list] = [process.argv[2], process.argv[3]];
(async () => {
  const b = await chromium.launch();
  const VERT = process.env.ORIENT === 'v';
  const p = await b.newPage({ viewport: VERT ? { width: 1080, height: 1920 } : { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://localhost:8790/' + (VERT ? 'stage_v.html' : 'stage.html'), { waitUntil: 'load' });
  await p.evaluate(async () => {
    await Promise.all(['400 40px Anton', '400 40px Manrope', '600 40px Manrope', '700 40px Manrope', '800 40px Manrope', 'italic 600 40px Manrope', '500 40px "JetBrains Mono"', '700 40px "JetBrains Mono"', '400 40px "Great Vibes"'].map(f => document.fonts.load(f)));
    await Promise.all(['site-altruva.jpg', 'site-tribe.jpg', 'site-dash.jpg'].map(u => { const i = new Image(); i.src = u; return i.decode(); }));
    E.prebuild();
  });
  for (const item of list.split(',')) {
    const [k, v] = item.split(':'); const t = k === 's' ? await p.evaluate(x => E.S(x), +v) : +v;
    await p.evaluate(t => window.renderAt(t), t);
    await p.screenshot({ path: `${outDir}/${k}${v}.jpg`, type: 'jpeg', quality: 80 });
  }
  console.log('errors', errs.slice(0, 8));
  await b.close();
})();

// Render the hero background. Usage: node render.js test t1,t2.. [w h]  |  node render.js range <from> <to> <outDir> [w h]
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const mode = process.argv[2]; const [w, h] = mode === 'test' ? [+(process.argv[4] || 1920), +(process.argv[5] || 1080)] : [+(process.argv[6] || 1920), +(process.argv[7] || 1080)];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto(`http://127.0.0.1:8772/stage/index.html?w=${w}&h=${h}` + (process.env.Q ? '&' + process.env.Q : ''), { waitUntil: 'networkidle' });
  await p.waitForFunction(() => window.READY === true, null, { timeout: 180000 });
  const fps = 30, T = await p.evaluate(() => window.TL.T);
  if (mode === 'test') { const out = path.join(__dirname, 'test'); fs.mkdirSync(out, { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) { await p.evaluate(t => window.R(t), t); await p.screenshot({ path: path.join(out, `t${t.toFixed(2)}_${w}${process.env.TAG ? '_' + process.env.TAG : ''}.jpg`), type: 'jpeg', quality: 92 }); } }
  else { const from = +process.argv[3], to = Math.min(+process.argv[4], Math.round(T * fps)), out = process.argv[5]; fs.mkdirSync(out, { recursive: true });
    for (let f = from; f < to; f++) { await p.evaluate(t => window.R(t), f / fps); await p.screenshot({ path: path.join(out, `f${String(f).padStart(4, '0')}.png`), type: 'png' }); }
    console.log('done', from, to); }
  await b.close();
})();

// node render.js stills <out dir> t1 t2 ...   |   node render.js range <f0> <f1> <out dir>
const { chromium } = require('playwright');
(async () => {
  const [mode, ...rest] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--font-render-hinting=none'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('pageerror:', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  await p.goto('http://127.0.0.1:8765/stage/stage.html'); await p.waitForFunction('window.ready===true', null, { timeout: 120000 });
  const shot = async (t, path) => { await p.evaluate(t => window.render(t), t); await p.screenshot({ path, type: 'jpeg', quality: 93 }); };
  if (mode === 'stills') { const [dir, ...ts] = rest; for (const t of ts) await shot(+t, `${dir}/t${(+t).toFixed(2)}.jpg`); }
  else if (mode === 'sfx') { console.log(JSON.stringify(await p.evaluate(() => ({ sfx: window.SFX, scenes: window.SCENES, T: window.TL.T })))); }
  else if (mode === 'list') { const [file, dir] = rest; const fs = JSON.parse(require('fs').readFileSync(file)); const fps = await p.evaluate(() => window.TL.fps); const t0 = Date.now();
    for (const f of fs) { await shot(f / fps, `${dir}/f${String(f).padStart(5, '0')}.jpg`); if (f % 100 === 0) console.log('frame', f, ((Date.now() - t0) / 1000).toFixed(0) + 's'); } }
  else { const [f0, f1, dir] = rest; const fps = await p.evaluate(() => window.TL.fps); const t0 = Date.now();
    for (let f = +f0; f < +f1; f++) { await shot(f / fps, `${dir}/f${String(f).padStart(5, '0')}.jpg`); if (f % 200 === 0) console.log('frame', f, ((Date.now() - t0) / 1000).toFixed(0) + 's'); } }
  await b.close();
})();

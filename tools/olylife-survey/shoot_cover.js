const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('pageerror', e.message));
  await p.goto('http://127.0.0.1:8765/stage/cover.html'); await p.waitForFunction('window.ready===true', null, { timeout: 60000 });
  await p.waitForTimeout(500);
  await p.screenshot({ path: 'out/tiktok-cover.png' }); await b.close();
})();

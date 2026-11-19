const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('pageerror', e => console.log('pageerror', e.message));
  await p.goto('http://127.0.0.1:8765/stage/yt_thumb.html'); await p.waitForFunction('window.ready===true', null, { timeout: 30000 }); await p.waitForTimeout(400);
  await p.screenshot({ path: 'out/yt_thumb.png' }); await b.close();
})();

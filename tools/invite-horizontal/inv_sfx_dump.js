const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('http://localhost:8790/stage.html', { waitUntil: 'load' });
  const j = await p.evaluate(() => { E.prebuild(); return JSON.stringify({ sfx: window.SFX, total: E.TOTAL, co: E.CO, s110: E.S(110.4) }); });
  require('fs').writeFileSync(process.argv[2], j); console.log(JSON.parse(j).sfx.length, 'cues');
  await b.close();
})();

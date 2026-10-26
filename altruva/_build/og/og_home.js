// Social preview image for mtgtribe.com (1200x630): the real home page hero, drawn still (reduced motion),
// with the buttons swapped for a short line and the join address. Usage: node og/og_home.js OUT.png
// Serves out/prod on :8771; Google Fonts are answered from local copies (the sandbox cannot reach them).
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = '/home/claude/site/out/prod', OUT = process.argv[2] || '/tmp/og-home.png';
const FONTS = { 'dm-sans': '/tmp/claude-0/-home-claude/dc91e5da-c02d-54a0-a639-05ec78f3d408/scratchpad/fonts/node_modules/@fontsource/dm-sans/files/',
  'outfit': '/tmp/claude-0/-home-claude/dc91e5da-c02d-54a0-a639-05ec78f3d408/scratchpad/fonts/node_modules/@fontsource/outfit/files/',
  'jetbrains-mono': '/tmp/claude-0/-home-claude/dc91e5da-c02d-54a0-a639-05ec78f3d408/scratchpad/fonts/node_modules/@fontsource/jetbrains-mono/files/' };
const css = [['DM Sans', 'dm-sans', [400, 500, 600, 700, 800]], ['Outfit', 'outfit', [700, 800]], ['JetBrains Mono', 'jetbrains-mono', [500]]]
  .map(([f, s, ws]) => ws.map(w => `@font-face{font-family:'${f}';font-weight:${w};src:url(https://fonts.gstatic.com/l/${s}/${w}.woff2)}`).join('\n')).join('\n');
const types = { '.html': 'text/html', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p); if (!fs.existsSync(f) || /\.mp4$/.test(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); }).listen(8771);
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  const pg = await ctx.newPage();
  await pg.route('https://fonts.googleapis.com/**', r => r.fulfill({ status: 200, contentType: 'text/css', body: css }));
  await pg.route('https://fonts.gstatic.com/**', r => { const m = r.request().url().match(/\/l\/([\w-]+)\/(\d+)/);
    r.fulfill({ status: 200, contentType: 'font/woff2', body: fs.readFileSync(`${FONTS[m[1]]}${m[1]}-latin-${m[2]}-normal.woff2`) }); });
  await pg.goto('http://localhost:8771/', { waitUntil: 'load' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.addStyleTag({ content: `
    .top .ring,.ctas,.live,.ticker,.skip,.invite,.open,.foot{display:none!important}
    .hero{min-height:630px!important;height:630px;padding:58px 0 96px!important}
    .nav{height:84px}.brand{font-size:17px}.brand img{width:44px;height:44px}
    .kicker{margin-bottom:22px}
    .l1{font-size:62px}.l2{font-size:150px}
    .lede{margin-top:22px;font-size:22px;max-width:none;color:#d4d7dc}
    .horizon{top:calc(100% - 86px)}
    .ogfoot{position:absolute;left:56px;right:56px;bottom:26px;display:flex;justify-content:space-between;align-items:center;z-index:3;font:700 21px/1 'DM Sans',sans-serif;color:#d7dade}
    .ogfoot i{display:inline-block;width:11px;height:11px;border-radius:50%;background:#3ddc84;box-shadow:0 0 10px #3ddc84;margin-right:12px;vertical-align:1px}
    .ogfoot b{color:#e8b862}
    .ogfoot span:last-child{font:500 19px/1 'JetBrains Mono',monospace;letter-spacing:.08em;color:#f2ad3c}` });
  await pg.evaluate(() => {
    document.querySelector('.lede').textContent = 'Tutorials, explainers, free tools and honest guides by MTG, Your Digital Architect.';
    const f = document.createElement('div'); f.className = 'ogfoot';
    f.innerHTML = '<span><i></i>Join the tribe: <b>mtgtribe.com/group</b></span><span>mtgtribe.com</span>';
    document.getElementById('hero').appendChild(f); window.dispatchEvent(new Event('resize')); });
  await pg.waitForTimeout(600);
  await pg.screenshot({ path: OUT, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  await b.close(); srv.close();
})();

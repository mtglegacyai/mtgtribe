// Shoot the 16:9 cover of JetUP explainer 9 (What "copying" really means); it is also the video's poster and thumbnail on the site.
// Usage: node shoot_cover.js [outDir]   (default: this folder)
// Writes cover-explainer-what-copying-really-means.jpg (1920x1080) and .webp (1280x720), each kept under 200 KB.
// Fails (exit 2) if a font or an image did not load, so a cover is never shot with fallback fonts or a missing JetUP disc.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs'); const { execFileSync } = require('child_process');
const NAME = 'cover-explainer-what-copying-really-means';
(async () => {
  const out = process.argv[2] || __dirname; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.join(__dirname, 'cover.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const fonts = await p.evaluate(async () => {
    await Promise.all(['400 132px Anton', '800 48px Manrope', '48px "Noto Color Emoji"'].map(f => document.fonts.load(f).catch(() => [])));
    const st = fam => [...document.fonts].filter(f => f.family.replace(/"/g, '') === fam).map(f => f.status);
    return { anton: st('Anton'), manrope: st('Manrope'), emoji: document.fonts.check('48px "Noto Color Emoji"') };
  });
  if (!fonts.anton.includes('loaded') || !fonts.manrope.includes('loaded') || !fonts.emoji) { console.error('FONTS MISSING', JSON.stringify(fonts)); process.exit(2); }
  const imgs = await p.evaluate(async () => { await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
    return [...document.images].map(i => [i.getAttribute('src'), i.naturalWidth]); });
  if (!imgs.length || imgs.some(([, w]) => !w)) { console.error('IMAGE MISSING', JSON.stringify(imgs)); process.exit(2); }
  if (errs.length) { console.error('PAGE ERROR', errs.join(' | ')); process.exit(2); }
  const png = await p.screenshot({ type: 'png' });
  await b.close();
  const py = `import io, os, sys
from PIL import Image
im = Image.open(io.BytesIO(sys.stdin.buffer.read())).convert('RGB'); assert im.size == (1920, 1080), im.size
jpg, webp = sys.argv[1], sys.argv[2]
for q in (88, 86, 84, 82, 80):
    im.save(jpg, quality=q, optimize=True, progressive=True)
    if os.path.getsize(jpg) <= 200 * 1024: break
sm = im.resize((1280, 720), Image.LANCZOS)
for q in (84, 80, 76, 72):
    sm.save(webp, quality=q, method=6)
    if os.path.getsize(webp) <= 200 * 1024: break
for f in (jpg, webp): print(os.path.basename(f), Image.open(f).size, round(os.path.getsize(f) / 1024), 'KB')`;
  process.stdout.write(execFileSync('python3', ['-c', py, path.join(out, NAME + '.jpg'), path.join(out, NAME + '.webp')], { input: png }));
})();

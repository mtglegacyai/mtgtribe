// Shoot a YouTube thumbnail: node tools/youtube-thumbnails/shoot.js <folder>
// Renders <folder>/thumb.html at 1920x1080, then writes <folder>/thumbnail.jpg at 1280x720 (YouTube's size, under 2 MB)
// and <folder>/thumbnail-320.png, the phone-size check (it must still read at 320 px wide).
const { chromium } = require('playwright'); const path = require('path'); const { execFileSync } = require('child_process');
(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(dir, 'thumb.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  for (const f of ['400 100px Anton', '800 40px Manrope', '40px "Noto Color Emoji"']) await p.evaluate(f => document.fonts.load(f), f);
  const png = path.join(dir, 'thumb.png'); await p.screenshot({ path: png }); await b.close();
  execFileSync('python3', ['-c', `from PIL import Image;import os,sys
d=sys.argv[1];im=Image.open(os.path.join(d,'thumb.png')).convert('RGB').resize((1280,720),Image.LANCZOS)
im.save(os.path.join(d,'thumbnail.jpg'),quality=90);im.resize((320,180),Image.LANCZOS).save(os.path.join(d,'thumbnail-320.png'))
os.remove(os.path.join(d,'thumb.png'));print('thumbnail.jpg',os.path.getsize(os.path.join(d,'thumbnail.jpg'))//1024,'KB')`, dir], { stdio: 'inherit' });
})();

// the new player: every state, every context, many screen sizes. Fails loudly on anything cut, covered or off screen.
const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8765';
const VPS = (process.env.VPS || '320x568,360x600,360x640,360x700,375x667,390x664,393x760,412x732,412x840,430x800,568x320,640x360,740x360,800x360,915x412,768x1024,820x1180,1024x768,1280x720,1366x768,1920x1080').split(',').map(s => s.split('x').map(Number));
const PAGES = (process.env.PAGES || '/bw/dashboard/tutorials/,/bw/dashboard/join/,/bw/dashboard/,/bw/,/bw/dashboard/tutorials/safepal-wallet-setup/,/bw/dashboard/tutorials/buy-bnb-send-to-safepal/,/bw/dashboard/tutorials/swap-bnb-to-btcb-activate-slot-1/,/bw/dashboard/explainers/,/bw/dashboard/explainers/bitcoin-wealth-presentation/,/bw/dashboard/what-is-bitcoin-wealth/,/bw/dashboard/how-it-works/').split(',');
const SHOT = process.env.SHOT, ONLYSHOT = (process.env.SHOTVP || '').split(',');
let bad = 0, checks = 0;
const fail = (ctx, msg) => { bad++; console.log('FAIL', ctx, msg); };
// geometry of a player, measured in the page
const probe = () => {
  const pl = document.querySelector('.pl.max') || document.querySelector('.pl.on'); if (!pl) return null;
  const R = e => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height }; };
  const v = pl.querySelector('video'), scr = pl.querySelector('.pl-scr'), bar = pl.querySelector('.pl-bar'), dev = pl.querySelector('.pl-dev');
  const vis = e => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && e.getBoundingClientRect().width > 0; };
  const btns = [...pl.querySelectorAll('.pl-b')].filter(vis).map(b => ({ name: b.getAttribute('aria-label'), ...R(b), text: b.innerText.trim() }));
  const vs = v ? getComputedStyle(v) : null, vr = v ? R(v) : null;
  // the picture inside the video box (object-fit:contain)
  let pic = null;
  if (v && v.videoWidth) { const ar = v.videoWidth / v.videoHeight, bw = vr.w, bh = vr.h; const w = Math.min(bw, bh * ar), h = w / ar; pic = { l: vr.l + (bw - w) / 2, t: vr.t + (bh - h) / 2, w, h, r: vr.l + (bw + w) / 2, b: vr.t + (bh + h) / 2 }; }
  // anything lying on the picture? sample a grid of points on it
  const over = [];
  if (pic) for (let i = 1; i < 10; i++) for (let j = 1; j < 10; j++) {
    const x = pic.l + pic.w * i / 10, y = pic.t + pic.h * j / 10; if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) { over.push('offscreen@' + i + ',' + j); continue; }
    const e = document.elementFromPoint(x, y); if (e !== v) over.push((e ? e.tagName + '.' + (e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className) : 'null') + '@' + i + ',' + j);
  }
  const hdr = document.querySelector('.dtop,.ltop'); const hb = hdr && getComputedStyle(hdr).position === 'sticky' ? hdr.getBoundingClientRect().bottom : 0;
  return { max: pl.classList.contains('max'), coverWin: pl.classList.contains('cover-win'), cls: pl.className, frame: R(pl.classList.contains('max') ? pl : (pl.querySelector('.pl-deck') && getComputedStyle(pl.querySelector('.pl-deck')).display !== 'none' ? pl : dev)), dev: R(dev), scr: R(scr), bar: R(bar), video: vr, pic, fit: vs && vs.objectFit, radius: vs && vs.borderRadius,
    natural: v && [v.videoWidth, v.videoHeight], btns, over: [...new Set(over)].slice(0, 5), vw: innerWidth, vh: innerHeight, hdrBottom: hb, fs: !!document.fullscreenElement, inSheet: !!pl.closest('.sheet') };
};
function judge(ctx, m, { inline }) {
  checks++;
  if (!m) return fail(ctx, 'no player found');
  const eps = 0.75;
  if (!m.video) return fail(ctx, 'no video');
  if (!m.natural || !m.natural[0]) return fail(ctx, 'video did not load');
  if (m.fit !== 'contain') fail(ctx, 'object-fit is ' + m.fit);
  if (parseFloat(m.radius) > 0) fail(ctx, 'video has rounded corners ' + m.radius);
  // the picture is whole and on screen
  const p = m.pic, top = inline ? m.hdrBottom : 0;
  if (p.l < -eps || p.t < top - eps || p.r > m.vw + eps || p.b > m.vh + eps) fail(ctx, `picture off screen: ${JSON.stringify([p.l, p.t, p.r, p.b].map(Math.round))} in ${m.vw}x${m.vh} top ${top}`);
  if (m.over.length) fail(ctx, 'something lies on the picture: ' + m.over.join(' '));
  // the screen has the video's shape (no bars inside the frame) unless full screen
  if (!m.max) { const ar = m.natural[0] / m.natural[1], sar = m.scr.w / m.scr.h; if (Math.abs(ar / sar - 1) > 0.01) fail(ctx, `screen shape ${sar.toFixed(4)} is not the video's ${ar.toFixed(4)}`); }
  // the whole frame is on screen too
  const f = m.frame; if (f.l < -4 || f.t < top - eps || f.r > m.vw + 4 || f.b > m.vh + eps) fail(ctx, `frame off screen: ${JSON.stringify([f.l, f.t, f.r, f.b].map(Math.round))} in ${m.vw}x${m.vh} top ${top}`);
  if (process.env.FALLBACK && m.max && !m.coverWin) fail(ctx, 'no full screen in this browser, and the player did not cover the window itself');
  if (!process.env.FALLBACK && m.max && !m.fs) fail(ctx, 'full screen is available but was not used');
  // Close and Full screen: there, on screen, big enough, not on the picture
  for (const want of [m.max ? 'Exit Full Screen' : 'Full Screen', 'Close the video']) {
    const b = m.btns.find(x => x.name === want); if (!b) { fail(ctx, 'button missing: ' + want); continue; }
    if (b.l < -eps || b.t < top - eps || b.r > m.vw + eps || b.b > m.vh + eps) fail(ctx, `button off screen: ${want}`);
    if (b.w < 30 || b.h < 30) fail(ctx, `button too small: ${want} ${Math.round(b.w)}x${Math.round(b.h)}`);
    // the words "Full Screen" always show, so a visitor knows what the button does (MTG, 16 Nov 2026)
    if (want !== 'Close the video' && b.text.replace(/\s+/g, ' ') !== want) fail(ctx, `the words "${want}" are not showing on the button (it shows "${b.text}")`);
    if (!(b.r <= p.l + eps || b.l >= p.r - eps || b.b <= p.t + eps || b.t >= p.b - eps)) fail(ctx, `button on the picture: ${want}`);
  }
  if (m.btns.length === 2) { const [a, b] = m.btns; if (!(a.r <= b.l + eps || b.r <= a.l + eps || a.b <= b.t + eps || b.b <= a.t + eps)) fail(ctx, 'buttons overlap'); }
  return m;
}
(async () => {
  const b = await chromium.launch();
  for (const [w, h] of VPS) {
    const mob = w < 1100;
    const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: mob, hasTouch: mob });
    // FALLBACK=1: a browser without full screen for page elements (some in-app browsers): the player must cover the window itself
    if (process.env.FALLBACK) await ctx.addInitScript(() => { Object.defineProperty(Document.prototype, 'fullscreenEnabled', { get: () => false }); Object.defineProperty(Document.prototype, 'webkitFullscreenEnabled', { get: () => false }); });
    const p = await ctx.newPage(); const errs = [];
    p.on('console', m => { if (m.type() === 'error' && !/coingecko|mempool|ERR_FAILED|status of 429/.test(m.text())) errs.push(m.text().slice(0, 140)); }); p.on('pageerror', e => errs.push('PAGEERROR ' + e.message.slice(0, 140)));
    const shot = async name => { if (SHOT && (ONLYSHOT[0] === '' || ONLYSHOT.includes(`${w}x${h}`))) await p.screenshot({ path: `${SHOT}/${w}x${h}-${name}.png` }); };
    for (const path of PAGES) {
      await p.goto(BASE + path, { waitUntil: 'load' }); await p.waitForTimeout(250);
      const n = await p.locator('.vplay').count();
      for (let i = 0; i < n; i++) {
        await p.goto(BASE + path, { waitUntil: 'load' }); await p.waitForTimeout(250);
        const btn = p.locator('.vplay').nth(i); const code = await btn.getAttribute('data-code');
        const pops = await btn.getAttribute('data-play');      // a vertical video's wide cover: pressing it opens the pop-up's phone
        const tag = `${w}x${h} ${path} ${pops ? 'cover' : 'inline'} ${code}`;
        // the cover: the frame fits the screen under the top bar (covers further down load when they come into view)
        await btn.scrollIntoViewIfNeeded(); await btn.evaluate(el => { const i = el.closest('.pl').querySelector('.pl-scr img'); return i && !i.complete ? new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); setTimeout(r, 5000); }) : null; });
        const cov = await btn.evaluate(el => { const pl = el.closest('.pl'), dev = pl.querySelector('.pl-dev').getBoundingClientRect(), deck = pl.querySelector('.pl-deck'), dk = getComputedStyle(deck).display !== 'none' ? deck.getBoundingClientRect().height : 0, scr = pl.querySelector('.pl-scr').getBoundingClientRect(), pb = el.querySelector('.pbtn').getBoundingClientRect(); return { h: dev.height + dk, w: pl.getBoundingClientRect().width, sw: scr.width, sh: scr.height, vh: innerHeight, vw: innerWidth, sb: pl.getBoundingClientRect().left,
          tall: pl.classList.contains('pl-v'), laptop: pl.classList.contains('pl-h') && getComputedStyle(deck).display !== 'none', img: (i => !!i && i.complete && i.naturalWidth > 0 && Math.abs(i.naturalWidth / i.naturalHeight / (16 / 9) - 1) < 0.02)(pl.querySelector('.pl-scr img')), spot: !!el.getAttribute('style'), bx: (pb.left + pb.width / 2 - scr.left) / scr.width, by: (pb.top + pb.height / 2 - scr.top) / scr.height, bw: pb.width, inside: pb.left >= scr.left && pb.right <= scr.right && pb.top >= scr.top && pb.bottom <= scr.bottom }; });
        // the play button cannot be missed (MTG, 16 Nov 2026): on a vertical cover it sits in the middle; on any cover it is whole and big enough
        checks++;
        if (!cov.inside) fail(tag, 'the play button is not wholly on the cover');
        if (cov.bw < 52) fail(tag, `the play button is only ${Math.round(cov.bw)} px wide`);
        if (cov.tall && !cov.spot && (Math.abs(cov.bx - 0.5) > 0.03 || Math.abs(cov.by - 0.5) > 0.05)) fail(tag, `the play button is not in the middle of the vertical cover: ${Math.round(cov.bx * 100)}%, ${Math.round(cov.by * 100)}%`);
        // every video on the page is a wide cover in the laptop frame (MTG, 17 Nov 2026), with the play button in its middle unless the cover names a spot
        checks++;
        if (!cov.laptop) fail(tag, 'the cover is not in the laptop frame');
        if (Math.abs(cov.sw / cov.sh / (16 / 9) - 1) > 0.02) fail(tag, `the cover is not 16:9 (${(cov.sw / cov.sh).toFixed(3)})`);
        if (!cov.img) fail(tag, 'the cover picture did not load, or is not 16:9');
        if (!cov.spot && (Math.abs(cov.bx - 0.5) > 0.03 || Math.abs(cov.by - 0.5) > 0.05)) fail(tag, `the play button is not in the middle of the cover: ${Math.round(cov.bx * 100)}%, ${Math.round(cov.by * 100)}%`);
        checks++;
        const short = cov.h > cov.vh - 66 + 0.75;      // the screen is too short for the smallest frame (a phone on its side): play must go straight to full screen
        if (cov.w > cov.vw || cov.sb < -0.75) fail(tag, 'cover frame wider than the screen');
        if (pops) {      // the pop-up loop below plays it; here: the press really opens the phone frame, and Close brings the cover back
          await btn.scrollIntoViewIfNeeded(); await btn.click(); await p.waitForFunction(() => { const v = document.querySelector('#pl-pop video'); return v && v.videoWidth > 0; }, null, { timeout: 15000 }).catch(() => {});
          await p.waitForTimeout(500);
          const st = await p.evaluate(() => { const pop = document.querySelector('#pl-pop'), v = pop && pop.querySelector('video'); return { phone: !!pop && pop.classList.contains('pl-v'), on: !!pop && pop.classList.contains('on'), tall: !!v && v.videoHeight > v.videoWidth, inline: !!document.querySelector('.vid .pl.on') }; });
          checks++; if (!st.on || !st.phone || !st.tall || st.inline) fail(tag, 'pressing the cover did not open the vertical video in the phone frame ' + JSON.stringify(st));
          await p.locator('#pl-pop [data-pl-x]').click(); await p.waitForTimeout(500);
          const back = await p.evaluate(() => ({ sheet: document.querySelector('#player').classList.contains('on'), vids: document.querySelectorAll('.pl video').length }));
          checks++; if (back.sheet || back.vids) fail(tag, 'Close did not bring the cover back ' + JSON.stringify(back));
          continue;
        }
        await btn.scrollIntoViewIfNeeded(); await btn.click(); await p.waitForFunction(() => { const v = document.querySelector('.pl.on video'); return v && v.videoWidth > 0; }, null, { timeout: 15000 }).catch(() => {});
        await p.waitForTimeout(900);
        let m = await p.evaluate(probe);
        if (short) {
          if (!m || !m.max) fail(tag, `frame ${Math.round(cov.h)} cannot fit ${cov.vh - 66} and play did not go to full screen`); else judge(tag + ' AUTO FULL', m, { inline: false });
          if (code === 't2' || code === 's1') await shot(`${path.replace(/\//g, '_')}${code}-autofull`);
          await p.locator('.pl.max [data-pl-max]').click(); await p.waitForTimeout(600);
        } else {
          judge(tag, m, { inline: true });
          if (i === 0 || code === 't2' || code === 's1') await shot(`${path.replace(/\//g, '_')}${code}-inline`);
          await p.locator('.pl.on [data-pl-max]').click(); await p.waitForTimeout(700);
          m = await p.evaluate(probe); if (m && !m.max) fail(tag, 'did not go full screen'); else judge(tag + ' FULL', m, { inline: false });
          if (code === 't2' || code === 's1') await shot(`${path.replace(/\//g, '_')}${code}-full`);
          await p.locator('.pl.max [data-pl-max]').click(); await p.waitForTimeout(600);
          m = await p.evaluate(probe); checks++; if (!m || m.max) fail(tag, 'did not leave full screen'); else judge(tag + ' BACK', m, { inline: true });
        }
        const playing = await p.evaluate(() => { const v = document.querySelector('.pl.on video'); return v && !v.paused; }); checks++; if (!playing) fail(tag, 'video stopped after full screen');
        // Close: back to the cover, floating buttons return
        await p.locator('.pl.on [data-pl-x]').click(); await p.waitForTimeout(300);
        const closed = await p.evaluate(() => ({ on: !!document.querySelector('.pl.on'), vids: document.querySelectorAll('.pl video').length, cls: document.documentElement.className, cover: !!document.querySelector('.vplay') && getComputedStyle(document.querySelector('.vplay')).display !== 'none' }));
        checks++; if (closed.on || closed.vids || /pl-playing/.test(closed.cls) || !closed.cover) fail(tag, 'close did not return to the cover ' + JSON.stringify(closed));
      }
      // a time button on a video's own page starts the video at that step
      const jumps = await p.locator('.wsec .tjump[data-at]').count();
      if (jumps > 3) {
        await p.goto(BASE + path, { waitUntil: 'load' }); await p.waitForTimeout(250);
        const j = p.locator('.wsec .tjump[data-at]').nth(Math.min(jumps - 1, 6)); const at = parseFloat(await j.getAttribute('data-at'));
        const tag = `${w}x${h} ${path} time button ${at}`;
        const jb = await j.evaluate(el => { const r = el.getBoundingClientRect(); return { w: r.width, h: r.height }; });
        checks++; if (jb.w < 44 || jb.h < 30) fail(tag, `the time button is only ${Math.round(jb.w)}x${Math.round(jb.h)}`);
        await j.scrollIntoViewIfNeeded(); await j.click();
        await p.waitForFunction(a => { const v = document.querySelector('#pl-pop video'); return v && v.videoWidth > 0 && v.currentTime >= a - 0.5; }, at, { timeout: 15000 }).catch(() => {});
        const ct = await p.evaluate(() => { const v = document.querySelector('#pl-pop video'); return v ? v.currentTime : -1; });
        checks++; if (!(ct >= at - 0.5 && ct < at + 20)) fail(tag, `the video did not start at ${at} s (it is at ${ct.toFixed(1)} s)`);
        await p.locator('#pl-pop [data-pl-x]').click(); await p.waitForTimeout(400);
      }
      // the pop-up
      const keys = await p.evaluate(() => [...new Set([...document.querySelectorAll('[data-play]')].filter(e => e.getBoundingClientRect().width > 0).map(e => e.dataset.play))]);
      for (const k of keys) {
        await p.goto(BASE + path, { waitUntil: 'load' }); await p.waitForTimeout(250);
        const tag = `${w}x${h} ${path} popup ${k}`;
        const t = p.locator(`[data-play="${k}"]:visible`).first(); await t.scrollIntoViewIfNeeded(); await t.click(); 
        await p.waitForFunction(() => { const v = document.querySelector('#pl-pop video'); return v && v.videoWidth > 0; }, null, { timeout: 15000 }).catch(() => {});
        await p.waitForTimeout(700);
        let m = await p.evaluate(probe); judge(tag + (m && m.max ? ' AUTO FULL' : ''), m, { inline: false });
        if (path === '/bw/dashboard/') await shot(`popup-${k}`);
        if (m && !m.max) { await p.locator('#pl-pop [data-pl-max]').click(); await p.waitForTimeout(700);
          m = await p.evaluate(probe); if (m && !m.max) fail(tag, 'did not go full screen'); else judge(tag + ' FULL', m, { inline: false }); }
        if (path === '/bw/dashboard/') await shot(`popup-${k}-full`);
        await p.locator('#pl-pop [data-pl-x]').click(); await p.waitForTimeout(600);
        const closed = await p.evaluate(() => ({ sheet: document.querySelector('#player').classList.contains('on'), hidden: document.querySelector('#player').hidden, fs: !!document.fullscreenElement, vids: document.querySelectorAll('.pl video').length, lock: document.body.style.overflow }));
        checks++; if (closed.sheet || !closed.hidden || closed.fs || closed.vids || closed.lock) fail(tag, 'close from full screen left something: ' + JSON.stringify(closed));
      }
    }
    if (errs.length) fail(`${w}x${h}`, 'console: ' + [...new Set(errs)].join(' | '));
    await ctx.close();
  }
  await b.close();
  console.log(`${checks} checks, ${bad} failures`);
  process.exit(bad ? 1 : 0);
})();

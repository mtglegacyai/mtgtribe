// Video return check (MTG, 10 Nov 2026): when a video ends, the page must come back to exactly where the visitor
// pressed play. Usage: node tools/qa/video-return-test.js [base url]. Needs a server that answers range requests,
// for example npx http-server . -p 8766 (python's http.server cannot seek videos). Add new pages and players to CASES.
// When a video ends, does the page come back to the video's spot? Each case runs with the new script blocked (old
// behaviour) and with it, at phone and laptop size. The page is knocked to the top mid-video (what full screen does on
// phones), then the video plays to its end.
const { chromium, devices } = require('playwright');
const B = process.argv[2] || 'http://127.0.0.1:8766';   // a static server WITH range requests (videos must seek)
const CASES = [
  ['JetUP How It Works, Amplify (pop-up)', '/jetup/how-it-works/', '[data-video$="amplify-24x-v2.mp4"]'],
  ['JetUP Videos, last video (pop-up)', '/jetup/videos/', '[data-video]', 'last'],
  ['JetUP home, 70/30 (pop-up)', '/jetup/', '[data-video$="70-30-split-v2.mp4"]'],
  ['Home, tribe invite (pop-up)', '/', 'a#watch[data-invite]'],
  ['ALTRUVA How It Works (inline)', '/altruva/dashboard/how-it-works/', '.vplay'],
  ['ALTRUVA dashboard, tutorial 2 (sheet)', '/altruva/dashboard/', '[data-play="t2"]'],
  ['Canton report (inline)', '/canton-weekly/2026-11-08/', '.vcover'],
];
(async () => {
  const b = await chromium.launch(); const rows = []; let bad = 0;
  for (const [devName, ctxOpt] of [['phone', { ...devices['Pixel 7'] }], ['laptop', { viewport: { width: 1280, height: 800 } }]]) {
    for (const withFix of [false, true]) {
      const ctx = await b.newContext(ctxOpt);
      await ctx.route(/coingecko|binance|googletagmanager|google-analytics|fonts\.g/, r => r.abort());
      if (!withFix) await ctx.route(/video-return\.js/, r => r.abort());
      for (const [name, url, sel, which] of CASES) {
        const p = await ctx.newPage();
        try {
          await p.goto(B + url, { waitUntil: 'load', timeout: 30000 }); await p.waitForTimeout(600);
          await p.evaluate(() => { const i = document.querySelector('.intro,#intro'); if (i) i.remove(); document.documentElement.classList.remove('intro-on'); });
          const loc = which === 'last' ? p.locator(sel).last() : p.locator(sel).first();
          await loc.evaluate(e => e.scrollIntoView({ block: 'center' })); await p.waitForTimeout(500);
          const y0 = await p.evaluate(() => Math.round(scrollY)); const t0 = await loc.evaluate(e => Math.round(e.getBoundingClientRect().top));
          await loc.evaluate(el => document.addEventListener('pointerdown', () => { window.__t0 = el.getBoundingClientRect().top; window.__y0 = scrollY; }, { capture: true, once: true }));
          await loc.click(); await p.waitForTimeout(900);
          const tap = await p.evaluate(() => ({ t0: Math.round(window.__t0), y0: Math.round(window.__y0) }));
          const r = await p.evaluate(async () => {
            const v = [...document.querySelectorAll('video')].find(v => !v.paused && !v.muted) || [...document.querySelectorAll('video')].find(v => !v.paused);
            if (!v) return { err: 'no playing video' };
            await new Promise(s => { if (v.readyState >= 1 && isFinite(v.duration)) s(); else { v.addEventListener('loadedmetadata', s, { once: true }); setTimeout(s, 8000); } });
            window.scrollTo(0, 0);                                   // what full screen does to the page on many phones
            v.currentTime = Math.max(0, v.duration - 1.0);
            try { await v.play(); } catch (e) {}
            const ended = await new Promise(s => { v.addEventListener('ended', () => s(true), { once: true }); setTimeout(() => s(false), 9000); });
            await new Promise(s => setTimeout(s, 3000));
            return { ended, src: (v.currentSrc || v.getAttribute('src') || '').split('/').pop().slice(0, 40) };
          });
          const y1 = await p.evaluate(() => Math.round(scrollY));
          const t1 = await loc.evaluate(e => Math.round(e.getBoundingClientRect().top)).catch(() => null); const onScreen = await loc.evaluate(e => { const r = e.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }).catch(() => null);
          const exact = t1 !== null && Math.abs(t1 - tap.t0) <= 6; const back = exact;
          if (withFix && (!back || !r.ended)) bad++;
          rows.push(`${back ? 'BACK ' : 'LOST '} ${devName.padEnd(6)} ${withFix ? 'new ' : 'old '} ${name.padEnd(40)} cover top on screen at the tap ${tap.t0} -> ${t1}${exact ? ' (exact)' : ''}, page y ${tap.y0} -> ${y1}, on screen: ${onScreen}, ended: ${r.ended}${r.err ? ' ' + r.err : ''}`);
        } catch (e) { rows.push(`ERR   ${devName} ${withFix ? 'new' : 'old'} ${name}: ${String(e).slice(0, 120)}`); if (withFix) bad++; }
        await p.close();
      }
      await ctx.close();
    }
  }
  await b.close(); console.log(rows.join('\n')); console.log(bad ? bad + ' PROBLEMS with the fix' : 'WITH THE FIX: every video came back to its spot'); process.exit(bad ? 1 : 0);
})();

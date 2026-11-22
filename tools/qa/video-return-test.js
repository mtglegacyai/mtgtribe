// Video return check (MTG, 10 Nov 2026): when a video ends, the page must come back to exactly where the visitor
// pressed play. Usage: node tools/qa/video-return-test.js [base url]. Needs a server that answers range requests,
// for example npx http-server . -p 8766 (python's http.server cannot seek videos). Add new pages and players to CASES.
// ONLY=<part of a case name> runs just the matching cases.
// When a video ends, does the page come back to the video's spot? Each case runs with the new script blocked (old
// behaviour) and with it, at phone and laptop size. The page is knocked to the top mid-video (what full screen does on
// phones), then the video plays to its end.
const { chromium, devices } = require('playwright');
const B = process.argv[2] || 'http://127.0.0.1:8766';   // a static server WITH range requests (videos must seek)
const CASES = [
  ['JetUP How It Works, Amplify (pop-up)', '/jetup/how-it-works/', '[data-video$="amplify-24x-v2.mp4"]'],
  ['JetUP 5 Checks, check 5, getting your money out (pop-up)', '/jetup/five-checks/', '[data-video$="getting-your-money-out.mp4"]'],
  ['JetUP How It Works, what copying really means (pop-up)', '/jetup/how-it-works/', '[data-video$="what-copying-really-means.mp4"]'],
  ['JetUP Get started, part 5, what copying really means (pop-up)', '/jetup/get-started/', '#part-5 [data-video$="what-copying-really-means.mp4"]'],
  ['JetUP Exposure Calculator, know your numbers (pop-up)', '/jetup/tools/exposure-calculator/', '[data-video$="know-your-numbers.mp4"]'],
  ['JetUP Partner Plan, the Infinity Bonus (pop-up)', '/jetup/partner-plan/', '[data-video$="infinity-bonus.mp4"]'],
  ['JetUP Partner Plan, the JetUP Assistant (pop-up, phone)', '/jetup/partner-plan/', '#assistant [data-video$="jetup-assistant-beta.mp4"]'],
  ['JetUP How It Works, Sonic AI the full picture (pop-up, phone)', '/jetup/how-it-works/', '#sonic-video [data-video$="sonic-ai-full-picture.mp4"]'],
  ['JetUP Five Checks, check 1, who holds what (pop-up)', '/jetup/five-checks/', '#check-1 [data-video$="who-does-what.mp4"]'],
  ['JetUP Zoom, watch first, the simple picture (pop-up)', '/jetup/zoom/', '#watch-first [data-video$="simple-picture-v3.mp4"]'],
  ['JetUP Promo, claim, the JetUP Assistant (pop-up, phone)', '/jetup/promo/', '#claim [data-video$="assistant-beta.mp4"]'],
  ['JetUP Get started, part 6, the JetUP Assistant (pop-up, phone)', '/jetup/get-started/', '#part-6 [data-video$="assistant-beta.mp4"]'],
  ['JetUP Videos, last video (pop-up)', '/jetup/videos/', '[data-video]', 'last'],
  ['JetUP home, 70/30 (pop-up)', '/jetup/', '[data-video$="70-30-split-v2.mp4"]'],
  ['Home, tribe invite (pop-up)', '/', 'a#watch[data-invite]'],
  ['ALTRUVA How It Works (inline)', '/altruva/dashboard/how-it-works/', '.vplay'],
  ['ALTRUVA dashboard, tutorial 2 (sheet)', '/altruva/dashboard/', '[data-play="t2"]'],
  ['Canton report (inline)', '/canton-weekly/2026-11-08/', '.vcover'],
  ['BW dashboard, The Missing Piece (inline, laptop frame)', '/bw/dashboard/', '.vplay[data-code="s1"]'],
  ['BW dashboard, The Missing Piece from its tile (sheet, laptop frame)', '/bw/dashboard/', '.vtile[data-play="s1"]'],
  ['BW tutorials, tutorial 1 from its laptop cover (sheet, phone frame)', '/bw/dashboard/tutorials/', '.vplay[data-code="t1"]'],
  ['BW tutorials, tutorial 2 from its laptop cover (sheet, phone frame)', '/bw/dashboard/tutorials/', '.vplay[data-code="t2"]'],
  ['BW join, tutorial 2 from its laptop cover (sheet, phone frame)', '/bw/dashboard/join/', '.vplay[data-code="t2"]'],
  ['BW landing, the presentation from its laptop cover (inline, laptop frame)', '/bw/', '.promo .vplay[data-code="i1"]'],
  ['BW tutorials page, Tutorial 3 from its laptop cover (sheet, phone frame)', '/bw/dashboard/tutorials/', '.vplay[data-play="t3"]'],
  ['BW Tutorial 3 page, a step\'s time button (sheet, phone frame)', '/bw/dashboard/tutorials/swap-bnb-to-btcb-activate-slot-1/', '#step-14 .tjump'],
  ['BW dashboard, promo video from its tile (sheet, phone frame)', '/bw/dashboard/', '.vtile[data-play="p1"]'],
  ['BW presentation page, the presentation (inline, laptop frame)', '/bw/dashboard/explainers/bitcoin-wealth-presentation/', '.vplay[data-code="i1"]'],
  ['BW presentation page, a chapter\'s time button (sheet, laptop frame)', '/bw/dashboard/explainers/bitcoin-wealth-presentation/', '#chapter-7 .tjump'],
  ['BW landing, the 34-second promo from its button (sheet, phone frame)', '/bw/', '.promo-acts [data-play="p1"]'],
  ['BW 14 positions, the presentation from its watch-this-part card (sheet, laptop frame)', '/bw/dashboard/how-it-works/', '.vjump[data-play="i1"]'],
  ['BW Explainer 1 page, the explainer (inline, laptop frame)', '/bw/dashboard/explainers/what-is-bitcoin-wealth-video/', '.vplay[data-code="e1"]'],
  ['BW Explainer 1 page, a chapter\'s time button (sheet, laptop frame)', '/bw/dashboard/explainers/what-is-bitcoin-wealth-video/', '#chapter-6 .tjump'],
  ['BW dashboard, Explainer 1 from its gold button (inline, laptop frame)', '/bw/dashboard/', '[data-start="e1"]'],
  ['BW stokvel, Explainer 1 from its watch-this-part card (sheet, laptop frame)', '/bw/dashboard/stokvel/', '.vjump[data-play="e1"]'],
  ['BW Explainer 2 page, the explainer (inline, laptop frame)', '/bw/dashboard/explainers/how-the-14-positions-pay-video/', '.vplay[data-code="e2"]'],
  ['BW Explainer 2 page, a chapter\'s time button (sheet, laptop frame)', '/bw/dashboard/explainers/how-the-14-positions-pay-video/', '#chapter-5 .tjump'],
  ['BW 14 positions, Explainer 2 at the top (inline, laptop frame)', '/bw/dashboard/how-it-works/', '.vplay[data-code="e2"]'],
  ['BW Explainer 3 page, the explainer (inline, laptop frame)', '/bw/dashboard/explainers/the-12-slots-video/', '.vplay[data-code="e3"]'],
  ['BW Explainer 3 page, a chapter\'s time button (sheet, laptop frame)', '/bw/dashboard/explainers/the-12-slots-video/', '#chapter-4 .tjump'],
  ['BW 12 slots, Explainer 3 at the top (inline, laptop frame)', '/bw/dashboard/12-slots/', '.vplay[data-code="e3"]'],
].filter(c => !process.env.ONLY || c[0].includes(process.env.ONLY));      // ONLY=BW node tools/qa/video-return-test.js runs just those cases
(async () => {
  const b = await chromium.launch(); const rows = []; let bad = 0;
  for (const [devName, ctxOpt] of [['phone', { ...devices['Pixel 7'] }], ['laptop', { viewport: { width: 1280, height: 800 } }]]) {
    for (const withFix of [false, true]) {
      const ctx = await b.newContext(ctxOpt);
      await ctx.route(/coingecko|binance|googletagmanager|google-analytics|fonts\.g/, r => r.abort());
      if (!withFix) await ctx.route(/video-return\.js/, r => r.abort()); await ctx.route(/\.(html?)?(\?|$)|\/(\?|$)/, r => r.continue({ headers: { ...r.request().headers(), 'cache-control': 'no-cache' } }));
      for (const [name, url, sel, which] of CASES) {
        const p = await ctx.newPage();
        try {
          await p.goto(B + url, { waitUntil: 'load', timeout: 30000 }); await p.waitForTimeout(600);
          await p.evaluate(() => { const i = document.querySelector('.intro,#intro'); if (i) i.remove(); document.documentElement.classList.remove('intro-on'); });
          const loc = which === 'last' ? p.locator(sel).last() : p.locator(sel).first();
          await loc.evaluate(e => e.scrollIntoView({ block: 'center', behavior: 'instant' })); await p.waitForTimeout(500);      // instant: a long page with smooth scrolling is still moving after half a second
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

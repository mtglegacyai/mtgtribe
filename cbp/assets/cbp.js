/* ClickBaitPays Guide by MTG: menu, sticky Join bar, video pop-up, calculator, copy order form. No tracking. */
(function () {
  'use strict';
  var d = document, w = window;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); }
  function on(el, ev, fn, o) { if (el) el.addEventListener(ev, fn, o || false); }
  var RM = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- menu (phones and tablets) */
  var menuBtn = $('[data-menu]'), nav = $('#site-nav');
  function closeMenu() { if (!nav) return; nav.classList.remove('open'); if (menuBtn) { menuBtn.setAttribute('aria-expanded', 'false'); $('.sr', menuBtn).textContent = 'Open the menu'; } }
  on(menuBtn, 'click', function () {
    var open = !nav.classList.contains('open');
    nav.classList.toggle('open', open); menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    $('.sr', menuBtn).textContent = open ? 'Close the menu' : 'Open the menu';
    if (open) { var a = $('a', nav); if (a) a.focus(); }
  });
  $$('#site-nav a').forEach(function (a) { on(a, 'click', closeMenu); });
  on(d, 'keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  on(d, 'click', function (e) { if (nav && nav.classList.contains('open') && !nav.contains(e.target) && !menuBtn.contains(e.target)) closeMenu(); });

  /* ---------------------------------------------------------------- sticky Join bar: after the hero, hidden near the final call to action */
  var stick = $('[data-stick]');
  if (stick) {
    var hero = $('.hero') || $('.sec'), fin = $('[data-final]') || $('.foot'), heroOut = false, finIn = false;
    function paint() { stick.hidden = !(heroOut && !finIn); }
    if ('IntersectionObserver' in w) {
      new IntersectionObserver(function (es) { heroOut = !es[0].isIntersecting; paint(); }, { rootMargin: '-120px 0px 0px 0px' }).observe(hero);
      if (fin) new IntersectionObserver(function (es) { finIn = es[0].isIntersecting; paint(); }).observe(fin);
    }
  }

  /* ---------------------------------------------------------------- video pop-up: laptop frame for 16:9, slim phone frame for 9:16.
     When a video plays to the end the player closes itself and the page returns to where the visitor pressed play. */
  var vm = $('#vm'), devBox = vm && $('[data-dev]', vm), opener = null, savedY = 0, ytPlayer = null, ytWaiting = [];
  function frameHtml(orient) {
    return orient === 'v'
      ? '<span class="dev phone"><span class="btns" aria-hidden="true"></span><span class="scr" data-scr></span><span class="island" aria-hidden="true"></span></span>'
      : '<span class="dev laptop"><span class="scr" data-scr></span><span class="base"><i></i></span></span>';
  }
  /* the player's own Full Screen (MTG, 16 Nov 2026): the bar keeps Exit Full Screen and Close, the whole video fills the rest.
     Where a phone cannot put a page element in full screen (iPhone), the pop-up fills the window instead. */
  var fsBtn = vm && $('[data-fs]', vm);
  function realFs() { return !!(d.fullscreenElement || d.webkitFullscreenElement); }
  function isFs() { return realFs() || (vm && vm.classList.contains('vm-max')); }
  function paintFs() { if (!vm) return; var onFs = isFs(); vm.classList.toggle('is-fs', onFs); if (fsBtn) $('.lbl', fsBtn).textContent = onFs ? 'Exit Full Screen' : 'Full Screen'; }
  function toggleFs() {
    var box = $('.vm-box', vm);
    if (isFs()) { if (realFs()) exitFs(); vm.classList.remove('vm-max'); setTimeout(paintFs, 50); return; }
    var req = box.requestFullscreen || box.webkitRequestFullscreen;
    if (req) {
      try { var pr = req.call(box); if (pr && pr.catch) pr.catch(function () { vm.classList.add('vm-max'); paintFs(); }); }
      catch (e) { vm.classList.add('vm-max'); }
    } else vm.classList.add('vm-max');
    paintFs();
  }
  function exitFs() {
    try { if (d.fullscreenElement) d.exitFullscreen(); else if (d.webkitFullscreenElement) d.webkitExitFullscreen(); } catch (e) {}
  }
  function closeVm() {
    if (!vm || vm.hidden) return;
    exitFs();
    if (ytPlayer) { try { ytPlayer.destroy(); } catch (e) {} ytPlayer = null; }
    devBox.innerHTML = ''; vm.hidden = true; vm.classList.remove('vm-max'); paintFs(); d.documentElement.style.overflow = '';
    setTimeout(function () {
      w.scrollTo({ top: savedY, behavior: 'instant' });
      if (opener) { try { opener.focus({ preventScroll: true }); } catch (e) { opener.focus(); } }
    }, 60);
  }
  function openVm(btn, build, orient) {
    opener = btn; savedY = w.pageYOffset || d.documentElement.scrollTop || 0;
    devBox.innerHTML = frameHtml(orient); vm.hidden = false; d.documentElement.style.overflow = 'hidden';
    build($('[data-scr]', devBox));
    var x = $('.vm-close', vm); if (x) x.focus();
  }
  function loadYT(cb) {
    if (w.YT && w.YT.Player) return cb();
    ytWaiting.push(cb);
    if (ytWaiting.length > 1) return;
    var prev = w.onYouTubeIframeAPIReady;
    w.onYouTubeIframeAPIReady = function () { if (prev) prev(); var q = ytWaiting; ytWaiting = []; q.forEach(function (f) { f(); }); };
    var s = d.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; s.async = true; d.head.appendChild(s);
  }
  if (vm) {
    $$('[data-close]', vm).forEach(function (el) { on(el, 'click', closeVm); });
    on(fsBtn, 'click', toggleFs);
    on(d, 'fullscreenchange', paintFs); on(d, 'webkitfullscreenchange', paintFs);
    on(d, 'keydown', function (e) { if (e.key === 'Escape' && !vm.hidden) { if (vm.classList.contains('vm-max')) { vm.classList.remove('vm-max'); paintFs(); } else if (!realFs()) closeVm(); } });
    $$('.vbtn[data-src]').forEach(function (b) {
      on(b, 'click', function () {
        openVm(b, function (scr) {
          var v = d.createElement('video');
          v.setAttribute('controlslist', 'nofullscreen'); v.disablePictureInPicture = true;
          v.src = b.getAttribute('data-src'); v.controls = true; v.autoplay = true; v.playsInline = true; v.setAttribute('playsinline', '');
          if (b.getAttribute('data-poster')) v.poster = b.getAttribute('data-poster');
          on(v, 'ended', closeVm); scr.appendChild(v);
          var p = v.play(); if (p && p.catch) p.catch(function () {});
        }, b.getAttribute('data-orient') || 'h');
      });
    });
    $$('.ytb[data-yt]').forEach(function (b) {
      on(b, 'click', function () {
        var id = b.getAttribute('data-yt');
        openVm(b, function (scr) {
          var holder = d.createElement('div'); holder.className = 'ytp'; scr.appendChild(holder);
          loadYT(function () {
            if (vm.hidden) return;
            ytPlayer = new w.YT.Player(holder, {
              host: 'https://www.youtube-nocookie.com', videoId: id, width: '100%', height: '100%',
              playerVars: { autoplay: 1, rel: 0, playsinline: 1, modestbranding: 1, fs: 0 },
              events: { onStateChange: function (e) { if (e.data === 0) closeVm(); } }
            });
          });
        }, 'h');
      });
    });
  }

  /* ---------------------------------------------------------------- calculator */
  var tool = $('[data-calc]');
  if (tool) {
    var L = JSON.parse(tool.getAttribute('data-calc')), nIn = $('#c-n', tool), dIn = $('#c-d', tool);
    function cents(x) { return Math.round(x * 100) / 100; }
    function usdt(x) { return cents(x).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' USDT'; }
    function num(x) { return cents(x).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
    function iso(dt) { return dt.getFullYear() + '-' + String(dt.getMonth() + 1).padStart(2, '0') + '-' + String(dt.getDate()).padStart(2, '0'); }
    function out(k, v) { var el = $('[data-o="' + k + '"]', tool); if (el) el.textContent = v; }
    function today() { return iso(new Date()); }
    dIn.value = today();
    function calc() {
      var lv = +($('[name="lvl"]:checked', tool) || {}).value || 4, x = L.filter(function (r) { return r.l === lv; })[0];
      var first = ($('[name="first"]:checked', tool) || {}).value === '1';
      var n = Math.max(1, Math.min(5, Math.round(+nIn.value || 1)));
      if (String(n) !== nIn.value) nIn.value = n;
      var pay = x.p * n + (first ? x.a : 0), clicks = x.n * n, day = x.c * x.n * n, tot = x.t * n;
      out('pay', usdt(pay));
      out('payx', (n > 1 ? n + ' x ' : '') + 'Level ' + lv + ' campaign ' + num(x.p) + (first ? ' + one-time activation ' + num(x.a) : ' (level already active)'));
      out('clicks', clicks);
      out('day', usdt(day));
      out('dayx', num(x.c) + ' per click x ' + clicks + ' clicks');
      out('tot', usdt(tot));
      var exact = cents(x.c * x.n * 12) === cents(x.t);
      out('totx', (n > 1 ? n + ' x ' : '') + num(x.t) + (exact ? ' (' + num(x.c) + ' x ' + x.n + ' x 12 days)' : ' (the site\'s own total)'));
      var start = dIn.value ? new Date(dIn.value + 'T12:00:00') : null;
      if (start && !isNaN(start)) {
        var rel = new Date(start.getTime()); rel.setDate(rel.getDate() + 18);
        out('date', rel.toLocaleDateString('en-ZA', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' }));
      } else out('date', '-');
      out('net', usdt(tot * 0.9));
      out('formula', 'Level ' + lv + ': you pay ' + usdt(pay) + ' today, click ' + clicks + ' ads a day for 12 click days, and the platform\'s figure for ' +
        (n > 1 ? 'these ' + n + ' campaigns' : 'this campaign') + ' is ' + usdt(tot) + '.');
    }
    $$('input', tool).forEach(function (i) { on(i, 'input', calc); on(i, 'change', calc); });
    on($('[data-inc]', tool), 'click', function () { nIn.value = Math.min(5, (+nIn.value || 1) + 1); calc(); });
    on($('[data-dec]', tool), 'click', function () { nIn.value = Math.max(1, (+nIn.value || 1) - 1); calc(); });
    on($('[data-reset]', tool), 'click', function () {
      $('[name="lvl"][value="4"]', tool).checked = true; $('[name="first"][value="1"]', tool).checked = true; nIn.value = 1; dIn.value = today(); calc();
    });
    calc();
  }

  /* ---------------------------------------------------------------- copy order form: builds a WhatsApp message, stores nothing */
  var OF = $('[data-order]');
  if (OF) {
    var slugIn = $('[name="slug"]', OF), prev = $('[data-out="addr"]', OF);
    function slugify(v) { return String(v || '').toLowerCase().replace(/[^a-z0-9]+/g, '').slice(0, 24); }
    function dom() { var r = $('[name="domain"]:checked', OF); return r ? r.value : 'mtgtribe.com/cbp/'; }
    function paintAddr() { prev.textContent = dom() + (slugify(slugIn.value) || 'yourname'); }
    on(slugIn, 'input', paintAddr); $$('[name="domain"]', OF).forEach(function (r) { on(r, 'change', paintAddr); }); paintAddr();
    on(OF, 'submit', function (e) {
      e.preventDefault();
      $$('.field', OF).forEach(function (f) { f.classList.remove('err'); });
      var bad = $$('[required]', OF).filter(function (x) { return x.type === 'radio' ? !$('[name="' + x.name + '"]:checked', OF) : !x.value.trim(); });
      var ref = $('[name="ref"]', OF);
      if (ref.value.trim() && !/^https?:\/\/\S*clickbaitpays\S*/i.test(ref.value.trim())) bad.push(ref);
      if (slugIn.value.trim() && !slugify(slugIn.value)) bad.push(slugIn);
      if (bad.length) { bad.forEach(function (x) { var f = x.closest('.field'); if (f) f.classList.add('err'); }); bad[0].focus(); return; }
      function v(n) { var x = $('[name="' + n + '"]', OF); return x ? x.value.trim() : ''; }
      var pay = $('[name="pay"]:checked', OF);
      var lines = ['Hi MTG, I would like to order my own ClickBaitPays guide website (R1,000 or $50 once-off, paid after it is built).', '',
        'Name: ' + v('name'), 'Page address: ' + dom() + slugify(v('slug')), 'My ClickBaitPays referral link: ' + v('ref'),
        'My WhatsApp number: ' + v('wa'), 'My WhatsApp group link: ' + (v('group') || 'none yet'),
        'TikTok: ' + (v('tiktok') || '-'), 'Facebook: ' + (v('fb') || '-'), 'YouTube: ' + (v('yt') || '-'),
        'How I would like to pay: ' + (pay ? pay.value : 'to agree on WhatsApp'), 'Notes: ' + (v('notes') || '-')];
      var url = OF.getAttribute('data-wa') + '?text=' + encodeURIComponent(lines.join('\n'));
      var win = w.open(url, '_blank', 'noopener'); if (!win) w.location.href = url;
      var ok = $('[data-sent]'); if (ok) { ok.hidden = false; ok.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' }); }
    });
  }
})();

/* MTG TRIBE | the quick bar at the bottom of a phone (MTG, 26 Nov 2026: "Add a similar bottom navigation buttons to the
   mtgtribe.com website like we have them on ClickBaitPaysUs.com, bitcoinwealthpays.com, and mtgtribe.com/jetup").
   Phones and small tablets only (820 px and narrower), like the JetUP thumb bar; the raised middle button is the one action
   that matters most, like the ClickBaitPays quick bar: Join the MTG TRIBE (free WhatsApp group).
     Home | Streams | Join Free | Invite | Dashboard (on /dashboard/: Menu, which opens the side menu)
   On the Canton pages (/cc, /cntn, /canton-weekly) Dashboard is the Canton weekly dashboard, as in their top bar.
   Lifts the back-to-top button above the bar and pads the page so the footer is never hidden.
   Include on any mtgtribe.com hub page: <script src="/assets/tribe/bottom-nav.js?v=1" defer></script>
   Not for /jetup, /cbp or /bw: they have their own bars. */
(function () {
'use strict';
var d = document, w = window;
if (d.getElementById('tbar')) return;
var path = location.pathname.replace(/index\.html$/, '');
var canton = /^\/(cc|cntn|canton-weekly)(\/|$)/.test(path);
var onHome = path === '/';
var onDash = /^\/dashboard\/?$/.test(path);
var menuBtn = onDash ? d.querySelector('.md-menu') : null;
var S = '<svg class="tbi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">';
var I = {
  home: S + '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9.5"/></svg>',
  streams: S + '<path d="m12 2.5 9 5-9 5-9-5z"/><path d="m3 12 9 5 9-5"/><path d="m3 16.5 9 5 9-5"/></svg>',
  invite: S + '<circle cx="12" cy="12" r="9.2"/><path d="m10 8.4 5.6 3.6-5.6 3.6z" fill="currentColor"/></svg>',
  dash: S + '<rect x="3.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.6"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.6"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.6"/></svg>',
  menu: S + '<path d="M4 6.5h16M4 12h16M4 17.5h16"/></svg>',
  wa: '<svg class="tbi" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.5 4.1 1.6 5.9L0 24l6.5-1.7a11.7 11.7 0 0 0 5.6 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.5-8.4Zm-8.4 18.2h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.9 1 1-3.8-.2-.4a9.8 9.8 0 1 1 8.6 4.8Zm5.4-7.3c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.2-.2.3-.8.9-.9 1.1-.2.2-.4.2-.7.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.7.1-.1.3-.4.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.1-.7-1.7-1-2.3-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3Z"/></svg>'
};
var css = d.createElement('style');
css.textContent =
'.tbar{display:none}' +
'@media (max-width:820px){' +
 'html.has-tbar body{padding-bottom:calc(68px + env(safe-area-inset-bottom,0px))}' +
 '.tbar{position:fixed;left:0;right:0;bottom:0;z-index:90;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));align-items:end;contain:inline-size;' +
  'padding:4px max(4px,env(safe-area-inset-right,0px)) calc(4px + env(safe-area-inset-bottom,0px)) max(4px,env(safe-area-inset-left,0px));' +
  'background:rgba(12,9,5,.95);border-top:1px solid rgba(242,173,60,.3);box-shadow:0 -14px 30px rgba(0,0,0,.45);-webkit-backdrop-filter:blur(14px) saturate(1.2);backdrop-filter:blur(14px) saturate(1.2)}' +
 '.tbar .tb{position:relative;display:grid;justify-items:center;align-content:end;gap:3px;min-width:0;min-height:56px;margin:0;padding:6px 2px 4px;border:0;border-radius:12px;background:none;' +
  'color:#b9ad97;font:700 11px/1.15 Manrope,"DM Sans",system-ui,sans-serif;letter-spacing:.01em;text-align:center;text-decoration:none;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:color .2s,background .2s}' +
 '.tbar .tb span{display:block;max-width:100%;overflow-wrap:anywhere}' +
 '.tbar .tbi{width:22px;height:22px}' +
 '.tbar .tb[aria-current],.tbar .tb[aria-expanded="true"]{color:#ffd98e}' +
 '.tbar .tb[aria-current]:before{content:"";position:absolute;top:0;left:30%;right:30%;height:3px;border-radius:0 0 3px 3px;background:#f2ad3c;box-shadow:0 0 10px #f2ad3c}' +
 '.tbar .tb:active{background:rgba(242,173,60,.1)}' +
 '.tbar .tb:focus-visible{outline:2px solid #ffd98e;outline-offset:-2px}' +
 '.tbar .tb-join{color:#fff3d6;font-weight:800}' +
 '.tbar .tb-join .tbi{box-sizing:content-box;width:24px;height:24px;margin-top:-22px;padding:12px;border-radius:50%;color:#1a1002;background:linear-gradient(180deg,#ffe3a3,#f2ad3c 60%,#d9901f);' +
  'box-shadow:0 0 0 4px rgba(12,9,5,.95),0 8px 22px rgba(242,173,60,.45),inset 0 1px 0 rgba(255,255,255,.5)}' +
 '#totop,.mtg-up{bottom:calc(84px + env(safe-area-inset-bottom,0px))!important}' +
 '#toast.toast{bottom:calc(152px + env(safe-area-inset-bottom,0px))!important}' +   /* the home page tour note: above the bar and the back-to-top button */
'}' +
'@media (max-width:820px) and (prefers-reduced-motion:no-preference){.tbar .tb-join .tbi{animation:tbpulse 3s ease-in-out infinite}}' +
'@keyframes tbpulse{0%,100%{box-shadow:0 0 0 4px rgba(12,9,5,.95),0 8px 22px rgba(242,173,60,.45),inset 0 1px 0 rgba(255,255,255,.5)}50%{box-shadow:0 0 0 4px rgba(12,9,5,.95),0 8px 32px rgba(242,173,60,.8),inset 0 1px 0 rgba(255,255,255,.5)}}' +
'@media print{.tbar{display:none!important}}';
d.head.appendChild(css);

function a(href, icon, label, extra) {
  return '<a class="tb' + (extra && extra.cls ? ' ' + extra.cls : '') + '" href="' + href + '"' + (extra && extra.cur ? ' aria-current="page"' : '') +
    (extra && extra.id ? ' id="' + extra.id + '"' : '') + '>' + I[icon] + '<span>' + label + '</span></a>';
}
var dashHref = canton ? '/canton-weekly/' : '/dashboard/';
var last = menuBtn
  ? '<button class="tb" type="button" id="tb-menu" aria-controls="mtg-menu" aria-expanded="false">' + I.menu + '<span>Menu</span></button>'
  : a(dashHref, 'dash', 'Dashboard', { cur: canton ? /^\/canton-weekly\/?$/.test(path) : onDash });
var nav = d.createElement('nav');
nav.className = 'tbar'; nav.id = 'tbar'; nav.setAttribute('aria-label', 'Quick links');
nav.innerHTML =
  a('/', 'home', 'Home', { cur: onHome }) +
  a(onDash ? '#streams' : '/dashboard/#streams', 'streams', 'Streams') +
  a('/group/', 'wa', 'Join Free', { cls: 'tb-join' }) +
  a('/#invite', 'invite', 'Invite', { id: 'tb-invite' }) +
  last;
d.body.appendChild(nav);
d.documentElement.classList.add('has-tbar');

// on the home page the invite opens in the page's own player, as from the top bar
var inv = d.getElementById('tb-invite');
inv.addEventListener('click', function (e) {
  var t = onHome && d.querySelector('[data-invite]');
  if (t) { e.preventDefault(); t.click(); }
});
// on the dashboard, Menu opens the side menu (the same as the menu button in the top bar)
if (menuBtn) {
  var mb = d.getElementById('tb-menu');
  mb.addEventListener('click', function () { menuBtn.click(); });
  var sync = function () { mb.setAttribute('aria-expanded', menuBtn.getAttribute('aria-expanded') === 'true' ? 'true' : 'false'); };
  if (w.MutationObserver) new MutationObserver(sync).observe(menuBtn, { attributes: true, attributeFilter: ['aria-expanded'] });
  sync();
}
})();

/* Up and Down buttons on long pages (MTG, 27 Nov 2026): loads /assets/updown.js once. */
;(function(){if(window.__mtgUD||document.querySelector('script[src*="updown.js"]'))return;var s=document.createElement("script");s.src="/assets/updown.js?v=1";s.defer=true;document.head.appendChild(s)})();

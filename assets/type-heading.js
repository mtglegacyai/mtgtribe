/* Typewriter heading for mtgtribe.com, matching the musathegiant.com hero:
   the gold line of the page's <h1> types itself out behind a glowing amber caret.

   - Two-line headings (<span class="w">, <span class="l1"> first line): only the second (gold) line types.
   - One-line headings: the whole heading types.
   - Types once per page view, then the caret keeps blinking (one phrase, so no delete and retype loop).
   - The full text stays in the page for search engines, the heading keeps its size while typing
     (letters are hidden, not removed, so nothing jumps), and screen readers get the whole heading.
   - Visitors who ask for reduced motion, or browsers without JavaScript, see the heading as normal.
   Include on any page with: <script src="/assets/type-heading.js?v=1" defer></script> */
(function () {
  "use strict";
  var h1 = document.querySelector("main h1, h1");
  if (!h1 || h1.dataset.typed) return;
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  h1.dataset.typed = "1";

  var css = document.createElement("style");
  css.textContent =
    ".th-c{visibility:hidden}.th-c.on{visibility:visible}" +
    ".th-caret{display:inline-block;width:.07em;height:.78em;margin-left:.06em;vertical-align:-.04em;border-radius:2px;" +
    "background:#f2ad3c;box-shadow:0 0 14px rgba(242,173,60,.7);-webkit-text-fill-color:initial;animation:th-blink 1s steps(1) infinite}" +
    ".th-caret.busy{animation:none}@keyframes th-blink{50%{opacity:0}}";
  document.head.appendChild(css);

  // Which part types: the gold line after the first-line span, or the whole heading.
  var first = h1.querySelector(":scope > .w, :scope > .l1");
  var target = h1.querySelector(":scope > .l2");
  var nodes = [];
  if (target) {
    nodes = textNodes(target);
  } else {
    var kids = Array.prototype.slice.call(h1.childNodes);
    kids.forEach(function (n) {
      if (first && (n === first || first.contains(n))) return;
      nodes = nodes.concat(textNodes(n));
    });
  }
  if (!nodes.length) return;

  // innerText keeps the break between the two heading lines ("How to buy" + "Canton Coin").
  h1.setAttribute("aria-label", (h1.innerText || h1.textContent).replace(/\s+/g, " ").trim());

  // Wrap every letter in a hidden span (keeps layout identical to the finished heading).
  var chars = [];
  nodes.forEach(function (tn) {
    var text = tn.nodeValue;
    if (!text.trim()) return;
    var frag = document.createDocumentFragment();
    for (var i = 0; i < text.length; i++) {
      var s = document.createElement("span");
      s.className = "th-c";
      s.setAttribute("aria-hidden", "true");
      s.textContent = text[i];
      frag.appendChild(s);
      chars.push(s);
    }
    tn.parentNode.replaceChild(frag, tn);
  });

  var caret = document.createElement("i");
  caret.className = "th-caret";
  caret.setAttribute("aria-hidden", "true");
  chars[0].parentNode.insertBefore(caret, chars[0]);

  var i = 0;
  function tick() {
    caret.classList.add("busy");
    var c = chars[i];
    c.classList.add("on");
    c.parentNode.insertBefore(caret, c.nextSibling);
    i++;
    if (i < chars.length) {
      setTimeout(tick, c.textContent === " " ? 40 : 75 + Math.random() * 55);
    } else {
      caret.classList.remove("busy");
    }
  }
  // Start once the heading's own entrance animation has mostly finished.
  setTimeout(tick, 900);

  function textNodes(root) {
    if (root.nodeType === 3) return [root];
    var out = [];
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    while (w.nextNode()) out.push(w.currentNode);
    return out;
  }
})();

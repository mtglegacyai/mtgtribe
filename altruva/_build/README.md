# ALTRUVA guide builder

Static site generator for mtgtribe.com/altruva (Python 3, Pillow, Playwright for the quick guide PDF).

- `build/config.py`: links (referral, login, WhatsApp, TikTok), the 13 videos, the side menu order.
- `build/core.py`: link helper `L()` (prod: absolute /altruva/ paths; preview: relative files), icons (lucide + simple-icons sprite), components, dashboard shell.
- `build/pages_*.py`: page content. `build/build.py`: images, OG image, quick guide PDF, pages, sitemap, robots, /group redirect, 404 case fix.
- `src/assets/altruva.css`, `src/assets/altruva.js`: design system and behaviour.
- `qa.js`: Playwright interaction checks (copy buttons, menu, players, calculators). `shoot.js`: screenshots.

Folders starting with `_` are not published by GitHub Pages (Jekyll), so this folder stays private to the repo.

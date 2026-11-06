# JetUP and TAG Markets guide: how the pages are built

Every page under `/jetup/` is written by `build.py` (Python 3.12 or newer). Edit the Python, then run:

```bash
python3 jetup/_build/build.py
```

The folder starts with `_`, so GitHub Pages does not publish it.

## Files

| File | What it holds |
|---|---|
| `layout.py` | Head and SEO, top bar, side menu, footer, the video player, icons, and shared facts (`RETAIL_LOSS`, links) |
| `pages_home.py` | `/jetup/`, the overview |
| `pages_start.py` | `/jetup/get-started/`, the 6-part sign-up training with the guide screenshots |
| `pages_learn.py` | The 5 checks, How it works, Partner plan, Dennis promo, BIX Card |
| `pages_tools.py` | Exposure Calculator, Profit Split Calculator, Videos, Downloads, FAQ, Disclaimer |
| `icons.json` | Icon symbols reused from the rest of mtgtribe.com |
| `../assets/jetup.css`, `../assets/jetup.js` | The design system and all interaction (no libraries) |

## Built-in guards

The build stops if any page contains an em dash or an en dash, or mentions Luno.

## Rules this site follows (MTG, 5 and 6 November 2026)

- 16:9 videos play in the laptop frame, 9:16 videos in the slim gold phone frame, and the player closes itself
  (leaving full screen first) when a video ends.
- MTG's profile photo is always shown whole (face, t-shirt print and the sign), in a rounded gold frame.
- Every tool has its own page and menu item. The candle chart in the hero is labelled as an illustration.
- Personal details are hidden in every screenshot. Guide page 20 has another member's balances blurred.
  Guide pages 10, 19 and 21 are left out (10 and 19 mention an exchange MTG does not use).
- Preview only until MTG approves. Never push to `main` without his approval.

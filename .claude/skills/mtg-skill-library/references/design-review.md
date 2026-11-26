# Design review: premium, never the "AI template" look

Use on every page, section, dashboard, calculator, flyer, cover, thumbnail and social preview, before the private
preview link goes to MTG. Run it beside the QA scripts we already have (`tools/qa/hscroll.js`,
`tools/qa/player-check.js`, `tools/og/check_og.py`). Design reference: musathegiant.com/cards/bellvercards.

Source: Impeccable by Paul Bakaus (Apache 2.0, `pbakaus/impeccable` at b49177d32788, impeccable.style), built on
Anthropic's frontend-design skill. Its craft floor, slop list, modes and command vocabulary, adapted for MTG.

Impeccable's own first rule, taken whole: **the brief wins.** MTG's standing rules (phone and laptop frames, the play
button in the middle, covers, gold-titanium style, Bellver cards look) always beat any taste below.

## First, name the page's mode

The mode says what success looks like for the visitor, so it decides how bold the design should be.

| Mode | MTG pages | What matters |
|---|---|---|
| **Persuade** | Landing pages, sales letters, order forms, promo pages, the main page of each guide | The first screen makes the offer clear and wanted, shows one obvious action, and proves something only this offer can prove (MTG's own BellverCards story, a check on chain, a real redacted screen). Bold, committed, distinctive. |
| **Operate** | Dashboards, calculators, back-office tours, order steps | Clarity, consistency and what the visitor already knows beat expression. The brand lives in precise details. |
| **Read** | Guides, FAQs, glossaries, step-by-step pages, watch pages | Structure for understanding: short answers first, scannable steps, comfortable reading. |

## The "AI template" tells to refuse

An agent left to itself reaches for these again and again. Any one of them makes a page look assembled, not designed.

- The whole page built from same-size cards (icon, heading, text). Cards inside cards: always wrong.
- Gradient text, purple-to-blue gradients, glass and blur used as decoration.
- Grey text on a coloured background. Tint the secondary text from the background's own colour.
- A coloured bar down one side of a rounded box. Use a full border, a tint or a leading icon.
- Hard block shadows (`4px 4px 0`) or zero-offset glow halos. Real shadows have an offset and a soft blur.
- A big-number hero (huge stat, small label, three supporting stats) as the default opening.
- One identical fade-in on every section. Motion should be one considered moment, smooth, and respect reduced motion.
- Section numbers (01, 02, 03) that carry no meaning. Real step numbers in a tutorial carry meaning and stay.
- Monospace text as a "techy" costume. Keep it for code, addresses and data.
- Browser defaults nobody styled: text selection colour, focus rings, scrollbars, link underline offset. Theming
  them from the palette is the cheapest sign that a page was built with care.
- A small label above every heading (an "eyebrow"). Keep one only when it tells the visitor something they need.
- A default system font as the headline voice. Our display font is chosen and loaded on purpose.

## Checks on the built page (look at it at 360 px and at desktop width)

- **Contrast:** body text at least 4.5:1, large text at least 3:1, including text on photos and covers.
- **Spacing:** tight inside a group, generous between groups, more space above a heading than below it.
- **Type:** comfortable line length on desktop (about 65 to 75 characters), clear steps in size and weight, nothing
  overflowing at any width (MTG's no-sideways-scroll rule, at normal and larger Android text size).
- **States:** hover, keyboard focus, loading, error and empty states all designed, not left to the browser.
- **Copy:** buttons name their action and its value ("Watch the 2-minute video", not "Learn more"). Errors say what went
  wrong and how to fix it.
- **Coverage:** everything the brief asked for is on the page and findable within seconds.

## Words MTG can use to steer (Impeccable's vocabulary)

He can say any of these about a page or one part of it, and we act on that part only (narrow targets give better results).

| Say | It means |
|---|---|
| **critique** | A scored review: Nielsen's 10 usability heuristics (0 to 4 each), how much the visitor has to think, and walk-throughs as real visitors (a first-time crypto beginner on a 360 px Android phone, a prospect arriving from WhatsApp, a returning member). Fixes ranked. |
| **audit** | A technical check: accessibility, speed, responsiveness, findings ranked P0 (blocking) to P3 (polish). |
| **polish** | The final pass before a preview. |
| **bolder** / **quieter** | Turn up a safe, bland design, or calm a loud one. |
| **distill** | Remove what the page does not need. |
| **clarify** | Rewrite unclear labels, buttons and messages (with `voice-pass.md`). |
| **adapt** | Make it work at every screen size. |
| **harden** | Edge cases: long names, empty states, errors, slow connections. |

## The tool itself (not installed yet)

Impeccable also ships a checker with 62 rules that runs with no AI and no API key (`npx impeccable detect <folder or
URL>`), a design hook that checks each edit, and a "live" mode. Status on 26 Nov 2026: not installed, waiting for MTG's
OK to run outside code. If he approves: run the checker on the built pages; keep live mode switched off
(`IMPECCABLE_LIVE_COPY_AGENT=off`), because when no chat is connected it can start an agent with permission checks
turned off; never inject it into a live site.

## Not taken, and why

- Its ban on emoji: MTG's brand emoji stay (👑 💪 👉 in his signature, captions and descriptions). For interface icons
  in menus and feature lists, drawn SVG icons in one consistent style still look more premium than emoji.
- Its "kicker above a heading is always banned": softened to "only when it carries information", so existing pages
  are judged case by case, not rebuilt.

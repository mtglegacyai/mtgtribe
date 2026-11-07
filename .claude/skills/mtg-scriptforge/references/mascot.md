# MTG's mascot: the mtgTribe lion

Approved direction (MTG, 7 November 2026: "redesign him to be clearly mine, I want him to wear this t-shirt"). Name:
to be chosen by MTG. Reference picture: `assets/mascot-reference.jpg` in this skill.

## Look (keep it identical in every clip)

- An original cartoon lion in a premium, high-end 3D animated film style.
- Rich honey-brown fur, cream muzzle and chest, dark chocolate-brown ear tips.
- Short, combed dark-brown hair on top. **Never** a spiky orange tuft: that resembles a famous film lion and could
  bring copyright trouble.
- Round gold-rimmed glasses ("Your Digital Architect"), warm amber eyes, expressive eyebrows.
- A gold wristwatch on his left wrist (like MTG's photo).
- MTG's white t-shirt with the exact print: the black evolution silhouettes, the row of icons (cow, gold bars, banknotes
  and coins, bank card) ending with a gold Bitcoin coin, then "mtgTribe.com" and "Let's Get This Crypto!".
- Home set: a black-and-gold studio (glossy black floor, curved gold light strips, warm rim light, golden bokeh).
  Other sets are fine when the story needs them.

**Personality:** curious, warm, a patient teacher. He reacts, wonders and explains with gestures. He never celebrates
money, never shows earnings and never pressures anyone.

## How to make a new clip (HeyGen, MTG's workspace)

- Tool: `reference_to_video` with both reference images:
  - mascot reference picture: asset `855fc4950cb54a9c91b6e829f70220dd`
  - t-shirt print: asset `47be82b6e98e45c5a0ba430e3416aa4b`
- Settings: 9:16 (Shorts) or 16:9 (YouTube), resolution 1080p, 5 to 15 seconds, prompt enhancement "quality".
- Prompt: copy the Look section above word for word, then the set, then one simple action, then these lines:
  "His paws never cover the t-shirt print. Keep the print large, flat and readable in every frame. Gentle, natural
  character animation, the same design in every frame. No other text, letters, logos or watermarks anywhere except the
  t-shirt print."
- One simple action per clip (look, wonder, react, point to the side where a graphic will appear, nod, wave). Complex
  actions and props cause glitches.
- Poll `get_model_video`, download, check every second of the clip (frame sheet) before using it.

## Cost (measured 7 November 2026)

- `text_to_video`, 8 s, 1080p: 7 credits.
- `reference_to_video` with a reference image, 8 s, 1080p: 15 credits (balance 236 to 221; other use of the account at
  the same time cannot be fully ruled out).

Plan 4 to 6 mascot clips per long video (hook, reactions, ending) and reuse them in the Shorts; the 3D studio's free
graphics do the explaining. Check the balance before and after, and ask MTG before generating a batch.

## Rules

- Generated clips come with HeyGen's own sound: mute it. Narration is MTG's approved voice; the ending uses his closing
  track.
- All other words, numbers and labels are added as graphics in the 3D studio, never generated inside the clip.
- The mascot never replaces MTG's circle photo at the greeting and end card (mtg-creative-standard section 10a).
- Platform labels: switch on the AI label on YouTube, TikTok and Meta (the narration is a synthetic voice, and the
  clips are AI-generated).
- The mascot only appears in content that passes `compliance.md`: never in recruitment, earnings or returns content on
  social platforms.
- Making him speak with lip sync (HeyGen `create_lipsync`) is possible in principle; test it on one clip first.

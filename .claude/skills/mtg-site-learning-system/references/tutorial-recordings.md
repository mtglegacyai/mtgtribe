# Editing MTG's own tutorial recordings

Lessons from the JetUP getting-started recordings (7 November 2026). MTG records each part as a silent phone screen
recording, tap by tap, and sends spoken notes. His recording beats every other source: update the facts register from it.

## Receiving and storing

- One part per short video ("chops"), never one long video. Save his narration notes for every part in the site's tutorial
  README (steps, exact on-screen labels, what to cut), without personal details.
- Large files come through Google Drive: he shares the file by link, you download it, he sets it back to Restricted and
  may delete it after approving the edit. Check the byte size against Drive.
- Raw recordings stay private in the session workspace. Never commit or publish them. Never write down one-time codes,
  passwords or anything personal he reads out.
- Map every recording before editing: contact sheets (1 frame every 2 to 4 seconds), then a table of source times, what each
  shows and keep or cut.

## Privacy: hide everything personal in every frame

Use `tools/tutorial-redact/` in the mtgtribe repository (README there). Personal words go in a private patterns file
outside the repository, never in code. Per frame:
1. Remove the screen recorder's timer bubble (paint it out from the background, never just blur it).
2. Blank the keyboard's suggestion and autofill strip whenever a keyboard is up: it suggests names and emails.
3. Cover the focused input field while he types (thick dark border detection): partial words defeat OCR.
4. OCR the page in overlapping bands, two modes (psm 11 and 6, plus an inverted pass on dark sheets), and cover every
   name, email, password, phone number, ID, CU number and referrer with a labelled pill ("Your email", "Your number").
5. Carry each cover across neighbouring frames along the measured scroll, so one missed OCR frame never leaks.
Then OCR every second frame of the finished video and look at contact sheets. Nothing goes to MTG until both are clean.
Cut app switchers, home screens, inboxes and anything showing balances or other apps.

## Script structure of every tutorial video (MTG, 7 Nov 2026: "Just like we did with the ALTRUVA tutorial videos")

1. **Greeting:** "Hi, my name is MTG, Your Digital Architect. Thank you for taking the time to watch this video." Say
   "video", not "training". Show his full profile photo, large (mtg-creative-standard Section 10a).
2. **In this video:** what you will show them, as a short list that fills in on screen as each item is said, so they know
   what to expect and what to ask. Then "Take your time. You can pause any step and follow along with me."
3. **The steps** (the meat and potatoes), every step voiced, with the success check.
4. **Recap:** "Let's recap what we covered in this video", ticking the same list item by item.
5. **Next video:** say what the next part will do, with its 2 or 3 actions on screen.
6. **Links and save/share**, then the **signature outro** (financial advice reminder, thank you, like/share/comment,
   massive action, "YOU are the best", "I'm MTG, Your Digital Architect. See you on the next one. Let's Get This Crypto!")
   with his photo, the brand line and the slogan. The closing track starts about 50 seconds before the end.

## Editing rules

- **Always show the browser address bar** when a new site or page opens, and point it out (ring plus a chip such as
  "Check the address: jetup.ibportal.io"), then zoom in. MTG: "so that they know they're at the right place".
- One action at a time: step card at the top (number, title, exact on-screen label in a highlight), the screen in a slim
  gold-titanium window, zoomed to the action, a ring on what to look at, a tap ripple where he taps, captions below.
- Show the success check of every step (for example "Registration Successful", "Email Verified!", "User Active").
- His mistakes and errors never appear. Turn the useful ones into tip cards (email already registered, wrong password,
  slow email, camera blocked by a screen recorder, documents already on another profile).
- Where he opened a sponsor's link, tell viewers to tap a sign-up button on MTG's website or use their own sponsor's
  Partner link.
- Steps the recorder could not capture (for example camera screens during KYC) are shown with his screenshots and cards.

## Voice

Build the first preview from banked lines (no credits). List the moments that only have on-screen text, propose new lines
with the character count and credit estimate (about 2 credits per 500 characters), and generate them only after MTG
approves. Check the finished audio by speech-to-text.

## After the parts are in

Update the facts register and the site pages from what the recordings show (MTG's screens win), cut chapter clips, then
the Getting started PDF and the master PDF companion, then the full consistency pass. Preview, publish only with approval.

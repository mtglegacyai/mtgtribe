# Privacy: hide everything personal in every frame

Tools: `tools/tutorial-redact/` (README there). Personal words (names, his own emails, phone and ID fragments) live in
`~/.tutorial-private-patterns.tsv`, never in the repository; recreate it in a new session from what is visible in the
recording, one `category<TAB>regex` line each.

Per clip (30 fps): timer bubble painted out; keyboard suggestion and autofill strip blanked; the focused field covered while
he types (label: First name, Last name, Your email, Your password, Your number); banded OCR in two modes plus an inverted
pass, covers carried along the measured scroll; labelled pills ("Your email", "Your ID", "Hidden" for the referrer).
Cut entirely: app switchers, home screens, inboxes, other apps, balances, camera screens.
Afterwards: OCR every second frame of the finished video (window crop, normal and inverted, two modes) for the private
patterns plus generic rules, and look at contact sheets. Zero flags before MTG sees it.

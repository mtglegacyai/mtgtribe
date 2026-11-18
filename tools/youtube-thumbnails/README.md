# YouTube thumbnails: the formula MTG approved (18 Nov 2026)

MTG on the Sonic AI + CopyX thumbnail: "That's much, much better, do this whenever I ask for these kinds of jobs." He turned down
a generic one ("JetUp Global Call": "boring ... you can do 100x better"). Start every thumbnail from these two:

- `sonic-copyx/` (the best one): the headline carries the title's words, and the right side SHOWS the idea as a little story
  (Sonic AI's card "BUY", a lime arrow "COPIED AUTOMATICALLY", "Your account: same trade, your name", a glowing gold bar).
- `jetup-bix-training/`: the words MTG asked for (JETUP / + BIX + TAG / TRAINING), big, with the BIX card as the visual.

## The formula
1. Headline: 3 stacked lines of Anton, 220 to 240 px on the 1920x1080 canvas, left half, white with the key word and the
   plus signs in lime (#CBFB61). Use the words of the video's title. Never a vague label ("Global Call").
2. The right half shows the idea in one glance: a before/after, a flow (this goes into that), or the product itself.
   Not just a stock picture: a picture that explains.
3. One red pill on top (#FF3B5C), 2 to 4 words of context (LIVE ON A PHONE, TAG MARKETS · GOLD).
4. One short line under the headline, with the key words in lime or gold.
5. The round JetUP logo in a gold ring top right. Never MTG's photo on JetUP thumbnails.
6. Keep the bottom right corner clear of anything important (YouTube's time badge sits there).
7. No money amounts, percentages, balances, profit screenshots, income promises or personal data. No dashes.
8. Check the 320 px version: the headline and the story must still read.

## Make one
Copy a folder, change the words and the visual in thumb.html, then:
`node tools/youtube-thumbnails/shoot.js tools/youtube-thumbnails/<folder>` (writes thumbnail.jpg and thumbnail-320.png).

# Closing track

Place MTG's approved closing track here as `they-call-me-mtg.mp3` (about 51 seconds). It is not stored in git.
If it is not attached, ask MTG for the mp3. Never substitute another song.

Then pass it to a composition, for example `closingTrack: 'music/they-call-me-mtg.mp3'` in its default props.
`src/components/ClosingTrack.tsx` starts it 50 seconds before the video ends, fades it in and out, and lowers it
under every spoken word (using the captions).

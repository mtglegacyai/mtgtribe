// MTG brand tokens, taken from the approved invite video (tools/invite-horizontal/stage.html)
// and the gold photo frame colours (brand-assets branch, brand/photo_card.py). MTG's photo is always shown in a circle.
// Rule: no em dashes or en dashes in any on-screen text.

export const BRAND = {
	line: 'MTG 👑 | Your Digital Architect',
	name: 'MTG',
	title: 'Your Digital Architect',
	// on-screen site: mtgtribe.com (mtg-hooks-standard). A video about another site can pass its address to <BrandBar site=... />
	site: 'mtgtribe.com',
	personalSite: 'MusaTheGiant.com',
	slogan: "Let's Get This Crypto! 💪",
} as const;

export const COLORS = {
	bg: '#050403',
	bgLift: '#15100a',
	gold: '#f2ad3c',
	goldHi: '#ffd98e',
	champagne: '#f7e6bf',
	text: '#f5efe6',
	muted: '#a39b8f',
	// photo frame gradient (photo_card.py GOLD_L and GOLD_D)
	frameLight: 'rgb(250, 228, 150)',
	frameDark: 'rgb(196, 142, 44)',
	frameGlow: 'rgba(232, 194, 90, 0.66)',
} as const;

// Files in public/.
// MTG, 9 November 2026: from video 05 on, every video uses his formal photo (navy blazer, white t-shirt, office view):
// "swap the image you've been using on the previous videos with this one going forward". It is a square crop of the
// photo he sent, centred on his face, in public/photos/. The earlier t-shirt photo (fetched from the brand-assets
// branch by scripts/fetch-brand.mjs) stays available as photoTshirt for re-renders of videos 01 to 04.
export const FILES = {
	photo: 'photos/mtg-photo-formal.jpg',
	faceCrop: 'photos/mtg-photo-formal-face.jpg',
	photoTshirt: 'brand/mtg-profile-photo.png',
	faceCropTshirt: 'brand/mtg-profile-face-crop.png',
	// MTG's approved 51 second closing track. Place the mp3 he supplies here (see public/music/README.md).
	closingTrack: 'music/they-call-me-mtg.mp3',
} as const;

/**
 * MTG, 7 November 2026: "Don't play the entire theme song, just only play the very last few seconds where it says
 * 'Let's Get This Crypto, wherever I go!'". That line, measured in the track: 48.56 s to the end (51.36 s).
 */
export const CLOSING_TAG = {from: 48.46, to: 51.36} as const;
export const CLOSING_TAG_SECONDS = CLOSING_TAG.to - CLOSING_TAG.from;
const CLOSING_TAG_GAP = 0.25; // pause between MTG's last spoken word and the song line
const CLOSING_TAG_END_PAD = 0.15; // the line ends this long before the last frame
/** End card length after the narration, so the tag plays right after the last word and ends with the video. */
export const closingTail = (lastWordEndSeconds: number, narrationSeconds: number) =>
	Math.max(0.5, lastWordEndSeconds + CLOSING_TAG_GAP + CLOSING_TAG_SECONDS + CLOSING_TAG_END_PAD - narrationSeconds);

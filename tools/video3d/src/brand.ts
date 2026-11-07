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

// Files in public/. MTG's photos are fetched by scripts/fetch-brand.mjs.
export const FILES = {
	photo: 'brand/mtg-profile-photo.png',
	faceCrop: 'brand/mtg-profile-face-crop.png',
	// MTG's approved 51 second closing track. Place the mp3 he supplies here (see public/music/README.md).
	closingTrack: 'music/they-call-me-mtg.mp3',
} as const;

export const CLOSING_TRACK_LEAD_SECONDS = 50; // the track starts 50 seconds before the video ends

import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {COLORS} from '../brand';
import {BODY, DISPLAY, MONO} from '../fonts';
import {BrandIcon, clamp, ease, fadeOut, GOLD_TEXT, usePop} from '../compositions/whatif01/ui';
import {PhotoCard} from './PhotoCard';
import {DEFAULT_PILLS, HintPill, SITE_PILLS, SitePillId, UrlPill} from './Pills';

/**
 * The end of every video from video 05 on (MTG, 9 and 10 November 2026), 9:16, in three steps timed to his words:
 *
 * 1. cardAt ("join the free MTG TRIBE ..."): the tribe invite with mtgtribe.com/group in a gold pill, and below it what
 *    people find on mtgtribe.com as 3 to 7 big pills that flip in one by one.
 * 2. photoAt ("I'm MTG ..."): his photo in the gold circle and his name take the top, side by side; the pills stay.
 * 3. sloganAt ("Let's Get This Crypto!"): his photo large, the signature, and under it the website in a big solid gold pill
 *    (MTG: "make it a little bit bigger and maybe even put it in a pill shape") plus the tribe address.
 *
 * Everything stays above y 1230, clear of the captions. The theme's last line plays over step 3 (ClosingTrack).
 */
export const EndScreen: React.FC<{t: number; cardAt: number; photoAt: number; sloganAt: number; pills?: SitePillId[]; pillsAt?: number}> = ({t, cardAt, photoAt, sloganAt, pills = DEFAULT_PILLS, pillsAt}) => {
	const list = pills.slice(0, 7);
	// pillsAt: when the pills start (default: right after the tribe card); set it to the words that name them
	const firstPill = pillsAt ?? cardAt + 0.9;
	const step = Math.min(0.55, Math.max(0.22, (photoAt - firstPill - 0.4) / Math.max(1, list.length)));
	const size = list.length <= 4 ? 42 : list.length === 5 ? 40 : list.length === 6 ? 36 : 34;
	const top = fadeOut(t, photoAt - 0.2, 0.3);
	return (
		<AbsoluteFill style={{opacity: ease(t, cardAt, 0.35)}}>
			{/* 1: the tribe invite (top zone, y 300 to 560) */}
			<div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18, opacity: Math.min(ease(t, cardAt + 0.05), top)}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 18, fontFamily: DISPLAY, fontSize: 70, lineHeight: 1, color: '#fff'}}>
					<BrandIcon icon="whatsapp" size={64} />
					<span>JOIN THE FREE <span style={GOLD_TEXT}>MTG TRIBE</span></span>
				</div>
				<UrlPill text="mtgtribe.com/group" size={58} t={t} at={cardAt + 0.25} />
				<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, opacity: ease(t, cardAt + 0.6)}}>A free WhatsApp community of action takers</div>
			</div>

			{/* 2: "I'm MTG": his photo and name take the same top zone, side by side */}
			<div style={{position: 'absolute', top: 290, width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 34, opacity: Math.min(ease(t, photoAt, 0.4), fadeOut(t, sloganAt - 0.2, 0.3))}}>
				<PhotoCard size={240} />
				<div>
					<div style={{fontFamily: DISPLAY, fontSize: 96, lineHeight: 1, ...GOLD_TEXT}}>MTG</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text, marginTop: 8}}>Your Digital<br />Architect</div>
				</div>
			</div>

			{/* 1 and 2: what people find on mtgtribe.com, as pills (y 610 to 1230, clear of the captions) */}
			<div style={{position: 'absolute', top: 610, left: 40, right: 40, opacity: fadeOut(t, sloganAt - 0.15, 0.3)}}>
				<div style={{textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 3, color: COLORS.goldHi, opacity: ease(t, firstPill - 0.2), marginBottom: 16}}>ON MTGTRIBE.COM YOU'LL FIND</div>
				<div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: `${size > 36 ? 16 : 12}px 14px`}}>
					{list.map((id, i) => {
						const [icon, text] = SITE_PILLS[id];
						return <HintPill key={id} icon={icon} text={text} size={size} t={t} at={firstPill + i * step} />;
					})}
				</div>
			</div>

			{/* 3: the signature: big photo, the slogan, then the website in a big gold pill and the tribe address */}
			<div style={{position: 'absolute', top: 280, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8, opacity: ease(t, sloganAt - 0.1, 0.4)}}>
				<PhotoCard size={300} />
				<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1, ...GOLD_TEXT, marginTop: 8}}>MTG</div>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 38, color: COLORS.text}}>Your Digital Architect</div>
			</div>
			<div style={{position: 'absolute', top: 790, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26}}>
				<div style={{opacity: ease(t, sloganAt), transform: `scale(${interpolate(usePop(sloganAt, 12), [0, 1], [0.7, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 96, ...GOLD_TEXT}}>Let's Get This Crypto!</span> <span style={{fontFamily: DISPLAY, fontSize: 96}}>💪</span>
				</div>
				<UrlPill text="mtgtribe.com" size={72} t={t} at={sloganAt + 0.35} />
				<div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '12px 30px', borderRadius: 999, border: '2.5px solid rgba(242,173,60,0.85)', background: 'rgba(18,14,9,0.94)', opacity: ease(t, sloganAt + 0.75), transform: `translateY(${interpolate(t, [sloganAt + 0.75, sloganAt + 1.15], [20, 0], clamp)}px)`}}>
					<BrandIcon icon="whatsapp" size={40} />
					<span style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, color: COLORS.text}}>Join the tribe: <span style={{color: COLORS.goldHi}}>mtgtribe.com/group</span></span>
				</div>
			</div>
		</AbsoluteFill>
	);
};

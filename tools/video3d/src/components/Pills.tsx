import React from 'react';
import {interpolate} from 'remotion';
import {COLORS} from '../brand';
import {BODY} from '../fonts';
import {clamp, ease} from '../compositions/whatif01/ui';

// Pills (MTG, 10 November 2026): "put it in a pill shape, just like we've been doing with the explainer videos explaining
// JetUp". Same idea as the JetUp explainers (fully rounded capsules, thin outline, an emoji, the address in a solid
// bright pill), in MTG's gold and black.

/** A web address in a solid gold pill: the address people should remember (big, dark text, soft gold glow). */
export const UrlPill: React.FC<{text: string; size?: number; t?: number; at?: number; style?: React.CSSProperties}> = ({text, size = 60, t, at, style}) => {
	const p = t === undefined || at === undefined ? 1 : ease(t, at, 0.45);
	// a soft light sweep crosses the pill once after it lands (a small 3D-feeling shine, no arbitrary motion)
	const sweep = t === undefined || at === undefined ? -1 : interpolate(t, [at + 0.5, at + 1.4], [-0.3, 1.3], clamp);
	return (
		<div style={{perspective: 900, display: 'inline-block', ...style}}>
			<div
				style={{
					position: 'relative', overflow: 'hidden', display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
					height: Math.round(size * 1.9), padding: `0 ${Math.round(size * 0.85)}px`, borderRadius: 999, boxSizing: 'border-box',
					background: `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold} 55%, #c98a2b)`,
					boxShadow: `inset 0 2px 0 rgba(255,240,200,0.75), inset 0 -3px 0 rgba(120,70,10,0.35), 0 16px 40px rgba(0,0,0,0.55), 0 0 44px rgba(242,173,60,0.35)`,
					fontFamily: BODY, fontWeight: 800, fontSize: size, lineHeight: 1, color: '#1a1206', whiteSpace: 'nowrap',
					opacity: p, transform: `rotateX(${(1 - p) * -70}deg) scale(${0.85 + 0.15 * p})`, transformOrigin: '50% 100%',
				}}
			>
				{text}
				{sweep > -0.3 && sweep < 1.3 && (
					<div style={{position: 'absolute', top: 0, bottom: 0, width: '35%', left: `${sweep * 100 - 17}%`, background: 'linear-gradient(100deg, transparent, rgba(255,255,255,0.55), transparent)', transform: 'skewX(-18deg)'}} />
				)}
			</div>
		</div>
	);
};

/** A dark capsule with a thin gold outline, an emoji and a short line: one thing people find on the website. */
export const HintPill: React.FC<{icon: React.ReactNode; text: string; size?: number; t?: number; at?: number; style?: React.CSSProperties}> = ({icon, text, size = 38, t, at, style}) => {
	const p = t === undefined || at === undefined ? 1 : ease(t, at, 0.4);
	return (
		<div style={{perspective: 900, display: 'inline-block', ...style}}>
			<div
				style={{
					display: 'inline-flex', alignItems: 'center', gap: Math.round(size * 0.45), minHeight: Math.round(size * 2.15),
					padding: `${Math.round(size * 0.3)}px ${Math.round(size * 0.75)}px`, borderRadius: 999, boxSizing: 'border-box',
					background: 'rgba(18,14,9,0.94)', border: `2.5px solid rgba(242,173,60,0.85)`,
					boxShadow: '0 12px 30px rgba(0,0,0,0.5), 0 0 22px rgba(242,173,60,0.12)',
					opacity: p, transform: `rotateX(${(1 - p) * 80}deg) translateY(${(1 - p) * 24}px)`, transformOrigin: '50% 0%',
				}}
			>
				<span style={{fontSize: size * 1.05, lineHeight: 1}}>{icon}</span>
				<span style={{fontFamily: BODY, fontWeight: 800, fontSize: size, lineHeight: 1.15, color: COLORS.text}}>{text}</span>
			</div>
		</div>
	);
};

/**
 * What people really find on mtgtribe.com (checked against the site on 10 November 2026: home page description, the
 * invite video description and the dashboard). Pick 3 to 7 per video, the ones that fit its topic (MTG: "4 or 5, but
 * definitely not more than 7, depending on how big the topic is"). Never add a line the site does not deliver.
 */
export const SITE_PILLS = {
	tutorials: ['🎬', 'Step-by-step tutorial videos'],
	explainers: ['💡', 'Explainer videos'],
	streams: ['💰', 'Multiple streams of income'],
	honest: ['⚖️', 'Honest guides, risks included'],
	crypto: ['🪙', 'Crypto portfolio basics'],
	ai: ['🤖', 'AI skills and tutorials'],
	wallet: ['🔐', 'Your own wallet and keys'],
	tools: ['🧮', 'Free tools and calculators'],
	traffic: ['📈', 'Traffic strategies'],
	websites: ['🌐', 'Websites with your own links'],
	tribe: ['🤝', 'A tribe of action takers'],
} as const;
export type SitePillId = keyof typeof SITE_PILLS;
export const DEFAULT_PILLS: SitePillId[] = ['tutorials', 'explainers', 'streams', 'crypto', 'ai'];

import React from 'react';
import {
	AbsoluteFill, Easing, Html5Audio, interpolate, OffthreadVideo, random, Sequence, spring, staticFile, useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import * as si from 'simple-icons';
import {COLORS} from '../../brand';
import {MONO} from '../../fonts';
import {useLayout} from '../../lib/layout';

// Shared building blocks for video 01 (v2): both orientations, 3D entrances, camera drift, sound cues.
// Every visual is timed in seconds inside its section (the narration's own word timings).

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const GOLD_TEXT: React.CSSProperties = {
	background: `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #c98a2b)`,
	WebkitBackgroundClip: 'text',
	backgroundClip: 'text',
	color: 'transparent',
};

export const useV = () => useLayout().vertical;

/** Seconds since the start of the current section. */
export const useT = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return frame / fps;
};

/** 0 to 1, eased, starting at `at` seconds. */
export const ease = (t: number, at: number, d = 0.4) =>
	interpolate(t, [at, at + d], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});

/** 1 to 0, eased, starting at `at` seconds. */
export const fadeOut = (t: number, at: number, d = 0.3) => 1 - ease(t, at, d);

/** A springy 0 to about 1 starting at `at` seconds. */
export const usePop = (at: number, damping = 14) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return spring({frame: frame - Math.round(at * fps), fps, config: {damping}});
};

export const Backdrop: React.FC = () => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	return (
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #2b1e0c 0%, ${COLORS.bgLift} 42%, ${COLORS.bg} 82%)`}}>
			{Array.from({length: 60}, (_, i) => {
				const depth = 0.4 + random(`d${i}`) * 1.2; // near dots move faster and look bigger: parallax depth
				const x = (random(`x${i}`) * width + frame * 0.15 * depth) % width;
				const y = ((random(`y${i}`) * height - frame * (0.2 + 0.5 * depth)) % height + height) % height;
				const size = 2 + depth * 5;
				return (
					<div key={i} style={{position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: '50%', background: COLORS.goldHi, opacity: 0.06 + depth * 0.14, filter: `blur(${depth > 1.2 ? 2.5 : 1}px)`}} />
				);
			})}
		</AbsoluteFill>
	);
};

/**
 * The area scenes draw in, clear of the brand bar and of the captions (and of the TikTok, Reels and Shorts buttons
 * on phones). It drifts gently forward like a slow camera push-in, so no frame is ever static.
 */
export const Stage: React.FC<{children: React.ReactNode; style?: React.CSSProperties; drift?: boolean}> = ({children, style, drift = true}) => {
	const t = useT();
	const v = useV();
	const push = drift ? 1 + Math.min(0.045, t * 0.0022) : 1;
	return (
		<AbsoluteFill
			style={{
				top: v ? 230 : 100, bottom: v ? 700 : 200, left: v ? 50 : 80, right: v ? 50 : 80, height: 'auto', width: 'auto',
				justifyContent: 'center', alignItems: 'center', transform: `scale(${push})`, ...style,
			}}
		>
			{children}
		</AbsoluteFill>
	);
};

/** 3D entrance: tips forward from depth, like a card turned toward the camera. */
export const Flip: React.FC<{at: number; children: React.ReactNode; from?: 'x' | 'y'; style?: React.CSSProperties; out?: number}> = ({at, children, from = 'x', style, out}) => {
	const t = useT();
	const p = usePop(at, 15);
	const o = Math.min(ease(t, at, 0.3), out === undefined ? 1 : fadeOut(t, out));
	const rot = interpolate(p, [0, 1], [from === 'x' ? 55 : -60, 0]);
	return (
		<div style={{perspective: 1400, opacity: o, ...style}}>
			<div style={{transform: `${from === 'x' ? 'rotateX' : 'rotateY'}(${rot}deg) translateZ(${interpolate(p, [0, 1], [-200, 0])}px)`, transformOrigin: from === 'x' ? 'center bottom' : 'left center'}}>
				{children}
			</div>
		</div>
	);
};

export const Panel: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<div
		style={{
			background: 'linear-gradient(160deg, rgba(255,255,255,0.09), rgba(255,255,255,0.02))',
			border: '1.5px solid rgba(242,173,60,0.5)',
			borderRadius: 32,
			boxShadow: '0 40px 90px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.12), 0 0 70px rgba(242,173,60,0.12)',
			padding: '30px 38px',
			...style,
		}}
	>
		{children}
	</div>
);

export const Chip: React.FC<{children: React.ReactNode; size?: number; style?: React.CSSProperties}> = ({children, size = 34, style}) => (
	<div
		style={{
			display: 'inline-block', padding: '12px 28px', borderRadius: 999, border: `2px solid ${COLORS.gold}`,
			background: 'rgba(20,14,6,0.8)', color: COLORS.goldHi, fontFamily: MONO, fontWeight: 700,
			fontSize: size, letterSpacing: 2, lineHeight: 1.25, ...style,
		}}
	>
		{children}
	</div>
);

/** Fades a whole section in and out at its edges. */
export const Section: React.FC<{children: React.ReactNode; seconds: number}> = ({children, seconds}) => {
	const t = useT();
	const o = Math.min(ease(t, 0, 0.25), fadeOut(t, seconds - 0.05, 0.25));
	return <AbsoluteFill style={{opacity: o}}>{children}</AbsoluteFill>;
};

/** One of Leo's HeyGen clips, muted, in a rounded gold window, or full screen. */
export const LeoClip: React.FC<{clip: string; from: number; seconds: number; style?: React.CSSProperties; full?: boolean; trim?: number; focus?: string}> = ({clip, from, seconds, style, full, trim = 0, focus}) => {
	const {fps} = useVideoConfig();
	return (
		<Sequence from={Math.round(from * fps)} durationInFrames={Math.round(seconds * fps)} layout="none" name={`Leo ${clip}`}>
			<LeoWindow clip={clip} style={style} full={full} trim={Math.round(trim * fps)} focus={focus} />
		</Sequence>
	);
};

// focus: which part of the clip a cropped window keeps (CSS object-position), e.g. '50% 3%' keeps Leo's face.
const LeoWindow: React.FC<{clip: string; style?: React.CSSProperties; full?: boolean; trim: number; focus?: string}> = ({clip, style, full, trim, focus = '50% 50%'}) => {
	const t = useT();
	const enter = usePop(0, 16);
	const video = <OffthreadVideo src={staticFile(`videos/01/leo/${clip}.mp4`)} muted trimBefore={trim} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: focus}} />;
	if (full) {
		return <AbsoluteFill style={{opacity: ease(t, 0, 0.25), transform: `scale(${interpolate(enter, [0, 1], [1.06, 1])})`}}>{video}</AbsoluteFill>;
	}
	return (
		<div style={{position: 'absolute', perspective: 1400, ...style}}>
			<div
				style={{
					width: '100%', height: '100%', overflow: 'hidden', borderRadius: 32, border: `3px solid ${COLORS.gold}`,
					boxShadow: '0 30px 80px rgba(0,0,0,0.6), 0 0 50px rgba(242,173,60,0.25)', opacity: enter,
					transform: `rotateY(${interpolate(enter, [0, 1], [-35, 0])}deg) scale(${interpolate(enter, [0, 1], [0.9, 1])})`,
				}}
			>
				{video}
			</div>
		</div>
	);
};

/**
 * Sound cues: [seconds, effect name, volume]. Effects live in public/sfx/: MTG's soft palette (scripts/make_sound.py),
 * all at the same loudness, so the volume here is the real balance. 0.3 to 0.6 keeps them 8 to 14 dB under his voice.
 */
export type Cue = [number, string, number?];
export const Cues: React.FC<{list: Cue[]}> = ({list}) => {
	const {fps} = useVideoConfig();
	return (
		<>
			{list.map(([at, name, vol = 0.4], i) => (
				<Sequence key={i} from={Math.max(0, Math.round(at * fps))} layout="none" name={`sfx ${name}`}>
					<Html5Audio src={staticFile(`sfx/${name}.mp3`)} volume={vol} />
				</Sequence>
			))}
		</>
	);
};

export const BrandIcon: React.FC<{icon: 'whatsapp' | 'telegram' | 'tiktok' | 'youtube'; size: number}> = ({icon, size}) => {
	const map = {whatsapp: si.siWhatsapp, telegram: si.siTelegram, tiktok: si.siTiktok, youtube: si.siYoutube};
	const ic = map[icon];
	const fill = icon === 'tiktok' ? '#ffffff' : `#${ic.hex}`;
	return (
		<svg width={size} height={size} viewBox="0 0 24 24" role="img" aria-label={ic.title}>
			<path d={ic.path} fill={fill} />
		</svg>
	);
};

export const Loaf: React.FC<{size: number; pulse?: number}> = ({size, pulse = 0}) => (
	<svg width={size} height={size * 0.63} viewBox="0 0 200 126" style={{transform: `scale(${1 + pulse * 0.07})`, filter: 'drop-shadow(0 18px 24px rgba(0,0,0,0.5))'}}>
		<defs>
			<linearGradient id="crust01" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor="#f6c56a" />
				<stop offset="0.55" stopColor="#d98b2e" />
				<stop offset="1" stopColor="#9a5a1c" />
			</linearGradient>
		</defs>
		<ellipse cx="100" cy="119" rx="92" ry="5" fill="rgba(0,0,0,0.45)" />
		<path d="M14 108 C6 74 22 30 64 20 C88 8 126 8 146 18 C184 30 198 74 188 108 Q186 118 172 118 L28 118 Q16 118 14 108 Z" fill="url(#crust01)" />
		{[56, 92, 128].map((x) => (
			<path key={x} d={`M${x} 34 q12 22 4 48`} stroke="#fbe2a6" strokeWidth="7" strokeLinecap="round" fill="none" opacity="0.85" />
		))}
		<ellipse cx="70" cy="40" rx="30" ry="9" fill="#fff6dc" opacity="0.28" />
	</svg>
);

/** A generic illustrated banknote (deliberately not a copy of any real note design). */
export const Note: React.FC<{width: number; label?: string; grey?: number; style?: React.CSSProperties}> = ({width, label = 'Z$', grey = 0, style}) => (
	<div
		style={{
			width, height: width * 0.45, borderRadius: width * 0.03, position: 'relative', overflow: 'hidden', flexShrink: 0,
			background: 'linear-gradient(120deg, #3c5a3a, #6f8f5a 45%, #3f6b52)', filter: `grayscale(${grey})`,
			border: '2px solid rgba(255,255,255,0.25)', boxShadow: '0 10px 24px rgba(0,0,0,0.45)', ...style,
		}}
	>
		<div style={{position: 'absolute', inset: width * 0.035, border: '2px solid rgba(255,255,255,0.35)', borderRadius: width * 0.02}} />
		<div style={{position: 'absolute', right: width * 0.08, top: '50%', transform: 'translateY(-50%)', width: width * 0.22, height: width * 0.22, borderRadius: '50%', border: '3px solid rgba(255,255,255,0.35)'}} />
		<div style={{position: 'absolute', left: width * 0.08, top: width * 0.06, fontFamily: MONO, fontWeight: 700, color: 'rgba(255,255,255,0.85)', fontSize: width * 0.09}}>{label}</div>
	</div>
);

/** A gold coin that flips once into view (3D). */
export const Coin: React.FC<{symbol: string; size: number; at: number}> = ({symbol, size, at}) => {
	const p = usePop(at, 12);
	return (
		<div style={{perspective: 900, opacity: Math.min(1, p * 1.5)}}>
			<div
				style={{
					width: size, height: size, borderRadius: '50%', transform: `rotateY(${interpolate(p, [0, 1], [180, 0])}deg) scale(${interpolate(p, [0, 1], [0.6, 1])})`,
					background: `radial-gradient(circle at 35% 30%, ${COLORS.goldHi}, ${COLORS.gold} 55%, #a8701f)`, display: 'flex', alignItems: 'center', justifyContent: 'center',
					fontFamily: 'Anton, Impact, sans-serif', fontSize: size * 0.6, color: '#3a2508', boxShadow: '0 20px 40px rgba(0,0,0,0.5), inset 0 -8px 16px rgba(0,0,0,0.25)',
				}}
			>
				{symbol}
			</div>
		</div>
	);
};

import React from 'react';
import {AbsoluteFill, Easing, interpolate, random, Sequence, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS} from '../brand';
import {BrandBar} from '../components/BrandBar';
import {BODY, DISPLAY, MONO} from '../fonts';
import {useLayout} from '../lib/layout';

// Graphics proof for video 01 (What If Prices Doubled Every Day?): three premium motion-graphics panels in MTG's
// black-and-gold look. Silent style test, not a finished video. Facts: tools/videos/01-what-if-prices-doubled/research.md

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const GOLD_TEXT: React.CSSProperties = {
	background: `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #c98a2b)`,
	WebkitBackgroundClip: 'text',
	backgroundClip: 'text',
	color: 'transparent',
};
const rand = (n: number) => `R${Math.round(n).toLocaleString('en-US')}`;

export const DOUBLING_PROOF_FRAMES = 480; // 16 s at 30 fps

const Backdrop: React.FC = () => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	return (
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 42%, #2b1e0c 0%, ${COLORS.bgLift} 40%, ${COLORS.bg} 80%)`}}>
			{Array.from({length: 36}, (_, i) => {
				const x = random(`x${i}`) * width;
				const y = ((random(`y${i}`) * height - frame * (0.3 + random(`s${i}`) * 0.7)) % height + height) % height;
				const size = 3 + random(`r${i}`) * 7;
				return (
					<div
						key={i}
						style={{
							position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: '50%',
							background: COLORS.goldHi, opacity: 0.12 + random(`o${i}`) * 0.25, filter: 'blur(1.5px)',
						}}
					/>
				);
			})}
		</AbsoluteFill>
	);
};

// A glass card with a gold edge: the premium panel used in every scene.
const Panel: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<div
		style={{
			background: 'linear-gradient(160deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02))',
			border: '1.5px solid rgba(242,173,60,0.45)',
			borderRadius: 36,
			boxShadow: '0 30px 80px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.1), 0 0 60px rgba(242,173,60,0.10)',
			padding: '34px 40px',
			...style,
		}}
	>
		{children}
	</div>
);

const Chip: React.FC<{children: React.ReactNode; size?: number}> = ({children, size = 30}) => (
	<div
		style={{
			display: 'inline-block', padding: '10px 26px', borderRadius: 999, border: `2px solid ${COLORS.gold}`,
			background: 'rgba(242,173,60,0.12)', color: COLORS.goldHi, fontFamily: MONO, fontWeight: 700,
			fontSize: size, letterSpacing: 2,
		}}
	>
		{children}
	</div>
);

// Enters with a spring, leaves with a fade, inside its Sequence.
const Scene: React.FC<{children: React.ReactNode; length: number}> = ({children, length}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const {vertical} = useLayout();
	const enter = spring({frame, fps, config: {damping: 16, mass: 0.7}});
	const exit = interpolate(frame, [length - 10, length], [1, 0], clamp);
	return (
		<AbsoluteFill
			style={{
				justifyContent: 'center', alignItems: 'center', opacity: Math.min(enter, exit), paddingBottom: vertical ? 200 : 0,
				transform: `translateY(${(1 - enter) * 40}px) scale(${interpolate(enter, [0, 1], [0.96, 1])})`,
			}}
		>
			{children}
		</AbsoluteFill>
	);
};

const Loaf: React.FC<{size: number; pulse: number}> = ({size, pulse}) => (
	<svg width={size} height={size * 0.63} viewBox="0 0 200 126" style={{transform: `scale(${1 + pulse * 0.06})`, filter: 'drop-shadow(0 18px 24px rgba(0,0,0,0.5))'}}>
		<defs>
			<linearGradient id="crust" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor="#f6c56a" />
				<stop offset="0.55" stopColor="#d98b2e" />
				<stop offset="1" stopColor="#9a5a1c" />
			</linearGradient>
		</defs>
		<ellipse cx="100" cy="119" rx="92" ry="5" fill="rgba(0,0,0,0.45)" />
		<path d="M14 108 C6 74 22 30 64 20 C88 8 126 8 146 18 C184 30 198 74 188 108 Q186 118 172 118 L28 118 Q16 118 14 108 Z" fill="url(#crust)" />
		{[56, 92, 128].map((x) => (
			<path key={x} d={`M${x} 34 q12 22 4 48`} stroke="#fbe2a6" strokeWidth="7" strokeLinecap="round" fill="none" opacity="0.85" />
		))}
		<path d="M40 28 C70 12 130 12 160 28" stroke="#fff3cf" strokeWidth="5" strokeLinecap="round" fill="none" opacity="0.5" />
		<ellipse cx="70" cy="40" rx="30" ry="9" fill="#fff6dc" opacity="0.28" />
		{[[40, 80], [150, 86], [110, 96], [72, 98], [168, 70]].map(([x, y]) => (
			<circle key={`${x}-${y}`} cx={x} cy={y} r="2.2" fill="#7a4313" opacity="0.5" />
		))}
	</svg>
);

// Scene 1: today R10, then double every day: 30 days later, R10,737,418,240.
const PriceScene: React.FC<{length: number}> = ({length}) => {
	const frame = useCurrentFrame();
	const {vertical} = useLayout();
	// the first three doublings are slow enough to read, then it accelerates
	const days =
		frame < 20 ? 0 : frame < 80 ? 1 + Math.floor((frame - 20) / 20) : Math.min(30, 3 + Math.floor(27 * Easing.in(Easing.cubic)(Math.min(1, (frame - 80) / 60))));
	const stepStart = frame < 80 ? 20 + (days - 1) * 20 : 0;
	const pulse = days > 0 && days <= 3 ? interpolate(frame - stepStart, [0, 4, 12], [0, 1, 0], clamp) : 0;
	const done = days === 30;
	const glow = done ? interpolate(frame, [140, 155], [0, 1], clamp) : 0;
	const priceSize = vertical ? 132 : 140;
	return (
		<Scene length={length}>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: vertical ? 48 : 28}}>
				<Chip size={vertical ? 40 : 30}>IMAGINE THIS</Chip>
				<Loaf size={vertical ? 540 : 320} pulse={pulse} />
				<Panel style={{textAlign: 'center', minWidth: vertical ? 960 : 1100}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: vertical ? 46 : 34, color: COLORS.muted, letterSpacing: 3}}>
						{days === 0 ? 'TODAY' : days === 30 ? '30 DAYS LATER' : `+${days} DAY${days > 1 ? 'S' : ''}`}
					</div>
					<div
						style={{
							fontFamily: DISPLAY, fontSize: priceSize, lineHeight: 1.1, marginTop: 8, ...GOLD_TEXT,
							filter: `drop-shadow(0 0 ${glow * 28}px rgba(255,217,142,${0.55 * glow}))`,
						}}
					>
						{rand(10 * 2 ** days)}
					</div>
					<div style={{marginTop: 22, height: 14, borderRadius: 7, background: 'rgba(255,255,255,0.08)', overflow: 'hidden'}}>
						<div style={{width: `${(days / 30) * 100}%`, height: '100%', background: `linear-gradient(90deg, ${COLORS.gold}, ${COLORS.goldHi})`}} />
					</div>
					<div style={{marginTop: 18, fontFamily: BODY, fontWeight: 700, fontSize: vertical ? 40 : 30, color: COLORS.text, opacity: done ? 1 : 0.65}}>
						One loaf of bread, if prices double every day
					</div>
				</Panel>
			</div>
		</Scene>
	);
};

// Scene 2: your pay, Friday to Friday, when prices double every day.
const DAYS = ['FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI'];
const LABELS = ['100%', '50%', '25%', '12.5%', '6.3%', '3.1%', '1.6%', '0.8%'];
const PayScene: React.FC<{length: number}> = ({length}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const {vertical} = useLayout();
	const maxH = vertical ? 680 : 400;
	const barW = vertical ? 92 : 110;
	const callout = spring({frame: frame - 78, fps, config: {damping: 12}});
	return (
		<Scene length={length}>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 30}}>
				<Chip size={vertical ? 38 : 30}>YOUR PAY, FRIDAY TO FRIDAY</Chip>
				<Panel style={{paddingBottom: 26}}>
					<div style={{display: 'flex', alignItems: 'flex-end', gap: vertical ? 18 : 30, height: maxH + 70}}>
						{DAYS.map((d, i) => {
							const grow = spring({frame: frame - 10 - i * 7, fps, config: {damping: 15}});
							const h = Math.max(4, maxH * 0.5 ** i * grow);
							const last = i === DAYS.length - 1;
							return (
								<div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: barW}}>
									<div style={{fontFamily: MONO, fontWeight: 700, fontSize: vertical ? 28 : 26, color: last ? COLORS.goldHi : COLORS.text, opacity: grow, marginBottom: 8}}>
										{LABELS[i]}
									</div>
									<div
										style={{
											width: barW, height: h, borderRadius: 14,
											background: last ? `linear-gradient(180deg, #ffb35c, #e0602f)` : `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold})`,
											boxShadow: last ? `0 0 ${30 * callout}px rgba(255,140,60,0.7)` : '0 10px 30px rgba(0,0,0,0.35)',
										}}
									/>
									<div style={{fontFamily: MONO, fontSize: vertical ? 30 : 26, color: COLORS.muted, marginTop: 12}}>{d}</div>
								</div>
							);
						})}
					</div>
				</Panel>
				<div style={{fontFamily: DISPLAY, fontSize: vertical ? 120 : 100, transform: `scale(${callout})`, ...GOLD_TEXT}}>UNDER 1%</div>
				<div style={{fontFamily: BODY, fontSize: vertical ? 32 : 26, color: COLORS.muted, maxWidth: vertical ? 900 : 1300, textAlign: 'center'}}>
					Zimbabwe, November 2008: prices doubled about every 24.7 hours (Hanke and Kwok). Simplified here to every day.
				</div>
			</div>
		</Scene>
	);
};

// Scene 3: guess the zeros, then count them in: 100,000,000,000,000.
const ZerosScene: React.FC<{length: number}> = ({length}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const {vertical} = useLayout();
	const zeros = Math.max(0, Math.min(14, Math.floor((frame - 40) / 5) + 1));
	const digits = '1' + '0'.repeat(zeros);
	const grouped = digits.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	const done = zeros === 14;
	const reveal = spring({frame: frame - 40 - 14 * 5, fps, config: {damping: 13}});
	return (
		<Scene length={length}>
			<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 34}}>
				<Chip size={vertical ? 36 : 30}>GUESS FIRST: HOW MANY ZEROS? 💬</Chip>
				<Panel style={{textAlign: 'center', minWidth: vertical ? 960 : 1300}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: vertical ? 40 : 30, color: COLORS.muted, letterSpacing: 3}}>ONE BANKNOTE</div>
					<div style={{fontFamily: DISPLAY, fontSize: vertical ? 92 : 150, lineHeight: 1.15, marginTop: 6, ...GOLD_TEXT}}>
						Z${grouped}
					</div>
					<div style={{display: 'flex', justifyContent: 'center', gap: vertical ? 10 : 12, marginTop: 18}}>
						{Array.from({length: 14}, (_, i) => (
							<div key={i} style={{width: vertical ? 40 : 46, height: 10, borderRadius: 5, background: i < zeros ? COLORS.goldHi : 'rgba(255,255,255,0.1)'}} />
						))}
					</div>
				</Panel>
				<div style={{fontFamily: DISPLAY, fontSize: vertical ? 170 : 130, opacity: done ? 1 : 0, transform: `scale(${done ? reveal : 0.8})`, ...GOLD_TEXT}}>
					14 ZEROS
				</div>
				<div style={{opacity: done ? reveal : 0}}>
					<Chip size={vertical ? 36 : 28}>Z$100 TRILLION ▪ JANUARY 2009</Chip>
				</div>
			</div>
		</Scene>
	);
};

export const DoublingProof: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<Backdrop />
		<Sequence from={0} durationInFrames={165} name="Bread price doubling">
			<PriceScene length={165} />
		</Sequence>
		<Sequence from={165} durationInFrames={140} name="Pay, Friday to Friday">
			<PayScene length={140} />
		</Sequence>
		<Sequence from={305} durationInFrames={175} name="Guess the zeros">
			<ZerosScene length={175} />
		</Sequence>
		<BrandBar />
	</AbsoluteFill>
);

import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, random, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/04/captions.json';
import timeline from '../../../public/videos/04/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {PhotoCard} from '../../components/PhotoCard';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, LeoClip, Note, Panel, SiteCard, usePop, useT} from '../whatif01/ui';

// Video 04 (9 Nov 2026, daily video): Myth or Fact: Is Your Money in a Vault? A 9:16 Short in the house format.
// Script and research: tools/videos/04-myth-or-fact-money-in-a-vault/. Times are seconds from the start (HeyGen word
// timings). Facts on screen: Bank of England Quarterly Bulletin 2014 Q1 (UK: 97% deposits, 3% notes and coins) and
// SARB CODI deposit insurance (R100,000 per depositor, per bank, since 1 April 2024).

export const MOF04_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const MOF04_FRAMES = Math.ceil((timeline.total + TAIL) * MOF04_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
/** A slow camera push-in across a scene. */
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.04], clamp)})`;

const RED = '#e0602f';
const GREEN_CELL = 'linear-gradient(145deg, #8fc27a, #4f8a4a 60%, #2f5f3a)';

const Stamp: React.FC<{text: string; at: number; color?: string; size?: number; rotate?: number}> = ({text, at, color = RED, size = 150, rotate = -10}) => {
	const t = useT();
	return (
		<span style={{display: 'inline-block', opacity: ease(t, at, 0.15), transform: `rotate(${rotate}deg) scale(${interpolate(usePop(at, 11), [0, 1], [1.7, 1])})`, border: `${size * 0.055}px solid ${color}`, color: color === RED ? '#ff8a4c' : COLORS.goldHi, fontFamily: DISPLAY, fontSize: size, lineHeight: 1.15, padding: `0 ${size * 0.24}px`, borderRadius: 14, background: 'rgba(5,4,3,0.78)', boxShadow: '0 20px 50px rgba(0,0,0,0.6)'}}>{text}</span>
	);
};

/** A round vault door: the wheel turns, then the door swings open on what is inside. */
const Vault: React.FC<{size: number; wheel: number; open: number; children?: React.ReactNode}> = ({size, wheel, open, children}) => {
	const inset = size * 0.06;
	return (
		<div style={{width: size, height: size, position: 'relative', perspective: size * 3}}>
			<div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: 'linear-gradient(145deg, #5a4220, #2a1e0e 55%, #6b4f22)', boxShadow: `0 0 0 3px ${COLORS.gold}, 0 30px 80px rgba(0,0,0,0.7), 0 0 60px rgba(242,173,60,0.18)`}} />
			<div style={{position: 'absolute', inset, borderRadius: '50%', overflow: 'hidden', background: 'radial-gradient(circle at 50% 45%, #2a1f10, #0a0805 75%)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
				{children}
			</div>
			<div style={{position: 'absolute', inset, transformOrigin: 'left center', transform: `rotateY(${-78 * open}deg)`, filter: `brightness(${1 - 0.35 * open})`}}>
				<svg width="100%" height="100%" viewBox="0 0 200 200" style={{display: 'block'}}>
					<defs>
						<radialGradient id="v04door" cx="0.4" cy="0.35" r="0.75">
							<stop offset="0" stopColor={COLORS.goldHi} />
							<stop offset="0.55" stopColor={COLORS.gold} />
							<stop offset="1" stopColor="#8a5a18" />
						</radialGradient>
					</defs>
					<circle cx="100" cy="100" r="100" fill="url(#v04door)" />
					<circle cx="100" cy="100" r="84" fill="none" stroke="#6b4512" strokeWidth="3" />
					<circle cx="100" cy="100" r="64" fill="none" stroke="rgba(90,58,16,0.55)" strokeWidth="2" />
					{Array.from({length: 12}, (_, i) => {
						const a = (i / 12) * Math.PI * 2;
						return <circle key={i} cx={100 + Math.cos(a) * 92} cy={100 + Math.sin(a) * 92} r="3.6" fill="#5a3a10" />;
					})}
					<g transform={`rotate(${wheel} 100 100)`}>
						{[0, 120, 240].map((d) => (
							<g key={d} transform={`rotate(${d} 100 100)`}>
								<rect x="96" y="44" width="8" height="56" rx="3" fill="#4a300c" />
								<circle cx="100" cy="42" r="9" fill="#4a300c" />
							</g>
						))}
						<circle cx="100" cy="100" r="18" fill="#4a300c" />
						<circle cx="100" cy="100" r="8" fill={COLORS.goldHi} />
					</g>
				</svg>
			</div>
		</div>
	);
};

/** A bundle of notes with a name tag, the picture many people have of their savings. */
const Bundle: React.FC<{size: number; tag: number}> = ({size, tag}) => (
	<div style={{position: 'relative', width: size, height: size * 0.62}}>
		{[0, 1, 2].map((k) => (
			<Note key={k} width={size} label="R" style={{position: 'absolute', left: 0, top: size * (0.16 - k * 0.07)}} />
		))}
		<div style={{position: 'absolute', left: size * 0.36, top: size * -0.02, width: size * 0.16, bottom: size * 0.02, background: 'rgba(242,173,60,0.85)', borderRadius: 4}} />
		<div style={{position: 'absolute', right: size * -0.12, top: size * 0.32, opacity: tag, transform: `rotate(${interpolate(tag, [0, 1], [-30, -8])}deg)`, transformOrigin: 'left center'}}>
			<div style={{padding: '8px 16px', borderRadius: 8, background: '#f7e6bf', color: '#2a1a05', fontFamily: MONO, fontWeight: 700, fontSize: size * 0.085, whiteSpace: 'nowrap', boxShadow: '0 8px 20px rgba(0,0,0,0.5)'}}>🏷️ YOUR NAME</div>
		</div>
	</div>
);

const Phone: React.FC<{children?: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<div style={{width: 420, height: 760, borderRadius: 56, background: '#0d0b08', border: '10px solid #2b241a', boxShadow: `0 0 0 2px ${COLORS.gold}, 0 30px 70px rgba(0,0,0,0.6)`, position: 'relative', overflow: 'hidden', ...style}}>
		<div style={{position: 'absolute', top: 14, left: '50%', transform: 'translateX(-50%)', width: 110, height: 28, borderRadius: 14, background: '#000'}} />
		{children}
	</div>
);

const Bank: React.FC<{width: number}> = ({width}) => (
	<svg width={width} height={width * 0.8} viewBox="0 0 300 240" style={{overflow: 'visible', filter: 'drop-shadow(0 20px 40px rgba(0,0,0,0.6))'}}>
		<defs>
			<linearGradient id="v04bank" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor={COLORS.goldHi} />
				<stop offset="1" stopColor="#b0761f" />
			</linearGradient>
		</defs>
		<path d="M150 8 L290 70 H10 Z" fill="url(#v04bank)" />
		<text x="150" y="60" textAnchor="middle" fontFamily="Anton, Impact, sans-serif" fontSize="30" fill="#2a1a05" letterSpacing="4">BANK</text>
		<rect x="22" y="72" width="256" height="12" fill="url(#v04bank)" />
		{[40, 90, 196, 246].map((x) => <rect key={x} x={x} y="88" width="16" height="118" fill="url(#v04bank)" />)}
		<rect x="122" y="128" width="56" height="78" rx="4" fill="#050403" stroke={COLORS.gold} strokeWidth="3" />
		<rect x="14" y="206" width="272" height="12" fill="url(#v04bank)" />
		<rect x="2" y="220" width="296" height="14" fill="url(#v04bank)" opacity="0.85" />
	</svg>
);

const Person: React.FC<{size: number; tone?: number}> = ({size, tone = 0}) => (
	<svg width={size} height={size * 1.3} viewBox="0 0 60 78">
		<circle cx="30" cy="16" r="12" fill={tone ? '#3a2a14' : '#2a2116'} stroke={COLORS.gold} strokeWidth="2.5" />
		<path d="M8 76 V54 a22 22 0 0 1 44 0 V76 Z" fill={tone ? '#3a2a14' : '#2a2116'} stroke={COLORS.gold} strokeWidth="2.5" />
	</svg>
);

// the queue snakes away from the bank door: 5 to the right, then 9 back, then 9 out again
const SLOTS: Array<[number, number]> = [
	...[540, 650, 760, 870, 980].map((x) => [x, 745] as [number, number]),
	...[980, 870, 760, 650, 540, 430, 320, 210, 100].map((x) => [x, 865] as [number, number]),
	...[100, 210, 320, 430, 540, 650, 760, 870, 980].map((x) => [x, 985] as [number, number]),
];
const personAt = (i: number) => (i < 3 ? 25.2 + i * 0.25 : 26.95 + (i - 3) * 0.07);

const Shield: React.FC<{width: number; children?: React.ReactNode; glow?: number}> = ({width, children, glow = 0}) => (
	<div style={{position: 'relative', width, height: width * 1.15}}>
		<svg width={width} height={width * 1.15} viewBox="0 0 200 230" style={{position: 'absolute', inset: 0, overflow: 'visible', filter: `drop-shadow(0 0 ${30 * glow}px rgba(255,217,142,0.55)) drop-shadow(0 24px 40px rgba(0,0,0,0.6))`}}>
			<defs>
				<linearGradient id="v04shield" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={COLORS.goldHi} />
					<stop offset="1" stopColor="#b0761f" />
				</linearGradient>
			</defs>
			<path d="M100 6 L190 38 V112 C190 170 150 206 100 224 C50 206 10 170 10 112 V38 Z" fill="rgba(18,14,9,0.96)" stroke="url(#v04shield)" strokeWidth="8" />
			<path d="M100 22 L176 49 V112 C176 160 142 191 100 207 C58 191 24 160 24 112 V49 Z" fill="none" stroke="rgba(242,173,60,0.35)" strokeWidth="2" />
		</svg>
		<div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: width * 0.2, boxSizing: 'border-box'}}>{children}</div>
	</div>
);

export const VaultMyth: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, 5.95, 0.35);
	const cashScene = win(t, 6.1, 10.75);
	const waffle = win(t, 10.8, 19.45);
	const promise = win(t, 19.6, 23.6);
	const bank = win(t, 23.7, 30.85);
	const protect = win(t, 30.95, 38.45);
	const cta = ease(t, 42.2, 0.4);

	// hook: the wheel spins, then the door swings open on the bundle with your name
	const wheel = interpolate(t, [1.75, 2.8], [0, 300], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const doorOpen = interpolate(t, [2.95, 3.9], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	// the 97%: counts up while the squares fill
	const pct = Math.round(interpolate(t, [10.96, 11.9], [0, 97], clamp));
	const fillAt = (i: number) => 10.96 + i * (3.8 / 97);
	// the run: the cash leaves note by note
	const notesLeft = (k: number) => interpolate(t, [28.3 + k * 0.17, 28.75 + k * 0.17], [0, 1], {...clamp, easing: Easing.in(Easing.quad)});
	const shake = t > 26.9 && t < 30.9 ? 1 : 0;
	const insured = Math.round(interpolate(t, [35.76, 36.45], [0, 100000], {...clamp, easing: Easing.out(Easing.cubic)}));

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* 0:00 HOOK: the vault opens on a bundle with your name; MYTH */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, 6)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.2), transform: `scale(${interpolate(usePop(0.2, 12), [0, 1], [0.8, 1])})`}}>
					<Chip size={44}>MYTH OR FACT?</Chip>
				</div>
				<div style={{position: 'absolute', top: 390, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', opacity: ease(t, 1.7), textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
					YOUR MONEY SITS<br /><span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>IN A VAULT?</span>
				</div>
				<div style={{position: 'absolute', left: 540 - 290, top: 600, opacity: ease(t, 0.5, 0.5), transform: `translateY(${(1 - ease(t, 0.5, 0.6)) * 80}px)`}}>
					<Vault size={580} wheel={wheel} open={doorOpen}>
						<div style={{transform: `scale(${interpolate(doorOpen, [0, 1], [0.85, 1])})`}}>
							<Bundle size={300} tag={ease(t, 4.35, 0.35)} />
						</div>
					</Vault>
				</div>
				<div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center'}}>
					<Stamp text="MYTH" at={5.33} size={190} />
				</div>
			</AbsoluteFill>
			<LeoClip clip="V6" from={5.3} seconds={2.5} trim={2.0} style={{left: 560, top: 930, width: 440, height: 290}} focus="50% 6%" />

			{/* 0:06 most money isn't even cash */}
			<AbsoluteFill style={{opacity: cashScene, transform: push(t, 6.1, 10.8)}}>
				<div style={{position: 'absolute', top: 340, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 124, lineHeight: 1.02}}>
					<div style={{color: '#fff', opacity: ease(t, 6.23)}}>MOST MONEY</div>
					<div style={{color: '#fff', opacity: ease(t, 7.04)}}>ISN'T EVEN</div>
					<div style={{position: 'relative', display: 'inline-block', opacity: ease(t, 7.55)}}>
						<span style={GOLD_TEXT}>CASH</span>
						<div style={{position: 'absolute', left: -20, right: -20, top: '52%', height: 14, borderRadius: 7, background: RED, transformOrigin: 'left center', transform: `scaleX(${interpolate(t, [7.7, 8.1], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)})}) rotate(-4deg)`}} />
					</div>
				</div>
				<div style={{position: 'absolute', left: 120, right: 120, top: 860}}>
					<Flip at={8.45}>
						<Panel style={{display: 'flex', alignItems: 'center', gap: 24, padding: '24px 30px'}}>
							<div style={{fontSize: 80}}>🏛️</div>
							<div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 48, color: COLORS.text}}>Bank of England</div>
								<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 32, color: COLORS.muted, opacity: ease(t, 10.15)}}>about the money people hold in the UK 🇬🇧</div>
							</div>
						</Panel>
					</Flip>
				</div>
			</AbsoluteFill>

			{/* 0:11 97 of every 100: numbers in a bank's records; 3: notes and coins */}
			<AbsoluteFill style={{opacity: waffle, transform: push(t, 10.8, 19.5)}}>
				<div style={{position: 'absolute', top: 290, left: 90, right: 90, display: 'flex', alignItems: 'center', gap: 30}}>
					<div style={{fontFamily: DISPLAY, fontSize: 200, lineHeight: 1, ...GOLD_TEXT, minWidth: 360, textAlign: 'right'}}>{pct}%</div>
					<div>
						<div style={{fontFamily: DISPLAY, fontSize: 72, lineHeight: 1.05, color: '#fff', opacity: ease(t, 13.9)}}>BANK DEPOSITS</div>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, lineHeight: 1.2, color: COLORS.champagne, opacity: ease(t, 15.1)}}>numbers in a bank's records</div>
					</div>
				</div>
				<div style={{position: 'absolute', left: 540 - 280, top: 520, width: 560, display: 'grid', gridTemplateColumns: 'repeat(10, 1fr)', gap: 6}}>
					{Array.from({length: 100}, (_, i) => {
						const cash = i >= 97;
						const on = cash ? ease(t, 17.45 + (i - 97) * 0.12, 0.25) : ease(t, fillAt(i), 0.2);
						return (
							<div key={i} style={{position: 'relative', aspectRatio: '1', borderRadius: 8, border: '2px solid rgba(242,173,60,0.25)', boxSizing: 'border-box', overflow: 'hidden'}}>
								<div style={{position: 'absolute', inset: 0, opacity: on, transform: `scale(${interpolate(on, [0, 1], [0.4, 1])})`, borderRadius: 6, background: cash ? GREEN_CELL : `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 26, color: '#5a3b10'}}>
									{cash ? <span style={{fontSize: 28}}>💵</span> : <span style={{opacity: ease(t, 15.1 + (i % 10) * 0.04, 0.25)}}>{Math.floor(random(`d04-${i}`) * 10)}</span>}
								</div>
							</div>
						);
					})}
				</div>
				<div style={{position: 'absolute', top: 1100, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: ease(t, 17.45)}}>
					<Chip size={40} style={{borderColor: '#6fae5f', color: '#bfe8b0'}}>💵 ONLY 3% NOTES AND COINS</Chip>
				</div>
				<div style={{position: 'absolute', top: 1185, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, 11.2)}}>Source: Bank of England, Quarterly Bulletin 2014 Q1 (UK)</div>
			</AbsoluteFill>

			{/* 0:20 your balance is a promise */}
			<AbsoluteFill style={{opacity: promise, transform: push(t, 19.6, 23.7)}}>
				<div style={{position: 'absolute', left: 330, top: 300, transform: `translateY(${(1 - ease(t, 19.6, 0.5)) * 80}px)`}}>
					<Phone>
						<div style={{position: 'absolute', top: 70, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 26, color: COLORS.goldHi, letterSpacing: 2}}>MY BANK APP</div>
						<div style={{position: 'absolute', top: 150, left: 30, right: 30, padding: '26px 24px', borderRadius: 24, background: 'linear-gradient(145deg, #2a2116, #15100a)', border: '1px solid rgba(242,173,60,0.4)'}}>
							<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 24, color: COLORS.muted}}>Available balance</div>
							<div style={{fontFamily: DISPLAY, fontSize: 74, lineHeight: 1.1, ...GOLD_TEXT}}>R1,000.00</div>
						</div>
						{[0, 1, 2, 3].map((k) => (
							<div key={k} style={{position: 'absolute', top: 360 + k * 80, left: 30, right: 30, height: 56, borderRadius: 14, background: 'rgba(255,255,255,0.06)', display: 'flex', alignItems: 'center', gap: 14, padding: '0 16px'}}>
								<div style={{width: 30, height: 30, borderRadius: '50%', background: 'rgba(242,173,60,0.35)'}} />
								<div style={{height: 12, width: 140 + (k % 2) * 60, borderRadius: 6, background: 'rgba(255,255,255,0.15)'}} />
							</div>
						))}
					</Phone>
				</div>
				<div style={{position: 'absolute', top: 640, width: '100%', textAlign: 'center'}}>
					<Stamp text="A PROMISE" at={20.81} color={COLORS.gold} size={120} rotate={-8} />
				</div>
				<div style={{position: 'absolute', top: 1110, width: '100%', textAlign: 'center', opacity: ease(t, 22.1)}}>
					<Chip size={40}>🤝 PAID TO YOU WHEN YOU ASK</Chip>
				</div>
			</AbsoluteFill>

			{/* 0:24 a normal day at the bank, then everyone at once: a bank run */}
			<AbsoluteFill style={{opacity: bank, transform: push(t, 23.7, 30.9)}}>
				<div style={{position: 'absolute', left: 540 - 260, top: 330, opacity: ease(t, 23.8), transform: `translateY(${(1 - ease(t, 23.8, 0.5)) * 60}px)`}}>
					<Bank width={520} />
				</div>
				<div style={{position: 'absolute', left: 50, top: 440, width: 200, opacity: ease(t, 24.6)}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, color: COLORS.champagne, textAlign: 'center', marginBottom: 8}}>CASH ON HAND</div>
					<div style={{position: 'relative', height: 200}}>
						{Array.from({length: 6}, (_, k) => {
							const gone = notesLeft(5 - k);
							return (
								<div key={k} style={{position: 'absolute', left: 10, top: 150 - k * 22, opacity: 1 - gone, transform: `translate(${gone * 420}px, ${gone * 520}px) rotate(${gone * 40}deg)`}}>
									<Note width={180} label="R" />
								</div>
							);
						})}
						<div style={{position: 'absolute', left: 0, right: 0, top: 120, textAlign: 'center', opacity: ease(t, 29.3)}}>
							<Chip size={30} style={{borderColor: RED, color: '#ff9a63'}}>EMPTY</Chip>
						</div>
					</div>
				</div>
				{SLOTS.map(([x, y], i) => {
					const p = usePop(personAt(i), 13);
					const jig = shake * Math.sin(t * 22 + i * 1.7) * 3;
					return (
						<div key={i} style={{position: 'absolute', left: x - 42 + jig, top: y, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 40}px)`}}>
							<Person size={84} tone={i % 2} />
						</div>
					);
				})}
				<div style={{position: 'absolute', top: 1115, width: '100%', textAlign: 'center', opacity: win(t, 25.95, 26.85, 0.25)}}>
					<Chip size={40}>☀️ A NORMAL DAY</Chip>
				</div>
				<div style={{position: 'absolute', top: 1115, width: '100%', textAlign: 'center', opacity: win(t, 27.1, 29.85, 0.25)}}>
					<Chip size={40} style={{borderColor: RED, color: '#ff9a63'}}>😮 EVERYONE AT ONCE</Chip>
				</div>
				<div style={{position: 'absolute', top: 740, width: '100%', textAlign: 'center'}}>
					<Stamp text="BANK RUN" at={30.0} size={150} />
				</div>
			</AbsoluteFill>

			{/* 0:31 why banks are regulated, and South Africa's deposit insurance */}
			<AbsoluteFill style={{opacity: protect, transform: push(t, 31.0, 38.5)}}>
				<div style={{position: 'absolute', top: 290, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
					<Flip at={31.1}>
						<Chip size={44}>⚖️ BANKS ARE REGULATED</Chip>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 400, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.text, opacity: ease(t, 32.99)}}>🇿🇦 South Africa insures deposits</div>
				<div style={{position: 'absolute', left: 540 - 270, top: 490, opacity: ease(t, 33.9, 0.4), transform: `scale(${interpolate(usePop(33.9, 13), [0, 1], [0.75, 1])})`}}>
					<Shield width={540} glow={ease(t, 35.76, 0.6)}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.champagne, letterSpacing: 3}}>DEPOSIT INSURANCE</div>
						<div style={{marginTop: 30, fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.muted, opacity: ease(t, 35.25)}}>UP TO</div>
						<div style={{fontFamily: DISPLAY, fontSize: 128, lineHeight: 1.05, ...GOLD_TEXT, opacity: ease(t, 35.76, 0.2)}}>R{insured.toLocaleString('en-US')}</div>
						<div style={{marginTop: 18, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12}}>
							<div style={{fontFamily: DISPLAY, fontSize: 56, color: '#fff', opacity: ease(t, 37.13), transform: `scale(${interpolate(usePop(37.13, 12), [0, 1], [0.7, 1])})`}}>PER PERSON</div>
							<div style={{fontFamily: DISPLAY, fontSize: 56, color: '#fff', opacity: ease(t, 37.98), transform: `scale(${interpolate(usePop(37.98, 12), [0, 1], [0.7, 1])})`}}>PER BANK</div>
						</div>
					</Shield>
				</div>
				<div style={{position: 'absolute', top: 1140, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, 34.4)}}>CODI (SARB), at every registered bank, since April 2024</div>
			</AbsoluteFill>

			{/* 0:39 the question: Leo thinks it over */}
			<LeoClip clip="V5" from={38.6} seconds={3.3} trim={0.4} style={{left: 160, top: 320, width: 760, height: 1330}} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: win(t, 38.75, 41.75)}}>
				<Chip size={36} style={{background: 'rgba(5,4,3,0.88)'}}>DID YOU THINK IT WAS IN A VAULT? 💬</Chip>
				<div style={{marginTop: 14, display: 'flex', justifyContent: 'center', gap: 18, opacity: ease(t, 40.5)}}>
					{['🙋 YES', '🙅 NO'].map((v) => (
						<span key={v} style={{display: 'inline-block', padding: '8px 26px', borderRadius: 14, background: 'rgba(5,4,3,0.88)', border: `2px solid ${COLORS.gold}`, fontFamily: BODY, fontWeight: 800, fontSize: 34, color: COLORS.text}}>{v}</span>
					))}
				</div>
			</div>

			{/* 0:42 call to action and sign-off, then MTG's theme line */}
			<AbsoluteFill style={{opacity: cta}}>
				<div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: ease(t, 45.7, 0.4)}}>
					<PhotoCard size={330} />
					<div style={{fontFamily: DISPLAY, fontSize: 90, lineHeight: 1, ...GOLD_TEXT}}>MTG</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text}}>Your Digital Architect</div>
				</div>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, 42.35), fadeOut(t, 45.6, 0.3))}}>
					<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.05, color: '#fff'}}>LEARN HOW MONEY<br /><span style={GOLD_TEXT}>REALLY WORKS</span></div>
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, bottom: 720, display: 'flex', justifyContent: 'center', opacity: fadeOut(t, 48.2, 0.4)}}>
					<SiteCard t={t} at={42.6} vertical />
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, top: 1000, textAlign: 'center', opacity: ease(t, 48.33), transform: `scale(${interpolate(usePop(48.33, 12), [0, 1], [0.7, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 92, ...GOLD_TEXT}}>Let's Get This Crypto!</span> <span style={{fontFamily: DISPLAY, fontSize: 92}}>💪</span>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi, marginTop: 14}}>mtgtribe.com</div>
				</div>
			</AbsoluteFill>

			{/* sound, fitted to this story and soft; the theme plays only its last line at the end */}
			<Cues
				list={[
					[0.1, 'air', 0.35], [0.2, 'reveal', 0.4], [1.75, 'vault', 0.55], [4.35, 'pluck3', 0.3], [5.33, 'thud', 0.5],
					[6.2, 'air', 0.3], [7.7, 'drop', 0.4], [8.45, 'pluck1', 0.35],
					[10.9, 'count', 0.22], [11.0, 'swell', 0.3], [13.9, 'pluck2', 0.35], [15.1, 'tick', 0.25], [17.45, 'coin', 0.4],
					[19.6, 'air', 0.3], [20.81, 'reveal', 0.4], [22.1, 'pluck3', 0.3],
					[23.8, 'air', 0.3], [25.2, 'tick', 0.2], [26.0, 'chime', 0.35],
					[26.9, 'murmur', 0.4], [28.3, 'murmur', 0.35], [28.4, 'melt', 0.35], [30.0, 'thud', 0.5],
					[31.1, 'air', 0.3], [31.84, 'pluck1', 0.35], [33.9, 'glow', 0.4], [35.76, 'reveal', 0.45], [37.13, 'pluck2', 0.35], [37.98, 'pluck3', 0.35],
					[38.7, 'air', 0.3], [38.9, 'clock', 0.18], [40.5, 'pluck2', 0.3],
					[42.2, 'glow', 0.35], [45.7, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/04/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover04: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 38%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={46}>MYTH OR FACT?</Chip>
		</div>
		<div style={{position: 'absolute', top: 370, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 116, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
			YOUR MONEY IS<br /><span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>IN A VAULT</span>
		</div>
		<div style={{position: 'absolute', left: 50, top: 650}}>
			<Vault size={560} wheel={40} open={0.9}>
				<Bundle size={290} tag={1} />
			</Vault>
		</div>
		<div style={{position: 'absolute', left: 50, width: 560, top: 840, textAlign: 'center'}}>
			<span style={{display: 'inline-block', transform: 'rotate(-12deg)', border: `10px solid ${RED}`, color: '#ff8a4c', fontFamily: DISPLAY, fontSize: 170, lineHeight: 1.15, padding: '0 40px', borderRadius: 16, background: 'rgba(5,4,3,0.8)', boxShadow: '0 20px 50px rgba(0,0,0,0.6)'}}>MYTH</span>
		</div>
		<div style={{position: 'absolute', top: 690, left: 640, width: 390, height: 500, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7)'}}>
			<Img src={staticFile('videos/01/leo/V6-laugh.png')} style={{width: 390, height: 682, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1260, left: 70, right: 70, display: 'flex', alignItems: 'center', gap: 36}}>
			<PhotoCard size={250} />
			<div style={{fontFamily: DISPLAY, fontSize: 82, lineHeight: 1.02, color: '#fff'}}>
				<span style={{...GOLD_TEXT}}>97%</span> OF MONEY<br />ISN'T CASH
				<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, lineHeight: 1.3, color: COLORS.muted, marginTop: 8}}>UK, Bank of England</div>
			</div>
		</div>
		<div style={{position: 'absolute', top: 1590, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.goldHi}}>mtgtribe.com</div>
	</AbsoluteFill>
);

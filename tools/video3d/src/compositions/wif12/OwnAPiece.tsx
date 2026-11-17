import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/12/captions.json';
import C from '../../../public/videos/12/cues.json';
import timeline from '../../../public/videos/12/timeline.json';
import W from '../../../public/videos/12/words.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Block3D, Notepad3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 12 (17 Nov 2026, daily video): What If You Owned a Piece of the Companies You Use Every Day? Stocks for
// beginners: a share, a dividend, an index fund, prices move, and one first step (look up the companies behind your
// brands). Education only: no tips, no predictions, no recommendation. Script and research:
// tools/videos/12-what-if-you-owned-a-piece/. Every time is a named cue from the voice's own word timings.
// Facts on screen: 2.2 billion servings a day (The Coca-Cola Company); its 64th consecutive annual dividend increase
// (company press release, 19 February 2026); the S&P 500, 500 leading U.S. companies (S&P Dow Jones Indices).
// No logos and no brand colours: the bottle is an original gold drawing.

export const WIF12_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const WIF12_FRAMES = Math.ceil((timeline.total + TAIL) * WIF12_FPS);
// MTG's approved slogan (16 November 2026): the start of each of its four words
const SLOGAN = W.words.slice(-4).map((w) => w.start);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};
const inOut = {...clamp, easing: Easing.inOut(Easing.cubic)};

/** An original drink bottle: amber glass, a gold cap, a blank gold label and rising bubbles. */
const Bottle: React.FC<{h: number; t: number; label?: string}> = ({h, t, label = 'DRINK'}) => (
	<svg width={h * 0.42} height={h} viewBox="0 0 120 286" style={{filter: 'drop-shadow(0 22px 30px rgba(0,0,0,0.6))'}}>
		<defs>
			<linearGradient id="b12glass" x1="0" y1="0" x2="1" y2="0">
				<stop offset="0" stopColor="#5a3510" />
				<stop offset="0.35" stopColor="#a8661c" />
				<stop offset="0.6" stopColor="#7a4714" />
				<stop offset="1" stopColor="#3d240b" />
			</linearGradient>
			<clipPath id="b12clip">
				<path d="M44 20 L76 20 L76 60 C76 80 100 92 100 120 L100 266 C100 276 92 282 82 282 L38 282 C28 282 20 276 20 266 L20 120 C20 92 44 80 44 60 Z" />
			</clipPath>
		</defs>
		<rect x="40" y="2" width="40" height="22" rx="5" fill={COLORS.gold} />
		<path d="M44 20 L76 20 L76 60 C76 80 100 92 100 120 L100 266 C100 276 92 282 82 282 L38 282 C28 282 20 276 20 266 L20 120 C20 92 44 80 44 60 Z" fill="url(#b12glass)" stroke={COLORS.goldHi} strokeWidth="2" />
		<g clipPath="url(#b12clip)">
			{Array.from({length: 12}).map((_, i) => {
				const y = 280 - (((t * 60 + i * 41) % 200) + 20);
				return <circle key={i} cx={34 + ((i * 23) % 54)} cy={y} r={2 + (i % 3)} fill="#fff" opacity={0.28} />;
			})}
			<path d="M28 100 L40 100 L32 270 L24 270 Z" fill="#fff" opacity="0.12" />
		</g>
		<rect x="22" y="150" width="76" height="62" rx="6" fill={COLORS.gold} />
		<text x="60" y="188" textAnchor="middle" fontFamily="sans-serif" fontWeight="900" fontSize="17" fill="#3a2508">{label}</text>
	</svg>
);

/** The whole business as a gold pie; one thin slice lifts out: one share. */
const Pie: React.FC<{size: number; lift: number; label?: string}> = ({size, lift, label}) => {
	const r = 46;
	const a = (16 / 360) * Math.PI * 2; // drawn far bigger than a real share so it can be seen
	const p = (ang: number, rr = r) => `${50 + rr * Math.sin(ang)} ${50 - rr * Math.cos(ang)}`;
	const dx = Math.sin(a / 2) * 16 * lift;
	const dy = -Math.cos(a / 2) * 16 * lift;
	return (
		<svg width={size} height={size} viewBox="-6 -10 112 112" style={{filter: 'drop-shadow(0 24px 30px rgba(0,0,0,0.55))'}}>
			<defs>
				<radialGradient id="p12g" cx="0.4" cy="0.35" r="0.7">
					<stop offset="0" stopColor={COLORS.goldHi} />
					<stop offset="1" stopColor="#a8691f" />
				</radialGradient>
			</defs>
			<path d={`M50 50 L${p(a)} A${r} ${r} 0 1 1 ${p(0)} Z`} fill="url(#p12g)" stroke="#3a2508" strokeWidth="0.8" />
			{Array.from({length: 18}).map((_, i) => (
				<line key={i} x1="50" y1="50" x2={50 + r * Math.sin(a + (i + 1) * ((Math.PI * 2 - a) / 19))} y2={50 - r * Math.cos(a + (i + 1) * ((Math.PI * 2 - a) / 19))} stroke="rgba(58,37,8,0.25)" strokeWidth="0.5" />
			))}
			{label && <text x="50" y="60" textAnchor="middle" fontFamily="sans-serif" fontWeight="900" fontSize="8" fill="#3a2508">{label}</text>}
			<g transform={`translate(${dx} ${dy})`}>
				<path d={`M50 50 L${p(0)} A${r} ${r} 0 0 1 ${p(a)} Z`} fill="#fff1c4" stroke={COLORS.gold} strokeWidth="0.8" style={{filter: `drop-shadow(0 0 ${3 * lift}px rgba(255,220,140,0.9))`}} />
			</g>
		</svg>
	);
};

/** A wicker-style gold basket, drawn in code. */
const Basket: React.FC<{w: number}> = ({w}) => (
	<svg width={w} height={w * 0.55} viewBox="0 0 200 110" style={{filter: 'drop-shadow(0 22px 28px rgba(0,0,0,0.6))'}}>
		<path d="M8 20 L192 20 L172 104 L28 104 Z" fill="#6b4512" stroke={COLORS.gold} strokeWidth="3" />
		{[0, 1, 2, 3].map((i) => (
			<path key={i} d={`M${12 + i * 1.5} ${36 + i * 18} L${188 - i * 1.5} ${36 + i * 18}`} stroke="rgba(242,173,60,0.55)" strokeWidth="5" />
		))}
		{Array.from({length: 9}).map((_, i) => (
			<line key={i} x1={20 + i * 20} y1="22" x2={34 + i * 16.5} y2="102" stroke="rgba(30,18,4,0.45)" strokeWidth="2" />
		))}
		<rect x="2" y="12" width="196" height="12" rx="6" fill={COLORS.gold} />
	</svg>
);

export const OwnAPiece: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.that - 0.3, 0.3);
	const share = win(t, C.that - 0.15, C.some - 0.3, 0.3);
	const div = win(t, C.some - 0.15, C.cant - 0.3, 0.3);
	const index = win(t, C.cant - 0.15, C.prices - 0.3, 0.3);
	const honest = win(t, C.prices - 0.15, C.start - 0.3, 0.3);
	const tip = win(t, C.start - 0.15, C.which - 0.3, 0.3);
	const ask = win(t, C.which - 0.1, C.send - 0.2, 0.25);
	const shareP = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const servings = interpolate(t, [C.served, C.billion + 0.3], [0, 2.2], outCubic);
	const lift = interpolate(t, [C.tiny - 0.1, C.tiny + 0.6], [0, 1], outCubic);
	const lift2 = interpolate(t, [C.one - 0.1, C.one + 0.6], [0, 1], outCubic);
	const years = Math.round(interpolate(t, [C.raised, C.row + 0.2], [0, 64], outCubic));
	const flow = interpolate(t, [C.profits - 0.1, C.owners + 0.6], [0, 1], clamp);
	const fill = interpolate(t, [C.holds - 0.1, C.basket + 0.2], [0, 1], inOut);

	// the price line: it wanders up and down, drawn left to right while he says it
	const chartW = 900;
	const pts = Array.from({length: 61}).map((_, i) => {
		const x = (i / 60) * chartW;
		const y = 150 - 30 * Math.sin(i * 0.33) - 22 * Math.sin(i * 0.9 + 1) - 14 * Math.sin(i * 2.1) - i * 1.1;
		return [x, y] as const;
	});
	const drawn = interpolate(t, [C.prices - 0.1, C.noPromises], [0, 1], clamp);
	const path = pts.slice(0, Math.max(2, Math.round(drawn * 61))).map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: what if every time you bought a drink, you owned a tiny piece of the company? 2.2 billion a day */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.that)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={40}>WHAT IF? 🤔</Chip>
				</div>
				<div style={{position: 'absolute', left: 120, top: 390, opacity: ease(t, C.bought - 0.25), transform: `translateY(${(1 - ease(t, C.bought - 0.25, 0.5)) * 60}px) rotate(${interpolate(t, [C.bought - 0.25, C.bought + 0.5], [-14, -6], outCubic)}deg)`}}>
					<Bottle h={480} t={t} />
				</div>
				<div style={{position: 'absolute', left: 360, top: 560, fontFamily: DISPLAY, fontSize: 120, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, C.owned - 0.1)}}>=</div>
				<div style={{position: 'absolute', left: 470, top: 410, opacity: ease(t, C.owned), transform: `scale(${interpolate(usePop(C.owned, 12), [0, 1], [0.6, 1])})`}}>
					<Pie size={480} lift={lift} label="THE COMPANY" />
				</div>
				<div style={{position: 'absolute', left: 760, top: 400, opacity: ease(t, C.tiny + 0.3)}}>
					<HintPill icon="👆" text="you" size={36} />
				</div>
				<div style={{position: 'absolute', top: 920, width: '100%', textAlign: 'center', opacity: ease(t, C.its - 0.1)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT}}>{servings.toFixed(1)} BILLION</div>
					<div style={{fontFamily: DISPLAY, fontSize: 56, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.day - 0.2)}}>OF ITS DRINKS SERVED, EVERY DAY</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 25, color: COLORS.muted, marginTop: 8, opacity: ease(t, C.day)}}>Source: The Coca-Cola Company, 2026</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.billion + 0.25} seconds={Math.min(1.5, C.that - C.billion - 0.4)} style={{left: 60, top: 600, width: 340, height: 260}} accent="wow" sound={null} />

			{/* A SHARE: one share makes you part owner of the whole business */}
			<AbsoluteFill style={{opacity: share, transform: push(t, C.that, C.some)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>THAT TINY PIECE IS...</Chip>
				</div>
				<div style={{position: 'absolute', top: 384, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, C.share - 0.1), transform: `scale(${interpolate(usePop(C.share - 0.1, 11), [0, 1], [1.4, 1])})`}}>A SHARE</div>
				<div style={{position: 'absolute', left: 40, top: 540, opacity: ease(t, C.one - 0.2)}}>
					<Pie size={440} lift={lift2} label="THE BUSINESS" />
				</div>
				<div style={{position: 'absolute', left: 500, right: 40, top: 570}}>
					<Flip at={C.partOwner - 0.3}>
						<Panel style={{padding: '22px 24px', background: 'linear-gradient(160deg, #f8edd2, #e9d8ad)', border: `4px double ${COLORS.gold}`, position: 'relative'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 3, color: '#7a5418', textAlign: 'center'}}>SHARE CERTIFICATE</div>
							<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 32, color: '#3a2508', marginTop: 14, lineHeight: 1.3, textAlign: 'center'}}>This shows that <b>YOU</b> own<br />1 share of the business</div>
							<div style={{marginTop: 16, height: 2, background: 'rgba(122,84,24,0.35)'}} />
							<div style={{height: 120}} />
							<div style={{position: 'absolute', left: '50%', marginLeft: -110, bottom: 22, width: 220, padding: '8px 0', textAlign: 'center', border: '5px solid #b0402a', borderRadius: 12, color: '#b0402a', fontFamily: DISPLAY, fontSize: 44, lineHeight: 1, opacity: ease(t, C.partOwner + 0.1, 0.12), transform: `rotate(-10deg) scale(${interpolate(t, [C.partOwner + 0.1, C.partOwner + 0.3], [1.8, 1], outCubic)})`}}>PART<br />OWNER</div>
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 1040, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 60, lineHeight: 1, color: '#fff', opacity: ease(t, C.whole - 0.1)}}>
					OF THE <span style={GOLD_TEXT}>WHOLE BUSINESS</span>
				</div>
			</AbsoluteFill>

			{/* A DIVIDEND: some companies share profits with their owners; Coca-Cola raised it 64 years in a row */}
			<AbsoluteFill style={{opacity: div, transform: push(t, C.some, C.cant)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>{t < C.dividend - 0.1 ? 'PROFITS, SHARED' : "THAT'S A DIVIDEND 💰"}</Chip>
				</div>
				<div style={{position: 'absolute', left: 80, top: 420, opacity: ease(t, C.some)}}>
					<Block3D w={260} h={200} d={160} rotX={-14} rotY={-24} label="🏭" sub="the company" />
				</div>
				<div style={{position: 'absolute', right: 50, top: 440, display: 'flex', gap: 6, opacity: ease(t, C.owners - 0.3)}}>
					{[0, 1, 2].map((i) => (
						<div key={i} style={{width: 110, textAlign: 'center'}}>
							<div style={{fontSize: 100, lineHeight: 1}}>🧑</div>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 20, color: COLORS.champagne}}>OWNER</div>
						</div>
					))}
				</div>
				{Array.from({length: 6}).map((_, i) => {
					const k = Math.max(0, Math.min(1, flow * 1.6 - i * 0.12));
					return <div key={i} style={{position: 'absolute', left: 360 + k * 340, top: 520 - Math.sin(k * Math.PI) * 90 + (i % 3) * 14, width: 46, height: 46, borderRadius: '50%', background: GOLD_FILL, border: '2px solid #fff1c4', opacity: k > 0 && k < 1 ? 1 : 0, boxShadow: '0 0 14px rgba(242,173,60,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 26, color: '#2a1a05'}}>$</div>;
				})}
				<div style={{position: 'absolute', top: 700, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 72, lineHeight: 1, color: '#fff', opacity: win(t, C.profits, C.coca - 0.4, 0.3)}}>PROFITS <span style={GOLD_TEXT}>→ OWNERS</span></div>
				<div style={{position: 'absolute', top: 700, width: '100%', textAlign: 'center', opacity: ease(t, C.coca - 0.2)}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: 3, color: COLORS.goldHi}}>COCA-COLA RAISED ITS DIVIDEND</div>
					<div style={{fontFamily: DISPLAY, fontSize: 130, lineHeight: 1.02, ...GOLD_TEXT}}>{years} YEARS IN A ROW</div>
				</div>
				<div style={{position: 'absolute', left: 90, right: 90, top: 880, height: 160, display: 'flex', alignItems: 'flex-end', gap: 3, opacity: ease(t, C.raised - 0.2)}}>
					{Array.from({length: 64}).map((_, i) => (
						<div key={i} style={{flex: 1, height: `${(8 + (i / 63) ** 1.6 * 92) * (i < years ? 1 : 0)}%`, borderRadius: 2, background: i === 63 ? '#fff1c4' : GOLD_FILL, boxShadow: i === 63 ? '0 0 16px rgba(255,220,140,0.9)' : 'none'}} />
					))}
				</div>
				<div style={{position: 'absolute', top: 1062, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 25, color: COLORS.muted, opacity: ease(t, C.row)}}>Company press release, 19 Feb 2026. An example, not a recommendation.</div>
			</AbsoluteFill>
			<LeoMoment m="mindblown" at={C.row + 0.1} seconds={Math.min(1.9, C.cant - C.row - 0.25)} style={{left: 330, top: 380, width: 330, height: 270}} focus="50% 4%" accent="wow" />

			{/* AN INDEX FUND: a little of hundreds at once; the S&P 500, 500 big U.S. companies in one basket (CSS 3D) */}
			<AbsoluteFill style={{opacity: index, transform: push(t, C.cant, C.prices)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>{t < C.index - 0.1 ? "CAN'T PICK ONE? 🤷" : 'AN INDEX FUND 🧺'}</Chip>
				</div>
				<div style={{position: 'absolute', top: 380, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 76, lineHeight: 1.02, color: '#fff', opacity: ease(t, C.holds - 0.1)}}>
					A LITTLE OF <span style={GOLD_TEXT}>HUNDREDS</span><br />AT ONCE
				</div>
				{/* hundreds of tiny companies falling into one basket */}
				<div style={{position: 'absolute', left: 140, top: 600, width: 800, height: 260, overflow: 'visible'}}>
					{Array.from({length: 60}).map((_, i) => {
						const col = i % 12;
						const row = Math.floor(i / 12);
						const k = Math.max(0, Math.min(1, fill * 1.4 - (i / 60) * 0.4));
						const x = 40 + col * 60;
						const y0 = row * 30;
						const y1 = 180 - row * 20;
						return <div key={i} style={{position: 'absolute', left: x + (1 - k) * Math.sin(i) * 20 + k * (400 - x) * 0.35, top: y0 + (y1 - y0) * k, width: 34, height: 34, borderRadius: 6, background: i % 5 === 0 ? '#fff1c4' : GOLD_FILL, border: '1.5px solid rgba(58,37,8,0.5)', opacity: ease(t, C.holds - 0.1 + (i / 60) * 0.5, 0.2), transform: `rotate(${(1 - k) * (i * 37 % 60 - 30)}deg)`}} />;
					})}
				</div>
				<div style={{position: 'absolute', left: 290, top: 740, opacity: ease(t, C.hundreds - 0.3)}}>
					<Basket w={500} />
				</div>
				<div style={{position: 'absolute', left: 290, width: 500, top: 826, textAlign: 'center', opacity: ease(t, C.sp - 0.1)}}><span style={{display: 'inline-block', padding: '6px 26px', borderRadius: 999, background: 'rgba(10,8,6,0.92)', border: `3px solid ${COLORS.goldHi}`, fontFamily: DISPLAY, fontSize: 60, lineHeight: 1, ...GOLD_TEXT}}>S&amp;P 500</span></div>
				<div style={{position: 'absolute', top: 1030, width: '100%', textAlign: 'center', opacity: ease(t, C.puts)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 64, lineHeight: 1, color: '#fff'}}><span style={GOLD_TEXT}>500</span> BIG U.S. COMPANIES, <span style={GOLD_TEXT}>ONE BASKET</span></div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 25, color: COLORS.muted, marginTop: 10, opacity: ease(t, C.big)}}>A stock market index by S&amp;P Dow Jones Indices</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.basket - 0.1} seconds={Math.min(1.15, C.prices - C.basket - 0.15)} style={{left: 806, top: 720, width: 240, height: 230}} accent="aha" focus="50% 6%" />

			{/* AN HONEST NOTE: prices go up and down, no promises */}
			<AbsoluteFill style={{opacity: honest, transform: push(t, C.prices, C.start)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>AN HONEST NOTE 🤝</Chip>
				</div>
				<div style={{position: 'absolute', top: 384, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.02, color: '#fff', opacity: ease(t, C.prices - 0.05)}}>
					PRICES GO <span style={GOLD_TEXT}>UP</span> AND <span style={{color: COLORS.champagne}}>DOWN</span>
				</div>
				<div style={{position: 'absolute', left: 90, top: 540, width: chartW, height: 300}}>
					<svg width={chartW} height={300} viewBox={`0 -20 ${chartW} 300`}>
						{[0, 1, 2, 3].map((i) => <line key={i} x1="0" x2={chartW} y1={i * 70} y2={i * 70} stroke="rgba(242,173,60,0.15)" strokeWidth="2" />)}
						<path d={path} fill="none" stroke={COLORS.goldHi} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" style={{filter: 'drop-shadow(0 0 10px rgba(242,173,60,0.6))'}} />
					</svg>
				</div>
				<div style={{position: 'absolute', top: 900, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 80, lineHeight: 1, color: COLORS.champagne, opacity: ease(t, C.noPromises - 0.1)}}>NO PROMISES</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.noPromises + 0.15} seconds={Math.min(1.35, C.start - C.noPromises - 0.3)} style={{left: 340, top: 990, width: 400, height: 230}} accent="relief" focus="50% 8%" />

			{/* THE FIRST STEP: look up the companies behind the brands you use every day (the notepad moment) */}
			<AbsoluteFill style={{opacity: tip, transform: push(t, C.start, C.which)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>💡 START HERE</Chip>
				</div>
				<div style={{position: 'absolute', top: 386, left: 40, right: 40, textAlign: 'center', fontFamily: DISPLAY, fontSize: 72, lineHeight: 1.04, color: '#fff', opacity: ease(t, C.lookUp - 0.2)}}>
					WHO'S BEHIND THE BRANDS<br /><span style={GOLD_TEXT}>YOU USE EVERY DAY?</span>
				</div>
				<div style={{position: 'absolute', left: 150, top: 590, opacity: ease(t, C.behind - 0.3), transform: `translateY(${(1 - ease(t, C.behind - 0.3, 0.5)) * 50}px)`}}>
					<Notepad3D w={780} t={t} title="MY EVERYDAY BRANDS" lines={[['🥤 My drink: who makes it?', C.behind], ['📱 My phone: who makes it?', C.everyDay - 0.3], ['🛒 My shop: who owns it?', C.investors - 0.5]]} />
				</div>
				<div style={{position: 'absolute', top: 1096, width: '100%', textAlign: 'center', display: 'flex', justifyContent: 'center', gap: 14}}>
					<HintPill icon="🔖" text="Save this" size={34} t={t} at={C.investors + 0.2} />
					<HintPill icon="📚" text="Education, not advice" size={34} t={t} at={C.investors + 0.4} />
				</div>
			</AbsoluteFill>

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.which} seconds={Math.min(4.2, C.send - C.which - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={38} style={{background: 'rgba(5,4,3,0.9)'}}>WHICH COMPANY WOULD YOU OWN? 🤔</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: shareP}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.friend)}}>who drinks the most Coke 🥤</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'ai', 'streams', 'tutorials', 'tribe']} sloganWords={SLOGAN} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [C.bought - 0.25, 'fizz', 0.5], [C.owned, 'pluck2', 0.3], [C.tiny - 0.1, 'link', 0.34], [C.served, 'count', 0.22], [C.billion + 0.3, 'reveal', 0.3],
					[C.that - 0.15, 'air', 0.26], [C.share - 0.1, 'pluck3', 0.32], [C.one - 0.1, 'link', 0.32], [C.partOwner - 0.3, 'paper', 0.32], [C.partOwner + 0.1, 'stamp', 0.5], [C.whole - 0.1, 'glow', 0.26],
					[C.some - 0.15, 'air', 0.26], [C.profits - 0.1, 'coinrain', 0.24], [C.dividend - 0.1, 'chime', 0.3], [C.raised, 'count', 0.22], [C.row + 0.15, 'reveal', 0.3],
					[C.cant - 0.15, 'pluck1', 0.28], [C.holds - 0.1, 'flutter', 0.22], [C.hundreds - 0.3, 'slide', 0.28], [C.sp - 0.1, 'pluck3', 0.3], [C.basket - 0.2, 'thud', 0.3],
					[C.prices - 0.1, 'swell', 0.24], [C.noPromises - 0.1, 'pluck1', 0.26],
					[C.start - 0.15, 'chime', 0.28], [C.behind - 0.05, 'scribble', 0.4], [C.everyDay - 0.35, 'scribble', 0.36], [C.investors - 0.55, 'scribble', 0.36], [C.investors + 0.2, 'pluck4', 0.26],
					[C.which, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/12/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover12: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>WHAT IF? 🤔</Chip>
		</div>
		<div style={{position: 'absolute', top: 366, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 132, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>YOU OWNED A PIECE</div>
		<div style={{position: 'absolute', top: 504, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.0, ...GOLD_TEXT}}>OF THE BRANDS YOU USE</div>
		<div style={{position: 'absolute', left: 70, top: 680}}>
			<Bottle h={460} t={2} />
		</div>
		<div style={{position: 'absolute', left: 250, top: 760}}>
			<Pie size={360} lift={1} />
		</div>
		<div style={{position: 'absolute', top: 690, left: 620, width: 400, height: 460, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V3-aha.png')} style={{width: 400, height: 700, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1222, width: '100%', display: 'flex', justifyContent: 'center', gap: 18}}>
			{['📜 SHARES', '💰 DIVIDENDS', '🧺 INDEX FUNDS'].map((x) => (
				<div key={x} style={{padding: '12px 22px', borderRadius: 999, border: `2.5px solid ${COLORS.gold}`, background: 'rgba(18,14,9,0.95)', fontFamily: DISPLAY, fontSize: 46, lineHeight: 1, color: '#fff'}}>{x}</div>
			))}
		</div>
		<div style={{position: 'absolute', top: 1340, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 38, color: COLORS.champagne}}>Stocks, explained in one minute</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

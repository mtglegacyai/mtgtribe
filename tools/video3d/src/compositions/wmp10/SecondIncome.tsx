import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/10/captions.json';
import C from '../../../public/videos/10/cues.json';
import timeline from '../../../public/videos/10/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Block3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 10 (15 Nov 2026, daily video): Why Most People Never Start a Second Income (and the Small First Step). For
// full-time employees: warm, respectful of the job, no income promises. Three hurdles from a survey, one reframe (the
// first step looks too big), one small step (20 minutes a day on one skill = about 120 hours a year = 15 working days).
// Script and research: tools/videos/10-why-most-people-never-start/. Every time is a named cue from the voice's own
// word timings (public/videos/10/cues.json).
// Facts on screen: 27% of U.S. adults have a side hustle (Bankrate, June 2025); the hurdles and their shares
// (GOBankingRates survey on starting a business, 2023); 20 min x 365 = 121.7 hours = 15.2 eight-hour days.

export const WMP10_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const WMP10_FRAMES = Math.ceil((timeline.total + TAIL) * WMP10_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};
const inOut = {...clamp, easing: Easing.inOut(Easing.cubic)};

/** A simple person (an original drawing): gold for "has a second income", dim for "not yet". */
const Person: React.FC<{size: number; gold?: number}> = ({size, gold = 0}) => (
	<svg width={size} height={size * 1.25} viewBox="0 0 100 125" style={{filter: `drop-shadow(0 0 ${24 * gold}px rgba(242,173,60,${0.8 * gold}))`}}>
		<defs>
			<linearGradient id="p10gold" x1="0" y1="0" x2="1" y2="1">
				<stop offset="0" stopColor={COLORS.goldHi} />
				<stop offset="1" stopColor="#b0761f" />
			</linearGradient>
		</defs>
		<g fill="#4a4034" opacity={1 - gold}>
			<circle cx="50" cy="26" r="20" />
			<path d="M14 120 C14 78 30 56 50 56 C70 56 86 78 86 120 Z" />
		</g>
		<g fill="url(#p10gold)" opacity={gold}>
			<circle cx="50" cy="26" r="20" />
			<path d="M14 120 C14 78 30 56 50 56 C70 56 86 78 86 120 Z" />
		</g>
	</svg>
);

const Badge: React.FC<{label: string; size: number}> = ({label, size}) => (
	<div style={{width: size, height: size, flexShrink: 0, borderRadius: '50%', background: GOLD_FILL, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: size * 0.62, lineHeight: 1, color: '#2a1a05', boxShadow: '0 12px 30px rgba(0,0,0,0.5)'}}>{label}</div>
);

const HURDLES: Array<[icon: string, said: string, big: string]> = [
	['💰', '44% said', 'NOT ENOUGH MONEY'],
	['💡', '16% said', "DON'T KNOW WHAT TO START"],
	['⏰', '13% said', 'NOT ENOUGH TIME'],
];

/** A clock face with a gold wedge for the first `minutes` of the hour. */
const Dial: React.FC<{size: number; minutes: number}> = ({size, minutes}) => {
	const r = 44;
	const a = (Math.min(59.9, minutes) / 60) * Math.PI * 2;
	const x = 50 + r * Math.sin(a);
	const y = 50 - r * Math.cos(a);
	return (
		<svg width={size} height={size} viewBox="0 0 100 100" style={{filter: 'drop-shadow(0 16px 26px rgba(0,0,0,0.55))'}}>
			<circle cx="50" cy="50" r="48" fill="#17110a" stroke={COLORS.gold} strokeWidth="2.5" />
			{minutes > 0.05 && <path d={`M50 50 L50 ${50 - r} A${r} ${r} 0 ${a > Math.PI ? 1 : 0} 1 ${x} ${y} Z`} fill={COLORS.gold} opacity="0.92" />}
			{Array.from({length: 12}).map((_, i) => (
				<line key={i} x1="50" y1="5" x2="50" y2={i % 3 === 0 ? 12 : 9} stroke={COLORS.champagne} strokeWidth={i % 3 === 0 ? 2 : 1.2} transform={`rotate(${i * 30} 50 50)`} />
			))}
			<line x1="50" y1="50" x2={50 + 40 * Math.sin(a)} y2={50 - 40 * Math.cos(a)} stroke="#fff" strokeWidth="2.6" strokeLinecap="round" />
			<circle cx="50" cy="50" r="3.6" fill="#fff" />
		</svg>
	);
};

export const SecondIncome: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.survey - 0.3, 0.3);
	const hurdles = win(t, C.survey - 0.15, C.but - 0.3, 0.3);
	const reframe = win(t, C.but - 0.15, C.heres - 0.1, 0.3);
	const smallStep = win(t, C.heres + 0.1, C.thats - 0.3, 0.3);
	const math = win(t, C.thats - 0.15, C.wont - 0.3, 0.3);
	const honest = win(t, C.wont - 0.15, C.which - 0.3, 0.3);
	const ask = win(t, C.which - 0.1, C.send - 0.2, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	// the big first step shrinks into a small one, and the person steps onto it
	const shrink = interpolate(t, [C.small - 0.1, C.small + 0.4], [0, 1], inOut);
	const bigH = 440;
	const smallH = 96;
	const stepH = bigH + (smallH - bigH) * shrink;
	const hop = interpolate(t, [C.small + 0.3, C.small + 0.75], [0, 1], inOut);
	const minutes = interpolate(t, [C.twenty, C.twenty + 0.9], [0, 20], outCubic);
	const hoursN = Math.round(interpolate(t, [C.hours, C.year], [0, 120], outCubic));
	// climbing the small steps in the honest note: one step at "gets you started", then two more
	const climbs = [C.gets, C.starting, C.skip - 0.3];
	const climb = climbs.reduce((s, at) => s + interpolate(t, [at, at + 0.45], [0, 1], inOut), 0);
	const STAIR_W = 150;
	const STAIR_H = 62;
	const STAIR_X = 240;
	const frac = climb - Math.floor(climb);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: only about one in four adults has a second income; you're not alone; so what stops us? */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.survey)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={38}>WHY MOST PEOPLE NEVER START</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, width: '100%', display: 'flex', justifyContent: 'center', gap: 26}}>
					{[0, 1, 2, 3].map((i) => {
						const p = usePop(0.2 + i * 0.1, 13);
						return (
							<div key={i} style={{opacity: Math.min(1, p * 1.5), transform: `scale(${0.6 + 0.4 * p}) translateY(${i === 0 ? -14 * ease(t, C.oneIn, 0.4) : 0}px)`}}>
								<Person size={190} gold={i === 0 ? ease(t, C.oneIn - 0.05, 0.4) : 0} />
							</div>
						);
					})}
				</div>
				<div style={{position: 'absolute', top: 650, width: '100%', textAlign: 'center', opacity: ease(t, C.oneIn - 0.05)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 200, lineHeight: 1, ...GOLD_TEXT}}>1 IN 4</div>
					<div style={{fontFamily: DISPLAY, fontSize: 62, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.adults)}}>ADULTS HAS A SECOND INCOME</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, marginTop: 12, opacity: ease(t, C.second + 0.3)}}>U.S. adults with a side hustle: 27% (Bankrate survey, 2025)</div>
				</div>
				<div style={{position: 'absolute', top: 1030, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 76, lineHeight: 1.05, color: COLORS.champagne, opacity: win(t, C.ifYou, C.alone - 0.3, 0.25)}}>
					💭 THOUGHT ABOUT IT<br />FOR <span style={GOLD_TEXT}>YEARS?</span>
				</div>
				<div style={{position: 'absolute', left: 420, right: 40, top: 1010}}>
					<div style={{position: 'absolute', fontFamily: DISPLAY, fontSize: 88, lineHeight: 1, color: '#fff', opacity: win(t, C.alone - 0.1, C.stops - 0.2, 0.2)}}>YOU'RE<br /><span style={GOLD_TEXT}>NOT ALONE</span></div>
					<div style={{position: 'absolute', fontFamily: DISPLAY, fontSize: 88, lineHeight: 1, color: '#fff', opacity: ease(t, C.stops, 0.2), transform: `scale(${interpolate(usePop(C.stops, 12), [0, 1], [0.8, 1])})`, transformOrigin: '0 50%'}}>SO WHAT<br /><span style={GOLD_TEXT}>STOPS US?</span></div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.alone - 0.25} seconds={Math.min(1.35, C.survey - C.alone - 0.2)} style={{left: 60, top: 990, width: 330, height: 232}} accent="relief" focus="50% 8%" />

			{/* THE THREE HURDLES a survey found: money, not knowing what to start, time */}
			<AbsoluteFill style={{opacity: hurdles, transform: push(t, C.survey, C.but)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>WHAT STOPS PEOPLE?</Chip>
				</div>
				{HURDLES.map(([icon, said, big], i) => (
					<div key={big} style={{position: 'absolute', left: 60, right: 60, top: 410 + i * 222}}>
						<Flip at={[C.h1, C.h2, C.h3][i] - 0.1}>
							<Panel style={{padding: '24px 28px', display: 'flex', alignItems: 'center', gap: 24, background: 'rgba(18,14,9,0.95)'}}>
								<Badge label={String(i + 1)} size={124} />
								<div style={{flex: 1}}>
									<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 34, color: COLORS.champagne, opacity: ease(t, [C.money, C.know, C.time][i])}}>{said}</div>
									<div style={{fontFamily: DISPLAY, fontSize: big.length > 18 ? 54 : 78, lineHeight: 1.02, color: '#fff'}}>{big}</div>
								</div>
								<div style={{fontSize: 92, lineHeight: 1}}>{icon}</div>
							</Panel>
						</Flip>
					</div>
				))}
				<div style={{position: 'absolute', top: 1100, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, C.time)}}>GOBankingRates survey on starting a business, 2023</div>
			</AbsoluteFill>
			<div style={{position: 'absolute', top: 850, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT, opacity: Math.min(hurdles, win(t, C.hurdles - 0.05, C.h1 - 0.2, 0.2))}}>3 HURDLES</div>
			<LeoMoment m="worried" at={C.hurdles - 0.1} seconds={Math.min(1.35, C.h1 - C.hurdles - 0.05)} style={{left: 340, top: 520, width: 400, height: 300}} sound={null} />

			{/* LOOK CLOSER: all three say the first step looks too big; so make it small (CSS 3D) */}
			<AbsoluteFill style={{opacity: reframe, transform: push(t, C.but, C.heres)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>LOOK CLOSER 🔍</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, width: '100%', display: 'flex', justifyContent: 'center', gap: 16}}>
					{[['💰', 'Money'], ['💡', 'Ideas'], ['⏰', 'Time']].map(([icon, text], i) => (
						<HintPill key={text} icon={icon} text={text} size={38} t={t} at={C.all + i * 0.12} />
					))}
				</div>
				<div style={{position: 'absolute', top: 492, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.04, color: '#fff'}}>
					<div style={{position: 'absolute', width: '100%', opacity: win(t, C.first - 0.1, C.small - 0.1, 0.25)}}>THE FIRST STEP<br /><span style={GOLD_TEXT}>LOOKS TOO BIG</span></div>
					<div style={{position: 'absolute', width: '100%', opacity: ease(t, C.small + 0.05, 0.25), transform: `scale(${interpolate(usePop(C.small + 0.05, 11), [0, 1], [0.75, 1])})`}}>SO MAKE IT<br /><span style={GOLD_TEXT}>SMALL</span></div>
				</div>
				{/* ground, the step and the person */}
				<div style={{position: 'absolute', left: 60, right: 60, top: 1180, height: 4, borderRadius: 2, background: `linear-gradient(90deg, transparent, ${COLORS.gold} 12%, ${COLORS.gold} 88%, transparent)`}} />
				<div style={{position: 'absolute', left: 470, top: 1180 - stepH, opacity: ease(t, C.first - 0.2, 0.3), transform: `translateY(${(1 - ease(t, C.first - 0.2, 0.5)) * 60}px)`}}>
					<Block3D w={400} h={stepH} d={220} rotX={-9} rotY={-24} tone={shrink > 0.6 ? 'gold' : 'dark'} label={<span style={{fontSize: shrink > 0.6 ? 54 : 92}}>STEP 1</span>} />
				</div>
				<div style={{position: 'absolute', left: 180 + hop * 420, top: 1180 - 150 - hop * smallH - Math.sin(hop * Math.PI) * 110, opacity: ease(t, C.same)}}>
					<Person size={120} gold={hop} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.small + 0.2} seconds={0.8} style={{left: 60, top: 700, width: 360, height: 270}} accent="aha" focus="50% 6%" />

			{/* THE SMALL FIRST STEP: 20 minutes a day on one skill; keep your job, keep your savings */}
			<AbsoluteFill style={{opacity: smallStep, transform: push(t, C.heres, C.thats)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>THE SMALL FIRST STEP 👣</Chip>
				</div>
				<div style={{position: 'absolute', left: 96, top: 404, opacity: ease(t, C.twenty - 0.2), transform: `perspective(1000px) rotateY(${interpolate(t, [C.twenty - 0.2, C.twenty + 0.7], [-70, 0], outCubic)}deg)`}}>
					<Dial size={340} minutes={minutes} />
				</div>
				<div style={{position: 'absolute', left: 486, top: 396, opacity: ease(t, C.twenty - 0.1), transform: `scale(${1 + 0.08 * Math.sin(Math.PI * interpolate(t, [C.just, C.just + 0.6], [0, 1], clamp))})`, transformOrigin: '0 50%'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 220, lineHeight: 0.95, ...GOLD_TEXT}}>20</div>
					<div style={{fontFamily: DISPLAY, fontSize: 76, lineHeight: 1, color: '#fff'}}>MINUTES<br />A DAY</div>
				</div>
				<div style={{position: 'absolute', top: 780, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 70, lineHeight: 1, color: '#fff', opacity: Math.min(ease(t, C.learning - 0.1), fadeOut(t, C.just - 0.2, 0.25))}}>
					LEARNING <span style={GOLD_TEXT}>ONE SKILL</span>
				</div>
				<div style={{position: 'absolute', top: 872, left: 20, right: 20, display: 'flex', justifyContent: 'center', gap: 10, opacity: fadeOut(t, C.just - 0.2, 0.25)}}>
					{[['🤖', 'AI tools'], ['✍️', 'Writing'], ['🎨', 'Design'], ['🛒', 'Selling online']].map(([icon, text], i) => (
						<HintPill key={text} icon={icon} text={text} size={30} t={t} at={C.learning + 0.25 + i * 0.12} />
					))}
				</div>
				<div style={{position: 'absolute', top: 1012, width: '100%', display: 'flex', justifyContent: 'center', gap: 16}}>
					<HintPill icon="✅" text="Keep your job" size={38} t={t} at={C.notJob} />
					<HintPill icon="✅" text="Keep your savings" size={38} t={t} at={C.notSave} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="thumbsup" at={C.just + 0.05} seconds={Math.min(1.2, C.thats - C.just - 0.1)} style={{left: 350, top: 772, width: 380, height: 226}} accent="warm" focus="50% 8%" />

			{/* THE MATH: about 120 hours a year, 15 full working days */}
			<AbsoluteFill style={{opacity: math, transform: push(t, C.thats, C.wont)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>20 MIN × 365 DAYS</Chip>
				</div>
				<div style={{position: 'absolute', top: 384, width: '100%', textAlign: 'center', opacity: ease(t, C.hours - 0.1)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 300, lineHeight: 1, ...GOLD_TEXT}}>{hoursN}</div>
					<div style={{fontFamily: DISPLAY, fontSize: 88, lineHeight: 1, color: '#fff', opacity: ease(t, C.year - 0.35)}}>HOURS A YEAR</div>
				</div>
				<div style={{position: 'absolute', top: 800, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 66, lineHeight: 1, color: '#fff', opacity: ease(t, C.fifteen - 0.1)}}>
					= <span style={GOLD_TEXT}>15 FULL WORKING DAYS</span>
				</div>
				<div style={{position: 'absolute', top: 890, left: 137, width: 806, display: 'flex', flexWrap: 'wrap', gap: 14}}>
					{Array.from({length: 15}).map((_, i) => {
						const at = C.fifteen + 0.15 + i * ((C.found - C.fifteen - 0.3) / 15);
						const p = usePop(at, 12);
						const glow = ease(t, C.found, 0.6);
						return (
							<div key={i} style={{width: 150, height: 94, borderRadius: 16, boxSizing: 'border-box', border: `2.5px solid ${COLORS.gold}`, background: `linear-gradient(160deg, rgba(242,173,60,${0.12 + 0.3 * glow}), rgba(18,14,9,0.95))`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: Math.min(1, p * 1.6), transform: `scale(${0.5 + 0.5 * p})`, boxShadow: `0 0 ${22 * glow}px rgba(242,173,60,0.35)`}}>
								<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 20, color: COLORS.champagne}}>DAY</div>
								<div style={{fontFamily: DISPLAY, fontSize: 48, lineHeight: 1, color: COLORS.goldHi}}>{i + 1}</div>
							</div>
						);
					})}
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.hours + 0.75} seconds={Math.min(1.15, C.fifteen - C.hours - 0.85)} style={{left: 340, top: 830, width: 400, height: 300}} accent="wow" />

			{/* AN HONEST NOTE: not rich overnight, but it gets you started; small steps (CSS 3D stairs) */}
			<AbsoluteFill style={{opacity: honest, transform: push(t, C.wont, C.which)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>AN HONEST NOTE 🤝</Chip>
				</div>
				<div style={{position: 'absolute', top: 396, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 78, lineHeight: 1.05, color: COLORS.champagne, opacity: ease(t, C.wont)}}>
					IT WON'T MAKE YOU<br />RICH OVERNIGHT
				</div>
				<div style={{position: 'absolute', top: 580, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 96, lineHeight: 1, color: '#fff', opacity: ease(t, C.gets - 0.05), transform: `scale(${interpolate(usePop(C.gets - 0.05, 12), [0, 1], [0.8, 1])})`}}>
					BUT IT GETS YOU <span style={GOLD_TEXT}>STARTED</span>
				</div>
				{[0, 1, 2, 3, 4].map((i) => {
					const on = ease(t, climbs[i] === undefined ? 1e9 : climbs[i] + 0.3, 0.3);
					return (
						<div key={i} style={{position: 'absolute', left: STAIR_X + i * STAIR_W, top: 1090 - (i + 1) * STAIR_H, width: STAIR_W, height: (i + 1) * STAIR_H, boxSizing: 'border-box', borderTop: `6px solid ${COLORS.gold}`, borderLeft: '2px solid rgba(242,173,60,0.5)', borderRight: '2px solid rgba(242,173,60,0.25)', borderRadius: '8px 8px 0 0', background: 'linear-gradient(180deg, #2a2116, #130e08)', opacity: ease(t, C.wont + 0.3 + i * 0.1), transform: `translateY(${(1 - ease(t, C.wont + 0.3 + i * 0.1, 0.5)) * 40}px)`, overflow: 'hidden'}}>
							<div style={{position: 'absolute', inset: 0, background: GOLD_FILL, opacity: on}} />
							<div style={{position: 'absolute', top: 6, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 34, color: on > 0.5 ? '#2a1a05' : COLORS.goldHi, opacity: 0.9}}>{i + 1}</div>
						</div>
					);
				})}
				<div style={{position: 'absolute', left: STAIR_X + (climb - 0.5) * STAIR_W - 55, top: 1090 - climb * STAIR_H - Math.sin(frac * Math.PI) * 52 - 134, opacity: ease(t, C.wont + 0.3)}}>
					<Person size={110} gold={Math.min(1, climb)} />
				</div>
				<div style={{position: 'absolute', top: 1112, width: '100%', textAlign: 'center'}}>
					<HintPill icon="🔖" text="Save this for your first 20 minutes" size={34} t={t} at={C.starting + 0.3} />
				</div>
				<div style={{position: 'absolute', top: 1192, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, C.rich)}}>No income promises. Results differ for everyone.</div>
			</AbsoluteFill>

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.which + 0.4} seconds={Math.min(4.2, C.send - C.which - 0.45)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={40} style={{background: 'rgba(5,4,3,0.9)'}}>WHAT HOLDS YOU BACK?</Chip>
				<div style={{marginTop: 14, display: 'flex', justifyContent: 'center', gap: 12}}>
					<HintPill icon="💰" text="Money" size={36} t={t} at={C.moneyQ} />
					<HintPill icon="💡" text="Ideas" size={36} t={t} at={C.ideas} />
					<HintPill icon="⏰" text="Time" size={36} t={t} at={C.timeQ} />
				</div>
				<div style={{marginTop: 12}}>
					<HintPill icon="👇" text="Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS TO <span style={GOLD_TEXT}>A COLLEAGUE</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.oneDay - 0.9)}}>who keeps saying “one day” 🗓️</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.colleague + 0.2} seconds={Math.min(2.05, C.join - C.colleague - 0.2)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'ai', 'streams', 'tutorials', 'tribe']} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [0.2, 'tick', 0.3], [0.3, 'tick', 0.3], [0.4, 'tick', 0.3], [0.5, 'tick', 0.3], [C.oneIn, 'coin', 0.32], [C.adults, 'pluck2', 0.26], [C.stops, 'tension', 0.3],
					[C.survey, 'paper', 0.3], [C.hurdles - 0.1, 'drop', 0.22], [C.h1 - 0.1, 'pluck3', 0.32], [C.h1 + 0.25, 'thud', 0.28], [C.h2 - 0.1, 'pluck2', 0.32], [C.h2 + 0.25, 'thud', 0.28], [C.h3 - 0.1, 'pluck1', 0.32], [C.h3 + 0.25, 'thud', 0.28],
					[C.but, 'air', 0.28], [C.all, 'pluck1', 0.26], [C.all + 0.12, 'pluck2', 0.26], [C.all + 0.24, 'pluck3', 0.26], [C.first - 0.2, 'rise', 0.36], [C.big, 'thud', 0.36], [C.small - 0.1, 'shrink', 0.5], [C.small + 0.7, 'step', 0.5],
					[C.heres, 'chime', 0.3], [C.twenty, 'clock', 0.3], [C.learning - 0.1, 'pluck2', 0.28], [C.learning + 0.25, 'pluck3', 0.22], [C.notJob, 'pluck4', 0.3], [C.notSave, 'pluck5', 0.3],
					[C.thats, 'paper', 0.28], [C.hours, 'count', 0.24], [C.year, 'reveal', 0.3], [C.fifteen - 0.1, 'pluck1', 0.28], [C.fifteen + 0.2, 'flutter', 0.24], [C.found, 'glow', 0.34],
					[C.wont, 'air', 0.26], [C.gets + 0.35, 'step', 0.5], [C.gets - 0.05, 'reveal', 0.3], [C.starting + 0.35, 'step', 0.5], [C.skip + 0.05, 'step', 0.5], [C.starting + 0.3, 'pluck3', 0.24],
					[C.which, 'chime', 0.3], [C.moneyQ, 'pluck1', 0.28], [C.ideas, 'pluck2', 0.28], [C.timeQ, 'pluck3', 0.28], [C.tell, 'pluck2', 0.26], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/10/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover10: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>WHY MOST PEOPLE</Chip>
		</div>
		<div style={{position: 'absolute', top: 370, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 196, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>NEVER START</div>
		<div style={{position: 'absolute', top: 566, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 124, lineHeight: 1.0, ...GOLD_TEXT}}>A SECOND INCOME</div>
		<div style={{position: 'absolute', left: 250, top: 760}}>
			<Block3D w={330} h={400} d={200} rotX={-9} rotY={-24} tone="dark" label={<span style={{fontSize: 84}}>STEP 1</span>} />
		</div>
		<div style={{position: 'absolute', left: 70, top: 1000}}>
			<Person size={130} />
		</div>
		<div style={{position: 'absolute', top: 750, left: 640, width: 380, height: 430, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V3-aha.png')} style={{width: 380, height: 666, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', left: 60, right: 60, top: 1164, height: 4, borderRadius: 2, background: `linear-gradient(90deg, transparent, ${COLORS.gold} 12%, ${COLORS.gold} 55%, transparent 62%)`}} />
		<div style={{position: 'absolute', top: 1232, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 100, lineHeight: 1.02, color: COLORS.champagne}}>AND THE <span style={GOLD_TEXT}>SMALL</span> FIRST STEP</div>
		<div style={{position: 'absolute', top: 1356, width: '100%', textAlign: 'center'}}>
			<Chip size={40}>FOR FULL-TIME EMPLOYEES 👣</Chip>
		</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

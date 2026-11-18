import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/13/captions.json';
import C from '../../../public/videos/13/cues.json';
import timeline from '../../../public/videos/13/timeline.json';
import W from '../../../public/videos/13/words.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Coin3D, Laptop3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 13 (18 Nov 2026, daily video): What Everyone Ought to Know About Copy Trading. Built on MTG's own JetUP guide
// (mtgtribe.com/jetup): his minibus taxi picture and his five checks, told without any brand name (his trading
// opportunities are promoted on his websites and in the tribe, never pitched in a social video). The risk is named
// once, gently. Script and research: tools/videos/13-what-everyone-ought-to-know-copy-trading/.
// Facts on screen: global FX trading of $9.5 trillion a day in April 2025 (BIS Triennial Survey, revised figure).

export const WEK13_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const WEK13_FRAMES = Math.ceil((timeline.total + TAIL) * WEK13_FPS);
// MTG's approved slogan (16 November 2026): the start of each of its four words
const SLOGAN = W.words.slice(-4).map((w) => w.start);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};

/** An original minibus taxi, seen from the side: a driver at the wheel and one seat marked "YOUR SEAT". */
const Minibus: React.FC<{w: number; t: number; seat: number; driver: number}> = ({w, t, seat, driver}) => {
	const wheel = t * 400;
	return (
		<svg width={w} height={w * 0.5} viewBox="0 0 400 200" style={{filter: 'drop-shadow(0 22px 26px rgba(0,0,0,0.6))'}}>
			<defs>
				<linearGradient id="mb13body" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#fbf3df" />
					<stop offset="1" stopColor="#d9c9a3" />
				</linearGradient>
			</defs>
			<path d="M20 150 L20 70 C20 52 30 40 52 40 L300 40 C326 40 340 50 352 70 L380 112 C386 122 386 130 386 140 L386 150 Z" fill="url(#mb13body)" stroke={COLORS.gold} strokeWidth="3" />
			<rect x="20" y="118" width="366" height="12" fill={COLORS.gold} />
			{/* windows: three passenger windows and the driver's window at the front */}
			{[40, 112, 184].map((x) => <rect key={x} x={x} y="54" width="62" height="44" rx="6" fill="#2a3a46" stroke="#1a2228" strokeWidth="2" />)}
			<path d="M262 54 L318 54 C328 54 334 58 340 66 L356 98 L262 98 Z" fill="#2a3a46" stroke="#1a2228" strokeWidth="2" />
			{/* passengers */}
			{[64, 136].map((x) => (
				<g key={x}>
					<circle cx={x} cy="72" r="9" fill="#6b5a44" />
					<rect x={x - 12} y="82" width="24" height="16" rx="6" fill="#6b5a44" />
				</g>
			))}
			{/* your seat, lit in gold */}
			<g opacity={0.35 + 0.65 * seat}>
				<rect x="190" y="58" width="50" height="40" rx="6" fill={COLORS.gold} opacity={0.25 + 0.6 * seat} />
				<circle cx="215" cy="72" r="9" fill={COLORS.goldHi} />
				<rect x="203" y="82" width="24" height="16" rx="6" fill={COLORS.goldHi} />
			</g>
			{/* the driver, with a cap and a wheel */}
			<g opacity={0.4 + 0.6 * driver}>
				<circle cx="296" cy="72" r="9" fill="#3a2508" />
				<rect x="285" y="62" width="22" height="6" rx="3" fill={COLORS.gold} />
				<rect x="284" y="82" width="24" height="16" rx="6" fill="#3a2508" />
				<circle cx="318" cy="84" r="9" fill="none" stroke={COLORS.gold} strokeWidth="3" />
			</g>
			<rect x="372" y="122" width="12" height="8" rx="3" fill="#ffe6a8" />
			{[90, 310].map((x) => (
				<g key={x} transform={`rotate(${wheel} ${x} 152)`}>
					<circle cx={x} cy="152" r="26" fill="#1a1410" stroke={COLORS.gold} strokeWidth="3" />
					<circle cx={x} cy="152" r="10" fill={COLORS.gold} />
					{[0, 60, 120].map((r) => <line key={r} x1={x - 20} y1="152" x2={x + 20} y2="152" stroke="#6b4512" strokeWidth="3" transform={`rotate(${r} ${x} 152)`} />)}
				</g>
			))}
		</svg>
	);
};

/** An account card that shows one trade appearing: a gold bar whose length is the trade size. */
const Account: React.FC<{title: string; balance: string; size: number; label: string; at: number; t: number; mine?: boolean}> = ({title, balance, size, label, at, t, mine}) => {
	const p = interpolate(t, [at, at + 0.5], [0, 1], outCubic);
	return (
		<Panel style={{padding: '22px 22px', background: 'rgba(14,11,7,0.97)', borderColor: mine ? COLORS.goldHi : 'rgba(242,173,60,0.5)'}}>
			<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 2, color: mine ? COLORS.goldHi : COLORS.champagne}}>{title}</div>
			<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.05, color: '#fff'}}>{balance}</div>
			<div style={{marginTop: 18, fontFamily: BODY, fontWeight: 800, fontSize: 32, color: COLORS.muted, opacity: p > 0 ? 1 : 0.35}}>{p > 0 ? 'Trade opened ▲' : 'Waiting...'}</div>
			<div style={{marginTop: 12, height: 46, borderRadius: 23, background: 'rgba(255,255,255,0.06)', overflow: 'hidden'}}>
				<div style={{width: `${size * p}%`, height: '100%', borderRadius: 23, background: GOLD_FILL, boxShadow: '0 0 14px rgba(242,173,60,0.6)'}} />
			</div>
			<div style={{marginTop: 10, fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.goldHi, opacity: p}}>{label}</div>
		</Panel>
	);
};

const QUESTIONS: Array<[icon: string, text: string]> = [
	['🏦', 'Who holds my money?'],
	['⚖️', 'Who regulates the broker?'],
	['📊', 'Are the results real?'],
	['📏', 'How big are the moves?'],
	['🚪', 'Can I get out?'],
];

export const CopyTrading: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.think - 0.3, 0.3);
	const bus = win(t, C.think - 0.15, C.copy2 - 0.3, 0.3);
	const copy = win(t, C.copy2 - 0.15, C.before - 0.3, 0.3);
	const qs = win(t, C.before - 0.15, C.risk - 0.3, 0.3);
	const risk = win(t, C.risk - 0.15, C.guide - 0.3, 0.3);
	const guide = win(t, C.guide - 0.15, C.which - 0.3, 0.3);
	const ask = win(t, C.which - 0.1, C.send - 0.2, 0.25);
	const shareP = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const trillions = interpolate(t, [C.about, C.trillion + 0.4], [0, 9.5], outCubic);
	const drive = interpolate(t, [C.minibus - 0.3, C.minibus + 0.9], [-700, 0], outCubic) + interpolate(t, [C.drives, C.copy2 - 0.2], [0, 140], clamp);
	const QA = [C.q1, C.q2, C.q3, C.q4, C.q5];
	const open = interpolate(t, [C.checks - 0.3, C.checks + 0.6], [0, 1], outCubic);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: what everyone ought to know about copy trading; about $9.5 trillion traded a day; here it is, simply */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.think)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={34}>WHAT EVERYONE OUGHT TO KNOW ABOUT</Chip>
				</div>
				<div style={{position: 'absolute', top: 378, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, C.copy - 0.15), transform: `scale(${interpolate(usePop(C.copy - 0.15, 11), [0, 1], [0.7, 1])})`}}>COPY TRADING</div>
				<div style={{position: 'absolute', top: 560, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 22, opacity: ease(t, C.every - 0.1)}}>
					{['$', '€', '£', '¥', 'R'].map((sym, i) => (
						<div key={sym} style={{transform: `translateY(${Math.sin(t * 1.8 + i) * 10}px)`, opacity: ease(t, C.every - 0.1 + i * 0.1)}}>
							<Coin3D size={130} symbol={sym} rotY={interpolate(t, [C.every - 0.1 + i * 0.1, C.every + 1.1 + i * 0.1], [-360, 0], outCubic) + Math.sin(t * 1.4 + i) * 16} glow={0.4} />
						</div>
					))}
				</div>
				<div style={{position: 'absolute', top: 740, width: '100%', textAlign: 'center', opacity: ease(t, C.about - 0.1)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT}}>${trillions.toFixed(1)} TRILLION</div>
					<div style={{fontFamily: DISPLAY, fontSize: 52, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.currency - 0.2)}}>TRADED IN CURRENCY MARKETS, EVERY DAY</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 24, color: COLORS.muted, marginTop: 8, opacity: ease(t, C.currency + 0.3)}}>Source: BIS Triennial Survey, April 2025</div>
				</div>
				<div style={{position: 'absolute', top: 1080, width: '100%', textAlign: 'center', opacity: ease(t, C.here - 0.1)}}>
					<HintPill icon="👇" text="Here it is, simply" size={40} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.trillion + 0.45} seconds={Math.min(1.6, C.most - C.trillion - 0.3)} style={{left: 340, top: 980, width: 400, height: 240}} accent="wow" sound={null} />

			{/* THE MINIBUS TAXI: you don't drive; pick a driver, take your seat, the driver does the driving */}
			<AbsoluteFill style={{opacity: bus, transform: push(t, C.think, C.copy2)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>THINK OF A MINIBUS TAXI 🚐</Chip>
				</div>
				<div style={{position: 'absolute', top: 384, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 96, lineHeight: 1, color: '#fff', opacity: ease(t, C.dont - 0.1)}}>
					YOU <span style={GOLD_TEXT}>DON'T DRIVE</span>
				</div>
				<div style={{position: 'absolute', left: 40, top: 520, transform: `translateX(${drive}px) translateY(${Math.abs(Math.sin(t * 9)) * -4}px)`}}>
					<Minibus w={1000} t={t} seat={ease(t, C.seat - 0.1)} driver={ease(t, C.pick - 0.1)} />
				</div>
				<div style={{position: 'absolute', top: 1050, left: 30, right: 30, display: 'flex', justifyContent: 'center', gap: 12}}>
					<HintPill icon="🧑‍✈️" text="Pick a driver" size={32} t={t} at={C.pick - 0.1} />
					<HintPill icon="💺" text="Take your seat" size={32} t={t} at={C.seat - 0.1} />
					<HintPill icon="🛣️" text="They drive" size={32} t={t} at={C.drives - 0.1} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="laugh" at={C.seat + 0.3} seconds={Math.min(2.0, C.copy2 - C.seat - 0.5)} style={{left: 360, top: 790, width: 360, height: 240}} focus="50% 6%" accent="warm" sound={null} />

			{/* COPY TRADING: you choose a strategy; its trades are copied into your account automatically, sized to your balance */}
			<AbsoluteFill style={{opacity: copy, transform: push(t, C.copy2, C.before)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>COPY TRADING WORKS THE SAME WAY</Chip>
				</div>
				<div style={{position: 'absolute', left: 50, width: 440, top: 400}}>
					<Flip at={C.strategy - 0.2}>
						<Account title="THE STRATEGY" balance="$10,000" size={90} label="trade size 10" at={C.trades} t={t} />
					</Flip>
				</div>
				<div style={{position: 'absolute', left: 494, width: 92, top: 560, textAlign: 'center', fontFamily: DISPLAY, fontSize: 90, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, C.copied - 0.1), transform: `translateX(${Math.sin(t * 5) * 6}px)`}}>➜</div>
				<div style={{position: 'absolute', left: 590, width: 440, top: 400}}>
					<Flip at={C.copied - 0.2}>
						<Account title="YOUR ACCOUNT" balance="$1,000" size={9} label="trade size 1" at={C.auto} t={t} mine />
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 850, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.04, color: '#fff', opacity: ease(t, C.auto - 0.1)}}>
					COPIED <span style={GOLD_TEXT}>AUTOMATICALLY</span>
				</div>
				<div style={{position: 'absolute', top: 956, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 72, lineHeight: 1, color: COLORS.champagne, opacity: ease(t, C.sized - 0.1)}}>
					SIZED TO YOUR BALANCE
				</div>
				<div style={{position: 'absolute', top: 1050, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, C.sized + 0.3)}}>An example with round numbers, not a real account.</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.choose - 0.05} seconds={Math.min(1.7, C.trades - C.choose)} style={{left: 360, top: 830, width: 360, height: 300}} focus="50% 12%" sound={null} />

			{/* FIVE QUESTIONS before you take a seat: MTG's five checks, ticked one by one */}
			<AbsoluteFill style={{opacity: qs, transform: push(t, C.before, C.risk)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>BEFORE YOU TAKE A SEAT 💺</Chip>
				</div>
				<div style={{position: 'absolute', top: 380, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 84, lineHeight: 1, color: '#fff', opacity: ease(t, C.five - 0.1)}}>
					ASK <span style={GOLD_TEXT}>5 QUESTIONS</span>
				</div>
				<div style={{position: 'absolute', left: 70, right: 70, top: 492, display: 'flex', flexDirection: 'column', gap: 14}}>
					{QUESTIONS.map(([icon, text], i) => {
						const at = QA[i];
						const p = usePop(at - 0.1, 13);
						const tick = ease(t, at + 0.55, 0.2);
						return (
							<div key={text} style={{display: 'flex', alignItems: 'center', gap: 18, padding: '14px 22px', borderRadius: 22, background: 'rgba(18,14,9,0.95)', border: `2px solid ${tick > 0.5 ? COLORS.goldHi : 'rgba(242,173,60,0.45)'}`, opacity: Math.min(1, p * 1.5), transform: `translateX(${(1 - Math.min(1, p)) * -80}px)`}}>
								<div style={{fontFamily: DISPLAY, fontSize: 44, width: 40, color: COLORS.goldHi}}>{i + 1}</div>
								<div style={{fontSize: 46, lineHeight: 1}}>{icon}</div>
								<div style={{flex: 1, fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text}}>{text}</div>
								<div style={{width: 52, height: 52, borderRadius: 12, border: `3px solid ${COLORS.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', background: tick > 0.5 ? GOLD_FILL : 'transparent'}}>
									<span style={{fontFamily: DISPLAY, fontSize: 40, lineHeight: 1, color: '#2a1a05', opacity: tick, transform: `scale(${0.5 + 0.5 * tick})`}}>✓</span>
								</div>
							</div>
						);
					})}
				</div>
				<div style={{position: 'absolute', top: 1110, width: '100%', textAlign: 'center'}}>
					<HintPill icon="🔖" text="Save these 5 questions" size={36} t={t} at={C.q5 + 0.4} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.five + 0.1} seconds={Math.min(1.15, C.q1 - C.five - 0.25)} style={{left: 380, top: 640, width: 320, height: 260}} accent="aha" focus="50% 6%" />

			{/* THE RISK, ONCE AND GENTLY: start small and learn first */}
			<AbsoluteFill style={{opacity: risk, transform: push(t, C.risk, C.guide)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>AN HONEST NOTE 🤝</Chip>
				</div>
				<div style={{position: 'absolute', top: 400, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 100, lineHeight: 1.02, color: COLORS.champagne, opacity: ease(t, C.risk - 0.05)}}>
					TRADING<br />CARRIES RISK
				</div>
				<div style={{position: 'absolute', top: 640, width: '100%', display: 'flex', justifyContent: 'center', gap: 18}}>
					<HintPill icon="🐢" text="Start small" size={50} t={t} at={C.small - 0.1} />
					<HintPill icon="📚" text="Learn first" size={50} t={t} at={C.learn - 0.1} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.risk + 0.35} seconds={Math.min(1.35, C.small - C.risk - 0.35)} style={{left: 290, top: 770, width: 500, height: 400}} accent="relief" focus="50% 8%" />
			<LeoMoment m="thumbsup" at={C.learn - 0.05} seconds={Math.min(1.5, C.guide - C.learn - 0.1)} style={{left: 290, top: 770, width: 500, height: 400}} accent="warm" focus="50% 8%" sound={null} />

			{/* MY FULL GUIDE: the five checks, waiting in the free tribe (the laptop moment) */}
			<AbsoluteFill style={{opacity: guide, transform: push(t, C.guide, C.which)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>MY FULL GUIDE 📖</Chip>
				</div>
				<div style={{position: 'absolute', left: 140, top: 420, opacity: ease(t, C.guide - 0.1)}}>
					<Laptop3D w={800} open={open}>
						<div style={{padding: '26px 34px', fontFamily: BODY, color: COLORS.text}}>
							<div style={{fontFamily: DISPLAY, fontSize: 54, lineHeight: 1, ...GOLD_TEXT}}>THE 5 CHECKS</div>
							{QUESTIONS.map(([icon, text], i) => (
								<div key={text} style={{fontWeight: 800, fontSize: 28, marginTop: 10, opacity: ease(t, C.checks + 0.4 + i * 0.15)}}>{icon} {text} <span style={{color: COLORS.goldHi}}>✓</span></div>
							))}
						</div>
					</Laptop3D>
				</div>
				<div style={{position: 'absolute', top: 1000, width: '100%', textAlign: 'center', opacity: ease(t, C.tribe - 0.3)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 56, lineHeight: 1, color: '#fff', marginBottom: 14}}>FREE IN THE <span style={GOLD_TEXT}>MTG TRIBE</span></div>
					<UrlPill text="mtgtribe.com/group" size={48} t={t} at={C.tribe - 0.1} />
				</div>
			</AbsoluteFill>

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.which} seconds={Math.min(4.2, C.send - C.which - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={38} style={{background: 'rgba(5,4,3,0.9)'}}>WHICH QUESTION FIRST? 🤔</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Tell me below: 1 to 5" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: shareP}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.curious - 0.2)}}>who's curious about trading 📈</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['honest', 'crypto', 'ai', 'streams', 'tribe']} sloganWords={SLOGAN} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [C.copy - 0.15, 'reveal', 0.3], [C.every - 0.1, 'coin', 0.3], [C.every + 0.2, 'coin', 0.24], [C.about, 'count', 0.22], [C.trillion + 0.4, 'swell', 0.26], [C.here - 0.1, 'pluck2', 0.28],
					[C.think - 0.15, 'air', 0.26], [C.minibus - 0.3, 'engine', 0.36], [C.pick - 0.1, 'pluck1', 0.3], [C.seat - 0.1, 'pluck2', 0.3], [C.drives - 0.1, 'pluck3', 0.3], [C.drives + 0.3, 'hoot', 0.3],
					[C.copy2 - 0.15, 'air', 0.26], [C.strategy - 0.2, 'paper', 0.28], [C.trades, 'pluck3', 0.3], [C.copied - 0.1, 'mirror', 0.45], [C.auto, 'pluck2', 0.26], [C.sized - 0.1, 'glow', 0.26],
					[C.before - 0.15, 'chime', 0.28], ...[C.q1, C.q2, C.q3, C.q4, C.q5].map((a) => [a + 0.55, 'tickbox', 0.42] as [number, string, number]), [C.q5 + 0.4, 'pluck4', 0.24],
					[C.risk - 0.15, 'air', 0.24], [C.small - 0.1, 'pluck1', 0.28], [C.learn - 0.1, 'pluck2', 0.28],
					[C.checks - 0.3, 'laptop', 0.45], [C.tribe - 0.1, 'glow', 0.3],
					[C.which, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/13/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover13: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={36}>WHAT EVERYONE OUGHT TO KNOW ABOUT</Chip>
		</div>
		<div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 196, lineHeight: 1.0, ...GOLD_TEXT}}>COPY TRADING</div>
		<div style={{position: 'absolute', left: 40, top: 640}}>
			<Minibus w={620} t={0} seat={1} driver={1} />
		</div>
		<div style={{position: 'absolute', top: 600, left: 670, width: 370, height: 430, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V5-think.png')} style={{width: 370, height: 648, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1066, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.02, color: '#fff'}}>
			5 QUESTIONS<br /><span style={{...GOLD_TEXT, fontSize: 84}}>BEFORE YOU TAKE A SEAT</span>
		</div>
		<div style={{position: 'absolute', top: 1300, width: '100%', display: 'flex', justifyContent: 'center', gap: 16}}>
			{QUESTIONS.map(([icon]) => (
				<div key={icon} style={{width: 92, height: 92, borderRadius: 22, border: `3px solid ${COLORS.gold}`, background: 'rgba(18,14,9,0.95)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 52}}>{icon}</div>
			))}
		</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

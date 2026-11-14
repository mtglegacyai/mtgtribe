import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/09/captions.json';
import C from '../../../public/videos/09/cues.json';
import timeline from '../../../public/videos/09/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Block3D, Coin3D, Notepad3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 09 (14 Nov 2026, daily video): Can You Guess How Much Gold Has Ever Been Mined? A quiz with three options, a
// countdown and a calm reveal; the lesson is scarcity (gold, then Bitcoin's 21 million) and one tip: ask how rare it is.
// Script and research: tools/videos/09-can-you-guess-gold/. Every time is a named cue from the voice's own word
// timings (public/videos/09/cues.json).
// Facts on screen (World Gold Council, read 14 November 2026): more than 220,000 tonnes mined in all of history; one
// cube of about 22.6 m on each side; a 105 x 68 m soccer field, of which that cube's footprint is about 7%.

export const CYG09_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const CYG09_FRAMES = Math.ceil((timeline.total + TAIL) * CYG09_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};
const outBack = {...clamp, easing: Easing.out(Easing.back(1.3))};

const OPTIONS: Array<[letter: string, icon: string, small: string, big: string]> = [
	['A', '⛰️', 'As big as a', 'MOUNTAIN'],
	['B', '🏟️', 'As big as a', 'STADIUM'],
	['C', '🏢', 'As tall as a', '7-FLOOR BUILDING'],
];

const Badge: React.FC<{letter: string; size: number; glow?: number}> = ({letter, size, glow = 0}) => (
	<div style={{width: size, height: size, flexShrink: 0, borderRadius: '50%', background: GOLD_FILL, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: size * 0.62, lineHeight: 1, color: '#2a1a05', boxShadow: `0 12px 30px rgba(0,0,0,0.5), 0 0 ${60 * glow}px rgba(242,173,60,${0.7 * glow})`}}>{letter}</div>
);

/** A seven-floor building, drawn floor by floor; the windows light up from the ground floor to the top. */
const Building: React.FC<{w: number; floorH: number; t: number; at: number}> = ({w, floorH, t, at}) => (
	<div style={{width: w}}>
		<div style={{height: 10, margin: '0 -8px', borderRadius: 4, background: COLORS.gold}} />
		{[7, 6, 5, 4, 3, 2, 1].map((n) => {
			const lit = ease(t, at + (n - 1) * 0.09, 0.25);
			return (
				<div key={n} style={{height: floorH, boxSizing: 'border-box', borderBottom: '2px solid rgba(242,173,60,0.35)', borderLeft: `3px solid ${COLORS.gold}`, borderRight: `3px solid ${COLORS.gold}`, background: 'linear-gradient(180deg, #2a2116, #17110a)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 12, position: 'relative'}}>
					<div style={{position: 'absolute', left: -46, fontFamily: MONO, fontWeight: 700, fontSize: 26, color: COLORS.goldHi, opacity: lit}}>{n}</div>
					{n === 1 ? (
						<>
							<div style={{width: 34, height: floorH * 0.5, borderRadius: 4, background: `rgba(255,214,130,${0.2 + 0.7 * lit})`}} />
							<div style={{width: 40, height: floorH * 0.78, alignSelf: 'flex-end', borderRadius: '6px 6px 0 0', background: '#5a3b10', border: `2px solid ${COLORS.gold}`}} />
							<div style={{width: 34, height: floorH * 0.5, borderRadius: 4, background: `rgba(255,214,130,${0.2 + 0.7 * lit})`}} />
						</>
					) : (
						[0, 1, 2, 3].map((k) => <div key={k} style={{width: 34, height: floorH * 0.5, borderRadius: 4, background: `rgba(255,214,130,${0.2 + 0.7 * lit})`, boxShadow: `0 0 ${14 * lit}px rgba(255,200,110,0.5)`}} />)
					)}
				</div>
			);
		})}
	</div>
);

/** A soccer field from above, drawn to scale: 105 x 68 m at `s` pixels per metre. */
const Pitch: React.FC<{s: number; children?: React.ReactNode}> = ({s, children}) => {
	const W = 105 * s;
	const H = 68 * s;
	const line = '4px solid rgba(255,255,255,0.85)';
	const box = (w: number, h: number, right: boolean): React.CSSProperties => ({position: 'absolute', top: (H - h * s) / 2, width: w * s, height: h * s, boxSizing: 'border-box', border: line, ...(right ? {right: 0, borderRight: 'none'} : {left: 0, borderLeft: 'none'})});
	return (
		<div style={{width: W, height: H, position: 'relative', boxSizing: 'border-box', border: line, borderRadius: 6, background: `repeating-linear-gradient(90deg, #2f7d3b 0 ${W / 12}px, #2a7035 ${W / 12}px ${W / 6}px)`, boxShadow: '0 40px 60px rgba(0,0,0,0.6)'}}>
			<div style={{position: 'absolute', left: W / 2 - 2, top: 0, bottom: 0, width: 4, background: 'rgba(255,255,255,0.85)'}} />
			<div style={{position: 'absolute', left: W / 2 - 9.15 * s, top: H / 2 - 9.15 * s, width: 18.3 * s, height: 18.3 * s, boxSizing: 'border-box', borderRadius: '50%', border: line}} />
			<div style={box(16.5, 40.3, false)} />
			<div style={box(16.5, 40.3, true)} />
			<div style={box(5.5, 18.3, false)} />
			<div style={box(5.5, 18.3, true)} />
			{children}
		</div>
	);
};

export const GoldCube: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hookA = fadeOut(t, C.picture - 0.3, 0.3);
	const hookB = win(t, C.picture - 0.15, C.optA - 0.3, 0.3);
	const quiz = win(t, C.optA - 0.15, C.its - 0.3, 0.3);
	const answer = win(t, C.its - 0.15, C.fits - 0.3, 0.3);
	const size = win(t, C.fits - 0.15, C.field - 0.3, 0.3);
	const field = win(t, C.field - 0.15, C.secret - 0.3, 0.3);
	const secret = win(t, C.secret - 0.15, C.btc - 0.3, 0.3);
	const btc = win(t, C.btc - 0.15, C.so - 0.3, 0.3);
	const tip = win(t, C.so - 0.15, C.did - 0.3, 0.3);
	const ask = win(t, C.did - 0.1, C.send - 0.15, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const years = Math.round(interpolate(t, [C.hook + 0.3, C.six + 0.5], [0, 6000], outCubic) / 100) * 100;
	const grow = interpolate(t, [C.melted, C.cube + 0.4], [0.12, 1], outCubic);
	const stream = Math.min(interpolate(t, [C.melted - 0.15, C.melted + 0.25], [0, 1], clamp), fadeOut(t, C.cube + 0.25, 0.3));
	const dim = interpolate(t, [C.three - 0.25, C.three], [1, 0.16], clamp);
	const tonnes = Math.round(interpolate(t, [C.tonnes, C.tonnesEnd - 0.25], [0, 220000], outCubic) / 1000) * 1000;
	const rise = interpolate(t, [C.fits - 0.1, C.fits + 0.7], [0, 1], outCubic);
	const land = interpolate(t, [C.covers - 0.1, C.covers + 0.35], [0, 1], outBack);
	const coins = Math.round(interpolate(t, [C.only + 0.2, C.only + 1.0], [0, 21], outCubic));
	const counts: Array<[string, number, number]> = [['3', C.three, C.two], ['2', C.two, C.one], ['1', C.one, C.its - 0.25]];

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK A: humans have chased gold for 6,000 years; can you guess how much we've found? */}
			<AbsoluteFill style={{opacity: hookA, transform: push(t, 0, C.picture)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={40}>CAN YOU GUESS? 🤔</Chip>
				</div>
				<div style={{position: 'absolute', top: 384, width: '100%', textAlign: 'center', opacity: ease(t, C.hook)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 230, lineHeight: 1, ...GOLD_TEXT}}>{years.toLocaleString('en-US')}</div>
					<div style={{fontFamily: DISPLAY, fontSize: 66, lineHeight: 1, color: '#fff', marginTop: 4}}>YEARS OF CHASING GOLD</div>
				</div>
				<div style={{position: 'absolute', top: 716, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 80, lineHeight: 1, color: COLORS.champagne, opacity: ease(t, C.guess), transform: `scale(${interpolate(usePop(C.guess, 12), [0, 1], [0.8, 1])})`}}>
					HOW MUCH HAVE <span style={GOLD_TEXT}>WE FOUND?</span>
				</div>
				<div style={{position: 'absolute', top: 812, width: '100%', display: 'flex', justifyContent: 'center', gap: 34}}>
					{['👑', '💍', '🥇', '🪙'].map((e, i) => {
						const p = usePop(C.found + i * 0.1, 11);
						return <div key={e} style={{fontSize: 92, lineHeight: 1, opacity: Math.min(1, p * 1.6), transform: `scale(${0.4 + 0.6 * p})`}}>{e}</div>;
					})}
				</div>
			</AbsoluteFill>
			<LeoMoment m="point" at={C.guess + 0.15} seconds={Math.min(1.45, C.picture - C.guess - 0.3)} style={{left: 340, top: 940, width: 400, height: 290}} focus="50% 8%" sound={null} />

			{/* HOOK B: picture all of it, melted into one cube (CSS 3D) */}
			<AbsoluteFill style={{opacity: hookB, transform: push(t, C.picture, C.optA)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>PICTURE THIS</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 112, lineHeight: 1.02, color: '#fff'}}>
					ALL THE GOLD<br /><span style={GOLD_TEXT}>EVER MINED</span>
				</div>
				<div style={{position: 'absolute', left: 527, top: 640, width: 26, height: 200 * stream, borderRadius: 13, background: `linear-gradient(180deg, #fff1c4, ${COLORS.goldHi} 30%, ${COLORS.gold})`, boxShadow: '0 0 30px rgba(255,190,90,0.8)', opacity: stream}} />
				<div style={{position: 'absolute', left: 395, top: 840, transform: `scale(${grow})`, transformOrigin: '50% 100%', opacity: ease(t, C.melted, 0.2)}}>
					<Block3D w={290} h={290} d={290} rotX={-14} rotY={-30 + Math.sin(t * 1.3) * 14} label="?" />
				</div>
			</AbsoluteFill>

			{/* THE QUIZ: A a mountain, B a stadium, C a 7-floor building; then three, two, one */}
			<AbsoluteFill style={{opacity: quiz, transform: push(t, C.optA, C.its)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>{t < C.three - 0.2 ? 'HOW BIG IS THAT CUBE?' : 'LOCK IN YOUR ANSWER 🔒'}</Chip>
				</div>
				{OPTIONS.map(([letter, icon, small, big], i) => (
					<div key={letter} style={{position: 'absolute', left: 70, right: 70, top: 410 + i * 226, opacity: dim}}>
						<Flip at={[C.optA, C.optB, C.optC][i] - 0.1}>
							<Panel style={{padding: '24px 30px', display: 'flex', alignItems: 'center', gap: 26, background: 'rgba(18,14,9,0.95)'}}>
								<Badge letter={letter} size={132} />
								<div style={{flex: 1}}>
									<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, color: COLORS.champagne}}>{small}</div>
									<div style={{fontFamily: DISPLAY, fontSize: big.length > 10 ? 80 : 96, lineHeight: 1, color: '#fff'}}>{big}</div>
								</div>
								<div style={{fontSize: 100, lineHeight: 1, opacity: ease(t, [C.mountain, C.stadium, C.building][i] - 0.1)}}>{icon}</div>
							</Panel>
						</Flip>
					</div>
				))}
				{counts.map(([n, a, b]) => (
					<div key={n} style={{position: 'absolute', top: 380, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 520, lineHeight: 1, ...GOLD_TEXT, filter: 'drop-shadow(0 20px 50px rgba(0,0,0,0.9))', opacity: win(t, a - 0.05, b - 0.12, 0.12), transform: `scale(${interpolate(t, [a - 0.05, a + 0.3], [1.5, 1], outCubic)})`}}>{n}</div>
				))}
			</AbsoluteFill>
			<LeoMoment m="think" at={C.three - 0.1} seconds={Math.min(2.4, C.its - C.three - 0.15)} style={{left: 370, top: 930, width: 340, height: 300}} focus="50% 12%" sound={null} />

			{/* THE ANSWER: it's C; more than 220,000 tonnes */}
			<AbsoluteFill style={{opacity: answer, transform: push(t, C.its, C.fits)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>THE ANSWER ✅</Chip>
				</div>
				<div style={{position: 'absolute', top: 400, left: 70, right: 70, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 30}}>
					<div style={{transform: `scale(${interpolate(usePop(C.its + 0.3, 10), [0, 1], [0.3, 1])})`}}>
						<Badge letter="C" size={210} glow={ease(t, C.its + 0.3, 0.5)} />
					</div>
					<div style={{opacity: ease(t, C.its + 0.5)}}>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 42, color: COLORS.champagne}}>As tall as a</div>
						<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1, color: '#fff'}}>7-FLOOR<br />BUILDING 🏢</div>
					</div>
				</div>
				<div style={{position: 'absolute', top: 690, width: '100%', textAlign: 'center', opacity: ease(t, C.tonnes - 0.1)}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: 3, color: COLORS.goldHi}}>ALL THE GOLD EVER MINED</div>
					<div style={{fontFamily: DISPLAY, fontSize: 216, lineHeight: 1.02, ...GOLD_TEXT}}>{tonnes.toLocaleString('en-US')}{tonnes >= 220000 ? '+' : ''}</div>
					<div style={{fontFamily: DISPLAY, fontSize: 96, lineHeight: 1, color: '#fff'}}>TONNES</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 28, color: COLORS.muted, marginTop: 18, opacity: ease(t, C.tonnesEnd)}}>Estimate: World Gold Council, 2026</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.its + 0.4} seconds={Math.min(1.6, C.tonnes - C.its - 0.6)} style={{left: 330, top: 700, width: 420, height: 320}} accent="wow" sound={null} />

			{/* THE SIZE: one cube, about 22.6 m on each side, beside a 7-floor building (CSS 3D) */}
			<AbsoluteFill style={{opacity: size, transform: push(t, C.fits, C.field)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>IT ALL FITS IN ONE CUBE</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, width: '100%', textAlign: 'center', opacity: ease(t, C.metres - 0.15), transform: `scale(${interpolate(usePop(C.metres - 0.15, 12), [0, 1], [0.8, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 170, lineHeight: 1, ...GOLD_TEXT}}>≈ 22.6 m</span>
					<div style={{fontFamily: DISPLAY, fontSize: 60, lineHeight: 1, color: '#fff'}}>ON EACH SIDE</div>
				</div>
				<div style={{position: 'absolute', left: 110, top: 696, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 2, color: COLORS.champagne, width: 250, textAlign: 'center'}}>7 FLOORS</div>
				<div style={{position: 'absolute', left: 110, top: 740}}>
					<Building w={250} floorH={58} t={t} at={C.fits + 0.1} />
				</div>
				<div style={{position: 'absolute', left: 384, top: 1108, textAlign: 'center', opacity: ease(t, C.fits + 0.5)}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 22, color: COLORS.champagne}}>you</div>
					<div style={{fontSize: 30, lineHeight: 1}}>🧍</div>
				</div>
				<div style={{position: 'absolute', left: 591, top: 779, transform: `scale(${0.1 + 0.9 * rise})`, transformOrigin: '50% 100%', opacity: Math.min(1, rise * 3)}}>
					<Block3D w={348} h={348} d={348} rotX={-7} rotY={-30 + Math.sin(t * 1.1) * 8} label="GOLD" sub="all of it" />
				</div>
				<div style={{position: 'absolute', left: 60, right: 60, top: 1156, height: 4, borderRadius: 2, background: `linear-gradient(90deg, transparent, ${COLORS.gold} 12%, ${COLORS.gold} 88%, transparent)`}} />
				<div style={{position: 'absolute', left: 96, width: interpolate(t, [C.metres, C.metres + 0.6], [0, 900], outCubic), top: 748, height: 0, borderTop: `4px dashed ${COLORS.goldHi}`, opacity: 0.85}} />
			</AbsoluteFill>

			{/* ON A SOCCER FIELD: it covers less than a tenth of the grass (to scale, CSS 3D tilt) */}
			<AbsoluteFill style={{opacity: field, transform: push(t, C.field, C.secret)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>ON A SOCCER FIELD ⚽</Chip>
				</div>
				<div style={{position: 'absolute', left: 67, top: 372, perspective: 1700}}>
					<div style={{transform: `rotateX(${interpolate(t, [C.field - 0.15, C.field + 0.8], [58, 30], outCubic)}deg)`, transformOrigin: '50% 60%'}}>
						<Pitch s={9}>
							<div style={{position: 'absolute', left: (945 - 203) / 2, top: (612 - 203) / 2, width: 203, height: 203, boxSizing: 'border-box', borderRadius: 6, background: GOLD_FILL, border: '3px solid #fff1c4', boxShadow: `0 0 ${50 * land}px rgba(255,200,90,0.9), 0 14px 22px rgba(0,0,0,0.5)`, opacity: Math.min(1, land * 2), transform: `scale(${interpolate(land, [0, 1], [1.9, 1])})`, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: DISPLAY, fontSize: 42, lineHeight: 1, color: '#2a1a05'}}>ALL THE<br />GOLD</div>
						</Pitch>
					</div>
				</div>
				<div style={{position: 'absolute', left: 420, right: 40, top: 990, opacity: ease(t, C.tenth - 0.35)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 88, lineHeight: 1, ...GOLD_TEXT}}>LESS THAN<br />A TENTH</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, color: COLORS.champagne, marginTop: 6}}>about 7% of the grass</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="mindblown" at={C.covers + 0.35} seconds={Math.min(1.75, C.secret - C.covers - 0.6)} style={{left: 60, top: 984, width: 330, height: 232}} focus="50% 4%" accent="wow" />

			{/* GOLD'S SECRET: it's rare, and nobody can print more */}
			<AbsoluteFill style={{opacity: secret, transform: push(t, C.secret, C.btc)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>GOLD'S SECRET 🤫</Chip>
				</div>
				<div style={{position: 'absolute', left: 410, top: 440}}>
					<Block3D w={260} h={260} d={260} rotX={-16} rotY={interpolate(t, [C.secret, C.btc], [-70, 20])} label="Au" sub="gold" />
				</div>
				<div style={{position: 'absolute', top: 810, left: 40, right: 40, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22}}>
					<HintPill icon="💎" text="It's rare" size={58} t={t} at={C.rare - 0.1} />
					<HintPill icon="🚫" text="Nobody can print more" size={50} t={t} at={C.print - 0.1} />
				</div>
				<div style={{position: 'absolute', top: 1096, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 32, color: COLORS.champagne, opacity: ease(t, C.print + 0.6)}}>New gold has to be found and mined, slowly.</div>
			</AbsoluteFill>

			{/* BITCOIN BORROWS THE IDEA: only 21 million coins, ever */}
			<AbsoluteFill style={{opacity: btc, transform: push(t, C.btc, C.so)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>BITCOIN BORROWS THE IDEA</Chip>
				</div>
				<div style={{position: 'absolute', left: 130, top: 440}}>
					<Block3D w={200} h={200} d={200} rotX={-16} rotY={-30 + Math.sin(t * 1.2) * 10} label="Au" />
				</div>
				<div style={{position: 'absolute', left: 400, width: 280, top: 440, textAlign: 'center', opacity: ease(t, C.btc + 0.2)}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 2, color: COLORS.champagne}}>SAME IDEA</div>
					<div style={{fontFamily: DISPLAY, fontSize: 130, lineHeight: 1, ...GOLD_TEXT, transform: `translateX(${Math.sin(t * 4) * 8}px)`}}>➜</div>
				</div>
				<div style={{position: 'absolute', left: 710, top: 420, opacity: ease(t, C.btc)}}>
					<Coin3D size={240} rotY={interpolate(t, [C.btc, C.btc + 1.2], [-360, 0], outCubic) + Math.sin(t * 1.6) * 16} rotX={8} glow={0.6} />
				</div>
				<div style={{position: 'absolute', top: 730, width: '100%', textAlign: 'center', opacity: ease(t, C.only - 0.1)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 70, lineHeight: 1, color: '#fff'}}>ONLY</div>
					<div style={{fontFamily: DISPLAY, fontSize: 200, lineHeight: 1.02, ...GOLD_TEXT}}>{coins},000,000</div>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1, color: '#fff', opacity: ease(t, C.ever - 0.5), transform: `scale(${interpolate(usePop(C.ever - 0.5, 11), [0, 1], [1.3, 1])})`}}>COINS, EVER</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, marginTop: 18, opacity: ease(t, C.ever)}}>The limit is written into Bitcoin's code.</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.only + 0.8} seconds={Math.min(1.15, C.so - C.only - 1.1)} style={{left: 390, top: 400, width: 300, height: 290}} accent="aha" focus="50% 6%" />

			{/* THE TIP: before you put money into anything, ask how rare it is (the notepad moment) */}
			<AbsoluteFill style={{opacity: tip, transform: push(t, C.so, C.did)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>💡 TODAY'S TIP</Chip>
				</div>
				<div style={{position: 'absolute', top: 396, left: 40, right: 40, textAlign: 'center', fontFamily: DISPLAY, fontSize: 80, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.so)}}>
					BEFORE YOU PUT MONEY<br />INTO ANYTHING, <span style={GOLD_TEXT}>ASK:</span>
				</div>
				<div style={{position: 'absolute', left: 150, top: 630, opacity: ease(t, C.ask - 0.3), transform: `translateY(${(1 - ease(t, C.ask - 0.3, 0.5)) * 50}px)`}}>
					<Notepad3D w={780} t={t} title="ASK FIRST" lines={[['How rare is it,', C.howRare - 0.05], ['really?', C.howRare + 0.95]]} />
				</div>
				<div style={{position: 'absolute', top: 1062, width: '100%', textAlign: 'center'}}>
					<HintPill icon="🔖" text="Save this tip" size={40} t={t} at={C.ask + 0.2} />
				</div>
				<div style={{position: 'absolute', top: 1172, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 27, color: COLORS.muted, opacity: ease(t, C.howRare)}}>Education, not financial advice. Prices move.</div>
			</AbsoluteFill>

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.did} seconds={Math.min(4.2, C.send - C.did - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={40} style={{background: 'rgba(5,4,3,0.9)'}}>DID YOU GUESS RIGHT? 🤔</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="A, B or C? Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.thinks - 0.2)}}>who thinks there's a mountain of gold ⛰️</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'ai', 'streams', 'tutorials', 'tribe']} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [C.hook + 0.3, 'count', 0.2], [C.six + 0.5, 'reveal', 0.3], [C.guess, 'tension', 0.32], [C.found, 'coin', 0.28],
					[C.picture - 0.15, 'air', 0.25], [C.melted - 0.15, 'pour', 0.5], [C.cube + 0.4, 'glow', 0.3],
					[C.optA - 0.1, 'pluck1', 0.32], [C.optB - 0.1, 'pluck2', 0.32], [C.optC - 0.1, 'pluck3', 0.32], [C.three - 0.25, 'swell', 0.3], [C.three, 'tick', 0.45], [C.two, 'tick', 0.45], [C.one, 'tick', 0.5],
					[C.its + 0.3, 'gong', 0.55], [C.tonnes, 'count', 0.22], [C.tonnesEnd - 0.25, 'coinrain', 0.24],
					[C.fits - 0.1, 'rise', 0.36], [C.metres - 0.15, 'reveal', 0.34],
					[C.field - 0.15, 'air', 0.28], [C.covers, 'thud', 0.42], [C.tenth - 0.35, 'pluck3', 0.28],
					[C.secret, 'shimmer', 0.36], [C.rare - 0.1, 'pluck2', 0.3], [C.print - 0.1, 'flutter', 0.24],
					[C.btc, 'coin', 0.32], [C.only + 0.2, 'count', 0.2], [C.ever - 0.5, 'thud', 0.32],
					[C.so, 'paper', 0.32], [C.ask + 0.2, 'pluck3', 0.26], [C.howRare - 0.05, 'scribble', 0.42],
					[C.did, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/09/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover09: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>CAN YOU GUESS? 🤔</Chip>
		</div>
		<div style={{position: 'absolute', top: 372, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 168, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>ALL THE GOLD</div>
		<div style={{position: 'absolute', top: 540, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 168, lineHeight: 1.0, ...GOLD_TEXT}}>EVER MINED</div>
		<div style={{position: 'absolute', left: 120, top: 800}}>
			<Block3D w={340} h={340} d={340} rotX={-14} rotY={-32} label={<span style={{fontSize: 230}}>?</span>} />
		</div>
		<div style={{position: 'absolute', top: 760, left: 620, width: 390, height: 440, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V5-think.png')} style={{width: 390, height: 683, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1246, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 112, lineHeight: 1, color: COLORS.champagne}}>HOW BIG IS THE CUBE?</div>
		<div style={{position: 'absolute', top: 1372, width: '100%', display: 'flex', justifyContent: 'center', gap: 30}}>
			{OPTIONS.map(([letter, icon]) => (
				<div key={letter} style={{display: 'flex', alignItems: 'center', gap: 12}}>
					<Badge letter={letter} size={74} />
					<span style={{fontSize: 66, lineHeight: 1}}>{icon}</span>
				</div>
			))}
		</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

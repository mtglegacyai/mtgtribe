import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/06/captions.json';
import C from '../../../public/videos/06/cues.json';
import timeline from '../../../public/videos/06/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Laptop3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, GOLD_TEXT, usePop, useT} from '../whatif01/ui';

// Video 06 (11 Nov 2026, daily video): The Hidden Cost of Your Commute. For full-time employees: calm, respectful,
// hopeful ("inform, never frighten"). Script and research: tools/videos/06-hidden-cost-of-your-commute/.
// Every time is a named cue from the voice's own word timings (public/videos/06/cues.json).
// The example: 1 hour there + 1 hour back, 5 days a week, 48 working weeks = 480 hours = 60 working days of 8 hours.
// 20 minutes a day = 80 hours a year = 10 working days.

export const HCC06_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const HCC06_FRAMES = Math.ceil((timeline.total + TAIL) * HCC06_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const RED = '#e0602f';
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};

/** A generic minibus taxi (an original drawing, no real make): the wheels turn with `spin` (degrees). */
const Taxi: React.FC<{w: number; spin: number; lights?: number}> = ({w, spin, lights = 1}) => {
	const h = w * 0.48;
	const wheel = (x: number) => (
		<g transform={`translate(${x} 152)`}>
			<circle r="26" fill="#14100b" stroke="#3a3024" strokeWidth="4" />
			<g transform={`rotate(${spin})`}>
				<circle r="12" fill={COLORS.gold} />
				{[0, 60, 120].map((d) => <rect key={d} x="-2.5" y="-20" width="5" height="40" rx="2" fill="#6b4512" transform={`rotate(${d})`} />)}
			</g>
		</g>
	);
	return (
		<svg width={w} height={h} viewBox="0 0 400 192" style={{overflow: 'visible', filter: 'drop-shadow(0 16px 20px rgba(0,0,0,0.55))'}}>
			<defs>
				<linearGradient id="t06body" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#fbf6ea" />
					<stop offset="1" stopColor="#d9cfbb" />
				</linearGradient>
			</defs>
			<ellipse cx="392" cy="120" rx={60 * lights} ry={26 * lights} fill="rgba(255,226,160,0.28)" />
			<path d="M26 150 V58 Q26 26 60 26 H292 Q322 26 340 52 L378 104 Q388 116 388 132 V150 Z" fill="url(#t06body)" stroke="#8a7a5c" strokeWidth="3" />
			<rect x="26" y="112" width="362" height="16" fill={COLORS.gold} />
			{[52, 122, 192].map((x) => <rect key={x} x={x} y="46" width="58" height="48" rx="8" fill="#22303c" stroke="#8a7a5c" strokeWidth="2" />)}
			<path d="M266 46 H292 Q306 46 318 62 L342 94 H266 Z" fill="#22303c" stroke="#8a7a5c" strokeWidth="2" />
			<rect x="246" y="46" width="6" height="104" fill="#8a7a5c" />
			<rect x="372" y="118" width="16" height="12" rx="4" fill="#ffe9a8" />
			<rect x="20" y="144" width="374" height="10" rx="4" fill="#3a3024" />
			{wheel(98)}
			{wheel(306)}
		</svg>
	);
};

/** A price tag that turns over in 3D: the fare on the front, the real cost on the back. */
const Tag: React.FC<{w: number; flip: number; strike: number}> = ({w, flip, strike}) => {
	const h = w * 0.56;
	const face: React.CSSProperties = {position: 'absolute', inset: 0, borderRadius: 36, backfaceVisibility: 'hidden', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', boxSizing: 'border-box'};
	return (
		<div style={{width: w, height: h, perspective: w * 2.6, filter: 'drop-shadow(0 24px 30px rgba(0,0,0,0.6))'}}>
			<div style={{position: 'relative', width: '100%', height: '100%', transformStyle: 'preserve-3d', transform: `rotateY(${flip * 180}deg) rotateZ(-4deg)`}}>
				<div style={{...face, background: 'linear-gradient(160deg, #fbf3df, #e6d6ae)', border: '4px solid #b99a55'}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: w * 0.07, letterSpacing: 4, color: '#6b4512'}}>THE FARE</div>
					<div style={{position: 'relative', fontFamily: DISPLAY, fontSize: w * 0.26, lineHeight: 1.05, color: '#2a1a05'}}>
						R 🚐
						<div style={{position: 'absolute', left: -14, right: -14, top: '50%', height: 12, borderRadius: 6, background: RED, transformOrigin: 'left center', transform: `scaleX(${strike}) rotate(-5deg)`}} />
					</div>
				</div>
				<div style={{...face, transform: 'rotateY(180deg)', background: GOLD_FILL, border: `4px solid ${COLORS.goldHi}`}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: w * 0.07, letterSpacing: 4, color: '#5a3b10'}}>THE REAL COST</div>
					<div style={{display: 'flex', alignItems: 'center', gap: w * 0.03, whiteSpace: 'nowrap'}}>
						<span style={{fontSize: w * 0.15, lineHeight: 1}}>⏳</span>
						<span style={{fontFamily: DISPLAY, fontSize: w * 0.17, lineHeight: 1.1, color: '#2a1a05'}}>YOUR TIME</span>
					</div>
				</div>
				<div style={{position: 'absolute', left: 26, top: '50%', width: 30, height: 30, marginTop: -15, borderRadius: '50%', background: COLORS.bg, border: '3px solid #b99a55', transform: 'translateZ(1px)'}} />
			</div>
		</div>
	);
};

const Sum: React.FC<{at: number; children: React.ReactNode; size?: number; color?: string}> = ({at, children, size = 76, color = '#fff'}) => {
	const p = usePop(at, 13);
	return <div style={{fontFamily: DISPLAY, fontSize: size, lineHeight: 1.12, color, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * 30}px)`}}>{children}</div>;
};

export const CommuteCost: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.there - 0.3, 0.3);
	const maths = win(t, C.there - 0.15, C.hidden - 0.3, 0.3);
	const reframe = win(t, C.hidden - 0.15, C.job - 0.3, 0.3);
	const job = win(t, C.job - 0.15, C.whatIf - 0.2, 0.25);
	const idea = win(t, C.whatIf - 0.1, C.day20 - 0.3, 0.3);
	const payA = win(t, C.day20 - 0.15, C.enough - 0.2, 0.25);
	const payB = win(t, C.enough - 0.1, C.q - 0.3, 0.3);
	const ask = win(t, C.q - 0.1, C.send - 0.15, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	// hook: the taxi rolls in, 60 squares fill as the days are counted
	const drive = interpolate(t, [0.1, 1.9], [0, 1], outCubic);
	const days = Math.round(interpolate(t, [C.sixty, C.just + 0.4], [0, 60], outCubic));
	const hours = Math.round(interpolate(t, [C.n480, C.year480], [0, 480], outCubic));
	const flip = interpolate(t, [C.yourTime - 0.2, C.yourTime + 0.4], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const slice = interpolate(t, [C.twenty2, C.learning], [0, 1 / 3], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const eighty = Math.round(interpolate(t, [C.n80 - 0.1, C.n80 + 0.7], [0, 80], outCubic));

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: an hour to work is 60 working days a year, just travelling; 20 minutes of it can change a lot */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.there)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.15)}}>
					<Chip size={38}>THE HIDDEN COST OF YOUR COMMUTE</Chip>
				</div>
				<div style={{position: 'absolute', left: 60, right: 60, top: 384, height: 210, borderRadius: 28, overflow: 'hidden', background: 'linear-gradient(180deg, #3a2610 0%, #20160b 55%, #120d07 100%)', border: '2px solid rgba(242,173,60,0.35)'}}>
					<div style={{position: 'absolute', left: '50%', top: 150, width: 420, height: 420, marginLeft: -210, borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,200,110,0.55), rgba(255,170,70,0.12) 55%, transparent 70%)', transform: `translateY(${-70 * ease(t, 0.2, 2.5)}px)`}} />
					<div style={{position: 'absolute', left: 0, right: 0, bottom: 22, height: 6, background: 'rgba(242,173,60,0.25)'}} />
					{Array.from({length: 9}, (_, i) => (
						<div key={i} style={{position: 'absolute', bottom: 22, height: 6, width: 70, borderRadius: 3, background: COLORS.gold, left: (((i * 150 - t * 260) % 1350) + 1350) % 1350 - 150}} />
					))}
					<div style={{position: 'absolute', left: -340 + drive * 640, bottom: 14 + Math.sin(t * 9) * 1.5}}>
						<Taxi w={320} spin={t * 520} lights={0.8 + 0.2 * Math.sin(t * 3)} />
					</div>
				</div>
				<div style={{position: 'absolute', left: 70, top: 612, width: 600, display: 'flex', alignItems: 'center', gap: 22, opacity: ease(t, C.sixty - 0.1, 0.25)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 200, lineHeight: 1, ...GOLD_TEXT, minWidth: 210, textAlign: 'right'}}>{days}</div>
					<div style={{fontFamily: DISPLAY, fontSize: 62, lineHeight: 1.05, color: '#fff'}}>WORKING DAYS<br /><span style={{color: COLORS.champagne}}>A YEAR</span></div>
				</div>
				<div style={{position: 'absolute', left: 540 - 350, top: 836, width: 700, display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: 6}}>
					{Array.from({length: 60}, (_, i) => {
						const k = (i % 12) * 5 + Math.floor(i / 12); // fill week by week (column by column)
						const on = k < days ? 1 : 0;
						return <div key={i} style={{aspectRatio: '1', borderRadius: 8, boxSizing: 'border-box', border: '2px solid rgba(242,173,60,0.3)', background: on ? GOLD_FILL : 'rgba(18,14,9,0.6)', opacity: ease(t, C.sixty - 0.2)}} />;
					})}
				</div>
				<div style={{position: 'absolute', top: 1146, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 34, color: COLORS.champagne, opacity: win(t, C.just, C.and20 - 0.1, 0.25)}}>12 working weeks, just travelling</div>
				<div style={{position: 'absolute', top: 1140, width: '100%', textAlign: 'center', opacity: ease(t, C.and20, 0.25), transform: `scale(${interpolate(usePop(C.and20, 11), [0, 1], [0.7, 1])})`}}>
					<Chip size={40} style={{borderColor: COLORS.goldHi, boxShadow: '0 0 34px rgba(242,173,60,0.45)'}}>⏱️ 20 MINUTES CAN CHANGE A LOT</Chip>
				</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.hook + 0.35} seconds={Math.min(1.8, C.sixty - C.hook - 0.35)} style={{left: 700, top: 606, width: 320, height: 212}} />
			<LeoMoment m="wow" at={C.sixty + 0.45} seconds={Math.min(1.7, C.and20 - C.sixty - 0.55)} style={{left: 700, top: 606, width: 320, height: 212}} accent="wow" />

			{/* THE MATHS: an hour there, an hour back, five days a week: 480 hours a year */}
			<AbsoluteFill style={{opacity: maths, transform: push(t, C.there, C.hidden)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, C.there - 0.1)}}>
					<Chip size={40}>🧮 THE MATHS</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, left: 0, right: 0, textAlign: 'center'}}>
					<div style={{display: 'flex', justifyContent: 'center', gap: 22}}>
						<Sum at={C.there}>1 HOUR THERE</Sum>
						<Sum at={C.back} color={COLORS.goldHi}>+ 1 BACK</Sum>
					</div>
					<Sum at={C.five}>× 5 DAYS A WEEK</Sum>
					<Sum at={C.five + 0.55} size={46} color={COLORS.champagne}>× 48 working weeks a year</Sum>
				</div>
				<div style={{position: 'absolute', left: 70, top: 676, width: 560, textAlign: 'center', opacity: ease(t, C.n480 - 0.1, 0.25)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 250, lineHeight: 1, ...GOLD_TEXT}}>{hours}</div>
					<div style={{fontFamily: DISPLAY, fontSize: 76, lineHeight: 1, color: '#fff', opacity: ease(t, C.year480 - 0.3)}}>HOURS A YEAR</div>
				</div>
				<div style={{position: 'absolute', top: 1040, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 38, color: COLORS.champagne, opacity: ease(t, C.year480 + 0.25)}}>= 60 working days of 8 hours</div>
				<div style={{position: 'absolute', top: 1128, left: 90, right: 90, textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, lineHeight: 1.3, color: COLORS.muted, opacity: ease(t, C.there + 0.5)}}>🇿🇦 A taxi trip to work takes about an hour on average<br />(Stats SA travel survey, 2020)</div>
			</AbsoluteFill>
			<LeoMoment m="mindblown" at={C.n480 + 0.5} seconds={Math.min(2.0, C.hidden - C.n480 - 0.85)} style={{left: 660, top: 690, width: 350, height: 300}} focus="50% 6%" />

			{/* THE REFRAME: not the fare, your time */}
			<AbsoluteFill style={{opacity: reframe, transform: push(t, C.hidden, C.job)}}>
				<div style={{position: 'absolute', top: 296, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.02, color: '#fff', opacity: ease(t, C.hidden), textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
					THE <span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>HIDDEN COST</span>
				</div>
				<div style={{position: 'absolute', left: 540 - 300, top: 470, opacity: ease(t, C.cost, 0.3), transform: `translateY(${(1 - ease(t, C.cost, 0.5)) * 60}px)`}}>
					<Tag w={600} flip={flip} strike={interpolate(t, [C.notFare + 0.15, C.notFare + 0.5], [0, 1], outCubic)} />
				</div>
				<div style={{position: 'absolute', top: 850, width: '100%', textAlign: 'center', opacity: win(t, C.notFare, C.yourTime - 0.1, 0.2)}}>
					<Chip size={40} style={{borderColor: RED, color: '#ffb48a'}}>NOT THE FARE</Chip>
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.yourTime + 0.15} seconds={Math.min(1.15, C.job - C.yourTime - 0.45)} style={{left: 330, top: 900, width: 420, height: 300}} accent="aha" focus="50% 6%" />

			{/* RESPECT FIRST: your job matters, keep it */}
			<AbsoluteFill style={{opacity: job}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', fontFamily: DISPLAY, lineHeight: 1.04}}>
					<div style={{fontSize: 104, color: '#fff', opacity: ease(t, C.job - 0.05), transform: `scale(${interpolate(usePop(C.job - 0.05, 12), [0, 1], [0.8, 1])})`}}>YOUR JOB MATTERS</div>
					<div style={{fontSize: 112, ...GOLD_TEXT, opacity: ease(t, C.keep - 0.05), transform: `scale(${interpolate(usePop(C.keep - 0.05, 11), [0, 1], [0.7, 1])})`}}>KEEP IT ✓</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.job + 0.1} seconds={Math.min(1.35, C.whatIf - C.job - 0.35)} style={{left: 300, top: 600, width: 480, height: 580}} accent="relief" focus="50% 10%" />

			{/* THE IDEA: 20 minutes of that trip, for learning */}
			<AbsoluteFill style={{opacity: idea, transform: push(t, C.whatIf, C.day20)}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.whatIf)}}>
					WHAT IF <span style={GOLD_TEXT}>20 MINUTES</span><br />WENT TO LEARNING?
				</div>
				<div style={{position: 'absolute', left: 90, right: 90, top: 640}}>
					<div style={{display: 'flex', justifyContent: 'space-between', fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.champagne, marginBottom: 12}}>
						<span>HOME</span>
						<span>YOUR TRIP: 60 MIN</span>
						<span>WORK</span>
					</div>
					<div style={{position: 'relative', height: 76, borderRadius: 38, border: `3px solid ${COLORS.gold}`, background: 'rgba(18,14,9,0.9)', overflow: 'hidden'}}>
						<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${slice * 100}%`, background: GOLD_FILL, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 34, color: '#1a1206', overflow: 'hidden', whiteSpace: 'nowrap'}}>{slice > 0.26 ? '20 MIN' : ''}</div>
					</div>
					<div style={{position: 'relative', height: 120}}>
						<div style={{position: 'absolute', left: `calc(${interpolate(t, [C.whatIf, C.day20], [0, 62], clamp)}% - 20px)`, top: 14}}>
							<Taxi w={190} spin={t * 520} lights={0.6} />
						</div>
					</div>
				</div>
				<div style={{position: 'absolute', top: 930, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
					<HintPill icon="🎧" text="20 minutes of learning, every trip" size={42} t={t} at={C.learning - 0.1} />
				</div>
				<div style={{position: 'absolute', top: 1090, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, opacity: ease(t, C.learning + 0.3)}}>Riding? Watch or read. Driving? Listen only.</div>
			</AbsoluteFill>

			{/* THE PAYOFF (a): 20 minutes a day is 80 hours a year, two full working weeks */}
			<AbsoluteFill style={{opacity: payA, transform: push(t, C.day20, C.enough)}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.day20)}}>20 MINUTES A DAY</div>
				<div style={{position: 'absolute', top: 410, width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 22, opacity: ease(t, C.n80 - 0.15, 0.25)}}>
					<span style={{fontFamily: DISPLAY, fontSize: 96, color: COLORS.champagne}}>=</span>
					<span style={{fontFamily: DISPLAY, fontSize: 260, lineHeight: 1, ...GOLD_TEXT}}>{eighty}</span>
					<span style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1, color: '#fff'}}>HOURS<br /><span style={{color: COLORS.champagne}}>A YEAR</span></span>
				</div>
				<div style={{position: 'absolute', left: 540 - 320, top: 760, width: 640, display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 14}}>
					{Array.from({length: 10}, (_, i) => {
						const p = usePop(C.twoWeeks + i * 0.09, 12);
						return (
							<div key={i} style={{height: 104, borderRadius: 16, background: GOLD_FILL, opacity: Math.min(1, p * 1.5), transform: `scale(${0.5 + 0.5 * p})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 28, color: '#5a3b10', boxShadow: '0 10px 24px rgba(0,0,0,0.45)'}}>{['MON', 'TUE', 'WED', 'THU', 'FRI'][i % 5]}</div>
						);
					})}
				</div>
				<div style={{position: 'absolute', top: 1030, width: '100%', textAlign: 'center', opacity: ease(t, C.twoWeeks + 0.5)}}>
					<Chip size={42}>2 FULL WORKING WEEKS</Chip>
				</div>
			</AbsoluteFill>

			{/* THE PAYOFF (b): enough to learn a skill, or start building a second income next to your job */}
			<AbsoluteFill style={{opacity: payB, transform: push(t, C.enough, C.q)}}>
				<div style={{position: 'absolute', top: 296, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.enough - 0.05)}}>
					<span style={GOLD_TEXT}>80 HOURS</span> IS ENOUGH TO
				</div>
				<div style={{position: 'absolute', top: 420, left: 40, right: 40, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
					<HintPill icon="🧠" text="Learn a new skill" size={46} t={t} at={C.skill - 0.15} />
					<HintPill icon="💼" text="Start a second income, next to your job" size={38} t={t} at={C.second - 0.2} />
				</div>
				<div style={{position: 'absolute', left: 500, top: 690, opacity: ease(t, C.enough + 0.1)}}>
					<Laptop3D w={500} open={interpolate(t, [C.enough + 0.2, C.enough + 1.2], [0, 1], outCubic)}>
						<div style={{width: '86%'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 22, color: COLORS.goldHi, letterSpacing: 2}}>▶ TUTORIAL 1</div>
							<div style={{marginTop: 12, height: 12, borderRadius: 6, background: 'rgba(255,255,255,0.15)'}}>
								<div style={{height: 12, borderRadius: 6, background: COLORS.gold, width: `${interpolate(t, [C.enough + 1.2, C.q], [5, 60], clamp)}%`}} />
							</div>
							<div style={{marginTop: 12, fontFamily: BODY, fontWeight: 800, fontSize: 22, color: COLORS.text}}>mtgtribe.com</div>
						</div>
					</Laptop3D>
				</div>
				<div style={{position: 'absolute', top: 1160, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, opacity: ease(t, C.second + 0.3)}}>No promises: it takes time and work.</div>
			</AbsoluteFill>
			<LeoMoment m="thumbsup" at={C.second + 0.1} seconds={Math.min(1.5, C.q - C.second - 0.45)} style={{left: 60, top: 700, width: 400, height: 430}} focus="50% 10%" sound="pluck3" volume={0.3} />

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.q} seconds={Math.min(4.2, C.send - C.q - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={38} style={{background: 'rgba(5,4,3,0.9)'}}>HOW LONG IS YOUR TRIP TO WORK? 💬</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Tell me in the comments" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO THE FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 46, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.rides - 0.3)}}>who rides with you 🚐</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'ai', 'streams', 'tutorials', 'tribe']} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'engine', 0.5], [1.5, 'hoot', 0.3], [C.sixty, 'count', 0.22], [C.and20, 'chime', 0.32],
					[C.there, 'pluck1', 0.32], [C.back, 'pluck2', 0.32], [C.five, 'pluck3', 0.32], [C.five + 0.55, 'tick', 0.25], [C.n480, 'swell', 0.3], [C.year480 + 0.25, 'pluck1', 0.28],
					[C.hidden, 'glow', 0.3], [C.notFare + 0.15, 'drop', 0.3], [C.yourTime - 0.2, 'paper', 0.42],
					[C.job - 0.05, 'pluck2', 0.3], [C.keep - 0.05, 'pluck3', 0.32],
					[C.whatIf, 'engine', 0.32], [C.twenty2, 'link', 0.38], [C.learning - 0.1, 'reveal', 0.35],
					[C.day20, 'pluck1', 0.3], [C.n80 - 0.1, 'swell', 0.3], [C.twoWeeks, 'count', 0.2],
					[C.enough + 0.2, 'laptop', 0.42], [C.skill - 0.15, 'pluck2', 0.32],
					[C.q, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'hoot', 0.26],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/06/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover06: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>IF YOU HAVE A JOB</Chip>
		</div>
		<div style={{position: 'absolute', top: 372, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 132, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
			THE <span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>HIDDEN COST</span><br />OF YOUR COMMUTE
		</div>
		<div style={{position: 'absolute', left: 60, top: 700}}>
			<Taxi w={500} spin={25} />
		</div>
		<div style={{position: 'absolute', top: 690, left: 600, width: 420, height: 470, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V5-think.png')} style={{width: 420, height: 735, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', left: 60, top: 968, width: 520, textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, lineHeight: 1.2, color: COLORS.champagne}}>1 hour there.<br />1 hour back.</div>
		<div style={{position: 'absolute', top: 1196, width: '100%', textAlign: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT}}>60 WORKING DAYS</div>
			<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 46, color: '#fff', marginTop: 6}}>a year, just travelling</div>
		</div>
		<div style={{position: 'absolute', top: 1470, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={180} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

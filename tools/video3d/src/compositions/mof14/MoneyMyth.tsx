import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/14/captions.json';
import C from '../../../public/videos/14/cues.json';
import timeline from '../../../public/videos/14/timeline.json';
import W from '../../../public/videos/14/words.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 14 (19 Nov 2026, daily video): Myth or Fact: You Need Money to Make Money Online. Three fact checks (what you
// really need, the free tools, the real cost) and an honest verdict: mostly myth; money helps you go faster, skills and
// time get you started; results take patience, no promises. No income claims. Script and research:
// tools/videos/14-myth-or-fact-money-to-make-money/. Every time is a named cue from the voice's own word timings.
// Facts on screen: 44% named "not enough money" as what stopped them starting a business (GOBankingRates survey,
// 2023, the same survey as video 10); a .com website name costs about $11 to $20 a year (registry price from
// 1 November 2026 plus registrar prices).

export const MOF14_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const MOF14_FRAMES = Math.ceil((timeline.total + TAIL) * MOF14_FPS);
// MTG's approved slogan (16 November 2026): the start of each of its four words
const SLOGAN = W.words.slice(-4).map((w) => w.start);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};

/** The claim on trial, with its two buttons. `pick` lights MYTH (-1) or FACT (1); 0 lets them pulse in turn. */
const Claim: React.FC<{t: number; scale?: number; pick?: number; stamp?: number}> = ({t, scale = 1, pick = 0, stamp = 0}) => {
	const pulse = (k: number) => (pick === 0 ? 0.5 + 0.5 * Math.sin(t * 5 + k * Math.PI) : pick === (k ? 1 : -1) ? 1 : 0.15);
	return (
		<div style={{transform: `scale(${scale})`, transformOrigin: '50% 0%', position: 'relative'}}>
			<Panel style={{padding: '30px 34px', background: 'rgba(18,14,9,0.97)', textAlign: 'center'}}>
				<div style={{fontFamily: DISPLAY, fontSize: 78, lineHeight: 1.04, color: '#fff'}}>“YOU NEED MONEY TO<br /><span style={GOLD_TEXT}>MAKE MONEY ONLINE”</span></div>
				<div style={{display: 'flex', justifyContent: 'center', gap: 26, marginTop: 26}}>
					{['MYTH', 'FACT'].map((label, k) => (
						<div key={label} style={{width: 250, padding: '14px 0', borderRadius: 999, fontFamily: DISPLAY, fontSize: 52, lineHeight: 1, color: '#2a1a05', background: GOLD_FILL, opacity: 0.35 + 0.65 * pulse(k), boxShadow: `0 0 ${36 * pulse(k)}px rgba(242,173,60,0.6)`, transform: `scale(${0.94 + 0.06 * pulse(k)})`}}>{label}</div>
					))}
				</div>
			</Panel>
			{stamp > 0 && (
				<div style={{position: 'absolute', left: '50%', top: '38%', width: 600, marginLeft: -300, textAlign: 'center', padding: '14px 0', border: '8px solid #e8954a', borderRadius: 20, color: '#e8954a', background: 'rgba(10,8,6,0.82)', fontFamily: DISPLAY, fontSize: 100, lineHeight: 1, opacity: Math.min(1, stamp * 3), transform: `rotate(-8deg) scale(${interpolate(stamp, [0, 0.35, 1], [2, 0.95, 1])})`, boxShadow: '0 20px 50px rgba(0,0,0,0.6)'}}>MOSTLY MYTH</div>
			)}
		</div>
	);
};

/** A tool tile whose price tag turns over from "$$$" to "$0" at `at` (a CSS 3D flip). */
const ToolTile: React.FC<{icon: string; name: string; at: number; t: number}> = ({icon, name, at, t}) => {
	const p = usePop(at - 0.25, 13);
	const flip = interpolate(t, [at + 0.15, at + 0.55], [0, 180], outCubic);
	return (
		<div style={{width: 320, textAlign: 'center', opacity: Math.min(1, p * 1.5), transform: `translateY(${(1 - Math.min(1, p)) * 60}px)`}}>
			<Panel style={{padding: '40px 14px 34px', background: 'rgba(18,14,9,0.96)'}}>
				<div style={{fontSize: 150, lineHeight: 1}}>{icon}</div>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 38, lineHeight: 1.15, color: COLORS.text, marginTop: 18, minHeight: 92}}>{name}</div>
				<div style={{perspective: 700, height: 90, marginTop: 14}}>
					<div style={{position: 'relative', width: 230, height: 90, margin: '0 auto', transformStyle: 'preserve-3d', transform: `rotateY(${flip}deg)`}}>
						<div style={{position: 'absolute', inset: 0, backfaceVisibility: 'hidden', borderRadius: 14, background: '#3a3024', border: '2px solid #6b5a44', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 56, color: COLORS.muted}}>$$$</div>
						<div style={{position: 'absolute', inset: 0, backfaceVisibility: 'hidden', transform: 'rotateY(180deg)', borderRadius: 14, background: GOLD_FILL, border: '2px solid #fff1c4', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 52, color: '#2a1a05', boxShadow: '0 0 24px rgba(242,173,60,0.6)'}}>$0 FREE</div>
					</div>
				</div>
			</Panel>
		</div>
	);
};

const NEEDS: Array<[icon: string, text: string, key: keyof typeof C]> = [
	['📱', 'A phone or a laptop', 'phone'],
	['📶', 'An internet connection', 'internet'],
	['🧠', 'One skill people need', 'skill'],
];

export const MoneyMyth: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.f1 - 0.3, 0.3);
	const f1 = win(t, C.f1 - 0.15, C.f2 - 0.3, 0.3);
	const f2 = win(t, C.f2 - 0.15, C.f3 - 0.3, 0.3);
	const f3 = win(t, C.f3 - 0.15, C.so - 0.3, 0.3);
	const verdict = win(t, C.so - 0.15, C.did - 0.3, 0.3);
	const ask = win(t, C.did - 0.1, C.send - 0.2, 0.25);
	const shareP = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const pct = Math.round(interpolate(t, [C.pct - 0.1, C.pct + 0.7], [0, 44], outCubic));
	const stamp = interpolate(t, [C.mostly - 0.05, C.mostly + 0.4], [0, 1], clamp);
	const hourglass = interpolate(t, [C.biggest, C.time + 0.6], [0, 180], outCubic);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: myth or fact? 44% said not enough money stopped them; let's check */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.f1)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={40}>MYTH OR FACT? 🤔</Chip>
				</div>
				<div style={{position: 'absolute', left: 50, right: 50, top: 386}}>
					<Flip at={C.needMoney - 0.3}>
						<Claim t={t} />
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 760, width: '100%', textAlign: 'center', opacity: ease(t, C.pct - 0.1)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 190, lineHeight: 1, ...GOLD_TEXT}}>{pct}%</div>
					<div style={{fontFamily: DISPLAY, fontSize: 50, lineHeight: 1.08, color: '#fff', opacity: ease(t, C.notEnough - 0.2)}}>SAID “NOT ENOUGH MONEY”<br />STOPPED THEM STARTING</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 24, color: COLORS.muted, marginTop: 8, opacity: ease(t, C.stopped)}}>GOBankingRates survey on starting a business, 2023</div>
				</div>
				<div style={{position: 'absolute', top: 1128, width: '100%', textAlign: 'center'}}>
					<HintPill icon="🔍" text="Let's check" size={38} t={t} at={C.check - 0.1} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.needMoney + 0.6} seconds={Math.min(2.2, C.pct - C.needMoney - 0.8)} style={{left: 360, top: 790, width: 360, height: 300}} focus="50% 12%" sound={null} />

			{/* FACT CHECK 1: what you really need: a phone or laptop, internet, one skill people need */}
			<AbsoluteFill style={{opacity: f1, transform: push(t, C.f1, C.f2)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>FACT CHECK 1 · WHAT YOU NEED</Chip>
				</div>
				<div style={{position: 'absolute', left: 70, right: 70, top: 400, display: 'flex', flexDirection: 'column', gap: 20}}>
					{NEEDS.map(([icon, text, key], i) => {
						const at = C[key] - 0.15;
						const p = usePop(at, 13);
						return (
							<div key={text} style={{display: 'flex', alignItems: 'center', gap: 26, padding: '22px 30px', borderRadius: 30, background: 'rgba(18,14,9,0.95)', border: `2px solid ${COLORS.gold}`, opacity: Math.min(1, p * 1.5), transform: `perspective(1200px) rotateX(${(1 - Math.min(1, p)) * 60}deg)`, boxShadow: '0 20px 40px rgba(0,0,0,0.5)'}}>
								<div style={{fontSize: 96, lineHeight: 1}}>{icon}</div>
								<div style={{flex: 1, fontFamily: DISPLAY, fontSize: 60, lineHeight: 1.02, color: i === 2 ? COLORS.goldHi : '#fff'}}>{text.toUpperCase()}</div>
								<div style={{fontFamily: DISPLAY, fontSize: 64, color: COLORS.goldHi, opacity: ease(t, at + 0.5)}}>✓</div>
							</div>
						);
					})}
				</div>
			</AbsoluteFill>
			<LeoMoment m="thumbsup" at={C.people + 0.2} seconds={Math.min(1.5, C.f2 - C.people - 0.3)} style={{left: 360, top: 990, width: 360, height: 230}} accent="warm" focus="50% 8%" sound={null} />

			{/* FACT CHECK 2: the tools: many of the best have free plans */}
			<AbsoluteFill style={{opacity: f2, transform: push(t, C.f2, C.f3)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>FACT CHECK 2 · THE TOOLS</Chip>
				</div>
				<div style={{position: 'absolute', top: 386, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 86, lineHeight: 1, color: '#fff', opacity: ease(t, C.freePlans - 0.3)}}>
					MANY HAVE <span style={GOLD_TEXT}>FREE PLANS</span>
				</div>
				<div style={{position: 'absolute', top: 540, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 18}}>
					<ToolTile icon="🎨" name="Design apps" at={C.design} t={t} />
					<ToolTile icon="🤖" name="AI assistants" at={C.ai} t={t} />
					<ToolTile icon="🖼️" name="Places to show your work" at={C.places} t={t} />
				</div>
				<div style={{position: 'absolute', top: 1110, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 28, color: COLORS.muted, opacity: ease(t, C.work)}}>Free plans have limits; paid plans add more. Start free.</div>
			</AbsoluteFill>
			<LeoMoment m="smile" at={C.tools + 0.05} seconds={Math.min(1.6, C.design - C.tools - 0.4)} style={{left: 340, top: 600, width: 400, height: 340}} accent="warm" focus="50% 8%" sound={null} />

			{/* FACT CHECK 3: the real cost: a website name about $20 a year or less; the biggest cost is time */}
			<AbsoluteFill style={{opacity: f3, transform: push(t, C.f3, C.so)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>FACT CHECK 3 · THE REAL COST</Chip>
				</div>
				<div style={{position: 'absolute', left: 90, right: 90, top: 400}}>
					<Flip at={C.realCost - 0.2}>
						<div style={{padding: '30px 34px 36px', borderRadius: 18, background: 'linear-gradient(180deg, #fbf3df, #ecdcb6)', boxShadow: '0 30px 60px rgba(0,0,0,0.6)', fontFamily: MONO, color: '#2a1a05', position: 'relative'}}>
							<div style={{textAlign: 'center', fontWeight: 700, fontSize: 30, letterSpacing: 4, color: '#7a5418'}}>YOUR START-UP RECEIPT</div>
							<div style={{borderTop: '3px dashed rgba(122,84,24,0.45)', margin: '16px 0'}} />
							<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', fontWeight: 700, fontSize: 38, opacity: ease(t, C.website - 0.1)}}>
								<span>🌐 Website name</span>
								<span style={{fontFamily: DISPLAY, fontSize: 56}}>≤ $20/yr</span>
							</div>
							<div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', fontWeight: 700, fontSize: 38, marginTop: 18, opacity: ease(t, C.biggest - 0.1)}}>
								<span>⏳ Your time</span>
								<span style={{fontFamily: DISPLAY, fontSize: 56, color: '#a8661c'}}>THE BIG ONE</span>
							</div>
							<div style={{borderTop: '3px dashed rgba(122,84,24,0.45)', margin: '18px 0 0'}} />
						</div>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 760, left: 200, width: 220, textAlign: 'center', fontSize: 170, lineHeight: 1, opacity: ease(t, C.biggest - 0.1), transform: `rotate(${hourglass}deg)`}}>⏳</div>
				<div style={{position: 'absolute', top: 970, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 25, color: COLORS.muted, opacity: ease(t, C.less)}}>A .com name: about $11 to $20 a year, depending on where you buy it (Nov 2026).</div>
				<div style={{position: 'absolute', top: 1040, width: '100%', textAlign: 'center'}}>
					<HintPill icon="🔖" text="Save this checklist" size={36} t={t} at={C.time + 0.3} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.time - 0.1} seconds={Math.min(1.15, C.so - C.time - 0.05)} style={{left: 560, top: 730, width: 320, height: 220}} accent="aha" focus="50% 6%" />

			{/* THE VERDICT: mostly myth; money helps you go faster; skills and time get you started; no promises */}
			<AbsoluteFill style={{opacity: verdict, transform: push(t, C.so, C.did)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>THE VERDICT ⚖️</Chip>
				</div>
				<div style={{position: 'absolute', left: 50, right: 50, top: 386}}>
					<Claim t={t} scale={0.86} pick={t > C.mostly ? -1 : 0} stamp={stamp} />
				</div>
				<div style={{position: 'absolute', left: 70, right: 70, top: 760, display: 'flex', flexDirection: 'column', gap: 16}}>
					<div style={{display: 'flex', alignItems: 'center', gap: 18, opacity: ease(t, C.faster - 0.4), transform: `translateX(${(1 - ease(t, C.faster - 0.4, 0.5)) * -60}px)`}}>
						<span style={{fontSize: 60}}>💸</span>
						<span style={{fontFamily: DISPLAY, fontSize: 58, color: COLORS.champagne}}>MONEY → <span style={{color: '#fff'}}>GO FASTER</span></span>
					</div>
					<div style={{display: 'flex', alignItems: 'center', gap: 18, opacity: ease(t, C.skills - 0.1), transform: `translateX(${(1 - ease(t, C.skills - 0.1, 0.5)) * -60}px)`}}>
						<span style={{fontSize: 60}}>🧠</span>
						<span style={{fontFamily: DISPLAY, fontSize: 58, color: COLORS.champagne}}>SKILLS + TIME → <span style={GOLD_TEXT}>GET STARTED</span></span>
					</div>
				</div>
				<div style={{position: 'absolute', top: 960, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 34, color: COLORS.champagne, opacity: ease(t, C.results - 0.1)}}>Results take patience. No promises.</div>
			</AbsoluteFill>
			<LeoMoment m="laugh" at={C.mostly + 0.4} seconds={Math.min(1.8, C.skills - C.mostly - 0.5)} style={{left: 360, top: 990, width: 360, height: 230}} focus="50% 6%" accent="warm" sound={null} />
			<LeoMoment m="reassure" at={C.results + 0.2} seconds={Math.min(1.35, C.did - C.results - 0.3)} style={{left: 360, top: 1010, width: 360, height: 210}} accent="relief" focus="50% 8%" />

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.did} seconds={Math.min(4.2, C.send - C.did - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={38} style={{background: 'rgba(5,4,3,0.9)'}}>DID YOU BELIEVE THIS ONE? 🤔</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Myth or fact? Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: shareP}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 42, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.illStart - 0.3)}}>who says “I'll start when I have money” 💸</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />
			<LeoMoment m="wave" at={C.send + 2.2} seconds={Math.min(2.45, C.join - C.send - 2.5)} style={{left: 290, top: 540, width: 500, height: 640}} focus="50% 10%" sound={null} />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['streams', 'ai', 'tutorials', 'tools', 'tribe']} sloganWords={SLOGAN} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [C.needMoney - 0.3, 'paper', 0.3], [C.online, 'tension', 0.26], [C.pct - 0.1, 'count', 0.22], [C.notEnough, 'drop', 0.18], [C.check - 0.1, 'pluck2', 0.28],
					[C.f1 - 0.15, 'air', 0.26], [C.phone - 0.15, 'pluck1', 0.3], [C.internet - 0.15, 'pluck2', 0.3], [C.skill - 0.15, 'pluck3', 0.3], [C.people, 'tickbox', 0.36],
					[C.f2 - 0.15, 'air', 0.26], [C.freePlans - 0.3, 'shimmer', 0.3], [C.design + 0.15, 'pricetag', 0.45], [C.ai + 0.15, 'pricetag', 0.45], [C.places + 0.15, 'pricetag', 0.45],
					[C.f3 - 0.15, 'air', 0.26], [C.realCost - 0.2, 'paper', 0.32], [C.website - 0.1, 'typing', 0.3], [C.biggest - 0.1, 'clock', 0.26],
					[C.so - 0.15, 'tension', 0.24], [C.mostly - 0.05, 'stamp', 0.5], [C.mostly + 0.15, 'verdict', 0.4], [C.faster - 0.4, 'pluck1', 0.28], [C.skills - 0.1, 'pluck4', 0.3],
					[C.did, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/14/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover14: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={48}>MYTH OR FACT? 🤔</Chip>
		</div>
		<div style={{position: 'absolute', top: 372, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 132, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>YOU NEED MONEY</div>
		<div style={{position: 'absolute', top: 506, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 132, lineHeight: 1.0, ...GOLD_TEXT}}>TO MAKE MONEY</div>
		<div style={{position: 'absolute', top: 640, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 100, lineHeight: 1.0, color: '#fff'}}>ONLINE?</div>
		<div style={{position: 'absolute', left: 80, top: 800, display: 'flex', flexDirection: 'column', gap: 30}}>
			{['MYTH', 'FACT'].map((label) => (
				<div key={label} style={{width: 420, padding: '26px 0', textAlign: 'center', borderRadius: 999, fontFamily: DISPLAY, fontSize: 92, lineHeight: 1, color: '#2a1a05', background: GOLD_FILL, boxShadow: '0 0 40px rgba(242,173,60,0.5)'}}>{label}</div>
			))}
			<div style={{width: 420, textAlign: 'center', fontFamily: DISPLAY, fontSize: 64, lineHeight: 1, color: COLORS.champagne}}>WHICH ONE? 👇</div>
		</div>
		<div style={{position: 'absolute', top: 780, left: 560, width: 440, height: 500, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V5-think.png')} style={{width: 440, height: 770, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1340, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.champagne}}>3 fact checks · an honest answer</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

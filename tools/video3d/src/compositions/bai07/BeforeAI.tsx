import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/07/captions.json';
import C from '../../../public/videos/07/cues.json';
import timeline from '../../../public/videos/07/timeline.json';
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

// Video 07 (12 Nov 2026, daily video): Before You Try to Make Money With AI, Do These 3 Things. The first AI video.
// Calm and encouraging, no income promises. Script and research: tools/videos/07-before-you-make-money-with-ai/.
// Every time is a named cue from the voice's own word timings (public/videos/07/cues.json).
// Facts on screen: 900 million weekly ChatGPT users (OpenAI, 27 February 2026); "AI can make mistakes: check
// important info" (the line under ChatGPT's message box).

export const BAI07_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const BAI07_FRAMES = Math.ceil((timeline.total + TAIL) * BAI07_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const AMBER = '#e8954a';
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};

/** The numbered step header: a round number and a title. */
const Step: React.FC<{n: string; title: string; at: number}> = ({n, title, at}) => {
	const p = usePop(at, 13);
	return (
		<div style={{position: 'absolute', top: 285, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * -30}px)`}}>
			<div style={{width: 104, height: 104, borderRadius: '50%', background: GOLD_FILL, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 70, color: '#2a1a05', boxShadow: '0 12px 30px rgba(0,0,0,0.55)', transform: `rotate(${(1 - p) * -180}deg)`}}>{n}</div>
			<div style={{fontFamily: DISPLAY, fontSize: 72, lineHeight: 1, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>{title}</div>
		</div>
	);
};

/** One line of the brief that types itself: a gold label, then the words. */
const BriefLine: React.FC<{t: number; at: number; label: string; text: string}> = ({t, at, label, text}) => {
	const p = interpolate(t, [at, at + 0.2 + text.length * 0.022], [0, 1], clamp);
	return (
		<div style={{marginBottom: 22, minHeight: 92}}>
			<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 2, color: COLORS.goldHi, opacity: 0.4 + 0.6 * ease(t, at - 0.1, 0.2)}}>{label}</div>
			<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 38, lineHeight: 1.25, color: COLORS.text, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`}}>{text}</div>
		</div>
	);
};

export const BeforeAI: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.one - 0.3, 0.3);
	const one = win(t, C.one - 0.15, C.two - 0.3, 0.3);
	const two = win(t, C.two - 0.15, C.three - 0.3, 0.3);
	const three = win(t, C.three - 0.15, C.small - 0.3, 0.3);
	const small = win(t, C.small - 0.15, C.q - 0.3, 0.3);
	const ask = win(t, C.q - 0.1, C.send - 0.15, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const users = Math.round(interpolate(t, [C.hook, C.people + 0.5], [0, 900], outCubic)) * 1_000_000;
	const coinIn = interpolate(t, [0.1, 1.4], [-540, 0], outCubic);
	const toolBack = ease(t, C.notTool, 0.4);
	const fix = ease(t, C.wrong + 0.35, 0.35);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: 900 million people use ChatGPT every week; before you try to make money with AI, 3 things */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.one)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={38}>BEFORE YOU MAKE MONEY WITH AI</Chip>
				</div>
				<div style={{position: 'absolute', left: 540 - 130, top: 384, opacity: ease(t, 0.1, 0.4)}}>
					<Coin3D size={260} symbol="AI" rotY={coinIn + Math.sin(t * 1.5) * 16} rotX={8} glow={0.6} />
				</div>
				<div style={{position: 'absolute', top: 664, width: '100%', textAlign: 'center', opacity: ease(t, C.hook, 0.25)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 138, lineHeight: 1, ...GOLD_TEXT}}>{users.toLocaleString('en-US')}</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text, marginTop: 6, opacity: ease(t, C.people)}}>people use ChatGPT every week</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, marginTop: 4, opacity: ease(t, C.week - 0.3)}}>OpenAI, February 2026</div>
				</div>
				<div style={{position: 'absolute', top: 936, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 64, lineHeight: 1, color: '#fff', opacity: ease(t, C.things - 0.5)}}>DO THESE <span style={GOLD_TEXT}>3 THINGS</span> FIRST</div>
				<div style={{position: 'absolute', top: 1030, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 20, opacity: ease(t, C.things - 0.2, 0.25)}}>
					{['1', '2', '3'].map((n, i) => {
						const hot = i === 1 ? ease(t, C.n2, 0.3) : 0;
						return (
							<div key={n} style={{width: 100, height: 100, borderRadius: '50%', background: hot > 0.5 ? GOLD_FILL : 'rgba(18,14,9,0.9)', border: `3px solid ${COLORS.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 60, color: hot > 0.5 ? '#2a1a05' : COLORS.goldHi, transform: `scale(${1 + 0.16 * hot + 0.04 * hot * Math.sin((t - C.n2) * 8)})`, boxShadow: `0 0 ${40 * hot}px rgba(242,173,60,0.7)`}}>{n}</div>
						);
					})}
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, color: COLORS.goldHi, marginLeft: 8, opacity: ease(t, C.apart - 0.5)}}>⭐ the skill that<br />sets you apart</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.people + 0.3} seconds={Math.min(1.8, C.before - C.people - 0.1)} style={{left: 730, top: 396, width: 300, height: 250}} accent="wow" sound={null} />

			{/* ONE: start with a problem, not a tool */}
			<AbsoluteFill style={{opacity: one, transform: push(t, C.one, C.two)}}>
				<Step n="1" title="A PROBLEM, NOT A TOOL" at={C.one} />
				<div style={{position: 'absolute', top: 440, left: 60, right: 60, display: 'flex', gap: 30}}>
					<div style={{flex: 1, opacity: ease(t, C.one + 0.3) * (1 - 0.6 * toolBack), transform: `scale(${1 - 0.1 * toolBack}) translateY(${toolBack * 16}px)`}}>
						<Panel style={{height: 300, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10, boxSizing: 'border-box'}}>
							<div style={{fontSize: 110, lineHeight: 1}}>🛠️</div>
							<div style={{fontFamily: DISPLAY, fontSize: 52, color: '#fff'}}>THE TOOL</div>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.muted, opacity: toolBack}}>comes second</div>
						</Panel>
					</div>
					<div style={{flex: 1, opacity: ease(t, C.problem - 0.15), transform: `scale(${interpolate(usePop(C.problem - 0.15, 12), [0, 1], [0.8, 1]) + 0.04 * toolBack})`}}>
						<Panel style={{height: 300, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10, boxSizing: 'border-box', borderColor: COLORS.goldHi, boxShadow: `0 0 ${50 * toolBack}px rgba(242,173,60,0.45)`}}>
							<div style={{fontSize: 110, lineHeight: 1}}>🙋</div>
							<div style={{fontFamily: DISPLAY, fontSize: 52, ...GOLD_TEXT}}>A PROBLEM</div>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.champagne, opacity: toolBack}}>comes first</div>
						</Panel>
					</div>
				</div>
				<div style={{position: 'absolute', top: 800, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 70, lineHeight: 1, color: '#fff', opacity: ease(t, C.who)}}>WHO DO YOU WANT TO <span style={GOLD_TEXT}>HELP?</span></div>
				<div style={{position: 'absolute', top: 910, left: 40, right: 40, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
					<HintPill icon="💇" text="A caption for a salon" size={44} t={t} at={C.caption - 0.1} />
					<HintPill icon="📄" text="A CV for a job seeker" size={44} t={t} at={C.cv - 0.1} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.who + 0.1} seconds={Math.min(2.4, C.cv - C.who - 0.2)} style={{left: 60, top: 440, width: 465, height: 300}} />

			{/* TWO: brief AI like a new assistant: who it's for, what you want, how it should sound */}
			<AbsoluteFill style={{opacity: two, transform: push(t, C.two, C.three)}}>
				<Step n="2" title="BRIEF IT WELL" at={C.two} />
				<div style={{position: 'absolute', top: 408, width: '100%', textAlign: 'center', opacity: ease(t, C.assistant - 0.3)}}>
					<Chip size={34}>🧑‍💼 LIKE A NEW ASSISTANT</Chip>
				</div>
				<div style={{position: 'absolute', left: 410, right: 50, top: 500}}>
					<Flip at={C.brief - 0.1}>
						<Panel style={{padding: '26px 30px 8px', background: 'rgba(18,14,9,0.96)'}}>
							<BriefLine t={t} at={C.whoFor} label="WHO IT'S FOR" text="Customers of a hair salon" />
							<BriefLine t={t} at={C.what} label="WHAT YOU WANT" text="3 short captions for a weekend special" />
							<BriefLine t={t} at={C.how} label="HOW IT SHOULD SOUND" text="Warm and friendly, one emoji" />
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 990, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 16}}>
					<HintPill icon="✍️" text="Clear in" size={42} t={t} at={C.clear} />
					<div style={{fontFamily: DISPLAY, fontSize: 60, color: COLORS.gold, opacity: ease(t, C.useful - 0.25)}}>➜</div>
					<HintPill icon="✨" text="Useful out" size={42} t={t} at={C.useful - 0.1} />
				</div>
				<div style={{position: 'absolute', top: 1110, width: '100%', textAlign: 'center', opacity: ease(t, C.useful + 0.5)}}>
					<Chip size={32} style={{borderColor: COLORS.goldHi}}>🔖 SAVE THIS: WHO • WHAT • HOW</Chip>
				</div>
			</AbsoluteFill>
			<LeoMoment m="present" at={C.assistant - 0.5} seconds={Math.min(4.0, C.clear - C.assistant - 0.3)} style={{left: 50, top: 520, width: 330, height: 340}} focus="50% 30%" sound={null} />
			<LeoMoment m="aha" at={C.useful - 0.1} seconds={Math.min(1.15, C.three - C.useful - 0.3)} style={{left: 50, top: 520, width: 330, height: 400}} accent="aha" focus="50% 8%" sound={null} />

			{/* THREE: check its work; AI can sound sure and still be wrong; you are the editor */}
			<AbsoluteFill style={{opacity: three, transform: push(t, C.three, C.small)}}>
				<Step n="3" title="CHECK ITS WORK" at={C.three} />
				<div style={{position: 'absolute', left: 60, top: 440, width: 620}}>
					<Flip at={C.check - 0.2}>
						<Panel style={{padding: '24px 28px', background: 'rgba(18,14,9,0.96)'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 2, color: COLORS.goldHi}}>✨ AI'S DRAFT</div>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 34, lineHeight: 1.3, color: COLORS.text, marginTop: 12}}>Weekend special at the salon! 💇</div>
							<div style={{position: 'relative', marginTop: 12, padding: '8px 12px', borderRadius: 12, background: `rgba(232,149,74,${0.22 * ease(t, C.sure, 0.3) * (1 - fix)})`, border: `2px solid rgba(232,149,74,${ease(t, C.sure, 0.3) * (1 - fix)})`}}>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 34, lineHeight: 1.3, color: COLORS.text, opacity: 1 - fix}}>Open Monday to Sunday</div>
								<div style={{position: 'absolute', left: 12, top: 8, fontFamily: BODY, fontWeight: 800, fontSize: 34, lineHeight: 1.3, color: COLORS.goldHi, opacity: fix}}>Open Tuesday to Saturday ✓</div>
							</div>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 34, lineHeight: 1.3, color: COLORS.text, marginTop: 12}}>Book your spot today.</div>
						</Panel>
					</Flip>
					<div style={{position: 'absolute', right: -36, top: 150, fontSize: 110, opacity: win(t, C.sure - 0.1, C.editor + 0.6, 0.25), transform: `translate(${interpolate(t, [C.sure - 0.1, C.wrong], [-260, 0], outCubic)}px, ${Math.sin(t * 5) * 5}px)`}}>🔍</div>
				</div>
				<div style={{position: 'absolute', left: 60, width: 620, top: 800, textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 32, color: AMBER, opacity: win(t, C.sure, C.wrong + 0.3, 0.2)}}>sounds sure… is it right?</div>
				<div style={{position: 'absolute', top: 900, width: '100%', textAlign: 'center', opacity: ease(t, C.editor - 0.6, 0.2), transform: `scale(${interpolate(usePop(C.editor - 0.6, 11), [0, 1], [1.5, 1])})`}}>
					<span style={{display: 'inline-block', transform: 'rotate(-4deg)', border: `7px solid ${COLORS.gold}`, color: COLORS.goldHi, fontFamily: DISPLAY, fontSize: 86, lineHeight: 1.2, padding: '0 30px', borderRadius: 14, background: 'rgba(5,4,3,0.82)'}}>YOU ARE THE EDITOR ✍️</span>
				</div>
				<div style={{position: 'absolute', top: 1090, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, opacity: ease(t, C.wrong)}}>AI can make mistakes: check important info.</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.editor - 0.5} seconds={Math.min(1.35, C.small - C.editor + 0.2)} style={{left: 716, top: 440, width: 320, height: 400}} accent="relief" focus="50% 10%" />

			{/* START SMALL: one problem, one person, this week */}
			<AbsoluteFill style={{opacity: small, transform: push(t, C.small, C.q)}}>
				<div style={{position: 'absolute', top: 296, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 124, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, C.small - 0.05), transform: `scale(${interpolate(usePop(C.small - 0.05, 12), [0, 1], [0.8, 1])})`}}>START SMALL</div>
				<div style={{position: 'absolute', top: 470, left: 60, width: 480, display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 18}}>
					<HintPill icon="🎯" text="One problem" size={46} t={t} at={C.oneProblem - 0.1} />
					<HintPill icon="🙋" text="One person" size={46} t={t} at={C.onePerson - 0.1} />
					<HintPill icon="📅" text="This week" size={46} t={t} at={C.thisWeek - 0.1} />
				</div>
				<div style={{position: 'absolute', left: 540, top: 480, opacity: ease(t, C.small + 0.2)}}>
					<Laptop3D w={480} open={interpolate(t, [C.small + 0.3, C.small + 1.3], [0, 1], outCubic)}>
						<div style={{width: '86%'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 20, color: COLORS.goldHi, letterSpacing: 2}}>MY FIRST BRIEF</div>
							{[0.9, 0.7, 0.8].map((w, i) => <div key={i} style={{marginTop: 10, height: 10, borderRadius: 5, width: `${w * interpolate(t, [C.oneProblem + i * 0.5, C.oneProblem + 0.6 + i * 0.5], [0, 100], clamp)}%`, background: i === 0 ? COLORS.gold : 'rgba(255,255,255,0.3)'}} />)}
						</div>
					</Laptop3D>
				</div>
				<div style={{position: 'absolute', top: 1170, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, opacity: ease(t, C.onePerson)}}>No promises: practice builds the skill.</div>
			</AbsoluteFill>
			<LeoMoment m="thumbsup" at={C.onePerson} seconds={Math.min(1.5, C.q - C.onePerson - 0.4)} style={{left: 90, top: 800, width: 380, height: 350}} focus="50% 10%" sound="pluck3" volume={0.3} />

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.q} seconds={Math.min(4.2, C.send - C.q - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={38} style={{background: 'rgba(5,4,3,0.9)'}}>WHICH ONE WILL YOU TRY FIRST? 💬</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="1, 2 or 3? Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 46, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.curious - 0.4)}}>who's curious about AI 🤖</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'ai', 'streams', 'tutorials', 'tribe']} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [1.1, 'coin', 0.28], [C.hook, 'count', 0.2], [C.people + 0.3, 'reveal', 0.35], [C.things - 0.5, 'pluck1', 0.3], [C.n2, 'chime', 0.34],
					[C.one, 'pluck1', 0.34], [C.problem - 0.15, 'reveal', 0.35], [C.notTool, 'drop', 0.26], [C.who, 'pluck2', 0.3], [C.caption - 0.1, 'pluck3', 0.32], [C.cv - 0.1, 'pluck3', 0.32],
					[C.two, 'pluck2', 0.34], [C.assistant - 0.3, 'pluck1', 0.28], [C.whoFor, 'typing', 0.42], [C.what, 'typing', 0.42], [C.how, 'typing', 0.42], [C.clear, 'pluck1', 0.3], [C.useful - 0.1, 'shimmer', 0.45],
					[C.three, 'pluck3', 0.34], [C.check - 0.2, 'paper', 0.35], [C.sure, 'tick', 0.28], [C.wrong + 0.35, 'scribble', 0.4], [C.editor - 0.6, 'reveal', 0.38],
					[C.small - 0.05, 'glow', 0.32], [C.small + 0.3, 'laptop', 0.4], [C.oneProblem - 0.1, 'pluck1', 0.3], [C.onePerson - 0.1, 'pluck2', 0.3],
					[C.q, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/07/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover07: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>BEFORE YOU START</Chip>
		</div>
		<div style={{position: 'absolute', top: 372, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 138, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
			MAKE MONEY<br /><span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>WITH AI?</span>
		</div>
		<div style={{position: 'absolute', left: 80, top: 700}}>
			<Coin3D size={360} symbol="AI" rotY={-26} rotX={8} glow={0.6} />
		</div>
		<div style={{position: 'absolute', top: 690, left: 580, width: 440, height: 480, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V7-point.png')} style={{width: 440, height: 770, objectFit: 'cover', objectPosition: '40% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1200, width: '100%', textAlign: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 124, lineHeight: 1, ...GOLD_TEXT}}>DO THESE 3 THINGS</div>
			<div style={{fontFamily: DISPLAY, fontSize: 124, lineHeight: 1.05, color: '#fff'}}>FIRST</div>
		</div>
		<div style={{position: 'absolute', top: 1480, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={180} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

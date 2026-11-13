import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/08/captions.json';
import C from '../../../public/videos/08/cues.json';
import timeline from '../../../public/videos/08/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {EndScreen} from '../../components/EndScreen';
import {LeoMoment} from '../../components/Leo';
import {PhotoCard} from '../../components/PhotoCard';
import {HintPill, UrlPill} from '../../components/Pills';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Coin3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 08 (13 Nov 2026, daily video): The Story of the Two Pizzas That Cost 10,000 Bitcoin. A warm, fun story with a
// real lesson; no regret, no pressure. Script and research: tools/videos/08-story-of-the-bitcoin-pizzas/.
// Every time is a named cue from the voice's own word timings (public/videos/08/cues.json).
// Facts on screen: Laszlo's forum post of 18 May 2010 (word for word), the purchase on 22 May 2010, about $41 then,
// about $710 million at about $71,000 per Bitcoin on 13 November 2026, his words to CBS in 2019.

export const SOP08_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const SOP08_FRAMES = Math.ceil((timeline.total + TAIL) * SOP08_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};
const outBack = {...clamp, easing: Easing.out(Easing.back(1.3))};

/** A pizza, seen from above (an original drawing): crust, sauce, cheese, toppings, cut into eight. */
const Pizza: React.FC<{size: number; rot?: number}> = ({size, rot = 0}) => {
	const tops: Array<[number, number]> = [[62, 58], [118, 52], [150, 96], [128, 142], [74, 148], [48, 104], [98, 100], [100, 66], [136, 120]];
	const greens: Array<[number, number, number]> = [[84, 78, 20], [128, 80, -30], [70, 122, 50], [112, 128, 10], [146, 72, 70], [56, 80, -50]];
	return (
		<svg width={size} height={size} viewBox="0 0 200 200" style={{transform: `rotate(${rot}deg)`, filter: 'drop-shadow(0 18px 22px rgba(0,0,0,0.55))'}}>
			<defs>
				<radialGradient id="p08crust" cx="0.5" cy="0.5" r="0.5">
					<stop offset="0.8" stopColor="#d9a04a" />
					<stop offset="1" stopColor="#a8691f" />
				</radialGradient>
				<radialGradient id="p08cheese" cx="0.42" cy="0.38" r="0.7">
					<stop offset="0" stopColor="#ffe08a" />
					<stop offset="1" stopColor="#f0b63c" />
				</radialGradient>
			</defs>
			<circle cx="100" cy="100" r="98" fill="url(#p08crust)" />
			<circle cx="100" cy="100" r="84" fill="#b5432a" />
			<circle cx="100" cy="100" r="79" fill="url(#p08cheese)" />
			{[0, 45, 90, 135].map((d) => <line key={d} x1="100" y1="6" x2="100" y2="194" stroke="rgba(150,90,20,0.45)" strokeWidth="2" transform={`rotate(${d} 100 100)`} />)}
			{tops.map(([x, y], i) => (
				<g key={i}>
					<circle cx={x} cy={y} r="13" fill="#a3301f" />
					<circle cx={x - 3} cy={y - 3} r="4" fill="#c4513c" />
				</g>
			))}
			{greens.map(([x, y, r], i) => <rect key={i} x={x} y={y} width="16" height="5" rx="2.5" fill="#4d8a3a" transform={`rotate(${r} ${x + 8} ${y + 2})`} />)}
		</svg>
	);
};

const Avatar: React.FC<{label: string; size?: number; gold?: boolean}> = ({label, size = 130, gold}) => (
	<div style={{width: size, height: size, borderRadius: '50%', background: gold ? GOLD_FILL : 'linear-gradient(145deg, #3a3024, #1c1610)', border: `3px solid ${COLORS.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: size * 0.46, color: gold ? '#2a1a05' : COLORS.goldHi, boxShadow: '0 12px 30px rgba(0,0,0,0.5)'}}>{label}</div>
);

export const PizzaStory: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.his - 0.3, 0.3);
	const post = win(t, C.his - 0.15, C.four - 0.3, 0.3);
	const deal = win(t, C.four - 0.15, C.back - 0.3, 0.3);
	const value = win(t, C.back - 0.15, C.but - 0.3, 0.3);
	const lesson = win(t, C.but - 0.15, C.would - 0.3, 0.3);
	const ask = win(t, C.would - 0.1, C.send - 0.15, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const coins = Math.round(interpolate(t, [C.tenK, C.tenK + 0.9], [0, 10000], outCubic));
	const pizzaIn = (k: number) => interpolate(t, [C.pizzas - 0.2 + k * 0.18, C.pizzas + 0.4 + k * 0.18], [0, 1], outBack);
	const quote = "I'll pay 10,000 bitcoins for a couple of pizzas..";
	const typed = interpolate(t, [C.illPay, C.couple + 0.9], [0, quote.length], clamp);
	const swap = interpolate(t, [C.took, C.took + 0.9], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const arrive = (k: number) => interpolate(t, [C.arrived - 0.25 + k * 0.15, C.arrived + 0.35 + k * 0.15], [0, 1], outBack);
	const now = interpolate(t, [C.seven, C.seven + 1.0], [0, 710], outCubic);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: in 2010 a man paid 10,000 Bitcoin for two pizzas, and that dinner made history */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.his)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={40}>THE STORY OF 2 PIZZAS 🍕</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, left: 60, right: 60, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 26, opacity: ease(t, C.paid, 0.25)}}>
					<Coin3D size={190} rotY={interpolate(t, [C.paid, C.paid + 1.2], [-360, 0], outCubic) + Math.sin(t * 1.6) * 14} rotX={8} glow={0.6} />
					<div>
						<div style={{fontFamily: DISPLAY, fontSize: 176, lineHeight: 1, ...GOLD_TEXT}}>{coins.toLocaleString('en-US')}</div>
						<div style={{fontFamily: DISPLAY, fontSize: 64, lineHeight: 1, color: '#fff'}}>BITCOIN</div>
					</div>
				</div>
				<div style={{position: 'absolute', top: 672, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 72, color: COLORS.champagne, opacity: ease(t, C.pizzas - 0.3)}}>FOR</div>
				<div style={{position: 'absolute', top: 760, left: 0, right: 0, height: 330}}>
					<div style={{position: 'absolute', left: 190, top: 0, opacity: Math.min(1, pizzaIn(0) * 1.5), transform: `translateX(${(1 - pizzaIn(0)) * -500}px)`}}>
						<Pizza size={330} rot={pizzaIn(0) * 200 + t * 6} />
					</div>
					<div style={{position: 'absolute', left: 560, top: 0, opacity: Math.min(1, pizzaIn(1) * 1.5), transform: `translateX(${(1 - pizzaIn(1)) * 500}px)`}}>
						<Pizza size={330} rot={-pizzaIn(1) * 200 - t * 6 + 20} />
					</div>
				</div>
				<div style={{position: 'absolute', top: 1124, width: '100%', textAlign: 'center', opacity: ease(t, C.history - 0.3), transform: `scale(${interpolate(usePop(C.history - 0.3, 12), [0, 1], [0.75, 1])})`}}>
					<Chip size={42} style={{borderColor: COLORS.goldHi, boxShadow: '0 0 34px rgba(242,173,60,0.4)'}}>AND THAT DINNER MADE HISTORY</Chip>
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.tenK + 0.5} seconds={Math.min(1.8, C.dinner - C.tenK - 0.5)} style={{left: 730, top: 600, width: 300, height: 190}} accent="wow" sound={null} />

			{/* LASZLO'S POST: Bitcoin was a year old; people mined it, hardly anyone spent it; so he posted online */}
			<AbsoluteFill style={{opacity: post, transform: push(t, C.his, C.four)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, C.his)}}>
					<Chip size={40}>2010: BITCOIN IS 1 YEAR OLD</Chip>
				</div>
				{/* first: who he is, how young Bitcoin was, what people did with it */}
				<AbsoluteFill style={{opacity: fadeOut(t, C.posted - 0.35, 0.3)}}>
					<div style={{position: 'absolute', top: 410, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 30, opacity: ease(t, C.his + 0.1), transform: `translateY(${(1 - ease(t, C.his + 0.1, 0.5)) * 40}px)`}}>
						<Avatar label="L" size={170} gold />
						<div>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.champagne}}>His name is</div>
							<div style={{fontFamily: DISPLAY, fontSize: 130, lineHeight: 1, ...GOLD_TEXT}}>LASZLO</div>
						</div>
					</div>
					<div style={{position: 'absolute', top: 650, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 26, opacity: ease(t, C.barely)}}>
						<Coin3D size={170} rotY={interpolate(t, [C.barely, C.barely + 1.0], [-300, 0], outCubic) + Math.sin(t * 1.6) * 14} rotX={8} glow={0.5} />
						<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.02, color: '#fff'}}>BARELY<br /><span style={GOLD_TEXT}>1 YEAR OLD 🎂</span></div>
					</div>
					<div style={{position: 'absolute', top: 900, left: 40, right: 40, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18}}>
						<HintPill icon="⛏️" text="People mined it" size={44} t={t} at={C.mined - 0.1} />
						<HintPill icon="🛒" text="Hardly anyone had spent it" size={44} t={t} at={C.spent - 0.1} />
					</div>
				</AbsoluteFill>
				<div style={{position: 'absolute', left: 400, right: 50, top: 440}}>
					<Flip at={C.posted - 0.15}>
						<Panel style={{padding: '24px 28px', background: 'rgba(18,14,9,0.97)'}}>
							<div style={{display: 'flex', alignItems: 'center', gap: 16}}>
								<Avatar label="L" size={78} gold />
								<div>
									<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, color: COLORS.text}}>laszlo</div>
									<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 24, color: COLORS.muted}}>Bitcoin Forum · 18 May 2010</div>
								</div>
							</div>
							<div style={{marginTop: 18, minHeight: 280, fontFamily: BODY, fontWeight: 800, fontSize: 46, lineHeight: 1.25, color: COLORS.text}}>
								“{quote.slice(0, Math.round(typed))}
								{typed >= quote.length ? '”' : <span style={{color: COLORS.gold}}>▍</span>}
							</div>
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 960, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.champagne, opacity: ease(t, C.couple + 0.9)}}>His real post, word for word (Laszlo Hanyecz)</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.posted - 0.1} seconds={Math.min(3.6, C.four - C.posted - 0.4)} style={{left: 50, top: 460, width: 320, height: 440}} focus="50% 12%" />

			{/* THE DEAL: four days later a 19-year-old took it, and two pizzas arrived: 22 May 2010, Bitcoin Pizza Day */}
			<AbsoluteFill style={{opacity: deal, transform: push(t, C.four, C.back)}}>
				<div style={{position: 'absolute', top: 290, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 14}}>
					{[18, 19, 20, 21, 22].map((d, i) => {
						const p = usePop(C.four + i * 0.14, 12);
						const last = i === 4;
						return (
							<div key={d} style={{width: 150, height: 150, borderRadius: 22, background: last ? GOLD_FILL : 'rgba(18,14,9,0.92)', border: `3px solid ${COLORS.gold}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: Math.min(1, p * 1.5), transform: `scale(${0.6 + 0.4 * p})`, boxShadow: last ? '0 0 36px rgba(242,173,60,0.5)' : 'none'}}>
								<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, color: last ? '#5a3b10' : COLORS.muted}}>MAY</div>
								<div style={{fontFamily: DISPLAY, fontSize: 76, lineHeight: 1, color: last ? '#2a1a05' : COLORS.goldHi}}>{d}</div>
							</div>
						);
					})}
				</div>
				<div style={{position: 'absolute', top: 500, left: 70, right: 70, height: 300, opacity: ease(t, C.nineteen - 0.1)}}>
					<div style={{position: 'absolute', left: 0, top: 30, textAlign: 'center', width: 190}}>
						<Avatar label="L" size={150} gold />
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 32, color: COLORS.text, marginTop: 10}}>Laszlo</div>
					</div>
					<div style={{position: 'absolute', right: 0, top: 30, textAlign: 'center', width: 190}}>
						<div style={{display: 'flex', justifyContent: 'center'}}><Avatar label="19" size={150} /></div>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 32, color: COLORS.text, marginTop: 10}}>age 19</div>
					</div>
					<div style={{position: 'absolute', left: 200 + swap * 400, top: 10, opacity: Math.min(ease(t, C.took - 0.1, 0.2), 1)}}>
						<Coin3D size={120} rotY={swap * 540} glow={0.7} />
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, color: COLORS.goldHi, textAlign: 'center'}}>10,000 ₿</div>
					</div>
					<div style={{position: 'absolute', left: 620 - swap * 400, top: 150, opacity: Math.min(ease(t, C.took - 0.1, 0.2), 1)}}>
						<Pizza size={120} rot={swap * -300} />
					</div>
				</div>
				<div style={{position: 'absolute', top: 820, left: 0, right: 0, height: 250}}>
					<div style={{position: 'absolute', left: 120, top: 0, opacity: Math.min(1, arrive(0) * 1.5), transform: `translateY(${(1 - arrive(0)) * 200}px)`}}><Pizza size={240} rot={10} /></div>
					<div style={{position: 'absolute', left: 330, top: 10, opacity: Math.min(1, arrive(1) * 1.5), transform: `translateY(${(1 - arrive(1)) * 200}px)`}}><Pizza size={240} rot={70} /></div>
				</div>
				<div style={{position: 'absolute', top: 1092, width: '100%', textAlign: 'center', opacity: ease(t, C.date, 0.2), transform: `scale(${interpolate(usePop(C.date, 11), [0, 1], [1.4, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1, ...GOLD_TEXT}}>22 MAY 2010</span>
					<span style={{fontFamily: DISPLAY, fontSize: 56, lineHeight: 1, color: '#fff', marginLeft: 20, opacity: ease(t, C.pizzaDay - 0.2)}}>BITCOIN PIZZA DAY 🍕</span>
				</div>
			</AbsoluteFill>
			<LeoMoment m="laugh" at={C.arrived + 0.25} seconds={Math.min(2.3, C.today - C.arrived - 0.1)} style={{left: 640, top: 800, width: 380, height: 270}} focus="50% 6%" accent="warm" sound={null} />

			{/* THEN AND NOW: about $41 then; about $700 million at today's price */}
			<AbsoluteFill style={{opacity: value, transform: push(t, C.back, C.but)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, C.back)}}>
					<Chip size={40}>10,000 BITCOIN: THEN AND NOW</Chip>
				</div>
				<div style={{position: 'absolute', top: 410, left: 70, right: 70, display: 'flex', gap: 26}}>
					<div style={{flex: 1}}>
						<Flip at={C.back + 0.2}>
							<Panel style={{padding: '22px 20px', textAlign: 'center'}}>
								<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 2, color: COLORS.muted}}>MAY 2010</div>
								<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.fortyOne - 0.1)}}>$41</div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 28, color: COLORS.champagne}}>about 2 pizzas</div>
							</Panel>
						</Flip>
					</div>
					<div style={{flex: 1.5}}>
						<Flip at={C.atToday - 0.1}>
							<Panel style={{padding: '22px 20px', textAlign: 'center', borderColor: COLORS.goldHi, boxShadow: `0 0 ${50 * ease(t, C.seven, 0.6)}px rgba(242,173,60,0.4)`}}>
								<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 2, color: COLORS.goldHi}}>13 NOV 2026</div>
								<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1.05, ...GOLD_TEXT, opacity: ease(t, C.seven - 0.1, 0.2)}}>${Math.round(now)}M</div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 28, color: COLORS.champagne}}>about $710 million</div>
							</Panel>
						</Flip>
					</div>
				</div>
				<div style={{position: 'absolute', top: 760, left: 80, right: 80, textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 28, lineHeight: 1.35, color: COLORS.muted, opacity: ease(t, C.seven + 0.3)}}>10,000 BTC at about $71,000 each, on 13 November 2026.</div>
				<div style={{position: 'absolute', top: 1130, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.champagne, opacity: ease(t, C.seven + 0.6)}}>Prices move. The past promises nothing about the future.</div>
			</AbsoluteFill>
			<LeoMoment m="mindblown" at={C.seven + 0.25} seconds={Math.min(2.0, C.but - C.seven - 0.55)} style={{left: 330, top: 830, width: 420, height: 280}} focus="50% 4%" />

			{/* THE LESSON: it made Bitcoin real; money becomes money when people start using it */}
			<AbsoluteFill style={{opacity: lesson, transform: push(t, C.but, C.would)}}>
				<div style={{position: 'absolute', left: 70, right: 70, top: 300}}>
					<Flip at={C.but + 0.1}>
						<Panel style={{padding: '26px 32px', background: 'rgba(18,14,9,0.97)'}}>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 46, lineHeight: 1.25, color: COLORS.text}}>“…made <span style={{color: COLORS.goldHi}}>[Bitcoin] real</span> for some people. It certainly did for me.”</div>
							<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, marginTop: 14}}>Laszlo Hanyecz, CBS interview, 2019</div>
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 690, width: '100%', textAlign: 'center', opacity: ease(t, C.lesson)}}>
					<Chip size={38}>💡 THE LESSON</Chip>
				</div>
				<div style={{position: 'absolute', top: 780, left: 40, right: 40, textAlign: 'center', fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.06, color: '#fff', opacity: ease(t, C.money - 0.1), textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
					MONEY BECOMES MONEY<br /><span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))', opacity: ease(t, C.using - 0.5)}}>WHEN PEOPLE USE IT</span>
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.using - 0.2} seconds={Math.min(1.15, C.would - C.using - 0.2)} style={{left: 340, top: 990, width: 400, height: 240}} accent="aha" focus="50% 6%" />

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.would} seconds={Math.min(4.2, C.send - C.would - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={40} style={{background: 'rgba(5,4,3,0.9)'}}>THE PIZZAS 🍕 OR THE COINS 🪙?</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 46, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.loves - 0.4)}}>who loves pizza 🍕</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'ai', 'streams', 'tutorials', 'tribe']} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [C.paid, 'coin', 0.32], [C.tenK, 'count', 0.2], [C.tenK + 0.5, 'reveal', 0.32], [C.pizzas - 0.2, 'slide', 0.4], [C.pizzas, 'slide', 0.34], [C.history - 0.3, 'chime', 0.34],
					[C.his, 'pluck1', 0.32], [C.barely, 'coin', 0.3], [C.mined - 0.1, 'pluck2', 0.3], [C.spent - 0.1, 'pluck3', 0.3], [C.posted - 0.15, 'paper', 0.35], [C.illPay, 'typing', 0.42], [C.illPay + 1.2, 'typing', 0.42], [C.couple + 0.3, 'typing', 0.36],
					[C.four, 'count', 0.2], [C.nineteen - 0.1, 'pluck2', 0.3], [C.took, 'swell', 0.3], [C.took + 0.8, 'coin', 0.35], [C.arrived - 0.25, 'doorbell', 0.5], [C.arrived + 0.1, 'slide', 0.3], [C.date, 'reveal', 0.38], [C.pizzaDay - 0.2, 'chime', 0.32],
					[C.back, 'pluck1', 0.32], [C.fortyOne - 0.1, 'tick', 0.28], [C.atToday - 0.1, 'paper', 0.3], [C.seven, 'swell', 0.32], [C.seven + 0.9, 'coinrain', 0.26],
					[C.but + 0.1, 'paper', 0.32], [C.lesson, 'pluck2', 0.3], [C.money - 0.1, 'glow', 0.32],
					[C.would, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/08/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover08: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>THE STORY OF</Chip>
		</div>
		<div style={{position: 'absolute', top: 368, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 200, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>2 PIZZAS</div>
		<div style={{position: 'absolute', left: 50, top: 600}}><Pizza size={380} rot={15} /></div>
		<div style={{position: 'absolute', left: 300, top: 690}}><Pizza size={380} rot={80} /></div>
		<div style={{position: 'absolute', top: 640, left: 640, width: 390, height: 440, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V3-shock.png')} style={{width: 390, height: 683, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1130, width: '100%', textAlign: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 80, lineHeight: 1, color: COLORS.champagne}}>THAT COST</div>
			<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, marginTop: 6, ...GOLD_TEXT}}>10,000 BITCOIN</div>
		</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

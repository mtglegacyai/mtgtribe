import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, interpolate, random, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/02/captions.json';
import timeline from '../../../public/videos/02/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {PhotoCard} from '../../components/PhotoCard';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, LeoClip, Panel, SiteCard, Stage, usePop, useT} from '../whatif01/ui';

// Video 02 (7 Nov 2026, the first daily video): Did You Know This Money Sank, and People Kept Spending It?
// The stone money of Yap, a 9:16 Short in the house format. Script and research: tools/videos/02-did-you-know-stone-money/
// Times are seconds from the start (one narration file, HeyGen word timings in public/videos/02/words.json).

export const DYK02_FPS = 30;
const captions = captionsJson as Caption[];
// end card: MTG's last word, then his theme's last line "Let's get this crypto, wherever I go!" in the clear
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const DYK02_FRAMES = Math.ceil((timeline.total + TAIL) * DYK02_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));

/** A rai stone: a great carved stone wheel with a hole in the middle. */
const Stone: React.FC<{size: number; style?: React.CSSProperties; grey?: number}> = ({size, style}) => (
	<svg width={size} height={size} viewBox="0 0 200 200" style={{overflow: 'visible', filter: 'drop-shadow(0 24px 36px rgba(0,0,0,0.6))', ...style}}>
		<defs>
			<radialGradient id="rai" cx="40%" cy="35%" r="70%">
				<stop offset="0" stopColor="#d9d0bf" />
				<stop offset="0.55" stopColor="#a69b86" />
				<stop offset="1" stopColor="#6e6553" />
			</radialGradient>
		</defs>
		<circle cx="100" cy="100" r="96" fill="url(#rai)" stroke="#5a5244" strokeWidth="3" />
		<circle cx="100" cy="100" r="80" fill="none" stroke="rgba(255,255,255,0.12)" strokeWidth="5" />
		<circle cx="100" cy="100" r="20" fill="#0b0906" stroke="#5a5244" strokeWidth="3" />
		<path d="M40 70 q12 8 18 22 M150 130 q-10 4 -14 16 M62 150 q8 -6 18 -4 M138 52 q4 10 14 12" stroke="rgba(60,52,40,0.55)" strokeWidth="3" fill="none" strokeLinecap="round" />
	</svg>
);

const Person: React.FC<{h: number; glow?: number; color?: string}> = ({h, glow = 0, color = '#2a2117'}) => (
	<svg width={h * 0.42} height={h} viewBox="0 0 42 100" style={{overflow: 'visible', filter: glow ? `drop-shadow(0 0 ${14 * glow}px rgba(255,217,142,${0.9 * glow}))` : undefined}}>
		<circle cx="21" cy="12" r="11" fill={color} stroke={COLORS.gold} strokeWidth="1.5" />
		<path d="M5 100 V44 q0 -16 16 -16 q16 0 16 16 V100 Z" fill={color} stroke={COLORS.gold} strokeWidth="1.5" />
	</svg>
);

const OwnerTag: React.FC<{scale?: number}> = ({scale = 1}) => (
	<div style={{transform: `scale(${scale})`, padding: '8px 18px', borderRadius: 14, background: `linear-gradient(135deg, ${COLORS.goldHi}, ${COLORS.gold})`, color: '#2a1a05', fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: 2, boxShadow: '0 0 30px rgba(242,173,60,0.6)', whiteSpace: 'nowrap'}}>
		🏷️ OWNER
	</div>
);

const Ocean: React.FC<{o: number}> = ({o}) => {
	const t = useT();
	return (
		<AbsoluteFill style={{opacity: o, background: 'linear-gradient(180deg, #0c2a33 0%, #071a21 38%, #040d10 75%, #050403 100%)'}}>
			{[0.18, 0.42, 0.66].map((x, i) => (
				<div key={i} style={{position: 'absolute', left: `${x * 100}%`, top: -200, width: 160, height: 1500, background: 'linear-gradient(180deg, rgba(255,217,142,0.22), rgba(255,217,142,0))', transform: `rotate(${12 - i * 8 + Math.sin(t * 0.6 + i) * 3}deg)`, transformOrigin: 'top center', filter: 'blur(18px)'}} />
			))}
			{Array.from({length: 26}, (_, i) => {
				const speed = 60 + random(`b${i}`) * 90;
				const y = ((1 - ((t * speed + random(`y${i}`) * 1920) % 1920) / 1920) * 1920);
				const s = 6 + random(`s${i}`) * 14;
				return <div key={i} style={{position: 'absolute', left: random(`x${i}`) * 1080, top: y, width: s, height: s, borderRadius: '50%', border: '2px solid rgba(220,240,255,0.35)', background: 'rgba(220,240,255,0.06)'}} />;
			})}
		</AbsoluteFill>
	);
};

const Big: React.FC<{children: React.ReactNode; size?: number; gold?: boolean; o?: number; top: number}> = ({children, size = 150, gold, o = 1, top}) => (
	<div style={{position: 'absolute', top, width: '100%', textAlign: 'center', opacity: o, fontFamily: DISPLAY, fontSize: size, lineHeight: 1, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.85)', ...(gold ? GOLD_TEXT : {})}}>{children}</div>
);

export const StoneMoney: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	// scene windows
	const hook = fadeOut(t, 4.6, 0.4);
	const island = win(t, 4.7, 7.5);
	const stoneUp = win(t, 7.6, 12.9);
	const twist = win(t, 13.2, 20.1);
	const sunk = win(t, 20.2, 26.9);
	const bridge = win(t, 27.0, 36.8);
	const cta = ease(t, 40.9, 0.4);

	// hook: the stone sinks through the water
	const sinkY = interpolate(t, [0, 1.2, 4.6], [-520, 560, 780], {...clamp, easing: Easing.out(Easing.cubic)}); // drops in fast, then sinks slowly below the words
	// sunken-stone scene: the stone slips off a canoe at 21.5 and lands on the sea floor
	const fall = interpolate(t, [21.5, 23.1], [0, 1], {...clamp, easing: Easing.in(Easing.quad)});
	const landed = usePop(23.1, 10);
	// twist: the owner tag moves from villager to villager
	const tagX = interpolate(t, [16.2, 16.9, 17.4, 18.0], [0, 1, 1, 2], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const VILLAGERS = [180, 540, 900];
	const tagLeft = interpolate(tagX, [0, 1, 2], VILLAGERS);
	const remember = ease(t, 18.1, 0.4);
	// bridge: blocks join the chain
	const BLOCKS = [33.0, 33.4, 33.8, 34.2];

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* 0:00 HOOK: the stone sinking */}
			<AbsoluteFill style={{opacity: hook}}>
				<Ocean o={1} />
				<div style={{position: 'absolute', left: 540 - 230, top: sinkY, transform: `rotate(${t * 14}deg)`}}>
					<Stone size={460} />
				</div>
				<Big top={300} size={190} gold o={ease(t, 1.3, 0.3)}>SUNK.</Big>
				<Big top={500} size={120} o={ease(t, 3.4, 0.3)}>STILL MONEY?</Big>
			</AbsoluteFill>

			{/* 0:05 the island of Yap */}
			<AbsoluteFill style={{opacity: island}}>
				<Ocean o={0.85} />
				<div style={{position: 'absolute', left: 300, top: 700, width: 480, height: 300}}>
					<svg width="480" height="300" viewBox="0 0 480 300">
						<path d="M60 170 q40 -90 140 -100 q90 -10 150 40 q70 60 20 110 q-60 50 -170 30 q-160 -20 -140 -80 Z" fill="#3d5a3a" stroke={COLORS.gold} strokeWidth="3" />
						<path d="M70 175 q40 -80 135 -92 q85 -8 142 38" stroke="#d9c38a" strokeWidth="6" fill="none" opacity="0.5" />
					</svg>
					<div style={{position: 'absolute', left: 205, top: -130 + interpolate(usePop(6.2, 11), [0, 1], [-260, 0]), opacity: ease(t, 6.1, 0.2), fontSize: 120}}>📍</div>
				</div>
				<div style={{position: 'absolute', top: 1040, width: '100%', textAlign: 'center', opacity: ease(t, 6.3)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 130, lineHeight: 1, ...GOLD_TEXT}}>YAP</div>
					<div style={{marginTop: 10}}><Chip size={34}>PACIFIC OCEAN</Chip></div>
				</div>
			</AbsoluteFill>

			{/* 0:08 the rai stone next to a person, measured */}
			<AbsoluteFill style={{opacity: stoneUp}}>
				<div style={{position: 'absolute', left: 120, top: 560, transform: `scale(${interpolate(usePop(7.7, 13), [0, 1], [0.85, 1])})`, transformOrigin: 'bottom center'}}>
					<Stone size={620} />
				</div>
				<div style={{position: 'absolute', left: 820, top: 880}}>
					<Person h={300} />
				</div>
				<div style={{position: 'absolute', left: 120, top: 1200, width: 620 * interpolate(t, [10.9, 12.0], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)}), height: 6, background: COLORS.goldHi, boxShadow: '0 0 16px rgba(255,217,142,0.8)'}} />
				<Big top={300} size={64} o={ease(t, 8.9)}><Chip size={40}>RAI STONE</Chip></Big>
				<div style={{position: 'absolute', top: 400, width: '100%', textAlign: 'center', opacity: ease(t, 11.4), fontFamily: DISPLAY, fontSize: 110, ...GOLD_TEXT}}>ABOUT 3.5 m</div>
			</AbsoluteFill>

			{/* 0:13 the stone stays, ownership moves */}
			<AbsoluteFill style={{opacity: twist}}>
				<div style={{position: 'absolute', left: 540 - 220, top: 440}}>
					<Stone size={440} />
				</div>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', opacity: ease(t, 15.4)}}>
					<Chip size={32}>THE STONE STAYS ▪ OWNERSHIP MOVES</Chip>
				</div>
				{VILLAGERS.map((x, i) => (
					<div key={x} style={{position: 'absolute', left: x - 50, top: 940, opacity: ease(t, 13.5 + i * 0.15)}}>
						<Person h={230} glow={remember} color="#3a2c18" />
					</div>
				))}
				<div style={{position: 'absolute', left: tagLeft - 95, top: 885, opacity: ease(t, 16.1, 0.25)}}>
					<OwnerTag />
				</div>
			</AbsoluteFill>

			{/* 0:20 the stone that sank, still owned */}
			<AbsoluteFill style={{opacity: sunk}}>
				<Ocean o={1} />
				<svg width="1080" height="200" style={{position: 'absolute', top: 300}} viewBox="0 0 1080 200">
					<path d={`M${280 + t * 6} 90 q260 70 520 0 l-40 40 q-220 50 -440 0 Z`} fill="#5a3b1c" stroke={COLORS.gold} strokeWidth="3" />
					<path d="M0 95 H1080" stroke="rgba(200,230,255,0.35)" strokeWidth="3" />
				</svg>
				<div style={{position: 'absolute', left: 540 - 200 + fall * 30, top: interpolate(fall, [0, 1], [250, 860]) - (1 - landed) * 0, transform: `rotate(${fall * 40}deg)`}}>
					<Stone size={400} />
				</div>
				<div style={{position: 'absolute', left: 540 - 95, top: 820, opacity: ease(t, 24.4, 0.3), transform: `scale(${interpolate(usePop(24.4, 12), [0, 1], [0.6, 1])})`}}>
					<OwnerTag />
				</div>
				<div style={{position: 'absolute', top: 1180, width: '100%', textAlign: 'center', opacity: ease(t, 24.6)}}>
					<span style={{display: 'inline-block', transform: 'rotate(-4deg)', border: '6px solid #6fcf7a', color: '#9be6a3', fontFamily: DISPLAY, fontSize: 70, padding: '4px 22px', borderRadius: 12, background: 'rgba(5,4,3,0.75)'}}>STILL MONEY ✓</span>
				</div>
			</AbsoluteFill>
			<LeoClip clip="V3" from={25.0} seconds={2.0} style={{left: 290, top: 330, width: 500, height: 360}} focus="50% 6%" />

			{/* 0:27 the bridge: a shared record, then a chain of blocks kept by computers */}
			<AbsoluteFill style={{opacity: bridge}}>
				<Stage style={{justifyContent: 'flex-start'}}>
					<div style={{textAlign: 'center', opacity: fadeOut(t, 29.3)}}>
						<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.05, color: '#fff'}}>MONEY WAS<br />NEVER <span style={GOLD_TEXT}>THE STONE</span></div>
					</div>
				</Stage>
				<Stage style={{justifyContent: 'flex-start', opacity: Math.min(ease(t, 29.5), fadeOut(t, 32.7))}}>
					<Flip at={29.5}>
						<Panel style={{width: 860, padding: '26px 34px'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.goldHi, letterSpacing: 3}}>THE SHARED RECORD</div>
							{['Stone 1 ▪ owned by family A', 'Stone 2 ▪ owned by family B', 'Sunken stone ▪ owned by family C'].map((r, i) => (
								<div key={r} style={{fontFamily: BODY, fontWeight: 800, fontSize: 38, color: COLORS.text, marginTop: 14, opacity: ease(t, 29.9 + i * 0.5)}}>✓ {r}</div>
							))}
							<div style={{fontFamily: BODY, fontSize: 30, color: COLORS.muted, marginTop: 16, opacity: ease(t, 30.9)}}>Everyone trusted it</div>
						</Panel>
					</Flip>
				</Stage>
				<Stage style={{justifyContent: 'flex-start', opacity: ease(t, 32.8)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 96, ...GOLD_TEXT, opacity: ease(t, 32.9)}}>BLOCKCHAIN</div>
					<div style={{display: 'flex', alignItems: 'center', marginTop: 30}}>
						{BLOCKS.map((at, i) => (
							<React.Fragment key={at}>
								{i ? <div style={{width: 40, height: 8, background: COLORS.gold, opacity: ease(t, at, 0.2)}} /> : null}
								<Flip at={at} from="y">
									<div style={{width: 170, height: 170, borderRadius: 20, background: `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 34, color: '#2a1a05', boxShadow: '0 16px 40px rgba(0,0,0,0.5)'}}>#{i + 1}</div>
								</Flip>
							</React.Fragment>
						))}
					</div>
					<div style={{display: 'flex', gap: 34, marginTop: 50}}>
						{Array.from({length: 6}, (_, i) => {
							const on = ease(t, 34.7 + i * 0.2, 0.2);
							return (
								<svg key={i} width="92" height="80" viewBox="0 0 46 40" style={{opacity: 0.25 + on * 0.75, filter: on > 0.5 ? 'drop-shadow(0 0 10px rgba(255,217,142,0.9))' : undefined}}>
									<rect x="3" y="3" width="40" height="26" rx="3" fill="#1a140b" stroke={COLORS.goldHi} strokeWidth="2.5" />
									<path d="M17 36 h12 M23 29 v7" stroke={COLORS.goldHi} strokeWidth="2.5" />
								</svg>
							);
						})}
					</div>
					<div style={{marginTop: 40, opacity: ease(t, 35.3)}}>
						<Chip size={34}>KEPT BY COMPUTERS, NOT MEMORY</Chip>
					</div>
				</Stage>
			</AbsoluteFill>

			{/* 0:37 the question, Leo asks */}
			<LeoClip clip="V2" from={36.9} seconds={4.1} style={{left: 160, top: 320, width: 760, height: 1330}} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: win(t, 37.0, 40.8)}}>
				<Chip size={34} style={{background: 'rgba(5,4,3,0.85)'}}>WOULD YOU ACCEPT MONEY YOU CAN NEVER SEE? 💬</Chip>
			</div>

			{/* 0:41 call to action and sign-off, then the end card with MTG's theme */}
			<AbsoluteFill style={{opacity: cta}}>
				<div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: ease(t, 46.3, 0.4)}}>
					<PhotoCard size={330} />
					<div style={{fontFamily: DISPLAY, fontSize: 90, lineHeight: 1, ...GOLD_TEXT}}>MTG</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text}}>Your Digital Architect</div>
				</div>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, 41.0), fadeOut(t, 46.2, 0.3))}}>
					<div style={{fontFamily: DISPLAY, fontSize: 96, lineHeight: 1.05, color: '#fff'}}>LEARN HOW MONEY<br /><span style={GOLD_TEXT}>REALLY WORKS</span></div>
					<div style={{marginTop: 16}}><Chip size={32}>OLD AND NEW</Chip></div>
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, bottom: 720, display: 'flex', justifyContent: 'center', opacity: fadeOut(t, 49.0, 0.4)}}>
					<SiteCard t={t} at={41.2} vertical />
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, top: 1000, textAlign: 'center', opacity: ease(t, 49.1), transform: `scale(${interpolate(usePop(49.1, 12), [0, 1], [0.7, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 92, ...GOLD_TEXT}}>Let's Get This Crypto!</span> <span style={{fontFamily: DISPLAY, fontSize: 92}}>💪</span>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi, marginTop: 14}}>mtgtribe.com</div>
				</div>
			</AbsoluteFill>

			{/* sound: fitted to this story, soft; MTG's theme plays only its last line, after his last word */}
			<Cues
				list={[
					[0.1, 'air', 0.4], [1.0, 'sink', 0.55], [3.5, 'thud', 0.3],
					[4.8, 'air', 0.3], [6.2, 'thud', 0.3], [7.7, 'air', 0.25], [10.9, 'tick', 0.3], [12.0, 'tick', 0.3],
					[13.3, 'air', 0.3], [16.2, 'thud', 0.3], [17.4, 'thud', 0.28], [18.1, 'tick', 0.22],
					[20.3, 'air', 0.3], [21.5, 'sink', 0.45], [24.4, 'thud', 0.35],
					[27.0, 'air', 0.3], [29.6, 'paper', 0.3], ...BLOCKS.map((a) => [a, 'link', 0.45] as [number, string, number]), [34.7, 'tick', 0.22],
					[36.9, 'air', 0.3], [41.0, 'thud', 0.35], [46.3, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/02/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16) for TikTok, Reels and Shorts: everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover02: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: 'linear-gradient(180deg, #0c2a33 0%, #071a21 45%, #040d10 80%, #050403 100%)'}} />
		{[0.2, 0.5, 0.75].map((x, i) => (
			<div key={i} style={{position: 'absolute', left: `${x * 100}%`, top: -200, width: 170, height: 1600, background: 'linear-gradient(180deg, rgba(255,217,142,0.25), rgba(255,217,142,0))', transform: `rotate(${12 - i * 9}deg)`, transformOrigin: 'top center', filter: 'blur(18px)'}} />
		))}
		<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
			<Chip size={40}>DID YOU KNOW?</Chip>
		</div>
		<div style={{position: 'absolute', top: 400, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 210, lineHeight: 0.95, ...GOLD_TEXT}}>SUNK.</div>
		<div style={{position: 'absolute', top: 610, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 130, lineHeight: 1, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>STILL MONEY.</div>
		<div style={{position: 'absolute', left: 540 - 270, top: 820, transform: 'rotate(18deg)'}}>
			<Stone size={540} />
		</div>
		{[[300, 900, 18], [760, 980, 12], [690, 1180, 22], [350, 1300, 10], [820, 1380, 16]].map(([x, y, s], i) => (
			<div key={i} style={{position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: '50%', border: '2px solid rgba(220,240,255,0.4)'}} />
		))}
		<div style={{position: 'absolute', top: 1430, right: 70}}>
			<PhotoCard size={230} />
		</div>
		<div style={{position: 'absolute', top: 1480, left: 70, fontFamily: BODY, fontWeight: 800, fontSize: 46, color: COLORS.champagne, textShadow: '0 4px 18px rgba(0,0,0,0.9)'}}>The stone money<br />of Yap</div>
		<div style={{position: 'absolute', bottom: 90, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi}}>mtgtribe.com</div>
	</AbsoluteFill>
);

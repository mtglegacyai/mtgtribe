import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/03/captions.json';
import timeline from '../../../public/videos/03/timeline.json';
import {closingTail, COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {PhotoCard} from '../../components/PhotoCard';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, Flip, GOLD_TEXT, LeoClip, Panel, SiteCard, usePop, useT} from '../whatif01/ui';

// Video 03 (8 Nov 2026, daily video): What Everyone Ought to Know About These 12 Words. A 9:16 Short in the house
// format. Script and research: tools/videos/03-what-everyone-ought-to-know-12-words/. Words are always masked (••••),
// so no frame ever shows a usable recovery phrase. Times are seconds from the start (HeyGen word timings).

export const DKO03_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const DKO03_FRAMES = Math.ceil((timeline.total + TAIL) * DKO03_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));

const Tile: React.FC<{n: number; w?: number}> = ({n, w = 280}) => (
	<div style={{width: w, height: w * 0.36, borderRadius: 16, background: `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`, display: 'flex', alignItems: 'center', gap: w * 0.06, padding: `0 ${w * 0.07}px`, boxShadow: '0 12px 30px rgba(0,0,0,0.5)', boxSizing: 'border-box'}}>
		<span style={{fontFamily: MONO, fontWeight: 700, fontSize: w * 0.13, color: '#5a3b10'}}>{n}.</span>
		<span style={{fontFamily: MONO, fontWeight: 700, fontSize: w * 0.15, letterSpacing: w * 0.012, color: '#2a1a05'}}>••••••</span>
	</div>
);

const Key: React.FC<{size: number; glow?: number}> = ({size, glow = 0}) => (
	<svg width={size} height={size * 0.45} viewBox="0 0 200 90" style={{overflow: 'visible', filter: `drop-shadow(0 0 ${20 * glow}px rgba(255,217,142,0.9)) drop-shadow(0 14px 22px rgba(0,0,0,0.5))`}}>
		<defs>
			<linearGradient id="k03" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor={COLORS.goldHi} />
				<stop offset="1" stopColor="#b0761f" />
			</linearGradient>
		</defs>
		<circle cx="42" cy="45" r="38" fill="url(#k03)" />
		<circle cx="42" cy="45" r="16" fill="#0b0906" />
		<rect x="74" y="36" width="122" height="18" rx="6" fill="url(#k03)" />
		<rect x="150" y="50" width="14" height="26" rx="3" fill="url(#k03)" />
		<rect x="176" y="50" width="14" height="20" rx="3" fill="url(#k03)" />
	</svg>
);

const House: React.FC<{size: number; open?: number}> = ({size, open = 0}) => (
	<svg width={size} height={size} viewBox="0 0 200 200" style={{overflow: 'visible'}}>
		<path d="M20 95 L100 25 L180 95" fill="none" stroke={COLORS.gold} strokeWidth="10" strokeLinejoin="round" />
		<rect x="38" y="90" width="124" height="100" rx="6" fill="#1a140b" stroke={COLORS.gold} strokeWidth="5" />
		<rect x="82" y="120" width="36" height="70" fill="#050403" />
		<rect x="82" y="120" width="36" height="70" fill="#5a3b1c" stroke={COLORS.goldHi} strokeWidth="3" style={{transformOrigin: '82px 155px', transform: `perspective(300px) rotateY(${-75 * open}deg)`}} />
	</svg>
);

const Phone: React.FC<{children?: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<div style={{width: 420, height: 760, borderRadius: 56, background: '#0d0b08', border: '10px solid #2b241a', boxShadow: `0 0 0 2px ${COLORS.gold}, 0 30px 70px rgba(0,0,0,0.6)`, position: 'relative', overflow: 'hidden', ...style}}>
		<div style={{position: 'absolute', top: 14, left: '50%', transform: 'translateX(-50%)', width: 110, height: 28, borderRadius: 14, background: '#000'}} />
		{children}
	</div>
);

const Globe: React.FC<{size: number}> = ({size}) => (
	<svg width={size} height={size} viewBox="0 0 200 200">
		<circle cx="100" cy="100" r="94" fill="rgba(242,173,60,0.08)" stroke={COLORS.gold} strokeWidth="3" />
		{[30, 60].map((rx) => <ellipse key={rx} cx="100" cy="100" rx={rx} ry="94" fill="none" stroke="rgba(242,173,60,0.45)" strokeWidth="2" />)}
		{[-50, 0, 50].map((y) => <path key={y} d={`M${100 - Math.sqrt(94 * 94 - y * y)} ${100 + y} H${100 + Math.sqrt(94 * 94 - y * y)}`} stroke="rgba(242,173,60,0.45)" strokeWidth="2" />)}
	</svg>
);

export const TwelveWords: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, 4.8, 0.35);
	const phoneScene = win(t, 5.0, 11.0);
	const keyScene = win(t, 11.1, 13.9);
	const restore = win(t, 13.9, 16.9);
	const copy = win(t, 17.1, 25.9);
	const scam = win(t, 26.1, 31.7);
	const todo = win(t, 32.0, 37.2);
	const cta = ease(t, 42.0, 0.4);

	// the copied key flies across the globe to a faraway door, which opens without a sound
	const fly = interpolate(t, [18.8, 20.4], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const doorOpen = interpolate(t, [22.3, 23.0], [0, 1], clamp);
	const coinsOut = interpolate(t, [23.3, 24.6], [0, 1], clamp);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* 0:00 HOOK: twelve masked word tiles */}
			<AbsoluteFill style={{opacity: hook}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.2)}}>
					<Chip size={34}>WHAT EVERYONE OUGHT TO KNOW</Chip>
				</div>
				<div style={{position: 'absolute', top: 380, left: 60, right: 60, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18, justifyItems: 'center'}}>
					{Array.from({length: 12}, (_, i) => (
						<Flip key={i} at={0.25 + i * 0.1}>
							<Tile n={i + 1} />
						</Flip>
					))}
				</div>
				<div style={{position: 'absolute', top: 900, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.02, color: '#fff', opacity: ease(t, 2.65, 0.25), textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>WHOEVER HAS THEM</div>
					<div style={{fontFamily: DISPLAY, fontSize: 118, lineHeight: 1.02, ...GOLD_TEXT, opacity: ease(t, 3.95, 0.25), transform: `scale(${interpolate(usePop(3.95, 12), [0, 1], [0.7, 1])})`}}>HAS YOUR MONEY</div>
				</div>
			</AbsoluteFill>

			{/* 0:05 your own wallet gives you 12 or 24 words: a recovery phrase */}
			<AbsoluteFill style={{opacity: phoneScene}}>
				<div style={{position: 'absolute', left: 330, top: 300, transform: `translateY(${(1 - ease(t, 5.0, 0.5)) * 80}px)`}}>
					<Phone>
						<div style={{position: 'absolute', top: 70, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 26, color: COLORS.goldHi, letterSpacing: 2}}>MY WALLET</div>
						<div style={{position: 'absolute', top: 130, left: 28, right: 28, display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, justifyItems: 'center'}}>
							{Array.from({length: 12}, (_, i) => (
								<div key={i} style={{opacity: ease(t, 7.4 + i * 0.08, 0.2)}}><Tile n={i + 1} w={160} /></div>
							))}
						</div>
					</Phone>
				</div>
				<div style={{position: 'absolute', top: 1100, width: '100%', textAlign: 'center', opacity: ease(t, 9.9)}}>
					<Chip size={40}>RECOVERY PHRASE</Chip>
				</div>
			</AbsoluteFill>

			{/* 0:11 the master key to your house */}
			<AbsoluteFill style={{opacity: keyScene}}>
				<div style={{position: 'absolute', top: 330, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 100, ...GOLD_TEXT, opacity: ease(t, 11.3)}}>MASTER KEY</div>
				<div style={{position: 'absolute', left: 540 - 260, top: 520, transform: `rotate(${interpolate(usePop(12.55, 10), [0, 1], [-30, 0])}deg) scale(${usePop(12.55, 10)})`}}>
					<Key size={520} glow={ease(t, 12.6)} />
				</div>
				<div style={{position: 'absolute', left: 540 - 160, top: 820, opacity: ease(t, 13.1), transform: `scale(${interpolate(usePop(13.1, 12), [0, 1], [0.7, 1])})`}}>
					<House size={320} />
				</div>
			</AbsoluteFill>

			{/* 0:14 lose your phone: the words open your wallet on a new one */}
			<AbsoluteFill style={{opacity: restore}}>
				<div style={{position: 'absolute', left: 90, top: 380, transform: `translateY(${interpolate(t, [14.3, 15.2], [0, 1300], {...clamp, easing: Easing.in(Easing.quad)})}px) rotate(${interpolate(t, [14.3, 15.2], [0, 40], clamp)}deg)`, opacity: 0.75}}>
					<Phone style={{transform: 'scale(0.7)', transformOrigin: 'top left'}} />
				</div>
				<div style={{position: 'absolute', left: 560, top: 380, opacity: ease(t, 15.2), transform: `translateX(${(1 - ease(t, 15.2, 0.5)) * 300}px) scale(0.7)`, transformOrigin: 'top left'}}>
					<Phone>
						<div style={{position: 'absolute', top: 260, width: '100%', textAlign: 'center', fontSize: 140, opacity: ease(t, 16.2)}}>✅</div>
						<div style={{position: 'absolute', top: 160, width: '100%', display: 'flex', justifyContent: 'center', opacity: ease(t, 15.5)}}><Key size={220} /></div>
					</Phone>
				</div>
				<div style={{position: 'absolute', top: 1000, width: '100%', textAlign: 'center', opacity: ease(t, 16.0)}}>
					<Chip size={36}>WALLET BACK ON A NEW PHONE</Chip>
				</div>
			</AbsoluteFill>

			{/* 0:17 where the key picture stops: a copy works from anywhere, silently; no bank to call */}
			<AbsoluteFill style={{opacity: copy}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', opacity: ease(t, 17.3)}}>
					<Chip size={34}>UNLIKE A HOUSE KEY</Chip>
				</div>
				<div style={{position: 'absolute', left: 540 - 230, top: 400, opacity: 0.9}}>
					<Globe size={460} />
				</div>
				<div style={{position: 'absolute', left: 150 + fly * 560, top: 600 - Math.sin(fly * Math.PI) * 260, opacity: ease(t, 18.7, 0.2), transform: `rotate(${fly * 30}deg)`}}>
					<Key size={180} glow={1} />
				</div>
				<div style={{position: 'absolute', left: 120, top: 560, opacity: Math.min(ease(t, 18.8), fadeOut(t, 21.2)), fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.champagne}}>COPY ↗</div>
				<div style={{position: 'absolute', left: 640, top: 830, opacity: ease(t, 21.4)}}>
					<House size={300} open={doorOpen} />
					<div style={{position: 'absolute', left: -110, top: 40, fontSize: 90, opacity: ease(t, 22.4)}}>🔇</div>
					{Array.from({length: 6}, (_, i) => (
						<div key={i} style={{position: 'absolute', left: 135 - coinsOut * (140 + i * 50), top: 250 - Math.sin(coinsOut * Math.PI) * (60 + i * 18), width: 44, height: 44, borderRadius: '50%', background: `radial-gradient(circle at 35% 30%, ${COLORS.goldHi}, ${COLORS.gold} 60%, #a8701f)`, opacity: coinsOut > 0.02 ? 1 - coinsOut * 0.6 : 0}} />
					))}
				</div>
				<div style={{position: 'absolute', top: 1170, width: '100%', textAlign: 'center', opacity: ease(t, 24.9)}}>
					<Chip size={40} style={{borderColor: '#e0602f', color: '#ff9a63'}}>☎️ NO BANK TO CALL</Chip>
				</div>
			</AbsoluteFill>
			<LeoClip clip="V3" from={20.5} seconds={2.6} style={{left: 90, top: 820, width: 500, height: 330}} focus="50% 6%" />

			{/* 0:26 the scam: fake support asks for the words */}
			<AbsoluteFill style={{opacity: scam}}>
				<div style={{position: 'absolute', left: 120, right: 120, top: 330}}>
					<Flip at={26.3}>
						<Panel style={{padding: '24px 28px', background: 'rgba(18,14,9,0.95)'}}>
							<div style={{display: 'flex', alignItems: 'center', gap: 16}}>
								<div style={{width: 64, height: 64, borderRadius: '50%', background: '#2b3a55', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 34}}>🎧</div>
								<div>
									<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 34, color: COLORS.text}}>Wallet Support ✔</div>
									<div style={{fontFamily: BODY, fontSize: 24, color: COLORS.muted}}>online now</div>
								</div>
							</div>
							<div style={{marginTop: 22, padding: '18px 22px', borderRadius: 22, background: '#24324a', fontFamily: BODY, fontWeight: 700, fontSize: 36, lineHeight: 1.3, color: '#eef3ff', opacity: ease(t, 26.9)}}>
								Hi! To fix your wallet, please send me your 12 words 🙏
							</div>
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 560, width: '100%', textAlign: 'center', opacity: ease(t, 28.9, 0.2)}}>
					<span style={{display: 'inline-block', transform: `rotate(-10deg) scale(${interpolate(usePop(28.9, 11), [0, 1], [1.6, 1])})`, border: '8px solid #e0602f', color: '#ff8a4c', fontFamily: DISPLAY, fontSize: 140, padding: '0 34px', borderRadius: 14, background: 'rgba(5,4,3,0.75)'}}>SCAM</span>
				</div>
				<div style={{position: 'absolute', top: 920, width: '100%', textAlign: 'center', opacity: ease(t, 29.7)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 96, lineHeight: 1.05, color: '#fff'}}>REAL SUPPORT</div>
					<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.05, ...GOLD_TEXT}}>NEVER ASKS</div>
				</div>
			</AbsoluteFill>

			{/* 0:32 what to do */}
			<AbsoluteFill style={{opacity: todo}}>
				<div style={{position: 'absolute', top: 320, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 96, ...GOLD_TEXT, opacity: ease(t, 32.1)}}>KEEP THEM SAFE</div>
				<div style={{position: 'absolute', left: 90, right: 90, top: 480, display: 'flex', flexDirection: 'column', gap: 26}}>
					{([['✅', 'Write them on paper', 32.1], ['✅', 'Keep them offline', 33.5], ['❌', 'Never type them into a link someone sent you', 34.6]] as Array<[string, string, number]>).map(([icon, text, at]) => (
						<Flip key={text} at={at}>
							<Panel style={{display: 'flex', alignItems: 'center', gap: 22, padding: '22px 28px', borderColor: icon === '❌' ? 'rgba(224,96,47,0.8)' : undefined}}>
								<div style={{fontSize: 64}}>{icon}</div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.text, lineHeight: 1.2}}>{text}</div>
							</Panel>
						</Flip>
					))}
				</div>
			</AbsoluteFill>

			{/* 0:37 the question, Leo asks; never post your words */}
			<LeoClip clip="V2" from={37.3} seconds={4.4} style={{left: 160, top: 320, width: 760, height: 1330}} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: win(t, 37.4, 41.6)}}>
				<Chip size={32} style={{background: 'rgba(5,4,3,0.85)'}}>HAS ANYONE ASKED YOU FOR YOUR WORDS? 💬</Chip>
				<div style={{marginTop: 12}}>
					<span style={{display: 'inline-block', padding: '8px 20px', borderRadius: 12, background: 'rgba(120,30,10,0.9)', border: '2px solid #e0602f', fontFamily: BODY, fontWeight: 800, fontSize: 30, color: '#ffd2bd'}}>⚠️ Never post your words in the comments</span>
				</div>
			</div>

			{/* 0:42 call to action and sign-off, then MTG's theme line */}
			<AbsoluteFill style={{opacity: cta}}>
				<div style={{position: 'absolute', top: 300, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: ease(t, 45.9, 0.4)}}>
					<PhotoCard size={330} />
					<div style={{fontFamily: DISPLAY, fontSize: 90, lineHeight: 1, ...GOLD_TEXT}}>MTG</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text}}>Your Digital Architect</div>
				</div>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, 42.0), fadeOut(t, 45.8, 0.3))}}>
					<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.05, color: '#fff'}}>STAY SAFE<br /><span style={GOLD_TEXT}>WITH CRYPTO</span></div>
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, bottom: 720, display: 'flex', justifyContent: 'center', opacity: fadeOut(t, 48.2, 0.4)}}>
					<SiteCard t={t} at={42.3} vertical />
				</div>
				<div style={{position: 'absolute', left: 0, right: 0, top: 1000, textAlign: 'center', opacity: ease(t, 48.25), transform: `scale(${interpolate(usePop(48.25, 12), [0, 1], [0.7, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 92, ...GOLD_TEXT}}>Let's Get This Crypto!</span> <span style={{fontFamily: DISPLAY, fontSize: 92}}>💪</span>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi, marginTop: 14}}>mtgtribe.com</div>
				</div>
			</AbsoluteFill>

			{/* sound, fitted to this story and soft; the theme plays only its last line at the end */}
			<Cues
				list={[
					[0.1, 'air', 0.35], [0.25, 'count', 0.22], [2.7, 'thud', 0.3], [3.95, 'reveal', 0.45],
					[5.0, 'air', 0.3], [7.4, 'tick', 0.25], [9.9, 'pluck2', 0.35], [12.55, 'key', 0.5], [13.1, 'pluck3', 0.3],
					[14.3, 'air', 0.3], [15.5, 'key', 0.35], [16.2, 'chime', 0.4],
					[17.2, 'air', 0.3], [18.8, 'key', 0.4], [19.0, 'swell', 0.35], [22.3, 'door', 0.5], [23.3, 'coinrain', 0.3], [24.9, 'drop', 0.45],
					[26.2, 'pluck1', 0.35], [28.9, 'thud', 0.5], [29.7, 'reveal', 0.45],
					[32.1, 'pluck1', 0.4], [33.5, 'pluck3', 0.4], [34.6, 'thud', 0.4],
					[37.3, 'air', 0.3], [38.0, 'chime', 0.4], [42.0, 'glow', 0.35], [45.9, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/03/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover03: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 35%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 280, width: '100%', textAlign: 'center'}}>
			<Chip size={36}>WHAT EVERYONE OUGHT TO KNOW</Chip>
		</div>
		<div style={{position: 'absolute', top: 360, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 250, lineHeight: 1, ...GOLD_TEXT}}>12 WORDS</div>
		<div style={{position: 'absolute', top: 640, left: 70, right: 70, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14, justifyItems: 'center'}}>
			{Array.from({length: 6}, (_, i) => <Tile key={i} n={i + 1} w={290} />)}
		</div>
		<div style={{position: 'absolute', top: 900, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 96, lineHeight: 1.02, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>WHOEVER HAS THEM<br /><span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>HAS YOUR MONEY</span></div>
		<div style={{position: 'absolute', top: 1170, left: 70, width: 470, height: 470, borderRadius: 36, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7)'}}>
			<Img src={staticFile('videos/01/leo/V3-shock.png')} style={{width: 470, height: 822, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1260, left: 590, right: 60, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22}}>
			<PhotoCard size={260} />
			<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 38, color: COLORS.champagne, textAlign: 'center'}}>Never share them</div>
		</div>
		<div style={{position: 'absolute', bottom: 90, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi}}>mtgtribe.com</div>
	</AbsoluteFill>
);

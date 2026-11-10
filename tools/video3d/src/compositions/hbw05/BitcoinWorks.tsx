import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/05/captions.json';
import C from '../../../public/videos/05/cues.json';
import timeline from '../../../public/videos/05/timeline.json';
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
import {Backdrop, Chip, clamp, Cue, Cues, ease, fadeOut, Flip, GOLD_TEXT, Panel, usePop, useT} from '../whatif01/ui';

// Video 05 (10 Nov 2026, daily video): How Bitcoin Really Works. A 9:16 Short, the first with MTG's upgrades: Leo at every
// emotional beat (LeoMoment), CSS 3D (the coin, the blocks), the notepad, and the EndScreen with pills.
// Script and research: tools/videos/05-how-bitcoin-really-works/. Every time below is a named cue from the voice's own
// word timings (public/videos/05/cues.json, made by scripts/make_cues.py from anchors.json), never a guessed second.

export const HBW05_FPS = 30;
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const HBW05_FRAMES = Math.ceil((timeline.total + TAIL) * HBW05_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const RED = '#e0602f';
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;

/** The numbered step header: a round number and a title. */
const Step: React.FC<{n: string; title: string; at: number; warn?: boolean}> = ({n, title, at, warn}) => {
	const p = usePop(at, 13);
	return (
		<div style={{position: 'absolute', top: 285, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, opacity: Math.min(1, p * 1.4), transform: `translateY(${(1 - p) * -30}px)`}}>
			<div style={{width: 104, height: 104, borderRadius: '50%', background: warn ? `linear-gradient(145deg, #ff9a63, ${RED})` : GOLD_FILL, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 70, color: '#2a1a05', boxShadow: '0 12px 30px rgba(0,0,0,0.55)', transform: `rotate(${(1 - p) * -180}deg)`}}>{n}</div>
			<div style={{fontFamily: DISPLAY, fontSize: 74, lineHeight: 1, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>{title}</div>
		</div>
	);
};

const Key: React.FC<{size: number; glow?: number}> = ({size, glow = 0}) => (
	<svg width={size} height={size * 0.45} viewBox="0 0 200 90" style={{overflow: 'visible', filter: `drop-shadow(0 0 ${20 * glow}px rgba(255,217,142,0.9)) drop-shadow(0 10px 16px rgba(0,0,0,0.5))`}}>
		<defs>
			<linearGradient id="k05" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor={COLORS.goldHi} />
				<stop offset="1" stopColor="#b0761f" />
			</linearGradient>
		</defs>
		<circle cx="42" cy="45" r="38" fill="url(#k05)" />
		<circle cx="42" cy="45" r="16" fill="#0b0906" />
		<rect x="74" y="36" width="122" height="18" rx="6" fill="url(#k05)" />
		<rect x="150" y="50" width="14" height="26" rx="3" fill="url(#k05)" />
		<rect x="176" y="50" width="14" height="20" rx="3" fill="url(#k05)" />
	</svg>
);

const MiniCoin: React.FC<{size: number}> = ({size}) => (
	<div style={{width: size, height: size, borderRadius: '50%', background: `radial-gradient(circle at 35% 30%, ${COLORS.goldHi}, ${COLORS.gold} 55%, #a8701f)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: size * 0.6, color: '#4a2f08', boxShadow: '0 6px 14px rgba(0,0,0,0.5)'}}>₿</div>
);

/** A small computer holding its own copy of the record. */
const Node: React.FC<{on: number}> = ({on}) => (
	<div style={{width: 112, opacity: Math.min(1, on * 1.4), transform: `scale(${0.5 + 0.5 * on})`}}>
		<div style={{height: 78, borderRadius: 10, border: `3px solid ${COLORS.gold}`, background: 'linear-gradient(180deg, #2a2116, #120e09)', boxShadow: `0 0 ${22 * on}px rgba(242,173,60,0.35)`, padding: '10px 12px', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: 7}}>
			{[1, 0.7, 0.85].map((w, i) => <div key={i} style={{height: 9, width: `${w * 100}%`, borderRadius: 4, background: i === 0 ? COLORS.goldHi : 'rgba(242,173,60,0.55)'}} />)}
		</div>
		<div style={{height: 9, margin: '0 14px', borderRadius: '0 0 8px 8px', background: COLORS.gold}} />
	</div>
);
const RING = Array.from({length: 8}, (_, k) => {
	const a = (k / 8) * Math.PI * 2 - Math.PI / 2;
	return [540 + Math.cos(a) * 345, 735 + Math.sin(a) * 265] as [number, number];
});

const HALVINGS: Array<[string, string, number]> = [['50', '2009', 1], ['25', '2012', 0.5], ['12.5', '2016', 0.25], ['6.25', '2020', 0.125], ['3.125', '2024', 0.0625]];

export const BitcoinWorks: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.one - 0.3, 0.3);
	const one = win(t, C.one - 0.15, C.two - 0.3, 0.3);
	const twoA = win(t, C.two - 0.15, C.fourYears - 0.25, 0.3);
	const twoB = win(t, C.fourYears - 0.1, C.three - 0.3, 0.3);
	const three = win(t, C.three - 0.15, C.tip - 0.3, 0.3);
	const tip = win(t, C.tip - 0.15, C.q - 0.3, 0.3);
	const ask = win(t, C.q - 0.15, C.send - 0.2, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	// hook: the coin turns in, the supply counts up, the bar fills
	const coinIn = interpolate(t, [0.15, 1.5], [-540, 0], {...clamp, easing: Easing.out(Easing.cubic)});
	const supply = Math.round(interpolate(t, [C.nMax + 0.1, C.nMax + 1.0], [0, 21], {...clamp, easing: Easing.out(Easing.cubic)}) * 1_000_000);
	const mined = interpolate(t, [C.nOut + 0.1, C.out + 0.2], [0, 0.952], {...clamp, easing: Easing.inOut(Easing.cubic)});
	// two: the new block drops onto the chain; the reward stairs
	const drop = interpolate(t, [C.block - 0.25, C.block + 0.25], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.4))});
	const reward = interpolate(t, [C.earn, C.earn + 0.7], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	const stairStep = Math.max(0.22, (C.stops - C.fourYears - 0.5) / 5);
	// three: the key slips away, the coins lock
	const keyGone = interpolate(t, [C.lose1 + 0.15, C.lose1 + 0.85], [0, 1], {...clamp, easing: Easing.in(Easing.quad)});
	const locked = ease(t, C.lose2 + 0.1, 0.35);

	const stairCues: Cue[] = HALVINGS.slice(1).map((_, k) => [C.fourYears + 0.1 + (k + 1) * stairStep, 'halve', 0.38]);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: if Bitcoin still confuses you; 21 million ever, over 20 million already out; number three */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.one)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.15)}}>
					<Chip size={40}>HOW BITCOIN REALLY WORKS</Chip>
				</div>
				<div style={{position: 'absolute', left: 540 - 150, top: 385, opacity: ease(t, 0.15, 0.4)}}>
					<Coin3D size={300} rotY={coinIn + Math.sin(t * 1.5) * 16} rotX={8} glow={0.5 + 0.3 * ease(t, C.nMax, 0.5)} />
				</div>
				<div style={{position: 'absolute', top: 705, width: '100%', textAlign: 'center', opacity: ease(t, C.nMax, 0.25)}}>
					<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT}}>{supply.toLocaleString('en-US')}</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.champagne, marginTop: 6, opacity: ease(t, C.nMax + 0.9)}}>BITCOIN. THAT'S ALL, EVER.</div>
				</div>
				<div style={{position: 'absolute', left: 110, right: 110, top: 950, opacity: ease(t, C.nOut, 0.3)}}>
					<div style={{height: 60, borderRadius: 30, border: `3px solid ${COLORS.gold}`, background: 'rgba(18,14,9,0.9)', overflow: 'hidden', position: 'relative'}}>
						<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${mined * 100}%`, background: GOLD_FILL, borderRadius: 30}} />
						<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 32, color: '#1a1206', opacity: ease(t, C.nOut + 0.7)}}>20,000,000+ ALREADY MINED</div>
					</div>
					<div style={{textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, marginTop: 10, opacity: ease(t, C.out)}}>The 20 millionth was mined in March 2026</div>
				</div>
				<div style={{position: 'absolute', top: 1095, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 18, opacity: ease(t, C.n3, 0.25)}}>
					{['1', '2', '3'].map((n, i) => {
						const hot = i === 2;
						const pulse = hot ? 1 + 0.07 * Math.sin((t - C.n3) * 9) * ease(t, C.n3 + 0.2) : 1;
						return (
							<div key={n} style={{width: 92, height: 92, borderRadius: '50%', background: hot ? `linear-gradient(145deg, #ff9a63, ${RED})` : 'rgba(18,14,9,0.9)', border: `3px solid ${hot ? RED : COLORS.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 56, color: hot ? '#2a1a05' : COLORS.goldHi, transform: `scale(${pulse})`, boxShadow: hot ? '0 0 34px rgba(224,96,47,0.6)' : 'none'}}>{n}</div>
						);
					})}
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 36, color: '#ff9a63', marginLeft: 8, opacity: ease(t, C.loseAll - 0.3)}}>⚠️ how people lose it all</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.hook + 0.35} seconds={Math.min(1.9, C.nMax - C.hook - 0.5)} style={{left: 46, top: 395, width: 300, height: 280}} />
			<LeoMoment m="wow" at={C.nOut + 0.3} seconds={Math.min(1.7, C.n3 - C.nOut - 0.2)} style={{left: 734, top: 395, width: 300, height: 280}} accent="wow" />
			<LeoMoment m="worried" at={C.n3 + 0.45} seconds={Math.min(1.5, C.one - C.n3 - 0.8)} style={{left: 46, top: 395, width: 300, height: 280}} accent="alert" />

			{/* ONE: a shared record, copied on thousands of computers; no bank or government runs it */}
			<AbsoluteFill style={{opacity: one, transform: push(t, C.one, C.two)}}>
				<Step n="1" title="A SHARED RECORD" at={C.one} />
				<svg width="1080" height="1920" style={{position: 'absolute', inset: 0}}>
					{RING.map(([x, y], k) => {
						const p = ease(t, C.computers + 0.1 + k * 0.11, 0.4);
						return <line key={k} x1="540" y1="735" x2={540 + (x - 540) * p} y2={735 + (y - 735) * p} stroke="rgba(242,173,60,0.55)" strokeWidth="3" strokeDasharray="8 10" />;
					})}
				</svg>
				{RING.map(([x, y], k) => (
					<div key={k} style={{position: 'absolute', left: x - 56, top: y - 44}}>
						<Node on={ease(t, C.computers + 0.2 + k * 0.11, 0.35)} />
					</div>
				))}
				<div style={{position: 'absolute', left: 540 - 160, top: 735 - 118}}>
					<Flip at={C.record - 0.1}>
						<Panel style={{width: 320, padding: '18px 22px', boxSizing: 'border-box', background: 'rgba(18,14,9,0.97)'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, color: COLORS.goldHi, letterSpacing: 2, textAlign: 'center'}}>WHO OWNS WHAT</div>
							{[['A ➜ B', '0.5 ₿'], ['C ➜ D', '1.2 ₿'], ['E ➜ F', '0.1 ₿']].map(([who, amt], i) => (
								<div key={who} style={{display: 'flex', justifyContent: 'space-between', fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.text, marginTop: 12, opacity: ease(t, C.record + 0.2 + i * 0.2)}}>
									<span>{who}</span>
									<span style={{color: COLORS.goldHi}}>{amt}</span>
								</div>
							))}
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 866, width: '100%', textAlign: 'center', opacity: win(t, C.thousands, C.noBank + 0.1, 0.25)}}>
					<Chip size={30} style={{background: 'rgba(5,4,3,0.9)'}}>🌍 THOUSANDS OF COPIES</Chip>
				</div>
				<div style={{position: 'absolute', top: 1090, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 22}}>
					{([['🏦', 'NO BANK', C.noBank], ['🏛️', 'NO GOVERNMENT', C.govt]] as Array<[string, string, number]>).map(([icon, text, at]) => (
						<div key={text} style={{position: 'relative', opacity: ease(t, at - 0.1, 0.25), transform: `scale(${interpolate(usePop(at - 0.1, 12), [0, 1], [0.7, 1])})`}}>
							<HintPill icon={icon} text={text} size={38} style={{}} />
							<div style={{position: 'absolute', left: 14, right: 14, top: '50%', height: 6, borderRadius: 3, background: RED, opacity: 0.9, transformOrigin: 'left center', transform: `scaleX(${interpolate(t, [at + 0.15, at + 0.5], [0, 1], clamp)}) rotate(-5deg)`}} />
						</div>
					))}
				</div>
			</AbsoluteFill>
			<LeoMoment m="point" at={C.noBank + 0.15} seconds={Math.min(2.6, C.two - C.noBank - 0.5)} style={{left: 385, top: 575, width: 310, height: 330}} focus="50% 14%" sound="pluck2" volume={0.3} />

			{/* TWO (a): about every 10 minutes, miners add the next page, a block, and earn new Bitcoin */}
			<AbsoluteFill style={{opacity: twoA, transform: push(t, C.two, C.fourYears)}}>
				<Step n="2" title="NEW BLOCKS" at={C.two} />
				<div style={{position: 'absolute', top: 425, width: '100%', textAlign: 'center', opacity: ease(t, C.tenMin - 0.1)}}>
					<Chip size={40}>⏱️ ABOUT EVERY 10 MINUTES</Chip>
				</div>
				<div style={{position: 'absolute', top: 640, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
					{[0, 1, 2].map((i) => {
						const p = i < 2 ? ease(t, C.two + 0.25 + i * 0.25, 0.45) : drop;
						return (
							<React.Fragment key={i}>
								{i > 0 && <div style={{width: 46, height: 14, borderRadius: 7, background: COLORS.gold, opacity: i < 2 ? p : ease(t, C.block + 0.15, 0.2), transform: `scaleX(${i < 2 ? p : ease(t, C.block + 0.15, 0.2)})`}} />}
								<div style={{opacity: Math.min(1, p * 1.5), transform: i < 2 ? `translateY(${(1 - p) * 60}px)` : `translateY(${(1 - p) * -260}px)`}}>
									<Block3D w={230} h={200} d={160} rotY={interpolate(t, [C.two, C.fourYears], [-36, -20], clamp)} label={i < 2 ? `#${i + 1}` : 'NEW'} sub="BLOCK" />
								</div>
							</React.Fragment>
						);
					})}
				</div>
				<div style={{position: 'absolute', left: 782 - 70, top: 560 - reward * 90, opacity: Math.min(1, reward * 2), transform: `scale(${0.4 + 0.6 * reward})`}}>
					<Coin3D size={140} rotY={(t - C.earn) * 200} glow={0.8} />
				</div>
				<div style={{position: 'absolute', top: 930, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text, opacity: ease(t, C.miners)}}>⛏️ Miners add the next page: <span style={{color: COLORS.goldHi}}>a block</span></div>
				<div style={{position: 'absolute', top: 1030, width: '100%', textAlign: 'center', opacity: ease(t, C.earn + 0.2)}}>
					<Chip size={36}>🪙 THEIR REWARD: NEW BITCOIN</Chip>
				</div>
			</AbsoluteFill>

			{/* TWO (b): every 4 years the reward halves; that's why it stops at 21 million */}
			<AbsoluteFill style={{opacity: twoB, transform: push(t, C.fourYears, C.three)}}>
				<Step n="2" title="THE REWARD HALVES" at={C.fourYears - 0.1} />
				<div style={{position: 'absolute', top: 425, left: 60, width: 500, textAlign: 'center', opacity: ease(t, C.fourYears + 0.1)}}>
					<Chip size={28}>⏳ EVERY 4 YEARS: HALF</Chip>
				</div>
				{HALVINGS.map(([amount, year, h], k) => {
					const p = interpolate(t, [C.fourYears + 0.1 + k * stairStep, C.fourYears + 0.5 + k * stairStep], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
					const height = Math.max(22, 360 * h);
					return (
						<div key={year} style={{position: 'absolute', left: 105 + k * 180, width: 150, top: 620, height: 400, opacity: Math.min(1, p * 2)}}>
							<div style={{position: 'absolute', left: 0, right: 0, bottom: 40 + height * p + 8, textAlign: 'center', fontFamily: DISPLAY, fontSize: 46, lineHeight: 1, ...GOLD_TEXT}}>{amount}</div>
							<div style={{position: 'absolute', left: 0, right: 0, bottom: 40, height: height * p, borderRadius: '10px 10px 0 0', background: GOLD_FILL, boxShadow: '0 0 30px rgba(242,173,60,0.2)'}} />
							<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.champagne}}>{year}</div>
						</div>
					);
				})}
				<div style={{position: 'absolute', top: 1032, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, C.fourYears + 0.6)}}>new Bitcoin per block</div>
				<div style={{position: 'absolute', top: 1078, width: '100%', textAlign: 'center', opacity: ease(t, C.max21 - 0.1, 0.2), transform: `scale(${interpolate(usePop(C.max21 - 0.1, 11), [0, 1], [1.5, 1])})`}}>
					<span style={{fontFamily: DISPLAY, fontSize: 96, lineHeight: 1, ...GOLD_TEXT}}>21,000,000 MAX</span>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.champagne}}>the last one: around the year 2140</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="aha" at={C.stops} style={{left: 590, top: 410, width: 420, height: 390}} accent="aha" focus="50% 8%" />

			{/* THREE: your wallet holds keys, not coins; lose the keys, lose the coins, forever */}
			<AbsoluteFill style={{opacity: three, transform: push(t, C.three, C.tip)}}>
				<Step n="3" title="KEYS, NOT COINS" at={C.three} warn />
				<div style={{position: 'absolute', left: 70, top: 440, width: 290, height: 500, borderRadius: 44, background: '#0d0b08', border: '8px solid #2b241a', boxShadow: `0 0 0 2px ${COLORS.gold}, 0 30px 70px rgba(0,0,0,0.6)`, overflow: 'hidden', opacity: ease(t, C.three + 0.15), transform: `translateY(${(1 - ease(t, C.three + 0.15, 0.5)) * 60}px)`}}>
					<div style={{position: 'absolute', top: 12, left: '50%', transform: 'translateX(-50%)', width: 86, height: 22, borderRadius: 11, background: '#000'}} />
					<div style={{position: 'absolute', top: 56, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 24, color: COLORS.goldHi, letterSpacing: 2}}>MY WALLET</div>
					<div style={{position: 'absolute', top: 120, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 12, opacity: fadeOut(t, C.noCoins + 0.1, 0.4)}}>
						{[0, 1, 2].map((i) => <MiniCoin key={i} size={62} />)}
					</div>
					<div style={{position: 'absolute', top: 128, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 28, color: COLORS.muted, opacity: ease(t, C.noCoins + 0.4)}}>no coins in here</div>
					<div style={{position: 'absolute', top: 225, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: ease(t, C.keys - 0.1, 0.3) * (1 - keyGone), transform: `translateY(${keyGone * 300}px) rotate(${-18 + keyGone * 70}deg) scale(${interpolate(usePop(C.keys - 0.1, 11), [0, 1], [0.5, 1])})`}}>
						<Key size={210} glow={ease(t, C.keys, 0.5)} />
					</div>
					<div style={{position: 'absolute', top: 350, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.goldHi, opacity: ease(t, C.keys + 0.3) * (1 - keyGone)}}>🔑 your keys</div>
					<div style={{position: 'absolute', top: 250, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 52, color: '#ff8a4c', opacity: ease(t, C.lose1 + 0.8)}}>KEYS LOST</div>
				</div>
				<div style={{position: 'absolute', left: 400, right: 40, top: 432, textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: 2, color: COLORS.champagne, opacity: ease(t, C.three + 0.5)}}>THE SHARED RECORD</div>
				<div style={{position: 'absolute', left: 400, right: 40, top: 560, display: 'flex', justifyContent: 'center', alignItems: 'center', opacity: ease(t, C.three + 0.4), filter: `grayscale(${locked * 0.85}) brightness(${1 - locked * 0.35})`}}>
					{[0, 1].map((i) => (
						<React.Fragment key={i}>
							{i > 0 && <div style={{width: 36, height: 12, borderRadius: 6, background: COLORS.gold}} />}
							<div style={{position: 'relative'}}>
								<Block3D w={200} h={170} d={140} rotY={-24} label="₿" sub="YOUR COINS" />
							</div>
						</React.Fragment>
					))}
				</div>
				<div style={{position: 'absolute', left: 400, right: 40, top: 575, textAlign: 'center', fontSize: 150, opacity: locked, transform: `scale(${interpolate(usePop(C.lose2 + 0.1, 11), [0, 1], [1.8, 1])})`}}>🔒</div>
				<div style={{position: 'absolute', left: 400, right: 40, top: 790, textAlign: 'center', opacity: win(t, C.noCoins + 0.5, C.lose2, 0.25)}}>
					<Chip size={30}>YOUR COINS LIVE HERE</Chip>
				</div>
				<div style={{position: 'absolute', left: 400, right: 40, top: 870, textAlign: 'center', opacity: win(t, C.prove - 0.1, C.lose1 + 0.2, 0.25)}}>
					<Chip size={30} style={{borderColor: COLORS.goldHi}}>🔑 = PROOF THEY'RE YOURS</Chip>
				</div>
				<div style={{position: 'absolute', left: 400, right: 40, top: 800, textAlign: 'center', opacity: ease(t, C.lose2 + 0.3)}}>
					<Chip size={36} style={{borderColor: RED, color: '#ff9a63'}}>🔒 LOCKED OUT</Chip>
				</div>
				<div style={{position: 'absolute', left: 470, right: 40, top: 985, textAlign: 'center', opacity: ease(t, C.forever - 0.05, 0.15)}}>
					<span style={{display: 'inline-block', transform: `rotate(-7deg) scale(${interpolate(usePop(C.forever - 0.05, 11), [0, 1], [1.7, 1])})`, border: `8px solid ${RED}`, color: '#ff8a4c', fontFamily: DISPLAY, fontSize: 124, lineHeight: 1.15, padding: '0 34px', borderRadius: 14, background: 'rgba(5,4,3,0.8)'}}>FOREVER</span>
				</div>
			</AbsoluteFill>
			<LeoMoment m="mindblown" at={C.forever + 0.2} seconds={Math.min(2.0, C.tip - C.forever - 0.5)} style={{left: 60, top: 960, width: 380, height: 270}} focus="50% 4%" />

			{/* MTG'S TIP: learn before you buy; never trust anyone who guarantees profits */}
			<AbsoluteFill style={{opacity: tip, transform: push(t, C.tip, C.q)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, C.tip - 0.1), transform: `scale(${interpolate(usePop(C.tip - 0.1, 12), [0, 1], [0.8, 1])})`}}>
					<Chip size={46}>💡 MTG'S TIP</Chip>
				</div>
				<div style={{position: 'absolute', left: 500, top: 470, opacity: ease(t, C.tip + 0.2)}}>
					<Notepad3D w={520} t={t} title="MY NOTES" lines={[['1. Learn before I buy ✓', C.learn], ['2. Guarantees = red flag 🚩', C.never + 0.4]]} />
				</div>
				<div style={{position: 'absolute', top: 1010, width: '100%', textAlign: 'center', opacity: ease(t, C.guarantees - 0.2)}}>
					<Chip size={38} style={{borderColor: RED, color: '#ffb48a'}}>🚩 "GUARANTEED PROFITS"? WALK AWAY</Chip>
				</div>
				<div style={{position: 'absolute', top: 1140, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 700, fontSize: 28, color: COLORS.muted, opacity: ease(t, C.tip + 0.6)}}>Education only, not financial advice</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.tip} style={{left: 60, top: 440, width: 410, height: 520}} accent="relief" focus="50% 10%" />
			<LeoMoment m="point" at={C.never} seconds={Math.min(2.6, C.q - C.never - 0.4)} style={{left: 60, top: 440, width: 410, height: 520}} focus="50% 10%" sound={null} />

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.q} seconds={Math.min(4.2, C.send - C.q - 0.1)} frame="tall" sound="chime" accent="none" />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={36} style={{background: 'rgba(5,4,3,0.9)'}}>WHAT CONFUSES YOU ABOUT BITCOIN? 💬</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Ask below. I'll answer in my next videos" size={34} t={t} at={C.askBelow} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.send + 0.5)}}>who still doesn't get Bitcoin</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.join - C.send - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pills={['tutorials', 'explainers', 'streams', 'crypto', 'ai']} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.32], [1.2, 'coin', 0.3], [C.nMax + 0.1, 'count', 0.22], [C.nOut + 0.1, 'swell', 0.3], [C.n3, 'tick', 0.3], [C.loseAll, 'thud', 0.35],
					[C.one, 'pluck1', 0.35], [C.record - 0.1, 'paper', 0.3], [C.computers + 0.15, 'ping', 0.45], [C.noBank + 0.15, 'drop', 0.3], [C.govt + 0.15, 'drop', 0.3],
					[C.two, 'pluck2', 0.35], [C.tenMin - 0.1, 'tick', 0.28], [C.block - 0.05, 'link', 0.5], [C.earn, 'coin', 0.4],
					[C.fourYears, 'pluck1', 0.3], [C.fourYears + 0.1, 'halve', 0.38], ...stairCues, [C.max21 - 0.1, 'reveal', 0.42],
					[C.three, 'pluck3', 0.35], [C.noCoins + 0.1, 'drop', 0.28], [C.keys - 0.1, 'key', 0.45], [C.lose1 + 0.15, 'melt', 0.35], [C.lose2 + 0.1, 'thud', 0.42], [C.forever - 0.05, 'thud', 0.5],
					[C.tip - 0.1, 'glow', 0.32], [C.learn, 'scribble', 0.42], [C.never + 0.4, 'scribble', 0.42], [C.guarantees - 0.2, 'drop', 0.3],
					[C.askBelow, 'pluck2', 0.3], [C.send, 'pluck3', 0.32],
					[C.join - 0.15, 'glow', 0.35], [C.im - 0.1, 'air', 0.25],
				]}
			/>
			<Html5Audio src={staticFile('videos/05/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover05: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 40%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={46}>IN 50 SECONDS</Chip>
		</div>
		<div style={{position: 'absolute', top: 372, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 150, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>
			HOW BITCOIN<br /><span style={{...GOLD_TEXT, textShadow: 'none', filter: 'drop-shadow(0 6px 18px rgba(0,0,0,0.8))'}}>REALLY WORKS</span>
		</div>
		<div style={{position: 'absolute', left: 70, top: 760}}>
			<Coin3D size={420} rotY={-28} rotX={8} glow={0.6} />
		</div>
		<div style={{position: 'absolute', top: 730, left: 560, width: 450, height: 500, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V3-aha.png')} style={{width: 450, height: 788, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1262, width: '100%', textAlign: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 116, lineHeight: 1, ...GOLD_TEXT}}>21,000,000 MAX</div>
			<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 42, color: '#fff', marginTop: 8}}>3 things nobody explained to you</div>
		</div>
		<div style={{position: 'absolute', top: 1470, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={180} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

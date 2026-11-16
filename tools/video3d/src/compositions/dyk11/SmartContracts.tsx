import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Easing, Html5Audio, Img, interpolate, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/11/captions.json';
import C from '../../../public/videos/11/cues.json';
import timeline from '../../../public/videos/11/timeline.json';
import W from '../../../public/videos/11/words.json';
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

// Video 11 (16 Nov 2026, daily video): Did You Know a Contract Can Run Itself? Smart contracts through a vending machine,
// where that picture stops (a live contract usually can't be fixed), and one Crypto 101 tip: never approve what you
// don't understand. Calm and informative: the risk is named once, then the tip. Script and research:
// tools/videos/11-did-you-know-smart-contracts/. Every time is a named cue from the voice's own word timings
// (public/videos/11/cues.json).
// Facts on screen: DeFi total value locked $71.6 billion on 16 November 2026 (DefiLlama); Nick Szabo coined "smart
// contract" in 1994 and used the vending machine picture (ethereum.org); code can't be changed once created
// (ethereum.org, for non-upgradeable contracts, hence "usually").

export const DYK11_FPS = 30;
// the banked deep slogan (MTG, 16 November 2026): the start of each of its four words, for the end screen and the sound
const SLOGAN = W.words.slice(-4).map((w) => w.start);
const captions = captionsJson as Caption[];
const TAIL = closingTail(captions[captions.length - 1].endMs / 1000, timeline.total);
export const DYK11_FRAMES = Math.ceil((timeline.total + TAIL) * DYK11_FPS);
const win = (t: number, a: number, b: number, d = 0.35) => Math.min(ease(t, a, d), fadeOut(t, b, d));
const push = (t: number, a: number, b: number) => `scale(${interpolate(t, [a, b], [1, 1.035], clamp)})`;
const GOLD_FILL = `linear-gradient(145deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`;
const outCubic = {...clamp, easing: Easing.out(Easing.cubic)};
const inCubic = {...clamp, easing: Easing.in(Easing.quad)};

const CAN_COLORS = ['#c0392b', '#2e86c1', '#f2ad3c', '#27ae60', '#8e44ad', '#e67e22'];

/**
 * A vending machine (an original drawing). `keys` 0..1 lights the keypad, `drop` 0..1 moves the chosen can (row 1,
 * column 1) from its shelf into the tray, `glow` lights the machine.
 */
const VendingMachine: React.FC<{w: number; keys?: number; drop?: number; glow?: number; label?: string}> = ({w, keys = 0, drop = 0, glow = 0, label = 'B2'}) => {
	const h = w * 1.7;
	const shelfY = [58, 138, 218, 298];
	const can = (x: number, y: number, c: string, k: string, o = 1) => (
		<g key={k} opacity={o}>
			<rect x={x - 15} y={y - 30} width={30} height={56} rx={7} fill={c} />
			<rect x={x - 15} y={y - 30} width={30} height={10} rx={5} fill="#d9d9d9" opacity={0.85} />
			<rect x={x - 9} y={y - 12} width={6} height={30} rx={3} fill="#fff" opacity={0.28} />
		</g>
	);
	const dropY = interpolate(drop, [0, 1], [shelfY[1], 432], inCubic);
	return (
		<svg width={w} height={h} viewBox="0 0 300 510" style={{filter: `drop-shadow(0 26px 40px rgba(0,0,0,0.6)) drop-shadow(0 0 ${40 * glow}px rgba(242,173,60,${0.5 * glow}))`}}>
			<defs>
				<linearGradient id="vm11body" x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor="#2c2318" />
					<stop offset="1" stopColor="#120d08" />
				</linearGradient>
				<linearGradient id="vm11glass" x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor="#1d2a33" />
					<stop offset="1" stopColor="#0b1116" />
				</linearGradient>
			</defs>
			<rect x="4" y="4" width="292" height="502" rx="22" fill="url(#vm11body)" stroke={COLORS.gold} strokeWidth="4" />
			<rect x="20" y="22" width="186" height="352" rx="10" fill="url(#vm11glass)" stroke="rgba(242,173,60,0.5)" strokeWidth="2" />
			{shelfY.map((y, r) => (
				<g key={r}>
					<rect x="24" y={y + 28} width="178" height="5" rx="2" fill="rgba(242,173,60,0.55)" />
					{[0, 1, 2].map((cIdx) => {
						const chosen = r === 1 && cIdx === 1;
						return can(56 + cIdx * 57, y, CAN_COLORS[(r * 3 + cIdx) % CAN_COLORS.length], `${r}-${cIdx}`, chosen ? 0 : 1);
					})}
				</g>
			))}
			{/* the glass shine */}
			<path d="M30 30 L90 30 L40 360 L30 360 Z" fill="#fff" opacity="0.06" />
			{/* the side panel: display, keypad, coin slot */}
			<rect x="216" y="30" width="66" height="40" rx="6" fill="#0a0806" stroke="rgba(242,173,60,0.6)" strokeWidth="2" />
			<text x="249" y="58" textAnchor="middle" fontFamily="monospace" fontWeight="700" fontSize="22" fill={keys > 0.95 ? COLORS.goldHi : '#5a4a30'}>{keys > 0.3 ? label.slice(0, keys > 0.65 ? 2 : 1) : '--'}</text>
			{Array.from({length: 9}).map((_, i) => {
				const lit = (i === 1 && keys > 0.3) || (i === 4 && keys > 0.65);
				return <rect key={i} x={222 + (i % 3) * 19} y={84 + Math.floor(i / 3) * 19} width="15" height="15" rx="4" fill={lit ? COLORS.goldHi : '#3a3024'} stroke="rgba(242,173,60,0.5)" strokeWidth="1" />;
			})}
			<rect x="236" y="160" width="26" height="44" rx="6" fill="#0a0806" stroke={COLORS.gold} strokeWidth="2" />
			<rect x="246" y="168" width="6" height="28" rx="3" fill="#2a2116" />
			<text x="249" y="226" textAnchor="middle" fontFamily="sans-serif" fontWeight="700" fontSize="13" fill={COLORS.champagne}>PAY</text>
			{/* the tray */}
			<rect x="30" y="398" width="170" height="78" rx="10" fill="#0a0806" stroke="rgba(242,173,60,0.6)" strokeWidth="2" />
			<rect x="30" y="398" width="170" height="16" rx="8" fill="#2a2116" />
			{drop > 0 && drop < 1 && <g clipPath="none">{can(113, dropY, CAN_COLORS[4], 'falling')}</g>}
			{drop >= 1 && <g transform="rotate(-90 113 450)">{can(113, 450, CAN_COLORS[4], 'tray')}</g>}
		</svg>
	);
};

/** A slim phone (gold-titanium rim, thin black bezel, camera island) with a wallet's approval request on screen. */
const WalletPhone: React.FC<{w: number; t: number; decide: number; hover: number}> = ({w, t, decide, hover}) => {
	const h = w * 2.05;
	const finger = interpolate(hover, [0, 1], [0, 1], clamp);
	return (
		<div style={{width: w, height: h, borderRadius: w * 0.14, padding: 3, background: `linear-gradient(150deg, #f6e2b0, ${COLORS.gold} 40%, #8a6424 70%, #f2d390)`, boxShadow: '0 30px 70px rgba(0,0,0,0.7)', position: 'relative'}}>
			<div style={{width: '100%', height: '100%', borderRadius: w * 0.13, background: '#000', padding: 9, boxSizing: 'border-box'}}>
				<div style={{width: '100%', height: '100%', borderRadius: w * 0.11, background: 'linear-gradient(180deg, #17120c, #0b0907)', position: 'relative', overflow: 'hidden', fontFamily: BODY}}>
					<div style={{position: 'absolute', top: 12, left: '50%', width: w * 0.3, height: 26, marginLeft: -w * 0.15, borderRadius: 13, background: '#000'}} />
					<div style={{position: 'absolute', top: 58, width: '100%', textAlign: 'center', fontWeight: 800, fontSize: 22, color: COLORS.muted}}>👛 My Wallet</div>
					<div style={{position: 'absolute', top: 104, left: 20, right: 20, borderRadius: 22, background: 'rgba(255,255,255,0.06)', border: '1.5px solid rgba(242,173,60,0.4)', padding: '20px 18px'}}>
						<div style={{fontWeight: 800, fontSize: 26, color: COLORS.text}}>Signature request</div>
						<div style={{fontWeight: 700, fontSize: 19, color: COLORS.muted, marginTop: 6}}>unknown-site.app</div>
						<div style={{marginTop: 18, fontWeight: 800, fontSize: 24, lineHeight: 1.3, color: COLORS.champagne}}>Allow this site to spend <span style={{color: COLORS.goldHi}}>all</span> your tokens?</div>
						<div style={{marginTop: 14, fontFamily: MONO, fontSize: 15, lineHeight: 1.45, color: '#7d7466', wordBreak: 'break-all'}}>0x095ea7b3 000000000 7a250d56 ffffffff ffffffff ffffffff</div>
					</div>
					<div style={{position: 'absolute', bottom: 60, left: 20, right: 20, display: 'flex', gap: 14}}>
						<div style={{flex: 1, height: 64, borderRadius: 32, border: `2.5px solid ${decide > 0.5 ? COLORS.goldHi : 'rgba(242,173,60,0.6)'}`, background: decide > 0.5 ? 'rgba(242,173,60,0.18)' : 'transparent', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: 24, color: COLORS.text, boxShadow: `0 0 ${30 * decide}px rgba(242,173,60,0.55)`, transform: `scale(${1 + 0.06 * decide})`}}>{decide > 0.5 ? '✓ Reject' : 'Reject'}</div>
						<div style={{flex: 1, height: 64, borderRadius: 32, background: GOLD_FILL, opacity: 1 - 0.65 * decide, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: 24, color: '#2a1a05'}}>Approve</div>
					</div>
					{/* a finger that hovers over Approve, then moves to Reject */}
					<div style={{position: 'absolute', bottom: 8, fontSize: 56, lineHeight: 1, left: interpolate(decide, [0, 1], [w * 0.62, w * 0.2]), opacity: finger, transform: `translateY(${Math.sin(t * 3) * 5}px)`}}>👆</div>
				</div>
			</div>
		</div>
	);
};

const Struck: React.FC<{icon: string; label: string; t: number; at: number}> = ({icon, label, t, at}) => {
	const p = usePop(at, 12);
	const cut = interpolate(t, [at + 0.25, at + 0.55], [0, 1], outCubic);
	return (
		<div style={{width: 280, textAlign: 'center', opacity: Math.min(1, p * 1.6), transform: `scale(${0.6 + 0.4 * p})`}}>
			<div style={{position: 'relative', display: 'inline-block'}}>
				<div style={{width: 170, height: 170, borderRadius: '50%', background: 'rgba(18,14,9,0.95)', border: `3px solid ${COLORS.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 96, lineHeight: 1, filter: `grayscale(${0.6 * cut})`}}>{icon}</div>
				<div style={{position: 'absolute', left: -6, top: 81, width: 182 * cut, height: 9, borderRadius: 5, background: GOLD_FILL, transform: 'rotate(-35deg)', transformOrigin: '50% 50%', boxShadow: '0 0 16px rgba(242,173,60,0.7)', marginLeft: 0}} />
			</div>
			<div style={{fontFamily: DISPLAY, fontSize: 46, lineHeight: 1, color: '#fff', marginTop: 14}}>NO {label}</div>
		</div>
	);
};

export const SmartContracts: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const t = useT();
	const hook = fadeOut(t, C.think - 0.3, 0.3);
	const vend = win(t, C.think - 0.15, C.aSmart - 0.3, 0.3);
	const code = win(t, C.aSmart - 0.15, C.but - 0.3, 0.3);
	const stop = win(t, C.but - 0.15, C.tip - 0.3, 0.3);
	const tip = win(t, C.tip - 0.15, C.did - 0.3, 0.3);
	const ask = win(t, C.did - 0.1, C.send - 0.2, 0.25);
	const share = win(t, C.send - 0.05, C.join - 0.3, 0.3);

	const billions = Math.round(interpolate(t, [C.about, C.billion + 0.4], [0, 70], outCubic));
	const coin = interpolate(t, [C.pay - 0.15, C.pay + 0.45], [0, 1], outCubic);
	const keys = interpolate(t, [C.pick - 0.05, C.pick + 0.5], [0, 1], clamp);
	const drop = interpolate(t, [C.drops - 0.05, C.drops + 0.4], [0, 1], clamp);
	const typed = (s: string, a: number, d = 0.7) => s.slice(0, Math.round(interpolate(t, [a, a + d], [0, s.length], clamp)));
	const decide = interpolate(t, [C.sign - 0.1, C.sign + 0.35], [0, 1], outCubic);

	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />

			{/* HOOK: no lawyer, no bank, no handshake; about $70 billion locked in them; they're called smart contracts */}
			<AbsoluteFill style={{opacity: hook, transform: push(t, 0, C.think)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={40}>DID YOU KNOW? 🤔</Chip>
				</div>
				<div style={{position: 'absolute', top: 392, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 14, opacity: fadeOut(t, C.called - 0.25, 0.3)}}>
					<Struck icon="⚖️" label="LAWYER" t={t} at={C.lawyer - 0.15} />
					<Struck icon="🏦" label="BANK" t={t} at={C.bank - 0.15} />
					<Struck icon="🤝" label="HANDSHAKE" t={t} at={C.handshake - 0.15} />
				</div>
				<div style={{position: 'absolute', top: 680, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, C.about - 0.1), fadeOut(t, C.called - 0.25, 0.3))}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: 3, color: COLORS.goldHi}}>LOCKED IN THEM RIGHT NOW</div>
					<div style={{fontFamily: DISPLAY, fontSize: 210, lineHeight: 1.02, ...GOLD_TEXT}}>${billions} BILLION</div>
					<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 26, color: COLORS.muted, opacity: ease(t, C.locked)}}>DeFi total value locked: $71.6 billion (DefiLlama, 16 Nov 2026)</div>
				</div>
				{/* "They're called smart contracts": the title and a gold 3D contract block */}
				<div style={{position: 'absolute', top: 400, width: '100%', textAlign: 'center', opacity: ease(t, C.called - 0.1), transform: `scale(${interpolate(usePop(C.called - 0.1, 12), [0, 1], [0.8, 1])})`}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 32, letterSpacing: 4, color: COLORS.champagne}}>THEY'RE CALLED</div>
					<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT}}>SMART</div>
					<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, color: '#fff'}}>CONTRACTS</div>
				</div>
				<div style={{position: 'absolute', left: 400, top: 820, opacity: ease(t, C.smartC), transform: `translateY(${(1 - ease(t, C.smartC, 0.5)) * 60}px)`}}>
					<Block3D w={280} h={200} d={160} rotX={-14} rotY={interpolate(t, [C.smartC, C.think], [-60, -24])} label="📜" sub="runs itself" />
				</div>
			</AbsoluteFill>
			<LeoMoment m="wow" at={C.billion + 0.45} seconds={Math.min(1.5, C.called - C.billion - 0.7)} style={{left: 340, top: 980, width: 400, height: 240}} accent="wow" sound={null} />

			{/* A VENDING MACHINE: you pay, you pick, the drink drops; no cashier; the rules live inside the machine */}
			<AbsoluteFill style={{opacity: vend, transform: push(t, C.think, C.aSmart)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>THINK OF A VENDING MACHINE</Chip>
				</div>
				<div style={{position: 'absolute', left: 70, top: 390, opacity: ease(t, C.vending - 0.2), transform: `perspective(1400px) rotateY(${interpolate(t, [C.vending - 0.2, C.vending + 0.8], [40, 12], outCubic)}deg)`}}>
					<VendingMachine w={460} keys={keys} drop={drop} glow={ease(t, C.inside - 0.2, 0.5)} />
				</div>
				{/* the coin going into the slot */}
				<div style={{position: 'absolute', left: interpolate(coin, [0, 1], [560, 444]), top: interpolate(coin, [0, 1], [430, 690]), width: 54, height: 54, borderRadius: '50%', background: GOLD_FILL, border: '3px solid #fff1c4', opacity: Math.min(ease(t, C.pay - 0.15, 0.15), 1 - interpolate(coin, [0.85, 1], [0, 1], clamp)), boxShadow: '0 0 18px rgba(242,173,60,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 30, color: '#2a1a05'}}>$</div>
				<div style={{position: 'absolute', left: 600, right: 40, top: 400, display: 'flex', flexDirection: 'column', gap: 16}}>
					{[['🪙', '1. Pay', C.pay], ['⌨️', '2. Pick', C.pick], ['🥤', '3. Drop', C.drops]].map(([icon, text, at]) => (
						<HintPill key={text as string} icon={icon as string} text={text as string} size={44} t={t} at={(at as number) - 0.1} />
					))}
				</div>
				<div style={{position: 'absolute', left: 600, right: 40, top: 730, fontFamily: DISPLAY, fontSize: 64, lineHeight: 1.02, color: '#fff', opacity: ease(t, C.cashier - 0.1)}}>
					NO CASHIER<br /><span style={GOLD_TEXT}>NEEDED</span>
				</div>
				<div style={{position: 'absolute', left: 600, right: 40, top: 940, opacity: ease(t, C.rules - 0.1)}}>
					<Panel style={{padding: '18px 20px', background: 'rgba(18,14,9,0.95)'}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: 2, color: COLORS.goldHi}}>THE RULES</div>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 32, lineHeight: 1.2, color: COLORS.text}}>live inside the machine ⚙️</div>
					</Panel>
				</div>
			</AbsoluteFill>
			<LeoMoment m="smile" at={C.drops + 0.35} seconds={Math.min(1.5, C.rules - C.drops - 0.45)} style={{left: 620, top: 920, width: 360, height: 260}} accent="warm" sound={null} />

			{/* A SMART CONTRACT: the same idea in code, on a blockchain; if this happens, then do that; open and the same for all */}
			<AbsoluteFill style={{opacity: code, transform: push(t, C.aSmart, C.but)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>A SMART CONTRACT</Chip>
				</div>
				<div style={{position: 'absolute', top: 384, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 76, lineHeight: 1, color: '#fff', opacity: ease(t, C.code - 0.1)}}>
					THE SAME IDEA, <span style={GOLD_TEXT}>IN CODE</span>
				</div>
				<div style={{position: 'absolute', top: 500, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 6}}>
					{['BLOCK', '📜', 'BLOCK'].map((label, i) => {
						const p = ease(t, C.chain - 0.15 + i * 0.12, 0.4);
						return (
							<React.Fragment key={i}>
								{i > 0 && <div style={{width: 40, height: 8, borderRadius: 4, background: COLORS.gold, opacity: p}} />}
								<div style={{opacity: p, transform: `translateY(${(1 - p) * 40}px)`}}>
									<Block3D w={i === 1 ? 190 : 160} h={i === 1 ? 150 : 124} d={110} rotX={-14} rotY={-22 + Math.sin(t * 1.1 + i) * 6} tone={i === 1 ? 'gold' : 'dark'} label={label} sub={i === 1 ? 'contract' : undefined} />
								</div>
							</React.Fragment>
						);
					})}
				</div>
				<div style={{position: 'absolute', left: 70, right: 70, top: 700}}>
					<Flip at={C.ifThis - 0.1}>
						<Panel style={{padding: '24px 30px', background: 'rgba(10,8,6,0.97)'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 46, lineHeight: 1.35, color: COLORS.text, minHeight: 124}}>
								<span style={{color: COLORS.goldHi}}>IF</span> {typed('this happens', C.ifThis + 0.1, 0.6)}
								<br />
								{t > C.then - 0.1 && (
									<>
										<span style={{color: COLORS.goldHi}}>THEN</span> {typed('do that', C.then, 0.4)}
									</>
								)}
							</div>
							<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 28, color: COLORS.muted, marginTop: 10, opacity: ease(t, C.then + 0.4)}}>Example: if the payment arrives, then the ticket is sent.</div>
						</Panel>
					</Flip>
				</div>
				<div style={{position: 'absolute', top: 1040, left: 30, right: 30, display: 'flex', justifyContent: 'center', gap: 14}}>
					<HintPill icon="👀" text="Anyone can check" size={36} t={t} at={C.anyone - 0.05} />
					<HintPill icon="⚖️" text="Same for everyone" size={36} t={t} at={C.same - 0.1} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="think" at={C.aSmart + 0.05} seconds={Math.min(2.6, C.ifThis - C.aSmart - 0.3)} style={{left: 360, top: 720, width: 360, height: 290}} focus="50% 12%" sound={null} />

			{/* WHERE THE PICTURE STOPS: a broken machine gets fixed; a live contract usually can't be; a mistake stays */}
			<AbsoluteFill style={{opacity: stop, transform: push(t, C.but, C.tip)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>WHERE THE PICTURE STOPS</Chip>
				</div>
				<div style={{position: 'absolute', top: 400, left: 60, right: 60, display: 'flex', gap: 26}}>
					<div style={{flex: 1}}>
						<Flip at={C.broken - 0.1}>
							<Panel style={{padding: '22px 18px', textAlign: 'center', height: 440, boxSizing: 'border-box'}}>
								<div style={{position: 'relative', height: 262, display: 'flex', justifyContent: 'center'}}>
									<VendingMachine w={150} />
									<div style={{position: 'absolute', right: 40, top: 110, fontSize: 84, lineHeight: 1, opacity: ease(t, C.fixed - 0.2), transform: `rotate(${Math.sin(t * 6) * 18 * ease(t, C.fixed - 0.2)}deg)`}}>🔧</div>
								</div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.champagne, marginTop: 16}}>Vending machine</div>
								<div style={{fontFamily: DISPLAY, fontSize: 60, lineHeight: 1.05, color: '#fff', opacity: ease(t, C.fixed - 0.1)}}>GETS FIXED ✅</div>
							</Panel>
						</Flip>
					</div>
					<div style={{flex: 1}}>
						<Flip at={C.usually - 0.6}>
							<Panel style={{padding: '22px 18px', textAlign: 'center', height: 440, boxSizing: 'border-box', borderColor: COLORS.goldHi}}>
								<div style={{position: 'relative', height: 262, display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
									<Block3D w={170} h={150} d={120} rotX={-14} rotY={-26} label="📜" sub="live" />
									<div style={{position: 'absolute', right: 20, top: 120, fontSize: 76, lineHeight: 1, opacity: ease(t, C.usually), transform: `scale(${interpolate(usePop(C.usually, 11), [0, 1], [1.6, 1])})`}}>🔒</div>
								</div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 30, color: COLORS.champagne, marginTop: 16}}>Smart contract</div>
								<div style={{fontFamily: DISPLAY, fontSize: 52, lineHeight: 1.05, ...GOLD_TEXT, opacity: ease(t, C.usually - 0.05)}}>USUALLY CAN'T BE</div>
							</Panel>
						</Flip>
					</div>
				</div>
				<div style={{position: 'absolute', top: 872, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 72, lineHeight: 1.05, color: COLORS.champagne, opacity: ease(t, C.mistake - 0.2)}}>
					A MISTAKE IN THE CODE <span style={{color: '#fff'}}>STAYS</span>
				</div>
			</AbsoluteFill>
			<LeoMoment m="worried" at={C.stays - 0.05} seconds={Math.min(1.25, C.tip - C.stays - 0.1)} style={{left: 340, top: 960, width: 400, height: 250}} sound={null} />

			{/* ONE TIP: never approve anything in your wallet you don't understand; can't explain it? don't sign it */}
			<AbsoluteFill style={{opacity: tip, transform: push(t, C.tip, C.did)}}>
				<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center'}}>
					<Chip size={40}>💡 ONE TIP</Chip>
				</div>
				<div style={{position: 'absolute', left: 60, width: 500, top: 390, fontFamily: DISPLAY, fontSize: 70, lineHeight: 1.04, color: '#fff', opacity: ease(t, C.never - 0.15)}}>
					NEVER APPROVE<br />WHAT YOU <span style={GOLD_TEXT}>DON'T UNDERSTAND</span>
				</div>
				<div style={{position: 'absolute', left: 600, top: 390, opacity: ease(t, C.wallet - 0.4), transform: `perspective(1400px) rotateY(${interpolate(t, [C.wallet - 0.4, C.wallet + 0.6], [-35, -8], outCubic)}deg)`}}>
					<WalletPhone w={380} t={t} decide={decide} hover={ease(t, C.understand, 0.3)} />
				</div>
				<div style={{position: 'absolute', left: 60, width: 500, top: 830, opacity: ease(t, C.explain - 0.1)}}>
					<Panel style={{padding: '20px 24px', background: 'rgba(18,14,9,0.96)'}}>
						<div style={{fontFamily: DISPLAY, fontSize: 52, lineHeight: 1.08, color: COLORS.champagne}}>CAN'T EXPLAIN IT?</div>
						<div style={{fontFamily: DISPLAY, fontSize: 64, lineHeight: 1.05, ...GOLD_TEXT, opacity: ease(t, C.sign - 0.15)}}>DON'T SIGN IT.</div>
					</Panel>
				</div>
				<div style={{position: 'absolute', left: 60, width: 500, top: 1078, textAlign: 'center'}}>
					<HintPill icon="🔖" text="Save this tip" size={36} t={t} at={C.sign + 0.2} />
				</div>
			</AbsoluteFill>
			<LeoMoment m="reassure" at={C.tip + 0.05} seconds={Math.min(1.35, C.explain - C.tip - 0.2)} style={{left: 70, top: 620, width: 460, height: 340}} accent="relief" focus="50% 8%" />
			<LeoMoment m="thumbsup" at={C.understand - 0.4} seconds={Math.min(1.4, C.explain - C.understand + 0.25)} style={{left: 70, top: 620, width: 460, height: 340}} accent="warm" focus="50% 8%" sound={null} />

			{/* THE QUESTION, then the share prompt */}
			<LeoMoment m="ask" at={C.did} seconds={Math.min(4.2, C.send - C.did - 0.1)} frame="tall" sound={null} />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ask}}>
				<Chip size={40} style={{background: 'rgba(5,4,3,0.9)'}}>DID YOU KNOW THIS? 🤔</Chip>
				<div style={{marginTop: 14}}>
					<HintPill icon="👇" text="Tell me below" size={36} t={t} at={C.tell} />
				</div>
			</div>
			<AbsoluteFill style={{opacity: share}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1.05, color: '#fff', transform: `scale(${interpolate(usePop(C.send, 12), [0, 1], [0.8, 1])})`}}>📤 SEND THIS <span style={GOLD_TEXT}>TO A FRIEND</span></div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 44, color: COLORS.champagne, marginTop: 10, opacity: ease(t, C.coins - 0.8)}}>who thinks crypto is just coins 🪙</div>
				</div>
			</AbsoluteFill>
			<LeoMoment m="winkup" at={C.send + 0.15} seconds={Math.min(2.05, C.coins - C.send)} style={{left: 290, top: 540, width: 500, height: 640}} accent="warm" focus="50% 10%" />
			<LeoMoment m="laugh" at={C.coins + 0.1} seconds={Math.min(2.3, C.join - C.coins - 0.45)} style={{left: 290, top: 540, width: 500, height: 640}} focus="50% 10%" sound={null} />

			{/* THE TRIBE, THE WEBSITE AND THE SIGN-OFF, then the theme's last line */}
			<EndScreen t={t} cardAt={C.join - 0.15} photoAt={C.im - 0.1} sloganAt={C.slogan - 0.05} pillsAt={C.weLearn - 0.35} pills={['crypto', 'wallet', 'ai', 'streams', 'tribe']} sloganWords={SLOGAN} />
			<LeoMoment m="welcome" at={C.site - 0.3} seconds={Math.min(2.1, C.weLearn - C.site - 0.35)} style={{left: 300, top: 630, width: 480, height: 570}} focus="50% 10%" sound={null} />

			{/* sound, fitted to this story and soft (Leo's accents bring their own); the theme plays only its last line */}
			<Cues
				list={[
					[0.1, 'air', 0.3], [C.lawyer - 0.15, 'pluck1', 0.3], [C.lawyer + 0.25, 'paper', 0.24], [C.bank - 0.15, 'pluck2', 0.3], [C.bank + 0.25, 'paper', 0.24], [C.handshake - 0.15, 'pluck3', 0.3], [C.handshake + 0.25, 'paper', 0.24],
					[C.about, 'count', 0.22], [C.billion + 0.4, 'reveal', 0.32], [C.called - 0.1, 'shimmer', 0.34], [C.smartC, 'link', 0.36],
					[C.think - 0.15, 'air', 0.26], [C.vending - 0.2, 'whirr', 0.18], [C.pay - 0.15, 'coin', 0.36], [C.pick - 0.05, 'keypad', 0.42], [C.drops - 0.05, 'vend', 0.6], [C.cashier - 0.1, 'pluck3', 0.26], [C.rules - 0.1, 'glow', 0.3],
					[C.aSmart - 0.15, 'air', 0.26], [C.chain - 0.15, 'link', 0.34], [C.chain + 0.1, 'link', 0.3], [C.ifThis + 0.1, 'typing', 0.4], [C.then, 'typing', 0.36], [C.anyone - 0.05, 'pluck2', 0.28], [C.same - 0.1, 'pluck3', 0.28],
					[C.but - 0.15, 'air', 0.26], [C.broken - 0.1, 'pluck1', 0.28], [C.fixed - 0.2, 'key', 0.32], [C.usually, 'thud', 0.34], [C.mistake - 0.2, 'tension', 0.26],
					[C.tip - 0.15, 'chime', 0.3], [C.wallet - 0.4, 'slide', 0.3], [C.understand, 'tick', 0.3], [C.explain - 0.1, 'pluck2', 0.28], [C.sign - 0.1, 'ping', 0.34], [C.sign + 0.2, 'pluck4', 0.26],
					[C.did, 'chime', 0.3], [C.tell, 'pluck2', 0.28], [C.send, 'pluck3', 0.3],
					[C.join - 0.15, 'glow', 0.35], [C.weLearn - 0.35, 'pluck1', 0.28], [C.im - 0.1, 'air', 0.25], [SLOGAN[3] - 0.02, 'land', 0.42],
				]}
			/>
			<Html5Audio src={staticFile('videos/11/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

/** Cover (9:16): everything inside the 3:4 grid crop (y 240 to 1680). */
export const Cover11: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, #2b1e0c 0%, ${COLORS.bgLift} 45%, ${COLORS.bg} 85%)`}} />
		<div style={{position: 'absolute', top: 270, width: '100%', textAlign: 'center'}}>
			<Chip size={44}>DID YOU KNOW? 🤔</Chip>
		</div>
		<div style={{position: 'absolute', top: 368, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 168, lineHeight: 1.0, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>A CONTRACT</div>
		<div style={{position: 'absolute', top: 534, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 150, lineHeight: 1.0, ...GOLD_TEXT}}>CAN RUN ITSELF</div>
		<div style={{position: 'absolute', left: 90, top: 730}}>
			<VendingMachine w={300} keys={1} drop={1} glow={0.6} />
		</div>
		<div style={{position: 'absolute', left: 404, top: 880, fontFamily: DISPLAY, fontSize: 170, lineHeight: 1, ...GOLD_TEXT}}>=</div>
		<div style={{position: 'absolute', top: 740, left: 560, width: 420, height: 470, borderRadius: 32, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.3)'}}>
			<Img src={staticFile('videos/01/leo/V3-aha.png')} style={{width: 420, height: 736, objectFit: 'cover', objectPosition: '50% 0%'}} />
		</div>
		<div style={{position: 'absolute', top: 1268, width: '100%', display: 'flex', justifyContent: 'center', gap: 22}}>
			{['⚖️ NO LAWYER', '🏦 NO BANK', '🤝 NO HANDSHAKE'].map((x) => (
				<div key={x} style={{padding: '12px 22px', borderRadius: 999, border: `2.5px solid ${COLORS.gold}`, background: 'rgba(18,14,9,0.95)', fontFamily: DISPLAY, fontSize: 44, lineHeight: 1, color: '#fff'}}>{x}</div>
			))}
		</div>
		<div style={{position: 'absolute', top: 1490, left: 80, right: 80, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 36}}>
			<PhotoCard size={170} />
			<UrlPill text="mtgtribe.com/group" size={50} />
		</div>
	</AbsoluteFill>
);

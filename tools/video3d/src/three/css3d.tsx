import React from 'react';
import {COLORS} from '../brand';
import {DISPLAY, MONO} from '../fonts';

// Fast 3D touches (MTG, 10 November 2026: "throw in some 3D effects here and there ... these are supposed to be 3D
// animated videos"). Real 3D objects made from CSS 3D transforms: they render in the browser like any frame, with no
// WebGL and no HeyGen credits, so a whole video still renders in minutes (the full Three.js version took too long).
// Drive every angle from useCurrentFrame() through the props, never from the clock.

/** A thick gold coin with a symbol on both faces; turn it with rotY (degrees). */
export const Coin3D: React.FC<{size: number; symbol?: string; rotY?: number; rotX?: number; thick?: number; glow?: number}> = ({size, symbol = '₿', rotY = 0, rotX = 0, thick = 0.11, glow = 0}) => {
	const layers = 18;
	const T = size * thick;
	const face = (back: boolean): React.CSSProperties => ({
		position: 'absolute', inset: 0, borderRadius: '50%', backfaceVisibility: 'hidden',
		transform: `${back ? 'rotateY(180deg) ' : ''}translateZ(${T / 2 + 0.5}px)`,
		background: `radial-gradient(circle at 35% 30%, ${COLORS.goldHi}, ${COLORS.gold} 55%, #a8701f)`,
		boxShadow: `inset 0 0 0 ${size * 0.035}px rgba(120,75,15,0.55), inset 0 0 ${size * 0.08}px rgba(90,55,10,0.4)`,
		display: 'flex', alignItems: 'center', justifyContent: 'center',
		fontFamily: DISPLAY, fontSize: size * 0.58, color: '#4a2f08', textShadow: '0 2px 0 rgba(255,230,170,0.6)',
	});
	return (
		<div style={{width: size, height: size, perspective: size * 4, filter: `drop-shadow(0 ${size * 0.08}px ${size * 0.1}px rgba(0,0,0,0.55)) drop-shadow(0 0 ${size * 0.25 * glow}px rgba(255,217,142,0.6))`}}>
			<div style={{width: '100%', height: '100%', position: 'relative', transformStyle: 'preserve-3d', transform: `rotateX(${rotX}deg) rotateY(${rotY}deg)`}}>
				{Array.from({length: layers}, (_, i) => (
					<div key={i} style={{position: 'absolute', inset: 0, borderRadius: '50%', transform: `translateZ(${-T / 2 + (i * T) / (layers - 1)}px)`, background: i % 2 ? '#9a6519' : '#b9802a'}} />
				))}
				<div style={face(false)}>{symbol}</div>
				<div style={face(true)}>{symbol}</div>
			</div>
		</div>
	);
};

/** A solid gold block (a cuboid) with a label on the front: blockchain blocks, gold bars, data. */
export const Block3D: React.FC<{w: number; h: number; d: number; rotX?: number; rotY?: number; label?: React.ReactNode; sub?: string; tone?: 'gold' | 'dark'}> = ({w, h, d, rotX = -18, rotY = -28, label, sub, tone = 'gold'}) => {
	const gold = tone === 'gold';
	const base: React.CSSProperties = {position: 'absolute', boxSizing: 'border-box', border: `2px solid ${gold ? 'rgba(110,70,12,0.55)' : 'rgba(242,173,60,0.6)'}`};
	const fill = (shade: number) =>
		gold
			? `linear-gradient(160deg, rgba(255,236,190,${0.25 * shade}), transparent 45%), linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`
			: `linear-gradient(180deg, #2a2116, #120e09)`;
	const faces: Array<[React.CSSProperties, number, React.ReactNode?]> = [
		[{width: w, height: h, transform: `translateZ(${d / 2}px)`}, 1, label],
		[{width: w, height: h, transform: `rotateY(180deg) translateZ(${d / 2}px)`}, 0.6],
		[{width: d, height: h, left: (w - d) / 2, transform: `rotateY(90deg) translateZ(${w / 2}px)`}, 0.55],
		[{width: d, height: h, left: (w - d) / 2, transform: `rotateY(-90deg) translateZ(${w / 2}px)`}, 0.55],
		[{width: w, height: d, top: (h - d) / 2, transform: `rotateX(90deg) translateZ(${h / 2}px)`}, 1.4],
		[{width: w, height: d, top: (h - d) / 2, transform: `rotateX(-90deg) translateZ(${h / 2}px)`}, 0.4],
	];
	return (
		<div style={{width: w, height: h, perspective: Math.max(w, h) * 5, filter: 'drop-shadow(0 18px 24px rgba(0,0,0,0.55))'}}>
			<div style={{width: '100%', height: '100%', position: 'relative', transformStyle: 'preserve-3d', transform: `rotateX(${rotX}deg) rotateY(${rotY}deg)`}}>
				{faces.map(([s, shade, content], i) => (
					<div key={i} style={{...base, ...s, background: fill(shade), filter: `brightness(${0.55 + 0.45 * Math.min(1, shade)})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
						{content !== undefined && (
							<>
								<div style={{fontFamily: DISPLAY, fontSize: typeof content === 'string' ? Math.min(h * 0.34, (w * 0.84) / (content.length * 0.5)) : h * 0.34, lineHeight: 1, color: gold ? '#3a2508' : COLORS.goldHi}}>{content}</div>
								{sub && <div style={{fontFamily: MONO, fontWeight: 700, fontSize: h * 0.13, color: gold ? '#5a3b10' : COLORS.champagne, marginTop: h * 0.05}}>{sub}</div>}
							</>
						)}
					</div>
				))}
			</div>
		</div>
	);
};

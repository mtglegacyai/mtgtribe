import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import {AbsoluteFill, Img, Sequence, staticFile} from 'remotion';
import * as THREE from 'three';
import {COLORS} from '../../brand';
import {PhotoCard} from '../../components/PhotoCard';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {World} from './Hook3D';
import {GOLD_TEXT, Loaf} from './ui';

// Covers (thumbnails) for video 01, 9:16 (1080x1920) for TikTok, Reels and Shorts. TikTok and Instagram show covers
// cropped to 3:4 on profile grids (the middle 1080x1440, y 240 to 1680), so every word, face and number sits there.
// One idea per cover: a shocked face, one big number, a few bold words, MTG's circle photo for trust.

const SAFE_TOP = 240;
const SAFE_BOTTOM = 1680;

const Stamp: React.FC<{children: React.ReactNode; size?: number}> = ({children, size = 60}) => (
	<div style={{display: 'inline-block', transform: 'rotate(-4deg)', border: '6px solid #e0602f', color: '#ff8a4c', fontFamily: DISPLAY, fontSize: size, padding: '4px 22px', borderRadius: 12, background: 'rgba(5,4,3,0.85)', letterSpacing: 1}}>{children}</div>
);

const Arrow: React.FC<{size: number}> = ({size}) => (
	<svg width={size} height={size * 0.6} viewBox="0 0 100 60">
		<path d="M4 30 H78 M58 8 L86 30 L58 52" stroke={COLORS.goldHi} strokeWidth="12" fill="none" strokeLinecap="round" strokeLinejoin="round" />
	</svg>
);

/** Cover for the 2.5D version (v4): Leo shocked next to the loaf, the price jump, "it really happened". */
export const Cover01: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<Img src={staticFile('videos/01/leo/V1-shock.png')} style={{position: 'absolute', left: -60, top: 330, width: 1200, height: 2100, objectFit: 'cover'}} />
		<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,4,3,1) 0%, rgba(5,4,3,0.92) 22%, rgba(5,4,3,0) 40%, rgba(5,4,3,0) 56%, rgba(5,4,3,0.9) 70%, rgba(5,4,3,1) 100%)'}} />
		<div style={{position: 'absolute', top: SAFE_TOP + 30, width: '100%', textAlign: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 132, lineHeight: 0.98, color: '#fff', textShadow: '0 8px 30px rgba(0,0,0,0.9)'}}>WHAT IF PRICES</div>
			<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1.0, ...GOLD_TEXT}}>DOUBLED DAILY?</div>
		</div>
		<div style={{position: 'absolute', top: 1180, width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 18}}>
			<Loaf size={170} />
			<div style={{fontFamily: DISPLAY, fontSize: 116, color: '#fff'}}>R10</div>
			<Arrow size={110} />
			<div style={{fontFamily: DISPLAY, fontSize: 116, ...GOLD_TEXT}}>R10 BILLION</div>
		</div>
		<div style={{position: 'absolute', top: 1340, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 40, letterSpacing: 6, color: COLORS.champagne}}>IN JUST 30 DAYS</div>
		<div style={{position: 'absolute', top: 1440, left: 70}}>
			<Stamp size={70}>IT REALLY HAPPENED</Stamp>
		</div>
		<div style={{position: 'absolute', top: SAFE_BOTTOM - 250, right: 60}}>
			<PhotoCard size={230} />
		</div>
		<div style={{position: 'absolute', bottom: 90, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi}}>mtgtribe.com</div>
	</AbsoluteFill>
);

/** Cover for the real 3D version: the 3D gold price over the mountain of coins, Leo's jaw drop, the question. */
export const Cover01_3D: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<Sequence from={-384} layout="none">
			<ThreeCanvas width={1080} height={1920} gl={{antialias: true, toneMapping: THREE.ACESFilmicToneMapping}} camera={{fov: 42, near: 0.1, far: 80}} shadows>
				<World />
			</ThreeCanvas>
		</Sequence>
		<AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,4,3,0.95) 0%, rgba(5,4,3,0.55) 18%, rgba(5,4,3,0) 30%, rgba(5,4,3,0) 60%, rgba(5,4,3,0.85) 80%, rgba(5,4,3,1) 100%)'}} />
		<div style={{position: 'absolute', top: SAFE_TOP + 10, width: '100%', textAlign: 'center'}}>
			<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1, color: '#fff', textShadow: '0 6px 24px rgba(0,0,0,0.9)'}}>ONE LOAF OF BREAD</div>
		</div>
		<div style={{position: 'absolute', top: 700, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 46, letterSpacing: 6, color: COLORS.champagne, textShadow: '0 4px 18px rgba(0,0,0,0.95)'}}>30 DAYS LATER</div>
		<div style={{position: 'absolute', top: 1180, left: 60, width: 440, height: 440, borderRadius: 36, overflow: 'hidden', border: `5px solid ${COLORS.gold}`, boxShadow: '0 20px 60px rgba(0,0,0,0.7), 0 0 50px rgba(242,173,60,0.35)'}}>
			<Img src={staticFile('videos/01/leo/V3-shock.png')} style={{width: 440, height: 770, objectFit: 'cover', objectPosition: '50% 0%', marginTop: -10}} />
		</div>
		<div style={{position: 'absolute', top: 1200, left: 530, right: 50, textAlign: 'center'}}>
			<Stamp size={58}>IT REALLY HAPPENED</Stamp>
			<div style={{marginTop: 36, display: 'flex', justifyContent: 'center'}}>
				<PhotoCard size={230} />
			</div>
		</div>
		<div style={{position: 'absolute', bottom: 90, width: '100%', textAlign: 'center', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.goldHi}}>mtgtribe.com</div>
	</AbsoluteFill>
);

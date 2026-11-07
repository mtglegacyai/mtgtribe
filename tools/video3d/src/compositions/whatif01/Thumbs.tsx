import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {COLORS} from '../../brand';
import {PhotoCard} from '../../components/PhotoCard';
import {DISPLAY, MONO} from '../../fonts';
import {Backdrop, Chip, GOLD_TEXT, Loaf} from './ui';

// YouTube thumbnails for video 01 (1280x720), two concepts for an A/B test. MTG's photo is always a circle.

export const Thumb01A: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<Backdrop />
		<div style={{position: 'absolute', left: 50, top: 40, fontFamily: DISPLAY, fontSize: 112, lineHeight: 0.95, ...GOLD_TEXT, textShadow: 'none'}}>
			DOUBLED<br />EVERY DAY
		</div>
		<div style={{position: 'absolute', left: 60, bottom: 50, display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 10}}>
			<div style={{display: 'flex', alignItems: 'flex-end', gap: 22}}>
				<Loaf size={250} />
				<Chip size={26}>30 DAYS LATER</Chip>
			</div>
			<div style={{fontFamily: DISPLAY, fontSize: 104, color: '#fff', textShadow: '0 6px 20px rgba(0,0,0,0.8)'}}>R10,737,418,240</div>
		</div>
		<div style={{position: 'absolute', right: 50, top: 70}}>
			<PhotoCard size={380} />
		</div>
	</AbsoluteFill>
);

export const Thumb01B: React.FC = () => (
	<AbsoluteFill style={{background: COLORS.bg}}>
		<Img src={staticFile('videos/01/leo/L3-frame.png')} style={{position: 'absolute', right: -60, top: 0, height: 720, width: 1260, objectFit: 'cover', objectPosition: '65% 30%'}} />
		<AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(5,4,3,0.95) 0%, rgba(5,4,3,0.85) 38%, rgba(5,4,3,0) 62%)'}} />
		<div style={{position: 'absolute', left: 50, top: 60}}>
			<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.goldHi, letterSpacing: 3}}>ONE BANKNOTE</div>
			<div style={{fontFamily: DISPLAY, fontSize: 160, lineHeight: 0.95, ...GOLD_TEXT}}>14<br />ZEROS</div>
			<div style={{fontFamily: DISPLAY, fontSize: 52, color: '#fff', marginTop: 8}}>IT REALLY HAPPENED</div>
		</div>
		<div style={{position: 'absolute', left: 50, bottom: 26}}>
			<PhotoCard size={165} />
		</div>
	</AbsoluteFill>
);

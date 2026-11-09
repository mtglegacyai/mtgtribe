import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {EndScreen} from '../../components/EndScreen';
import {Block3D, Coin3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, ease, fadeOut, useT} from '../whatif01/ui';

// A silent preview of the upgrades MTG asked for on 10 November 2026: fast CSS 3D touches (a thick gold coin, solid
// blocks joining a chain) and the new end: tribe pill, website pills, signature and the big gold website pill.
export const NEWLOOK_FRAMES = 30 * 11;

export const NewLook: React.FC = () => {
	const t = useT();
	const s1 = fadeOut(t, 3.9, 0.35);
	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />
			<AbsoluteFill style={{opacity: s1}}>
				<div style={{position: 'absolute', top: 300, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
					<Chip size={40}>HOW BITCOIN REALLY WORKS</Chip>
				</div>
				<div style={{position: 'absolute', left: 540 - 210, top: 420, opacity: ease(t, 0.2, 0.5)}}>
					<Coin3D size={420} rotY={t * 140} rotX={10} glow={0.6} />
				</div>
				<div style={{position: 'absolute', top: 960, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 0}}>
					{[0, 1, 2].map((i) => {
						const p = ease(t, 1.2 + i * 0.5, 0.5);
						return (
							<React.Fragment key={i}>
								{i > 0 && <div style={{width: 46, height: 14, borderRadius: 7, background: COLORS.gold, opacity: p, transform: `scaleX(${p})`}} />}
								<div style={{opacity: p, transform: `translateY(${(1 - p) * -120}px)`}}>
									<Block3D w={230} h={200} d={160} rotY={interpolate(t, [0, 4], [-38, -18], clamp)} label={`#${939_998 + i}`} sub="BLOCK" />
								</div>
							</React.Fragment>
						);
					})}
				</div>
			</AbsoluteFill>
			<EndScreen t={t} cardAt={4.0} photoAt={6.6} sloganAt={8.0} pills={['tutorials', 'explainers', 'streams', 'crypto', 'ai']} />
			<BrandBar />
		</AbsoluteFill>
	);
};

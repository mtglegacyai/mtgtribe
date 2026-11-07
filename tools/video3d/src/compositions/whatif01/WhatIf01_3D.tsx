import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Html5Audio, Sequence, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/01/captions.json';
import timeline from '../../../public/videos/01/timeline.json';
import {COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {Hook3DScene} from './Hook3D';
import {S02Greeting3D, S03Setup3D, S04Doubling3D, S05Why3D, S06Coping3D, S07Zeros3D, S08Posters3D, S09Promise3D, S10Lesson3D, S11Tribe3D, S12Outro3D} from './scenes3d';
import {Section} from './ui';

// Video 01 in real 3D (vertical): same narration, captions, Leo moments and MTG's theme as the 2.5D version (v4),
// with every scene rebuilt as a Three.js world. Made 7 Nov 2026 so MTG can compare the two side by side.

export const WHATIF01_3D_FPS = 30;
const TAIL_SECONDS = 5.0; // posted with this end card; future videos use closingTail() from brand.ts
export const WHATIF01_3D_FRAMES = Math.ceil((timeline.total + TAIL_SECONDS) * WHATIF01_3D_FPS);

const SCENES = [Hook3DScene, S02Greeting3D, S03Setup3D, S04Doubling3D, S05Why3D, S06Coping3D, S07Zeros3D, S08Posters3D, S09Promise3D, S10Lesson3D, S11Tribe3D, S12Outro3D];
const captions = captionsJson as Caption[];

export const WhatIf01_3D: React.FC<{closingTrack: string | null}> = ({closingTrack}) => {
	const fps = WHATIF01_3D_FPS;
	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			{SCENES.map((Scene, i) => {
				const start = timeline.starts[i];
				const isLast = i === SCENES.length - 1;
				const seconds = isLast ? timeline.durations[i] + TAIL_SECONDS : timeline.durations[i] + timeline.gap;
				return (
					<Sequence key={i} from={Math.round(start * fps)} durationInFrames={Math.round(seconds * fps)} name={`3D S${String(i + 1).padStart(2, '0')}`}>
						<Section seconds={seconds}>
							<Scene />
						</Section>
						<Html5Audio src={staticFile(`videos/01/voice/s${String(i + 1).padStart(2, '0')}.wav`)} />
					</Sequence>
				);
			})}
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

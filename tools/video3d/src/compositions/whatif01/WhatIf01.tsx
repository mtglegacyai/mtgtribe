import type {Caption} from '@remotion/captions';
import React from 'react';
import {AbsoluteFill, Html5Audio, Sequence, staticFile} from 'remotion';
import captionsJson from '../../../public/videos/01/captions.json';
import timeline from '../../../public/videos/01/timeline.json';
import {COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {ClosingTrack} from '../../components/ClosingTrack';
import {
	S01Hook, S02Greeting, S03Setup, S04Doubling, S05Why, S06Coping, S07Zeros, S08Posters, S09Promise, S10Lesson, S11Tribe,
	S12Outro,
} from './scenes';
import {Backdrop, Section} from './ui';

// Video 01: What If Prices Doubled Every Day? (It Really Happened). Script approved by MTG on 7 November 2026.
// Research, script and compliance record: tools/videos/01-what-if-prices-doubled/

export const WHATIF01_FPS = 30;
const TAIL_SECONDS = 1.0;
export const WHATIF01_FRAMES = Math.ceil((timeline.total + TAIL_SECONDS) * WHATIF01_FPS);

const SCENES = [S01Hook, S02Greeting, S03Setup, S04Doubling, S05Why, S06Coping, S07Zeros, S08Posters, S09Promise, S10Lesson, S11Tribe, S12Outro];
const captions = captionsJson as Caption[];

export type WhatIf01Props = {
	closingTrack: string | null; // 'music/they-call-me-mtg.mp3' once MTG supplies it
};

export const WhatIf01: React.FC<WhatIf01Props> = ({closingTrack}) => {
	const fps = WHATIF01_FPS;
	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />
			{SCENES.map((Scene, i) => {
				const start = timeline.starts[i];
				const isLast = i === SCENES.length - 1;
				const seconds = isLast ? timeline.durations[i] + TAIL_SECONDS : timeline.durations[i] + timeline.gap;
				return (
					<Sequence key={i} from={Math.round(start * fps)} durationInFrames={Math.round(seconds * fps)} name={`S${String(i + 1).padStart(2, '0')}`}>
						<Section seconds={seconds}>
							<Scene />
						</Section>
						<Html5Audio src={staticFile(`videos/01/voice/s${String(i + 1).padStart(2, '0')}.wav`)} />
					</Sequence>
				);
			})}
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
			<ClosingTrack src={closingTrack} speech={captions} />
		</AbsoluteFill>
	);
};

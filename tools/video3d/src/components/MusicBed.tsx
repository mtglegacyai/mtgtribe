import type {Caption} from '@remotion/captions';
import React, {useMemo} from 'react';
import {Html5Audio, interpolate, staticFile, useVideoConfig} from 'remotion';
import {speechIntervals} from '../lib/media';

type Props = {
	src: string; // file in public/
	speech: Caption[]; // the bed dips under every spoken word
	volume?: number; // level between sentences
	duckTo?: number; // level while MTG speaks
	endAt?: number | null; // seconds: fade out here (hand over to the closing track), null = play to the end
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// A soft, copyright-free music bed under the whole video (made in code, see scripts/make_sound.py).
export const MusicBed: React.FC<Props> = ({src, speech, volume = 0.13, duckTo = 0.05, endAt = null}) => {
	const {fps, durationInFrames} = useVideoConfig();
	const intervals = useMemo(() => speechIntervals(speech, 350), [speech]);
	const end = endAt ?? durationInFrames / fps;
	return (
		<Html5Audio
			src={staticFile(src)}
			volume={(f) => {
				const s = f / fps;
				const ms = s * 1000;
				let duck = 0;
				for (const [a, b] of intervals) {
					const d = ms < a ? a - ms : ms > b ? ms - b : 0;
					duck = Math.max(duck, 1 - Math.min(1, d / 300));
				}
				const fadeIn = interpolate(s, [0, 1.2], [0, 1], clamp);
				const fadeOut = interpolate(s, [end - 3, end], [1, 0], clamp);
				return (volume - (volume - duckTo) * duck) * fadeIn * fadeOut;
			}}
		/>
	);
};

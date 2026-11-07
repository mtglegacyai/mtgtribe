import type {Caption} from '@remotion/captions';
import React, {useMemo} from 'react';
import {Html5Audio, interpolate, Sequence, staticFile, useVideoConfig} from 'remotion';
import {CLOSING_TRACK_LEAD_SECONDS, FILES} from '../brand';
import {speechIntervals} from '../lib/media';

type Props = {
	// file in public/, defaults to MTG's approved track "They Call Me MTG" (public/music/they-call-me-mtg.mp3)
	src?: string | null;
	// the narration captions: the music dips under every spoken word
	speech?: Caption[];
	volume?: number; // music level between sentences
	duckTo?: number; // music level while MTG speaks
	// for videos shorter than 50 seconds: where in the track the excerpt starts
	startInTrackSeconds?: number;
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// MTG's closing track starts 50 seconds before the video ends (or at 0 if the video is shorter),
// fades in, sits softly under the voice and fades out with the last frame.
export const ClosingTrack: React.FC<Props> = ({
	src = FILES.closingTrack,
	speech = [],
	volume = 0.5,
	duckTo = 0.14,
	startInTrackSeconds = 0,
}) => {
	const {durationInFrames, fps} = useVideoConfig();
	const intervals = useMemo(() => speechIntervals(speech), [speech]);
	if (!src) return null;

	const from = Math.max(0, durationInFrames - CLOSING_TRACK_LEAD_SECONDS * fps);
	const length = durationInFrames - from;
	const rampMs = 350;

	const duck = (ms: number) => {
		let amount = 0;
		for (const [start, end] of intervals) {
			const distance = ms < start ? start - ms : ms > end ? ms - end : 0;
			amount = Math.max(amount, 1 - Math.min(1, distance / rampMs));
		}
		return amount;
	};

	return (
		<Sequence from={from} durationInFrames={length} name="Closing track: They Call Me MTG" layout="none">
			<Html5Audio
				src={staticFile(src)}
				trimBefore={Math.round(startInTrackSeconds * fps)}
				volume={(f) => {
					const ms = ((from + f) / fps) * 1000;
					const fadeIn = interpolate(f, [0, fps * 1.2], [0, 1], clamp);
					const fadeOut = interpolate(f, [length - fps * 2.5, length - 1], [1, 0], clamp);
					const level = volume - (volume - duckTo) * duck(ms);
					return level * fadeIn * fadeOut;
				}}
			/>
		</Sequence>
	);
};

import React from 'react';
import {Html5Audio, interpolate, Sequence, staticFile, useVideoConfig} from 'remotion';
import {CLOSING_TAG, CLOSING_TAG_SECONDS, FILES} from '../brand';

type Props = {
	// file in public/, defaults to MTG's approved track "They Call Me MTG" (public/music/they-call-me-mtg.mp3); null = none
	src?: string | null;
	volume?: number;
	endPadSeconds?: number; // the line ends this long before the last frame
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/**
 * MTG's theme at the very end of every video: only its last line, "Let's get this crypto, wherever I go!" (about 2.9 s,
 * MTG 7 November 2026: "just only play the very last few seconds"). It ends with the video. Give the video an end card
 * with `closingTail()` from brand.ts so the line plays right after MTG's last word, in the clear.
 */
export const ClosingTrack: React.FC<Props> = ({src = FILES.closingTrack, volume = 0.6, endPadSeconds = 0.15}) => {
	const {durationInFrames, fps} = useVideoConfig();
	if (!src) return null;
	const length = Math.round(CLOSING_TAG_SECONDS * fps);
	const from = Math.max(0, durationInFrames - length - Math.round(endPadSeconds * fps));
	return (
		<Sequence from={from} durationInFrames={length} name="MTG theme: Let's get this crypto, wherever I go!" layout="none">
			<Html5Audio
				src={staticFile(src)}
				trimBefore={Math.round(CLOSING_TAG.from * fps)}
				volume={(f) => volume * interpolate(f, [0, 3], [0, 1], clamp) * interpolate(f, [length - 6, length - 1], [1, 0], clamp)}
			/>
		</Sequence>
	);
};

import type {Caption} from '@remotion/captions';
import {ALL_FORMATS, Input, UrlSource} from 'mediabunny';

// Exact length of an audio or video file in seconds. Use it in calculateMetadata
// so the video is as long as the final narration, never a guess.
export const getMediaDurationInSeconds = async (src: string): Promise<number> => {
	const input = new Input({formats: ALL_FORMATS, source: new UrlSource(src)});
	try {
		return await input.computeDuration();
	} finally {
		input.dispose();
	}
};

// Loads a captions JSON file (Caption[], made by scripts/transcribe.py or scripts/whisper-to-captions.mjs).
export const loadCaptions = async (src: string, signal?: AbortSignal): Promise<Caption[]> => {
	const res = await fetch(src, {signal});
	if (!res.ok) throw new Error(`Could not load captions ${src}: HTTP ${res.status}`);
	return (await res.json()) as Caption[];
};

// The moments someone is speaking, merged into intervals (milliseconds). Used to duck music under the voice.
export const speechIntervals = (captions: Caption[], joinGapMs = 450): Array<[number, number]> => {
	const sorted = [...captions].sort((a, b) => a.startMs - b.startMs);
	const out: Array<[number, number]> = [];
	for (const c of sorted) {
		const last = out[out.length - 1];
		if (last && c.startMs - last[1] <= joinGapMs) last[1] = Math.max(last[1], c.endMs);
		else out.push([c.startMs, c.endMs]);
	}
	return out;
};

// When a given word starts, in frames. Handy to land a 3D action exactly on a spoken word.
export const wordStartFrames = (captions: Caption[], fps: number) =>
	captions.map((c) => Math.round((c.startMs / 1000) * fps));

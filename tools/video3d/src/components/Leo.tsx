import React from 'react';
import {Html5Audio, interpolate, OffthreadVideo, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS} from '../brand';
import {clamp} from '../compositions/whatif01/ui';

// Leo's moments (MTG, 10 November 2026): "let my mascot actions, expressions, movements, sound effects speak louder than
// words". Every emotion below is an exact stretch of one of Leo's existing clips (public/videos/01/leo/), checked frame
// by frame, so he can react often and precisely without new HeyGen credits. Pick the moment whose feeling matches the
// spoken line, start it on the word, keep it short, never two identical moments in a row.

export type LeoMomentDef = {clip: string; from: number; to: number; feel: string; focus?: string};

export const LEO_MOMENTS = {
	aha: {clip: 'V3', from: 0.3, to: 1.45, feel: 'now I get it: a light bulb lights up above his head'},
	wow: {clip: 'V3', from: 1.1, to: 2.9, feel: 'amazed, eyes wide, mouth open'},
	mindblown: {clip: 'V3', from: 3.0, to: 5.0, feel: 'paw on his head: that changes everything'},
	worried: {clip: 'V1', from: 5.0, to: 6.5, feel: 'worried, wide eyes: careful (a warning)', focus: '50% 22%'},
	think: {clip: 'V5', from: 0.5, to: 4.4, feel: 'thinking it over, paw on his chin'},
	reassure: {clip: 'V5', from: 5.15, to: 6.5, feel: "a warm, reassuring smile: it's going to be okay"},
	laugh: {clip: 'V6', from: 2.0, to: 4.3, feel: 'laughs warmly'},
	welcome: {clip: 'V6', from: 4.4, to: 6.5, feel: 'open arms and a big smile: come in, you belong here'},
	smile: {clip: 'V4', from: 0.4, to: 2.0, feel: 'a warm, friendly smile'},
	wave: {clip: 'V4', from: 2.0, to: 4.45, feel: 'waves hello'},
	wink: {clip: 'V4', from: 4.45, to: 5.0, feel: 'a quick wink: our secret'},
	thumbsup: {clip: 'V4', from: 5.0, to: 6.5, feel: "thumbs up: you've got this, let's go"},
	winkup: {clip: 'V4', from: 4.45, to: 6.5, feel: 'a wink, then a thumbs up: between friends (the share prompt)'},
	point: {clip: 'V7', from: 2.4, to: 5.3, feel: 'raises one finger: this part is important'},
	ask: {clip: 'V2', from: 2.3, to: 6.5, feel: 'open paw to the viewer: your turn, tell me'},
	present: {clip: 'L2', from: 2.5, to: 6.5, feel: 'both paws open: here it is (wide clip, cropped)'},
} satisfies Record<string, LeoMomentDef>;
export type LeoMomentId = keyof typeof LEO_MOMENTS;

/**
 * Small accents that make a feeling land, drawn in code around his window (no credits), each with its soft sound:
 * aha (a warm burst of light around his light bulb, `aha`), wow (soft sparkles, `reveal`), relief (two gold breath rings, `exhale`),
 * warm (a soft glow, `chime`), alert (a calm amber outline, `drop`).
 */
export type LeoAccent = 'aha' | 'wow' | 'relief' | 'warm' | 'alert' | 'none';
const ACCENT_SOUND: Record<LeoAccent, string | null> = {aha: 'aha', wow: 'reveal', relief: 'exhale', warm: 'chime', alert: 'drop', none: null};

export type LeoFrame = 'face' | 'bust' | 'tall';
const FRAMES: Record<LeoFrame, {style: React.CSSProperties; focus: string}> = {
	face: {style: {left: 560, top: 930, width: 440, height: 290}, focus: '50% 6%'},
	bust: {style: {left: 600, top: 700, width: 400, height: 500}, focus: '50% 10%'},
	tall: {style: {left: 160, top: 320, width: 760, height: 1330}, focus: '50% 50%'},
};

export const LeoMoment: React.FC<{
	m: LeoMomentId; at: number; frame?: LeoFrame; style?: React.CSSProperties; seconds?: number; accent?: LeoAccent;
	sound?: string | null; volume?: number; focus?: string;
}> = ({m, at, frame = 'face', style, seconds, accent = 'none', sound, volume = 0.35, focus}) => {
	const {fps} = useVideoConfig();
	const def: LeoMomentDef = LEO_MOMENTS[m];
	const dur = Math.min(seconds ?? def.to - def.from, def.to - def.from);
	const snd = sound === undefined ? ACCENT_SOUND[accent] : sound;
	if (dur < 0.5) return null; // no room for the moment between two cues: leave it out rather than flash it
	return (
		<Sequence from={Math.round(at * fps)} durationInFrames={Math.round(dur * fps)} layout="none" name={`Leo ${m}`}>
			<LeoWindow def={def} dur={dur} style={{...FRAMES[frame].style, ...style}} focus={focus ?? def.focus ?? FRAMES[frame].focus} accent={accent} />
			{snd && <Html5Audio src={staticFile(`sfx/${snd}.mp3`)} volume={volume} />}
		</Sequence>
	);
};

const LeoWindow: React.FC<{def: LeoMomentDef; dur: number; style: React.CSSProperties; focus: string; accent: LeoAccent}> = ({def, dur, style, focus, accent}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const enter = spring({frame, fps, config: {damping: 15}});
	const out = interpolate(t, [dur - 0.22, dur], [1, 0], clamp);
	const w = Number(style.width ?? 400);
	return (
		<div style={{position: 'absolute', perspective: 1400, ...style, opacity: Math.min(1, enter * 1.3) * out}}>
			{accent === 'relief' &&
				[0, 0.35].map((d) => {
					const p = interpolate(t, [0.15 + d, 1.35 + d], [0, 1], clamp);
					return <div key={d} style={{position: 'absolute', inset: -10 - p * 70, borderRadius: 44 + p * 40, border: `3px solid rgba(255,217,142,${0.55 * (1 - p)})`}} />;
				})}
			{accent === 'warm' && <div style={{position: 'absolute', inset: -40, borderRadius: 70, background: 'radial-gradient(ellipse, rgba(255,200,120,0.35), transparent 70%)', opacity: interpolate(t, [0, 0.5, dur], [0, 1, 0.6], clamp)}} />}
			<div
				style={{
					width: '100%', height: '100%', overflow: 'hidden', borderRadius: 32, position: 'relative',
					border: `3px solid ${accent === 'alert' ? '#e8954a' : COLORS.gold}`,
					boxShadow: accent === 'alert' ? '0 30px 80px rgba(0,0,0,0.6), 0 0 40px rgba(232,149,74,0.45)' : '0 30px 80px rgba(0,0,0,0.6), 0 0 50px rgba(242,173,60,0.25)',
					transform: `rotateY(${interpolate(enter, [0, 1], [-30, 0])}deg) scale(${interpolate(enter, [0, 1], [0.88, 1])})`,
				}}
			>
				<OffthreadVideo src={staticFile(`videos/01/leo/${def.clip}.mp4`)} muted trimBefore={Math.round(def.from * fps)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: focus}} />
			</div>
			{accent === 'aha' &&
				// a warm burst of light behind the top of his window, timed with the light bulb in his clip (no extra icon)
				[0, 1].map((k) => {
					const p = interpolate(t, [0.15 + k * 0.18, 0.9 + k * 0.18], [0, 1], clamp);
					return <div key={k} style={{position: 'absolute', left: '50%', top: 0, width: w * (0.5 + 1.1 * p), height: w * (0.5 + 1.1 * p), transform: 'translate(-50%, -50%)', borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,226,160,0.55), rgba(255,200,110,0.18) 45%, transparent 70%)', opacity: (1 - p) * 0.9, pointerEvents: 'none', zIndex: -1}} />;
				})}
			{accent === 'wow' &&
				[[-0.06, -0.08, 0.15], [1.0, 0.05, 0.3], [0.92, 0.9, 0.45]].map(([x, y, d], i) => (
					<div key={i} style={{position: 'absolute', left: `${x * 100}%`, top: `${y * 100}%`, fontSize: w * 0.12, opacity: interpolate(t, [d, d + 0.25, d + 1.0], [0, 1, 0], clamp), transform: `scale(${interpolate(t, [d, d + 0.3], [0.3, 1], clamp)})`, filter: 'drop-shadow(0 0 12px rgba(255,217,142,0.9))'}}>✨</div>
				))}
		</div>
	);
};

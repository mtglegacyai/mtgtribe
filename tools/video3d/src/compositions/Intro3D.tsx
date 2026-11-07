import type {Caption} from '@remotion/captions';
import {ThreeCanvas} from '@remotion/three';
import React from 'react';
import {
	AbsoluteFill,
	type CalculateMetadataFunction,
	Easing,
	Html5Audio,
	interpolate,
	spring,
	staticFile,
	useCurrentFrame,
	useVideoConfig,
} from 'remotion';
import {BRAND, COLORS} from '../brand';
import {BrandBar} from '../components/BrandBar';
import {Captions} from '../components/Captions';
import {ClosingTrack} from '../components/ClosingTrack';
import {PhotoCard} from '../components/PhotoCard';
import {BODY, DISPLAY} from '../fonts';
import {useLayout} from '../lib/layout';
import {getMediaDurationInSeconds, loadCaptions, wordStartFrames} from '../lib/media';
import {BuildingBlocks} from '../three/BuildingBlocks';
import {CameraRig, StudioLights} from '../three/Studio';

// Demo and starting point: MTG's own recorded line "Hi, my name is MTG, Your Digital Architect"
// (from the approved invite, no new HeyGen credits), word synced captions, his full photo,
// and eight 3D gold blocks that land on his eight spoken words.

export type Intro3DProps = {
	voice: string; // narration file in public/
	captionsFile: string; // Caption[] JSON in public/ (scripts/transcribe.py)
	endCardSeconds: number; // time after the narration for the slogan
	closingTrack: string | null; // null until MTG's track is in public/music/
	captions?: Caption[]; // filled in by calculateMetadata
};

export const intro3DDefaults: Intro3DProps = {
	voice: 'demo/mtg-voice-intro.m4a',
	captionsFile: 'demo/mtg-voice-intro.captions.json',
	endCardSeconds: 2.4,
	closingTrack: null,
};

// The video is exactly as long as the narration plus the end card, measured from the real audio file.
export const calculateIntro3DMetadata: CalculateMetadataFunction<Intro3DProps> = async ({props, abortSignal}) => {
	const fps = 30;
	const [voiceSeconds, captions] = await Promise.all([
		getMediaDurationInSeconds(staticFile(props.voice)),
		loadCaptions(staticFile(props.captionsFile), abortSignal),
	]);
	return {fps, durationInFrames: Math.ceil((voiceSeconds + props.endCardSeconds) * fps), props: {...props, captions}};
};

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const CAPTION_HOLD_MS = 700;

export const Intro3D: React.FC<Intro3DProps> = ({voice, closingTrack, captions = []}) => {
	const frame = useCurrentFrame();
	const {fps, durationInFrames} = useVideoConfig();
	const layout = useLayout();
	const {vertical, width} = layout;

	// every visual cue comes from the word timestamps of the real audio
	const words = wordStartFrames(captions, fps);
	const landFrames = words.map((f) => Math.max(f, 12)); // blocks need 10 frames to fall in
	const nameFrame = words[4] ?? 45; // "MTG,"
	const titleFrame = words[5] ?? 70; // "Your Digital Architect"
	const lastWordEndMs = captions.length ? captions[captions.length - 1].endMs : 3000;
	const sloganFrame = Math.round(((lastWordEndMs + CAPTION_HOLD_MS) / 1000) * fps);

	const photoIn = spring({frame, fps, config: {damping: 18, mass: 0.8}});
	const nameIn = spring({frame: frame - nameFrame, fps, config: {damping: 16}});
	const titleIn = spring({frame: frame - titleFrame, fps, config: {damping: 200}, durationInFrames: 12});
	const sloganIn = spring({frame: frame - sloganFrame, fps, config: {damping: 14}});
	const fadeOut = interpolate(frame, [durationInFrames - 12, durationInFrames - 1], [1, 0], clamp);

	// layout per orientation (1920x1080 or 1080x1920)
	const L = vertical
		? {
				photo: {size: 500, top: 250},
				// starts under the photo frame (never over the t-shirt print) and is transparent,
				// so blocks drop in from behind the name instead of popping out mid screen
				canvas: {top: 790, left: 0, width, height: 690},
				name: {top: 795, left: 0, width},
				nameSize: 120,
				titleSize: 46,
				camera: {radius: 6.6, height: 2.9, lookY: 1.0, fov: 53.1},
			}
		: {
				photo: {size: 580, top: 230},
				canvas: {top: 60, left: 780, width: 1080, height: 560},
				name: {top: 590, left: 780, width: 1080},
				nameSize: 150,
				titleSize: 52,
				camera: {radius: 9, height: 4.2, lookY: 1.0, fov: 30},
			};

	// a slow camera move that shows the cube is real 3D, without spinning for the sake of it
	const orbit = interpolate(frame, [0, durationInFrames], [-0.6, 0.3], {easing: Easing.inOut(Easing.sin)});
	const cam = L.camera;

	return (
		<AbsoluteFill style={{background: COLORS.bg, opacity: fadeOut}}>
			<AbsoluteFill
				style={{
					background: `radial-gradient(ellipse at ${vertical ? '50% 60%' : '68% 45%'}, #2b1e0c 0%, ${COLORS.bgLift} 38%, ${COLORS.bg} 78%)`,
				}}
			/>

			<div style={{position: 'absolute', ...L.canvas}}>
				<ThreeCanvas width={L.canvas.width} height={L.canvas.height} gl={{antialias: true}} camera={{fov: cam.fov}}>
					<CameraRig
						position={[Math.sin(orbit) * cam.radius, cam.height, Math.cos(orbit) * cam.radius]}
						lookAt={[0, cam.lookY, 0]}
						fov={cam.fov}
					/>
					<StudioLights />
					<BuildingBlocks landFrames={landFrames} />
				</ThreeCanvas>
			</div>

			<div
				style={{
					position: 'absolute',
					top: L.photo.top,
					left: vertical ? '50%' : 110,
					transform: `${vertical ? 'translateX(-50%) ' : ''}scale(${interpolate(photoIn, [0, 1], [0.9, 1])})`,
					opacity: photoIn,
				}}
			>
				<PhotoCard size={L.photo.size} />
			</div>

			<div style={{position: 'absolute', ...L.name, textAlign: 'center'}}>
				<div
					style={{
						fontFamily: DISPLAY,
						fontSize: L.nameSize,
						lineHeight: 1,
						letterSpacing: 4,
						background: `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold} 62%, #c98a2b)`,
						WebkitBackgroundClip: 'text',
						backgroundClip: 'text',
						color: 'transparent',
						opacity: nameIn,
						transform: `translateY(${(1 - nameIn) * 30}px)`,
					}}
				>
					{BRAND.name}
				</div>
				<div
					style={{
						marginTop: 10,
						fontFamily: BODY,
						fontWeight: 800,
						fontSize: L.titleSize,
						color: COLORS.text,
						opacity: titleIn,
						transform: `translateY(${(1 - titleIn) * 16}px)`,
					}}
				>
					{BRAND.title}
				</div>
			</div>

			<Captions captions={captions} holdMs={CAPTION_HOLD_MS} />

			<AbsoluteFill
				style={{
					justifyContent: 'flex-end',
					alignItems: 'center',
					paddingBottom: layout.safe.bottom,
					opacity: sloganIn,
				}}
			>
				<div style={{fontFamily: DISPLAY, fontSize: vertical ? 76 : 92, letterSpacing: 2, transform: `scale(${interpolate(sloganIn, [0, 1], [0.92, 1])})`}}>
					<span
						style={{
							background: `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold} 62%, #c98a2b)`,
							WebkitBackgroundClip: 'text',
							backgroundClip: 'text',
							color: 'transparent',
						}}
					>
						{BRAND.slogan.replace(/\s*💪$/u, '')}
					</span>{' '}
					<span>💪</span>
				</div>
			</AbsoluteFill>

			<BrandBar />

			<Html5Audio src={staticFile(voice)} />
			<ClosingTrack src={closingTrack} />
		</AbsoluteFill>
	);
};

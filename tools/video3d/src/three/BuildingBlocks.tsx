import {RoundedBox} from '@react-three/drei';
import React from 'react';
import {Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS} from '../brand';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const GAP = 1.08;

// Eight gold blocks that build a 2 x 2 x 2 cube: the "digital architect" builds, block by block.
// Bottom layer first, back to front, so a new block never hides one that is still landing.
export const CUBE_SLOTS: Array<[number, number, number]> = [
	[-0.5, 0, -0.5],
	[0.5, 0, -0.5],
	[-0.5, 0, 0.5],
	[0.5, 0, 0.5],
	[-0.5, 1, -0.5],
	[0.5, 1, -0.5],
	[-0.5, 1, 0.5],
	[0.5, 1, 0.5],
].map(([x, y, z]) => [x * GAP, y * GAP, z * GAP]);

type BlockProps = {
	slot: [number, number, number]; // bottom centre of the block
	landFrame: number; // the frame the block touches down (put it on a spoken word)
	glowFrame: number; // the frame its completion glow peaks
	index: number;
};

const FALL_FRAMES = 10;

const Block: React.FC<BlockProps> = ({slot, landFrame, glowFrame, index}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	if (frame < landFrame - FALL_FRAMES) return null;

	// falls like it has weight (accelerates), lands exactly on landFrame
	const y = interpolate(frame, [landFrame - FALL_FRAMES, landFrame], [slot[1] + 4.2, slot[1]], {
		...clamp,
		easing: Easing.in(Easing.quad),
	});
	const turn = interpolate(frame, [landFrame - FALL_FRAMES, landFrame], [0.5, 0], clamp) * (index % 2 ? 1 : -1);
	// a small squash on impact that springs back
	const settle = spring({frame: frame - landFrame, fps, config: {damping: 9, stiffness: 240, mass: 0.6}});
	const squashY = frame < landFrame ? 1 : interpolate(settle, [0, 1], [0.84, 1]);
	const squashXZ = 1 + (1 - squashY) * 0.5;
	// a soft gold glow that runs through the finished cube, block by block
	const glow = interpolate(frame, [glowFrame - 6, glowFrame, glowFrame + 12], [0, 0.55, 0], clamp);

	return (
		<group position={[slot[0], y, slot[2]]} rotation={[0, turn, 0]}>
			<RoundedBox
				args={[1, 1, 1]}
				radius={0.09}
				smoothness={5}
				position={[0, 0.5 * squashY, 0]}
				scale={[squashXZ, squashY, squashXZ]}
			>
				<meshStandardMaterial
					color={index % 3 === 1 ? COLORS.goldHi : COLORS.gold}
					metalness={0.9}
					roughness={0.3}
					emissive={COLORS.gold}
					emissiveIntensity={glow}
				/>
			</RoundedBox>
		</group>
	);
};

// landFrames: one frame per block, usually the start of each spoken word (see wordStartFrames in lib/media.ts).
export const BuildingBlocks: React.FC<{landFrames: number[]}> = ({landFrames}) => {
	const done = Math.max(...landFrames) + 8;
	return (
		<group>
			{CUBE_SLOTS.map((slot, i) => (
				<Block key={i} slot={slot} index={i} landFrame={landFrames[i] ?? done} glowFrame={done + i * 2} />
			))}
		</group>
	);
};

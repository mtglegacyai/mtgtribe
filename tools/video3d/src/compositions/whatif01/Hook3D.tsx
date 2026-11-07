import type {Caption} from '@remotion/captions';
import {MeshReflectorMaterial, Text3D} from '@react-three/drei';
import {useFrame, useThree} from '@react-three/fiber';
import {ThreeCanvas} from '@remotion/three';
import React, {useMemo, useRef} from 'react';
import {AbsoluteFill, Easing, Html5Audio, interpolate, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import captionsJson from '../../../public/videos/01/captions.json';
import timeline from '../../../public/videos/01/timeline.json';
import {COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {Captions} from '../../components/Captions';
import {MONO} from '../../fonts';
import {StudioLights} from '../../three/Studio';
import {Chip, Cues} from './ui';

// Video 01's hook rebuilt in REAL 3D (Three.js), to compare with the 2.5D version: a black-and-gold studio with depth
// (gold arches, reflective floor, fog), a 3D loaf on a pedestal, the price carved in extruded gold Anton, and gold coins
// that rain down and pile up as the price doubles. Everything is driven by the frame number, never the clock.

const FPS = 30;
const SECONDS = timeline.durations[0] + 1.0;
export const HOOK3D_FRAMES = Math.round(SECONDS * FPS);
const captions = (captionsJson as Caption[]).filter((c) => c.startMs < timeline.starts[1] * 1000 - 100); // section 1 only
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const FONT = staticFile('fonts/anton.typeface.json');

// Days since "today", from the narration: twenty at 5.3 s, forty at 7.1 s, then a month in four seconds.
const daysAt = (t: number) =>
	t < 5.3 ? 0 : t < 7.1 ? 1 : t < 8.0 ? 2 : Math.min(30, 2 + Math.floor(28 * Easing.in(Easing.cubic)(Math.min(1, (t - 8.0) / 3.9))));
const priceText = (d: number) => `R${(10 * 2 ** d).toLocaleString('en-US')}`;

// Coins: one more for every doubling, capped (a real 2^30 would be a billion coins).
const MAX_COINS = 170;
const coinsAt = (t: number) => (daysAt(t) >= 8 ? Math.min(MAX_COINS, Math.round(interpolate(t, [9.0, 11.9], [2 ** 7, MAX_COINS], clamp))) : Math.min(MAX_COINS, 2 ** daysAt(t)));
const COIN_LAND: number[] = (() => {
	const out: number[] = [];
	for (let f = 0; f < SECONDS * FPS; f++) {
		const n = coinsAt(f / FPS);
		while (out.length < n) out.push(f / FPS);
	}
	return out;
})();

// Where each coin ends up: a heap around the pedestal, higher towards the middle.
const COIN_SPOTS = Array.from({length: MAX_COINS}, (_, i) => {
	// the first coins land in a neat row in front of the pedestal, where the camera sees them clearly
	if (i < 4) return {x: (i - 1.5) * 0.62, z: 1.75, y: 0.035, tiltX: 0, tiltZ: 0, spin: 5 + i};
	const a = random(`a${i}`) * Math.PI * 2;
	const r = 1.3 + Math.pow(random(`r${i}`), 0.7) * 2.4;
	const layer = Math.floor(i / 34);
	return {
		x: Math.cos(a) * r,
		z: Math.sin(a) * r * 0.8 + 0.4,
		y: 0.035 + layer * 0.07 + (r < 2.2 ? 0.05 : 0),
		tiltX: (random(`tx${i}`) - 0.5) * 0.5,
		tiltZ: (random(`tz${i}`) - 0.5) * 0.5,
		spin: random(`s${i}`) * 6 + 4,
	};
});

const GOLD = new THREE.MeshStandardMaterial({color: '#f2ad3c', metalness: 1, roughness: 0.22});
const GOLD_HI = new THREE.MeshStandardMaterial({color: '#ffd98e', metalness: 1, roughness: 0.18});

const Camera: React.FC = () => {
	const frame = useCurrentFrame();
	const camera = useThree((s) => s.camera);
	const t = frame / FPS;
	const e = Easing.inOut(Easing.cubic);
	// push in, a gentle orbit while prices double, then rise and pull back to show the mountain of coins
	const dist = interpolate(t, [0, 2.6, 7.6, 11.4, SECONDS], [14, 10.5, 9.8, 15.5, 15], {...clamp, easing: e});
	const height = interpolate(t, [0, 2.6, 7.6, 11.4, SECONDS], [3.0, 2.6, 2.8, 7.4, 7.0], {...clamp, easing: e});
	const orbit = interpolate(t, [0, 5.3, 7.1, 11.4, SECONDS], [-0.2, 0.12, -0.1, 0.24, 0.28], {...clamp, easing: e});
	const lookY = interpolate(t, [0, 7.6, 11.4], [0.95, 0.95, 0.55], {...clamp, easing: e}); // keeps the loaf above the captions
	useFrame(() => {
		camera.position.set(Math.sin(orbit) * dist, height, Math.cos(orbit) * dist);
		camera.lookAt(0, lookY, 0);
	}, -1);
	return null;
};

// The price is carved in 3D gold and travels with the camera (so it is always framed), turning a little so its depth shows.
const Price: React.FC = () => {
	const frame = useCurrentFrame();
	const camera = useThree((s) => s.camera);
	const group = useRef<THREE.Group>(null);
	const t = frame / FPS;
	const d = daysAt(t);
	const text = priceText(d);
	const pulse = [5.3, 7.1].some((at) => t >= at && t < at + 0.25) ? 1.08 : 1;
	const size = 0.5;
	const swing = Math.sin(t * 0.9) * 0.22;
	const appear = interpolate(t, [0.3, 1.1], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.4))});
	const big = interpolate(t, [11.9, 12.5], [1, 1.12], {...clamp, easing: Easing.out(Easing.cubic)});
	useFrame(() => {
		const g = group.current;
		if (!g) return;
		const fwd = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
		const up = new THREE.Vector3(0, 1, 0).applyQuaternion(camera.quaternion);
		g.position.copy(camera.position).add(fwd.multiplyScalar(5)).add(up.multiplyScalar(0.86));
		g.quaternion.copy(camera.quaternion);
		g.rotateY(swing);
		g.scale.setScalar(appear * pulse * big);
	});
	return (
		<group ref={group}>
			<Text3D key={text} font={FONT} size={size} height={size * 0.32} bevelEnabled bevelSize={size * 0.025} bevelThickness={size * 0.04} bevelSegments={3} curveSegments={6} material={d === 30 ? GOLD_HI : GOLD}>
				{text}
			</Text3D>
			<CenterX text={text} size={size} />
			{/* a warm light in front of the number, so the gold never turns dark as it turns */}
			<pointLight position={[0.6, 0.8, 2.2]} intensity={9} color="#fff1d6" distance={6} />
		</group>
	);
};

// Text3D starts at x = 0; shift the parent so the number is centred (Anton's average advance is about 0.47 em).
const CenterX: React.FC<{text: string; size: number}> = ({text, size}) => {
	const ref = useRef<THREE.Object3D>(null);
	useFrame(() => {
		const p = ref.current?.parent;
		if (!p) return;
		const textMesh = p.children.find((c) => (c as THREE.Mesh).isMesh) as THREE.Mesh | undefined;
		if (!textMesh) return;
		textMesh.geometry.computeBoundingBox();
		const bb = textMesh.geometry.boundingBox;
		if (!bb) return;
		const fit = Math.min(1, 1.85 / (bb.max.x - bb.min.x)); // never wider than the frame (1.85 of 2.1 units)
		textMesh.scale.setScalar(fit);
		textMesh.position.set((-(bb.max.x + bb.min.x) / 2) * fit, (-(bb.max.y + bb.min.y) / 2) * fit, -size * 0.16 * fit);
	});
	return <object3D ref={ref} />;
};

/** The 3D loaf of bread. pulses: seconds where it swells a little (a price change). */
export const Loaf3D: React.FC<{pulses?: number[]; position?: [number, number, number]; size?: number}> = ({pulses = [], position = [0, 1.02, 0], size = 0.82}) => {
	const frame = useCurrentFrame();
	const t = frame / FPS;
	const pulse = pulses.reduce((acc, at) => acc + Math.max(0, 1 - Math.abs(t - at - 0.12) / 0.18) * 0.06, 0);
	const crust = useMemo(() => new THREE.MeshPhysicalMaterial({color: '#d98b2e', roughness: 0.55, clearcoat: 0.35, clearcoatRoughness: 0.4, sheen: 0.4, sheenColor: new THREE.Color('#ffd59a')}), []);
	const score = useMemo(() => new THREE.MeshStandardMaterial({color: '#f6d28e', roughness: 0.8}), []);
	return (
		<group position={position} rotation={[0, t * 0.25 - 0.4, 0]} scale={(1 + pulse) * size}>
			<mesh material={crust} scale={[1.3, 0.62, 0.68]} castShadow>
				<sphereGeometry args={[1, 64, 32, 0, Math.PI * 2, 0, Math.PI * 0.56]} />
			</mesh>
			<mesh material={crust} position={[0, 0.012, 0]} rotation={[-Math.PI / 2, 0, 0]} scale={[1.3 * 0.985, 0.68 * 0.985, 1]}>
				<circleGeometry args={[1, 64]} />
			</mesh>
			{[-0.55, 0, 0.55].map((x) => (
				<mesh key={x} material={score} position={[x, 0.62 * Math.sqrt(1 - (x / 1.3) ** 2) - 0.035, 0]} rotation={[0, 0, Math.atan((0.62 * x) / (1.3 * 1.3 * Math.sqrt(1 - (x / 1.3) ** 2)))]} scale={[0.11, 0.035, 0.4]}>
					<sphereGeometry args={[1, 24, 12]} />
				</mesh>
			))}
		</group>
	);
};

const Pedestal: React.FC = () => (
	<group>
		<mesh position={[0, 0.5, 0]} receiveShadow>
			<cylinderGeometry args={[1.05, 1.15, 1, 64]} />
			<meshStandardMaterial color="#14100a" metalness={0.6} roughness={0.35} />
		</mesh>
		<mesh position={[0, 1.0, 0]} rotation={[Math.PI / 2, 0, 0]} material={GOLD}>
			<torusGeometry args={[1.05, 0.035, 16, 96]} />
		</mesh>
	</group>
);

const Arches: React.FC = () => {
	const glow = useMemo(() => new THREE.MeshStandardMaterial({color: '#ffcf7a', emissive: new THREE.Color('#f2ad3c'), emissiveIntensity: 2.2, toneMapped: false}), []);
	return (
		<group>
			{[-5, -8.5, -12, -15.5, -19].map((z, i) => (
				<mesh key={z} position={[0, 0, z]} material={glow}>
					<torusGeometry args={[5.2 + i * 0.15, 0.045, 12, 120, Math.PI]} />
				</mesh>
			))}
			{[-4.2, 4.2].flatMap((x) =>
				[-3, -6.5, -10].map((z) => (
					<mesh key={`${x}${z}`} position={[x, 2.2, z]} material={glow}>
						<boxGeometry args={[0.05, 4.4, 0.05]} />
					</mesh>
				)),
			)}
		</group>
	);
};

const COIN_GEO = new THREE.CylinderGeometry(0.26, 0.26, 0.06, 40);
const Coins: React.FC = () => {
	const frame = useCurrentFrame();
	const t = frame / FPS;
	return (
		<group>
			{COIN_SPOTS.map((s, i) => {
				const land = COIN_LAND[i];
				if (land === undefined || t < land - 0.55) return null;
				const p = interpolate(t, [land - 0.55, land], [0, 1], {...clamp, easing: Easing.in(Easing.quad)});
				const bounce = t > land ? Math.max(0, Math.sin((t - land) * 18) * Math.exp(-(t - land) * 9) * 0.12) : 0;
				const y = s.y + (1 - p) * 7 + bounce;
				const tumble = (1 - p) * s.spin;
				return <mesh key={i} geometry={COIN_GEO} material={i % 5 === 0 ? GOLD_HI : GOLD} position={[s.x, y, s.z]} rotation={[s.tiltX + tumble, tumble * 0.6, s.tiltZ]} castShadow />;
			})}
		</group>
	);
};

const Floor: React.FC = () => (
	<mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
		<planeGeometry args={[60, 60]} />
		<MeshReflectorMaterial resolution={512} mirror={0.55} blur={[260, 80]} mixBlur={1} mixStrength={2.2} depthScale={0.6} minDepthThreshold={0.6} color="#0d0a06" metalness={0.5} roughness={0.75} />
	</mesh>
);

export const World: React.FC = () => (
	<>
		<color attach="background" args={['#050403']} />
		<fog attach="fog" args={['#050403', 9, 30]} />
		<Camera />
		<StudioLights shadowY={0.001} shadowScale={14} />
		<spotLight position={[0, 7, 3]} angle={0.45} penumbra={0.8} intensity={60} color="#fff1d6" distance={20} />
		<pointLight position={[-3, 2.5, -3]} intensity={12} color="#f2ad3c" distance={12} />
		<pointLight position={[3, 2.5, -3]} intensity={12} color="#f2ad3c" distance={12} />
		<Arches />
		<Floor />
		<Pedestal />
		<Loaf3D pulses={[2.6, 5.3, 7.1]} />
		<Coins />
		<Price />
	</>
);

/** The hook's picture and sound effects (no voice or captions): scene 1 of the full 3D video, and the sample below. */
export const Hook3DScene: React.FC = () => {
	const frame = useCurrentFrame();
	const {width, height} = useVideoConfig();
	const t = frame / FPS;
	const d = daysAt(t);
	const label = d === 0 ? 'TODAY' : d === 30 ? '30 DAYS LATER' : `+${d} DAY${d > 1 ? 'S' : ''}`;
	return (
		<AbsoluteFill>
			<ThreeCanvas width={width} height={height} gl={{antialias: true, toneMapping: THREE.ACESFilmicToneMapping}} camera={{fov: 42, near: 0.1, far: 80}} shadows>
				<World />
			</ThreeCanvas>
			<div style={{position: 'absolute', top: 250, width: '100%', textAlign: 'center', opacity: interpolate(t, [0.2, 0.6, 2.4, 2.8], [0, 1, 1, 0], clamp)}}>
				<Chip size={40}>IMAGINE THIS</Chip>
			</div>
			<div style={{position: 'absolute', top: 700, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 44, letterSpacing: 4, color: COLORS.champagne, textShadow: '0 4px 18px rgba(0,0,0,0.9)', opacity: interpolate(t, [0.6, 1.0], [0, 1], clamp)}}>
				{label}
			</div>
			{/* sound: rising notes as the price doubles, soft ticks speeding up, coins raining, a swell into R10 billion */}
			<Cues list={[[0.1, 'air', 0.4], [2.6, 'pluck1', 0.45], [5.33, 'pluck3', 0.45], [7.13, 'pluck5', 0.45], [8.2, 'count', 0.28], [9.0, 'coinrain', 0.4], [9.3, 'swell', 0.45], [11.9, 'reveal', 0.55]]} />
		</AbsoluteFill>
	);
};

export const Hook3D: React.FC = () => {
	const frame = useCurrentFrame();
	const t = frame / FPS;
	const fade = interpolate(t, [0, 0.4, SECONDS - 0.4, SECONDS], [0, 1, 1, 0], clamp);
	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<AbsoluteFill style={{opacity: fade}}>
				<Hook3DScene />
			</AbsoluteFill>
			<Html5Audio src={staticFile('videos/01/voice/s01.wav')} />
			<Captions captions={captions} holdMs={600} />
			<BrandBar />
		</AbsoluteFill>
	);
};

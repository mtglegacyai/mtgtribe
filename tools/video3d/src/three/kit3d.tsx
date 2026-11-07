import {MeshReflectorMaterial, Text3D} from '@react-three/drei';
import {useFrame, useThree} from '@react-three/fiber';
import React, {useMemo, useRef} from 'react';
import {Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {StudioLights} from './Studio';

// MTG's real 3D kit: one black-and-gold world shared by every 3D scene (gold arches, reflective floor, fog), gold text
// carved from his Anton font, coins, banknotes, a pedestal and camera moves. Everything follows the frame number.

export const FONT = staticFile('fonts/anton.typeface.json');
export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const smooth = Easing.inOut(Easing.cubic);

export const GOLD = new THREE.MeshStandardMaterial({color: '#f2ad3c', metalness: 1, roughness: 0.22});
export const GOLD_HI = new THREE.MeshStandardMaterial({color: '#ffd98e', metalness: 1, roughness: 0.18});
export const DARK = new THREE.MeshStandardMaterial({color: '#14100a', metalness: 0.6, roughness: 0.35});
export const CHAMPAGNE = new THREE.MeshStandardMaterial({color: '#f7e6bf', metalness: 0.3, roughness: 0.4});
export const RED = new THREE.MeshStandardMaterial({color: '#e0602f', metalness: 0.2, roughness: 0.4, emissive: new THREE.Color('#7a2208'), emissiveIntensity: 0.6});

/** Seconds inside the current Sequence. */
export const useSec = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	return frame / fps;
};

/** Keyframed number: k(t, [0, 2, 5], [1, 3, 2]) with smooth easing between keys. */
export const k = (t: number, times: number[], values: number[], easing = smooth) => interpolate(t, times, values, {...clamp, easing});

/** 0 to 1 springy pop (overshoots a little) starting at `at`. */
export const pop = (t: number, at: number, d = 0.5) => interpolate(t, [at, at + d], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.6))});
export const fade = (t: number, at: number, d = 0.4) => interpolate(t, [at, at + d], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});

type V3 = [number, number, number];
/** Camera keyframes: [[time, [x,y,z] position, [x,y,z] look-at], ...]. */
export const Cam: React.FC<{keys: Array<[number, V3, V3]>; fov?: number}> = ({keys, fov}) => {
	const t = useSec();
	const camera = useThree((s) => s.camera) as THREE.PerspectiveCamera;
	const times = keys.map((x) => x[0]);
	const at = (i: 1 | 2, axis: 0 | 1 | 2) => (times.length === 1 ? keys[0][i][axis] : k(t, times, keys.map((x) => x[i][axis])));
	useFrame(() => {
		camera.position.set(at(1, 0), at(1, 1), at(1, 2));
		camera.lookAt(at(2, 0), at(2, 1), at(2, 2));
		if (fov && camera.fov !== fov) {
			camera.fov = fov;
			camera.updateProjectionMatrix();
		}
	}, -1);
	return null;
};

const Arches: React.FC<{z?: number}> = ({z = -5}) => {
	const glow = useMemo(() => new THREE.MeshStandardMaterial({color: '#ffcf7a', emissive: new THREE.Color('#f2ad3c'), emissiveIntensity: 2.2, toneMapped: false}), []);
	return (
		<group position={[0, 0, z + 5]}>
			{[-5, -8.5, -12, -15.5, -19].map((az, i) => (
				<mesh key={az} position={[0, 0, az]} material={glow}>
					<torusGeometry args={[5.2 + i * 0.15, 0.045, 12, 120, Math.PI]} />
				</mesh>
			))}
			{[-4.2, 4.2].flatMap((x) =>
				[-3, -6.5, -10].map((pz) => (
					<mesh key={`${x}${pz}`} position={[x, 2.2, pz]} material={glow}>
						<boxGeometry args={[0.05, 4.4, 0.05]} />
					</mesh>
				)),
			)}
		</group>
	);
};

/** The shared studio: background, fog, warm lights, gold arches and a softly reflective floor. */
export const GoldWorld: React.FC<{dim?: number; archZ?: number; fogNear?: number; fogFar?: number; floor?: boolean}> = ({dim = 1, archZ = -5, fogNear = 9, fogFar = 30, floor = true}) => (
	<>
		<color attach="background" args={['#050403']} />
		<fog attach="fog" args={['#050403', fogNear, fogFar]} />
		<StudioLights shadowY={0.001} shadowScale={14} />
		<spotLight position={[0, 7, 3]} angle={0.5} penumbra={0.8} intensity={60 * dim} color="#fff1d6" distance={22} />
		<pointLight position={[-3, 2.5, -3]} intensity={12 * dim} color="#f2ad3c" distance={12} />
		<pointLight position={[3, 2.5, -3]} intensity={12 * dim} color="#f2ad3c" distance={12} />
		<Arches z={archZ} />
		{floor ? (
			<mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
				<planeGeometry args={[60, 60]} />
				<MeshReflectorMaterial resolution={512} mirror={0.45} blur={[400, 140]} mixBlur={1} mixStrength={1.2} depthScale={0.6} minDepthThreshold={0.6} color="#0d0a06" metalness={0.5} roughness={0.8} />
			</mesh>
		) : null}
	</>
);

/**
 * Text carved in 3D from MTG's Anton font, centred on its position and never wider than maxWidth (world units).
 * Change `text` freely (counters): a new shape is built for each value.
 */
export const GoldText: React.FC<{
	text: string;
	size?: number;
	depth?: number;
	maxWidth?: number;
	material?: THREE.Material;
	position?: V3;
	rotation?: V3;
	scale?: number;
	align?: 'center' | 'left';
}> = ({text, size = 0.5, depth = 0.32, maxWidth = 99, material = GOLD, position = [0, 0, 0], rotation = [0, 0, 0], scale = 1, align = 'center'}) => {
	const group = useRef<THREE.Group>(null);
	useFrame(() => {
		const mesh = group.current?.children.find((c) => (c as THREE.Mesh).isMesh) as THREE.Mesh | undefined;
		if (!mesh) return;
		mesh.geometry.computeBoundingBox();
		const bb = mesh.geometry.boundingBox;
		if (!bb) return;
		const fit = Math.min(1, maxWidth / Math.max(0.001, bb.max.x - bb.min.x));
		mesh.scale.setScalar(fit);
		const x = align === 'center' ? (-(bb.max.x + bb.min.x) / 2) * fit : -bb.min.x * fit;
		mesh.position.set(x, (-(bb.max.y + bb.min.y) / 2) * fit, -size * depth * 0.5 * fit);
	});
	return (
		<group ref={group} position={position} rotation={rotation} scale={scale}>
			<Text3D key={text} font={FONT} size={size} height={size * depth} bevelEnabled bevelSize={size * 0.025} bevelThickness={size * 0.04} bevelSegments={3} curveSegments={6} material={material}>
				{text}
			</Text3D>
		</group>
	);
};

/**
 * Keeps its children in front of the camera (dist units away, `up` units above the centre line), turning gently so
 * their depth shows. A warm light travels with them, so gold never goes dark. 0.86 up at dist 5 sits about a quarter
 * of the way down a 9:16 frame.
 */
export const OnCamera: React.FC<{children: React.ReactNode; dist?: number; up?: number; right?: number; swing?: number; scale?: number}> = ({children, dist = 5, up = 0, right = 0, swing = 0.2, scale = 1}) => {
	const t = useSec();
	const camera = useThree((s) => s.camera);
	const g = useRef<THREE.Group>(null);
	const sw = Math.sin(t * 0.9) * swing;
	useFrame(() => {
		const grp = g.current;
		if (!grp) return;
		const q = camera.quaternion;
		grp.position.copy(camera.position)
			.add(new THREE.Vector3(0, 0, -1).applyQuaternion(q).multiplyScalar(dist))
			.add(new THREE.Vector3(0, 1, 0).applyQuaternion(q).multiplyScalar(up))
			.add(new THREE.Vector3(1, 0, 0).applyQuaternion(q).multiplyScalar(right));
		grp.quaternion.copy(q);
		grp.rotateY(sw);
		grp.scale.setScalar(Math.max(0.0001, scale));
	});
	return (
		<group ref={g}>
			{children}
			<pointLight position={[0.6, 0.8, 2.2]} intensity={9} color="#fff1d6" distance={6} />
		</group>
	);
};

export const Pedestal: React.FC<{position?: V3; radius?: number; height?: number}> = ({position = [0, 0, 0], radius = 1.05, height = 1}) => (
	<group position={position}>
		<mesh position={[0, height / 2, 0]} material={DARK} receiveShadow>
			<cylinderGeometry args={[radius, radius * 1.1, height, 64]} />
		</mesh>
		<mesh position={[0, height, 0]} rotation={[Math.PI / 2, 0, 0]} material={GOLD}>
			<torusGeometry args={[radius, 0.035, 16, 96]} />
		</mesh>
	</group>
);

const COIN_GEO = new THREE.CylinderGeometry(0.26, 0.26, 0.06, 40);
/** A gold coin. upright = facing the camera like a medal; symbol is carved on its face. */
export const Coin3D: React.FC<{position?: V3; rotation?: V3; scale?: number; symbol?: string; upright?: boolean; material?: THREE.Material}> = ({position = [0, 0, 0], rotation = [0, 0, 0], scale = 1, symbol, upright, material = GOLD}) => (
	<group position={position} rotation={rotation} scale={scale}>
		<group rotation={upright ? [Math.PI / 2, 0, 0] : [0, 0, 0]}>
			<mesh geometry={COIN_GEO} material={material} castShadow />
			<mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0.03, 0]} material={GOLD_HI}>
				<torusGeometry args={[0.22, 0.012, 8, 48]} />
			</mesh>
		</group>
		{symbol ? <GoldText text={symbol} size={0.26} depth={0.25} material={GOLD_HI} position={[0, 0, upright ? 0.045 : 0]} rotation={upright ? [0, 0, 0] : [-Math.PI / 2, 0, 0]} /> : null}
	</group>
);

const NOTE_W = 1.6;
const NOTE_H = 0.72;
/** A generic banknote in 3D (deliberately not a copy of any real design). grey: 0 colour, 1 grey (worthless). */
export const Note3D: React.FC<{position?: V3; rotation?: V3; scale?: number; grey?: number; label?: string}> = ({position = [0, 0, 0], rotation = [0, 0, 0], scale = 1, grey = 0, label = 'Z$'}) => {
	const mats = useMemo(() => {
		const base = new THREE.Color('#4f7a4a').lerp(new THREE.Color('#6b6b66'), grey);
		const light = new THREE.Color('#9cc28a').lerp(new THREE.Color('#a9a9a2'), grey);
		return {
			base: new THREE.MeshStandardMaterial({color: base, roughness: 0.7, metalness: 0.05}),
			line: new THREE.MeshStandardMaterial({color: light, roughness: 0.6}),
		};
	}, [grey]);
	return (
		<group position={position} rotation={rotation} scale={scale}>
			<mesh material={mats.base} castShadow>
				<boxGeometry args={[NOTE_W, NOTE_H, 0.012]} />
			</mesh>
			{[
				[0, NOTE_H / 2 - 0.06, NOTE_W - 0.12, 0.018],
				[0, -NOTE_H / 2 + 0.06, NOTE_W - 0.12, 0.018],
			].map(([x, y, w, h], i) => (
				<mesh key={i} position={[x, y, 0.008]} material={mats.line}>
					<boxGeometry args={[w, h, 0.004]} />
				</mesh>
			))}
			<mesh position={[NOTE_W * 0.3, 0, 0.008]} material={mats.line}>
				<torusGeometry args={[0.17, 0.014, 8, 48]} />
			</mesh>
			<GoldText text={label} size={0.16} depth={0.08} material={mats.line} position={[-NOTE_W * 0.32, NOTE_H * 0.18, 0.012]} />
		</group>
	);
};
export const NOTE_SIZE = {w: NOTE_W, h: NOTE_H};

/** Small glowing gold dust that drifts upward: life in the air without distracting. */
export const Dust: React.FC<{count?: number; spread?: number}> = ({count = 60, spread = 8}) => {
	const t = useSec();
	const mat = useMemo(() => new THREE.MeshBasicMaterial({color: '#ffd98e', transparent: true, opacity: 0.55, toneMapped: false}), []);
	const geo = useMemo(() => new THREE.SphereGeometry(0.02, 6, 6), []);
	return (
		<group>
			{Array.from({length: count}, (_, i) => {
				const r = (n: number) => (Math.sin(i * 12.9898 + n * 78.233) * 43758.5453) % 1;
				const x = (Math.abs(r(1)) - 0.5) * spread;
				const z = (Math.abs(r(2)) - 0.5) * spread - 2;
				const y = ((Math.abs(r(3)) * 6 + t * (0.15 + Math.abs(r(4)) * 0.2)) % 6) + 0.2;
				return <mesh key={i} geometry={geo} material={mat} position={[x, y, z]} />;
			})}
		</group>
	);
};

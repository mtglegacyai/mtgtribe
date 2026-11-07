import {useTexture} from '@react-three/drei';
import {ThreeCanvas} from '@remotion/three';
import {geoMercator, geoPath} from 'd3-geo';
import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, staticFile, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import {feature} from 'topojson-client';
import type {GeometryCollection, Topology} from 'topojson-specification';
import countries50m from 'world-atlas/countries-50m.json';
import {COLORS, FILES} from '../../brand';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {Cam, CHAMPAGNE, Coin3D, DARK, Dust, fade, GOLD, GOLD_HI, GoldText, GoldWorld, k, Note3D, OnCamera, Pedestal, pop, RED, useSec} from '../../three/kit3d';
import {Loaf3D} from './Hook3D';
import {S12Outro} from './scenes';
import {BrandIcon, Chip, Cues, type Cue, GOLD_TEXT, LeoClip, Panel} from './ui';

// Video 01 in REAL 3D (vertical 9:16): every scene is a Three.js world (MTG's black-and-gold studio) with carved gold
// text and 3D props. 2D is kept only where it reads better on a phone: captions, chips, the quote, the call to action
// and the end card. Times are seconds inside each section, from the narration's word timings.

const LEO_TALL: React.CSSProperties = {left: 160, top: 320, width: 760, height: 1330};
const LEO_FACE: React.CSSProperties = {left: 140, top: 730, width: 800, height: 540};
const FACE = '50% 3%';
const TAB = 290;

/** In at `a`, out at `b` (0 to 1 to 0), with a little overshoot on the way in. */
const win = (t: number, a: number, b: number, d = 0.45) => Math.min(pop(t, a, d), 1 - fade(t, b, 0.3));

const Canvas3D: React.FC<{children: React.ReactNode}> = ({children}) => {
	const {width, height} = useVideoConfig();
	return (
		<ThreeCanvas width={width} height={height} gl={{antialias: true, toneMapping: THREE.ACESFilmicToneMapping}} camera={{fov: 42, near: 0.1, far: 80}} shadows>
			{children}
		</ThreeCanvas>
	);
};

const Top: React.FC<{children: React.ReactNode; top?: number; o?: number}> = ({children, top = TAB, o = 1}) => (
	<div style={{position: 'absolute', top, left: 40, right: 40, textAlign: 'center', opacity: o}}>{children}</div>
);

const Line: React.FC<{children: React.ReactNode; size?: number}> = ({children, size = 50}) => (
	<div style={{fontFamily: BODY, fontWeight: 800, fontSize: size, color: COLORS.text, textShadow: '0 4px 20px rgba(0,0,0,0.95)', lineHeight: 1.2}}>{children}</div>
);

// S02: MTG's photo as a gold medallion (always a circle, the whole photo), his name carved in gold
const Medallion: React.FC<{t: number}> = ({t}) => {
	const tex = useTexture(staticFile(FILES.photo));
	useMemo(() => {
		tex.colorSpace = THREE.SRGBColorSpace;
	}, [tex]);
	const p = pop(t, 0.1, 1.1);
	const z = interpolate(p, [0, 1], [-6, 0]);
	const spin = interpolate(p, [0, 1], [-Math.PI * 2, 0]) + Math.sin(t * 0.8) * 0.12;
	return (
		<group position={[0, 2.45 + Math.sin(t * 1.3) * 0.04, z]} rotation={[0, spin, 0]}>
			<mesh>
				<circleGeometry args={[0.8, 96]} />
				<meshBasicMaterial map={tex} toneMapped={false} />
			</mesh>
			<mesh position={[0, 0, -0.06]} rotation={[Math.PI / 2, 0, 0]} material={GOLD}>
				<cylinderGeometry args={[0.84, 0.84, 0.1, 96]} />
			</mesh>
			<mesh material={GOLD_HI}>
				<torusGeometry args={[0.82, 0.035, 20, 120]} />
			</mesh>
			<mesh position={[0, 0, -0.12]}>
				<torusGeometry args={[0.9, 0.06, 12, 120]} />
				<meshBasicMaterial color="#f2ad3c" transparent opacity={0.25 + Math.sin(t * 2) * 0.08} toneMapped={false} />
			</mesh>
		</group>
	);
};

export const S02Greeting3D: React.FC = () => {
	const t = useSec();
	const chip = fade(t, 6.0, 0.5);
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld />
				<Dust />
				<Cam keys={[[0, [-0.7, 1.8, 7.2], [0, 1.5, 0]], [12, [0.6, 1.7, 6.4], [0, 1.5, 0]]]} />
				<Medallion t={t} />
				<GoldText text="MTG" size={0.5} position={[0, 1.18, 0.2]} scale={Math.max(0.001, pop(t, 1.3) * (1 - chip))} material={GOLD} />
				<GoldText text="YOUR DIGITAL ARCHITECT" size={0.16} depth={0.2} maxWidth={2.4} position={[0, 0.82, 0.2]} scale={Math.max(0.001, pop(t, 2.2) * (1 - chip))} material={CHAMPAGNE} />
			</Canvas3D>
			<Top top={1090} o={chip}>
				<Chip size={32}>WHEN MONEY STOPS KEEPING ITS PROMISE</Chip>
			</Top>
			<Cues list={[[0.1, 'glow', 0.45], [1.3, 'thud', 0.3], [6.1, 'pluck3', 0.4]]} />
		</AbsoluteFill>
	);
};

// S03: 2008, a real 3D map of southern Africa rising out of the floor, then the question
const REGION = ['710', '716', '072', '508', '516', '894', '426', '748'];
const MAP = (() => {
	const topo = countries50m as unknown as Topology<{countries: GeometryCollection<{name: string}>}>;
	const feats = feature(topo, topo.objects.countries).features.filter((f) => REGION.includes(String(f.id)));
	const proj = geoMercator().fitExtent([[-1.75, -1.75], [1.75, 1.75]], {type: 'FeatureCollection', features: feats});
	const path = geoPath(proj);
	const pt = ([lon, lat]: number[]) => {
		const [x, y] = proj([lon, lat]) ?? [0, 0];
		return new THREE.Vector2(x, -y);
	};
	return feats.map((f) => {
		const g = f.geometry as unknown as {type: string; coordinates: number[][][] | number[][][][]};
		const polys = (g.type === 'Polygon' ? [g.coordinates] : g.coordinates) as number[][][][];
		const shapes = polys.map((rings) => {
			const sh = new THREE.Shape(rings[0].map(pt));
			rings.slice(1).forEach((h) => sh.holes.push(new THREE.Path(h.map(pt))));
			return sh;
		});
		const [cx, cy] = path.centroid(f);
		return {id: String(f.id), geo: new THREE.ExtrudeGeometry(shapes, {depth: 0.1, bevelEnabled: false}), cx, cy};
	});
})();
const ZW = MAP.find((m) => m.id === '716') ?? MAP[0];
const SA = MAP.find((m) => m.id === '710') ?? MAP[0];

const Map3D: React.FC<{t: number}> = ({t}) => {
	const mats = useMemo(
		() => ({
			other: new THREE.MeshStandardMaterial({color: '#2a2117', metalness: 0.3, roughness: 0.6}),
			sa: new THREE.MeshStandardMaterial({color: '#b07a2a', metalness: 0.8, roughness: 0.3}),
			zw: new THREE.MeshStandardMaterial({color: '#ffd98e', metalness: 0.9, roughness: 0.2, emissive: new THREE.Color('#f2ad3c'), emissiveIntensity: 0}),
		}),
		[],
	);
	mats.zw.emissiveIntensity = fade(t, 7.7, 0.6) * 0.6;
	const base = k(t, [5.6, 6.4], [0.01, 1]);
	const sa = base + k(t, [6.7, 7.3], [0, 2]);
	const zw = base + k(t, [7.7, 8.4], [0, 4]);
	return (
		<group rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
			{MAP.map((m) => (
				<mesh key={m.id} geometry={m.geo} material={m.id === '716' ? mats.zw : m.id === '710' ? mats.sa : mats.other} scale={[1, 1, m.id === '716' ? zw : m.id === '710' ? sa : base]} castShadow receiveShadow />
			))}
			<GoldText text="SOUTH AFRICA" size={0.15} depth={0.15} material={CHAMPAGNE} position={[SA.cx, -SA.cy, sa * 0.1 + 0.03]} scale={Math.max(0.001, fade(t, 6.8))} />
			<GoldText text="ZIMBABWE" size={0.17} depth={0.15} material={GOLD_HI} position={[ZW.cx, -ZW.cy, zw * 0.1 + 0.03]} scale={Math.max(0.001, pop(t, 7.8))} />
		</group>
	);
};

export const S03Setup3D: React.FC = () => {
	const t = useSec();
	const zx = ZW.cx;
	const zz = ZW.cy;
	const q = win(t, 16.8, 99);
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld archZ={-7} />
				<Cam
					keys={[
						[0, [0, 3.2, 8.5], [0, 1.6, 0]],
						[5.4, [0, 4.6, 6.5], [0, 0.6, 0]],
						[7.4, [0, 5.0, 4.4], [0, 0, 0.3]],
						[9.6, [zx * 0.6 + 0.4, 4.2, zz * 0.6 + 3.8], [zx * 0.6, 0.2, zz * 0.6]],
						[15.5, [zx * 0.6 - 0.5, 4.4, zz * 0.6 + 4.0], [zx * 0.6, 0.2, zz * 0.6]],
						[17.6, [0, 3.0, 7.0], [0, 1.2, 0]],
					]}
				/>
				<Map3D t={t} />
				<OnCamera up={0.86} scale={win(t, 4.45, 5.6)}>
					<GoldText text="2008" size={0.8} maxWidth={1.7} />
				</OnCamera>
				<OnCamera up={0.86} scale={q}>
					<GoldText text="HOW MANY ZEROS?" size={0.42} maxWidth={1.85} />
				</OnCamera>
				<OnCamera up={-0.15} swing={0.6} scale={q}>
					<GoldText text="?" size={1.1} material={GOLD_HI} rotation={[0, Math.sin(t * 1.3) * 0.55, 0]} />
				</OnCamera>
			</Canvas3D>
			<Top top={300} o={Math.min(fade(t, 1.6), 1 - fade(t, 4.3, 0.3))}>
				<Line size={56}>This is not science fiction.</Line>
			</Top>
			<Top top={300} o={Math.min(fade(t, 10.8), 1 - fade(t, 16.4, 0.3))}>
				<Chip size={32}>ONE LESSON THAT STILL PROTECTS PEOPLE</Chip>
			</Top>
			<Top top={1150} o={fade(t, 22.2)}>
				<Chip size={40}>COMMENT YOUR GUESS 💬</Chip>
			</Top>
			<Cues list={[[1.6, 'air', 0.35], [4.5, 'thud', 0.5], [5.6, 'rise', 0.45], [6.7, 'pluck2', 0.35], [7.7, 'pluck4', 0.45], [10.8, 'pluck2', 0.3], [16.8, 'tension', 0.5], [20.2, 'chime', 0.45], [22.2, 'pluck3', 0.4]]} />
		</AbsoluteFill>
	);
};

// S04: Hanke and Kwok, a gold clock racing to 24.7 hours, then the pay bars that halve and melt
const BAR_AT = [13.2, 14.2, 14.6, 15.0, 15.4, 15.8, 16.4, 16.9];
const DAYS = ['FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI'];
const Clock3D: React.FC<{t: number}> = ({t}) => {
	const spin = k(t, [5.6, 8.4], [0, Math.PI * 2 * 9]);
	const s = win(t, 5.4, 11.6, 0.6);
	return (
		<group position={[0, 1.7, 0]} scale={Math.max(0.001, s * 0.78)}>
			<mesh rotation={[Math.PI / 2, 0, 0]} material={DARK}>
				<cylinderGeometry args={[0.85, 0.85, 0.12, 96]} />
			</mesh>
			<mesh position={[0, 0, 0.06]} material={GOLD}>
				<torusGeometry args={[0.86, 0.05, 16, 120]} />
			</mesh>
			{Array.from({length: 12}, (_, i) => (
				<mesh key={i} position={[Math.sin((i / 12) * Math.PI * 2) * 0.7, Math.cos((i / 12) * Math.PI * 2) * 0.7, 0.07]} rotation={[0, 0, -(i / 12) * Math.PI * 2]} material={GOLD_HI}>
					<boxGeometry args={[0.04, i % 3 === 0 ? 0.16 : 0.09, 0.02]} />
				</mesh>
			))}
			<group rotation={[0, 0, -spin]} position={[0, 0, 0.09]}>
				<mesh position={[0, 0.28, 0]} material={GOLD_HI}>
					<boxGeometry args={[0.04, 0.58, 0.02]} />
				</mesh>
			</group>
			<group rotation={[0, 0, -spin / 12 - 0.5]} position={[0, 0, 0.1]}>
				<mesh position={[0, 0.18, 0]} material={GOLD}>
					<boxGeometry args={[0.06, 0.38, 0.02]} />
				</mesh>
			</group>
			<mesh position={[0, 0, 0.12]} material={GOLD_HI}>
				<sphereGeometry args={[0.05, 16, 16]} />
			</mesh>
		</group>
	);
};

const PayBars: React.FC<{t: number}> = ({t}) => {
	const melt = 1 - k(t, [21.2, 22.6], [0, 1]);
	return (
		<group position={[0, 0, 0]}>
			{DAYS.map((d, i) => {
				const h = 2.4 * 0.5 ** i;
				const g = Math.min(1, fade(t, BAR_AT[i], 0.35)) * melt;
				const x = -1.45 + i * 0.42;
				const z = -i * 0.25;
				const last = i === DAYS.length - 1;
				return (
					<group key={i} position={[x, 0, z]}>
						<mesh position={[0, (Math.max(0.03, h) * g) / 2, 0]} scale={[1, Math.max(0.001, g), 1]} material={last ? RED : GOLD} castShadow>
							<boxGeometry args={[0.3, Math.max(0.03, h), 0.3]} />
						</mesh>
						<GoldText text={d} size={0.12} depth={0.15} material={CHAMPAGNE} position={[0, -0.12, 0.25]} scale={Math.max(0.001, fade(t, BAR_AT[i]) * melt)} />
					</group>
				);
			})}
		</group>
	);
};

export const S04Doubling3D: React.FC = () => {
	const t = useSec();
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld />
				<Dust count={40} />
				<Cam
					keys={[
						[0, [0, 2.2, 7.5], [0, 1.7, 0]],
						[5.0, [0, 2.2, 6.6], [0, 1.6, 0]],
						[11.0, [0.3, 2.3, 6.3], [0, 1.6, 0]],
						[12.6, [1.6, 2.4, 4.9], [-0.45, 0.7, -0.9]],
						[19.5, [1.3, 2.2, 4.5], [-0.5, 0.6, -0.9]],
						[22.6, [1.0, 2.6, 5.0], [-0.5, 0.3, -0.9]],
					]}
				/>
				<OnCamera up={0.86} scale={win(t, 0.2, 2.1)}>
					<GoldText text="NOVEMBER 2008" size={0.36} maxWidth={1.85} />
				</OnCamera>
				<Clock3D t={t} />
				<OnCamera up={0.86} scale={win(t, 8.4, 11.5)}>
					<GoldText text="24.7 HOURS" size={0.48} maxWidth={1.85} material={GOLD_HI} />
				</OnCamera>
				<PayBars t={t} />
				<OnCamera up={0.86} scale={win(t, 17.8, 20.4)}>
					<GoldText text="UNDER 1%" size={0.55} maxWidth={1.85} material={GOLD_HI} />
				</OnCamera>
			</Canvas3D>
			<Top top={300} o={Math.min(fade(t, 2.2), 1 - fade(t, 5.4, 0.3))}>
				<Chip size={30}>ECONOMISTS STEVE HANKE AND ALEX KWOK</Chip>
			</Top>
			<Top top={300} o={Math.min(fade(t, 6.6), 1 - fade(t, 8.2, 0.3))}>
				<Line size={52}>Prices doubled about every...</Line>
			</Top>
			<Top top={300} o={Math.min(fade(t, 12.4), 1 - fade(t, 17.6, 0.3))}>
				<Chip size={32}>YOUR PAY, FRIDAY TO FRIDAY</Chip>
			</Top>
			<Top top={300} o={fade(t, 20.6)}>
				<Chip size={34}>SO HOW DOES MONEY MELT?</Chip>
			</Top>
			<Cues list={[[0.3, 'air', 0.35], [2.2, 'pluck2', 0.3], [5.6, 'whirr', 0.4], [8.4, 'reveal', 0.55], [12.0, 'air', 0.35], ...BAR_AT.map((a, i) => [a, `pluck${Math.max(1, 5 - i)}`, 0.45 - i * 0.035] as Cue), [17.8, 'drop', 0.55], [21.2, 'melt', 0.45]]} />
		</AbsoluteFill>
	);
};

// S05: Leo thinks; then money printed (stacks of notes grow) while goods disappear; the loaf's price climbs
const PRICE_STEPS = [13.9, 14.9, 15.9, 16.9, 17.9, 18.9];
const Printing: React.FC<{t: number}> = ({t}) => {
	const stack = k(t, [4.1, 7.3, 11.0, 13.0, 16.0, 21.5], [0.05, 0.6, 0.6, 1.0, 1.0, 1.8]);
	const crates = k(t, [4.1, 7.3, 18.6, 21.0], [8, 6, 6, 2]);
	const falling = [4.3, 4.8, 5.3, 11.2, 11.7, 16.5, 17.0, 17.5, 18.0];
	return (
		<group>
			{[-1.05, -0.95].map((x, si) => (
				<group key={si} position={[x, 0, 0.35 - si * 0.7]}>
					<mesh position={[0, (stack * (si ? 0.85 : 1)) / 2, 0]} castShadow>
						<boxGeometry args={[0.5, Math.max(0.01, stack * (si ? 0.85 : 1)), 0.26]} />
						<meshStandardMaterial color="#5d8a55" roughness={0.75} />
					</mesh>
					<Note3D scale={0.32} position={[0, stack * (si ? 0.85 : 1) + 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]} />
				</group>
			))}
			{falling.map((at, i) => {
				if (t < at || t > at + 0.9) return null;
				const p = (t - at) / 0.9;
				return <Note3D key={i} scale={0.32} position={[-1.0, 3.6 - p * (3.4 - stack), 0.35 - (i % 2) * 0.7]} rotation={[-Math.PI / 2 + p * 3, p * 2, p]} />;
			})}
			{Array.from({length: 8}, (_, i) => {
				const s = Math.max(0.001, Math.min(1, Math.max(0, crates - i)));
				return (
					<mesh key={i} position={[0.95 + (i % 2) * 0.36, 0.16 * s, 0.4 - Math.floor(i / 2) * 0.38]} scale={s} material={i % 2 ? DARK : GOLD} castShadow>
						<boxGeometry args={[0.32, 0.32, 0.32]} />
					</mesh>
				);
			})}
			<GoldText text="MONEY PRINTED" size={0.11} depth={0.15} maxWidth={0.85} material={CHAMPAGNE} position={[-1.0, Math.max(0.6, stack + 0.3), 0.35]} scale={Math.max(0.001, fade(t, 4.4))} />
			<GoldText text="GOODS MADE" size={0.11} depth={0.15} maxWidth={0.75} material={CHAMPAGNE} position={[1.13, 0.6, 0.4]} scale={Math.max(0.001, fade(t, 4.6))} />
		</group>
	);
};

export const S05Why3D: React.FC = () => {
	const t = useSec();
	const steps = PRICE_STEPS.filter((s) => t >= s).length;
	const price = `R${(10 * 2 ** steps).toLocaleString('en-US')}`;
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld />
				<Dust count={40} />
				<Cam keys={[[0, [0, 2.3, 8.4], [0, 1.4, 0]], [4.0, [0, 2.4, 7.4], [0, 0.95, 0]], [14.0, [0.3, 2.5, 7.2], [0, 0.95, 0]], [21.7, [-0.3, 2.7, 7.3], [0, 0.9, 0]]]} />
				<Pedestal radius={0.62} height={0.75} />
				<Loaf3D position={[0, 0.77, 0]} size={0.5} pulses={PRICE_STEPS} />
				<Printing t={t} />
				<GoldText text={price} size={0.4} maxWidth={2.2} material={steps ? GOLD_HI : GOLD} position={[0, 1.75, 0]} scale={Math.max(0.001, fade(t, 8.5))} />
			</Canvas3D>
			<LeoClip clip="V5" from={0} seconds={4.0} style={LEO_TALL} />
			<Top o={Math.min(fade(t, 0.3), 1 - fade(t, 3.8, 0.3))}>
				<Chip size={32}>CAUSES ARE DEBATED. ONE IS CLEAR:</Chip>
			</Top>
			<Top o={fade(t, 14.5)}>
				<Chip size={30}>MORE MONEY + FEWER GOODS = HIGHER PRICES</Chip>
				<div style={{fontFamily: BODY, fontSize: 26, color: COLORS.muted, marginTop: 6}}>(simplified)</div>
			</Top>
			<Cues list={[[0.0, 'air', 0.35], [4.1, 'flutter', 0.4], [8.5, 'air', 0.3], [11.2, 'flutter', 0.3], [11.9, 'coin', 0.45], ...PRICE_STEPS.map((a) => [a, 'tick', 0.3] as Cue), [14.5, 'pluck3', 0.35], [16.5, 'flutter', 0.35], [19.0, 'drop', 0.4]]} />
		</AbsoluteFill>
	);
};

// S06: how people coped (three moments), respect, then Leo asks what you would buy first
export const S06Coping3D: React.FC = () => {
	const t = useSec();
	const respect = Math.min(fade(t, 17.9, 0.6), 1 - fade(t, 21.9, 0.3));
	const fly = k(t, [4.6, 6.8], [0, 1]);
	const swap = k(t, [9.2, 11.6], [0, Math.PI]);
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld dim={1 - respect * 0.7} />
				<Dust count={40} />
				<Cam keys={[[0, [0, 2.0, 7.4], [0, 1.4, 0]], [9, [0.5, 2.1, 6.8], [0, 1.3, 0]], [17, [-0.4, 2.0, 6.6], [0, 1.3, 0]], [22, [0, 1.9, 7.6], [0, 1.4, 0]]]} />
				<OnCamera up={0.86} scale={win(t, 2.2, 3.2)}>
					<GoldText text="THEY ADAPTED" size={0.42} maxWidth={1.85} />
				</OnCamera>
				<OnCamera up={0.86} scale={win(t, 3.3, 8.4)}>
					<GoldText text="SPEND IT FAST" size={0.42} maxWidth={1.85} />
				</OnCamera>
				{t > 3.3 && t < 8.6 ? <Note3D scale={Math.max(0.001, pop(t, 3.4) * 0.9 * (1 - fly * 0.5))} position={[fly * 2.2, 1.45 + fly * 1.6, -fly * 8]} rotation={[0.1 + fly * 0.9, -0.25 + fly * 1.8, fly * 0.4]} /> : null}
				<OnCamera up={0.86} scale={win(t, 8.6, 13.1)}>
					<GoldText text="SWAP GOODS" size={0.42} maxWidth={1.85} />
				</OnCamera>
				{t > 8.4 && t < 13.3 ? (
					<group position={[0, 1.2, 0]} rotation={[0, swap, 0]} scale={Math.max(0.001, win(t, 8.6, 13.0))}>
						<group position={[-0.9, 0, 0]} rotation={[0, -swap, 0]}>
							<mesh material={DARK}><boxGeometry args={[0.9, 0.7, 0.6]} /></mesh>
							<GoldText text="MAIZE" size={0.17} depth={0.2} position={[0, 0, 0.32]} />
						</group>
						<group position={[0.9, 0, 0]} rotation={[0, -swap, 0]}>
							<mesh material={DARK}><boxGeometry args={[0.9, 0.7, 0.6]} /></mesh>
							<GoldText text="SHOES" size={0.17} depth={0.2} position={[0, 0, 0.32]} />
						</group>
					</group>
				) : null}
				<OnCamera up={0.86} scale={win(t, 13.4, 17.6)}>
					<GoldText text="DOLLARS AND RAND" size={0.38} maxWidth={1.85} />
				</OnCamera>
				{t > 13.4 && t < 17.9 ? (
					<group position={[0, 1.25, 0]} scale={Math.max(0.001, win(t, 13.5, 17.6))}>
						<Coin3D upright symbol="$" scale={2.2} position={[-0.75, 0, 0]} rotation={[0, interpolate(pop(t, 15.4, 0.8), [0, 1], [Math.PI, 0]) + Math.sin(t) * 0.2, 0]} />
						<Coin3D upright symbol="R" scale={2.2} position={[0.75, 0, 0]} rotation={[0, interpolate(pop(t, 16.7, 0.8), [0, 1], [Math.PI, 0]) - Math.sin(t) * 0.2, 0]} />
					</group>
				) : null}
			</Canvas3D>
			<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: respect}}>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 64, color: COLORS.champagne, textAlign: 'center', padding: '0 70px', textShadow: '0 0 30px rgba(242,173,60,0.35)'}}>Real families lived through this.</div>
			</AbsoluteFill>
			<LeoClip clip="V2" from={22.3} seconds={6.6} style={LEO_TALL} />
			<Top o={fade(t, 23.5)}>
				<Chip size={38} style={{background: 'rgba(5,4,3,0.85)'}}>WHAT WOULD YOU BUY FIRST? 💬</Chip>
			</Top>
			<Cues list={[[2.2, 'air', 0.3], [3.3, 'pluck1', 0.45], [4.0, 'air', 0.3], [8.6, 'pluck3', 0.45], [9.2, 'air', 0.3], [13.7, 'pluck5', 0.45], [15.4, 'coin', 0.4], [16.7, 'coin', 0.35], [22.3, 'air', 0.3], [23.5, 'chime', 0.5]]} />
		</AbsoluteFill>
	);
};

// S07: the 100 trillion note in 3D, the zeros counted in gold, Leo amazed
export const S07Zeros3D: React.FC = () => {
	const t = useSec();
	const zeros = t < 11.0 ? 0 : Math.min(14, Math.floor((t - 11.0) / 0.09) + 1);
	const num = ('1' + '0'.repeat(zeros)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	const flip = interpolate(pop(t, 4.3, 1.0), [0, 1], [Math.PI, 0]);
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld />
				<Dust count={40} />
				<Cam keys={[[0, [0, 2.0, 7.0], [0, 1.6, 0]], [8.4, [0.4, 2.1, 6.2], [0, 1.6, 0]], [15.8, [-0.3, 2.2, 6.6], [0, 1.7, 0]]]} />
				<Note3D scale={1.35 * Math.max(0.001, win(t, 4.2, 9.0))} position={[0, 1.55, 0]} rotation={[0.1, flip + Math.sin(t * 0.7) * 0.15, 0]} label="Z$100T" />
				<OnCamera up={0.86} scale={win(t, 5.8, 8.6)}>
					<GoldText text="100 TRILLION" size={0.44} maxWidth={1.85} material={GOLD_HI} />
				</OnCamera>
				<OnCamera up={0.86} scale={win(t, 10.5, 12.3, 0.3)}>
					<GoldText text={`Z$${num}`} size={0.3} maxWidth={1.9} />
				</OnCamera>
				<OnCamera up={0.86} scale={pop(t, 12.3)}>
					<GoldText text="14 ZEROS" size={0.5} maxWidth={1.75} material={GOLD_HI} />
				</OnCamera>
			</Canvas3D>
			<Top o={Math.min(fade(t, 0.3), 1 - fade(t, 5.6, 0.3))}>
				<Chip size={28}>JANUARY 2009 ▪ RESERVE BANK OF ZIMBABWE</Chip>
			</Top>
			<Top top={672} o={Math.min(fade(t, 8.4), 1 - fade(t, 10.4, 0.3))}>
				<Chip size={32}>HOW CLOSE WAS YOUR GUESS?</Chip>
			</Top>
			<Top top={672} o={fade(t, 13.4)}>
				<Chip size={32}>AND STILL, NOT ENOUGH</Chip>
			</Top>
			<LeoClip clip="V3" from={9.4} seconds={6.17} style={LEO_FACE} focus={FACE} />
			<Cues list={[[0.3, 'air', 0.35], [4.3, 'flutter', 0.35], [5.8, 'reveal', 0.45], [8.4, 'pluck2', 0.35], [9.4, 'air', 0.3], [9.9, 'swell', 0.45], [11.0, 'count', 0.3], [12.3, 'reveal', 0.55], [14.5, 'thud', 0.4]]} />
		</AbsoluteFill>
	);
};

// S08: banknotes fly onto a wall as posters, the award, abandoned, dollar and rand, the part most people miss
const WALL = Array.from({length: 12}, (_, i) => ({x: ((i % 3) - 1) * 0.95, y: 0.75 + Math.floor(i / 3) * 0.5, at: 6.5 + i * 0.27}));
const Trophy: React.FC<{t: number}> = ({t}) => {
	const pts = useMemo(() => [[0, 0], [0.3, 0], [0.3, 0.06], [0.1, 0.1], [0.06, 0.35], [0.12, 0.42], [0.36, 0.62], [0.42, 0.95], [0.4, 0.97], [0, 0.97]].map(([x, y]) => new THREE.Vector2(x, y)), []);
	return (
		<group rotation={[0, t * 0.8, 0]} position={[0, -0.45, 0]}>
			<mesh material={GOLD}>
				<latheGeometry args={[pts, 64]} />
			</mesh>
			{[-1, 1].map((s) => (
				<mesh key={s} position={[s * 0.42, 0.72, 0]} rotation={[0, 0, s * 0.2]} material={GOLD_HI}>
					<torusGeometry args={[0.13, 0.025, 10, 40, Math.PI]} />
				</mesh>
			))}
		</group>
	);
};

export const S08Posters3D: React.FC = () => {
	const t = useSec();
	const grey = k(t, [26.8, 27.9], [0, 1]);
	const quote = Math.min(fade(t, 12.7), 1 - fade(t, 16.8, 0.3));
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld dim={1 - quote * 0.5} />
				<Cam
					keys={[
						[0, [0, 2.0, 7.6], [0, 1.5, -1]],
						[6.0, [0.2, 1.8, 5.8], [0, 1.5, -1.2]],
						[12.0, [-0.3, 1.9, 5.2], [0, 1.6, -1.2]],
						[23.6, [0, 1.9, 6.0], [0, 1.5, -0.6]],
						[32.4, [0, 1.8, 5.2], [0, 1.4, 0]],
					]}
				/>
				<mesh position={[0, 1.5, -1.5]} material={DARK} receiveShadow>
					<boxGeometry args={[3.6, 2.6, 0.08]} />
				</mesh>
				<mesh position={[0, 1.5, -1.45]} material={GOLD}>
					<boxGeometry args={[3.7, 0.04, 0.04]} />
				</mesh>
				{WALL.map((w, i) => {
					if (t < w.at) return null;
					const p = pop(t, w.at, 0.55);
					const out = 1 - fade(t, 23.4, 0.4);
					return <Note3D key={i} scale={0.55 * Math.max(0.001, out)} position={[w.x, w.y + (1 - p) * 1.5, -1.42 + (1 - p) * 4]} rotation={[(1 - p) * 1.2, (1 - p) * 2, 0]} />;
				})}
				<OnCamera up={0.86} scale={win(t, 10.1, 12.6)}>
					<GoldText text="CHEAPER THAN PAPER" size={0.36} maxWidth={1.85} />
				</OnCamera>
				<OnCamera up={0.75} scale={win(t, 17.8, 23.0, 0.6)}>
					<Trophy t={t} />
				</OnCamera>
				{t > 23.6 && t < 32.6 ? (
					<group position={[0, 1.55, 0]} scale={Math.max(0.001, win(t, 23.9, 32.2))}>
						<Note3D scale={1.25} grey={grey} rotation={[0.08, Math.sin(t * 0.6) * 0.2, 0]} />
						<Coin3D upright symbol="$" scale={1.25 * Math.max(0.001, pop(t, 29.4, 0.8))} position={[-0.7, -0.62, 0.35]} rotation={[0, interpolate(pop(t, 29.4, 0.8), [0, 1], [Math.PI, 0]), 0]} />
						<Coin3D upright symbol="R" scale={1.25 * Math.max(0.001, pop(t, 30.9, 0.8))} position={[0.7, -0.62, 0.35]} rotation={[0, interpolate(pop(t, 30.9, 0.8), [0, 1], [Math.PI, 0]), 0]} />
					</group>
				) : null}
				<OnCamera up={0.55} scale={pop(t, 32.4)}>
					<GoldText text="HERE'S THE PART" size={0.36} maxWidth={1.85} material={CHAMPAGNE} position={[0, 0.3, 0]} />
					<GoldText text="MOST PEOPLE MISS" size={0.4} maxWidth={1.85} material={GOLD_HI} position={[0, -0.2, 0]} />
				</OnCamera>
			</Canvas3D>
			<Top o={Math.min(fade(t, 0.4), 1 - fade(t, 6.3, 0.3))}>
				<Chip size={32}>JOHANNESBURG ▪ MARCH 2009</Chip>
				<div style={{marginTop: 24}}>
					<Line size={46}>An ad agency printed posters straight onto real banknotes</Line>
				</div>
			</Top>
			<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: quote, padding: '0 50px'}}>
				<Panel style={{textAlign: 'center', padding: '34px 30px', background: 'rgba(12,9,5,0.88)'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 80, lineHeight: 1.1, ...GOLD_TEXT}}>"It's cheaper to print this on money than paper."</div>
					<div style={{fontFamily: BODY, fontSize: 28, color: COLORS.muted, marginTop: 16}}>Poster line from the 2009 campaign by TBWA\Hunt\Lascaris, Johannesburg</div>
				</Panel>
			</AbsoluteFill>
			<Top top={655} o={win(t, 17.9, 22.8)}>
				<Chip size={26}>CANNES LIONS 2009 ▪ OUTDOOR GRAND PRIX</Chip>
			</Top>
			<LeoClip clip="V6" from={16.9} seconds={6.0} style={LEO_FACE} focus={FACE} />
			<div style={{position: 'absolute', top: 560, width: '100%', display: 'flex', justifyContent: 'center', opacity: Math.min(fade(t, 25.1), 1 - fade(t, 32.0, 0.3))}}>
				<div style={{transform: `rotate(-10deg) scale(${interpolate(fade(t, 25.1, 0.35), [0, 1], [1.6, 1])})`, border: '6px solid #e0602f', color: '#ff8a4c', fontFamily: DISPLAY, fontSize: 64, padding: '6px 24px', borderRadius: 12, background: 'rgba(5,4,3,0.7)', whiteSpace: 'nowrap'}}>ABANDONED ▪ APRIL 2009</div>
			</div>
			<Cues list={[[0.4, 'air', 0.35], [4.4, 'pluck2', 0.3], [6.5, 'flutter', 0.45], [8.0, 'flutter', 0.35], [10.1, 'pluck3', 0.4], [12.7, 'air', 0.3], [15.1, 'chime', 0.4], [16.9, 'air', 0.3], [17.8, 'glow', 0.45], [23.9, 'air', 0.35], [25.1, 'thud', 0.5], [27.0, 'melt', 0.35], [29.4, 'coin', 0.45], [30.9, 'coin', 0.35], [31.0, 'tension', 0.4], [32.4, 'drop', 0.5]]} />
		</AbsoluteFill>
	);
};

// S09: not paper, not metal; money = promise + trust; the closed shop and the voucher that stops being worth anything
const Shop: React.FC<{t: number}> = ({t}) => {
	const shutter = k(t, [8.2, 9.1], [0, 1]);
	const grey = k(t, [12.0, 12.9], [0, 1]);
	const voucher = useMemo(() => new THREE.MeshStandardMaterial({metalness: 0.8, roughness: 0.3}), []);
	voucher.color = new THREE.Color('#f2ad3c').lerp(new THREE.Color('#5c5a55'), grey);
	const glow = useMemo(() => new THREE.MeshStandardMaterial({color: '#ffe2a8', emissive: new THREE.Color('#f2ad3c'), emissiveIntensity: 1.2, toneMapped: false}), []);
	return (
		<group scale={Math.max(0.001, win(t, 6.6, 99))}>
			<mesh position={[0.3, 1.0, -0.6]} material={DARK} castShadow>
				<boxGeometry args={[2.3, 2.0, 1.0]} />
			</mesh>
			<mesh position={[0.3, 0.75, -0.09]} material={glow}>
				<planeGeometry args={[1.4, 1.2]} />
			</mesh>
			<mesh position={[0.3, 1.35 - (shutter * 1.2) / 2, -0.07]} scale={[1, Math.max(0.001, shutter), 1]}>
				<boxGeometry args={[1.45, 1.2, 0.03]} />
				<meshStandardMaterial color="#6a6a68" metalness={0.7} roughness={0.45} />
			</mesh>
			<GoldText text="SHOP" size={0.3} position={[0.3, 1.75, -0.05]} />
			<GoldText text="CLOSED" size={0.17} material={RED} position={[0.3, 0.75, 0.0]} scale={Math.max(0.001, fade(t, 8.9))} />
			<group position={[-0.45, 2.45, 0.3]} scale={0.8} rotation={[0.15, 0.3 + Math.sin(t * 0.8) * 0.1, -0.1]}>
				<mesh material={voucher}>
					<boxGeometry args={[1.2, 0.62, 0.05]} />
				</mesh>
				<GoldText text="VOUCHER" size={0.15} depth={0.2} material={DARK} position={[0, 0.08, 0.04]} />
				<GoldText text="R500" size={0.13} depth={0.2} material={DARK} position={[0, -0.14, 0.04]} />
			</group>
		</group>
	);
};

export const S09Promise3D: React.FC = () => {
	const t = useSec();
	const cross = (at: number) => Math.min(1, fade(t, at, 0.3));
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld />
				<Dust count={40} />
				<Cam keys={[[0, [0, 2.0, 6.6], [0, 1.4, 0]], [6.0, [0, 2.0, 6.2], [0, 1.4, 0]], [7.0, [-0.4, 2.3, 6.9], [0, 1.4, -0.2]], [17.3, [0.4, 2.4, 7.1], [0, 1.4, -0.2]]]} />
				{t < 3.2 ? (
					<group scale={Math.max(0.001, 1 - fade(t, 2.9, 0.3))}>
						<group position={[-0.75, 1.5, 0]}>
							<Note3D scale={0.75} rotation={[0, 0.3, 0]} />
							<mesh rotation={[0, 0, 0.6]} scale={[cross(1.0), 1, 1]} position={[0, 0, 0.1]} material={RED}><boxGeometry args={[1.5, 0.08, 0.05]} /></mesh>
							<GoldText text="PAPER" size={0.18} material={CHAMPAGNE} position={[0, -0.55, 0]} />
						</group>
						<group position={[0.8, 1.5, 0]}>
							<Coin3D upright scale={2.0} rotation={[0, -0.3, 0]} />
							<mesh rotation={[0, 0, -0.6]} scale={[cross(2.1), 1, 1]} position={[0, 0, 0.15]} material={RED}><boxGeometry args={[1.2, 0.08, 0.05]} /></mesh>
							<GoldText text="METAL" size={0.18} material={CHAMPAGNE} position={[0, -0.75, 0]} />
						</group>
					</group>
				) : null}
				<OnCamera up={0.55} scale={win(t, 3.2, 6.4)}>
					<GoldText text="MONEY = PROMISE" size={0.36} maxWidth={1.85} position={[0, 0.3, 0]} />
					<GoldText text="+ TRUST" size={0.46} maxWidth={1.85} material={GOLD_HI} position={[0, -0.25, 0]} scale={Math.max(0.001, pop(t, 4.6))} />
				</OnCamera>
				<Shop t={t} />
			</Canvas3D>
			<Top o={fade(t, 13.8)}>
				<Chip size={36}>NO TRUST, NO MONEY</Chip>
			</Top>
			<Cues list={[[1.0, 'thud', 0.35], [2.1, 'thud', 0.35], [3.2, 'reveal', 0.5], [6.6, 'air', 0.35], [8.2, 'shutter', 0.5], [12.0, 'melt', 0.4], [13.8, 'pluck1', 0.4]]} />
		</AbsoluteFill>
	);
};

// S10: the lesson: three kinds of money on three pedestals, what stands behind each, knowledge, the comment prompt
const KINDS = [
	{x: -0.98, label: 'CASH', at: 8.8, line: "A government's promise"},
	{x: 0, label: 'STABLECOIN', at: 13.3, line: 'As strong as its company and reserves'},
	{x: 0.98, label: 'BITCOIN', at: 17.0, line: 'Big price swings, up and down'},
];
export const S10Lesson3D: React.FC = () => {
	const t = useSec();
	const focus = t < 8.8 ? -1 : t < 13.3 ? 0 : t < 17.0 ? 1 : t < 20.0 ? 2 : -1;
	const fx = focus >= 0 ? KINDS[focus].x : 0;
	const book = win(t, 21.5, 24.0, 0.6);
	const swing = t > 17.8 && t < 19.8 ? Math.sin((t - 17.8) * 6) * 0.35 : 0;
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld />
				<Dust count={40} />
				<Cam keys={[[0, [0, 2.4, 8.8], [0, 1.3, 0]], [3.3, [0, 2.4, 7.6], [0, 1.0, 0]], [8.4, [0, 2.4, 7.6], [0, 1.0, 0]], [9.2, [fx * 0.8, 2.1, 5.0], [fx, 1.0, 0]], [20.0, [fx * 0.8, 2.1, 5.0], [fx, 1.0, 0]], [21.0, [0, 2.3, 6.6], [0, 1.2, 0]]]} />
				{KINDS.map((kd, i) => {
					const s = Math.max(0.001, Math.min(pop(t, 3.3 + i * 0.5), 1 - fade(t, 21.0, 0.4)));
					const lit = focus === i ? 1 : 0.55;
					return (
						<group key={kd.label} position={[kd.x, 0, 0]} scale={s}>
							<Pedestal radius={0.36} height={0.7} />
							<group position={[0, 1.25 + (i === 2 ? swing : 0), 0]} rotation={[0, t * 0.6 + i, 0]} scale={lit + 0.45}>
								{i === 0 ? <Note3D scale={0.36} /> : <Coin3D upright scale={1.2} symbol={i === 1 ? 'S' : 'B'} />}
							</group>
							<GoldText text={kd.label} size={0.12} depth={0.15} maxWidth={0.85} material={focus === i ? GOLD_HI : CHAMPAGNE} position={[0, 0.35, 0.45]} />
						</group>
					);
				})}
				<group position={[0, 1.4, 0]} scale={Math.max(0.001, book)} rotation={[0.25, t * 0.5, 0]}>
					<mesh material={GOLD}><boxGeometry args={[1.0, 1.3, 0.22]} /></mesh>
					<mesh position={[0.02, 0, 0]}><boxGeometry args={[0.96, 1.24, 0.24]} /><meshStandardMaterial color="#f7efe0" roughness={0.8} /></mesh>
				</group>
				<OnCamera up={0.86} scale={win(t, 22.7, 24.0)}>
					<GoldText text="KNOWLEDGE" size={0.55} maxWidth={1.85} material={GOLD_HI} />
				</OnCamera>
				<OnCamera up={0.4} scale={pop(t, 24.2)}>
					<GoldText text="MONEY IS ___ ?" size={0.5} maxWidth={1.85} />
				</OnCamera>
			</Canvas3D>
			<LeoClip clip="V7" from={0} seconds={3.3} style={LEO_TALL} />
			<Top o={Math.min(fade(t, 0.3), 1 - fade(t, 3.1, 0.3))}>
				<Chip size={40}>THE LESSON</Chip>
			</Top>
			<Top o={Math.min(fade(t, 3.3), 1 - fade(t, 8.6, 0.3))}>
				<Chip size={27}>NEVER PUT ALL YOUR TRUST IN ONE KIND OF MONEY</Chip>
			</Top>
			{KINDS.map((kd, i) => (
				<Top key={kd.label} o={focus === i ? fade(t, kd.at + 0.3) : 0}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.muted, letterSpacing: 3}}>WHAT STANDS BEHIND IT?</div>
					<Line size={48}>{kd.line}</Line>
				</Top>
			))}
			<Top o={Math.min(fade(t, 20.0), 1 - fade(t, 21.4, 0.3))}>
				<Line size={56}>No money is perfect.</Line>
			</Top>
			<Top top={1150} o={fade(t, 24.4)}>
				<Chip size={30}>FINISH THE SENTENCE IN THE COMMENTS 💬</Chip>
			</Top>
			<Cues list={[[0.0, 'air', 0.35], [3.3, 'pluck1', 0.4], [3.8, 'pluck3', 0.4], [4.3, 'pluck5', 0.4], [8.8, 'tick', 0.35], [13.3, 'tick', 0.35], [17.0, 'tick', 0.35], [17.8, 'air', 0.25], [20.0, 'swell', 0.45], [22.7, 'reveal', 0.5], [24.2, 'chime', 0.5]]} />
		</AbsoluteFill>
	);
};

// S11: the MTG TRIBE in carved gold (MTG's theme is playing: only soft toneless effects)
export const S11Tribe3D: React.FC = () => {
	const t = useSec();
	const cta = pop(t, 12.3, 0.5);
	const share = fade(t, 15.8);
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld dim={1 - share * 0.5} />
				<Dust count={90} />
				<Cam keys={[[0, [0, 1.9, 7.0], [0, 1.5, 0]], [12, [0.8, 2.0, 6.2], [0, 1.6, 0]], [20.2, [-0.6, 2.1, 6.6], [0, 1.6, 0]]]} />
				<OnCamera up={0.6} swing={0.25} scale={Math.min(pop(t, 1.8, 0.7), 1 - share)}>
					<GoldText text="MTG TRIBE" size={0.62} maxWidth={1.9} material={GOLD_HI} />
				</OnCamera>
			</Canvas3D>
			<Top o={Math.min(fade(t, 0.3), 1 - fade(t, 2.2, 0.3))}>
				<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 38, color: COLORS.champagne, letterSpacing: 4}}>THAT'S EXACTLY WHY THE</div>
			</Top>
			<div style={{position: 'absolute', top: 760, left: 0, right: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16, opacity: 1 - fade(t, 11.9, 0.4)}}>
				<div style={{opacity: fade(t, 3.8)}}><Line size={48}>A community of action takers</Line></div>
				{([['LEARN HOW MONEY WORKS', 5.9], ['OLD AND NEW', 7.8], ['YOUR OWN DECISIONS', 9.0]] as Array<[string, number]>).map(([w, at]) => (
					<div key={w} style={{opacity: fade(t, at), transform: `translateY(${(1 - fade(t, at)) * 20}px)`}}>
						<Chip size={34}>{w}</Chip>
					</div>
				))}
			</div>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 720, display: 'flex', justifyContent: 'center', opacity: cta, transform: `translateY(${(1 - cta) * 40}px)`}}>
				<Panel style={{display: 'flex', alignItems: 'center', gap: 26, padding: '20px 30px', background: 'rgba(12,9,5,0.92)'}}>
					<BrandIcon icon="whatsapp" size={80} />
					<div>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.muted, letterSpacing: 2}}>JOIN THE MTG TRIBE</div>
						<div style={{fontFamily: DISPLAY, fontSize: 84, lineHeight: 1, ...GOLD_TEXT}}>mtgtribe.com/group</div>
					</div>
				</Panel>
			</div>
			<AbsoluteFill style={{top: 300, bottom: 900, height: 'auto', justifyContent: 'center', alignItems: 'center', opacity: share, padding: '0 60px'}}>
				<div style={{fontSize: 110}}>🔁</div>
				<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.08, color: COLORS.text, textAlign: 'center', marginTop: 10}}>
					SEND THIS TO THE FRIEND WHO KEEPS <span style={GOLD_TEXT}>ALL THEIR SAVINGS IN ONE PLACE</span>
				</div>
			</AbsoluteFill>
			<Cues list={[[1.8, 'air', 0.35], [12.3, 'thud', 0.4], [15.8, 'air', 0.3]]} />
		</AbsoluteFill>
	);
};

// S12: the end card (2D, readable) over the living 3D studio
export const S12Outro3D: React.FC = () => {
	return (
		<AbsoluteFill>
			<Canvas3D>
				<GoldWorld dim={0.7} />
				<Dust count={90} />
				<Cam keys={[[0, [0, 2.4, 9.0], [0, 1.8, -2]], [28.5, [0.8, 2.2, 7.6], [0, 1.8, -2]]]} />
			</Canvas3D>
			<AbsoluteFill style={{background: 'rgba(5,4,3,0.35)'}} />
			<S12Outro />
		</AbsoluteFill>
	);
};


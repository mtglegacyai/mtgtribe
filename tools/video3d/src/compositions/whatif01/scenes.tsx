import {geoMercator, geoPath} from 'd3-geo';
import React, {useMemo} from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';
import {feature} from 'topojson-client';
import type {GeometryCollection, Topology} from 'topojson-specification';
import countries50m from 'world-atlas/countries-50m.json';
import {BRAND, COLORS} from '../../brand';
import {PhotoCard} from '../../components/PhotoCard';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {BrandIcon, Chip, clamp, Coin, Cues, ease, fadeOut, Flip, GOLD_TEXT, LeoClip, Loaf, Note, Panel, Stage, usePop, useT, useV} from './ui';

// Video 01 v2: both orientations (16:9 and 9:16), 3D entrances, camera drift, sound cues, 7 Leo moments.
// Times are seconds inside each section, from the narration's word timings (HeyGen, 7 Nov 2026).

const rand = (n: number) => `R${Math.round(n).toLocaleString('en-US')}`;
// Leo windows: portrait window on the right in 16:9; tall window (face and full print above the captions) or a
// face window under a panel in 9:16.
const LEO_H: React.CSSProperties = {right: 110, top: 115, width: 440, height: 770};
const LEO_V_TALL: React.CSSProperties = {left: 160, top: 320, width: 760, height: 1330}; // print ends about y 1250
const LEO_V_FACE: React.CSSProperties = {left: 140, top: 730, width: 800, height: 540}; // with FACE focus
const FACE = '50% 3%';
const TAB_V = 290; // a label sitting on the top edge of the tall window, under the brand bar

// S01 HOOK: "today ten rand ... tomorrow twenty ... forty ... in one month more than ten billion rand"
export const S01Hook: React.FC = () => {
	const t = useT();
	const v = useV();
	const days = t < 5.3 ? 0 : t < 7.1 ? 1 : t < 8.0 ? 2 : Math.min(30, 2 + Math.floor(28 * Easing.in(Easing.cubic)(Math.min(1, (t - 8.0) / 3.9))));
	const done = days === 30;
	const slide = ease(t, 8.2, 0.6);
	const glow = ease(t, 11.9, 0.4);
	const pulse = (t > 5.3 && t < 5.6) || (t > 7.1 && t < 7.4) ? 1 : 0;
	return (
		<AbsoluteFill>
			<Cues list={[[0.1, 'whoosh', 0.25], [2.6, 'pop', 0.22], [5.33, 'tick', 0.55], [7.13, 'tick', 0.55], [8.2, 'counter', 0.28], [9.7, 'counter', 0.3], [8.3, 'swish', 0.22], [11.9, 'stinger', 0.38]]} />
			<Stage style={v ? {justifyContent: 'flex-start'} : {transform: `translateX(${-420 * slide}px)`}}>
				<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: v ? 18 : 22, transform: v ? `scale(${interpolate(slide, [0, 1], [1, 0.68])})` : undefined, transformOrigin: 'top center'}}>
					<Flip at={0.1}><Chip size={v ? 40 : 36}>IMAGINE THIS</Chip></Flip>
					<Loaf size={v ? 380 : 300} pulse={pulse} />
					<Flip at={0.4}>
						<Panel style={{textAlign: 'center', width: v ? 960 : 900}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: v ? 42 : 38, color: COLORS.muted, letterSpacing: 3}}>
								{days === 0 ? 'TODAY' : days === 30 ? '30 DAYS LATER' : `+${days} DAY${days > 1 ? 'S' : ''}`}
							</div>
							<div style={{fontFamily: DISPLAY, fontSize: v ? 126 : interpolate(slide, [0, 1], [140, 112]), lineHeight: 1.1, marginTop: 4, ...GOLD_TEXT, filter: `drop-shadow(0 0 ${glow * 26}px rgba(255,217,142,${0.6 * glow}))`}}>{rand(10 * 2 ** days)}</div>
							<div style={{marginTop: 14, height: 14, borderRadius: 7, background: 'rgba(255,255,255,0.08)', overflow: 'hidden'}}>
								<div style={{width: `${(days / 30) * 100}%`, height: '100%', background: `linear-gradient(90deg, ${COLORS.gold}, ${COLORS.goldHi})`}} />
							</div>
							<div style={{marginTop: 14, fontFamily: BODY, fontWeight: 700, fontSize: v ? 38 : 34, color: COLORS.text, opacity: done ? 1 : 0.65}}>One loaf of bread, if prices double every day</div>
						</Panel>
					</Flip>
				</div>
			</Stage>
			<LeoClip clip="V1" from={8.3} seconds={5.0} style={v ? LEO_V_FACE : LEO_H} focus={v ? `50% ${interpolate(t, [8.3, 13.3], [4, 22], clamp)}%` : undefined} /> {/* V1's camera pushes in: follow his face */}
		</AbsoluteFill>
	);
};

// S02 GREETING: MTG's circle photo, large, his name beside or below it
export const S02Greeting: React.FC = () => {
	const t = useT();
	const v = useV();
	const photo = usePop(0.1, 18);
	const name = usePop(1.4);
	return (
		<Stage>
			<Cues list={[[0.1, 'shimmer', 0.28], [1.4, 'swish', 0.2], [6.1, 'pop', 0.25]]} />
			<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: 'center', gap: v ? 40 : 80, textAlign: v ? 'center' : 'left'}}>
				<div style={{opacity: photo, transform: `scale(${interpolate(photo, [0, 1], [0.85, 1])}) rotateY(${interpolate(photo, [0, 1], [-25, 0])}deg)`}}>
					<PhotoCard size={v ? 560 : 560} />
				</div>
				<div style={{width: v ? 960 : 860}}>
					<div style={{fontFamily: DISPLAY, fontSize: v ? 170 : 200, lineHeight: 1, ...GOLD_TEXT, opacity: name, transform: `translateY(${(1 - name) * 30}px)`}}>{BRAND.name}</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 60 : 64, color: COLORS.text, marginTop: 8, opacity: ease(t, 2.1)}}>{BRAND.title}</div>
					<div style={{marginTop: 30}}><Flip at={6.1}><Chip size={v ? 34 : 30}>WHEN MONEY STOPS KEEPING ITS PROMISE</Chip></Flip></div>
				</div>
			</div>
		</Stage>
	);
};

// S03 SETUP: "It happened. In 2008. Right next door to South Africa, in Zimbabwe." then the guess
const REGION = ['710', '716', '072', '508', '516', '894', '426', '748'];
const NAMES: Record<string, string> = {'710': 'SOUTH AFRICA', '716': 'ZIMBABWE'};
export const S03Setup: React.FC = () => {
	const t = useT();
	const v = useV();
	const W = v ? 980 : 1100;
	const H = v ? 760 : 820;
	const shapes = useMemo(() => {
		const topo = countries50m as unknown as Topology<{countries: GeometryCollection<{name: string}>}>;
		const all = feature(topo, topo.objects.countries);
		const feats = all.features.filter((f) => REGION.includes(String(f.id)));
		const proj = geoMercator().fitExtent([[40, 30], [W - 40, H - 30]], {type: 'FeatureCollection', features: feats});
		const path = geoPath(proj);
		return feats.map((f) => ({id: String(f.id), d: path(f) ?? '', c: path.centroid(f)}));
	}, [W, H]);
	const sa = ease(t, 5.7, 0.5);
	const zw = ease(t, 7.6, 0.5);
	const zoom = interpolate(t, [7.6, 9.4], [1, 1.35], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const tilt = interpolate(t, [5.6, 7.6, 15.5], [38, 24, 14], clamp); // the map lies in 3D, then lifts toward us
	const zwc = shapes.find((s) => s.id === '716')?.c ?? [W / 2, H / 3];
	const guess = ease(t, 16.2, 0.45);
	return (
		<AbsoluteFill>
			<Cues list={[[1.6, 'whoosh', 0.2], [4.5, 'hit', 0.4], [5.6, 'swish', 0.22], [5.75, 'pop', 0.25], [7.65, 'ding', 0.3], [10.8, 'pop', 0.22], [15.6, 'riser', 0.3], [16.2, 'impact', 0.3], [21.9, 'pop', 0.25]]} />
			<Stage style={{opacity: 1 - guess * 0.85}}>
				<div style={{position: 'absolute', left: v ? 0 : 40, top: v ? 0 : 60, width: v ? '100%' : 760, textAlign: v ? 'center' : 'left', opacity: fadeOut(t, 16.0), zIndex: 2}}>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 50 : 58, color: COLORS.text, opacity: ease(t, 1.6)}}>This is not science fiction.</div>
					<div style={{fontFamily: DISPLAY, fontSize: v ? 150 : 230, lineHeight: 1, marginTop: 6, ...GOLD_TEXT, opacity: ease(t, 4.4), transform: `scale(${interpolate(usePop(4.4, 11), [0, 1], [1.6, 1])})`, transformOrigin: v ? 'center' : 'left center'}}>2008</div>
					<div style={{marginTop: 24}}><Flip at={10.8}><Chip size={v ? 32 : 32}>ONE LESSON THAT STILL PROTECTS PEOPLE</Chip></Flip></div>
				</div>
				<div style={{position: 'absolute', right: v ? 0 : 0, top: v ? 260 : -20, perspective: 1600, opacity: ease(t, 5.6, 0.5)}}>
					<svg width={W} height={H} style={{transform: `rotateX(${tilt}deg)`, transformOrigin: 'center 70%', overflow: 'visible'}}>
						<g transform={`translate(${zwc[0]} ${zwc[1]}) scale(${zoom}) translate(${-zwc[0]} ${-zwc[1]})`}>
							{shapes.map((s) => {
								const isZ = s.id === '716';
								const isSA = s.id === '710';
								const fill = isZ ? `rgba(255,217,142,${0.15 + 0.75 * zw})` : isSA ? `rgba(242,173,60,${0.12 + 0.45 * sa})` : 'rgba(255,255,255,0.06)';
								return <path key={s.id} d={s.d} fill={fill} stroke={isZ || isSA ? COLORS.goldHi : 'rgba(255,255,255,0.25)'} strokeWidth={isZ ? 3 : 1.4} style={{filter: isZ ? `drop-shadow(0 0 ${14 * zw}px rgba(255,217,142,0.8))` : undefined}} />;
							})}
							{shapes.filter((s) => NAMES[s.id]).map((s) => (
								<text key={s.id} x={s.c[0]} y={s.c[1]} textAnchor="middle" fontFamily={MONO} fontWeight={700} fontSize={(s.id === '716' ? 36 : 34) / zoom} fill={s.id === '716' ? '#1a1206' : COLORS.text} opacity={s.id === '716' ? zw : sa}>
									{NAMES[s.id]}
								</text>
							))}
						</g>
					</svg>
				</div>
			</Stage>
			<Stage style={{opacity: guess}}>
				<Flip at={16.2}>
					<Panel style={{textAlign: 'center', padding: v ? '40px 30px' : '44px 70px', background: 'rgba(12,9,5,0.9)'}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: v ? 34 : 38, color: COLORS.muted, letterSpacing: 3}}>BEFORE I SHOW YOU THE BIGGEST BANKNOTE</div>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 128 : 140, lineHeight: 1.1, marginTop: 10, ...GOLD_TEXT}}>HOW MANY ZEROS?</div>
						<div style={{marginTop: 20, opacity: ease(t, 21.9)}}><Chip size={v ? 40 : 40}>COMMENT YOUR GUESS 💬</Chip></div>
					</Panel>
				</Flip>
			</Stage>
		</AbsoluteFill>
	);
};

// S04 BEAT 1: Hanke and Kwok, 24.7 hours, then the pay bars Friday to Friday
const DAYS = ['FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI'];
const PCTS = ['100%', '50%', '25%', '12.5%', '6.3%', '3.1%', '1.6%', '0.8%'];
const BAR_AT = [13.2, 14.0, 14.4, 14.8, 15.2, 15.6, 16.0, 16.7];
export const S04Doubling: React.FC = () => {
	const t = useT();
	const v = useV();
	const part1 = fadeOut(t, 11.5);
	const sweep = interpolate(t, [8.4, 9.9], [0, 360], clamp);
	const under = usePop(17.7, 12);
	const barW = v ? 92 : 92;
	const maxH = v ? 470 : 470;
	return (
		<AbsoluteFill>
			<Cues list={[[0.3, 'whoosh', 0.2], [2.2, 'pop', 0.22], [7.4, 'clock', 0.22], [8.4, 'impact', 0.32], [12.0, 'swish', 0.22], ...BAR_AT.map((a, i) => [a, 'blip', 0.16 + i * 0.01] as [number, string, number]), [17.7, 'stinger', 0.34], [20.4, 'pop', 0.22]]} />
			<Stage style={{opacity: part1}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: 'center', gap: v ? 40 : 70, textAlign: v ? 'center' : 'left'}}>
					<Flip at={0.3} from="y">
						<svg width={v ? 340 : 360} height={v ? 340 : 360} viewBox="0 0 200 200">
							<circle cx="100" cy="100" r="92" fill="rgba(255,255,255,0.04)" stroke={COLORS.gold} strokeWidth="5" />
							{Array.from({length: 12}, (_, i) => <line key={i} x1="100" y1="16" x2="100" y2="28" stroke={COLORS.goldHi} strokeWidth="4" transform={`rotate(${i * 30} 100 100)`} />)}
							<line x1="100" y1="100" x2="100" y2="34" stroke={COLORS.goldHi} strokeWidth="6" strokeLinecap="round" transform={`rotate(${sweep} 100 100)`} />
							<circle cx="100" cy="100" r="7" fill={COLORS.goldHi} />
						</svg>
					</Flip>
					<div style={{width: v ? 980 : 980}}>
						<Flip at={2.1}><div style={{fontFamily: MONO, fontWeight: 700, fontSize: v ? 32 : 34, color: COLORS.muted, letterSpacing: 2}}>ECONOMISTS STEVE HANKE AND ALEX KWOK ▪ NOVEMBER 2008</div></Flip>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 62 : 70, color: COLORS.text, marginTop: 18, opacity: ease(t, 6.0)}}>Prices doubled about every</div>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 170 : 190, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, 8.4), transform: `scale(${interpolate(usePop(8.4, 12), [0, 1], [1.3, 1])})`, transformOrigin: v ? 'center' : 'left center'}}>24.7 HOURS</div>
					</div>
				</div>
			</Stage>
			<Stage style={{opacity: ease(t, 12.0)}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: 'center', gap: v ? 30 : 60}}>
					<Flip at={12.0}>
						<Panel style={{paddingBottom: 20}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: v ? 34 : 34, color: COLORS.goldHi, letterSpacing: 2, marginBottom: 14}}>YOUR PAY, FRIDAY TO FRIDAY</div>
							<div style={{display: 'flex', alignItems: 'flex-end', gap: v ? 14 : 22, height: maxH + 70}}>
								{DAYS.map((d, i) => {
									const g = ease(t, BAR_AT[i], 0.3);
									const last = i === DAYS.length - 1;
									return (
										<div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: barW}}>
											<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, color: last ? COLORS.goldHi : COLORS.text, opacity: g, marginBottom: 6}}>{PCTS[i]}</div>
											<div style={{width: barW, height: Math.max(4, maxH * 0.5 ** i * g), borderRadius: 12, background: last ? 'linear-gradient(180deg, #ffb35c, #e0602f)' : `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold})`, boxShadow: last ? `0 0 ${30 * under}px rgba(255,140,60,0.7)` : '0 10px 30px rgba(0,0,0,0.35)'}} />
											<div style={{fontFamily: MONO, fontSize: 30, color: COLORS.muted, marginTop: 10}}>{d}</div>
										</div>
									);
								})}
							</div>
						</Panel>
					</Flip>
					<div style={{width: v ? 960 : 680, textAlign: v ? 'center' : 'left'}}>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 130 : 150, lineHeight: 1, ...GOLD_TEXT, transform: `scale(${under})`, transformOrigin: v ? 'center' : 'left center'}}>UNDER 1%</div>
						<div style={{fontFamily: BODY, fontWeight: 700, fontSize: v ? 36 : 38, color: COLORS.text, marginTop: 12, opacity: ease(t, 18.3)}}>of what your pay bought a week before</div>
						<div style={{fontFamily: BODY, fontSize: 28, color: COLORS.muted, marginTop: 10, opacity: ease(t, 18.3)}}>Simplified: halves every day</div>
						<div style={{marginTop: 24}}><Flip at={20.4}><Chip size={34}>SO HOW DOES MONEY MELT?</Chip></Flip></div>
					</div>
				</div>
			</Stage>
		</AbsoluteFill>
	);
};

// S05 BEAT 2: Leo thinks, then more money + fewer goods = higher prices (the auction)
const GOODS = ['🌽', '🍞', '🥛', '🧴', '👟', '🧱', '🍅', '🛢️'];
export const S05Why: React.FC = () => {
	const t = useT();
	const v = useV();
	const notes = Math.round(interpolate(t, [4.2, 7.8, 11.8, 13.5, 16.4, 21], [2, 8, 8, 16, 16, v ? 24 : 30], clamp));
	const goods = Math.round(interpolate(t, [4.2, 7.8, 18.9, 21], [8, 6, 6, 2], clamp));
	const price = t < 13.9 ? 10 : 10 * 2 ** Math.min(6, Math.floor((t - 13.9) / 1.0) + 1);
	const main = ease(t, 4.0, 0.4);
	const priceSteps = [13.9, 14.9, 15.9, 16.9, 17.9, 18.9];
	return (
		<AbsoluteFill>
			<Cues list={[[0.0, 'swish', 0.22], [4.1, 'whoosh', 0.22], [5.0, 'paper', 0.25], [11.85, 'coin', 0.3], [12.4, 'paper', 0.25], ...priceSteps.map((a) => [a, 'tick', 0.4] as [number, string, number]), [14.5, 'pop', 0.25], [16.4, 'paper', 0.25], [18.9, 'glitch', 0.18]]} />
			<LeoClip clip="V5" from={0} seconds={4.0} style={v ? LEO_V_TALL : LEO_H} />
			{v ? null : (
				<Stage style={{opacity: fadeOut(t, 3.8), justifyContent: 'center', alignItems: 'flex-start', paddingLeft: 40}}>
					<Flip at={0.3}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 34, color: COLORS.muted, letterSpacing: 3}}>WHY DID IT HAPPEN?</div>
						<div style={{fontFamily: DISPLAY, fontSize: 120, lineHeight: 1.05, color: COLORS.text, marginTop: 10}}>CAUSES ARE<br />DEBATED.</div>
						<div style={{fontFamily: DISPLAY, fontSize: 120, lineHeight: 1.05, ...GOLD_TEXT, opacity: ease(t, 2.0)}}>ONE IS CLEAR:</div>
					</Flip>
				</Stage>
			)}
			{v ? (
				<div style={{position: 'absolute', top: TAB_V, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, 0.3), fadeOut(t, 3.8))}}>
					<Chip size={32}>CAUSES ARE DEBATED. ONE IS CLEAR:</Chip>
				</div>
			) : null}
			<Stage style={{opacity: main}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: v ? 'center' : 'flex-end', gap: v ? 22 : 80}}>
					<Flip at={4.1}>
						<Panel style={{width: v ? 900 : 480, textAlign: 'center', padding: v ? '18px 24px' : '26px 32px'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 32, color: COLORS.goldHi, letterSpacing: 2}}>MONEY PRINTED</div>
							<div style={{display: 'flex', flexWrap: 'wrap-reverse', gap: 6, justifyContent: 'center', marginTop: 12, height: v ? 200 : 360, alignContent: 'flex-start', overflow: 'hidden'}}>
								{Array.from({length: notes}, (_, i) => <Note key={i} width={v ? 104 : 124} />)}
							</div>
						</Panel>
					</Flip>
					<div style={{display: 'flex', flexDirection: v ? 'row' : 'column', alignItems: 'center', gap: v ? 30 : 10, opacity: ease(t, 8.5)}}>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 110 : 110, ...GOLD_TEXT, transform: `scale(${t > 13.9 && (t - 13.9) % 1 < 0.15 ? 1.08 : 1})`, minWidth: v ? 300 : undefined, textAlign: 'center'}}>{rand(price)}</div>
						<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
							<Loaf size={v ? 190 : 270} />
							<div style={{fontFamily: MONO, fontSize: 28, color: COLORS.muted}}>ONE LOAF</div>
						</div>
					</div>
					<Flip at={4.4}>
						<Panel style={{width: v ? 900 : 480, textAlign: 'center', padding: v ? '18px 24px' : '26px 32px'}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 32, color: COLORS.goldHi, letterSpacing: 2}}>GOODS PRODUCED</div>
							<div style={{display: 'flex', flexWrap: 'wrap', gap: 14, justifyContent: 'center', marginTop: 16, height: v ? 90 : 330, alignContent: 'flex-start'}}>
								{GOODS.map((g, i) => <div key={i} style={{fontSize: v ? 68 : 80, opacity: i < goods ? 1 : 0.08, filter: i < goods ? 'none' : 'grayscale(1)', transform: `scale(${i < goods ? 1 : 0.7})`}}>{g}</div>)}
							</div>
						</Panel>
					</Flip>
					{v ? <Equation t={t} v /> : null}
				</div>
			</Stage>
			{v ? null : <div style={{position: 'absolute', bottom: 215, width: '100%'}}><Equation t={t} v={false} /></div>}
		</AbsoluteFill>
	);
};

const Equation: React.FC<{t: number; v: boolean}> = ({t, v}) => (
	<div style={{textAlign: 'center', opacity: ease(t, 14.5)}}>
		<Chip size={v ? 30 : 36}>MORE MONEY + FEWER GOODS = HIGHER PRICES</Chip>
		<div style={{fontFamily: BODY, fontSize: 26, color: COLORS.muted, marginTop: 6}}>(simplified)</div>
	</div>
);

// S06 BEAT 3: how people coped, respect, then Leo asks "what would you buy first?"
const COPE = [
	{at: 3.3, icon: '⏱️', title: 'SPEND IT FAST', sub: 'Waiting one day cost them'},
	{at: 8.6, icon: '🌽 ⇄ 👟', title: 'SWAP GOODS', sub: 'A bag of maize for a pair of shoes'},
	{at: 13.7, icon: '$  R', title: 'US DOLLARS AND RAND', sub: 'Money people still trusted'},
];
export const S06Coping: React.FC = () => {
	const t = useT();
	const v = useV();
	const respect = ease(t, 17.75, 0.6);
	return (
		<AbsoluteFill>
			<Cues list={[[3.3, 'swish', 0.25], [8.6, 'swish', 0.25], [9.2, 'pop', 0.2], [13.7, 'swish', 0.25], [14.1, 'coin', 0.3], [22.1, 'whoosh', 0.2], [23.4, 'pop', 0.28]]} />
			<Stage style={{opacity: fadeOut(t, 21.9)}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', gap: v ? 22 : 40, opacity: 1 - respect}}>
					{COPE.map((c) => (
						<Flip key={c.title} at={c.at}>
							<Panel style={{width: v ? 900 : 520, textAlign: 'center', padding: v ? '20px 30px' : '30px 38px', display: v ? 'flex' : 'block', alignItems: 'center', gap: 26}}>
								<div style={{fontSize: v ? 80 : 104, fontFamily: DISPLAY, ...(c.icon.includes('$') ? GOLD_TEXT : {})}}>{c.icon}</div>
								<div style={{textAlign: v ? 'left' : 'center'}}>
									<div style={{fontFamily: DISPLAY, fontSize: v ? 56 : 66, marginTop: 6, ...GOLD_TEXT}}>{c.title}</div>
									<div style={{fontFamily: BODY, fontWeight: 700, fontSize: v ? 32 : 34, color: COLORS.text, marginTop: 6}}>{c.sub}</div>
								</div>
							</Panel>
						</Flip>
					))}
				</div>
				<div style={{position: 'absolute', fontFamily: BODY, fontWeight: 800, fontSize: v ? 64 : 72, color: COLORS.champagne, opacity: respect, textShadow: '0 0 30px rgba(242,173,60,0.4)', textAlign: 'center', width: '100%'}}>
					Real families lived through this.
				</div>
			</Stage>
			{v ? <LeoClip clip="V2" from={22.1} seconds={6.6} style={LEO_V_TALL} /> : <LeoClip clip="L2" from={22.1} seconds={6.6} full />}
			<div style={{position: 'absolute', top: v ? TAB_V : 110, width: '100%', textAlign: 'center', opacity: ease(t, 23.4)}}>
				<Chip size={v ? 38 : 46} style={{background: 'rgba(5,4,3,0.85)'}}>WHAT WOULD YOU BUY FIRST? 💬</Chip>
			</div>
		</AbsoluteFill>
	);
};

// S07 BEAT 4: the 100 trillion note and the 14 zeros, Leo amazed
export const S07Zeros: React.FC = () => {
	const t = useT();
	const v = useV();
	const zeros = t < 10.6 ? 0 : Math.min(14, Math.floor((t - 10.6) / 0.13) + 1);
	const grouped = ('1' + '0'.repeat(zeros)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	const done = zeros === 14;
	const reveal = usePop(12.5, 13);
	return (
		<AbsoluteFill>
			<Cues list={[[0.3, 'whoosh', 0.2], [4.3, 'paper', 0.3], [8.1, 'pop', 0.22], [9.4, 'swish', 0.2], [10.65, 'counter', 0.32], [12.5, 'shimmer', 0.36], [13.0, 'hit', 0.3]]} />
			<Stage style={v ? {justifyContent: 'flex-start'} : {justifyContent: 'center', alignItems: 'flex-start', paddingLeft: 20}}>
				<div style={{width: v ? 980 : 1150, textAlign: v ? 'center' : 'left', transform: v ? `scale(${interpolate(ease(t, 9.2, 0.6), [0, 1], [1, 0.74])})` : undefined, transformOrigin: 'top center'}}>
					<Flip at={0.3}><Chip size={v ? 30 : 32}>JANUARY 2009 ▪ RESERVE BANK OF ZIMBABWE</Chip></Flip>
					<div style={{display: 'flex', alignItems: 'center', justifyContent: v ? 'center' : 'flex-start', gap: 30, marginTop: 26, opacity: ease(t, 4.3)}}>
						<div style={{transform: `perspective(900px) rotateY(${interpolate(usePop(4.3, 14), [0, 1], [70, -8])}deg)`}}><Note width={v ? 300 : 360} /></div>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 84 : 100, lineHeight: 1, ...GOLD_TEXT, textAlign: 'left'}}>100 TRILLION<br />DOLLARS</div>
					</div>
					<Flip at={8.0}>
						<Panel style={{marginTop: 30}}>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 32, color: COLORS.muted, letterSpacing: 3}}>HOW CLOSE WAS YOUR GUESS?</div>
							<div style={{fontFamily: DISPLAY, fontSize: v ? 84 : 110, lineHeight: 1.15, ...GOLD_TEXT}}>Z${grouped}</div>
							<div style={{display: 'flex', gap: 10, marginTop: 12, justifyContent: v ? 'center' : 'flex-start'}}>
								{Array.from({length: 14}, (_, i) => <div key={i} style={{width: v ? 48 : 52, height: 12, borderRadius: 6, background: i < zeros ? COLORS.goldHi : 'rgba(255,255,255,0.1)'}} />)}
							</div>
						</Panel>
					</Flip>
					<div style={{display: 'flex', alignItems: 'center', justifyContent: v ? 'center' : 'flex-start', gap: 30, marginTop: 22}}>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 100 : 124, opacity: done ? 1 : 0, transform: `scale(${done ? reveal : 0.8})`, transformOrigin: 'left center', ...GOLD_TEXT}}>14 ZEROS</div>
						<div style={{opacity: ease(t, 13.0)}}><Chip size={32}>AND STILL, NOT ENOUGH</Chip></div>
					</div>
				</div>
			</Stage>
			<LeoClip clip="V3" from={9.4} seconds={6.17} style={v ? LEO_V_FACE : LEO_H} focus={v ? FACE : undefined} />
		</AbsoluteFill>
	);
};

// S08 BEAT 5: money cheaper than paper (the 2009 poster campaign), Leo laughs, Cannes Lions, abandoned April 2009
export const S08Posters: React.FC = () => {
	const t = useT();
	const v = useV();
	const wall = Math.round(interpolate(t, [6.6, 10.0], [0, v ? 12 : 24], clamp));
	const quote = Math.min(ease(t, 13.0), fadeOut(t, 23.4));
	const trophy = usePop(17.6, 13);
	const abandon = ease(t, 24.9, 0.5);
	const intro = fadeOut(t, 12.9);
	return (
		<AbsoluteFill>
			<Cues list={[[0.4, 'whoosh', 0.2], [4.4, 'pop', 0.22], [6.7, 'paper', 0.28], [8.0, 'paper', 0.28], [9.3, 'paper', 0.28], [10.3, 'swish', 0.22], [13.0, 'ding', 0.3], [16.9, 'swish', 0.22], [17.6, 'shimmer', 0.32], [24.9, 'stamp', 0.45], [29.2, 'coin', 0.3], [29.5, 'coin', 0.25], [31.6, 'riser', 0.26], [32.1, 'hit', 0.32]]} />
			<Stage style={{opacity: intro, justifyContent: v ? 'flex-start' : 'center'}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: v ? 'center' : 'flex-start', gap: v ? 26 : 60, width: '100%'}}>
					<div style={{width: v ? '100%' : 820, textAlign: v ? 'center' : 'left'}}>
						<Flip at={0.4}><Chip size={34}>JOHANNESBURG ▪ MARCH 2009</Chip></Flip>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 52 : 60, color: COLORS.text, marginTop: 20, opacity: ease(t, 4.3)}}>An ad agency printed posters straight onto real banknotes</div>
						<div style={{display: 'flex', gap: 24, alignItems: 'center', justifyContent: v ? 'center' : 'flex-start', marginTop: 30}}>
							<Flip at={10.3} from="y"><Panel style={{padding: '16px 24px', textAlign: 'center'}}><div style={{fontFamily: MONO, fontSize: 28, color: COLORS.goldHi}}>PRINT ON MONEY</div><div style={{fontFamily: DISPLAY, fontSize: 68, ...GOLD_TEXT}}>CHEAPER</div></Panel></Flip>
							<div style={{fontFamily: DISPLAY, fontSize: 64, color: COLORS.muted, opacity: ease(t, 10.6)}}>THAN</div>
							<Flip at={10.8} from="y"><Panel style={{padding: '16px 24px', textAlign: 'center'}}><div style={{fontFamily: MONO, fontSize: 28, color: COLORS.muted}}>BUYING</div><div style={{fontFamily: DISPLAY, fontSize: 68, color: COLORS.text}}>PAPER</div></Panel></Flip>
						</div>
					</div>
					<div style={{display: 'flex', flexWrap: 'wrap', gap: 8, width: v ? 900 : 760, justifyContent: 'center', perspective: 1400}}>
						{Array.from({length: wall}, (_, i) => (
							<div key={i} style={{transform: `rotateX(${interpolate(t, [6.6 + i * 0.14, 6.9 + i * 0.14], [80, 0], clamp)}deg)`}}><Note width={v ? 210 : 180} /></div>
						))}
					</div>
				</div>
			</Stage>
			<Stage style={{opacity: quote, justifyContent: v ? 'flex-start' : 'center'}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 40, width: '100%', justifyContent: v ? 'center' : 'flex-start'}}>
					<Panel style={{width: v ? 960 : 1180, textAlign: 'center', padding: v ? '30px 30px' : '44px 56px', background: 'rgba(12,9,5,0.9)'}}>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 76 : 92, lineHeight: 1.1, ...GOLD_TEXT}}>"It's cheaper to print this on money than paper."</div>
						<div style={{fontFamily: BODY, fontSize: 28, color: COLORS.muted, marginTop: 16}}>Poster line from the 2009 campaign by TBWA\Hunt\Lascaris, Johannesburg</div>
						<div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 20, marginTop: 26, opacity: trophy, transform: `scale(${trophy}) rotateY(${interpolate(trophy, [0, 1], [90, 0])}deg)`}}>
							<svg width="90" height="90" viewBox="0 0 64 64">
								<path d="M18 6h28v10c0 10-6 18-14 18S18 26 18 16z" fill={COLORS.gold} />
								<path d="M18 10H8c0 9 5 14 11 15M46 10h10c0 9-5 14-11 15" stroke={COLORS.gold} strokeWidth="4" fill="none" />
								<rect x="28" y="34" width="8" height="12" fill={COLORS.gold} /><rect x="18" y="46" width="28" height="8" rx="2" fill={COLORS.goldHi} />
							</svg>
							<Chip size={v ? 26 : 34}>CANNES LIONS 2009 ▪ OUTDOOR GRAND PRIX</Chip>
						</div>
					</Panel>
				</div>
			</Stage>
			<LeoClip clip="V6" from={16.9} seconds={6.0} style={v ? LEO_V_FACE : LEO_H} focus={v ? FACE : undefined} />
			<Stage style={{opacity: Math.min(abandon, fadeOut(t, 31.9))}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: 'center', gap: v ? 50 : 70}}>
					<div style={{position: 'relative'}}>
						<Note width={v ? 640 : 560} grey={abandon} />
						<div style={{position: 'absolute', left: '50%', top: '50%', transform: `translate(-50%,-50%) rotate(-12deg) scale(${interpolate(abandon, [0, 1], [1.6, 1])})`, border: '6px solid #e0602f', color: '#ff8a4c', fontFamily: DISPLAY, fontSize: v ? 68 : 70, padding: '6px 26px', borderRadius: 12, background: 'rgba(5,4,3,0.65)', whiteSpace: 'nowrap'}}>ABANDONED ▪ APRIL 2009</div>
					</div>
					<div style={{display: 'flex', gap: 30}}>
						<Coin symbol="$" size={v ? 210 : 200} at={29.2} />
						<Coin symbol="R" size={v ? 210 : 200} at={29.5} />
					</div>
				</div>
			</Stage>
			<Stage style={{opacity: ease(t, 32.1, 0.3)}}>
				<div style={{fontFamily: DISPLAY, fontSize: v ? 128 : 150, lineHeight: 1.05, textAlign: 'center', color: COLORS.text, transform: `scale(${interpolate(usePop(32.1, 12), [0, 1], [0.7, 1])})`}}>
					HERE'S THE PART<br /><span style={GOLD_TEXT}>MOST PEOPLE MISS</span>
				</div>
			</Stage>
		</AbsoluteFill>
	);
};

// S09 BEAT 6: money is a promise plus trust; the voucher from a closed shop
export const S09Promise: React.FC = () => {
	const t = useT();
	const v = useV();
	const eq = Math.min(ease(t, 3.0), fadeOut(t, 6.4));
	const shutter = interpolate(t, [8.3, 9.2], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const gone = ease(t, 11.3, 1.2);
	return (
		<AbsoluteFill>
			<Cues list={[[0.9, 'hit', 0.3], [2.4, 'hit', 0.3], [3.0, 'shimmer', 0.3], [6.6, 'whoosh', 0.2], [7.1, 'pop', 0.2], [8.3, 'shutter', 0.42], [11.3, 'impact', 0.22], [13.4, 'pop', 0.25]]} />
			<Stage style={{opacity: Math.min(ease(t, 0.3), fadeOut(t, 2.9))}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', gap: v ? 60 : 120, alignItems: 'center'}}>
					{['📄 PAPER', '🪙 METAL'].map((w, i) => (
						<div key={w} style={{position: 'relative', fontFamily: DISPLAY, fontSize: v ? 120 : 130, color: COLORS.text, opacity: ease(t, 0.3 + i * 1.5)}}>
							{w}
							<div style={{position: 'absolute', left: -10, right: -10, top: '50%', height: 12, background: '#e0602f', transform: `rotate(-8deg) scaleX(${ease(t, 0.9 + i * 1.5)})`, borderRadius: 6}} />
						</div>
					))}
				</div>
			</Stage>
			<Stage style={{opacity: eq}}>
				<div style={{fontFamily: DISPLAY, fontSize: v ? 130 : 170, lineHeight: 1.05, textAlign: 'center', ...GOLD_TEXT, transform: `scale(${interpolate(usePop(3.0, 12), [0, 1], [0.7, 1])})`}}>MONEY = {v ? <br /> : null}PROMISE + TRUST</div>
			</Stage>
			<Stage style={{opacity: ease(t, 6.6)}}>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: 'center', gap: v ? 40 : 80}}>
					<Flip at={6.6} from="y">
						<div style={{position: 'relative', width: v ? 560 : 560, height: v ? 420 : 460, borderRadius: 18, background: 'linear-gradient(180deg, #3a2c18, #1a140b)', border: `2px solid ${COLORS.gold}`, overflow: 'hidden'}}>
							<div style={{position: 'absolute', top: 18, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 60, ...GOLD_TEXT}}>THE SHOP</div>
							<div style={{position: 'absolute', left: 60, right: 60, bottom: 0, top: 100, background: 'linear-gradient(180deg, rgba(255,217,142,0.35), rgba(255,217,142,0.08))'}} />
							<div style={{position: 'absolute', left: 60, right: 60, top: 100, height: `${shutter * 360}px`, background: 'repeating-linear-gradient(180deg, #6b6b6b 0 14px, #4a4a4a 14px 18px)'}} />
							<div style={{position: 'absolute', bottom: 24, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 34, color: '#ff8a4c', opacity: ease(t, 9.0)}}>CLOSED</div>
						</div>
					</Flip>
					<div style={{perspective: 1000}}>
						<div style={{width: v ? 560 : 500, height: v ? 280 : 270, borderRadius: 22, background: `linear-gradient(135deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`, filter: `grayscale(${gone}) brightness(${1 - gone * 0.35})`, boxShadow: `0 0 ${50 * (1 - gone)}px rgba(242,173,60,0.6)`, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', transform: `rotate(-4deg) rotateY(${interpolate(usePop(7.0, 14), [0, 1], [-80, 0])}deg)`}}>
							<div style={{fontFamily: DISPLAY, fontSize: 76, color: '#3a2508'}}>VOUCHER</div>
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 32, color: '#3a2508'}}>R500 AT THE SHOP</div>
						</div>
					</div>
				</div>
				<div style={{marginTop: 34}}><Flip at={13.4}><Chip size={40}>NO TRUST, NO MONEY</Chip></Flip></div>
			</Stage>
		</AbsoluteFill>
	);
};

// S10 PAYOFF: Leo makes the point, never all your trust in one kind of money, what stands behind it, knowledge
const KINDS = [
	{title: 'CASH', icon: '💵', behind: "A government's promise", at: 9.0},
	{title: 'STABLECOIN', icon: '🪙', behind: 'As strong as its company and reserves', at: 13.1},
	{title: 'BITCOIN', icon: '₿', behind: 'Big price swings, up and down', at: 17.05},
];
export const S10Lesson: React.FC = () => {
	const t = useT();
	const v = useV();
	const book = usePop(21.3, 13);
	const prompt = ease(t, 23.8);
	return (
		<AbsoluteFill>
			<Cues list={[[0.0, 'swish', 0.2], [3.2, 'swish', 0.22], [3.7, 'swish', 0.22], [4.2, 'swish', 0.22], [9.0, 'blip', 0.25], [13.1, 'blip', 0.25], [17.05, 'blip', 0.25], [21.3, 'ding', 0.32], [23.8, 'pop', 0.3]]} />
			<LeoClip clip="V7" from={0} seconds={3.3} style={v ? LEO_V_TALL : LEO_H} />
			{v ? (
				<div style={{position: 'absolute', top: TAB_V, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, 0.3), fadeOut(t, 3.1))}}>
					<Chip size={40}>THE LESSON</Chip>
				</div>
			) : (
				<Stage style={{opacity: fadeOut(t, 3.1), justifyContent: 'center', alignItems: 'flex-start', paddingLeft: 40}}>
					<Flip at={0.2}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 34, color: COLORS.muted, letterSpacing: 3}}>WHAT FAMILIES LEARNED</div>
						<div style={{fontFamily: DISPLAY, fontSize: 190, lineHeight: 1, ...GOLD_TEXT}}>THE LESSON</div>
					</Flip>
				</Stage>
			)}
			<Stage style={{opacity: Math.min(ease(t, 3.2), 1 - prompt)}}>
				<div style={{textAlign: 'center', marginBottom: v ? 20 : 26}}><Chip size={v ? 27 : 36}>NEVER PUT ALL YOUR TRUST IN ONE KIND OF MONEY</Chip></div>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', gap: v ? 16 : 40}}>
					{KINDS.map((k, i) => (
						<Flip key={k.title} at={3.2 + i * 0.5} from={v ? 'x' : 'y'}>
							<Panel style={{width: v ? 900 : 500, textAlign: v ? 'left' : 'center', padding: v ? '16px 28px' : '28px 34px', display: v ? 'flex' : 'block', alignItems: 'center', gap: 24}}>
								<div style={{fontSize: v ? 76 : 104, fontFamily: DISPLAY, ...(k.icon === '₿' ? GOLD_TEXT : {})}}>{k.icon}</div>
								<div>
									<div style={{fontFamily: DISPLAY, fontSize: v ? 56 : 68, ...GOLD_TEXT}}>{k.title}</div>
									<div style={{fontFamily: MONO, fontSize: 26, color: COLORS.muted, marginTop: 6, opacity: ease(t, 6.5)}}>WHAT STANDS BEHIND IT?</div>
									<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 34 : 36, color: COLORS.text, marginTop: 6, minHeight: v ? 0 : 90, opacity: ease(t, k.at)}}>{k.behind}</div>
								</div>
							</Panel>
						</Flip>
					))}
				</div>
				<div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 20, marginTop: v ? 20 : 30, opacity: book, transform: `scale(${book})`}}>
					<div style={{fontSize: v ? 70 : 84}}>📘</div>
					<div style={{fontFamily: DISPLAY, fontSize: v ? 66 : 90, ...GOLD_TEXT}}>YOUR PROTECTION = KNOWLEDGE</div>
				</div>
			</Stage>
			<Stage style={{opacity: prompt}}>
				<Flip at={23.8}>
					<Panel style={{textAlign: 'center', padding: v ? '40px 30px' : '44px 70px', background: 'rgba(12,9,5,0.92)'}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: v ? 34 : 38, color: COLORS.muted, letterSpacing: 3}}>FINISH THE SENTENCE IN THE COMMENTS</div>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 140 : 160, lineHeight: 1.1, marginTop: 10, ...GOLD_TEXT}}>MONEY IS ___ 💬</div>
					</Panel>
				</Flip>
			</Stage>
		</AbsoluteFill>
	);
};

// S11 BRIDGE AND CTA: the MTG TRIBE, mtgtribe.com/group, share it
export const S11Tribe: React.FC = () => {
	const t = useT();
	const v = useV();
	const cta = usePop(12.9, 14);
	const share = ease(t, 16.0);
	return (
		<AbsoluteFill>
			<Cues list={[[1.5, 'powerup', 0.28], [5.9, 'pop', 0.22], [7.8, 'pop', 0.22], [9.6, 'pop', 0.22], [12.9, 'impact', 0.3], [13.1, 'ding', 0.25], [16.0, 'swish', 0.25]]} />
			<Stage style={{opacity: Math.min(ease(t, 1.5), 1 - share), justifyContent: v ? 'flex-start' : 'center', paddingTop: v ? 40 : 0}}>
				<div style={{fontFamily: DISPLAY, fontSize: v ? 160 : 190, lineHeight: 1, ...GOLD_TEXT, transform: `scale(${interpolate(usePop(1.5, 12), [0, 1], [0.6, 1])})`}}>MTG TRIBE</div>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 50 : 54, color: COLORS.text, marginTop: 14, opacity: ease(t, 3.7)}}>A community of action takers</div>
				<div style={{display: 'flex', flexDirection: v ? 'column' : 'row', alignItems: 'center', gap: v ? 14 : 24, marginTop: 30}}>
					{([['LEARN HOW MONEY WORKS', 5.9], ['OLD AND NEW', 7.8], ['YOUR OWN DECISIONS', 9.6]] as Array<[string, number]>).map(([w, at]) => (
						<Flip key={w} at={at}><Chip size={v ? 36 : 34}>{w}</Chip></Flip>
					))}
				</div>
			</Stage>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: v ? 720 : 215, display: 'flex', justifyContent: 'center', opacity: cta, transform: `translateY(${(1 - cta) * 40}px) scale(${interpolate(cta, [0, 1], [0.9, 1])})`}}>
				<Panel style={{display: 'flex', alignItems: 'center', gap: 26, padding: v ? '20px 30px' : '22px 44px', background: 'rgba(12,9,5,0.92)'}}>
					<BrandIcon icon="whatsapp" size={v ? 80 : 90} />
					<div>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.muted, letterSpacing: 2}}>JOIN THE MTG TRIBE</div>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 84 : 100, lineHeight: 1, ...GOLD_TEXT}}>mtgtribe.com/group</div>
					</div>
				</Panel>
			</div>
			<Stage style={{opacity: share, justifyContent: 'flex-start', paddingTop: v ? 60 : 10}}>
				<Flip at={16.0}>
					<div style={{textAlign: 'center', width: v ? 960 : 1500}}>
						<div style={{fontSize: v ? 110 : 96}}>🔁</div>
						<div style={{fontFamily: DISPLAY, fontSize: v ? 96 : 92, lineHeight: 1.08, color: COLORS.text, marginTop: 10}}>SEND THIS TO THE FRIEND WHO KEEPS <span style={GOLD_TEXT}>ALL THEIR SAVINGS IN ONE PLACE</span></div>
					</div>
				</Flip>
			</Stage>
		</AbsoluteFill>
	);
};

// S12 OUTRO: MTG's end card (circle photo), like share comment, platforms, Leo waves, slogan
const PLATFORMS: Array<['whatsapp' | 'telegram' | 'tiktok' | 'youtube', string]> = [
	['whatsapp', 'mtgtribe.com/group'],
	['telegram', 't.me/mtgtribez'],
	['tiktok', '@joinmtgtribe'],
	['youtube', '@mtgtribe'],
];
export const S12Outro: React.FC = () => {
	const t = useT();
	const v = useV();
	const photo = usePop(0.1, 18);
	const slogan = usePop(22.0, 12);
	const leoIn = v ? Math.min(ease(t, 12.4, 0.3), fadeOut(t, 18.2)) : 0;
	return (
		<AbsoluteFill>
			<Cues list={[[0.1, 'shimmer', 0.28], [7.5, 'pop', 0.25], [7.9, 'pop', 0.25], [8.3, 'pop', 0.25], [9.6, 'swish', 0.2], [14.5, 'whoosh', 0.18], [22.0, 'impact', 0.3]]} />
			<Stage style={{justifyContent: v ? 'flex-start' : 'center', alignItems: v ? 'center' : 'flex-start', opacity: 1 - leoIn}}>
				<div style={{display: 'flex', flexDirection: 'column', alignItems: v ? 'center' : 'flex-start', gap: v ? 20 : 24, textAlign: v ? 'center' : 'left'}}>
					<div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', gap: v ? 30 : 40, textAlign: 'left'}}>
						<div style={{opacity: photo, transform: `scale(${interpolate(photo, [0, 1], [0.85, 1])})`}}><PhotoCard size={v ? 330 : 400} /></div>
						<div>
							<div style={{fontFamily: DISPLAY, fontSize: v ? 100 : 120, lineHeight: 1, ...GOLD_TEXT}}>{BRAND.name}</div>
							<div style={{fontFamily: BODY, fontWeight: 800, fontSize: v ? 40 : 46, color: COLORS.text}}>{BRAND.title}</div>
							<div style={{fontFamily: BODY, fontSize: v ? 28 : 30, color: COLORS.muted, marginTop: 8, opacity: ease(t, 0.3), maxWidth: v ? 520 : undefined}}>Education only. Not financial advice.</div>
						</div>
					</div>
					<div style={{display: 'flex', gap: 18}}>
						{['👍 LIKE', '🔁 SHARE', '💬 COMMENT'].map((w, i) => <Flip key={w} at={7.5 + i * 0.4}><Chip size={v ? 32 : 34}>{w}</Chip></Flip>)}
					</div>
					<div style={{display: 'grid', gridTemplateColumns: v ? '1fr' : '1fr 1fr', gap: v ? 12 : 14, width: v ? 760 : 1000}}>
						{PLATFORMS.map(([icon, label], i) => (
							<Flip key={icon} at={9.6 + i * 0.25} from="y">
								<Panel style={{display: 'flex', alignItems: 'center', gap: 18, padding: v ? '10px 26px' : '12px 22px'}}>
									<BrandIcon icon={icon} size={v ? 48 : 52} />
									<div style={{fontFamily: MONO, fontWeight: 700, fontSize: v ? 36 : 34, color: COLORS.text}}>{label}</div>
								</Panel>
							</Flip>
						))}
					</div>
				</div>
			</Stage>
			{v ? <LeoClip clip="V4" from={12.4} seconds={6.0} style={LEO_V_TALL} /> : <LeoClip clip="V4" from={14.5} seconds={6.0} style={LEO_H} />}
			<div style={{position: 'absolute', right: v ? 0 : 60, left: v ? 0 : undefined, bottom: v ? 720 : 215, width: v ? '100%' : 760, textAlign: 'center', opacity: slogan, transform: `scale(${slogan})`}}>
				<span style={{fontFamily: DISPLAY, fontSize: v ? 84 : 92, ...GOLD_TEXT}}>Let's Get This Crypto!</span>{' '}
				<span style={{fontFamily: DISPLAY, fontSize: v ? 84 : 92}}>💪</span>
			</div>
		</AbsoluteFill>
	);
};

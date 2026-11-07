import {geoMercator, geoPath} from 'd3-geo';
import React, {useMemo} from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';
import {feature} from 'topojson-client';
import type {GeometryCollection, Topology} from 'topojson-specification';
import countries50m from 'world-atlas/countries-50m.json';
import {BRAND, COLORS} from '../../brand';
import {PhotoCard} from '../../components/PhotoCard';
import {BODY, DISPLAY, MONO} from '../../fonts';
import {BrandIcon, Chip, clamp, ease, fadeOut, GOLD_TEXT, LeoClip, Loaf, Note, Panel, usePop, useT} from './ui';

// Times are seconds inside each section, read from the narration's word timings (HeyGen, 7 Nov 2026).
const rand = (n: number) => `R${Math.round(n).toLocaleString('en-US')}`;
const Center: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 150, ...style}}>{children}</AbsoluteFill>
);

// S01 HOOK: "today ten rand ... tomorrow twenty ... forty ... in one month more than ten billion rand"
export const S01Hook: React.FC = () => {
	const t = useT();
	const days = t < 5.3 ? 0 : t < 7.1 ? 1 : t < 8.0 ? 2 : Math.min(30, 2 + Math.floor(28 * Easing.in(Easing.cubic)(Math.min(1, (t - 8.0) / 3.9))));
	const done = days === 30;
	const slide = ease(t, 8.2, 0.7);
	const glow = ease(t, 11.9, 0.4);
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 150, transform: `translateX(${-450 * slide}px)`}}>
				<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 26, opacity: ease(t, 0.1)}}>
					<Chip>IMAGINE THIS</Chip>
					<Loaf size={300} pulse={t > 5.3 && t < 5.6 ? 1 : t > 7.1 && t < 7.4 ? 1 : 0} />
					<Panel style={{textAlign: 'center', width: 860}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 34, color: COLORS.muted, letterSpacing: 3}}>
							{days === 0 ? 'TODAY' : days === 30 ? '30 DAYS LATER' : `+${days} DAY${days > 1 ? 'S' : ''}`}
						</div>
						<div style={{fontFamily: DISPLAY, fontSize: interpolate(slide, [0, 1], [130, 108]), lineHeight: 1.1, marginTop: 4, ...GOLD_TEXT, filter: `drop-shadow(0 0 ${glow * 26}px rgba(255,217,142,${0.6 * glow}))`}}>{rand(10 * 2 ** days)}</div>
						<div style={{marginTop: 16, height: 12, borderRadius: 6, background: 'rgba(255,255,255,0.08)', overflow: 'hidden'}}>
							<div style={{width: `${(days / 30) * 100}%`, height: '100%', background: `linear-gradient(90deg, ${COLORS.gold}, ${COLORS.goldHi})`}} />
						</div>
						<div style={{marginTop: 14, fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.text, opacity: done ? 1 : 0.6}}>One loaf of bread, if prices double every day</div>
					</Panel>
				</div>
			</AbsoluteFill>
			<LeoClip clip="L1" from={8.3} seconds={5.3} style={{right: 90, top: 120, width: 760, height: 700}} />
		</AbsoluteFill>
	);
};

// S02 GREETING: MTG's circle photo, large, name on the right
export const S02Greeting: React.FC = () => {
	const t = useT();
	const photo = usePop(0.1, 18);
	const name = usePop(1.4);
	return (
		<Center>
			<div style={{display: 'flex', alignItems: 'center', gap: 80}}>
				<div style={{opacity: photo, transform: `scale(${interpolate(photo, [0, 1], [0.9, 1])})`}}>
					<PhotoCard size={560} />
				</div>
				<div style={{width: 820}}>
					<div style={{fontFamily: DISPLAY, fontSize: 190, lineHeight: 1, ...GOLD_TEXT, opacity: name, transform: `translateY(${(1 - name) * 30}px)`}}>{BRAND.name}</div>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 58, color: COLORS.text, marginTop: 10, opacity: ease(t, 2.1)}}>{BRAND.title}</div>
					<div style={{marginTop: 40, opacity: ease(t, 6.1)}}>
						<Chip size={30}>WHEN MONEY STOPS KEEPING ITS PROMISE</Chip>
					</div>
				</div>
			</div>
		</Center>
	);
};

// S03 SETUP: "It happened. In 2008. Right next door to South Africa, in Zimbabwe." then the guess
const REGION = ['710', '716', '072', '508', '516', '894', '426', '748'];
const NAMES: Record<string, string> = {'710': 'SOUTH AFRICA', '716': 'ZIMBABWE'};
export const S03Setup: React.FC = () => {
	const t = useT();
	const shapes = useMemo(() => {
		const topo = countries50m as unknown as Topology<{countries: GeometryCollection<{name: string}>}>;
		const all = feature(topo, topo.objects.countries);
		const feats = all.features.filter((f) => REGION.includes(String(f.id)));
		const proj = geoMercator().fitExtent([[60, 40], [1060, 820]], {type: 'FeatureCollection', features: feats});
		const path = geoPath(proj);
		return feats.map((f) => ({id: String(f.id), d: path(f) ?? '', c: path.centroid(f)}));
	}, []);
	const sa = ease(t, 5.7, 0.5);
	const zw = ease(t, 7.6, 0.5);
	const zoom = interpolate(t, [7.6, 9.2], [1, 1.35], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const zwc = shapes.find((s) => s.id === '716')?.c ?? [560, 300];
	const guess = ease(t, 16.2, 0.5);
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', left: 120, top: 150, opacity: Math.min(ease(t, 1.6), fadeOut(t, 16.0))}}>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 52, color: COLORS.text, opacity: ease(t, 1.6)}}>This is not science fiction.</div>
				<div style={{fontFamily: DISPLAY, fontSize: 210, lineHeight: 1, marginTop: 10, ...GOLD_TEXT, opacity: ease(t, 4.4)}}>2008</div>
				<div style={{marginTop: 30, opacity: ease(t, 10.8)}}>
					<Chip size={28}>ONE LESSON THAT STILL PROTECTS PEOPLE</Chip>
				</div>
			</div>
			<svg width={1120} height={860} style={{position: 'absolute', right: 40, top: 60, opacity: Math.min(ease(t, 5.6, 0.6), 1 - guess * 0.75)}}>
				<g transform={`translate(${zwc[0]} ${zwc[1]}) scale(${zoom}) translate(${-zwc[0]} ${-zwc[1]})`}>
					{shapes.map((s) => {
						const isZ = s.id === '716';
						const isSA = s.id === '710';
						const fill = isZ ? `rgba(255,217,142,${0.15 + 0.75 * zw})` : isSA ? `rgba(242,173,60,${0.12 + 0.45 * sa})` : 'rgba(255,255,255,0.06)';
						return <path key={s.id} d={s.d} fill={fill} stroke={isZ || isSA ? COLORS.goldHi : 'rgba(255,255,255,0.25)'} strokeWidth={isZ ? 2.5 : 1.2} />;
					})}
					{shapes.filter((s) => NAMES[s.id]).map((s) => (
						<text key={s.id} x={s.c[0]} y={s.c[1]} textAnchor="middle" fontFamily={MONO} fontWeight={700} fontSize={s.id === '716' ? 30 / zoom : 28 / zoom} fill={s.id === '716' ? '#1a1206' : COLORS.text} opacity={s.id === '716' ? zw : sa}>
							{NAMES[s.id]}
						</text>
					))}
				</g>
			</svg>
			<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingBottom: 150, opacity: guess}}>
				<Panel style={{textAlign: 'center', padding: '40px 60px', transform: `scale(${interpolate(guess, [0, 1], [0.92, 1])})`}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 34, color: COLORS.muted, letterSpacing: 3}}>BEFORE I SHOW YOU THE BIGGEST BANKNOTE</div>
					<div style={{fontFamily: DISPLAY, fontSize: 120, lineHeight: 1.1, marginTop: 10, ...GOLD_TEXT}}>HOW MANY ZEROS?</div>
					<div style={{marginTop: 20, opacity: ease(t, 21.9)}}>
						<Chip size={34}>COMMENT YOUR GUESS 💬</Chip>
					</div>
				</Panel>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};

// S04 BEAT 1: Hanke and Kwok, 24.7 hours, then the pay bars Friday to Friday
const DAYS = ['FRI', 'SAT', 'SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI'];
const PCTS = ['100%', '50%', '25%', '12.5%', '6.3%', '3.1%', '1.6%', '0.8%'];
const BAR_AT = [13.2, 14.0, 14.4, 14.8, 15.2, 15.6, 16.0, 16.7];
export const S04Doubling: React.FC = () => {
	const t = useT();
	const part1 = Math.min(ease(t, 0.2), fadeOut(t, 11.6));
	const sweep = interpolate(t, [8.4, 9.9], [0, 360], clamp);
	const part2 = ease(t, 12.1);
	const under = usePop(17.7, 12);
	return (
		<AbsoluteFill>
			<Center style={{opacity: part1}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 70}}>
					<svg width={340} height={340} viewBox="0 0 200 200">
						<circle cx="100" cy="100" r="92" fill="rgba(255,255,255,0.04)" stroke={COLORS.gold} strokeWidth="5" />
						{Array.from({length: 12}, (_, i) => (
							<line key={i} x1="100" y1="16" x2="100" y2="28" stroke={COLORS.goldHi} strokeWidth="4" transform={`rotate(${i * 30} 100 100)`} />
						))}
						<line x1="100" y1="100" x2="100" y2="34" stroke={COLORS.goldHi} strokeWidth="6" strokeLinecap="round" transform={`rotate(${sweep} 100 100)`} />
						<circle cx="100" cy="100" r="7" fill={COLORS.goldHi} />
					</svg>
					<div style={{width: 900}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.muted, letterSpacing: 2, opacity: ease(t, 2.1)}}>ECONOMISTS STEVE HANKE AND ALEX KWOK ▪ NOVEMBER 2008</div>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 64, color: COLORS.text, marginTop: 18, opacity: ease(t, 6.0)}}>Prices doubled about every</div>
						<div style={{fontFamily: DISPLAY, fontSize: 170, lineHeight: 1, ...GOLD_TEXT, opacity: ease(t, 8.4)}}>24.7 HOURS</div>
					</div>
				</div>
			</Center>
			<Center style={{opacity: part2}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 60}}>
					<Panel style={{paddingBottom: 22}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.goldHi, letterSpacing: 2, marginBottom: 14}}>YOUR PAY, FRIDAY TO FRIDAY</div>
						<div style={{display: 'flex', alignItems: 'flex-end', gap: 22, height: 470}}>
							{DAYS.map((d, i) => {
								const g = ease(t, BAR_AT[i], 0.35);
								const last = i === DAYS.length - 1;
								return (
									<div key={i} style={{display: 'flex', flexDirection: 'column', alignItems: 'center', width: 84}}>
										<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 24, color: last ? COLORS.goldHi : COLORS.text, opacity: g, marginBottom: 6}}>{PCTS[i]}</div>
										<div style={{width: 84, height: Math.max(4, 400 * 0.5 ** i * g), borderRadius: 12, background: last ? 'linear-gradient(180deg, #ffb35c, #e0602f)' : `linear-gradient(180deg, ${COLORS.goldHi}, ${COLORS.gold})`, boxShadow: last ? `0 0 ${30 * under}px rgba(255,140,60,0.7)` : '0 10px 30px rgba(0,0,0,0.35)'}} />
										<div style={{fontFamily: MONO, fontSize: 26, color: COLORS.muted, marginTop: 10}}>{d}</div>
									</div>
								);
							})}
						</div>
					</Panel>
					<div style={{width: 520}}>
						<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, ...GOLD_TEXT, transform: `scale(${under})`, transformOrigin: 'left center'}}>UNDER 1%</div>
						<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 32, color: COLORS.text, marginTop: 16, opacity: ease(t, 18.3)}}>of what your pay bought a week before</div>
						<div style={{fontFamily: BODY, fontSize: 24, color: COLORS.muted, marginTop: 14, opacity: ease(t, 18.3)}}>Simplified: halves every day</div>
						<div style={{marginTop: 30, opacity: ease(t, 20.4)}}>
							<Chip size={28}>SO HOW DOES MONEY MELT?</Chip>
						</div>
					</div>
				</div>
			</Center>
		</AbsoluteFill>
	);
};

// S05 BEAT 2: more money, fewer goods, higher prices (the auction)
const GOODS = ['🌽', '🍞', '🥛', '🧴', '👟', '🧱', '🍅', '🛢️'];
export const S05Why: React.FC = () => {
	const t = useT();
	const notes = Math.round(interpolate(t, [4.2, 7.8, 11.8, 13.5, 16.4, 21], [2, 8, 8, 18, 18, 34], clamp));
	const goods = Math.round(interpolate(t, [4.2, 7.8, 18.9, 21], [8, 6, 6, 2], clamp));
	const price = t < 13.9 ? 10 : 10 * 2 ** Math.min(6, Math.floor((t - 13.9) / 1.0) + 1);
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', top: 120, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, 0.3), fadeOut(t, 8.2))}}>
				<Chip size={30}>CAUSES ARE DEBATED. ONE IS CLEAR:</Chip>
			</div>
			<Center>
				<div style={{display: 'flex', alignItems: 'flex-end', gap: 90, opacity: ease(t, 4.1)}}>
					<Panel style={{width: 470, textAlign: 'center'}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.goldHi, letterSpacing: 2}}>MONEY PRINTED</div>
						<div style={{display: 'flex', flexWrap: 'wrap-reverse', gap: 6, justifyContent: 'center', marginTop: 18, height: 360, alignContent: 'flex-start'}}>
							{Array.from({length: notes}, (_, i) => <Note key={i} width={120} label="Z$" />)}
						</div>
					</Panel>
					<div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14, opacity: ease(t, 8.5)}}>
						<div style={{fontFamily: DISPLAY, fontSize: 96, ...GOLD_TEXT}}>{rand(price)}</div>
						<Loaf size={260} />
						<div style={{width: 260, height: 26, borderRadius: 8, background: 'linear-gradient(180deg, #2a2a2a, #111)', border: `1px solid ${COLORS.gold}`}} />
						<div style={{fontFamily: MONO, fontSize: 24, color: COLORS.muted}}>ONE LOAF</div>
					</div>
					<Panel style={{width: 470, textAlign: 'center'}}>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.goldHi, letterSpacing: 2}}>GOODS PRODUCED</div>
						<div style={{display: 'flex', flexWrap: 'wrap', gap: 14, justifyContent: 'center', marginTop: 24, height: 340, alignContent: 'flex-start'}}>
							{GOODS.map((g, i) => (
								<div key={i} style={{fontSize: 74, opacity: i < goods ? 1 : 0.08, filter: i < goods ? 'none' : 'grayscale(1)'}}>{g}</div>
							))}
						</div>
					</Panel>
				</div>
			</Center>
			<div style={{position: 'absolute', bottom: 190, width: '100%', textAlign: 'center', opacity: ease(t, 14.5)}}>
				<Chip size={32}>MORE MONEY + FEWER GOODS = HIGHER PRICES</Chip>
				<span style={{fontFamily: BODY, fontSize: 22, color: COLORS.muted, marginLeft: 18}}>(simplified)</span>
			</div>
		</AbsoluteFill>
	);
};

// S06 BEAT 3: how people coped, respect, then Leo asks "what would you buy first?"
const COPE = [
	{at: 3.3, icon: '⏱️', title: 'SPEND IT FAST', sub: 'Waiting one day cost them'},
	{at: 8.6, icon: '🌽 ⇄ 👟', title: 'SWAP GOODS', sub: 'A bag of maize for a pair of shoes'},
	{at: 13.7, icon: '$  R', title: 'US DOLLARS AND RAND', sub: 'Money people still trusted'},
];
export const S06Coping: React.FC = () => {
	const t = useT();
	const respect = ease(t, 17.75, 0.6);
	return (
		<AbsoluteFill>
			<Center style={{opacity: fadeOut(t, 21.9)}}>
				<div style={{display: 'flex', gap: 40, opacity: 1 - respect * 0.75}}>
					{COPE.map((c, i) => {
						const p = ease(t, c.at, 0.5);
						return (
							<Panel key={i} style={{width: 500, textAlign: 'center', opacity: p, transform: `translateY(${(1 - p) * 40}px)`}}>
								<div style={{fontSize: 96, fontFamily: DISPLAY, ...(c.icon.includes('$') ? GOLD_TEXT : {})}}>{c.icon}</div>
								<div style={{fontFamily: DISPLAY, fontSize: 60, marginTop: 6, ...GOLD_TEXT}}>{c.title}</div>
								<div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: COLORS.text, marginTop: 8}}>{c.sub}</div>
							</Panel>
						);
					})}
				</div>
				<div style={{position: 'absolute', fontFamily: BODY, fontWeight: 800, fontSize: 64, color: COLORS.champagne, opacity: respect, textShadow: '0 0 30px rgba(242,173,60,0.4)', textAlign: 'center'}}>
					Real families lived through this.
				</div>
			</Center>
			<LeoClip clip="L2" from={22.1} seconds={6.6} full />
			<div style={{position: 'absolute', top: 110, width: '100%', textAlign: 'center', opacity: ease(t, 23.4)}}>
				<Chip size={40} style={{background: 'rgba(5,4,3,0.75)'}}>WHAT WOULD YOU BUY FIRST? 💬</Chip>
			</div>
		</AbsoluteFill>
	);
};

// S07 BEAT 4: the 100 trillion note and the 14 zeros, Leo amazed
export const S07Zeros: React.FC = () => {
	const t = useT();
	const zeros = t < 10.6 ? 0 : Math.min(14, Math.floor((t - 10.6) / 0.13) + 1);
	const grouped = ('1' + '0'.repeat(zeros)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	const done = zeros === 14;
	const reveal = usePop(12.5, 13);
	const counting = ease(t, 8.0);
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', left: 110, top: 150, width: 1060}}>
				<div style={{opacity: ease(t, 0.3)}}>
					<Chip size={28}>JANUARY 2009 ▪ RESERVE BANK OF ZIMBABWE</Chip>
				</div>
				<div style={{display: 'flex', alignItems: 'center', gap: 34, marginTop: 34, opacity: ease(t, 4.3)}}>
					<Note width={360} label="Z$" />
					<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1, ...GOLD_TEXT}}>100 TRILLION<br />DOLLARS</div>
				</div>
				<Panel style={{marginTop: 40, opacity: counting}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.muted, letterSpacing: 3}}>HOW CLOSE WAS YOUR GUESS?</div>
					<div style={{fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.15, ...GOLD_TEXT}}>Z${grouped}</div>
					<div style={{display: 'flex', gap: 10, marginTop: 12}}>
						{Array.from({length: 14}, (_, i) => <div key={i} style={{width: 48, height: 10, borderRadius: 5, background: i < zeros ? COLORS.goldHi : 'rgba(255,255,255,0.1)'}} />)}
					</div>
				</Panel>
				<div style={{display: 'flex', alignItems: 'center', gap: 30, marginTop: 26}}>
					<div style={{fontFamily: DISPLAY, fontSize: 110, opacity: done ? 1 : 0, transform: `scale(${done ? reveal : 0.8})`, transformOrigin: 'left center', ...GOLD_TEXT}}>14 ZEROS</div>
					<div style={{opacity: ease(t, 13.0)}}><Chip size={28}>AND STILL, NOT ENOUGH</Chip></div>
				</div>
			</div>
			<LeoClip clip="L3" from={9.4} seconds={6.17} style={{right: 70, top: 150, width: 620, height: 640}} />
		</AbsoluteFill>
	);
};

// S08 BEAT 5: money cheaper than paper (the 2009 poster campaign), Cannes Lions, abandoned April 2009
export const S08Posters: React.FC = () => {
	const t = useT();
	const wall = Math.round(interpolate(t, [6.6, 10.0], [0, 24], clamp));
	const quote = Math.min(ease(t, 13.0), fadeOut(t, 23.4));
	const trophy = usePop(17.6, 13);
	const abandon = ease(t, 24.9, 0.5);
	const coins = usePop(29.2, 13);
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', left: 110, top: 130, opacity: Math.min(ease(t, 0.4), fadeOut(t, 12.9))}}>
				<Chip size={30}>JOHANNESBURG ▪ MARCH 2009</Chip>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 56, color: COLORS.text, marginTop: 24, width: 780, opacity: ease(t, 4.3)}}>
					An ad agency printed posters straight onto real banknotes
				</div>
				<div style={{display: 'flex', gap: 30, alignItems: 'center', marginTop: 40, opacity: ease(t, 10.3)}}>
					<Panel style={{padding: '18px 26px', textAlign: 'center'}}>
						<div style={{fontFamily: MONO, fontSize: 26, color: COLORS.goldHi}}>PRINT ON MONEY</div>
						<div style={{fontFamily: DISPLAY, fontSize: 64, ...GOLD_TEXT}}>CHEAPER</div>
					</Panel>
					<div style={{fontFamily: DISPLAY, fontSize: 64, color: COLORS.muted}}>THAN</div>
					<Panel style={{padding: '18px 26px', textAlign: 'center'}}>
						<div style={{fontFamily: MONO, fontSize: 26, color: COLORS.muted}}>BUYING</div>
						<div style={{fontFamily: DISPLAY, fontSize: 64, color: COLORS.text}}>PAPER</div>
					</Panel>
				</div>
			</div>
			<div style={{position: 'absolute', right: 110, top: 140, width: 760, display: 'flex', flexWrap: 'wrap', gap: 8, opacity: Math.min(1, fadeOut(t, 12.9) + 0)}}>
				{Array.from({length: wall}, (_, i) => <Note key={i} width={180} label="Z$" />)}
			</div>
			<Center style={{opacity: quote}}>
				<Panel style={{width: 1300, textAlign: 'center', padding: '44px 60px'}}>
					<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1.1, ...GOLD_TEXT}}>"It's cheaper to print this on money than paper."</div>
					<div style={{fontFamily: BODY, fontSize: 26, color: COLORS.muted, marginTop: 18}}>Poster line from the 2009 campaign by TBWA\Hunt\Lascaris, Johannesburg</div>
					<div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, marginTop: 30, opacity: trophy, transform: `scale(${trophy})`}}>
						<svg width="90" height="90" viewBox="0 0 64 64">
							<path d="M18 6h28v10c0 10-6 18-14 18S18 26 18 16z" fill={COLORS.gold} />
							<path d="M18 10H8c0 9 5 14 11 15M46 10h10c0 9-5 14-11 15" stroke={COLORS.gold} strokeWidth="4" fill="none" />
							<rect x="28" y="34" width="8" height="12" fill={COLORS.gold} /><rect x="18" y="46" width="28" height="8" rx="2" fill={COLORS.goldHi} />
						</svg>
						<Chip size={32}>CANNES LIONS 2009 ▪ OUTDOOR GRAND PRIX</Chip>
					</div>
				</Panel>
			</Center>
			<Center style={{opacity: Math.min(abandon, fadeOut(t, 31.9))}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 70}}>
					<div style={{position: 'relative'}}>
						<Note width={520} label="Z$" grey={abandon} />
						<div style={{position: 'absolute', left: '50%', top: '50%', transform: `translate(-50%,-50%) rotate(-12deg) scale(${interpolate(abandon, [0, 1], [1.4, 1])})`, border: '6px solid #e0602f', color: '#ff8a4c', fontFamily: DISPLAY, fontSize: 64, padding: '6px 26px', borderRadius: 12, background: 'rgba(5,4,3,0.6)', whiteSpace: 'nowrap'}}>ABANDONED ▪ APRIL 2009</div>
					</div>
					<div style={{display: 'flex', gap: 30, opacity: coins, transform: `scale(${coins})`}}>
						{['$', 'R'].map((s) => (
							<div key={s} style={{width: 190, height: 190, borderRadius: '50%', background: `radial-gradient(circle at 35% 30%, ${COLORS.goldHi}, ${COLORS.gold} 55%, #a8701f)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 120, color: '#3a2508', boxShadow: '0 20px 40px rgba(0,0,0,0.5)'}}>{s}</div>
						))}
					</div>
				</div>
			</Center>
			<div style={{position: 'absolute', bottom: 200, width: '100%', textAlign: 'center', opacity: ease(t, 32.1)}}>
				<Chip size={38}>HERE'S THE PART MOST PEOPLE MISS</Chip>
			</div>
		</AbsoluteFill>
	);
};

// S09 BEAT 6: money is a promise plus trust; the voucher from a closed shop
export const S09Promise: React.FC = () => {
	const t = useT();
	const eq = Math.min(ease(t, 3.0), fadeOut(t, 6.4));
	const shop = ease(t, 6.6);
	const shutter = interpolate(t, [8.3, 9.2], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const gone = ease(t, 11.3, 1.2);
	return (
		<AbsoluteFill>
			<Center style={{opacity: Math.min(ease(t, 0.3), fadeOut(t, 2.9))}}>
				<div style={{display: 'flex', gap: 120}}>
					{['📄 PAPER', '🪙 METAL'].map((w, i) => (
						<div key={w} style={{position: 'relative', fontFamily: DISPLAY, fontSize: 110, color: COLORS.text, opacity: ease(t, 0.3 + i * 1.5)}}>
							{w}
							<div style={{position: 'absolute', left: -10, right: -10, top: '50%', height: 10, background: '#e0602f', transform: `rotate(-8deg) scaleX(${ease(t, 0.9 + i * 1.5)})`, borderRadius: 5}} />
						</div>
					))}
				</div>
			</Center>
			<Center style={{opacity: eq}}>
				<div style={{fontFamily: DISPLAY, fontSize: 150, ...GOLD_TEXT}}>MONEY = PROMISE + TRUST</div>
			</Center>
			<Center style={{opacity: shop}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 80}}>
					<div style={{position: 'relative', width: 520, height: 420, borderRadius: 18, background: 'linear-gradient(180deg, #3a2c18, #1a140b)', border: `2px solid ${COLORS.gold}`, overflow: 'hidden'}}>
						<div style={{position: 'absolute', top: 18, width: '100%', textAlign: 'center', fontFamily: DISPLAY, fontSize: 56, ...GOLD_TEXT}}>THE SHOP</div>
						<div style={{position: 'absolute', left: 60, right: 60, bottom: 0, top: 100, background: 'linear-gradient(180deg, rgba(255,217,142,0.35), rgba(255,217,142,0.08))'}} />
						<div style={{position: 'absolute', left: 60, right: 60, top: 100, height: `${shutter * 320}px`, background: 'repeating-linear-gradient(180deg, #6b6b6b 0 14px, #4a4a4a 14px 18px)'}} />
						<div style={{position: 'absolute', bottom: 24, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 30, color: '#ff8a4c', opacity: ease(t, 9.0)}}>CLOSED</div>
					</div>
					<div style={{width: 470, height: 250, borderRadius: 22, background: `linear-gradient(135deg, ${COLORS.goldHi}, ${COLORS.gold} 60%, #b0761f)`, filter: `grayscale(${gone}) brightness(${1 - gone * 0.35})`, boxShadow: `0 0 ${50 * (1 - gone)}px rgba(242,173,60,0.6)`, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', transform: 'rotate(-4deg)'}}>
						<div style={{fontFamily: DISPLAY, fontSize: 70, color: '#3a2508'}}>VOUCHER</div>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: '#3a2508'}}>R500 AT THE SHOP</div>
					</div>
				</div>
				<div style={{marginTop: 40, opacity: ease(t, 13.4)}}><Chip size={36}>NO TRUST, NO MONEY</Chip></div>
			</Center>
		</AbsoluteFill>
	);
};

// S10 PAYOFF: never all your trust in one kind of money; know what stands behind it; knowledge
const KINDS = [
	{title: 'CASH', icon: '💵', behind: "A government's promise", at: 9.0},
	{title: 'STABLECOIN', icon: '🪙', behind: 'As strong as its company and reserves', at: 13.1},
	{title: 'BITCOIN', icon: '₿', behind: 'Big price swings, up and down', at: 17.05},
];
export const S10Lesson: React.FC = () => {
	const t = useT();
	const book = usePop(21.3, 13);
	const prompt = ease(t, 23.8);
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', top: 120, width: '100%', textAlign: 'center', opacity: ease(t, 0.3)}}>
				<Chip size={32}>NEVER PUT ALL YOUR TRUST IN ONE KIND OF MONEY</Chip>
			</div>
			<Center style={{opacity: 1 - prompt}}>
				<div style={{display: 'flex', gap: 40, marginTop: 40}}>
					{KINDS.map((k, i) => {
						const p = ease(t, 3.2 + i * 0.5, 0.5);
						const b = ease(t, k.at, 0.5);
						return (
							<Panel key={k.title} style={{width: 470, textAlign: 'center', opacity: p, transform: `translateY(${(1 - p) * 40}px)`}}>
								<div style={{fontSize: 100, fontFamily: DISPLAY, ...(k.icon === '₿' ? GOLD_TEXT : {})}}>{k.icon}</div>
								<div style={{fontFamily: DISPLAY, fontSize: 64, ...GOLD_TEXT}}>{k.title}</div>
								<div style={{fontFamily: MONO, fontSize: 24, color: COLORS.muted, marginTop: 10, opacity: ease(t, 6.5)}}>WHAT STANDS BEHIND IT?</div>
								<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 32, color: COLORS.text, marginTop: 8, minHeight: 84, opacity: b}}>{k.behind}</div>
							</Panel>
						);
					})}
				</div>
				<div style={{display: 'flex', alignItems: 'center', gap: 24, marginTop: 36, opacity: book, transform: `scale(${book})`}}>
					<div style={{fontSize: 80}}>📘</div>
					<div style={{fontFamily: DISPLAY, fontSize: 84, ...GOLD_TEXT}}>YOUR PROTECTION = KNOWLEDGE</div>
				</div>
			</Center>
			<Center style={{opacity: prompt}}>
				<Panel style={{textAlign: 'center', padding: '44px 70px', background: 'rgba(12,9,5,0.92)'}}>
					<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 34, color: COLORS.muted, letterSpacing: 3}}>FINISH THE SENTENCE IN THE COMMENTS</div>
					<div style={{fontFamily: DISPLAY, fontSize: 150, lineHeight: 1.1, marginTop: 10, ...GOLD_TEXT}}>MONEY IS ___ 💬</div>
				</Panel>
			</Center>
		</AbsoluteFill>
	);
};

// S11 BRIDGE AND CTA: the MTG TRIBE, mtgtribe.com/group, share it
export const S11Tribe: React.FC = () => {
	const t = useT();
	const cta = usePop(12.9, 14);
	const share = ease(t, 16.0);
	return (
		<AbsoluteFill>
			<Center style={{opacity: Math.min(ease(t, 1.5), 1 - share * 0.7)}}>
				<div style={{fontFamily: DISPLAY, fontSize: 170, lineHeight: 1, ...GOLD_TEXT}}>MTG TRIBE</div>
				<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 48, color: COLORS.text, marginTop: 14, opacity: ease(t, 3.7)}}>A community of action takers</div>
				<div style={{display: 'flex', gap: 24, marginTop: 34}}>
					{[['LEARN HOW MONEY WORKS', 5.9], ['OLD AND NEW', 7.8], ['YOUR OWN DECISIONS', 9.6]].map(([w, at]) => (
						<div key={w as string} style={{opacity: ease(t, at as number)}}><Chip size={30}>{w as string}</Chip></div>
					))}
				</div>
			</Center>
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 200, display: 'flex', justifyContent: 'center', opacity: cta, transform: `translateY(${(1 - cta) * 40}px)`}}>
				<Panel style={{display: 'flex', alignItems: 'center', gap: 28, padding: '22px 44px'}}>
					<BrandIcon icon="whatsapp" size={84} />
					<div>
						<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 28, color: COLORS.muted, letterSpacing: 2}}>JOIN THE MTG TRIBE</div>
						<div style={{fontFamily: DISPLAY, fontSize: 92, lineHeight: 1, ...GOLD_TEXT}}>mtgtribe.com/group</div>
					</div>
				</Panel>
			</div>
			<div style={{position: 'absolute', top: 130, width: '100%', textAlign: 'center', opacity: share}}>
				<Chip size={34}>🔁 SEND THIS TO THE FRIEND WHO KEEPS ALL THEIR SAVINGS IN ONE PLACE</Chip>
			</div>
		</AbsoluteFill>
	);
};

// S12 OUTRO: MTG's end card (circle photo), platforms, like share comment, Leo waves, slogan
const PLATFORMS: Array<['whatsapp' | 'telegram' | 'tiktok' | 'youtube', string]> = [
	['whatsapp', 'mtgtribe.com/group'],
	['telegram', 't.me/mtgtribez'],
	['tiktok', '@joinmtgtribe'],
	['youtube', '@mtgtribe'],
];
export const S12Outro: React.FC = () => {
	const t = useT();
	const photo = usePop(0.1, 18);
	const slogan = usePop(22.0, 12);
	return (
		<AbsoluteFill>
			<div style={{position: 'absolute', left: 110, top: 110, display: 'flex', flexDirection: 'column', gap: 26}}>
				<div style={{display: 'flex', alignItems: 'center', gap: 40}}>
					<div style={{opacity: photo, transform: `scale(${interpolate(photo, [0, 1], [0.9, 1])})`}}><PhotoCard size={330} /></div>
					<div>
						<div style={{fontFamily: DISPLAY, fontSize: 110, lineHeight: 1, ...GOLD_TEXT}}>{BRAND.name}</div>
						<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text}}>{BRAND.title}</div>
						<div style={{fontFamily: BODY, fontSize: 26, color: COLORS.muted, marginTop: 10, opacity: ease(t, 0.3)}}>Education only. Not financial advice.</div>
					</div>
				</div>
				<div style={{display: 'flex', gap: 22, opacity: ease(t, 7.4)}}>
					{['👍 LIKE', '🔁 SHARE', '💬 COMMENT'].map((w, i) => (
						<div key={w} style={{opacity: ease(t, 7.5 + i * 0.4)}}><Chip size={30}>{w}</Chip></div>
					))}
				</div>
				<div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, width: 980, opacity: ease(t, 9.6)}}>
					{PLATFORMS.map(([icon, label], i) => (
						<Panel key={icon} style={{display: 'flex', alignItems: 'center', gap: 18, padding: '14px 22px', opacity: ease(t, 9.6 + i * 0.3)}}>
							<BrandIcon icon={icon} size={48} />
							<div style={{fontFamily: MONO, fontWeight: 700, fontSize: 30, color: COLORS.text}}>{label}</div>
						</Panel>
					))}
				</div>
			</div>
			<LeoClip clip="L4" from={14.5} seconds={6.0} style={{right: 90, top: 150, width: 620, height: 620}} />
			<div style={{position: 'absolute', right: 90, bottom: 200, width: 700, textAlign: 'center', opacity: slogan, transform: `scale(${slogan})`}}>
				<span style={{fontFamily: DISPLAY, fontSize: 84, ...GOLD_TEXT}}>Let's Get This Crypto!</span>{' '}
				<span style={{fontFamily: DISPLAY, fontSize: 84}}>💪</span>
			</div>
		</AbsoluteFill>
	);
};

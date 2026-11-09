import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {COLORS} from '../../brand';
import {BrandBar} from '../../components/BrandBar';
import {LeoMoment} from '../../components/Leo';
import {UrlPill} from '../../components/Pills';
import {BODY} from '../../fonts';
import {Laptop3D, Notepad3D} from '../../three/css3d';
import {Backdrop, Chip, clamp, Cues, ease, fadeOut, useT} from '../whatif01/ui';

// Preview for MTG (10 November 2026): Leo's moments from his existing clips, each with its accent and soft sound, and
// the free 3D props for the action moments (a notepad that writes itself, a laptop that opens). Labels are for MTG only.
export const LEOMOMENTS_FRAMES = 30 * 17;

const Label: React.FC<{t: number; a: number; b: number; text: string}> = ({t, a, b, text}) => (
	<div style={{position: 'absolute', top: 1290, width: '100%', textAlign: 'center', opacity: Math.min(ease(t, a, 0.25), fadeOut(t, b, 0.25))}}>
		<span style={{display: 'inline-block', padding: '12px 30px', borderRadius: 999, background: 'rgba(18,14,9,0.94)', border: '2.5px solid rgba(242,173,60,0.85)', fontFamily: BODY, fontWeight: 800, fontSize: 40, color: COLORS.text}}>{text}</span>
	</div>
);

export const LeoMoments: React.FC = () => {
	const t = useT();
	return (
		<AbsoluteFill style={{background: COLORS.bg}}>
			<Backdrop />
			<div style={{position: 'absolute', top: 290, width: '100%', textAlign: 'center', opacity: ease(t, 0.1)}}>
				<Chip size={40}>LEO'S MOMENTS</Chip>
			</div>
			<LeoMoment m="aha" at={0.4} frame="bust" style={{left: 290, top: 470, width: 500, height: 640}} accent="aha" />
			<Label t={t} a={0.5} b={1.55} text="💡 Aha: now I get it" />
			<LeoMoment m="wow" at={1.9} frame="bust" style={{left: 290, top: 470, width: 500, height: 640}} accent="wow" seconds={1.7} />
			<Label t={t} a={2.0} b={3.5} text="✨ Wow" />
			<LeoMoment m="worried" at={3.9} frame="bust" style={{left: 290, top: 470, width: 500, height: 640}} accent="alert" />
			<Label t={t} a={4.0} b={5.3} text="⚠️ Careful (a warning)" />
			<LeoMoment m="reassure" at={5.5} frame="bust" style={{left: 290, top: 470, width: 500, height: 640}} accent="relief" />
			<Label t={t} a={5.6} b={6.75} text="😌 It's going to be okay" />
			<LeoMoment m="point" at={7.0} frame="bust" style={{left: 70, top: 470, width: 440, height: 620}} seconds={2.9} />
			<div style={{position: 'absolute', left: 560, top: 560, opacity: Math.min(ease(t, 7.2), fadeOut(t, 9.85))}}>
				<Notepad3D w={440} t={t} title="MY NOTES" lines={[['1. Learn first ✓', 7.6], ['2. Keep my keys safe ✓', 8.5]]} />
			</div>
			<Label t={t} a={7.1} b={9.8} text="📝 This is important (taking notes)" />
			<LeoMoment m="thumbsup" at={10.1} frame="bust" style={{left: 70, top: 470, width: 440, height: 620}} />
			<div style={{position: 'absolute', left: 500, top: 560, opacity: Math.min(ease(t, 10.0), fadeOut(t, 13.0))}}>
				<Laptop3D w={500} open={interpolate(t, [10.3, 11.3], [0, 1], clamp)}>
					<UrlPill text="mtgtribe.com" size={34} />
				</Laptop3D>
			</div>
			<Label t={t} a={10.2} b={13.0} text="💻 Let me get started now" />
			<LeoMoment m="welcome" at={13.3} frame="bust" style={{left: 290, top: 470, width: 500, height: 640}} accent="warm" />
			<Label t={t} a={13.4} b={16.5} text="🤗 Come in, you belong here" />
			<Cues list={[[0.1, 'air', 0.3], [7.0, 'pluck2', 0.3], [7.6, 'scribble', 0.4], [8.5, 'scribble', 0.4], [10.3, 'laptop', 0.45], [10.15, 'pluck3', 0.25]]} />
			<BrandBar />
		</AbsoluteFill>
	);
};

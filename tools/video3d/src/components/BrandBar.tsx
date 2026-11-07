import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND, COLORS, FILES} from '../brand';
import {BODY, MONO} from '../fonts';
import {useLayout} from '../lib/layout';

// The small brand bar shown in every frame. The tiny icon is the only place the face crop is used,
// because the t-shirt print cannot be read at this size.
export const BrandBar: React.FC<{opacity?: number}> = ({opacity = 1}) => {
	const {vertical, safe} = useLayout();
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity}}>
			<div
				style={{
					position: 'absolute',
					top: vertical ? safe.top - 60 : 40,
					left: vertical ? 0 : 56,
					right: vertical ? 0 : undefined,
					display: 'flex',
					justifyContent: vertical ? 'center' : 'flex-start',
					alignItems: 'center',
					gap: 16,
				}}
			>
				<Img
					src={staticFile(FILES.faceCrop)}
					alt=""
					style={{width: 54, height: 54, borderRadius: '50%', border: `2px solid ${COLORS.gold}`, objectFit: 'cover'}}
				/>
				<div style={{lineHeight: 1.2}}>
					<div style={{fontFamily: BODY, fontWeight: 800, fontSize: 25, color: COLORS.text}}>
						{BRAND.line.split('|')[0]}
						<span style={{color: COLORS.gold, fontWeight: 500}}>|</span>
						{BRAND.line.split('|')[1]}
					</div>
					<div style={{fontFamily: MONO, fontWeight: 500, fontSize: 18, color: COLORS.gold, letterSpacing: 1}}>
						{BRAND.site}
					</div>
				</div>
			</div>
		</AbsoluteFill>
	);
};

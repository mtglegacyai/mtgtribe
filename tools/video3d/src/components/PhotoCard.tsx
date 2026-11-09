import React from 'react';
import {Img, staticFile} from 'remotion';
import {COLORS, FILES} from '../brand';

// MTG's profile photo, always in a CIRCLE (MTG, 7 November 2026: "always put my profile picture in a circle").
// The whole square photo fills the circle (since 9 November 2026 his formal photo: face, navy blazer and the office
// view all visible). Never zoom in to a face-only crop, and never shrink it: make room in the layout instead.
// Gold gradient ring and a soft gold glow, same colours as brand/photo_card.py.
// Reference sizes (diameter) on 1920x1080: intro about 600 px, signature about 580 px,
// slogan scene about 330 px, end card 300 to 400 px.
export const PhotoCard: React.FC<{size: number; style?: React.CSSProperties}> = ({size, style}) => {
	const ring = Math.max(4, Math.round(size / 50));
	const glow = Math.max(14, Math.round(size / 9));
	return (
		<div
			style={{
				boxSizing: 'content-box',
				width: size,
				height: size,
				padding: ring,
				borderRadius: '50%',
				background: `linear-gradient(146deg, ${COLORS.frameLight}, ${COLORS.frameDark})`,
				boxShadow: `0 0 ${Math.round(glow * 1.1)}px ${Math.round(glow * 0.2)}px ${COLORS.frameGlow}`,
				...style,
			}}
		>
			<Img
				src={staticFile(FILES.photo)}
				alt="MTG"
				style={{display: 'block', width: size, height: size, borderRadius: '50%', objectFit: 'cover'}}
			/>
		</div>
	);
};

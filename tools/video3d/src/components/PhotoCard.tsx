import React from 'react';
import {Img, staticFile} from 'remotion';
import {COLORS, FILES} from '../brand';

// MTG's full profile photo: face, the mtgTribe.com t-shirt print and the sign all visible.
// Square with rounded corners, gold gradient frame and a soft gold glow (same maths as brand/photo_card.py).
// Never crop it to a small face circle. Reference sizes on 1920x1080: intro about 600 px,
// signature about 580 px, slogan scene about 330 px, end card 300 to 400 px.
export const PhotoCard: React.FC<{size: number; style?: React.CSSProperties}> = ({size, style}) => {
	const ring = Math.max(4, Math.floor(size / 55));
	const pad = Math.max(14, Math.floor(size / 9));
	const radius = Math.floor(size / 12);
	return (
		<div
			style={{
				boxSizing: 'content-box',
				width: size,
				height: size,
				padding: ring,
				borderRadius: radius + ring,
				background: `linear-gradient(146deg, ${COLORS.frameLight}, ${COLORS.frameDark})`,
				boxShadow: `0 0 ${Math.round(pad * 1.1)}px ${Math.round(pad * 0.2)}px ${COLORS.frameGlow}`,
				...style,
			}}
		>
			<Img
				src={staticFile(FILES.photo)}
				alt="MTG"
				style={{display: 'block', width: size, height: size, borderRadius: radius}}
			/>
		</div>
	);
};

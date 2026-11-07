import {useVideoConfig} from 'remotion';

// Safe areas, so captions and text stay clear of the buttons and text that
// TikTok, Reels and Shorts draw over vertical videos, and of player controls on 16:9.
export const useLayout = () => {
	const {width, height} = useVideoConfig();
	const vertical = height > width;
	return {
		width,
		height,
		vertical,
		// distance from each edge that stays free of important text
		safe: vertical
			? {top: 200, bottom: 480, left: 70, right: 150}
			: {top: 60, bottom: 90, left: 90, right: 90},
		captionSize: vertical ? 78 : 72,
		captionMaxWidth: vertical ? 820 : 1500,
	};
};

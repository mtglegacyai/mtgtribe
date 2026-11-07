import {type Caption, createTikTokStyleCaptions, type TikTokPage} from '@remotion/captions';
import React, {useMemo} from 'react';
import {AbsoluteFill, Sequence, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS} from '../brand';
import {BODY} from '../fonts';
import {useLayout} from '../lib/layout';

type Props = {
	captions: Caption[];
	// words closer together than this share one caption page (shorter on phones)
	combineWithinMs?: number;
	// how long the last words stay up after they are spoken
	holdMs?: number;
};

// Word by word captions synced to the narration. The spoken word lights up in gold.
// Captions come from scripts/transcribe.py (word timestamps of the final audio), never from guessed timing.
export const Captions: React.FC<Props> = ({captions, combineWithinMs, holdMs = 700}) => {
	const {fps} = useVideoConfig();
	const {vertical} = useLayout();
	const {pages} = useMemo(
		() =>
			createTikTokStyleCaptions({
				captions,
				combineTokensWithinMilliseconds: combineWithinMs ?? (vertical ? 1000 : 1400),
			}),
		[captions, combineWithinMs, vertical],
	);

	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{pages.map((page, i) => {
				const lastWordEnd = page.tokens[page.tokens.length - 1]?.toMs ?? page.startMs + page.durationMs;
				const endMs = Math.min(pages[i + 1]?.startMs ?? Infinity, lastWordEnd + holdMs);
				const from = Math.round((page.startMs / 1000) * fps);
				const durationInFrames = Math.round((endMs / 1000) * fps) - from;
				if (durationInFrames <= 0) return null;
				return (
					<Sequence key={page.startMs} from={from} durationInFrames={durationInFrames} name={`Caption: ${page.text.trim()}`}>
						<CaptionPage page={page} />
					</Sequence>
				);
			})}
		</AbsoluteFill>
	);
};

const CaptionPage: React.FC<{page: TikTokPage}> = ({page}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const layout = useLayout();
	const nowMs = page.startMs + (frame / fps) * 1000;
	const enter = spring({frame, fps, config: {damping: 200}, durationInFrames: 6});

	return (
		<AbsoluteFill
			style={{
				justifyContent: 'flex-end',
				alignItems: 'center',
				paddingBottom: layout.safe.bottom,
				paddingLeft: layout.safe.left,
				paddingRight: layout.safe.right,
			}}
		>
			<div
				style={{
					maxWidth: layout.captionMaxWidth,
					padding: '10px 26px 14px',
					borderRadius: 22,
					background: 'rgba(5, 4, 3, 0.62)',
					fontFamily: BODY,
					fontWeight: 800,
					fontSize: layout.captionSize,
					lineHeight: 1.18,
					textAlign: 'center',
					textShadow: '0 2px 10px rgba(0, 0, 0, 0.7)',
					opacity: enter,
					transform: `translateY(${(1 - enter) * 18}px)`,
				}}
			>
				{page.tokens.map((token, i) => {
					const active = token.fromMs <= nowMs && nowMs < token.toMs;
					const spoken = token.toMs <= nowMs;
					return (
						<span
							key={i}
							style={{
								whiteSpace: 'pre-wrap',
								color: active ? COLORS.goldHi : spoken ? COLORS.text : 'rgba(245, 239, 230, 0.55)',
							}}
						>
							{token.text}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};

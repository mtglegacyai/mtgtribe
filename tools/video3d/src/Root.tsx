import React from 'react';
import {Composition, Folder} from 'remotion';
import {DOUBLING_PROOF_FRAMES, DoublingProof} from './compositions/DoublingProof';
import {calculateIntro3DMetadata, Intro3D, intro3DDefaults} from './compositions/Intro3D';

// Every video is registered here. Keep orientation as built: 16:9 stays 16:9, 9:16 stays 9:16.
export const RemotionRoot: React.FC = () => (
	<>
	<Folder name="Proofs">
		<Composition id="DoublingProof-9x16" component={DoublingProof} width={1080} height={1920} fps={30} durationInFrames={DOUBLING_PROOF_FRAMES} />
		<Composition id="DoublingProof-16x9" component={DoublingProof} width={1920} height={1080} fps={30} durationInFrames={DOUBLING_PROOF_FRAMES} />
	</Folder>
	<Folder name="Demo">
		<Composition
			id="Intro3D-16x9"
			component={Intro3D}
			width={1920}
			height={1080}
			fps={30}
			durationInFrames={180}
			defaultProps={intro3DDefaults}
			calculateMetadata={calculateIntro3DMetadata}
		/>
		<Composition
			id="Intro3D-9x16"
			component={Intro3D}
			width={1080}
			height={1920}
			fps={30}
			durationInFrames={180}
			defaultProps={intro3DDefaults}
			calculateMetadata={calculateIntro3DMetadata}
		/>
	</Folder>
	</>
);

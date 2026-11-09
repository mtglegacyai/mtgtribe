import React from 'react';
import {Composition, Folder, Still} from 'remotion';
import {FILES} from './brand';
import {DOUBLING_PROOF_FRAMES, DoublingProof} from './compositions/DoublingProof';
import {Thumb01A, Thumb01B} from './compositions/whatif01/Thumbs';
import {Cover01, Cover01_3D} from './compositions/whatif01/Covers';
import {Cover02, DYK02_FPS, DYK02_FRAMES, StoneMoney} from './compositions/dyk02/StoneMoney';
import {Cover03, DKO03_FPS, DKO03_FRAMES, TwelveWords} from './compositions/dko03/TwelveWords';
import {Cover04, MOF04_FPS, MOF04_FRAMES, VaultMyth} from './compositions/mof04/VaultMyth';
import {NEWLOOK_FRAMES, NewLook} from './compositions/preview/NewLook';
import {Hook3D, HOOK3D_FRAMES} from './compositions/whatif01/Hook3D';
import {WHATIF01_3D_FRAMES, WhatIf01_3D} from './compositions/whatif01/WhatIf01_3D';
import {WHATIF01_FPS, WHATIF01_FRAMES, WhatIf01} from './compositions/whatif01/WhatIf01';
import {calculateIntro3DMetadata, Intro3D, intro3DDefaults} from './compositions/Intro3D';

// Every video is registered here. Keep orientation as built: 16:9 stays 16:9, 9:16 stays 9:16.
export const RemotionRoot: React.FC = () => (
	<>
	<Folder name="Videos">
		<Composition id="WhatIf01-16x9" component={WhatIf01} width={1920} height={1080} fps={WHATIF01_FPS} durationInFrames={WHATIF01_FRAMES} defaultProps={{closingTrack: FILES.closingTrack}} />
			<Composition id="WhatIf01-9x16" component={WhatIf01} width={1080} height={1920} fps={WHATIF01_FPS} durationInFrames={WHATIF01_FRAMES} defaultProps={{closingTrack: FILES.closingTrack}} />
		<Still id="Cover01-9x16" component={Cover01} width={1080} height={1920} />
		<Still id="Cover01-3D-9x16" component={Cover01_3D} width={1080} height={1920} />
		<Still id="Thumb01A" component={Thumb01A} width={1280} height={720} />
		<Still id="Thumb01B" component={Thumb01B} width={1280} height={720} />
	</Folder>
	<Folder name="Video02">
		<Composition id="DYK02-9x16" component={StoneMoney} width={1080} height={1920} fps={DYK02_FPS} durationInFrames={DYK02_FRAMES} defaultProps={{closingTrack: FILES.closingTrack}} />
		<Still id="Cover02-9x16" component={Cover02} width={1080} height={1920} />
	</Folder>
	<Folder name="Video03">
		<Composition id="DKO03-9x16" component={TwelveWords} width={1080} height={1920} fps={DKO03_FPS} durationInFrames={DKO03_FRAMES} defaultProps={{closingTrack: FILES.closingTrack}} />
		<Still id="Cover03-9x16" component={Cover03} width={1080} height={1920} />
	</Folder>
	<Folder name="Video04">
		<Composition id="MOF04-9x16" component={VaultMyth} width={1080} height={1920} fps={MOF04_FPS} durationInFrames={MOF04_FRAMES} defaultProps={{closingTrack: FILES.closingTrack}} />
		<Still id="Cover04-9x16" component={Cover04} width={1080} height={1920} />
	</Folder>
	<Folder name="Real3D">
		<Composition id="WhatIf01-3D-9x16" component={WhatIf01_3D} width={1080} height={1920} fps={30} durationInFrames={WHATIF01_3D_FRAMES} defaultProps={{closingTrack: FILES.closingTrack}} />
		<Composition id="Hook3D-9x16" component={Hook3D} width={1080} height={1920} fps={30} durationInFrames={HOOK3D_FRAMES} />
	</Folder>
	<Folder name="Proofs">
		<Composition id="NewLook-9x16" component={NewLook} width={1080} height={1920} fps={30} durationInFrames={NEWLOOK_FRAMES} />
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

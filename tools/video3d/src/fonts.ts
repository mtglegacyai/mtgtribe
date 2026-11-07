// The same fonts as mtgtribe.com and the approved invite video, bundled locally from npm (@fontsource),
// so renders never depend on Google Fonts being reachable. Remotion waits for them before it renders a frame.
import antonUrl from '@fontsource/anton/files/anton-latin-400-normal.woff2';
import mono500Url from '@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2';
import mono700Url from '@fontsource/jetbrains-mono/files/jetbrains-mono-latin-700-normal.woff2';
import manrope500Url from '@fontsource/manrope/files/manrope-latin-500-normal.woff2';
import manrope700Url from '@fontsource/manrope/files/manrope-latin-700-normal.woff2';
import manrope800Url from '@fontsource/manrope/files/manrope-latin-800-normal.woff2';
import {loadFont} from '@remotion/fonts';

const FACES: Array<[family: string, url: string, weight: string]> = [
	['Anton', antonUrl, '400'],
	['Manrope', manrope500Url, '500'],
	['Manrope', manrope700Url, '700'],
	['Manrope', manrope800Url, '800'],
	['JetBrains Mono', mono500Url, '500'],
	['JetBrains Mono', mono700Url, '700'],
];

for (const [family, url, weight] of FACES) {
	loadFont({family, url, weight, style: 'normal'}).catch((err) => {
		throw new Error(`Font ${family} ${weight} failed to load: ${err}`);
	});
}

const EMOJI = '"Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji"';
export const DISPLAY = `Anton, Impact, sans-serif, ${EMOJI}`;
export const BODY = `Manrope, system-ui, sans-serif, ${EMOJI}`;
export const MONO = `"JetBrains Mono", monospace`;

// Quality check stills: render chosen moments of a video to PNG, with one browser for all of them (fast).
// Times are given per section, the way scenes are written: "<section number>:<seconds inside the section>".
//
//   npx remotion bundle --out-dir=/tmp/bundle
//   node scripts/qc-stills.mjs /tmp/bundle /tmp/qc WhatIf01-9x16 public/videos/01/timeline.json 1:3 1:12.5 8:33
//
// Stills are rendered at half size (enough to judge layout); file names are <id>-s<section>-<seconds>.png.
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import {mkdirSync, readFileSync} from 'node:fs';

const [, , bundle, outDir, id, timelinePath, ...points] = process.argv;
if (!bundle || !outDir || !id || !timelinePath || points.length === 0) {
	console.error('usage: node scripts/qc-stills.mjs <bundle dir> <out dir> <composition id> <timeline.json> <section:seconds> ...');
	process.exit(1);
}
const {starts} = JSON.parse(readFileSync(timelinePath, 'utf8'));
mkdirSync(outDir, {recursive: true});
const chromiumOptions = {gl: 'swangle'};
const browser = await openBrowser('chrome', {chromiumOptions});
const composition = await selectComposition({serveUrl: bundle, id, puppeteerInstance: browser});
for (const point of points) {
	const [section, seconds] = point.split(':').map(Number);
	const frame = Math.round((starts[section - 1] + seconds) * composition.fps);
	const output = `${outDir}/${id}-s${String(section).padStart(2, '0')}-${seconds.toFixed(1)}.png`;
	await renderStill({composition, serveUrl: bundle, output, frame, scale: 0.5, puppeteerInstance: browser, chromiumOptions});
	console.log(output);
}
await browser.close({silent: true});

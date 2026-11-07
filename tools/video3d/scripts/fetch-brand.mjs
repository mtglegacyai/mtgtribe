// Copies MTG's approved profile photo and face crop into public/brand/.
// Source of truth: GitHub repo mtglegacyai/mtgtribe, branch brand-assets, folder brand/.
// Tries the local git checkout first (works offline once fetched), then HTTPS.
// Usage: node scripts/fetch-brand.mjs [--force] [--quiet]
import {execFileSync} from 'node:child_process';
import {existsSync, mkdirSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, '..', 'public', 'brand');
const force = process.argv.includes('--force');
const quiet = process.argv.includes('--quiet');
const FILES = ['mtg-profile-photo.png', 'mtg-profile-face-crop.png'];
const RAW = 'https://raw.githubusercontent.com/mtglegacyai/mtgtribe/brand-assets/brand/';

const log = (msg) => {
	if (!quiet) console.log(msg);
};

const fromGit = (file) => {
	try {
		return execFileSync('git', ['show', `origin/brand-assets:brand/${file}`], {
			cwd: here,
			maxBuffer: 64 * 1024 * 1024,
			stdio: ['ignore', 'pipe', 'ignore'],
		});
	} catch {
		return null;
	}
};

const fromHttps = async (file) => {
	const res = await fetch(RAW + file);
	if (!res.ok) throw new Error(`HTTP ${res.status} for ${RAW + file}`);
	return Buffer.from(await res.arrayBuffer());
};

mkdirSync(outDir, {recursive: true});
let failed = 0;
for (const file of FILES) {
	const target = join(outDir, file);
	if (existsSync(target) && !force) {
		log(`ok      ${file} (already there)`);
		continue;
	}
	try {
		const data = fromGit(file) ?? (await fromHttps(file));
		writeFileSync(target, data);
		log(`fetched ${file} (${Math.round(data.length / 1024)} KB)`);
	} catch (err) {
		failed++;
		console.warn(`Could not fetch ${file}: ${err.message}`);
	}
}

if (failed) {
	console.warn(
		'MTG\'s photo is missing. Run "npm run setup" when online, or copy the files from the brand-assets branch into public/brand/.',
	);
}

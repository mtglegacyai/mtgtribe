// Turns a word-level transcript into Remotion captions (the Caption[] format of @remotion/captions).
//
// Input: the JSON written by scripts/transcribe.py --raw or tools/invite-horizontal/transcribe.py
// (faster-whisper: [{start, end, text, words: [{w, s, e, p}]}]), or an .srt file.
// Output: Caption[] JSON, ready for <Captions /> in src/components/Captions.tsx.
//
// Usage:
//   node scripts/whisper-to-captions.mjs <transcript.json|file.srt> <out.json> [--from 0] [--to 3.3] [--shift 0]
//   --from / --to   keep only words inside this time range (seconds in the source)
//   --shift         seconds added to every word (negative moves captions earlier)
// Words that start at --from are moved to 0, so a cut clip lines up with its captions.
import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {dirname} from 'node:path';
import {parseSrt} from '@remotion/captions';

const [, , input, output, ...rest] = process.argv;
if (!input || !output) {
	console.error('Usage: node scripts/whisper-to-captions.mjs <transcript.json|file.srt> <out.json> [--from s] [--to s] [--shift s]');
	process.exit(1);
}
const opt = (name, fallback) => {
	const i = rest.indexOf(`--${name}`);
	return i === -1 ? fallback : Number(rest[i + 1]);
};
const from = opt('from', 0);
const to = opt('to', Infinity);
const shift = opt('shift', 0);

// MTG's rule: no em dashes or en dashes on screen. Replace them with a comma.
const clean = (text) => text.replace(/\s*[\u2013\u2014]\s*/g, ', ').replace(/,\s*,/g, ',');

let words;
const raw = readFileSync(input, 'utf8');
if (input.toLowerCase().endsWith('.srt')) {
	words = parseSrt({input: raw}).captions.map((c) => ({
		text: ` ${c.text.trim()}`,
		s: c.startMs / 1000,
		e: c.endMs / 1000,
		p: null,
	}));
} else {
	const data = JSON.parse(raw);
	const segments = Array.isArray(data) ? data : data.segments;
	words = segments.flatMap((seg) =>
		(seg.words ?? []).map((w) => ({text: w.w ?? w.word, s: w.s ?? w.start, e: w.e ?? w.end, p: w.p ?? w.probability ?? null})),
	);
}

const captions = words
	.filter((w) => w.s >= from - 0.001 && w.e <= to + 0.001)
	.map((w) => {
		const startMs = Math.max(0, Math.round((w.s - from + shift) * 1000));
		const endMs = Math.max(startMs + 1, Math.round((w.e - from + shift) * 1000));
		const text = clean(w.text.startsWith(' ') ? w.text : ` ${w.text}`);
		return {text, startMs, endMs, timestampMs: Math.round((startMs + endMs) / 2), confidence: w.p};
	});

// The first word has no leading space, so captions do not start with a gap.
if (captions.length) captions[0].text = captions[0].text.trimStart();

mkdirSync(dirname(output), {recursive: true});
writeFileSync(output, `${JSON.stringify(captions, null, 1)}\n`);
console.log(`${captions.length} words -> ${output}`);
const low = captions.filter((c) => c.confidence !== null && c.confidence < 0.6);
if (low.length) {
	console.log(`Check these words by ear (low confidence): ${low.map((c) => `"${c.text.trim()}" at ${(c.startMs / 1000).toFixed(2)}s`).join(', ')}`);
}

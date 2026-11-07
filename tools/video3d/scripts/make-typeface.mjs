// Turns a brand font into the typeface JSON that Three.js needs for real 3D (extruded) letters and numbers
// (drei <Text3D font="fonts/anton.typeface.json">). Same format as facetype.js.
//
//   node scripts/make-typeface.mjs node_modules/@fontsource/anton/files/anton-latin-400-normal.woff public/fonts/anton.typeface.json
import {readFileSync, writeFileSync} from 'node:fs';
import opentype from 'opentype.js';

const [, , input, output] = process.argv;
if (!input || !output) {
	console.error('usage: node scripts/make-typeface.mjs <font.woff|ttf|otf> <out.typeface.json>');
	process.exit(1);
}
const buf = readFileSync(input);
const font = opentype.parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
const scale = (1000 * 100) / ((font.unitsPerEm || 2048) * 72);
const r = (v) => Math.round(v * scale);
const chars = ' 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;!?$%&+-=/()\'"#@*R';
const glyphs = {};
for (const ch of new Set(chars)) {
	const g = font.charToGlyph(ch);
	if (!g || g.unicode === undefined) continue;
	const o = g.path.commands
		.map((c) => {
			if (c.type === 'M') return `m ${r(c.x)} ${r(c.y)}`;
			if (c.type === 'L') return `l ${r(c.x)} ${r(c.y)}`;
			if (c.type === 'Q') return `q ${r(c.x)} ${r(c.y)} ${r(c.x1)} ${r(c.y1)}`;
			if (c.type === 'C') return `b ${r(c.x)} ${r(c.y)} ${r(c.x1)} ${r(c.y1)} ${r(c.x2)} ${r(c.y2)}`;
			return '';
		})
		.filter(Boolean)
		.join(' ');
	const bb = g.getBoundingBox();
	glyphs[ch] = {ha: r(g.advanceWidth), x_min: r(bb.x1), x_max: r(bb.x2), o};
}
const head = font.tables.head;
writeFileSync(
	output,
	JSON.stringify({
		glyphs,
		familyName: font.names.fontFamily?.en ?? 'font',
		ascender: r(font.ascender),
		descender: r(font.descender),
		underlinePosition: r(font.tables.post.underlinePosition),
		underlineThickness: r(font.tables.post.underlineThickness),
		boundingBox: {xMin: r(head.xMin), yMin: r(head.yMin), xMax: r(head.xMax), yMax: r(head.yMax)},
		resolution: 1000,
		original_font_information: {format: 0, fontFamily: font.names.fontFamily?.en ?? ''},
	}),
);
console.log(`${Object.keys(glyphs).length} glyphs -> ${output}`);

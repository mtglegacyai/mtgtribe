// Font files imported in src/fonts.ts resolve to a URL at build time.
declare module '*.woff2' {
	const url: string;
	export default url;
}

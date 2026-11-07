// Render settings for every video in this studio. Command line flags override them.
// https://www.remotion.dev/docs/config
import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setOverwriteOutput(true);

// Three.js needs WebGL inside the headless browser.
// "angle" uses the graphics card when the computer has one.
// On a server or cloud session without a graphics card, render with software WebGL:
//   REMOTION_GL=swangle npx remotion render ...   (or add --gl=swangle)
type GlRenderer = Parameters<typeof Config.setChromiumOpenGlRenderer>[0];
Config.setChromiumOpenGlRenderer((process.env.REMOTION_GL as GlRenderer | undefined) ?? 'angle');

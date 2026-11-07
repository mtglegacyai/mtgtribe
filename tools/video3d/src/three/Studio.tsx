import {ContactShadows, Environment, Lightformer} from '@react-three/drei';
import {useFrame, useThree} from '@react-three/fiber';
import React from 'react';
import {COLORS} from '../brand';

// A premium product-shot light setup: warm key light, gold rim light, soft reflections
// and a grounded contact shadow. Everything is built locally (no HDR downloads),
// so renders are identical every time and work offline.
export const StudioLights: React.FC<{shadowY?: number; shadowScale?: number}> = ({shadowY = 0, shadowScale = 12}) => (
	<>
		<ambientLight intensity={0.25} />
		<directionalLight position={[5, 9, 6]} intensity={2.4} color="#fff1d6" />
		<directionalLight position={[-6, 4, -5]} intensity={1.4} color={COLORS.gold} />
		<Environment resolution={256} frames={1}>
			<Lightformer form="rect" intensity={2.4} position={[0, 5, -7]} scale={[12, 3, 1]} color="#ffffff" />
			<Lightformer form="rect" intensity={1.6} position={[-7, 2, 1]} rotation-y={Math.PI / 2} scale={[8, 2, 1]} color="#ffe2a8" />
			<Lightformer form="rect" intensity={1.0} position={[7, 2, 1]} rotation-y={-Math.PI / 2} scale={[8, 2, 1]} color="#ffffff" />
			<Lightformer form="circle" intensity={2.2} position={[0, 9, 0]} rotation-x={Math.PI / 2} scale={5} color="#fff6e0" />
			{/* soft fill from the camera side, so front faces reflect warm light instead of black */}
			<Lightformer form="rect" intensity={1.3} position={[0, 2.5, 9]} rotation-y={Math.PI} scale={[14, 5, 1]} color="#ffe8bd" />
			<Lightformer form="rect" intensity={0.8} position={[0, -3, 4]} rotation-x={-Math.PI / 3} scale={[12, 3, 1]} color="#c98a2b" />
		</Environment>
		<ContactShadows position={[0, shadowY, 0]} opacity={0.65} scale={shadowScale} blur={2.6} far={6} resolution={512} />
	</>
);

type CameraProps = {
	// where the camera is, as a function of the current Remotion frame
	position: [number, number, number];
	lookAt: [number, number, number];
	fov?: number;
};

// Puts the camera where the current frame says. Drive it with interpolate() or spring() from useCurrentFrame(),
// never with clock time, so every render is frame-exact.
export const CameraRig: React.FC<CameraProps> = ({position, lookAt, fov}) => {
	const camera = useThree((s) => s.camera);
	useFrame(() => {
		camera.position.set(...position);
		camera.lookAt(...lookAt);
		if (fov !== undefined && 'fov' in camera && camera.fov !== fov) {
			camera.fov = fov;
			camera.updateProjectionMatrix();
		}
	}, -1);
	return null;
};

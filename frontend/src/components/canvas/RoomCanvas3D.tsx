import React, { useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, Html } from '@react-three/drei';
import * as THREE from 'three';
import { LayoutItem } from '../../types';
import { ProceduralFurnitureMesh } from './ProceduralFurnitureMesh';
import { Layers, Eye, Smartphone, AlertCircle, RotateCcw } from 'lucide-react';

interface RoomCanvas3DProps {
  width?: number;
  length?: number;
  height?: number;
  items: LayoutItem[];
  selectedItemId?: string | null;
  onSelectItem: (itemId: string | null) => void;
  onMoveItem?: (itemId: string, newPos: { x: number; z: number }) => void;
}

const RoomEnclosure: React.FC<{ width: number; length: number; height: number }> = ({
  width,
  length,
  height,
}) => {
  const wallThickness = 0.08;
  const halfW = width / 2;
  const halfL = length / 2;

  return (
    <group>
      {/* Floor with parquet tint */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
        <planeGeometry args={[width, length]} />
        <meshStandardMaterial color="#EAE4D8" roughness={0.6} />
      </mesh>

      {/* Floor measurement grid */}
      <Grid
        position={[0, 0.001, 0]}
        args={[width, length]}
        cellSize={0.5}
        cellThickness={0.8}
        cellColor="#D6CEC0"
        sectionSize={1.0}
        sectionThickness={1.2}
        sectionColor="#B5A995"
        fadeDistance={20}
      />

      {/* Back Wall */}
      <mesh position={[0, height / 2, -halfL - wallThickness / 2]} receiveShadow>
        <boxGeometry args={[width + wallThickness * 2, height, wallThickness]} />
        <meshStandardMaterial color="#F4F1EA" roughness={0.9} />
      </mesh>

      {/* Left Wall */}
      <mesh position={[-halfW - wallThickness / 2, height / 2, 0]} receiveShadow>
        <boxGeometry args={[wallThickness, height, length]} />
        <meshStandardMaterial color="#F7F5F0" roughness={0.9} />
      </mesh>

      {/* Floor Baseboards */}
      <mesh position={[0, 0.05, -halfL + 0.01]}>
        <boxGeometry args={[width, 0.1, 0.02]} />
        <meshStandardMaterial color="#D9D2C5" />
      </mesh>
    </group>
  );
};

export const RoomCanvas3D: React.FC<RoomCanvas3DProps> = ({
  width = 4.0,
  length = 5.0,
  height = 2.8,
  items,
  selectedItemId,
  onSelectItem,
}) => {
  const [isFloorPlanView, setIsFloorPlanView] = useState(false);
  const [showARModal, setShowARModal] = useState(false);
  const [hasWebXRSupport, setHasWebXRSupport] = useState<boolean | null>(null);

  const checkWebXR = async () => {
    if ('xr' in navigator && (navigator as any).xr?.isSessionSupported) {
      try {
        const supported = await (navigator as any).xr.isSessionSupported('immersive-ar');
        setHasWebXRSupport(supported);
      } catch {
        setHasWebXRSupport(false);
      }
    } else {
      setHasWebXRSupport(false);
    }
    setShowARModal(true);
  };

  return (
    <div className="relative w-full h-[540px] lg:h-[620px] rounded-2xl overflow-hidden shadow-lg border border-warm-border bg-[#F5F2EB]">
      {/* 3D Canvas */}
      <Canvas
        shadows
        camera={{
          position: isFloorPlanView ? [0, 8, 0] : [0, 4.5, 6],
          fov: isFloorPlanView ? 35 : 45,
        }}
      >
        <ambientLight intensity={0.7} />
        <directionalLight
          position={[5, 8, 4]}
          intensity={1.2}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-camera-near={0.5}
          shadow-camera-far={20}
          shadow-camera-left={-4}
          shadow-camera-right={4}
          shadow-camera-top={4}
          shadow-camera-bottom={-4}
        />
        <pointLight position={[-3, 3, -2]} intensity={0.4} color="#FFF5E0" />

        {/* Room Architectural Structure */}
        <RoomEnclosure width={width} length={length} height={height} />

        {/* Furniture Objects */}
        {items.map((item, index) => {
          const furn = item.furniture;
          const itemId = item.id || `item-${index}`;
          const isSelected = selectedItemId === itemId;

          return (
            <group
              key={itemId}
              position={[item.pos_x, item.pos_y, item.pos_z]}
              rotation={[0, item.rot_y, 0]}
              scale={[item.scale_x || 1, item.scale_y || 1, item.scale_z || 1]}
              onClick={(e) => {
                e.stopPropagation();
                onSelectItem(itemId);
              }}
            >
              <ProceduralFurnitureMesh
                category={furn?.category || 'chair'}
                width={furn?.width_m || 1.0}
                height={furn?.height_m || 0.8}
                depth={furn?.depth_m || 0.8}
                colorHex={furn?.color_hex || '#5E7363'}
                isSelected={isSelected}
              />

              {/* Selection Halo / Label */}
              {isSelected && (
                <Html position={[0, (furn?.height_m || 0.8) + 0.25, 0]} center>
                  <div className="bg-charcoal text-white text-[11px] font-medium px-2.5 py-1 rounded-full shadow-lg pointer-events-none whitespace-nowrap border border-white/20">
                    {furn?.name || 'Selected Object'}
                  </div>
                </Html>
              )}
            </group>
          );
        })}

        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          maxPolarAngle={isFloorPlanView ? 0.01 : Math.PI / 2 - 0.05}
          minDistance={2}
          maxDistance={14}
        />
      </Canvas>

      {/* Floating Toolbar Controls */}
      <div className="absolute top-4 left-4 flex gap-2">
        <button
          onClick={() => setIsFloorPlanView(!isFloorPlanView)}
          className={`px-3.5 py-2 rounded-xl text-xs font-medium flex items-center gap-1.5 transition-all shadow-sm ${
            isFloorPlanView
              ? 'bg-sage-600 text-white shadow-sage-200'
              : 'bg-white/90 text-charcoal hover:bg-white border border-warm-border'
          }`}
          title="Toggle Top-Down / Isometric 3D View"
        >
          {isFloorPlanView ? <Eye className="w-3.5 h-3.5" /> : <Layers className="w-3.5 h-3.5" />}
          {isFloorPlanView ? '3D Orbit View' : 'Overhead Floor Plan'}
        </button>

        <button
          onClick={checkWebXR}
          className="px-3.5 py-2 rounded-xl text-xs font-medium flex items-center gap-1.5 bg-white/90 text-charcoal hover:bg-white border border-warm-border shadow-sm transition-all"
        >
          <Smartphone className="w-3.5 h-3.5 text-sage-600" />
          AR Preview
        </button>
      </div>

      {/* Room Dimensions Overlay */}
      <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-warm-border text-[11px] font-medium text-charcoal-muted shadow-sm">
        Room: <span className="text-charcoal font-semibold">{width.toFixed(1)}m × {length.toFixed(1)}m</span> (H: {height.toFixed(1)}m)
      </div>

      {/* AR Compatibility & WebXR Modal */}
      {showARModal && (
        <div className="absolute inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-warm-border">
            <div className="flex items-center gap-3 mb-3 text-sage-700">
              <Smartphone className="w-6 h-6" />
              <h3 className="font-semibold text-lg text-charcoal">Augmented Reality Mode</h3>
            </div>
            
            <p className="text-sm text-charcoal-muted leading-relaxed mb-4">
              {hasWebXRSupport ? (
                <span className="text-emerald-700 font-medium">
                  WebXR immersive-ar session is supported on this browser device. You can launch real-time surface detection camera streaming.
                </span>
              ) : (
                <span>
                  Notice: True camera-based AR requires a mobile device with ARCore (Android) or ARKit (iOS) and a supported WebXR / WebGL browser environment. Desktop browsers operate in interactive 3D simulation mode.
                </span>
              )}
            </p>

            <div className="p-3 bg-sage-50 rounded-xl border border-sage-100 text-xs text-charcoal-light mb-5">
              <div className="flex items-start gap-2">
                <AlertCircle className="w-4 h-4 text-sage-600 shrink-0 mt-0.5" />
                <span>
                  <strong>Architecture Note:</strong> Full metrically accurate camera scanning connects to mobile client bridges (Unity AR Foundation or WebXR session). The 3D room viewer above functions as your interactive layout workstation.
                </span>
              </div>
            </div>

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowARModal(false)}
                className="px-4 py-2 text-xs font-medium rounded-xl border border-warm-border text-charcoal hover:bg-neutral-50"
              >
                Close & Return to 3D View
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { ProceduralFurnitureMesh } from './canvas/ProceduralFurnitureMesh';
import { FurnitureItem } from '../types';
import { Box, Sparkles, Eye, Layers } from 'lucide-react';
import { resolveImageUrl } from '../utils/image';

interface FurnitureVisualPreviewProps {
  item: FurnitureItem;
  className?: string;
  interactive?: boolean;
}

// Category-specific architectural vector illustration fallback for non-WebGL environments
export const CategoryVectorIllustration: React.FC<{
  category: string;
  colorHex: string;
  name: string;
}> = ({ category, colorHex, name }) => {
  const cat = category.toLowerCase();
  const c = colorHex || '#6B7C6E';

  if (cat.includes('sofa') || cat.includes('loveseat')) {
    return (
      <svg viewBox="0 0 160 120" className="w-28 h-20 drop-shadow-md" fill="none">
        {/* Shadow */}
        <ellipse cx="80" cy="108" rx="60" ry="8" fill="rgba(0,0,0,0.08)" />
        {/* Legs */}
        <rect x="32" y="94" width="6" height="12" rx="2" fill="#8A624A" />
        <rect x="122" y="94" width="6" height="12" rx="2" fill="#8A624A" />
        {/* Base Cushion */}
        <rect x="24" y="68" width="112" height="28" rx="8" fill={c} />
        {/* Backrest */}
        <rect x="30" y="32" width="100" height="38" rx="10" fill={c} opacity="0.9" />
        {/* Left Armrest */}
        <rect x="18" y="52" width="16" height="42" rx="6" fill={c} opacity="0.95" />
        {/* Right Armrest */}
        <rect x="126" y="52" width="16" height="42" rx="6" fill={c} opacity="0.95" />
        {/* Cushion Seams */}
        <line x1="80" y1="68" x2="80" y2="96" stroke="rgba(255,255,255,0.3)" strokeWidth="2" />
      </svg>
    );
  }

  if (cat.includes('bed')) {
    return (
      <svg viewBox="0 0 160 120" className="w-28 h-20 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="110" rx="55" ry="7" fill="rgba(0,0,0,0.08)" />
        {/* Headboard */}
        <rect x="25" y="24" width="110" height="40" rx="6" fill={c} />
        {/* Mattress Base */}
        <rect x="28" y="58" width="104" height="46" rx="8" fill="#EAE5DC" />
        {/* Folded Duvet / Blanket */}
        <rect x="28" y="74" width="104" height="30" rx="6" fill={c} opacity="0.85" />
        {/* Pillows */}
        <rect x="38" y="44" width="38" height="20" rx="5" fill="#FFFFFF" stroke="#D1D5DB" strokeWidth="1" />
        <rect x="84" y="44" width="38" height="20" rx="5" fill="#FFFFFF" stroke="#D1D5DB" strokeWidth="1" />
      </svg>
    );
  }

  if (cat.includes('armchair')) {
    return (
      <svg viewBox="0 0 160 120" className="w-24 h-20 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="108" rx="40" ry="6" fill="rgba(0,0,0,0.08)" />
        <rect x="50" y="96" width="5" height="12" rx="2" fill="#8A624A" />
        <rect x="105" y="96" width="5" height="12" rx="2" fill="#8A624A" />
        <rect x="42" y="66" width="76" height="30" rx="8" fill={c} />
        <rect x="48" y="30" width="64" height="40" rx="10" fill={c} opacity="0.9" />
        <rect x="36" y="52" width="14" height="42" rx="6" fill={c} opacity="0.95" />
        <rect x="110" y="52" width="14" height="42" rx="6" fill={c} opacity="0.95" />
      </svg>
    );
  }

  if (cat.includes('table') || cat.includes('desk')) {
    return (
      <svg viewBox="0 0 160 120" className="w-28 h-20 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="110" rx="50" ry="6" fill="rgba(0,0,0,0.08)" />
        {/* Legs */}
        <rect x="36" y="55" width="6" height="52" rx="2" fill="#4B5563" />
        <rect x="118" y="55" width="6" height="52" rx="2" fill="#4B5563" />
        <rect x="52" y="55" width="6" height="48" rx="2" fill="#4B5563" opacity="0.7" />
        <rect x="102" y="55" width="6" height="48" rx="2" fill="#4B5563" opacity="0.7" />
        {/* Table Top */}
        <rect x="25" y="44" width="110" height="14" rx="4" fill={c} />
      </svg>
    );
  }

  if (cat.includes('wardrobe') || cat.includes('bookshelf') || cat.includes('storage')) {
    return (
      <svg viewBox="0 0 160 120" className="w-24 h-24 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="114" rx="45" ry="6" fill="rgba(0,0,0,0.08)" />
        <rect x="40" y="16" width="80" height="96" rx="4" fill={c} />
        <line x1="80" y1="18" x2="80" y2="110" stroke="#FFFFFF" strokeWidth="2" opacity="0.6" />
        <circle cx="74" cy="64" r="3" fill="#D1D5DB" />
        <circle cx="86" cy="64" r="3" fill="#D1D5DB" />
      </svg>
    );
  }

  if (cat.includes('lamp')) {
    return (
      <svg viewBox="0 0 160 120" className="w-20 h-24 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="112" rx="25" ry="5" fill="rgba(0,0,0,0.1)" />
        <line x1="80" y1="40" x2="80" y2="110" stroke="#374151" strokeWidth="4" />
        <polygon points="60,40 100,40 112,65 48,65" fill={c} />
      </svg>
    );
  }

  if (cat.includes('plant')) {
    return (
      <svg viewBox="0 0 160 120" className="w-20 h-24 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="112" rx="22" ry="5" fill="rgba(0,0,0,0.1)" />
        {/* Pot */}
        <polygon points="64,80 96,80 90,110 70,110" fill="#B45309" />
        {/* Foliage */}
        <circle cx="80" cy="60" r="22" fill="#2E7D32" />
        <circle cx="68" cy="48" r="16" fill="#388E3C" />
        <circle cx="92" cy="48" r="16" fill="#43A047" />
        <circle cx="80" cy="36" r="14" fill="#4CAF50" />
      </svg>
    );
  }

  if (cat.includes('rug')) {
    return (
      <svg viewBox="0 0 160 120" className="w-32 h-16 drop-shadow-md" fill="none">
        <ellipse cx="80" cy="60" rx="65" ry="25" fill={c} stroke="#FFFFFF" strokeWidth="3" strokeDasharray="6 4" />
        <ellipse cx="80" cy="60" rx="45" ry="16" fill="rgba(255,255,255,0.2)" />
      </svg>
    );
  }

  // Default elegant architectural box
  return (
    <svg viewBox="0 0 160 120" className="w-24 h-20 drop-shadow-md" fill="none">
      <ellipse cx="80" cy="105" rx="40" ry="6" fill="rgba(0,0,0,0.08)" />
      <polygon points="80,30 130,55 80,80 30,55" fill={c} />
      <polygon points="30,55 80,80 80,105 30,80" fill={c} opacity="0.85" />
      <polygon points="130,55 80,80 80,105 130,80" fill={c} opacity="0.7" />
    </svg>
  );
};

export const FurnitureVisualPreview: React.FC<FurnitureVisualPreviewProps> = ({
  item,
  className = 'h-48',
  interactive = true,
}) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [viewMode, setViewMode] = useState<'image' | '3d'>('image');

  const resolvedUrl = item.image_url ? resolveImageUrl(item.image_url) : null;
  // If item has valid image_url and hasn't errored, prefer image when in 'image' mode
  const showImage = Boolean(resolvedUrl && !imageError && viewMode === 'image');

  return (
    <div
      className={`relative w-full ${className} overflow-hidden rounded-t-2xl flex items-center justify-center transition-all group select-none`}
      style={{
        backgroundColor: `${item.color_hex}14`,
      }}
    >
      {/* Real Image / Vector Illustration Mode */}
      {showImage ? (
        <div className="relative w-full h-full flex items-center justify-center bg-white/40">
          {!imageLoaded && (
            <div className="absolute inset-0 bg-neutral-100/80 animate-pulse flex items-center justify-center">
              <Box className="w-6 h-6 text-charcoal-muted opacity-30" />
            </div>
          )}
          <img
            src={resolvedUrl!}
            alt={`${item.name} - ${item.category} interior design model`}
            loading="lazy"
            onLoad={() => setImageLoaded(true)}
            onError={() => {
              setImageError(true);
              setViewMode('3d');
            }}
            className={`w-full h-full object-contain p-3 transition-opacity duration-300 ${
              imageLoaded ? 'opacity-100' : 'opacity-0'
            }`}
          />
        </div>
      ) : (
        /* Real-Time Interactive 3D WebGL / Vector Preview */
        <div className="relative w-full h-full flex items-center justify-center">
          <div className="w-full h-full absolute inset-0 cursor-grab active:cursor-grabbing">
            <Suspense
              fallback={
                <div className="w-full h-full flex items-center justify-center">
                  <CategoryVectorIllustration
                    category={item.category}
                    colorHex={item.color_hex}
                    name={item.name}
                  />
                </div>
              }
            >
              <Canvas
                shadows
                camera={{ position: [1.8, 1.4, 1.8], fov: 42 }}
                gl={{ antialias: true, alpha: true }}
                style={{ pointerEvents: interactive ? 'auto' : 'none' }}
              >
                <ambientLight intensity={0.9} />
                <directionalLight position={[4, 6, 3]} intensity={1.3} castShadow shadow-mapSize={512} />
                <directionalLight position={[-3, 2, -3]} intensity={0.4} />

                {/* Centered Furniture Object */}
                <group position={[0, -0.35, 0]}>
                  <ProceduralFurnitureMesh
                    category={item.category}
                    width={item.width_m}
                    height={item.height_m}
                    depth={item.depth_m}
                    colorHex={item.color_hex}
                    isSelected={false}
                  />
                  {/* Subtle Ground Shadow Plane */}
                  <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]} receiveShadow>
                    <planeGeometry args={[3, 3]} />
                    <shadowMaterial opacity={0.15} />
                  </mesh>
                </group>
              </Canvas>
            </Suspense>
          </div>

          {/* 3D Live Indicator Pill */}
          <div className="absolute bottom-2.5 right-2.5 z-10 bg-white/95 backdrop-blur-xs px-2 py-0.5 rounded-full border border-warm-border text-[9px] font-semibold text-charcoal flex items-center gap-1 shadow-2xs pointer-events-none">
            <Sparkles className="w-2.5 h-2.5 text-sage-600" />
            <span>3D Procedural</span>
          </div>
        </div>
      )}

      {/* Category Pill Top Left */}
      <div className="absolute top-2.5 left-2.5 z-10 bg-white/95 backdrop-blur-xs text-[10px] font-semibold px-2.5 py-1 rounded-md text-charcoal border border-warm-border shadow-2xs">
        {item.category}
      </div>

      {/* Style Pill & Mode Toggle Top Right */}
      <div className="absolute top-2.5 right-2.5 z-10 flex items-center gap-1.5">
        <span className="bg-sage-50/95 backdrop-blur-xs text-[10px] font-semibold px-2 py-0.5 rounded-md text-sage-700 border border-sage-200">
          {item.style}
        </span>

        {/* 3D / Image Toggle button */}
        {resolvedUrl && !imageError && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setViewMode(viewMode === 'image' ? '3d' : 'image');
            }}
            title={viewMode === 'image' ? 'Switch to 3D View' : 'Switch to Image View'}
            className="p-1 rounded-md bg-white/95 hover:bg-neutral-100 text-charcoal-muted hover:text-charcoal border border-warm-border shadow-2xs transition-all"
          >
            {viewMode === 'image' ? (
              <Box className="w-3.5 h-3.5 text-sage-600" />
            ) : (
              <Eye className="w-3.5 h-3.5 text-charcoal" />
            )}
          </button>
        )}
      </div>
    </div>
  );
};


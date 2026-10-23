import React from 'react';
import * as THREE from 'three';

interface ProceduralFurnitureMeshProps {
  category: string;
  width?: number;
  height?: number;
  depth?: number;
  colorHex?: string;
  isSelected?: boolean;
}

export const ProceduralFurnitureMesh: React.FC<ProceduralFurnitureMeshProps> = ({
  category,
  width = 1.0,
  height = 0.8,
  depth = 0.8,
  colorHex = '#5E7363',
  isSelected = false,
}) => {
  const primaryColor = isSelected ? '#A3B899' : colorHex;
  const woodColor = '#8A624A';
  const metallicColor = '#3A3A3A';
  const fabricColor = isSelected ? '#D4E2D4' : '#E8E3D8';

  const cat = category.toLowerCase();

  // 1. SOFA
  if (cat.includes('sofa') || cat.includes('loveseat')) {
    const seatH = height * 0.45;
    return (
      <group>
        {/* Base / Cushion */}
        <mesh position={[0, seatH / 2, 0]} castShadow receiveShadow>
          <boxGeometry args={[width * 0.95, seatH * 0.8, depth * 0.85]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Backrest */}
        <mesh position={[0, height * 0.65, -depth * 0.35]} castShadow>
          <boxGeometry args={[width * 0.95, height * 0.6, depth * 0.22]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Left Armrest */}
        <mesh position={[-width * 0.45, height * 0.45, 0]} castShadow>
          <boxGeometry args={[width * 0.12, height * 0.5, depth * 0.88]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Right Armrest */}
        <mesh position={[width * 0.45, height * 0.45, 0]} castShadow>
          <boxGeometry args={[width * 0.12, height * 0.5, depth * 0.88]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* 4 Wooden Legs */}
        {[-width * 0.4, width * 0.4].map((lx) =>
          [-depth * 0.35, depth * 0.35].map((lz) => (
            <mesh key={`${lx}-${lz}`} position={[lx, 0.05, lz]} castShadow>
              <cylinderGeometry args={[0.03, 0.02, 0.1, 8]} />
              <meshStandardMaterial color={woodColor} roughness={0.4} />
            </mesh>
          ))
        )}
      </group>
    );
  }

  // 2. BED
  if (cat.includes('bed')) {
    const frameH = 0.3;
    const mattressH = 0.25;
    return (
      <group>
        {/* Wooden Frame */}
        <mesh position={[0, frameH / 2, 0]} castShadow receiveShadow>
          <boxGeometry args={[width, frameH, depth]} />
          <meshStandardMaterial color={woodColor} roughness={0.5} />
        </mesh>
        {/* Mattress */}
        <mesh position={[0, frameH + mattressH / 2, 0.05]} castShadow>
          <boxGeometry args={[width * 0.92, mattressH, depth * 0.9]} />
          <meshStandardMaterial color={fabricColor} roughness={0.9} />
        </mesh>
        {/* Headboard */}
        <mesh position={[0, height * 0.55, -depth / 2 + 0.05]} castShadow>
          <boxGeometry args={[width * 1.02, height * 0.7, 0.1]} />
          <meshStandardMaterial color={primaryColor} roughness={0.6} />
        </mesh>
        {/* Two Pillows */}
        {[-width * 0.24, width * 0.24].map((px) => (
          <mesh key={px} position={[px, frameH + mattressH + 0.06, -depth * 0.32]} castShadow>
            <boxGeometry args={[width * 0.35, 0.1, depth * 0.2]} />
            <meshStandardMaterial color="#FFFFFF" roughness={0.9} />
          </mesh>
        ))}
      </group>
    );
  }

  // 3. ARMCHAIR
  if (cat.includes('armchair')) {
    return (
      <group>
        <mesh position={[0, height * 0.35, 0]} castShadow>
          <boxGeometry args={[width * 0.85, height * 0.3, depth * 0.8]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Backrest */}
        <mesh position={[0, height * 0.65, -depth * 0.28]} castShadow>
          <boxGeometry args={[width * 0.85, height * 0.6, depth * 0.2]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Armrests */}
        <mesh position={[-width * 0.4, height * 0.5, 0]} castShadow>
          <boxGeometry args={[width * 0.12, height * 0.35, depth * 0.7]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        <mesh position={[width * 0.4, height * 0.5, 0]} castShadow>
          <boxGeometry args={[width * 0.12, height * 0.35, depth * 0.7]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Legs */}
        {[-width * 0.35, width * 0.35].map((lx) =>
          [-depth * 0.3, depth * 0.3].map((lz) => (
            <mesh key={`${lx}-${lz}`} position={[lx, height * 0.1, lz]} castShadow>
              <cylinderGeometry args={[0.025, 0.015, height * 0.2, 8]} />
              <meshStandardMaterial color={woodColor} roughness={0.4} />
            </mesh>
          ))
        )}
      </group>
    );
  }

  // 4. DINING TABLE / DESK
  if (cat.includes('table') || cat.includes('desk')) {
    const topH = 0.05;
    const legH = height - topH;
    return (
      <group>
        {/* Table Top */}
        <mesh position={[0, height - topH / 2, 0]} castShadow receiveShadow>
          <boxGeometry args={[width, topH, depth]} />
          <meshStandardMaterial color={cat.includes('desk') ? metallicColor : woodColor} roughness={0.4} />
        </mesh>
        {/* 4 Sturdy Legs */}
        {[-width / 2 + 0.08, width / 2 - 0.08].map((lx) =>
          [-depth / 2 + 0.08, depth / 2 - 0.08].map((lz) => (
            <mesh key={`${lx}-${lz}`} position={[lx, legH / 2, lz]} castShadow>
              <cylinderGeometry args={[0.035, 0.03, legH, 12]} />
              <meshStandardMaterial color={metallicColor} roughness={0.5} />
            </mesh>
          ))
        )}
      </group>
    );
  }

  // 5. CHAIR
  if (cat.includes('chair')) {
    const seatY = height * 0.5;
    return (
      <group>
        {/* Seat */}
        <mesh position={[0, seatY, 0]} castShadow>
          <boxGeometry args={[width * 0.85, 0.06, depth * 0.85]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Backrest */}
        <mesh position={[0, height * 0.75, -depth * 0.35]} castShadow>
          <boxGeometry args={[width * 0.8, height * 0.45, 0.05]} />
          <meshStandardMaterial color={primaryColor} roughness={0.7} />
        </mesh>
        {/* Legs */}
        {[-width * 0.35, width * 0.35].map((lx) =>
          [-depth * 0.35, depth * 0.35].map((lz) => (
            <mesh key={`${lx}-${lz}`} position={[lx, seatY / 2, lz]} castShadow>
              <cylinderGeometry args={[0.02, 0.015, seatY, 8]} />
              <meshStandardMaterial color={metallicColor} roughness={0.4} />
            </mesh>
          ))
        )}
      </group>
    );
  }

  // 6. WARDROBE
  if (cat.includes('wardrobe')) {
    return (
      <group>
        <mesh position={[0, height / 2, 0]} castShadow receiveShadow>
          <boxGeometry args={[width, height, depth]} />
          <meshStandardMaterial color={primaryColor} roughness={0.5} />
        </mesh>
        {/* Handle details */}
        <mesh position={[0.05, height * 0.5, depth / 2 + 0.02]}>
          <cylinderGeometry args={[0.01, 0.01, 0.3, 8]} />
          <meshStandardMaterial color={metallicColor} metalness={0.8} />
        </mesh>
      </group>
    );
  }

  // 7. TV UNIT
  if (cat.includes('tv unit') || cat.includes('tv')) {
    return (
      <group>
        <mesh position={[0, height / 2, 0]} castShadow receiveShadow>
          <boxGeometry args={[width, height, depth]} />
          <meshStandardMaterial color={woodColor} roughness={0.4} />
        </mesh>
        {/* Media shelf accent line */}
        <mesh position={[0, height * 0.5, depth / 2 + 0.01]}>
          <boxGeometry args={[width * 0.9, height * 0.35, 0.02]} />
          <meshStandardMaterial color="#2E332F" roughness={0.8} />
        </mesh>
      </group>
    );
  }

  // 8. BOOKSHELF
  if (cat.includes('bookshelf')) {
    return (
      <group>
        <mesh position={[0, height / 2, 0]} castShadow receiveShadow>
          <boxGeometry args={[width, height, depth]} />
          <meshStandardMaterial color={metallicColor} roughness={0.6} />
        </mesh>
        {/* Open Shelves lines */}
        {[0.25, 0.5, 0.75].map((pct) => (
          <mesh key={pct} position={[0, height * pct, 0.02]}>
            <boxGeometry args={[width * 0.92, 0.03, depth * 0.95]} />
            <meshStandardMaterial color={woodColor} roughness={0.4} />
          </mesh>
        ))}
      </group>
    );
  }

  // 9. FLOOR LAMP
  if (cat.includes('lamp')) {
    return (
      <group>
        {/* Base */}
        <mesh position={[0, 0.02, 0]} castShadow>
          <cylinderGeometry args={[width * 0.4, width * 0.45, 0.04, 16]} />
          <meshStandardMaterial color={metallicColor} metalness={0.7} />
        </mesh>
        {/* Stem */}
        <mesh position={[0, height * 0.5, 0]} castShadow>
          <cylinderGeometry args={[0.02, 0.02, height * 0.9, 12]} />
          <meshStandardMaterial color={metallicColor} metalness={0.7} />
        </mesh>
        {/* Shade with warm light simulation */}
        <mesh position={[0, height * 0.92, 0]} castShadow>
          <cylinderGeometry args={[0.18, 0.28, 0.3, 16]} />
          <meshStandardMaterial color="#FFF8E7" emissive="#FFEBB0" emissiveIntensity={0.6} />
        </mesh>
      </group>
    );
  }

  // 10. PLANT
  if (cat.includes('plant')) {
    return (
      <group>
        {/* Ceramic Pot */}
        <mesh position={[0, height * 0.2, 0]} castShadow receiveShadow>
          <cylinderGeometry args={[width * 0.45, width * 0.35, height * 0.4, 16]} />
          <meshStandardMaterial color="#EAE5DC" roughness={0.3} />
        </mesh>
        {/* Stem and Foliage */}
        <mesh position={[0, height * 0.65, 0]} castShadow>
          <sphereGeometry args={[width * 0.48, 12, 12]} />
          <meshStandardMaterial color="#3C6B46" roughness={0.8} />
        </mesh>
      </group>
    );
  }

  // 11. RUG
  if (cat.includes('rug')) {
    return (
      <mesh position={[0, 0.005, 0]} receiveShadow>
        <boxGeometry args={[width, 0.01, depth]} />
        <meshStandardMaterial color="#DED6C7" roughness={0.95} />
      </mesh>
    );
  }

  // Generic fallback geometric box
  return (
    <mesh position={[0, height / 2, 0]} castShadow receiveShadow>
      <boxGeometry args={[width, height, depth]} />
      <meshStandardMaterial color={primaryColor} roughness={0.5} />
    </mesh>
  );
};

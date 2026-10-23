export const CANONICAL_ROOM_TYPES = [
  'Bathroom',
  'Bedroom',
  'DiningRoom',
  'HomeOffice',
  'Kitchen',
  'LivingRoom',
] as const;

export type CanonicalRoomType = typeof CANONICAL_ROOM_TYPES[number];

export const ROOM_TYPE_LABELS: Record<string, string> = {
  Bathroom: 'Bathroom',
  Bedroom: 'Bedroom',
  DiningRoom: 'Dining Room',
  HomeOffice: 'Home Office',
  Kitchen: 'Kitchen',
  LivingRoom: 'Living Room',
  Other: 'Other'
};

export function formatRoomTypeLabel(roomType?: string | null): string {
  if (!roomType) return 'Unknown';
  return ROOM_TYPE_LABELS[roomType] || roomType.replace(/([A-Z])/g, ' $1').trim();
}

/**
 * Normalizes user, query parameter, or prediction room strings
 * (e.g. 'dining_room', 'dining room', 'Bedroom', 'office')
 * into the canonical PascalCase room typology name.
 */
export function normalizeRoomType(roomType?: string | null): string {
  if (!roomType) return 'all';
  const clean = roomType.trim().toLowerCase().replace(/[\s\-_]/g, '');
  if (clean === 'all' || clean === '*' || clean === '') return 'all';
  if (clean === 'bathroom') return 'Bathroom';
  if (clean === 'bedroom') return 'Bedroom';
  if (clean === 'dining' || clean === 'diningroom') return 'DiningRoom';
  if (clean === 'homeoffice' || clean === 'office') return 'HomeOffice';
  if (clean === 'kitchen') return 'Kitchen';
  if (clean === 'living' || clean === 'livingroom') return 'LivingRoom';
  return 'all';
}

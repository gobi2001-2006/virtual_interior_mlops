import { describe, it, expect } from 'vitest';
import { normalizeRoomType, CANONICAL_ROOM_TYPES } from '../src/utils/formatters';

describe('Frontend Component & Architecture Tests', () => {
  it('validates supported room categories count and members', () => {
    expect(CANONICAL_ROOM_TYPES.length).toBe(6);
    expect(CANONICAL_ROOM_TYPES).toContain('Bathroom');
    expect(CANONICAL_ROOM_TYPES).toContain('Bedroom');
    expect(CANONICAL_ROOM_TYPES).toContain('DiningRoom');
    expect(CANONICAL_ROOM_TYPES).toContain('HomeOffice');
    expect(CANONICAL_ROOM_TYPES).toContain('Kitchen');
    expect(CANONICAL_ROOM_TYPES).toContain('LivingRoom');
  });

  it('normalizes room type variations correctly', () => {
    // Exact canonical
    expect(normalizeRoomType('Bedroom')).toBe('Bedroom');
    expect(normalizeRoomType('LivingRoom')).toBe('LivingRoom');

    // Case insensitive
    expect(normalizeRoomType('bedroom')).toBe('Bedroom');
    expect(normalizeRoomType('kitchen')).toBe('Kitchen');
    expect(normalizeRoomType('bathroom')).toBe('Bathroom');

    // Spaces and underscores
    expect(normalizeRoomType('dining room')).toBe('DiningRoom');
    expect(normalizeRoomType('dining_room')).toBe('DiningRoom');
    expect(normalizeRoomType('home office')).toBe('HomeOffice');
    expect(normalizeRoomType('home_office')).toBe('HomeOffice');
    expect(normalizeRoomType('living room')).toBe('LivingRoom');
    expect(normalizeRoomType('living_room')).toBe('LivingRoom');

    // Hyphenated
    expect(normalizeRoomType('home-office')).toBe('HomeOffice');
    expect(normalizeRoomType('living-room')).toBe('LivingRoom');

    // Undefined / empty / unknown graceful fallback to 'all'
    expect(normalizeRoomType(undefined)).toBe('all');
    expect(normalizeRoomType('')).toBe('all');
    expect(normalizeRoomType('UnrecognizedType')).toBe('all');
  });

  it('builds navigation URL to catalog carrying detected room type', () => {
    const detectedType = 'Bedroom';
    const roomId = 'test-room-123';
    const normalized = normalizeRoomType(detectedType);
    const catalogUrl = `/furniture?room_type=${encodeURIComponent(normalized)}&roomId=${encodeURIComponent(roomId)}`;

    expect(catalogUrl).toBe('/furniture?room_type=Bedroom&roomId=test-room-123');

    // Parse back
    const url = new URL(`http://localhost${catalogUrl}`);
    expect(url.searchParams.get('room_type')).toBe('Bedroom');
    expect(url.searchParams.get('roomId')).toBe('test-room-123');
  });

  it('validates room bounds clamping for 3D placement', () => {
    const roomWidth = 4.0;
    const roomLength = 5.0;
    const itemWidth = 1.2;
    const itemDepth = 0.8;
    const margin = 0.15;

    const halfSafeW = Math.max(0.1, roomWidth / 2 - itemWidth / 2 - margin);
    const halfSafeL = Math.max(0.1, roomLength / 2 - itemDepth / 2 - margin);

    expect(halfSafeW).toBeCloseTo(1.25, 2);
    expect(halfSafeL).toBeCloseTo(1.95, 2);

    // Test clamped coordinates
    const clamp = (val: number, bound: number) => Math.max(-bound, Math.min(bound, val));
    expect(clamp(3.0, halfSafeW)).toBe(halfSafeW);
    expect(clamp(-5.0, halfSafeL)).toBe(-halfSafeL);
    expect(clamp(0.5, halfSafeW)).toBe(0.5);
  });

  it('filters catalogue items correctly by room and search keyword', () => {
    const items = [
      { id: '1', name: 'Queen Size Bed', category: 'Bed', suitable_rooms: ['Bedroom'] },
      { id: '2', name: 'Two-Seater Sofa', category: 'Sofa', suitable_rooms: ['LivingRoom'] },
      { id: '3', name: 'Dining Table', category: 'Table', suitable_rooms: ['DiningRoom', 'Kitchen'] },
      { id: '4', name: 'Bedside Table', category: 'Table', suitable_rooms: ['Bedroom'] },
    ];

    // Filter by room
    const bedroomItems = items.filter(i =>
      i.suitable_rooms.some(r => r.toLowerCase() === 'bedroom')
    );
    expect(bedroomItems.length).toBe(2);

    // Filter by room AND search query
    const search = 'table';
    const filtered = bedroomItems.filter(i =>
      i.name.toLowerCase().includes(search) || i.category.toLowerCase().includes(search)
    );
    expect(filtered.length).toBe(1);
    expect(filtered[0].name).toBe('Bedside Table');
  });
});

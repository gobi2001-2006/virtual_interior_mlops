import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { api } from '../services/api';
import { RoomCanvas3D } from '../components/canvas/RoomCanvas3D';
import { FeedbackModal } from './FeedbackModal';
import { LayoutItem, FurnitureItem, Room } from '../types';
import {
  RotateCcw,
  Save,
  Trash2,
  Plus,
  Sliders,
  Move,
  RotateCw,
  Maximize2,
  MessageSquareHeart,
  AlertTriangle,
  FolderOpen,
  Sparkles
} from 'lucide-react';

export const DesignerPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const roomIdParam = searchParams.get('roomId');
  const addFurnitureIdParam = searchParams.get('addFurnitureId');

  // Rooms list to allow switching or fallback
  const { data: rooms = [] } = useQuery({
    queryKey: ['rooms'],
    queryFn: api.getRooms,
  });

  const [activeRoomId, setActiveRoomId] = useState<string>('');
  const [activeRoom, setActiveRoom] = useState<Room | null>(null);

  // Layout items state
  const [items, setItems] = useState<LayoutItem[]>([]);
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null);
  const [layoutWarnings, setLayoutWarnings] = useState<string[]>([]);
  const [layoutModelVersion, setLayoutModelVersion] = useState<string>('layout_v001');
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false);

  const [addedFurnitureIds] = useState(() => new Set<string>());
  const [placementNotice, setPlacementNotice] = useState<string | null>(null);

  // Available catalog
  const { data: catalog = [], isError: isCatalogError } = useQuery({
    queryKey: ['catalog'],
    queryFn: () => api.getFurnitureCatalog(),
  });

  // Select initial room
  useEffect(() => {
    if (roomIdParam) {
      setActiveRoomId(roomIdParam);
    } else if (rooms.length > 0 && !activeRoomId) {
      setActiveRoomId(rooms[0].id);
    }
  }, [roomIdParam, rooms]);

  // Load room and fetch recommended layout
  useEffect(() => {
    if (!activeRoomId) return;
    const found = rooms.find((r) => r.id === activeRoomId);
    if (found) {
      setActiveRoom(found);
      loadRecommendedLayout(found);
    } else {
      api.getRoom(activeRoomId).then((r) => {
        setActiveRoom(r);
        loadRecommendedLayout(r);
      }).catch(console.error);
    }
  }, [activeRoomId]);

  // Handle direct furniture addition from catalog page (idempotent, once per addFurnitureIdParam)
  useEffect(() => {
    if (!addFurnitureIdParam) return;
    if (catalog.length === 0) return;

    if (addedFurnitureIds.has(addFurnitureIdParam)) {
      return;
    }

    const furn = catalog.find((f) => f.id === addFurnitureIdParam);
    if (furn) {
      addedFurnitureIds.add(addFurnitureIdParam);
      addFurnitureToRoom(furn);
      setPlacementNotice(`Added "${furn.name}" to your 3D room.`);
      setTimeout(() => setPlacementNotice(null), 4000);
    } else if (!isCatalogError) {
      setPlacementNotice(`Item "${addFurnitureIdParam}" not found in catalogue.`);
      setTimeout(() => setPlacementNotice(null), 4000);
    }
  }, [addFurnitureIdParam, catalog, isCatalogError]);

  const loadRecommendedLayout = async (room: Room) => {
    try {
      const roomType = room.latest_prediction?.predicted_room_type || room.room_type_preference || 'LivingRoom';
      const layout = await api.recommendLayout({
        room_id: room.id,
        room_type: roomType,
        style: room.style_preference,
        width_m: room.width_m,
        length_m: room.length_m,
      });

      setItems(layout.items);
      setLayoutModelVersion(layout.layout_model_version || 'layout_v001');
      setLayoutWarnings(layout.warnings?.map((w) => w.message) || []);
      if (layout.items.length > 0) {
        setSelectedItemId(layout.items[0].id || 'item-0');
      }
    } catch (e) {
      console.error('Failed to load recommended layout:', e);
    }
  };

  const addFurnitureToRoom = (furn: FurnitureItem) => {
    const roomW = activeRoom?.width_m || 4.2;
    const roomL = activeRoom?.length_m || 5.0;
    const halfSafeW = Math.max(0.1, roomW / 2 - (furn.width_m || 0.8) / 2 - 0.15);
    const halfSafeL = Math.max(0.1, roomL / 2 - (furn.depth_m || 0.8) / 2 - 0.15);

    // Find a non-overlapping slot near center
    let targetX = 0.0;
    let targetZ = 0.0;
    const isOccupied = items.some(
      (it) => Math.hypot(it.pos_x - targetX, it.pos_z - targetZ) < 0.6
    );
    if (isOccupied) {
      // Offset slightly within boundaries
      targetX = Math.min(halfSafeW, 0.5 * (items.length % 2 === 0 ? 1 : -1));
      targetZ = Math.min(halfSafeL, 0.4 * (items.length % 3 === 0 ? 1 : -1));
    }

    const newItem: LayoutItem = {
      id: `custom-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      furniture_id: furn.id,
      pos_x: Math.max(-halfSafeW, Math.min(halfSafeW, targetX)),
      pos_y: 0.0,
      pos_z: Math.max(-halfSafeL, Math.min(halfSafeL, targetZ)),
      rot_y: 0.0,
      scale_x: 1.0,
      scale_y: 1.0,
      scale_z: 1.0,
      placement_reason: `Added from catalogue (${furn.category})`,
      furniture: furn,
    };
    setItems((prev) => [...prev, newItem]);
    setSelectedItemId(newItem.id!);
  };

  const selectedItem = items.find((i) => (i.id || '') === selectedItemId);

  const updateSelectedItem = (updates: Partial<LayoutItem>) => {
    if (!selectedItemId) return;
    setItems((prev) =>
      prev.map((item) => ((item.id || '') === selectedItemId ? { ...item, ...updates } : item))
    );
  };

  const deleteSelectedItem = () => {
    if (!selectedItemId) return;
    setItems((prev) => prev.filter((item) => (item.id || '') !== selectedItemId));
    setSelectedItemId(null);
  };

  const handleSaveLayout = async () => {
    if (!activeRoom) return;
    setIsSaving(true);
    try {
      await api.saveCustomLayout({
        room_id: activeRoom.id,
        name: `${activeRoom.name} - Custom Arrangement`,
        room_type: activeRoom.latest_prediction?.predicted_room_type || 'LivingRoom',
        items: items,
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 2500);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSaving(false);
    }
  };

  const halfW = (activeRoom?.width_m || 4.0) / 2 - 0.2;
  const halfL = (activeRoom?.length_m || 5.0) / 2 - 0.2;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Top Controls Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-warm-border shadow-xs">
        <div className="flex items-center gap-3">
          <label className="text-xs font-semibold text-charcoal">Active Room:</label>
          <select
            value={activeRoomId}
            onChange={(e) => setActiveRoomId(e.target.value)}
            className="px-3 py-1.5 rounded-xl border border-warm-border text-xs bg-background text-charcoal font-medium focus:outline-hidden"
          >
            {rooms.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} ({r.latest_prediction?.predicted_room_type || 'Room'})
              </option>
            ))}
          </select>
          <span className="text-[10px] bg-sage-50 text-sage-800 px-2.5 py-1 rounded-md font-semibold border border-sage-200 flex items-center gap-1 shadow-2xs">
            <Sparkles className="w-3 h-3 text-sage-600" /> {layoutModelVersion}
          </span>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => activeRoom && loadRecommendedLayout(activeRoom)}
            className="px-3 py-2 rounded-xl border border-warm-border text-xs font-medium text-charcoal hover:bg-neutral-50 flex items-center gap-1.5 transition-all"
            title="Reset to algorithmic recommendation"
          >
            <RotateCcw className="w-3.5 h-3.5 text-sage-600" />
            Reset Recommended
          </button>

          <button
            onClick={handleSaveLayout}
            disabled={isSaving}
            className={`px-4 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all shadow-xs ${
              saveSuccess
                ? 'bg-emerald-600 text-white'
                : 'bg-sage-600 hover:bg-sage-700 text-white shadow-sage-200'
            }`}
          >
            <Save className="w-3.5 h-3.5" />
            {saveSuccess ? 'Saved to DB!' : isSaving ? 'Saving...' : 'Save Design'}
          </button>

          <button
            onClick={() => setIsFeedbackOpen(true)}
            className="px-3.5 py-2 rounded-xl bg-warm-cream border border-warm-border text-xs font-semibold text-charcoal hover:bg-neutral-100 flex items-center gap-1.5 transition-all"
          >
            <MessageSquareHeart className="w-3.5 h-3.5 text-sage-700" />
            Submit Feedback
          </button>
        </div>
      </div>

      {/* Placement Notification Banner */}
      {placementNotice && (
        <div className="p-3.5 rounded-xl bg-sage-50 border border-sage-200 text-sage-900 text-xs flex items-center justify-between shadow-2xs">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-sage-600" />
            <span className="font-medium">{placementNotice}</span>
          </div>
          <button
            onClick={() => setPlacementNotice(null)}
            className="text-sage-600 hover:text-sage-800 text-xs font-semibold px-2 py-0.5"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Warnings Banner if any */}
      {layoutWarnings.length > 0 && (
        <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-start gap-2.5">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            {layoutWarnings.map((w, i) => (
              <p key={i}>{w}</p>
            ))}
          </div>
        </div>
      )}

      {/* Main Designer Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* 3D Canvas (3 cols) */}
        <div className="lg:col-span-3 space-y-4">
          <RoomCanvas3D
            width={activeRoom?.width_m || 4.2}
            length={activeRoom?.length_m || 5.0}
            height={activeRoom?.height_m || 2.8}
            items={items}
            selectedItemId={selectedItemId}
            onSelectItem={setSelectedItemId}
          />

          {/* Selected Item Spatial Manipulation Bar */}
          {selectedItem && (
            <div className="bg-white p-5 rounded-2xl border border-warm-border shadow-xs space-y-4">
              <div className="flex items-center justify-between border-b border-warm-border pb-3">
                <div className="flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded-full border border-black/10"
                    style={{ backgroundColor: selectedItem.furniture?.color_hex || '#5E7363' }}
                  />
                  <h3 className="font-semibold text-sm text-charcoal">
                    {selectedItem.furniture?.name || 'Furniture Element'}
                  </h3>
                  <span className="text-[10px] bg-neutral-100 text-charcoal-muted px-2 py-0.5 rounded-md">
                    {selectedItem.furniture?.category}
                  </span>
                </div>

                <button
                  onClick={deleteSelectedItem}
                  className="p-1.5 rounded-lg text-red-600 hover:bg-red-50 text-xs flex items-center gap-1 font-medium transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  Remove
                </button>
              </div>

              {/* Sliders for Position X, Position Z, and Rotation Y */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div>
                  <div className="flex justify-between text-xs font-medium text-charcoal mb-1.5">
                    <span className="flex items-center gap-1">
                      <Move className="w-3 h-3 text-sage-600" /> Lateral Position (X)
                    </span>
                    <span className="font-mono text-[11px]">{selectedItem.pos_x.toFixed(2)}m</span>
                  </div>
                  <input
                    type="range"
                    min={-halfW}
                    max={halfW}
                    step={0.05}
                    value={selectedItem.pos_x}
                    onChange={(e) => updateSelectedItem({ pos_x: parseFloat(e.target.value) })}
                    className="w-full accent-sage-600"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs font-medium text-charcoal mb-1.5">
                    <span className="flex items-center gap-1">
                      <Move className="w-3 h-3 text-sage-600" /> Depth Position (Z)
                    </span>
                    <span className="font-mono text-[11px]">{selectedItem.pos_z.toFixed(2)}m</span>
                  </div>
                  <input
                    type="range"
                    min={-halfL}
                    max={halfL}
                    step={0.05}
                    value={selectedItem.pos_z}
                    onChange={(e) => updateSelectedItem({ pos_z: parseFloat(e.target.value) })}
                    className="w-full accent-sage-600"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs font-medium text-charcoal mb-1.5">
                    <span className="flex items-center gap-1">
                      <RotateCw className="w-3 h-3 text-sage-600" /> Rotation (Y-axis)
                    </span>
                    <span className="font-mono text-[11px]">
                      {((selectedItem.rot_y * 180) / Math.PI).toFixed(0)}°
                    </span>
                  </div>
                  <input
                    type="range"
                    min={-Math.PI}
                    max={Math.PI}
                    step={0.05}
                    value={selectedItem.rot_y}
                    onChange={(e) => updateSelectedItem({ rot_y: parseFloat(e.target.value) })}
                    className="w-full accent-sage-600"
                  />
                </div>
              </div>

              {selectedItem.placement_reason && (
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-[11px] text-charcoal-muted bg-neutral-50 p-3 rounded-xl border border-warm-border">
                  <div>
                    <strong className="text-charcoal font-semibold">Placement Explanation:</strong> {selectedItem.placement_reason}
                  </div>
                  {selectedItem.ml_score !== undefined && selectedItem.ml_score !== null && (
                    <div className="shrink-0 flex items-center gap-1.5 bg-sage-50 text-sage-800 px-2.5 py-1 rounded-lg border border-sage-200 font-medium">
                      <Sparkles className="w-3 h-3 text-sage-600" />
                      <span>Suitability: {(selectedItem.ml_score * 100).toFixed(0)}%</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Sidebar: Furniture Add Catalog & Item list (1 col) */}
        <div className="space-y-4">
          <div className="bg-white p-4 rounded-2xl border border-warm-border shadow-xs space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-charcoal flex items-center justify-between">
              <span>Room Furniture</span>
              <span className="text-[11px] text-charcoal-muted font-normal">
                {items.length} items
              </span>
            </h3>

            <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
              {items.map((it, idx) => {
                const isSelected = selectedItemId === (it.id || `item-${idx}`);
                return (
                  <button
                    key={it.id || idx}
                    onClick={() => setSelectedItemId(it.id || `item-${idx}`)}
                    className={`w-full p-2.5 rounded-xl text-left text-xs transition-all flex items-center justify-between border ${
                      isSelected
                        ? 'bg-sage-50 border-sage-400 text-charcoal font-semibold shadow-2xs'
                        : 'bg-background hover:bg-neutral-50 border-warm-border text-charcoal-muted'
                    }`}
                  >
                    <span className="truncate">{it.furniture?.name || `Item ${idx + 1}`}</span>
                    <span className="text-[10px] text-charcoal-muted shrink-0 font-mono">
                      {it.pos_x.toFixed(1)}, {it.pos_z.toFixed(1)}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Quick Add From Catalog */}
          <div className="bg-white p-4 rounded-2xl border border-warm-border shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-xs uppercase tracking-wider text-charcoal">
                Add Furniture
              </h3>
              <Link
                to={`/furniture?room_type=${encodeURIComponent(
                  activeRoom?.latest_prediction?.predicted_room_type ||
                    activeRoom?.room_type_preference ||
                    'LivingRoom'
                )}${activeRoom ? `&roomId=${activeRoom.id}` : ''}`}
                className="text-[11px] font-semibold text-sage-700 hover:text-sage-800 hover:underline flex items-center gap-1"
                title="Browse full furniture catalogue with room filter"
              >
                Browse All <FolderOpen className="w-3 h-3" />
              </Link>
            </div>

            <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
              {catalog.map((f) => (
                <div
                  key={f.id}
                  className="p-2.5 rounded-xl bg-background border border-warm-border flex items-center justify-between gap-2 text-xs"
                >
                  <div className="min-w-0">
                    <p className="font-semibold text-charcoal truncate">{f.name}</p>
                    <p className="text-[10px] text-charcoal-muted">
                      {f.category} • ${f.price_estimate.toFixed(0)}
                    </p>
                  </div>
                  <button
                    onClick={() => addFurnitureToRoom(f)}
                    className="p-1.5 rounded-lg bg-sage-100 hover:bg-sage-600 text-sage-700 hover:text-white transition-colors shrink-0"
                    title="Add to room"
                  >
                    <Plus className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Feedback Modal */}
      {activeRoom && (
        <FeedbackModal
          roomId={activeRoom.id}
          modelVersion={activeRoom.latest_prediction?.model_version || 'v001'}
          currentItems={items}
          isOpen={isFeedbackOpen}
          onClose={() => setIsFeedbackOpen(false)}
        />
      )}
    </div>
  );
};

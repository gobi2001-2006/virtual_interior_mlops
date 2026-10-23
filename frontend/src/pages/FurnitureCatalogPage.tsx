import React, { useState, useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import { FurnitureItem } from '../types';
import { FurnitureVisualPreview } from '../components/FurnitureVisualPreview';
import { normalizeRoomType, formatRoomTypeLabel, CANONICAL_ROOM_TYPES } from '../utils/formatters';
import {
  Sofa,
  Filter,
  Search,
  Plus,
  Maximize2,
  DollarSign,
  ArrowUpDown,
  RotateCcw,
  AlertCircle,
  X,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export const FurnitureCatalogPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  // Extract initial parameters from URL
  const initialRoomParam = searchParams.get('room_type') || searchParams.get('roomType');
  const initialRoom = initialRoomParam ? normalizeRoomType(initialRoomParam) : 'all';
  const initialCategory = searchParams.get('category') || 'all';
  const initialStyle = searchParams.get('style') || 'all';
  const roomId = searchParams.get('roomId') || searchParams.get('room_id') || '';

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>(initialCategory);
  const [selectedRoomType, setSelectedRoomType] = useState<string>(initialRoom);
  const [selectedStyle, setSelectedStyle] = useState<string>(initialStyle);
  const [sortBy, setSortBy] = useState<'default' | 'price_asc' | 'price_desc' | 'name_asc' | 'name_desc'>('default');
  const [maxPrice, setMaxPrice] = useState<number>(2000);

  // Synchronize state when URL query parameters change (e.g. from Navigation or History)
  useEffect(() => {
    const r = searchParams.get('room_type') || searchParams.get('roomType');
    if (r) {
      setSelectedRoomType(normalizeRoomType(r));
    }
    const c = searchParams.get('category');
    if (c) setSelectedCategory(c);
    const s = searchParams.get('style');
    if (s) setSelectedStyle(s);
  }, [searchParams]);

  // Query catalog from backend API
  const {
    data: catalog = [],
    isLoading,
    isError,
    error,
    refetch
  } = useQuery({
    queryKey: ['furniture', selectedCategory, selectedRoomType, selectedStyle, maxPrice],
    queryFn: () =>
      api.getFurnitureCatalog({
        category: selectedCategory !== 'all' ? selectedCategory : undefined,
        room_type: selectedRoomType !== 'all' ? selectedRoomType : undefined,
        style: selectedStyle !== 'all' ? selectedStyle : undefined,
        max_price: maxPrice,
      }),
  });

  // Dynamically derive category pills from both catalog and canonical definitions
  const categories = useMemo(() => {
    const predefined = [
      'all',
      'Sofa',
      'Armchair',
      'Bed',
      'Dining table',
      'Coffee table',
      'Side table',
      'Desk',
      'Chair',
      'Cabinet',
      'Kitchen island',
      'Counter',
      'Bar stool',
      'Bar table',
      'Pantry',
      'Vanity',
      'Wardrobe',
      'Chest of drawers',
      'Dressing table',
      'Bench',
      'TV unit',
      'Bookshelf',
      'Floor lamp',
      'Plant',
      'Rug',
      'Storage',
      'Storage rack'
    ];
    const fromData = Array.from(new Set(catalog.map((i) => i.category))).filter(Boolean);
    const merged = Array.from(new Set([...predefined, ...fromData]));
    return merged;
  }, [catalog]);

  const roomTypes = ['all', ...CANONICAL_ROOM_TYPES];
  const styles = ['all', 'Scandinavian', 'modern', 'minimalist', 'industrial', 'contemporary'];

  // Update room filter and sync URL
  const handleRoomTypeChange = (newRoom: string) => {
    setSelectedRoomType(newRoom);
    const nextParams = new URLSearchParams(searchParams);
    if (newRoom === 'all') {
      nextParams.delete('room_type');
      nextParams.delete('roomType');
    } else {
      nextParams.set('room_type', newRoom);
    }
    setSearchParams(nextParams, { replace: true });
  };

  // Update category filter and sync URL
  const handleCategoryChange = (cat: string) => {
    setSelectedCategory(cat);
    const nextParams = new URLSearchParams(searchParams);
    if (cat === 'all') {
      nextParams.delete('category');
    } else {
      nextParams.set('category', cat);
    }
    setSearchParams(nextParams, { replace: true });
  };

  const handleResetFilters = () => {
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedRoomType('all');
    setSelectedStyle('all');
    setSortBy('default');
    setMaxPrice(2000);
    const nextParams = new URLSearchParams();
    if (roomId) nextParams.set('roomId', roomId);
    setSearchParams(nextParams, { replace: true });
  };

  // Filter items locally by search query
  const filteredItems = useMemo(() => {
    let result = catalog.filter((item) => {
      const q = searchQuery.toLowerCase().trim();
      if (!q) return true;
      return (
        item.name.toLowerCase().includes(q) ||
        item.category.toLowerCase().includes(q) ||
        (item.description && item.description.toLowerCase().includes(q)) ||
        item.style.toLowerCase().includes(q)
      );
    });

    // Apply sorting
    if (sortBy === 'price_asc') {
      result.sort((a, b) => a.price_estimate - b.price_estimate);
    } else if (sortBy === 'price_desc') {
      result.sort((a, b) => b.price_estimate - a.price_estimate);
    } else if (sortBy === 'name_asc') {
      result.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'name_desc') {
      result.sort((a, b) => b.name.localeCompare(a.name));
    }

    return result;
  }, [catalog, searchQuery, sortBy]);

  // Navigate to 3D designer preserving room context
  const handleAddToDesigner = (item: FurnitureItem) => {
    const targetRoomId = roomId ? `&roomId=${roomId}` : '';
    const targetRoomType = selectedRoomType !== 'all' ? `&roomType=${selectedRoomType}` : '';
    navigate(`/designer?addFurnitureId=${item.id}${targetRoomId}${targetRoomType}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-charcoal tracking-tight">
            Furniture Catalogue
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-muted mt-1 max-w-2xl">
            Verified architectural furnishings with exact metric dimensions, room suitability tags, and estimated pricing.
          </p>
        </div>

        {roomId && (
          <div className="flex items-center gap-2 bg-sage-50 text-sage-800 px-3 py-1.5 rounded-xl border border-sage-200 text-xs font-medium">
            <Sparkles className="w-4 h-4 text-sage-600" />
            <span>Active Room Session: <strong>{selectedRoomType !== 'all' ? formatRoomTypeLabel(selectedRoomType) : 'Custom Room'}</strong></span>
          </div>
        )}
      </div>

      {/* Active Room Filter Alert Banner if room filter is on */}
      {selectedRoomType !== 'all' && (
        <div className="bg-sage-50/90 border border-sage-200 rounded-2xl p-3.5 flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-sage-900">
            <Filter className="w-4 h-4 text-sage-600 shrink-0" />
            <span>
              Showing curated furniture matching <strong>{formatRoomTypeLabel(selectedRoomType)}</strong> ({filteredItems.length} items available)
            </span>
          </div>
          <button
            type="button"
            onClick={() => handleRoomTypeChange('all')}
            className="px-2.5 py-1 bg-white hover:bg-neutral-100 text-charcoal font-semibold rounded-lg border border-warm-border shadow-2xs transition-all flex items-center gap-1 cursor-pointer"
          >
            <X className="w-3.5 h-3.5" />
            Show All Rooms
          </button>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white p-5 rounded-2xl border border-warm-border shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row items-center gap-3">
          {/* Search Input */}
          <div className="relative w-full md:flex-1">
            <Search className="w-4 h-4 text-charcoal-muted absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              id="furniture-search-input"
              placeholder="Search by furniture name, category, or style..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-9 py-2.5 rounded-xl border border-warm-border text-xs focus:outline-hidden focus:border-sage-500 bg-background text-charcoal"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-charcoal-muted hover:text-charcoal p-0.5"
                aria-label="Clear search"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Room Filter Select */}
          <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
            <div className="flex items-center gap-1 bg-background border border-warm-border rounded-xl px-2.5 py-1.5 text-xs text-charcoal">
              <span className="text-charcoal-muted text-[11px] font-medium">Room:</span>
              <select
                id="furniture-room-filter"
                value={selectedRoomType}
                onChange={(e) => handleRoomTypeChange(e.target.value)}
                className="bg-transparent text-xs font-semibold text-charcoal focus:outline-hidden cursor-pointer"
                aria-label="Filter by room type"
              >
                <option value="all">All Rooms</option>
                {CANONICAL_ROOM_TYPES.map((r) => (
                  <option key={r} value={r}>
                    {formatRoomTypeLabel(r)}
                  </option>
                ))}
              </select>
            </div>

            {/* Style Filter Select */}
            <div className="flex items-center gap-1 bg-background border border-warm-border rounded-xl px-2.5 py-1.5 text-xs text-charcoal">
              <span className="text-charcoal-muted text-[11px] font-medium">Style:</span>
              <select
                id="furniture-style-filter"
                value={selectedStyle}
                onChange={(e) => setSelectedStyle(e.target.value)}
                className="bg-transparent text-xs font-semibold text-charcoal capitalize focus:outline-hidden cursor-pointer"
                aria-label="Filter by style"
              >
                <option value="all">All Styles</option>
                {styles.filter((s) => s !== 'all').map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort Select */}
            <div className="flex items-center gap-1 bg-background border border-warm-border rounded-xl px-2.5 py-1.5 text-xs text-charcoal">
              <ArrowUpDown className="w-3.5 h-3.5 text-charcoal-muted" />
              <select
                id="furniture-sort-select"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="bg-transparent text-xs font-semibold text-charcoal focus:outline-hidden cursor-pointer"
                aria-label="Sort furniture items"
              >
                <option value="default">Default Order</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="name_asc">Name: A to Z</option>
                <option value="name_desc">Name: Z to A</option>
              </select>
            </div>
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => handleCategoryChange(cat)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium whitespace-nowrap transition-all border cursor-pointer ${
                selectedCategory === cat
                  ? 'bg-sage-600 text-white border-sage-600 shadow-xs'
                  : 'bg-background hover:bg-neutral-100/80 border-warm-border text-charcoal-muted'
              }`}
            >
              {cat === 'all' ? 'All Categories' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Error State */}
      {isError && (
        <div className="p-6 rounded-2xl bg-red-50 border border-red-200 text-red-800 text-xs flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
            <div>
              <div className="font-semibold text-sm">Failed to retrieve furniture catalog</div>
              <p className="text-[11px] text-red-700 mt-0.5">
                {(error as Error)?.message || 'Network connection failed. Please ensure the backend is running.'}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => refetch()}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl font-semibold shadow-xs transition-all cursor-pointer"
          >
            Retry Request
          </button>
        </div>
      )}

      {/* Grid of Furniture Cards */}
      {isLoading ? (
        <div className="py-24 text-center">
          <div className="w-8 h-8 border-3 border-sage-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          <p className="text-xs text-charcoal-muted">Loading architectural furniture catalogue...</p>
        </div>
      ) : filteredItems.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-warm-border p-8 space-y-3">
          <Sofa className="w-12 h-12 text-charcoal-muted mx-auto mb-2 opacity-35" />
          <h3 className="text-sm font-semibold text-charcoal">No Matching Furniture Found</h3>
          <p className="text-xs text-charcoal-muted max-w-md mx-auto">
            {selectedRoomType !== 'all'
              ? `No furniture found matching room filter "${formatRoomTypeLabel(selectedRoomType)}" with the current category or keywords.`
              : 'No furniture items match your search keywords or price filters.'}
          </p>
          <button
            type="button"
            onClick={handleResetFilters}
            className="mt-2 px-4 py-2 bg-sage-50 text-sage-700 border border-sage-200 hover:bg-sage-600 hover:text-white rounded-xl text-xs font-semibold transition-all inline-flex items-center gap-1.5 cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset All Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-2xl border border-warm-border overflow-hidden card-hover flex flex-col justify-between"
            >
              {/* Visual Preview (Real Image with 3D WebGL Toggle) */}
              <FurnitureVisualPreview item={item} className="h-44" />

              {/* Item Details */}
              <div className="p-4 space-y-3 flex-1 flex flex-col justify-between">
                <div>
                  <h3 className="font-semibold text-sm text-charcoal line-clamp-1">{item.name}</h3>
                  <p className="text-[11px] text-charcoal-muted mt-1 line-clamp-2">
                    {item.description || 'Architecturally proportioned interior furniture element.'}
                  </p>
                </div>

                <div className="pt-2 border-t border-warm-border/60 space-y-1.5 text-[11px] text-charcoal-muted">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1">
                      <Maximize2 className="w-3 h-3 text-sage-600" />
                      Dimensions (W×H×D)
                    </span>
                    <span className="font-medium text-charcoal">
                      {item.width_m}m × {item.height_m}m × {item.depth_m}m
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span>Est. Price</span>
                    <span className="font-bold text-sm text-charcoal">
                      ${item.price_estimate.toFixed(0)} <span className="text-[10px] font-normal text-charcoal-muted">{item.currency}</span>
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-1 mt-1 pt-1">
                    {item.suitable_rooms?.map((rm) => (
                      <span
                        key={rm}
                        className={`text-[9px] px-1.5 py-0.5 rounded-sm font-medium ${
                          selectedRoomType !== 'all' && normalizeRoomType(rm) === selectedRoomType
                            ? 'bg-sage-100 text-sage-800 font-semibold'
                            : 'bg-neutral-100 text-charcoal-muted'
                        }`}
                      >
                        {formatRoomTypeLabel(rm)}
                      </span>
                    ))}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => handleAddToDesigner(item)}
                  className="w-full py-2 bg-sage-50 hover:bg-sage-600 text-sage-700 hover:text-white border border-sage-200 hover:border-sage-600 rounded-xl text-xs font-semibold transition-all flex items-center justify-center gap-1.5 mt-2 cursor-pointer focus:outline-hidden focus:ring-2 focus:ring-sage-500"
                  aria-label={`Add ${item.name} to 3D Room Designer`}
                >
                  <Plus className="w-3.5 h-3.5" />
                  Add to 3D Room Designer
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

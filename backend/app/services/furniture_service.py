from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.furniture import FurnitureItem
from backend.app.schemas.furniture import FurnitureCreate, FurnitureFilter


def normalize_room_type(room_type: Optional[str]) -> Optional[str]:
    """
    Normalizes variations of room typology strings (e.g. 'dining_room', 'Dining Room',
    'livingroom', 'living') to the canonical PascalCase class names used in the MLOps pipeline.
    """
    if not room_type:
        return None
    clean = room_type.strip().lower().replace(" ", "").replace("_", "").replace("-", "")
    if clean in ("all", "*", ""):
        return None
    mapping = {
        "bathroom": "Bathroom",
        "bedroom": "Bedroom",
        "dining": "DiningRoom",
        "diningroom": "DiningRoom",
        "homeoffice": "HomeOffice",
        "office": "HomeOffice",
        "kitchen": "Kitchen",
        "living": "LivingRoom",
        "livingroom": "LivingRoom",
    }
    return mapping.get(clean, room_type)


# Comprehensive architectural furniture catalogue (57 items across all 6 canonical room classes)
DEFAULT_FURNITURE_CATALOG = [
    # ==================== 1. SOFAS & LIVING SEATING ====================
    {
        "name": "Nordic Fabric 3-Seater Sofa",
        "category": "Sofa",
        "width_m": 2.2,
        "height_m": 0.85,
        "depth_m": 0.95,
        "price_estimate": 780.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["LivingRoom", "HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#6B7C6E",
        "image_url": "/static/furniture/sofa_nordic_3seater.svg",
        "description": "Ergonomic 3-seater with natural pine legs and muted sage linen upholstery."
    },
    {
        "name": "Modern Minimalist Loveseat",
        "category": "Sofa",
        "width_m": 1.6,
        "height_m": 0.8,
        "depth_m": 0.85,
        "price_estimate": 520.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["LivingRoom", "Bedroom", "HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#8A9A86",
        "image_url": "/static/furniture/sofa_minimalist_loveseat.svg",
        "description": "Compact two-seater sofa ideal for modern apartments and studios."
    },
    {
        "name": "L-Shaped Modular Sectional Sofa",
        "category": "Sofa",
        "width_m": 2.6,
        "height_m": 0.85,
        "depth_m": 1.8,
        "price_estimate": 1350.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#5D6E60",
        "image_url": "/static/furniture/sofa_sectional_lshape.svg",
        "description": "Spacious L-shaped modular sectional sofa with chaise lounge and high-density foam cushions."
    },
    {
        "name": "Lounge Accent Armchair",
        "category": "Armchair",
        "width_m": 0.85,
        "height_m": 0.9,
        "depth_m": 0.85,
        "price_estimate": 340.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["LivingRoom", "Bedroom", "HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#B88E75",
        "image_url": "/static/furniture/armchair_lounge_accent.svg",
        "description": "Plush cushioned armchair with brushed brass accents."
    },

    # ==================== 2. BEDS & BEDROOM SUITE ====================
    {
        "name": "Single Platform Daybed with Storage",
        "category": "Bed",
        "width_m": 1.05,
        "height_m": 0.85,
        "depth_m": 2.05,
        "price_estimate": 480.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#B39274",
        "image_url": "/static/furniture/bed_single_platform.svg",
        "description": "Single platform bed with integrated pull-out underbed storage drawers."
    },
    {
        "name": "Platform Queen Bed with Headboard",
        "category": "Bed",
        "width_m": 1.7,
        "height_m": 1.1,
        "depth_m": 2.15,
        "price_estimate": 950.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#D8CFBC",
        "image_url": "/static/furniture/bed_platform_queen.svg",
        "description": "Sturdy oak platform bed with cushioned fabric headboard."
    },
    {
        "name": "Scandinavian King Bed Frame",
        "category": "Bed",
        "width_m": 2.0,
        "height_m": 1.05,
        "depth_m": 2.2,
        "price_estimate": 1150.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#C5BAA8",
        "image_url": "/static/furniture/bed_scandinavian_king.svg",
        "description": "Solid ash wood frame with minimalist slatted headboard."
    },
    {
        "name": "Minimalist Bedside Nightstand",
        "category": "Side table",
        "width_m": 0.5,
        "height_m": 0.55,
        "depth_m": 0.45,
        "price_estimate": 140.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["Bedroom", "LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#DDD5C7",
        "image_url": "/static/furniture/table_minimalist_nightstand.svg",
        "description": "Single-drawer compact nightstand with open lower storage shelf."
    },
    {
        "name": "6-Drawer Oak Chest of Drawers",
        "category": "Chest of drawers",
        "width_m": 1.1,
        "height_m": 1.15,
        "depth_m": 0.5,
        "price_estimate": 460.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#A88B74",
        "image_url": "/static/furniture/bedroom_chest_drawers.svg",
        "description": "Vertical 6-drawer dresser in white oak with brushed brass finger pulls."
    },
    {
        "name": "Modern Vanity Dressing Table with Mirror",
        "category": "Dressing table",
        "width_m": 1.0,
        "height_m": 1.35,
        "depth_m": 0.45,
        "price_estimate": 390.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#B38B6D",
        "image_url": "/static/furniture/bedroom_dressing_table.svg",
        "description": "Dressing vanity with round backlit mirror, dual cosmetic drawers, and cushioned stool."
    },
    {
        "name": "Upholstered Bedroom End-of-Bed Bench",
        "category": "Bench",
        "width_m": 1.3,
        "height_m": 0.45,
        "depth_m": 0.42,
        "price_estimate": 220.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#C8B89E",
        "image_url": "/static/furniture/bedroom_end_bench.svg",
        "description": "Tufted oatmeal linen bench with tapered solid walnut legs."
    },
    {
        "name": "Compact Bedside Lamp and Charging Stand",
        "category": "Table lamp",
        "width_m": 0.35,
        "height_m": 0.5,
        "depth_m": 0.35,
        "price_estimate": 95.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bedroom", "HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#D4AF37",
        "image_url": "/static/furniture/bedroom_bedside_lamp.svg",
        "description": "Warm ambient table lamp with pleated linen shade and brass touch dimmer stem."
    },
    {
        "name": "Modular Sliding Door Wardrobe",
        "category": "Wardrobe",
        "width_m": 1.8,
        "height_m": 2.1,
        "depth_m": 0.65,
        "price_estimate": 890.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bedroom"],
        "model_type": "procedural",
        "color_hex": "#EDE8DE",
        "image_url": "/static/furniture/storage_sliding_wardrobe.svg",
        "description": "Spacious wardrobe with dual mirrored sliding doors and internal organizers."
    },

    # ==================== 3. LIVING ROOM TABLES & MEDIA ====================
    {
        "name": "Round Glass Coffee Table",
        "category": "Coffee table",
        "width_m": 0.9,
        "height_m": 0.45,
        "depth_m": 0.9,
        "price_estimate": 240.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#2E3630",
        "image_url": "/static/furniture/table_round_glass_coffee.svg",
        "description": "Tempered glass top with architectural matte black steel tripod base."
    },
    {
        "name": "Minimalist Ceramic Side End Table",
        "category": "Side table",
        "width_m": 0.45,
        "height_m": 0.52,
        "depth_m": 0.45,
        "price_estimate": 160.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["LivingRoom", "Bedroom"],
        "model_type": "procedural",
        "color_hex": "#D3CBC0",
        "image_url": "/static/furniture/living_side_table_ceramic.svg",
        "description": "Sculptural fluted ceramic end table with smooth glazed top surface."
    },
    {
        "name": "Low-Profile Media Console TV Unit",
        "category": "TV unit",
        "width_m": 1.8,
        "height_m": 0.5,
        "depth_m": 0.42,
        "price_estimate": 420.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#9E8B75",
        "image_url": "/static/furniture/storage_media_console_tv.svg",
        "description": "Media console with slatted acoustic sliding cabinet doors."
    },
    {
        "name": "Acoustic Slatted Media Storage Credenza",
        "category": "Storage",
        "width_m": 1.6,
        "height_m": 0.72,
        "depth_m": 0.45,
        "price_estimate": 580.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#7A583E",
        "image_url": "/static/furniture/living_media_credenza.svg",
        "description": "Solid walnut entertainment credenza with ventilated cable raceway and acoustic slatted panels."
    },
    {
        "name": "Tall Architectural Bookshelf",
        "category": "Bookshelf",
        "width_m": 0.9,
        "height_m": 1.9,
        "depth_m": 0.35,
        "price_estimate": 310.0,
        "currency": "USD",
        "style": "industrial",
        "suitable_rooms": ["LivingRoom", "HomeOffice", "Bedroom"],
        "model_type": "procedural",
        "color_hex": "#383E3A",
        "image_url": "/static/furniture/storage_architectural_bookshelf.svg",
        "description": "5-tier vertical open shelving unit with durable steel uprights."
    },

    # ==================== 4. DINING ROOM SUITE ====================
    {
        "name": "Compact 2-Seater Bistro Dining Table",
        "category": "Dining table",
        "width_m": 0.8,
        "height_m": 0.75,
        "depth_m": 0.8,
        "price_estimate": 240.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["DiningRoom", "Kitchen"],
        "model_type": "procedural",
        "color_hex": "#8D6E63",
        "image_url": "/static/furniture/dining_table_2seater.svg",
        "description": "Space-saving square bistro dining table on heavy cast-iron pedestal base."
    },
    {
        "name": "Round 4-Seater Scandinavian Dining Table",
        "category": "Dining table",
        "width_m": 1.1,
        "height_m": 0.76,
        "depth_m": 1.1,
        "price_estimate": 420.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["DiningRoom", "Kitchen"],
        "model_type": "procedural",
        "color_hex": "#D7CCC8",
        "image_url": "/static/furniture/dining_table_4seater.svg",
        "description": "Round light oak dining table with beveled edges and splayed solid legs."
    },
    {
        "name": "Solid Wood Dining Table",
        "category": "Dining table",
        "width_m": 1.8,
        "height_m": 0.76,
        "depth_m": 0.9,
        "price_estimate": 680.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["DiningRoom", "Kitchen"],
        "model_type": "procedural",
        "color_hex": "#7A583E",
        "image_url": "/static/furniture/table_solid_wood_dining.svg",
        "description": "6-seater dining table with warm walnut veneer and beveled edges."
    },
    {
        "name": "Grand 8-Seater Walnut Dining Table",
        "category": "Dining table",
        "width_m": 2.4,
        "height_m": 0.76,
        "depth_m": 1.0,
        "price_estimate": 980.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["DiningRoom"],
        "model_type": "procedural",
        "color_hex": "#5D4037",
        "image_url": "/static/furniture/dining_table_8seater.svg",
        "description": "Expansive 8-seater dining table crafted from solid American walnut with double trestle base."
    },
    {
        "name": "Curved Backrest Wooden Dining Chair",
        "category": "Chair",
        "width_m": 0.5,
        "height_m": 0.84,
        "depth_m": 0.52,
        "price_estimate": 140.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["DiningRoom", "Kitchen"],
        "model_type": "procedural",
        "color_hex": "#C5A880",
        "image_url": "/static/furniture/dining_chair_wood.svg",
        "description": "Ergonomic spindle-back dining chair with sculpted natural seat contour."
    },
    {
        "name": "Upholstered Dining Bench Seat",
        "category": "Bench",
        "width_m": 1.4,
        "height_m": 0.48,
        "depth_m": 0.4,
        "price_estimate": 260.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["DiningRoom"],
        "model_type": "procedural",
        "color_hex": "#B0BEC5",
        "image_url": "/static/furniture/dining_bench_upholstered.svg",
        "description": "Low-profile upholstered dining bench matching banquet and farmhouse tables."
    },
    {
        "name": "Scandinavian 3-Door Dining Sideboard Credenza",
        "category": "Sideboard",
        "width_m": 1.6,
        "height_m": 0.82,
        "depth_m": 0.45,
        "price_estimate": 640.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["DiningRoom", "LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#A1887F",
        "image_url": "/static/furniture/dining_sideboard_credenza.svg",
        "description": "Multi-tier buffet sideboard with cutlery drawers and adjustable china shelving."
    },
    {
        "name": "Glass-Front Display Crockery Cabinet",
        "category": "Display cabinet",
        "width_m": 0.95,
        "height_m": 1.85,
        "depth_m": 0.42,
        "price_estimate": 710.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["DiningRoom", "LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#3E2723",
        "image_url": "/static/furniture/dining_display_cabinet.svg",
        "description": "Tempered glass display cabinet for glassware and dinnerware with integrated spotlighting."
    },
    {
        "name": "Rolling Beverage and Serving Bar Cart",
        "category": "Serving trolley",
        "width_m": 0.75,
        "height_m": 0.85,
        "depth_m": 0.45,
        "price_estimate": 180.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["DiningRoom", "LivingRoom"],
        "model_type": "procedural",
        "color_hex": "#D4AF37",
        "image_url": "/static/furniture/dining_serving_cart.svg",
        "description": "2-tier brass and tempered glass mobile serving trolley with stemware rack."
    },

    # ==================== 5. KITCHEN FURNITURE & FIXTURES ====================
    {
        "name": "Modular Double-Door Kitchen Base Cabinet",
        "category": "Cabinet",
        "width_m": 0.9,
        "height_m": 0.9,
        "depth_m": 0.6,
        "price_estimate": 340.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Kitchen"],
        "model_type": "procedural",
        "color_hex": "#455A64",
        "image_url": "/static/furniture/kitchen_base_cabinet.svg",
        "description": "Modular lower kitchen cabinet with quartz countertop and soft-close European hinges."
    },
    {
        "name": "Frosted Glass Kitchen Wall Hanging Cabinet",
        "category": "Wall cabinet",
        "width_m": 0.9,
        "height_m": 0.75,
        "depth_m": 0.35,
        "price_estimate": 280.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Kitchen"],
        "model_type": "procedural",
        "color_hex": "#37474F",
        "image_url": "/static/furniture/kitchen_wall_cabinet.svg",
        "description": "Upper kitchen wall cabinet with dual frosted glass lift-up doors."
    },
    {
        "name": "Stainless Kitchen Prep Island Cart",
        "category": "Kitchen island",
        "width_m": 1.4,
        "height_m": 0.9,
        "depth_m": 0.7,
        "price_estimate": 450.0,
        "currency": "USD",
        "style": "industrial",
        "suitable_rooms": ["Kitchen", "DiningRoom"],
        "model_type": "procedural",
        "color_hex": "#90A4AE",
        "image_url": "/static/furniture/island_kitchen_prep_cart.svg",
        "description": "Commercial-grade butcher block mobile preparation island with locking casters."
    },
    {
        "name": "Butcher Block Heavy Kitchen Island",
        "category": "Kitchen island",
        "width_m": 1.6,
        "height_m": 0.92,
        "depth_m": 0.9,
        "price_estimate": 720.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["Kitchen"],
        "model_type": "procedural",
        "color_hex": "#2E3D34",
        "image_url": "/static/furniture/kitchen_island_butcherblock.svg",
        "description": "Freestanding center island with 3-inch end-grain maple butcher block and deep pot drawers."
    },
    {
        "name": "Granite Top Kitchen Preparation Counter",
        "category": "Counter",
        "width_m": 1.4,
        "height_m": 0.9,
        "depth_m": 0.65,
        "price_estimate": 590.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Kitchen"],
        "model_type": "procedural",
        "color_hex": "#37474F",
        "image_url": "/static/furniture/kitchen_prep_counter.svg",
        "description": "Granite surface kitchen prep station with utensil hooks and knife block slot."
    },
    {
        "name": "Swivel Oak Padded Bar Stool",
        "category": "Bar stool",
        "width_m": 0.45,
        "height_m": 0.95,
        "depth_m": 0.45,
        "price_estimate": 130.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["Kitchen", "DiningRoom"],
        "model_type": "procedural",
        "color_hex": "#C5A07A",
        "image_url": "/static/furniture/kitchen_bar_stool.svg",
        "description": "Counter-height swivel bar stool with 360-degree rotation and vegan leather seat."
    },
    {
        "name": "High Countertop Dining Bar Table",
        "category": "Bar table",
        "width_m": 1.3,
        "height_m": 1.05,
        "depth_m": 0.6,
        "price_estimate": 360.0,
        "currency": "USD",
        "style": "industrial",
        "suitable_rooms": ["Kitchen", "DiningRoom"],
        "model_type": "procedural",
        "color_hex": "#7A583E",
        "image_url": "/static/furniture/kitchen_bar_table.svg",
        "description": "Pub-height narrow bar dining table with heavy gauge steel trestle frame."
    },
    {
        "name": "Tall 4-Door Kitchen Pantry Cabinet",
        "category": "Pantry",
        "width_m": 0.8,
        "height_m": 2.0,
        "depth_m": 0.55,
        "price_estimate": 520.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["Kitchen"],
        "model_type": "procedural",
        "color_hex": "#F5F5F0",
        "image_url": "/static/furniture/kitchen_pantry_cabinet.svg",
        "description": "Floor-to-ceiling kitchen pantry with door spice racks and pull-out wire baskets."
    },
    {
        "name": "Multi-Tier Metal Kitchen Baker Rack",
        "category": "Storage rack",
        "width_m": 0.85,
        "height_m": 1.65,
        "depth_m": 0.4,
        "price_estimate": 190.0,
        "currency": "USD",
        "style": "industrial",
        "suitable_rooms": ["Kitchen"],
        "model_type": "procedural",
        "color_hex": "#2E342F",
        "image_url": "/static/furniture/kitchen_bakers_rack.svg",
        "description": "Microwave and cookware utility storage baker's rack with power cord grommets."
    },

    # ==================== 6. BATHROOM FIXTURES & STORAGE ====================
    {
        "name": "Modern Floating Bathroom Vanity",
        "category": "Vanity",
        "width_m": 1.2,
        "height_m": 0.85,
        "depth_m": 0.55,
        "price_estimate": 620.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#8D6E63",
        "image_url": "/static/furniture/vanity_floating_bathroom.svg",
        "description": "Floating walnut vanity with ceramic vessel basin and soft-close storage drawers."
    },
    {
        "name": "Double Vessel Sink Master Vanity Unit",
        "category": "Vanity",
        "width_m": 1.6,
        "height_m": 0.85,
        "depth_m": 0.55,
        "price_estimate": 890.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#37474F",
        "image_url": "/static/furniture/bathroom_double_vanity.svg",
        "description": "60-inch master bathroom vanity with dual porcelain vessel sinks and quartz countertop."
    },
    {
        "name": "Wall-Mounted Minimalist Washbasin Unit",
        "category": "Vanity",
        "width_m": 0.65,
        "height_m": 0.5,
        "depth_m": 0.45,
        "price_estimate": 310.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#CFD8DC",
        "image_url": "/static/furniture/bathroom_wall_washbasin.svg",
        "description": "Compact wall-hung washbasin cabinet designed for powder rooms and guest baths."
    },
    {
        "name": "LED Backlit Medicine Mirror Cabinet",
        "category": "Mirror cabinet",
        "width_m": 0.8,
        "height_m": 0.7,
        "depth_m": 0.16,
        "price_estimate": 220.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#ECEFF1",
        "image_url": "/static/furniture/bathroom_mirror_cabinet.svg",
        "description": "Defogging LED backlit dual mirror doors concealing adjustable glass shelving."
    },
    {
        "name": "Tall Slim Bathroom Linen Tower Cabinet",
        "category": "Linen cabinet",
        "width_m": 0.42,
        "height_m": 1.85,
        "depth_m": 0.38,
        "price_estimate": 340.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#FFFFFF",
        "image_url": "/static/furniture/bathroom_linen_tower.svg",
        "description": "Vertical space-saving bathroom column cabinet with laundry hamper compartment."
    },
    {
        "name": "Freestanding Bamboo Bathroom Towel Shelf",
        "category": "Shelving",
        "width_m": 0.5,
        "height_m": 1.2,
        "depth_m": 0.35,
        "price_estimate": 110.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#C5A07A",
        "image_url": "/static/furniture/bathroom_towel_shelf.svg",
        "description": "Moisture-resistant natural bamboo 4-tier open towel and toiletry organizer."
    },
    {
        "name": "Slatted Teak Bathroom Waterproof Stool",
        "category": "Stool",
        "width_m": 0.42,
        "height_m": 0.45,
        "depth_m": 0.35,
        "price_estimate": 95.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#8D6E63",
        "image_url": "/static/furniture/bathroom_teak_stool.svg",
        "description": "Water-resistant solid teak spa shower stool with curved seat and lower shelf."
    },
    {
        "name": "Woven Fabric Laundry Hamper with Lid",
        "category": "Laundry hamper",
        "width_m": 0.45,
        "height_m": 0.65,
        "depth_m": 0.38,
        "price_estimate": 65.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["Bathroom", "Bedroom"],
        "model_type": "procedural",
        "color_hex": "#B0BEC5",
        "image_url": "/static/furniture/bathroom_laundry_hamper.svg",
        "description": "Breathable woven laundry hamper with bamboo rim and removable canvas liner."
    },
    {
        "name": "Over-Toilet Space Saver Storage Rack",
        "category": "Storage rack",
        "width_m": 0.65,
        "height_m": 1.65,
        "depth_m": 0.28,
        "price_estimate": 125.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["Bathroom"],
        "model_type": "procedural",
        "color_hex": "#37474F",
        "image_url": "/static/furniture/bathroom_overtoilet_rack.svg",
        "description": "3-shelf matte black metal organizer that fits directly above standard toilet cisterns."
    },

    # ==================== 7. HOME OFFICE WORKSPACE ====================
    {
        "name": "Compact Floating Computer Study Desk",
        "category": "Desk",
        "width_m": 1.1,
        "height_m": 0.75,
        "depth_m": 0.55,
        "price_estimate": 260.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["HomeOffice", "Bedroom"],
        "model_type": "procedural",
        "color_hex": "#C5A07A",
        "image_url": "/static/furniture/office_compact_study_desk.svg",
        "description": "Compact study desk with integrated pen groove, cord grommet, and stationery drawer."
    },
    {
        "name": "Executive Standing Desk",
        "category": "Desk",
        "width_m": 1.5,
        "height_m": 0.75,
        "depth_m": 0.75,
        "price_estimate": 490.0,
        "currency": "USD",
        "style": "industrial",
        "suitable_rooms": ["HomeOffice", "Bedroom"],
        "model_type": "procedural",
        "color_hex": "#434B45",
        "image_url": "/static/furniture/desk_executive_standing.svg",
        "description": "Heavy-duty steel frame office desk with cable management."
    },
    {
        "name": "Dual-Motor Electric Height Adjustable Standing Desk",
        "category": "Desk",
        "width_m": 1.6,
        "height_m": 0.75,
        "depth_m": 0.8,
        "price_estimate": 620.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#FFFFFF",
        "image_url": "/static/furniture/office_electric_sitstand_desk.svg",
        "description": "Whisper-quiet dual motor electric sit-stand desk with 4 programmable memory presets."
    },
    {
        "name": "Ergonomic Mesh Task Chair",
        "category": "Chair",
        "width_m": 0.65,
        "height_m": 1.05,
        "depth_m": 0.65,
        "price_estimate": 280.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#252B26",
        "image_url": "/static/furniture/chair_ergonomic_task.svg",
        "description": "High-back breathable mesh chair with adjustable lumbar support."
    },
    {
        "name": "High-Back Leather Executive Chair",
        "category": "Chair",
        "width_m": 0.7,
        "height_m": 1.18,
        "depth_m": 0.7,
        "price_estimate": 390.0,
        "currency": "USD",
        "style": "contemporary",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#3E2723",
        "image_url": "/static/furniture/office_executive_leather_chair.svg",
        "description": "Top-grain bonded leather executive chair with pneumatic tilt tension and polished base."
    },
    {
        "name": "Lockable Under-Desk Mobile Drawer Pedestal",
        "category": "Filing cabinet",
        "width_m": 0.42,
        "height_m": 0.6,
        "depth_m": 0.5,
        "price_estimate": 180.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#ECEFF1",
        "image_url": "/static/furniture/office_mobile_pedestal.svg",
        "description": "3-drawer lockable steel filing cabinet fitting letter and legal folders on swivel casters."
    },
    {
        "name": "Solid Wood Dual Monitor Stand with Riser Shelf",
        "category": "Monitor stand",
        "width_m": 1.0,
        "height_m": 0.12,
        "depth_m": 0.24,
        "price_estimate": 75.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#8D6E63",
        "image_url": "/static/furniture/office_dual_monitor_stand.svg",
        "description": "Ergonomic eye-level wooden desk riser with slots for phone, tablet, and keyboard tuckaway."
    },
    {
        "name": "Lateral 2-Drawer Office File Cabinet",
        "category": "Filing cabinet",
        "width_m": 0.85,
        "height_m": 0.75,
        "depth_m": 0.5,
        "price_estimate": 290.0,
        "currency": "USD",
        "style": "industrial",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#37474F",
        "image_url": "/static/furniture/office_file_cabinet.svg",
        "description": "Heavy-duty anti-tip lateral filing cabinet with full extension ball-bearing drawer slides."
    },
    {
        "name": "Modular Storage Credenza with Sliding Doors",
        "category": "Storage",
        "width_m": 1.4,
        "height_m": 0.76,
        "depth_m": 0.42,
        "price_estimate": 480.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#5D4037",
        "image_url": "/static/furniture/office_storage_credenza.svg",
        "description": "Office printer stand and storage cabinet with dual sliding acoustic bypass doors."
    },

    # ==================== 8. LIGHTING & BOTANICAL ACCENTS ====================
    {
        "name": "Arc Brass Floor Lamp",
        "category": "Floor lamp",
        "width_m": 0.45,
        "height_m": 1.85,
        "depth_m": 0.85,
        "price_estimate": 160.0,
        "currency": "USD",
        "style": "modern",
        "suitable_rooms": ["LivingRoom", "Bedroom", "HomeOffice"],
        "model_type": "procedural",
        "color_hex": "#D4AF37",
        "image_url": "/static/furniture/lamp_arc_brass_floor.svg",
        "description": "Sweeping curved arc lamp with white linen dome shade."
    },
    {
        "name": "Potted Fiddle Leaf Fig Tree",
        "category": "Plant",
        "width_m": 0.5,
        "height_m": 1.4,
        "depth_m": 0.5,
        "price_estimate": 75.0,
        "currency": "USD",
        "style": "Scandinavian",
        "suitable_rooms": ["LivingRoom", "Bedroom", "DiningRoom", "HomeOffice", "Bathroom"],
        "model_type": "procedural",
        "color_hex": "#3E6B48",
        "image_url": "/static/furniture/plant_fiddle_leaf_fig.svg",
        "description": "Lush indoor botanical accent in matte white ceramic planter."
    },
    {
        "name": "Wool Geometric Area Rug",
        "category": "Rug",
        "width_m": 2.4,
        "height_m": 0.02,
        "depth_m": 1.7,
        "price_estimate": 290.0,
        "currency": "USD",
        "style": "minimalist",
        "suitable_rooms": ["LivingRoom", "Bedroom", "DiningRoom"],
        "model_type": "procedural",
        "color_hex": "#E3DCCF",
        "image_url": "/static/furniture/rug_wool_geometric.svg",
        "description": "Hand-tufted low-pile wool rug with soft tonal geometric patterns."
    }
]


class FurnitureService:
    @staticmethod
    def get_all(
        db: Session,
        category: Optional[str] = None,
        room_type: Optional[str] = None,
        style: Optional[str] = None,
        max_price: Optional[float] = None
    ) -> List[FurnitureItem]:
        query = db.query(FurnitureItem)
        
        if category:
            query = query.filter(FurnitureItem.category.ilike(f"%{category}%"))
        if style:
            query = query.filter(FurnitureItem.style.ilike(f"%{style}%"))
        if max_price is not None:
            query = query.filter(FurnitureItem.price_estimate <= max_price)
            
        items = query.all()
        
        # Room typology filtering with robust normalization
        if room_type:
            norm_room = normalize_room_type(room_type)
            if norm_room:
                filtered = []
                for item in items:
                    suitable = item.suitable_rooms or []
                    if any(normalize_room_type(r) == norm_room for r in suitable):
                        filtered.append(item)
                return filtered
            
        return items

    @staticmethod
    def get_by_id(db: Session, furniture_id: str) -> Optional[FurnitureItem]:
        return db.query(FurnitureItem).filter(FurnitureItem.id == furniture_id).first()

    @staticmethod
    def create(db: Session, payload: FurnitureCreate) -> FurnitureItem:
        item = FurnitureItem(**payload.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def seed_catalog(db: Session) -> int:
        catalog_by_name = {item["name"]: item for item in DEFAULT_FURNITURE_CATALOG}
        existing_items = db.query(FurnitureItem).all()
        existing_names = set()

        for item in existing_items:
            existing_names.add(item.name)
            if item.name in catalog_by_name:
                cat_data = catalog_by_name[item.name]
                # Update image_url, suitable_rooms, description, and color_hex idempotently
                if cat_data.get("image_url") and item.image_url != cat_data["image_url"]:
                    item.image_url = cat_data["image_url"]
                if cat_data.get("suitable_rooms"):
                    item.suitable_rooms = cat_data["suitable_rooms"]
                if cat_data.get("description") and not item.description:
                    item.description = cat_data["description"]
                if cat_data.get("color_hex") and not item.color_hex:
                    item.color_hex = cat_data["color_hex"]

        for name, data in catalog_by_name.items():
            if name not in existing_names:
                new_item = FurnitureItem(**data)
                db.add(new_item)

        db.commit()
        return db.query(FurnitureItem).count()

import pytest
from backend.app.services.furniture_service import FurnitureService
from backend.app.models.furniture import FurnitureItem

CANONICAL_ROOM_TYPES = [
    "Bathroom",
    "Bedroom",
    "DiningRoom",
    "HomeOffice",
    "Kitchen",
    "LivingRoom",
]

def test_expanded_catalog_record_count(client):
    """Test that the catalog has expanded to between 48 and 60 items (we have 57)."""
    response = client.get("/api/furniture")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 48, f"Expected at least 48 items, found {len(items)}"
    assert len(items) <= 70, f"Expected catalog size around 48-60 items, found {len(items)}"

def test_each_canonical_room_type_has_at_least_eight_items(client):
    """Test that each of the 6 canonical room types has at least 8 matching items."""
    for room_type in CANONICAL_ROOM_TYPES:
        response = client.get(f"/api/furniture?room_type={room_type}")
        assert response.status_code == 200
        items = response.json()
        assert len(items) >= 8, f"Expected >= 8 items for {room_type}, but got {len(items)}"
        for item in items:
            suitable_lower = [r.lower() for r in item.get("suitable_rooms", [])]
            assert room_type.lower() in suitable_lower, (
                f"Item {item['name']} returned for {room_type} but suitable_rooms is {item.get('suitable_rooms')}"
            )

def test_room_type_normalization_query_variations(client):
    """Test that various room type query formats (snake_case, spaces, lowercase) normalize correctly."""
    variations = [
        ("dining_room", "DiningRoom"),
        ("dining room", "DiningRoom"),
        ("home_office", "HomeOffice"),
        ("living_room", "LivingRoom"),
        ("bedroom", "Bedroom"),
        ("bathroom", "Bathroom"),
        ("kitchen", "Kitchen"),
    ]
    for param_val, canonical in variations:
        resp = client.get(f"/api/furniture?room_type={param_val}")
        assert resp.status_code == 200
        items = resp.json()
        assert len(items) >= 8, f"Query '{param_val}' should resolve to {canonical} with >=8 items"

def test_all_catalog_images_exist_and_return_http_200(client):
    """Verify that every catalog record has a valid image_url and static SVGs return HTTP 200."""
    response = client.get("/api/furniture")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 48

    for item in items:
        img_url = item.get("image_url")
        assert img_url, f"Item {item.get('name')} is missing an image_url"
        assert img_url.startswith("/static/furniture/") or img_url.startswith("http"), (
            f"Item {item.get('name')} has unexpected image_url format: {img_url}"
        )

        if img_url.startswith("/static/furniture/"):
            static_resp = client.get(img_url)
            assert static_resp.status_code == 200, (
                f"Static image for {item.get('name')} at {img_url} returned {static_resp.status_code}"
            )
            assert "image/svg+xml" in static_resp.headers.get("content-type", "")

def test_repeated_seeding_is_idempotent_and_preserves_existing_ids(db_session):
    """Verify that calling FurnitureService.seed_catalog multiple times does not duplicate or alter IDs."""
    existing_items = db_session.query(FurnitureItem).all()
    count_before = len(existing_items)
    id_map_before = {item.name: item.id for item in existing_items}

    # Run seed_catalog again
    total_count = FurnitureService.seed_catalog(db_session)
    assert total_count == count_before, f"Expected total count {count_before} on repeated seed, got {total_count}"

    items_after = db_session.query(FurnitureItem).all()
    assert len(items_after) == count_before, "Item count changed after repeated seeding"

    # Verify every pre-existing item's ID remains unchanged
    for item in items_after:
        if item.name in id_map_before:
            assert item.id == id_map_before[item.name], f"ID changed for item '{item.name}'"

def test_filter_furniture_by_category(client):
    """Test filtering by category."""
    response = client.get("/api/furniture?category=Sofa")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 3
    assert all("sofa" in i["category"].lower() for i in items)

def test_filter_furniture_by_price(client):
    """Test filtering by maximum price."""
    response = client.get("/api/furniture?max_price=300")
    assert response.status_code == 200
    items = response.json()
    assert len(items) > 0
    assert all(i["price_estimate"] <= 300 for i in items)

def test_get_furniture_by_id(client):
    """Test fetching a single furniture item by ID."""
    catalog = client.get("/api/furniture").json()
    item_id = catalog[0]["id"]
    response = client.get(f"/api/furniture/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["image_url"] is not None

def test_get_nonexistent_furniture_returns_404(client):
    """Test that requesting an unknown furniture ID returns 404."""
    response = client.get("/api/furniture/non-existent-furniture-uuid")
    assert response.status_code == 404

def test_invalid_room_type_filter_handled_gracefully(client):
    """Test that an unknown room_type query parameter gracefully returns an empty list without 500 error."""
    response = client.get("/api/furniture?room_type=UnknownRoomTypeXYZ123")
    assert response.status_code == 200
    assert response.json() == []

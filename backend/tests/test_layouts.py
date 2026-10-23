def test_recommend_layout(client, dummy_room_image):
    # Create room first
    room_res = client.post(
        "/api/rooms/analyze",
        data={"name": "Layout Test Room", "width_m": 4.0, "length_m": 5.0},
        files={"file": ("room.jpg", dummy_room_image, "image/jpeg")}
    ).json()

    room_id = room_res["id"]
    response = client.post(
        "/api/layouts/recommend",
        json={"room_id": room_id, "room_type": "LivingRoom", "style": "modern"}
    )
    assert response.status_code == 201
    layout = response.json()
    assert layout["room_id"] == room_id
    assert layout["is_recommended"] is True
    assert len(layout["items"]) > 0
    # Verify items have coordinates and placement reasoning
    for item in layout["items"]:
        assert "pos_x" in item
        assert "pos_z" in item
        assert "placement_reason" in item

def test_recommend_layout_tight_room_warning(client, dummy_room_image):
    room_res = client.post(
        "/api/rooms/analyze",
        data={"name": "Compact Room", "width_m": 2.6, "length_m": 2.8},
        files={"file": ("compact.jpg", dummy_room_image, "image/jpeg")}
    ).json()

    response = client.post(
        "/api/layouts/recommend",
        json={"room_id": room_res["id"], "width_m": 2.6, "length_m": 2.8}
    )
    assert response.status_code == 201
    layout = response.json()
    assert any(w["code"] == "TIGHT_DIMENSIONS" for w in layout["warnings"])

def test_save_and_retrieve_custom_layout(client, dummy_room_image):
    room_res = client.post(
        "/api/rooms/analyze",
        data={"name": "Custom Layout Room"},
        files={"file": ("c_room.jpg", dummy_room_image, "image/jpeg")}
    ).json()
    room_id = room_res["id"]

    catalog = client.get("/api/furniture").json()
    f1_id = catalog[0]["id"]

    # Save custom layout
    save_res = client.post(
        "/api/layouts",
        json={
            "room_id": room_id,
            "name": "My Custom Setup",
            "room_type": "Bedroom",
            "items": [
                {"furniture_id": f1_id, "pos_x": 0.5, "pos_y": 0.0, "pos_z": -1.2, "rot_y": 0.0}
            ]
        }
    )
    assert save_res.status_code == 201
    created_id = save_res.json()["id"]

    # Retrieve saved layout
    get_res = client.get(f"/api/layouts/{created_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "My Custom Setup"
    assert len(get_res.json()["items"]) == 1

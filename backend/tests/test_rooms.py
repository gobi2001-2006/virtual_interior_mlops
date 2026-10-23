import io

def test_analyze_room_success(client, dummy_room_image):
    response = client.post(
        "/api/rooms/analyze",
        data={
            "name": "Master Bedroom Test",
            "style_preference": "modern",
            "budget_preference": "medium",
            "width_m": 4.5,
            "length_m": 5.0
        },
        files={"file": ("test_room.jpg", dummy_room_image, "image/jpeg")}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Master Bedroom Test"
    assert "image_path" in data
    assert data["latest_prediction"] is not None
    pred = data["latest_prediction"]
    assert "predicted_room_type" in pred
    assert "confidence" in pred
    assert len(pred["top_predictions"]) > 0

def test_analyze_room_invalid_mimetype(client):
    invalid_file = io.BytesIO(b"dummy text file content")
    response = client.post(
        "/api/rooms/analyze",
        data={"name": "Bad Upload"},
        files={"file": ("test.txt", invalid_file, "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported image type" in response.json()["detail"]

def test_get_rooms(client, dummy_room_image):
    # Upload one room
    client.post(
        "/api/rooms/analyze",
        data={"name": "List Room Test"},
        files={"file": ("room1.jpg", dummy_room_image, "image/jpeg")}
    )
    response = client.get("/api/rooms")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

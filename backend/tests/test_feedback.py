def test_submit_and_summarize_feedback(client, dummy_room_image):
    room_res = client.post(
        "/api/rooms/analyze",
        data={"name": "Feedback Test Room"},
        files={"file": ("fb_room.jpg", dummy_room_image, "image/jpeg")}
    ).json()
    room_id = room_res["id"]

    # Submit positive feedback
    fb1 = client.post(
        "/api/feedback",
        json={
            "room_id": room_id,
            "star_rating": 5,
            "is_liked": True,
            "comments": "Great Scandinavian placement!"
        }
    )
    assert fb1.status_code == 201

    # Submit correction feedback
    fb2 = client.post(
        "/api/feedback",
        json={
            "room_id": room_id,
            "star_rating": 2,
            "is_liked": False,
            "corrected_room_type": "HomeOffice",
            "dissatisfaction_reason": "Wrong room type prediction",
            "comments": "This is actually my home study, not a bedroom."
        }
    )
    assert fb2.status_code == 201
    assert fb2.json()["corrected_room_type"] == "HomeOffice"
    # Verify approval defaults to False for safety
    assert fb2.json()["is_approved_for_training"] is False

    # Check summary
    summary_res = client.get("/api/feedback/summary")
    assert summary_res.status_code == 200
    summary = summary_res.json()
    assert summary["total_feedbacks"] >= 2
    assert summary["total_corrected_room_types"] >= 1
    assert "Wrong room type prediction" in summary["dissatisfaction_reasons_breakdown"]

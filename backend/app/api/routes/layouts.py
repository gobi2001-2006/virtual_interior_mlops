from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.app.db.session import get_db
from backend.app.models.room import Room
from backend.app.models.layout import Layout, LayoutItem
from backend.app.models.furniture import FurnitureItem
from backend.app.schemas.layout import (
    LayoutResponse,
    LayoutCreate,
    LayoutUpdate,
    LayoutRecommendRequest,
    LayoutItemResponse,
    LayoutWarning
)
from backend.app.schemas.furniture import FurnitureResponse
from backend.app.services.layout_service import LayoutEngine

router = APIRouter(prefix="/layouts", tags=["Layouts"])

@router.post("/recommend", response_model=LayoutResponse, status_code=status.HTTP_201_CREATED)
def recommend_layout(payload: LayoutRecommendRequest, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == payload.room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    # Inherit preferences if not provided
    effective_room_type = payload.room_type or room.room_type_preference or "LivingRoom"
    effective_style = payload.style or room.style_preference or "modern"
    effective_budget = payload.budget or room.budget_preference or "medium"
    effective_w = payload.width_m or room.width_m
    effective_l = payload.length_m or room.length_m

    req = LayoutRecommendRequest(
        room_id=room.id,
        room_type=effective_room_type,
        style=effective_style,
        budget=effective_budget,
        width_m=effective_w,
        length_m=effective_l
    )

    rec_res = LayoutEngine.generate_recommendations(db, req)
    if len(rec_res) == 3:
        placements, warnings, model_version = rec_res
    else:
        placements, warnings = rec_res
        model_version = "layout_v001"

    # Persist layout
    layout = Layout(
        room_id=room.id,
        name=f"Recommended {effective_room_type} Layout",
        room_type=effective_room_type,
        style=effective_style,
        budget=effective_budget,
        is_recommended=True,
        layout_model_version=model_version,
        total_cost=sum(p["furniture"].price_estimate for p in placements if p["furniture"])
    )
    db.add(layout)
    db.flush()

    layout_items_res = []
    for p in placements:
        furn: FurnitureItem = p["furniture"]
        item = LayoutItem(
            layout_id=layout.id,
            furniture_id=furn.id,
            pos_x=p["pos_x"],
            pos_y=p["pos_y"],
            pos_z=p["pos_z"],
            rot_y=p["rot_y"],
            placement_reason=p["reason"],
            ml_score=p.get("ml_score")
        )
        db.add(item)
        db.flush()

        item_res = LayoutItemResponse(
            id=item.id,
            layout_id=layout.id,
            furniture_id=furn.id,
            pos_x=item.pos_x,
            pos_y=item.pos_y,
            pos_z=item.pos_z,
            rot_y=item.rot_y,
            scale_x=item.scale_x,
            scale_y=item.scale_y,
            scale_z=item.scale_z,
            placement_reason=item.placement_reason,
            ml_score=item.ml_score,
            furniture=FurnitureResponse.model_validate(furn),
            created_at=item.created_at
        )
        layout_items_res.append(item_res)

    db.commit()
    db.refresh(layout)

    res = LayoutResponse(
        id=layout.id,
        room_id=layout.room_id,
        name=layout.name,
        room_type=layout.room_type,
        style=layout.style,
        budget=layout.budget,
        total_cost=layout.total_cost,
        is_recommended=layout.is_recommended,
        layout_model_version=layout.layout_model_version,
        items=layout_items_res,
        warnings=warnings,
        created_at=layout.created_at,
        updated_at=layout.updated_at
    )
    return res

@router.post("", response_model=LayoutResponse, status_code=status.HTTP_201_CREATED)
def save_custom_layout(payload: LayoutCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == payload.room_id).first()
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")

    layout = Layout(
        room_id=room.id,
        name=payload.name or "My Custom Layout",
        room_type=payload.room_type,
        style=payload.style or "modern",
        budget=payload.budget or "medium",
        is_recommended=False,
        total_cost=0.0
    )
    db.add(layout)
    db.flush()

    total_cost = 0.0
    items_res = []
    for item_data in payload.items:
        furn = db.query(FurnitureItem).filter(FurnitureItem.id == item_data.furniture_id).first()
        if furn:
            total_cost += furn.price_estimate
        item = LayoutItem(
            layout_id=layout.id,
            furniture_id=item_data.furniture_id,
            pos_x=item_data.pos_x,
            pos_y=item_data.pos_y,
            pos_z=item_data.pos_z,
            rot_y=item_data.rot_y,
            scale_x=item_data.scale_x,
            scale_y=item_data.scale_y,
            scale_z=item_data.scale_z,
            placement_reason=item_data.placement_reason or "User placement"
        )
        db.add(item)
        db.flush()
        
        items_res.append(LayoutItemResponse(
            id=item.id,
            layout_id=layout.id,
            furniture_id=item.furniture_id,
            pos_x=item.pos_x,
            pos_y=item.pos_y,
            pos_z=item.pos_z,
            rot_y=item.rot_y,
            scale_x=item.scale_x,
            scale_y=item.scale_y,
            scale_z=item.scale_z,
            placement_reason=item.placement_reason,
            furniture=FurnitureResponse.model_validate(furn) if furn else None,
            created_at=item.created_at
        ))

    layout.total_cost = total_cost
    db.commit()
    db.refresh(layout)

    return LayoutResponse(
        id=layout.id,
        room_id=layout.room_id,
        name=layout.name,
        room_type=layout.room_type,
        style=layout.style,
        budget=layout.budget,
        total_cost=layout.total_cost,
        is_recommended=layout.is_recommended,
        items=items_res,
        warnings=[],
        created_at=layout.created_at,
        updated_at=layout.updated_at
    )

@router.get("/{layout_id}", response_model=LayoutResponse)
def get_layout(layout_id: str, db: Session = Depends(get_db)):
    layout = db.query(Layout).options(
        joinedload(Layout.items).joinedload(LayoutItem.furniture)
    ).filter(Layout.id == layout_id).first()
    
    if not layout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Layout not found")
        
    items_res = []
    for item in layout.items:
        items_res.append(LayoutItemResponse(
            id=item.id,
            layout_id=item.layout_id,
            furniture_id=item.furniture_id,
            pos_x=item.pos_x,
            pos_y=item.pos_y,
            pos_z=item.pos_z,
            rot_y=item.rot_y,
            scale_x=item.scale_x,
            scale_y=item.scale_y,
            scale_z=item.scale_z,
            placement_reason=item.placement_reason,
            furniture=FurnitureResponse.model_validate(item.furniture) if item.furniture else None,
            created_at=item.created_at
        ))

    return LayoutResponse(
        id=layout.id,
        room_id=layout.room_id,
        name=layout.name,
        room_type=layout.room_type,
        style=layout.style,
        budget=layout.budget,
        total_cost=layout.total_cost,
        is_recommended=layout.is_recommended,
        items=items_res,
        warnings=[],
        created_at=layout.created_at,
        updated_at=layout.updated_at
    )

@router.delete("/{layout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_layout(layout_id: str, db: Session = Depends(get_db)):
    layout = db.query(Layout).filter(Layout.id == layout_id).first()
    if not layout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Layout not found")
    db.delete(layout)
    db.commit()
    return None

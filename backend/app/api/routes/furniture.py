from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.furniture import FurnitureResponse, FurnitureCreate
from backend.app.services.furniture_service import FurnitureService
from backend.app.core.security import verify_admin_api_key

router = APIRouter(prefix="/furniture", tags=["Furniture"])

@router.get("", response_model=List[FurnitureResponse])
def get_furniture_catalog(
    category: Optional[str] = Query(None, description="Filter by category (e.g. Sofa, Bed, Desk)"),
    room_type: Optional[str] = Query(None, description="Filter by room suitability (e.g. LivingRoom, Bedroom)"),
    style: Optional[str] = Query(None, description="Filter by style (e.g. Scandinavian, modern)"),
    max_price: Optional[float] = Query(None, description="Maximum price limit"),
    db: Session = Depends(get_db)
):
    items = FurnitureService.get_all(
        db=db,
        category=category,
        room_type=room_type,
        style=style,
        max_price=max_price
    )
    return items

@router.get("/{furniture_id}", response_model=FurnitureResponse)
def get_furniture_item(furniture_id: str, db: Session = Depends(get_db)):
    item = FurnitureService.get_by_id(db, furniture_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Furniture item not found")
    return item

@router.post("", response_model=FurnitureResponse, status_code=status.HTTP_201_CREATED)
def create_furniture_item(
    payload: FurnitureCreate,
    db: Session = Depends(get_db),
    _authorized: bool = Depends(verify_admin_api_key)
):
    return FurnitureService.create(db, payload)

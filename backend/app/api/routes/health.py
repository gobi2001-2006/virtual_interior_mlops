from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.db.session import get_db, db_status
from backend.app.ml.inference import InferenceService

router = APIRouter(prefix="", tags=["Health"])

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "MLOps-Driven Virtual Interior Designer API",
        "version": "1.0.0"
    }

@router.get("/health/ready", status_code=status.HTTP_200_OK)
def readiness_check(db: Session = Depends(get_db)):
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
        
    inference_service = InferenceService.get_instance()
    is_trained = inference_service.is_trained
    
    # If the database had to fall back or is disconnected, mark degraded
    is_fallback = db_status.get("is_fallback", False)
    overall_status = "ready" if (db_ok and not is_fallback) else "degraded"
    
    return {
        "status": overall_status,
        "database_connected": db_ok,
        "active_database_backend": db_status.get("active_backend", "unknown"),
        "is_sqlite_fallback": is_fallback,
        "database_connection_note": db_status.get("connection_error"),
        "inference_engine_ready": True,
        "trained_model_loaded": is_trained,
        "fallback_mode": not is_trained
    }

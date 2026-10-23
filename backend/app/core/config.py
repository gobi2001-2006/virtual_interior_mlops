import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "MLOps-Driven Virtual Interior Designer"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "dev-secret-key-virtual-interior-mlops-2026"
    
    # API
    API_V1_PREFIX: str = "/api"
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    ADMIN_API_KEY: str = "admin-dev-secret-key-2026"
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgrespassword@localhost:5432/virtual_interior_db"
    SQLITE_FALLBACK: bool = True
    SQLITE_DATABASE_URL: str = "sqlite:///./virtual_interior_dev.db"
    
    # Storage & Uploads
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".webp"]
    ALLOWED_MIME_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]
    
    # ML & MLOps
    MODEL_ARTIFACT_DIR: str = str(BASE_DIR / "ml" / "artifacts")
    ACTIVE_MODEL_VERSION: str = "v003"
    MLFLOW_TRACKING_URI: str = str(BASE_DIR / "ml" / "experiments" / "mlruns")
    
    # 6-class room classifier target categories
    TARGET_ROOM_CLASSES: List[str] = [
        "Bedroom",
        "LivingRoom",
        "Kitchen",
        "DiningRoom",
        "Bathroom",
        "HomeOffice"
    ]
    
    # Target room classes in exact canonical order
    ROOM_CLASSES: List[str] = [
        "Bedroom",
        "LivingRoom",
        "Kitchen",
        "DiningRoom",
        "Bathroom",
        "HomeOffice",
        "Other"
    ]
    
    # Retraining threshold
    MIN_APPROVED_FEEDBACK_SAMPLES: int = 10
    EVALUATION_ACCURACY_THRESHOLD: float = 0.50

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_ARTIFACT_DIR, exist_ok=True)
os.makedirs(Path(settings.MLFLOW_TRACKING_URI).parent, exist_ok=True)

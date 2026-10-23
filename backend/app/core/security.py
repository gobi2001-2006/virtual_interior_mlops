import os
import uuid
from pathlib import Path
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from backend.app.core.config import settings

api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)

def verify_admin_api_key(api_key: str = Security(api_key_header)):
    # In development mode, allow if key matches or if header omitted in dev
    if settings.ENVIRONMENT == "development" and not api_key:
        return True
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid or missing Admin API Key"
        )
    return True

def sanitize_filename(original_name: str) -> str:
    ext = Path(original_name).suffix.lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        ext = ".jpg"
    return f"{uuid.uuid4().hex}{ext}"

def is_safe_path(base_dir: str, target_path: str) -> bool:
    base = Path(base_dir).resolve()
    target = Path(target_path).resolve()
    return base in target.parents or base == target

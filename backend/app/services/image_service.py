import os
from pathlib import Path
from PIL import Image
from fastapi import UploadFile, HTTPException, status
from backend.app.core.config import settings
from backend.app.core.security import sanitize_filename, is_safe_path
from backend.app.core.logging import logger

class ImageService:
    @staticmethod
    def validate_image_upload(file: UploadFile) -> None:
        if file.content_type not in settings.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image type '{file.content_type}'. Supported: JPEG, PNG, WebP."
            )

    @staticmethod
    async def save_upload_image(file: UploadFile) -> str:
        """
        Validates image header, checks file integrity via Pillow,
        saves to UPLOAD_DIR with safe filename and returns relative path.
        """
        ImageService.validate_image_upload(file)
        
        safe_name = sanitize_filename(file.filename or "upload.jpg")
        dest_path = Path(settings.UPLOAD_DIR) / safe_name
        
        if not is_safe_path(settings.UPLOAD_DIR, str(dest_path)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file destination")

        content = await file.read()
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Image file exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
            )
            
        dest_path.write_bytes(content)
        
        # Verify it can be opened as an image
        try:
            with Image.open(dest_path) as img:
                img.verify()
        except Exception as e:
            if dest_path.exists():
                dest_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Corrupted or invalid image file: {str(e)}"
            )

        logger.info(f"Successfully saved uploaded room image: {safe_name}")
        return f"/uploads/{safe_name}"

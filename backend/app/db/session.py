import os
from typing import Dict, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import settings
from backend.app.core.logging import logger

db_status: Dict[str, Any] = {
    "configured_backend": "unknown",
    "active_backend": "none",
    "is_fallback": False,
    "connection_error": None,
}

def mask_db_url(url: str) -> str:
    try:
        if "@" in url and "://" in url:
            scheme, rest = url.split("://", 1)
            auth, host_db = rest.split("@", 1)
            user = auth.split(":")[0] if ":" in auth else auth
            return f"{scheme}://{user}:***@{host_db}"
        return url
    except Exception:
        return "database://***"

def get_engine():
    is_sqlite = settings.DATABASE_URL.startswith("sqlite")
    db_status["configured_backend"] = "sqlite" if is_sqlite else "postgresql"
    
    # 1. Explicit SQLite configuration
    if is_sqlite:
        logger.info(f"Using explicitly configured SQLite database: {mask_db_url(settings.DATABASE_URL)}")
        db_status["active_backend"] = "sqlite"
        db_status["is_fallback"] = False
        db_status["connection_error"] = None
        return create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False}
        )

    # 2. PostgreSQL Configuration
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3} if "postgresql" in settings.DATABASE_URL else {}
        )
        with engine.connect() as conn:
            pass
        logger.info(f"Connected successfully to PostgreSQL database: {mask_db_url(settings.DATABASE_URL)}")
        db_status["active_backend"] = "postgresql"
        db_status["is_fallback"] = False
        db_status["connection_error"] = None
        return engine
    except Exception as e:
        error_msg = str(e)
        db_status["connection_error"] = error_msg
        
        # In production or when SQLITE_FALLBACK is disabled, FAIL immediately with a useful error
        if settings.ENVIRONMENT == "production" or not settings.SQLITE_FALLBACK:
            logger.error(
                f"PostgreSQL connection to {mask_db_url(settings.DATABASE_URL)} failed: {error_msg}. "
                "SQLITE_FALLBACK is disabled or ENVIRONMENT is production. Aborting startup."
            )
            raise RuntimeError(f"Database connection failed: {error_msg}")

        # In development mode with explicit fallback enabled:
        logger.warning(
            f"PostgreSQL connection to {mask_db_url(settings.DATABASE_URL)} failed ({error_msg}). "
            f"Development mode active with SQLITE_FALLBACK=true: falling back to local SQLite at {settings.SQLITE_DATABASE_URL}"
        )
        db_status["active_backend"] = "sqlite_fallback"
        db_status["is_fallback"] = True
        return create_engine(
            settings.SQLITE_DATABASE_URL,
            connect_args={"check_same_thread": False}
        )

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

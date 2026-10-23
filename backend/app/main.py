import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging, logger
from backend.app.db.base import Base
from backend.app.db.session import engine, SessionLocal
from backend.app.services.furniture_service import FurnitureService
from backend.app.ml.inference import InferenceService

# Import routers
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.rooms import router as rooms_router
from backend.app.api.routes.furniture import router as furniture_router
from backend.app.api.routes.layouts import router as layouts_router
from backend.app.api.routes.feedback import router as feedback_router
from backend.app.api.routes.mlops import router as mlops_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    
    # Auto-create tables if running in development mode
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

    # Seed furniture catalog
    try:
        with SessionLocal() as db:
            seeded_count = FurnitureService.seed_catalog(db)
            logger.info(f"Furniture catalog verified with {seeded_count} items.")
    except Exception as e:
        logger.error(f"Error seeding furniture catalog: {e}")

    # Warm up inference service
    try:
        inf = InferenceService.get_instance()
        loaded = inf.load_model(settings.ACTIVE_MODEL_VERSION)
        status_msg = "Trained weights loaded" if loaded else "Operating in Demo Fallback mode"
        logger.info(f"Inference engine initialized: {status_msg}")
    except Exception as e:
        logger.warning(f"Inference engine initialization note: {e}")

    yield

    # Shutdown
    logger.info("Application shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="End-to-End MLOps Virtual Interior Designer API with Image Classification, Deterministic Layout Engine, and Retraining Pipeline.",
    lifespan=lifespan
)

# CORS configuration
configured_origins = [o.strip() for o in settings.FRONTEND_ORIGIN.split(",") if o.strip()]
origins = list(set(configured_origins + [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]))

is_wildcard = "*" in origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if is_wildcard else origins,
    allow_origin_regex=r"https?://.*" if not is_wildcard else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads static folder
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount static assets folder (e.g., furniture illustrations)
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API Routers under /api
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(rooms_router, prefix=settings.API_V1_PREFIX)
app.include_router(rooms_router, prefix="/api/v1")
app.include_router(furniture_router, prefix=settings.API_V1_PREFIX)
app.include_router(layouts_router, prefix=settings.API_V1_PREFIX)
app.include_router(feedback_router, prefix=settings.API_V1_PREFIX)
app.include_router(mlops_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "message": "Welcome to MLOps-Driven Virtual Interior Designer API",
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_PREFIX}/health"
    }

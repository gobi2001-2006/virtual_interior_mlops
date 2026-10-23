from backend.app.db.base import Base
from backend.app.db.session import engine, SessionLocal
from backend.app.services.furniture_service import FurnitureService
from backend.app.core.logging import logger, setup_logging

def init_db():
    setup_logging()
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema created.")
    
    with SessionLocal() as db:
        count = FurnitureService.seed_catalog(db)
        logger.info(f"Seeded furniture catalog ({count} items ready).")

if __name__ == "__main__":
    init_db()

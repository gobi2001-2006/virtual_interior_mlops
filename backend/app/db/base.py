from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base

def utc_now():
    return datetime.now(timezone.utc)

Base = declarative_base()

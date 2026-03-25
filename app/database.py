from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy setup with connection pool health checks
# These settings prevent "SSL connection has been closed unexpectedly" errors
# that occur when Neon PostgreSQL drops idle connections after ~5 minutes
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,              # Number of persistent connections
    max_overflow=10,          # Extra connections when pool is full
    pool_timeout=30,          # Seconds to wait for a connection
    pool_recycle=300,         # Recycle connections every 5 minutes (before Neon drops them)
    pool_pre_ping=True,       # Test connection health before using it (auto-reconnect)
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.models import User, Project, ContactMessage, Skill, BlogPost

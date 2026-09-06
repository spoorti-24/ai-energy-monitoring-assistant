"""
PostgreSQL Database Session and Engine setup using SQLAlchemy.
"""
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings


class Base(DeclarativeBase):
    """Base ORM model class inherited by all database models."""
    pass


# Construct database URL safely using URL.create() to handle special characters in DB_PASSWORD
db_url = URL.create(
    drivername="postgresql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

# Create SQLAlchemy database engine
engine = create_engine(
    db_url,
    pool_pre_ping=True
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency generator for FastAPI routes to yield database sessions.
    Automatically closes session after request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

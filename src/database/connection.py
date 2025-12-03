"""
Database connection management
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from src.config import settings
from .models import Base


class Database:
    """Database connection manager"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def initialize(self):
        """Initialize database connection and create tables"""
        database_url = settings.database_url

        # Special handling for SQLite
        if database_url.startswith("sqlite"):
            # Ensure database directory exists
            db_path = database_url.replace("sqlite:///", "")
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

            # Create engine with SQLite-specific settings
            self.engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=settings.database_echo,
            )

            # Enable foreign keys for SQLite
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        else:
            # For PostgreSQL and other databases
            self.engine = create_engine(
                database_url,
                echo=settings.database_echo,
                pool_pre_ping=True,
            )

        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Create all tables
        self.create_tables()

    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        """
        Get a database session

        Returns:
            SQLAlchemy Session
        """
        return self.SessionLocal()

    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()

    def drop_all_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(bind=self.engine)

    def reset_database(self):
        """Reset database (drop all and recreate)"""
        self.drop_all_tables()
        self.create_tables()


# Global database instance
_db = Database()


def get_db() -> Database:
    """
    Get or initialize the database instance

    Returns:
        Database instance
    """
    if _db.engine is None:
        _db.initialize()
    return _db


def get_session() -> Session:
    """
    Get a new database session

    Returns:
        SQLAlchemy Session
    """
    return get_db().get_session()

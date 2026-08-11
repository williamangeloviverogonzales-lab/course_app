import os
from sqlmodel import SQLModel, create_engine, Session

# Use local SQLite DB for development; fallback to Supabase PostgreSQL in production
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./course_app.db"
)

# SQLite requires connect_args for multithreading in FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def init_db():
    """Create all database tables on startup."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency injection helper for database sessions."""
    with Session(engine) as session:
        yield session
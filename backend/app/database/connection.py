import os
from pathlib import Path
from typing import Tuple
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Engine configuration
connect_args = {}
engine_kwargs = {
    "pool_pre_ping": True,
    "echo": False,
}

db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    # Ensure relative SQLite path resolves consistently regardless of current working directory
    if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////") and ":memory:" not in db_url:
        rel_path = db_url.replace("sqlite:///", "")
        backend_dir = Path(__file__).resolve().parent.parent.parent  # backend
        project_root = backend_dir.parent
        # Prefer root if it exists, otherwise backend_dir or default to project_root
        if (project_root / rel_path).exists() and (project_root / rel_path).stat().st_size > 0:
            target_path = (project_root / rel_path).resolve()
        elif (backend_dir / rel_path).exists() and (backend_dir / rel_path).stat().st_size > 0:
            target_path = (backend_dir / rel_path).resolve()
        else:
            target_path = (project_root / rel_path).resolve()
        db_url = f"sqlite:///{target_path.as_posix()}"
else:
    # PostgreSQL connection pooling optimizations
    connect_args["connect_timeout"] = 3
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20
    engine_kwargs["pool_recycle"] = 1800

engine = create_engine(
    db_url,
    connect_args=connect_args,
    **engine_kwargs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_database_connection() -> Tuple[bool, str]:
    """Test the database connection and return (is_healthy, message)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return True, "Connected"
    except Exception as exc:
        return False, str(exc)

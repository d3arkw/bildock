import os

os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5433/auth_db"
)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-ci")

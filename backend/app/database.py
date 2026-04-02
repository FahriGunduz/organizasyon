"""
EOS - Entegre Organizasyon Yönetim Sistemi
Database Configuration Module (Vercel Postgres Destekli)
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Vercel'da POSTGRES_URL environment variable olarak gelir. 
# Eğer yoksa, geçici olarak SQLite kullanılır.
SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL", os.getenv("DATABASE_URL", "sqlite:///./eos_database.db"))

# Postgres için check_same_thread kaldırılmalı
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # Vercel postgres pool fix (neon pgbouncer vb.)
    connect_args = {"sslmode": "require"}
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

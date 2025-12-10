"""
Script to create database tables.
Run this script to initialize the database.
"""
import asyncio
from src.database import engine, Base
from src.models import user, journal, assessment  # Import all models


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        # Создаём все таблицы
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
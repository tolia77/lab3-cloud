from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.settings import settings

# Створення асинхронного двигуна
engine = create_async_engine(
    settings.postgres_url,
    echo=False,  # Встановіть True для дебагу SQL запитів
    future=True
)

# Фабрика сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Базовий клас для ORM моделей
class Base(DeclarativeBase):
    pass

# Міксін для автоматичного додавання created_at та updated_at
class UpdatedMix:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

# Dependency для отримання сесії в роутерах
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
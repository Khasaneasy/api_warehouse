from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncAttrs)
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr,
    Mapped, mapped_column)

from app.config import get_db_url


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Определяем имя таблицы на основе имени класса."""
        return f'{cls.__name__.lower()}s'

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now())


async def create_tables():
    async with async_session_maker():
        await engine.run_sync(Base.metadata.create_all)

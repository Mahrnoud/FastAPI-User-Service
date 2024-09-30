from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_write_session, Base
from ..core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine


async def init_db():
    # Use the write engine for the master database
    engine = create_async_engine(settings.DATABASE_WRITE_URL) if settings.USE_DB_REPLICATION else create_async_engine(
        settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

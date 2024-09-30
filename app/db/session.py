from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

if settings.USE_DB_REPLICATION:
    # Use separate databases for write and read operations
    write_engine = create_async_engine(settings.DATABASE_WRITE_URL, future=True, echo=True)
    read_engine = create_async_engine(settings.DATABASE_READ_URL, future=True, echo=True)
else:
    # Use the default database for both read and write operations
    default_engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Session for write operations
WriteSessionLocal = sessionmaker(
    bind=write_engine if settings.USE_DB_REPLICATION else default_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Session for read operations (HAProxy load-balancing slaves)
ReadSessionLocal = sessionmaker(
    bind=read_engine if settings.USE_DB_REPLICATION else default_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Declare base
Base = declarative_base()


# Dependency injection for FastAPI
async def get_write_session() -> AsyncSession:
    async with WriteSessionLocal() as session:
        yield session


async def get_read_session() -> AsyncSession:
    async with ReadSessionLocal() as session:
        yield session

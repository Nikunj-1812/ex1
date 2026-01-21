"""
Database Configuration and Connection Management
=================================================

Manages connections to PostgreSQL, MongoDB, and Redis.

Author: MAI-PAEP Team
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as aioredis
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# ==========================================
# POSTGRESQL (SQLAlchemy)
# ==========================================

# Convert postgresql:// to postgresql+asyncpg://
ASYNC_POSTGRES_URL = settings.POSTGRES_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create async engine
engine = create_async_engine(
    ASYNC_POSTGRES_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Declarative base for ORM models
Base = declarative_base()


async def get_db():
    """
    Dependency for getting async database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# ==========================================
# MONGODB
# ==========================================

mongodb_client: AsyncIOMotorClient = None
mongodb_database = None


def get_mongodb():
    """
    Get MongoDB database instance.
    
    Returns:
        AsyncIOMotorDatabase: MongoDB database
    """
    return mongodb_database


# ==========================================
# REDIS (Cache)
# ==========================================

redis_client: aioredis.Redis = None


def get_redis():
    """
    Get Redis client instance.
    
    Returns:
        aioredis.Redis: Redis client
    """
    return redis_client


# ==========================================
# CONNECTION MANAGEMENT
# ==========================================

async def init_db():
    """
    Initialize all database connections.
    Called on application startup.
    """
    global mongodb_client, mongodb_database, redis_client
    
    try:
        # PostgreSQL - tables will be created by migrations
        logger.info("Connecting to PostgreSQL...")
        async with engine.begin() as conn:
            # Create tables if they don't exist
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ PostgreSQL connected")
        
        # MongoDB
        logger.info("Connecting to MongoDB...")
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        mongodb_database = mongodb_client[settings.MONGODB_DB]
        # Test connection
        await mongodb_database.command("ping")
        logger.info("✅ MongoDB connected")
        
        # Redis
        logger.info("Connecting to Redis...")
        redis_client = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        # Test connection
        await redis_client.ping()
        logger.info("✅ Redis connected")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def close_db():
    """
    Close all database connections.
    Called on application shutdown.
    """
    global mongodb_client, redis_client
    
    try:
        # Close PostgreSQL
        await engine.dispose()
        logger.info("PostgreSQL connection closed")
        
        # Close MongoDB
        if mongodb_client:
            mongodb_client.close()
            logger.info("MongoDB connection closed")
        
        # Close Redis
        if redis_client:
            await redis_client.close()
            logger.info("Redis connection closed")
            
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")

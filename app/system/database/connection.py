from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.system.config import Config as config


SQLALCHEMY_DATABASE_URL:str = config.DATABASE_URL

if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace('sqlite:///', 'sqlite+aiosqlite:///')

elif SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')

if 'postgresql+asyncpg://' in SQLALCHEMY_DATABASE_URL:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, 
                                 pool_size=10, 
                                 max_overflow=20, 
                                 pool_timeout=30, 
                                 pool_pre_ping=True, 
                                 echo=True)
    
    Session = sessionmaker(autocommit=False, 
                           autoflush=False, 
                           bind=engine, 
                           class_=AsyncSession, 
                           expire_on_commit=False)

elif 'sqlite:///' in SQLALCHEMY_DATABASE_URL:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, 
                                 pool_pre_ping=True, 
                                 echo=True)
    
    Session = sessionmaker(autocommit=False, 
                           autoflush=False, 
                           bind=engine, 
                           class_=AsyncSession)

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

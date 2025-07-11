from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    # ⬅️ IMPORTA tus modelos aquí para que SQLAlchemy cree las tablas
    from app.models.route import Route, Segment

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

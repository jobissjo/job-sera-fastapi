from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Updated database URL with async driver
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./db/job-sera.db"

# Use declarative_base for ORM models
Base = declarative_base()

# Create async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create async session
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

# Dependency for getting a database session
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


def create_table(table_model:any):
    try:
        table_model.create(engine)
    except IntegrityError as e:
        print(f"{e}")
    except Exception:
        ...

async def create_tables():
    async with engine.begin() as conn:
        # This runs the create_all method within the async context
        await conn.run_sync(Base.metadata.create_all)
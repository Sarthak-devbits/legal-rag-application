from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine , async_sessionmaker

engine= create_async_engine(
    settings.database_urlm,
    echo= settings.app_env == "development"
)

AsyncSessionLocal= async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit= False
    # expire_on_commit=False — by default SQLAlchemy expires all objects after a commit, meaning you'd have to re-fetch them from DB. Setting this to False keeps your objects usable after committing — important for async code
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# 1. get_db() starts
# 2. opens a fresh session
# 3. yield session → PAUSES, hands session to route handler
# 4. route handler runs:
#        user = await session.execute(...)
#        documents = await session.execute(...)
# 5. route handler returns response
# 6. get_db() RESUMES after yield
# 7. commits the transaction
# 8. session automatically closes
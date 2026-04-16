import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
# Think of context like Alembic's global state object
from alembic import context
from app.db.base import Base
from app.core.config import settings
# This forces Python to load all model files, which registers them with Base.metadata. Without this Alembic would see an empty database schema and generate blank migrations.
from app.models import document, user, job, chunk

config= context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata

def run_migrations_offline()-> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online()-> None:
    connectable= create_async_engine(settings.database_url)
    
    async with connectable.connect() as connection:
        await connection.run_sync(lambda sync_conn : context.configure(
            connection= sync_conn,
            target_metadata=target_metadata
        ) )
        
        async with connection.begin():
            await connection.run_sync(lambda _:context.run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
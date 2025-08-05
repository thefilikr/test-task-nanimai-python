import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

# from app.utils.db.base import Base
from db.base import Base
from app.balance.models import Balance
from app.user.models import User
from app.transaction.models import Transaction, TransactionStatus


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = create_async_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    async def do_run_migrations(connection):
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn, target_metadata=target_metadata
            )
        )
        await connection.run_sync(
            lambda sync_conn: context.run_migrations()
        )

    import asyncio
    async def run():
        async with connectable.connect() as connection:
            await do_run_migrations(connection)
        await connectable.dispose()

    asyncio.run(run())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

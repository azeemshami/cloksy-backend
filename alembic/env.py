
import os
from dotenv import load_dotenv
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.environ.get("DB_USER", "root"))
config.set_section_option(section, "DB_PASSWORD", os.environ.get("DB_PASSWORD", "root"))
config.set_section_option(section, "DB_HOST", os.environ.get("DB_HOST", "localhost"))
config.set_section_option(section, "DB_NAME", os.environ.get("DB_NAME", "aiwhis"))
config.set_section_option(section, "DB_PORT", os.environ.get("DB_PORT", "8888"))


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

fileConfig(context.config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support.
target_metadata = Base.metadata

connectable = create_async_engine(DATABASE_URL, echo=True)

async def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    """Define the synchronous migration context configuration."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    context.configure(url=DATABASE_URL)
    with context.begin_transaction():
        context.run_migrations()
else:
    import asyncio
    asyncio.run(run_migrations_online())

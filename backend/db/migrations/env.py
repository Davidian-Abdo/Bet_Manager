# backend/db/migrations/env.py

from __future__ import with_statement
import os,sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# make sure project root is on PYTHONPATH for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in os.sys.path:
    os.sys.path.insert(0, project_root)
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from backend.db.base import Base
from backend.core.config import settings


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# overwrite sqlalchemy.url with runtime settings (from .env via settings)
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # FORCE TCP/IP CONNECTION - This is the fix for Windows
    connection_string = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    from sqlalchemy import create_engine
    # Create engine with explicit TCP/IP connection
    connectable = create_engine(
        connection_string,
        connect_args={}  # Ensure no socket connection
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
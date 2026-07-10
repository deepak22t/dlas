from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import get_settings
from app.database.base import Base

# Import all models here
import app.models
from sqlalchemy.exc import OperationalError
import sys

settings = get_settings()

config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.database_url,
)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    try:
        engine = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()

    except OperationalError as e:
        print("\n❌ Unable to connect to PostgreSQL.\n")

        message = str(e.orig)

        if "Connection refused" in message:
            print("Possible reasons:")
            print("  • PostgreSQL container is not running.")
            print("  • Port 5432 is not exposed.")
            print("  • POSTGRES_HOST or POSTGRES_PORT is incorrect.")
        elif "password authentication failed" in message:
            print("Possible reasons:")
            print("  • POSTGRES_USER is incorrect.")
            print("  • POSTGRES_PASSWORD is incorrect.")
        elif "database" in message and "does not exist" in message:
            print("Possible reasons:")
            print("  • Database does not exist.")
        else:
            print(message)

        sys.exit(1)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
from sqlalchemy import engine_from_config, pool

from alembic import context

from app.config import settings
from app.database import Base
import app.models  # noqa: F401 -- side-effect import, registers every model on Base.metadata

# Alembic's Config object -- gives access to values in alembic.ini, plus lets us
# override them here in real Python (alembic.ini is plain text, it can't reference
# settings.DATABASE_URL directly).
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Skipping fileConfig(config.config_file_name) here on purpose -- that call expects
# [loggers]/[handlers]/[formatters] sections in alembic.ini, which this project's
# minimal alembic.ini doesn't define. Add those sections later if you want Alembic's
# logging configured; migrations work fine without it.

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Generate SQL scripts without a live DB connection (`alembic upgrade head --sql`)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Connect to the real DB and apply migrations -- the normal case."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

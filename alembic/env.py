import logging
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from models import Base  # Adjust according to your project structure
from config import DATABASE_URL  # Import your DATABASE_URL from the config

# Ensure that you define target_metadata
target_metadata = Base.metadata  # This is your metadata for Alembic

# Logging setup (necessary for Alembic)
fileConfig(context.config.config_file_name)  # This loads logging configuration from alembic.ini
logger = logging.getLogger('alembic.env')  # Create a logger for Alembic

def run_migrations_online():
    # Set up the connection to your database using SQLAlchemy engine
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    # Open a connection and run migrations
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata  # Pass target_metadata here
        )

        with context.begin_transaction():
            context.run_migrations()

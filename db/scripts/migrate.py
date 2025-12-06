import sys
import os
import logging

# Import psycopg2 to handle the database creation command
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from yoyo import read_migrations, get_backend

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from backend.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("db_migration")
load_dotenv()


def get_env_vars():
    """Helper to get vars to reuse in creation and migration"""
    return {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
    }


def create_database_if_not_exists():
    """
    Connects to the default 'postgres' database to check if the target DB exists.
    If not, creates it.
    """
    env = get_env_vars()
    target_db_name = env["dbname"]
    try:
        conn = psycopg2.connect(
            user=env["user"],
            password=env["password"],
            host=env["host"],
            port=env["port"],
            database="postgres",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (target_db_name,)
        )
        exists = cursor.fetchone()
        if not exists:
            logger.info(f"Database '{target_db_name}' does not exist. Creating it...")
            cursor.execute(f"CREATE DATABASE {target_db_name}")
            logger.info(f"Database '{target_db_name}' created successfully.")
        else:
            logger.debug(f"Database '{target_db_name}' already exists.")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.warning(
            f"Could not create database automatically (this might be due to permissions or the DB already existing): {e}"
        )


def get_db_url():
    env = get_env_vars()
    if not all(env.values()):
        logger.critical("Missing database credentials in .env file")
        sys.exit(1)

    logger.debug(
        f"Connecting to database at {env['host']}:{env['port']}/{env['dbname']}"
    )
    return f"postgresql://{env['user']}:{env['password']}@{env['host']}:{env['port']}/{env['dbname']}"


def apply_migrations():
    create_database_if_not_exists()
    logger.info("Starting database migration process...")
    db_url = get_db_url()
    try:
        backend = get_backend(db_url)
        migrations = read_migrations(
            os.path.join(os.path.dirname(__file__), "../migrations")
        )
        to_apply = backend.to_apply(migrations)
        if not to_apply:
            logger.info("Database is already up to date.")
            return
        logger.info(f"Applying {len(to_apply)} migrations...")
        backend.apply_migrations(to_apply)
        logger.info("Migrations applied successfully.")

    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    apply_migrations()
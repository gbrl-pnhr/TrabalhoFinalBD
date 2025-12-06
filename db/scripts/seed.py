import sys
import os
import logging
import psycopg2
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from backend.core.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("db_seed")
load_dotenv()

SEED_DIR = os.path.join(os.path.dirname(__file__), "../seeds")


def get_db_connection():
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        logger.critical(f"Failed to connect to DB: {e}")
        sys.exit(1)


def apply_seeds():
    global filename
    if not os.path.exists(SEED_DIR):
        logger.error(f"Seed directory not found: {SEED_DIR}")
        logger.error("Run 'taskipy generate_seeds' first.")
        sys.exit(1)
    files = sorted([f for f in os.listdir(SEED_DIR) if f.endswith(".sql")])
    if not files:
        logger.warning("No .sql files found in seeds directory.")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    logger.info(f"Found {len(files)} seed files. Starting application...")
    try:
        for filename in files:
            file_path = os.path.join(SEED_DIR, filename)
            logger.info(f"Executing {filename}...")
            with open(file_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            if sql_content.strip():
                cursor.execute(sql_content)
        conn.commit()
        logger.info("All seeds applied successfully!")

    except Exception as e:
        conn.rollback()
        logger.error(f"Error applying seed {filename}: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_seeds()
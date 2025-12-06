import typer
import sys

from packages.common.src.log_config import setup_logging
from .operations import apply_migrations, reset_database, generate_seeds, apply_seeds
from .config import logger

app = typer.Typer(help="Database management CLI for TrabalhoFinalBD")

@app.command()
def migrate():
    """Apply database migrations."""
    try:
        apply_migrations()
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)

@app.command()
def reset(force: bool = False):
    """Reset the database (rollback and re-apply migrations)."""
    if not force:
        confirm = typer.prompt("\n⚠️ WARNING: This will DELETE ALL DATA. Type 'yes' to confirm")
        if confirm.lower() != 'yes':
            logger.info("Reset cancelled.")
            return
    try:
        reset_database()
    except Exception as e:
        logger.error(f"Reset failed: {e}")
        sys.exit(1)

@app.command()
def generate_seeds():
    """Generate seed SQL files."""
    try:
        generate_seeds()
    except Exception as e:
        logger.error(f"Seed generation failed: {e}")
        sys.exit(1)

@app.command()
def seed():
    """Apply generated seed SQL files."""
    try:
        apply_seeds()
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_logging(app_name="db_cli", log_dir=None)
    app()
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

class FrontendSettings(BaseSettings):
    """
    Frontend specific settings.
    Falls back to defaults if .env is missing or variables are unset.
    """
    API_BASE_URL: str = "http://localhost:8000/api/v1"
    PAGE_TITLE: str = "Restaurant Manager"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=True,
        extra="ignore"
    )

settings = FrontendSettings()
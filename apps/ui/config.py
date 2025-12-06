from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

class FrontendSettings(BaseSettings):
    """
    Frontend configuration.
    Values can be overridden by environment variables in .env file.
    Example in .env: API_BASE_URL=http://192.168.1.5:8000/api/v1
    """
    API_BASE_URL: str = "http://localhost:8000/api/v1"
    API_TIMEOUT: int = 10
    PAGE_TITLE: str = "Restaurant Manager"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=True,
        extra="ignore"
    )

settings = FrontendSettings()
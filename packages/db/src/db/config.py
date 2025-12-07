import logging
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class DBSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    API_BASE_URL: str
    API_TIMEOUT: int
    PAGE_TITLE: str
    PROJECT_NAME: str

    @property
    def database_url(self) -> str:
        logger.debug(f"Connecting to database at 'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'")
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = DBSettings()
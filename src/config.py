from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    PRIVATE_KEY_NAME: str
    PUBLIC_KEY_NAME: str
    CERTS_DIRECTORY_NAME: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_LIFETIME: int = 15
    REFRESH_TOKEN_LIFETIME: int = 30

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    REDIS_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def PRIVATE_KEY_PATH(self):
        return BASE_DIR / self.CERTS_DIRECTORY_NAME / self.PRIVATE_KEY_NAME

    @property
    def PUBLIC_KEY_PATH(self):
        return BASE_DIR / self.CERTS_DIRECTORY_NAME / self.PUBLIC_KEY_NAME

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file='../.env')


load_dotenv(find_dotenv('../.env'))
settings = Settings()

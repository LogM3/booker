from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import NullPool


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    DB_NAME: str
    TEST_DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str

    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int
    SECRET_KEY: str

    REDIS_URL: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    @property
    def database_url(self) -> str:
        db_name: str = (
            self.TEST_DB_NAME if self.MODE == 'TEST' else self.DB_NAME
        )
        return (
            f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}/{db_name}'
        )

    @property
    def database_params(self) -> dict:
        return {'poolclass': NullPool} if self.MODE == 'TEST' else {}

    model_config = SettingsConfigDict(env_file='.env')


settings: Settings = Settings()

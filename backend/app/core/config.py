from functools import cached_property
from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl, computed_field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # CORE SETTINGS
    SECRET_KEY: str
    ENVIRONMENT: Literal["DEV", "PYTEST", "STG", "PRD"] = "DEV"
    SECURITY_BCRYPT_ROUNDS: int = 12
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 40320  # 28 days
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # PROJECT NAME, VERSION AND DESCRIPTION
    PROJECT_NAME: str
    VERSION: str
    DESCRIPTION: str

    # MONGODB
    DEFAULT_DATABASE_HOSTNAME: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    DEFAULT_DATABASE_PORT: int
    DEFAULT_DATABASE_DB: str

    # FIRST SUPERUSER
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    # PULSEFIRE SETTINGS
    RIOT_API_KEY: str
    RATELIMITER_HOST: str = "localhost"
    RATELIMITER_PORT: int = 12227

    @computed_field
    @cached_property
    def DEFAULT_MONGODB_URI(self) -> str:
        return str(
            MongoDsn.build(
                scheme="mongodb",
                host=self.DEFAULT_DATABASE_HOSTNAME,
                username=self.MONGO_INITDB_ROOT_USERNAME,
                password=self.MONGO_INITDB_ROOT_PASSWORD,
                port=self.DEFAULT_DATABASE_PORT,
            )
        )
    
    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env", case_sensitive=True
    )


settings: Settings = Settings()  # type: ignore

from enum import StrEnum
from pathlib import Path

from pydantic import BaseSettings, SecretStr


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Settings for the application. Get settings from .env file.
    """

    APP_TITLE = "InNoHassle Events API"
    APP_DESCRIPTION = "API of Events project in InNoHassle Ecosystem."
    APP_VERSION = "0.1.0"

    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # You can run 'openssl rand -hex 32' to generate keys
    SESSION_SECRET_KEY: SecretStr
    JWT_SECRET_KEY: SecretStr

    # PostgreSQL database connection URL
    DB_URL: SecretStr

    # Authentication
    AUTH_COOKIE_DOMAIN: str = (
        "innohassle.ru" if ENVIRONMENT == Environment.PRODUCTION else "localhost"
    )

    # Use these only in production
    INNOPOLIS_SSO_CLIENT_ID: SecretStr = ""
    INNOPOLIS_SSO_CLIENT_SECRET: SecretStr = ""
    INNOPOLIS_SSO_REDIRECT_URI: str = (
        "https://innohassle.campus.innopolis.university/oauth2/callback"
    )

    # Use dev auth while development
    DEV_AUTH_EMAIL: str = ""

    PREDEFINED_USERS_FILE: Path = Path(
        "src/repositories/users/innopolis_user_data.json"
    )

    PREDEFINED_GROUPS_FILE: Path = Path("src/repositories/users/predefined_groups.json")

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()

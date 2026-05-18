# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app
from models.logging import LoggingLevel


class Settings(BaseSettings):
    """Налаштування сервера та логування."""

    logging_level: LoggingLevel | None = None

    model_config = SettingsConfigDict(
        env_file=app.settings.env_file,
        env_prefix="SERVER__",
        extra="ignore",
    )


settings = Settings()

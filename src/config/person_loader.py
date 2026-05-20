# -*- coding: utf-8 -*-

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app


class Settings(BaseSettings):
    """Налаштування завантажувача персон"""

    db_dir: Path = app.settings.database_dir
    db_filename: str = "persons.yaml"
    images_dir: Path = app.settings.assets_dir / "images" / "persons"
    default_image_filename: str = "slovohr-ai.png"

    model_config = SettingsConfigDict(
        env_file=app.settings.env_file,
        env_prefix="PERSONS_LOADER__",
        extra="ignore",
    )


settings = Settings()

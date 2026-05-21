# -*- coding: utf-8 -*-

import os
from importlib.metadata import metadata
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

meta = metadata("slovohr-ai")


class Settings(BaseSettings):
    """Основні налаштування програми."""

    @staticmethod
    def get_asset_dir() -> Path:
        """Повертає шлях до директорії з ресурсами."""
        default_assets_dir = Path(__file__).resolve().parent.parent / "assets"
        return Path(os.environ.get("FLET_ASSETS_DIR", default_assets_dir)).resolve()

    name: str = meta["name"]
    version: str = meta["version"]
    license: str = meta["License-Expression"]

    base_url: str = ""

    assets_dir: Path = get_asset_dir()

    env_file: Path = assets_dir / ".env"
    database_dir: Path = assets_dir / "database"
    images_dir: Path = assets_dir / "images" / "characters"

    characters_filename: str = "characters.yaml"
    global_prompt_filename: str = "global_prompt.yaml"

    default_character_image_filename: str = "slovohr-ai.png"
    default_character_name: str = "Словограй"
    default_character_prompt: str = ""

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_prefix="APP__",
        extra="ignore",
    )


settings = Settings()

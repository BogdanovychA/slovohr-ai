# -*- coding: utf-8 -*-

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app


class Settings(BaseSettings):
    """Налаштування завантажувача"""

    prompts_dir: Path = app.settings.assets_dir / "database"
    system_prompts_filename: str = "system_prompts.yaml"
    base_system_prompt_filename: str = "base_system_prompt.yaml"

    model_config = SettingsConfigDict(
        env_file=app.settings.env_file,
        env_prefix="PROMPTS_LOADER__",
        extra="ignore",
    )


settings = Settings()

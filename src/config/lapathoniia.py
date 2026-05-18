# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app


class Settings(BaseSettings):
    '''Налаштування Lapathoniia'''

    key: str = ""
    base_url: str = "https://api.lapathoniia.top"

    models: dict[str, str] = {
        "lapa": "LapaLLM-Gemma-3-12B-v0.1.2-instruct",
        "mamay": "MamayLM-Gemma-3-12B-IT-v1.0",
    }

    model_config = SettingsConfigDict(
        env_file=app.settings.env_file,
        env_prefix="LAPATHONIIA__",
        extra="ignore",
    )


settings = Settings()

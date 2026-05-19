# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app
from models.ai_model import AIModel


class Settings(BaseSettings):
    """Налаштування Lapathoniia"""

    api_key: str = ""
    base_url: str = "https://api.lapathoniia.top"
    max_tokens: int = 500
    temperature: float = 1.0

    models_dict: dict[AIModel, str] = {
        AIModel.MAMAY: "MamayLM-Gemma-3-12B-IT-v1.0",
        AIModel.LAPA: "LapaLLM-Gemma-3-12B-v0.1.2-instruct",
    }

    model_key: AIModel = AIModel.MAMAY

    model_config = SettingsConfigDict(
        env_file=app.settings.env_file,
        env_prefix="LAPATHONIIA__",
        extra="ignore",
    )


settings = Settings()

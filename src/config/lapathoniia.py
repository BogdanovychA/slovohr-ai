# -*- coding: utf-8 -*-

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config import app
from models.ai_model import AIModel


class Settings(BaseSettings):
    """Налаштування Lapathoniia"""

    api_key: str = ""
    base_url: str = "https://api.lapathoniia.top"
    max_tokens: int = 1000
    temperature: float = 0.7
    stream: bool = True

    model_key: AIModel = AIModel.MAMAY

    lapa: str = ""
    mamay: str = ""

    @computed_field
    @property
    def models_dict(self) -> dict[AIModel, str]:
        return {
            AIModel.MAMAY: self.mamay,
            AIModel.LAPA: self.lapa,
        }

    model_config = SettingsConfigDict(
        env_file=app.settings.env_file,
        env_prefix="LAPATHONIIA__",
        extra="ignore",
    )


settings = Settings()

if __name__ == "__main__":
    print(settings)

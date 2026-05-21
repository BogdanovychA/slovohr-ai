# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.ai_model import AIModel

import logging

from openai import AsyncOpenAI, AuthenticationError, RateLimitError

from utils import utils

logger = logging.getLogger(__name__)


class Lapathoniia:
    """Клієнт для взаємодії з API Lapathoniia (OpenAI-сумісний сервіс)."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        max_tokens: int,
        temperature: float,
        models_dict: dict[AIModel, str],
        model_key: AIModel,
    ):
        """Ініціалізація клієнта та налаштувань підключення до API."""

        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.models_dict = models_dict
        self.model_key = model_key

    @property
    def model(self):
        """Повертає назву моделі за поточним ключем."""
        return self.models_dict[self._model_key]

    @property
    def model_key(self):
        """Повертає поточний обраний ключ моделі."""
        return self._model_key

    @model_key.setter
    def model_key(self, value: str):
        """Встановлює новий ключ моделі після валідації."""
        if value not in self.models_dict:
            raise ValueError(f"Model with key '{value}' not found in models_dict.")
        self._model_key = value

    @utils.api_timer
    async def query(self, system_prompt: str, user_prompt: str) -> str:
        """Надсилає асинхронний запит до LLM моделі та повертає текстову відповідь."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                n=1,
            )

            message = response.choices[0].message
            text = message.content.strip() if message.content else ""

            if text == "":
                logger.warning("Empty message")

        except AuthenticationError as e:
            text = "Некоректний API-ключ. Повідомте розробника."
            logger.warning("AuthenticationError: %s", e)

        except RateLimitError as e:
            text = (
                "Перевищено ліміт звернень до мовної моделі. Спробуйте ще раз пізніше."
            )
            logger.warning("RateLimitError: %s", e)

        except Exception as e:
            text = "Неочікувана помилка. Повідомте розробника."
            logger.exception("Unexpected error: %s", e)

        return text

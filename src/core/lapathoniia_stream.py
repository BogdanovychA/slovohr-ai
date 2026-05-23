# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
from typing import Any, AsyncGenerator, cast

from openai import AsyncOpenAI, AuthenticationError, RateLimitError

from models.ai_model import AIModel

logger = logging.getLogger(__name__)


class LapathoniiaStream:
    """Клієнт для потокової взаємодії з API Lapathoniia (OpenAI-сумісний сервіс)."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        max_tokens: int,
        temperature: float,
        models_dict: dict[AIModel, str],
        model_key: AIModel | str,
    ) -> None:
        """Ініціалізація клієнта та налаштувань підключення до API."""

        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.models_dict = models_dict
        self.model_key = model_key

    @property
    def model(self) -> str:
        """Повертає назву моделі за поточним ключем."""
        return self.models_dict[self._model_key]

    @property
    def model_key(self) -> AIModel:
        """Повертає поточний обраний ключ моделі."""
        return self._model_key

    @model_key.setter
    def model_key(self, value: AIModel | str) -> None:
        """Встановлює новий ключ моделі після валідації."""
        try:
            model_enum = AIModel(value)
        except ValueError:
            raise ValueError(f"Model with key '{value}' not found in models_dict.")

        if model_enum not in self.models_dict:
            raise ValueError(f"Model with key '{value}' not found in models_dict.")
        self._model_key = model_enum

    async def query(
        self, system_prompt: str, user_prompt: str
    ) -> AsyncGenerator[str, None]:
        """Надсилає асинхронний запит до LLM моделі та повертає відповідь у вигляді потоку чанків."""

        messages = cast(  # Щоб PyCharm не сварився :)
            Any,
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        try:
            stream = cast(  # Щоб PyCharm не сварився :)
                Any,
                await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    stream=True,
                    n=1,
                ),
            )

            async for chunk in stream:
                if chunk.choices:
                    text = chunk.choices[0].delta.content
                    if text:
                        yield text

        except AuthenticationError as e:
            logger.warning("AuthenticationError: %s", e)
            yield "Некоректний API-ключ. Повідомте розробника."

        except RateLimitError as e:
            logger.warning("RateLimitError: %s", e)
            yield "Перевищено ліміт звернень до мовної моделі. Спробуйте ще раз пізніше."

        except Exception as e:
            logger.exception("Unexpected error: %s", e)
            yield "Неочікувана помилка. Повідомте розробника."

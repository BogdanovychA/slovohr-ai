# -*- coding: utf-8 -*-

import logging

from openai import AsyncOpenAI, AuthenticationError, RateLimitError

from config import lapathoniia as l9a_config
from utils import utils

logger = logging.getLogger(__name__)


class Lapathoniia:

    MAX_TOKENS = 1000
    TEMPERATURE = 0.7

    def __init__(self, model: str):

        self.client = AsyncOpenAI(
            api_key=l9a_config.settings.key, base_url=l9a_config.settings.base_url
        )

        self.model = model

    @utils.api_timer
    async def query(self, system_prompt: str, user_prompt: str) -> str:

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.MAX_TOKENS,
                temperature=self.TEMPERATURE,
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


if __name__ == "__main__":
    import asyncio

    import yaml

    from config import app

    prompt_file = app.settings.assets_dir / "database" / "prompts.yaml"

    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)

    async def main():

        l9a = Lapathoniia(l9a_config.settings.models["mamay"])

        print(await l9a.query(prompts["ukrainka"], "Розкажи про Україну"))

    asyncio.run(main())

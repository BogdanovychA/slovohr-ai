# -*- coding: utf-8 -*-

import logging

import openai

from config import lapathoniia as l9a_config

logger = logging.getLogger(__name__)


class Lapathoniia:

    MAX_TOKENS = 1000
    TEMPERATURE = 0.7

    def __init__(self, model: str):

        self.client = openai.AsyncOpenAI(
            api_key=l9a_config.settings.key, base_url=l9a_config.settings.base_url
        )

        self.model = model

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

        except openai.AuthenticationError as e:
            text = "Не коректний API-ключ. Повідомте розробника."
            logger.warning("AuthenticationError in %s: %s", e)

        except openai.RateLimitError as e:
            text = (
                "Перевищено ліміт звернень до мовної моделі. Спробуйте ще раз пізніше."
            )
            logger.warning("ClientError in %s: %s", str(e))

        except Exception as e:
            text = "Неочікувана помилка. Повідомте розробника."
            logger.exception("Unexpected error in %s")

        return text


if __name__ == "__main__":
    import asyncio

    import yaml

    from config import app

    prompt_file = app.settings.assets_dir / "data" / "prompts.yaml"

    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)

    async def main():

        l9a = Lapathoniia(l9a_config.settings.models["mamay"])

        print(await l9a.query(prompts["ukrainka"], "Розкажи про Україну"))

    asyncio.run(main())

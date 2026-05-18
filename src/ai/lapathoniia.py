# -*- coding: utf-8 -*-

import logging

from openai import AsyncOpenAI

from config import lapathoniia as l9a_config

logger = logging.getLogger(__name__)


class Lapathoniia:

    MAX_TOKENS = 1000
    TEMPERATURE = 0.7

    def __init__(self, model: str):

        self.client = AsyncOpenAI(
            api_key=l9a_config.settings.key, base_url=l9a_config.settings.base_url
        )

        self.model = model

    async def query(self, system_prompt: str, user_prompt: str) -> str:

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.MAX_TOKENS,
            temperature=self.TEMPERATURE,
            n=1,
        )

        message = response.choices[0].message
        text = message.content.strip() if message.content else ""

        return text


if __name__ == "__main__":
    import asyncio

    async def main():

        l9a = Lapathoniia(l9a_config.settings.models["mamay"])
        print(
            await l9a.query("Використовуй закарпатський суржик", "Розкажи про Україну")
        )

    asyncio.run(main())

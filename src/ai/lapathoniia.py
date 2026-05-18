# -*- coding: utf-8 -*-

import logging

from openai import OpenAI

from config import lapathoniia as l9a_config

logger = logging.getLogger(__name__)


class Lapathoniia:
    def __init__(self, model: str):

        self.client = OpenAI(
            api_key=l9a_config.settings.key, base_url=l9a_config.settings.base_url
        )

        self.model = model

    def query(self, system_prompt: str, user_prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        return response.choices[0].message.content


if __name__ == "__main__":
    l9a = Lapathoniia(l9a_config.settings.models["mamay"])
    print(l9a.query("Використовуй Markdown-розмітку", "Розкажи про Україну"))

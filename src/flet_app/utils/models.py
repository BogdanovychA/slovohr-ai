# -*- coding: utf-8 -*-

from dataclasses import dataclass

from flet_storage import FletStorage

from abstract.prompt_loader import BasePromptLoader
from core.lapathoniia import Lapathoniia


@dataclass
class PandorasBox:
    """Контейнер для зберігання основних об'єктів та стану застосунку"""

    storage: FletStorage
    l9a: Lapathoniia
    prompt_loader: BasePromptLoader
    system_prompts_dict: dict
    base_system_prompt: str = ""

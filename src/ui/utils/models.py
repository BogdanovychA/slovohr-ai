# -*- coding: utf-8 -*-

from dataclasses import dataclass

from flet_storage import FletStorage

from ai.lapathoniia import Lapathoniia


@dataclass
class PandorasBox:
    """Контейнер для зберігання основних об'єктів та стану застосунку"""

    storage: FletStorage
    l9a: Lapathoniia

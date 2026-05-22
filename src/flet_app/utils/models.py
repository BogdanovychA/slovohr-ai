# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_storage import FletStorage
    from measurement_api import MeasurementAPI

    from core.lapathoniia import Lapathoniia
    from models.character import Character, CharacterDictKey

from dataclasses import dataclass


@dataclass
class PandorasBox:
    """Контейнер для зберігання основних об'єктів та стану застосунку"""

    storage: FletStorage
    l9a: Lapathoniia
    characters_dict: dict[CharacterDictKey | str, Character]
    global_prompt: str
    m9t: MeasurementAPI
    client_id: str
    client_platform: str

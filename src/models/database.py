# -*- coding: utf-8 -*-

from enum import StrEnum


class CharacterKey(StrEnum):
    """Ключі полів налаштувань персонажа в базі даних (YAML)."""

    IMAGE = "image_filename"
    NAME = "name"
    PROMPT = "prompt"

# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import logging

from models.character import Character, CharacterDictKey
from models.database import CharacterKey

logger = logging.getLogger(__name__)


class CharacterManager:
    """Менеджер для створення та управління об'єктами персонажів."""

    def __init__(
        self,
        default_character_image_filename: str,
        default_character_name: str,
        default_character_prompt: str,
        images_dir: Path,
        characters_dict: dict[str, dict[CharacterKey, str]],
    ) -> None:
        """Ініціалізує менеджер персонажів та створює дефолтного персонажа."""

        self.images_dir = images_dir
        self.characters_dict = characters_dict

        self.default_character = Character(
            image_filepath=self.images_dir / default_character_image_filename,
            name=default_character_name,
            prompt=default_character_prompt,
        )

    def create_dict(self) -> dict[CharacterDictKey | str, Character]:
        """Будує та повертає словник персонажів із валідованими даними."""

        result: dict[CharacterDictKey | str, Character] = {
            CharacterDictKey.DEFAULT: self.default_character,
        }

        for key, value in self.characters_dict.items():
            character = Character(
                image_filepath=self.images_dir / value[CharacterKey.IMAGE],
                name=value[CharacterKey.NAME],
                prompt=value[CharacterKey.PROMPT],
            )

            result[key] = character

        return result

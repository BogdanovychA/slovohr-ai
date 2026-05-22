from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.character import Character, CharacterDictKey

from abc import ABC, abstractmethod

from config import app
from core.character_manager import CharacterManager
from core.yaml_manager import CharacterYamlManager


class BaseCharacterLoader(ABC):
    """Абстрактний базовий клас для завантажувача конфігурацій персонажів."""

    @abstractmethod
    def create_dict(self) -> dict[CharacterDictKey | str, Character]:
        """Створює словник з персонажами"""
        pass


class CharacterLoader(BaseCharacterLoader):
    """Клас для завантаження та менеджменту персонажів із конфігураційних файлів."""

    def __init__(self) -> None:
        """Ініціалізація завантажувача персонажів з YAML та менеджера їх властивостей."""

        self.data_manager = CharacterYamlManager(
            database_dir=app.settings.database_dir,
            filename=app.settings.characters_filename,
        )

        self.character_manager = CharacterManager(
            default_character_image_filename=app.settings.default_character_image_filename,
            default_character_name=app.settings.default_character_name,
            default_character_prompt=app.settings.default_character_prompt,
            images_dir=app.settings.images_dir,
            characters_dict=self.data_manager.create_dict(),
        )

    def create_dict(self) -> dict[CharacterDictKey | str, Character]:
        """Повертає сформований та валідований словник об'єктів персонажів."""
        return self.character_manager.create_dict()

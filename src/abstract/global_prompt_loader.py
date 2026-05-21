# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from config import app
from core.yaml_manager import GlobalPromptYamlManager


class BaseGlobalPromptLoader(ABC):
    """Абстрактний базовий клас для завантажувача глобальних промптів."""

    @abstractmethod
    def get_prompt(self) -> str:
        """Повертає глобальний промпт"""
        pass


class GlobalPromptLoader(BaseGlobalPromptLoader):
    """Клас для завантаження глобального промпту з YAML файлу."""

    def __init__(self) -> None:
        """Ініціалізація завантажувача та менеджера YAML."""
        self.manager = GlobalPromptYamlManager(
            database_dir=app.settings.database_dir,
            filename=app.settings.global_prompt_filename,
        )

    def get_prompt(self) -> str:
        """Зчитує та повертає глобальний системний промпт."""
        return self.manager.get_prompt()


if __name__ == "__main__":
    loader = GlobalPromptLoader()
    print(loader.get_prompt())

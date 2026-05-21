# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from config import app
from core.yaml_manager import GlobalPromptYamlManager


class BaseGlobalPromptLoader(ABC):

    @abstractmethod
    def get_prompt(self) -> str:
        """Повертає глобальний промпт"""
        pass


class GlobalPromptLoader(BaseGlobalPromptLoader):

    def __init__(self) -> None:
        self.manager = GlobalPromptYamlManager(
            database_dir=app.settings.database_dir,
            filename=app.settings.global_prompt_filename,
        )

    def get_prompt(self) -> str:
        return self.manager.get_prompt()


if __name__ == "__main__":
    loader = GlobalPromptLoader()
    print(loader.get_prompt())

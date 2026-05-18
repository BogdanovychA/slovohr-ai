# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

from abc import ABC, abstractmethod

from config import app
from utils import utils


class BasePromptLoader(ABC):

    @abstractmethod
    def load(self) -> dict[str, str]:
        """Завантажує наявні промпти"""
        pass


class YamlPromptLoader(BasePromptLoader):
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> dict[str, str]:
        prompts = utils.read_yaml_file(self.file_path)
        if not prompts:
            return {"no_prompt": ""}
        return prompts


if __name__ == "__main__":
    loader = YamlPromptLoader(app.settings.assets_dir / "data" / "prompts.yaml")
    print(loader.load())

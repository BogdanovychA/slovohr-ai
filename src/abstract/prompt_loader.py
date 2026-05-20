# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import logging
from abc import ABC, abstractmethod

from models.prompt import PromptKey, PromptValue
from utils import utils

logger = logging.getLogger(__name__)


class BasePromptLoader(ABC):

    @abstractmethod
    def load_system_prompts(self) -> dict[str, str]:
        """Завантажує наявні системні промпти"""
        pass

    @abstractmethod
    def load_base_system_prompt(self) -> str:
        """Завантажує базовий системний промпт"""
        pass


class YamlPromptLoader(BasePromptLoader):
    def __init__(
        self,
        prompts_dir: Path,
        system_prompts_filename: str,
        base_system_prompt_filename: str,
    ) -> None:
        self.prompts_dir = prompts_dir
        self.system_prompts_filename = system_prompts_filename
        self.base_system_prompt_filename = base_system_prompt_filename

    def load_system_prompts(self) -> dict[str, str]:

        prompts = utils.read_yaml_file(self.prompts_dir / self.system_prompts_filename)

        return {PromptKey.EMPTY: PromptValue.EMPTY, **prompts}

    def load_base_system_prompt(self) -> str:

        try:
            prompts = utils.read_yaml_file(
                self.prompts_dir / self.base_system_prompt_filename
            )
            prompts_list = list(prompts.values())
            base_system_prompt = prompts_list[0]

        except IndexError as e:
            base_system_prompt = ""
            logger.warning("IndexError: %s", e)
        except Exception as e:
            base_system_prompt = ""
            logger.exception("Unexpected error: %s", e)

        return base_system_prompt


if __name__ == "__main__":

    from config import prompt_loader

    loader = YamlPromptLoader(**prompt_loader.settings.model_dump())

    print("load_system_prompts:", f"->{loader.load_system_prompts()}<-")
    print("load_base_system_prompt:", f"->{loader.load_base_system_prompt()}<-")

# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import logging

from models.database import CharacterKey
from utils import utils

logger = logging.getLogger(__name__)


class CharacterYamlManager:
    def __init__(self, database_dir: Path, filename: str) -> None:

        self.database_dir = database_dir
        self.filename = filename

    def create_dict(self) -> dict[str, dict[CharacterKey, str]]:

        raw_dict = utils.read_yaml_file(self.database_dir / self.filename)

        result = {}

        for key, value in raw_dict.items():

            is_filename = CharacterKey.IMAGE in value
            is_name = CharacterKey.NAME in value
            is_prompt = CharacterKey.PROMPT in value

            if is_filename and is_name and is_prompt:
                result[key] = value

        return result


class GlobalPromptYamlManager:
    def __init__(self, database_dir: Path, filename: str) -> None:

        self.database_dir = database_dir
        self.filename = filename

    def get_prompt(self) -> str:

        try:
            raw_list = utils.read_yaml_file(self.database_dir / self.filename)
            prompts_list = list(raw_list.values())
            prompt = prompts_list[0]

        except IndexError as e:
            prompt = ""
            logger.warning("IndexError: %s", e)

        except Exception as e:
            prompt = ""
            logger.exception("Unexpected error: %s", e)

        return prompt

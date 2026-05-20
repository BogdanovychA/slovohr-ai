# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import logging
from abc import ABC, abstractmethod

from models.prompt import PromptKey
from utils import utils

logger = logging.getLogger(__name__)


class BasePersonLoader(ABC):

    @abstractmethod
    def load_person_image_paths(self) -> dict[str, Path]:
        """Завантажує картинки персонажей"""
        pass

    @property
    @abstractmethod
    def default_image_path(self) -> Path:
        pass


class YamlPersonLoader(BasePersonLoader):
    def __init__(
        self,
        db_dir: Path,
        db_filename: str,
        images_dir: Path,
        default_image_filename: str,
    ) -> None:
        self.db_dir = db_dir
        self.db_filename = db_filename
        self.images_dir = images_dir
        self.default_image_filename = default_image_filename

    def load_person_image_paths(self) -> dict[str, Path]:
        images_dict = utils.read_yaml_file(self.db_dir / self.db_filename)

        result = {PromptKey.EMPTY: self.default_image_path}

        if isinstance(images_dict, dict):
            result.update({k: self.images_dir / v for k, v in images_dict.items()})

        return result

    @property
    def default_image_path(self) -> Path:
        return self.images_dir / self.default_image_filename


if __name__ == "__main__":

    from config import person_loader

    loader = YamlPersonLoader(**person_loader.settings.model_dump())

    print("load_person_images:", loader.load_person_image_paths())
    print("default_image_path:", f"->{loader.default_image_path}<-")

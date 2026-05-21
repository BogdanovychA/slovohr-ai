# -*- coding: utf-8 -*-

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel


class Character(BaseModel):
    name: str
    prompt: str
    image_filepath: Path


class CharacterDictKey(StrEnum):
    DEFAULT = "default"

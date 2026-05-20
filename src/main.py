# -*- coding: utf-8 -*-

import logging

import flet as ft

from config import app, server
from flet_app.main import main

logging.basicConfig(
    level=server.settings.logging_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ft.run(main, assets_dir=app.settings.assets_dir)

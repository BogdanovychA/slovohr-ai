# -*- coding: utf-8 -*-

import flet as ft

from config import app
from ui.main import main

if __name__ == "__main__":
    ft.run(main, assets_dir=app.settings.assets_dir)

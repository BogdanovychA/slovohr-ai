# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.utils.models import PandorasBox

import flet as ft

from config import app
from ui.utils import elements, style

ROUTE = app.settings.base_url + "/404"


def build_view(page: ft.Page, box: PandorasBox) -> ft.View:
    """Будує вікно для відображення помилки 404 (Сторінка не знайдена)"""

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar("Сторінка не знайдена", page),
            ft.Text(""),
            ft.Text("Сторінка не знайдена", size=style.settings.text_size),
            ft.Text(f"Цільова сторінка: {page.route}"),
            ft.Text(""),
            elements.back_button(page, "Назад"),
        ],
    )

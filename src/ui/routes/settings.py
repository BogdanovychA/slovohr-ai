# -*- coding: utf-8 -*-

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.utils.models import PandorasBox

import flet as ft

from config import app
from ui.utils import elements, style

ROUTE = app.settings.base_url + "/settings"
TITLE = "Налаштування"


def button(page, text: str) -> ft.Button:
    """Створює кнопку для переходу до екрану налаштувань"""
    return ft.Button(
        text,
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


async def build_view(
    page: ft.Page,
    box: PandorasBox,
) -> ft.View:
    """Будує вікно для введення даних про звернення громадянина"""

    page.title = TITLE

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Text(TITLE, size=style.settings.text_size),
            ft.Text(""),
            elements.back_button(page, "Назад"),
        ],
    )

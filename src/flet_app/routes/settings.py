# -*- coding: utf-8 -*-

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_app.utils.models import PandorasBox

import flet as ft

from config import app, lapathoniia
from flet_app.utils import elements, style

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
    """Будує вікно налаштувань"""

    def _switch_model():
        box.l9a.model_key = model_switcher.value

    model_switcher = ft.Dropdown(
        label_style=ft.TextStyle(size=style.settings.text_size),
        width=400,
        options=[
            ft.DropdownOption(key=k, text=v)
            for k, v in lapathoniia.settings.models.items()
        ],
        value=box.l9a.model_key,
        label="Поточна ШІ модель",
        on_select=_switch_model,
    )

    page.title = TITLE

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            model_switcher,
            ft.Text(""),
            elements.back_button(page, "Назад"),
        ],
    )

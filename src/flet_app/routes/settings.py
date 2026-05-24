# -*- coding: utf-8 -*-

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_app.utils.models import PandorasBox

import flet as ft

from config import app
from flet_app.utils import elements, style
from flet_app.utils import utils as ft_utils

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
        """Оновлює ключ використовуваної моделі в налаштуваннях."""
        box.l9a.model_key = model_switcher.value

    def _switch_stream():
        box.l9a.stream = True if stream_switcher.value == "True" else False

    def _change_tokens_block():
        """Оновлює ліміт максимальної кількості токенів
        у налаштуваннях та інтерфейсі.
        """
        box.l9a.max_tokens = int(tokens_slider.value)
        ft_utils.set_attr(tokens_block, "value", f"Токени: {box.l9a.max_tokens}")

    def _change_temperature():
        """Оновлює параметр температури (креативності) моделі
        в налаштуваннях та інтерфейсі.
        """
        box.l9a.temperature = round(float(temperature_slider.value), 1)
        ft_utils.set_attr(
            temperature_block, "value", f"Температура: {box.l9a.temperature}"
        )

    model_switcher = ft.Dropdown(
        label_style=ft.TextStyle(size=style.settings.text_size),
        width=350,
        options=[
            ft.DropdownOption(key=k, text=v) for k, v in box.l9a.models_dict.items()
        ],
        value=box.l9a.model_key,
        label="Поточна ШІ модель",
        on_select=_switch_model,
    )

    temperature_block = ft.Text(
        f"Температура: {box.l9a.temperature}",
        size=style.settings.text_size,
    )

    temperature_slider = ft.Slider(
        width=350,
        min=0.5,
        max=1.0,
        divisions=5,
        value=box.l9a.temperature,
        on_change=_change_temperature,
    )

    tokens_block = ft.Text(
        f"Токени: {box.l9a.max_tokens}",
        size=style.settings.text_size,
    )

    tokens_slider = ft.Slider(
        width=350,
        min=500,
        max=1000,
        divisions=5,
        value=box.l9a.max_tokens,
        on_change=_change_tokens_block,
    )

    stream_options_dict = {"True": "Стрімінг", "False": "Чат"}

    stream_switcher = ft.Dropdown(
        label_style=ft.TextStyle(size=style.settings.text_size),
        width=250,
        options=[
            ft.DropdownOption(key=k, text=v) for k, v in stream_options_dict.items()
        ],
        value=str(box.l9a.stream),
        label="Режим роботи",
        on_select=_switch_stream,
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
            temperature_block,
            temperature_slider,
            ft.Text(""),
            tokens_block,
            tokens_slider,
            ft.Text(""),
            stream_switcher,
            ft.Text(""),
            elements.back_button(page, "Назад"),
        ],
    )

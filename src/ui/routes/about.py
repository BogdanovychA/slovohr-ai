# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.utils.models import PandorasBox

import asyncio

import flet as ft

from config import app
from ui.utils import elements, style

ROUTE = app.settings.base_url + "/about"
TITLE = "Про застосунок"


def button(page, text: str) -> ft.Button:
    """Створює кнопку для переходу на сторінку "Про застосунок" """
    return ft.Button(
        text,
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


def build_view(page: ft.Page, box: PandorasBox) -> ft.View:
    """Будує вікно з інформацією про застосунок"""
    page.title = TITLE
    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text("Slovohr.AI (Словограй)", size=style.settings.text_size),
            ft.Text(f"Версія: {app.settings.version}"),
            ft.Text(f"Ліцензія: {app.settings.license}"),
            ft.Text(""),
            ft.Image(
                src="/images/slovohr-ai_logo.png",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                "Проєкт створений в межах бета-тесту Lapathoniia — першого українського LLM інференс-провайдера.",
                size=style.settings.text_size,
            ),
            ft.Text(""),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        "Гітхаб",
                        "https://github.com/BogdanovychA/slovohr-ai",
                    ),
                ],
            ),
            ft.Text(""),
            ft.Image(
                src="/images/lapathoniia_logo.jpeg",
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        "Lapathoniia",
                        "https://lapathoniia.top/",
                    ),
                ],
            ),
            ft.Text(""),
            elements.back_button(page, "Назад"),
        ],
    )

# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flet_app.utils.models import PandorasBox

import asyncio

import flet as ft

from config import app
from flet_app.utils import elements, style

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
            ft.Image(
                src="/images/slovohr-ai_logo.png",
                width=200,
                height=200,
            ),
            ft.Text(
                "Мінімалістичний чат-інтерфейс, "
                "створений для демонстрації можливостей Lapathoniia",
                size=style.settings.text_size,
            ),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        "Slovohr.AI на Github",
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
            ft.Text(
                "Lapathoniia — перший український LLM інференс провайдер.",
                size=style.settings.text_size,
            ),
            ft.Text(
                size=style.settings.text_size,
                spans=[
                    elements.link(
                        "Сайт Lapathoniia",
                        "https://lapathoniia.top/",
                    ),
                ],
            ),
            ft.Text(""),
            elements.back_button(page, "Назад"),
        ],
    )

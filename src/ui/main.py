# -*- coding: utf-8 -*-

import asyncio
import logging

import flet as ft
from flet_storage import FletStorage

from abstract.prompt_loader import YamlPromptLoader
from config import app, lapathoniia, server
from core.lapathoniia import Lapathoniia
from ui.routes import about, author, error404, root, settings
from ui.utils import elements, style
from ui.utils.models import PandorasBox

logging.basicConfig(
    level=server.settings.logging_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
# logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def build_main_view(
    page: ft.Page,
    box: PandorasBox,
) -> ft.View:
    """Будує головне вікно"""

    page.title = root.TITLE

    message_block = ft.Text(
        default_message_text := "Введіть свій запит",
        size=style.settings.text_size,
    )

    return ft.View(
        route=root.ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE, page),
            message_block,
            ft.Text(""),
            ft.Row(
                controls=[
                    author.button(page, "Про автора"),
                    about.button(page, "Про застосунок"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )


async def main(page: ft.Page):
    """Головна функція ініціалізації та запуску Flet-застосунку"""

    async def route_change():
        """Обробляє зміну маршруту сторінки"""

        page.views.clear()
        page.views.append(await build_main_view(page, box))

        match page.route:
            case author.ROUTE:
                page.views.append(author.build_view(page, box))
            case about.ROUTE:
                page.views.append(about.build_view(page, box))
            case settings.ROUTE:
                page.views.append(await settings.build_view(page, box))
            case _:
                if page.route != root.ROUTE:
                    page.views.append(error404.build_view(page, box))

        page.update()

    async def view_pop(e):
        """Обробляє повернення на попередню сторінку"""
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    box = PandorasBox(
        storage=FletStorage(app.settings.name),
        l9a=Lapathoniia(lapathoniia.settings.models["mamay"]),
        prompt_loader=YamlPromptLoader(
            app.settings.assets_dir / "data" / "prompts.yaml"
        ),
    )

    # await asyncio.sleep(0.2)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await route_change()

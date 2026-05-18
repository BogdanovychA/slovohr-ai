# -*- coding: utf-8 -*-

import asyncio
import logging

import flet as ft
from flet_storage import FletStorage

from abstract.prompt_loader import YamlPromptLoader
from config import app, lapathoniia, server
from core.lapathoniia import Lapathoniia
from flet_app.routes import about, author, error404, root, settings
from flet_app.utils import elements, style
from flet_app.utils.models import PandorasBox

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

    async def _ok() -> None:
        pass

    async def _rerun() -> None:
        pass

    page.title = root.TITLE

    info_block = ft.Text(
        f"Модель: {box.l9a.model}",
        size=style.settings.text_size,
    )

    message_block = ft.Text(
        default_message_text := "Введіть свій запит",
        size=style.settings.text_size,
    )

    form = ft.TextField(
        label="Запит",
        value="",
        hint_text="Запит до LLM",
        width=400,
        bgcolor=style.settings.form_bg_color,
        border_color=style.settings.form_border_color,
    )

    return ft.View(
        route=root.ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE, page),
            info_block,
            ft.Text(""),
            message_block,
            ft.Text(""),
            form,
            ft.Text(""),
            ft.Row(
                buttons_block := [
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                    ft.IconButton(ft.Icons.DONE_OUTLINE, on_click=_ok),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
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

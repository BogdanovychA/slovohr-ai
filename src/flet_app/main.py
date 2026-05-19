# -*- coding: utf-8 -*-

import logging

import flet as ft
from flet_storage import FletStorage

from abstract.prompt_loader import YamlPromptLoader
from config import app, lapathoniia, server
from core.lapathoniia import Lapathoniia
from flet_app.routes import about, author, error404, root, settings
from flet_app.utils import elements, style
from flet_app.utils import utils as ft_utils
from flet_app.utils.models import PandorasBox
from models.prompt import PromptKey

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

        try:
            ft_utils.set_attr(request_block, "disabled", True)
            ft_utils.set_attr(buttons_block, "disabled", True)

            system_prompt = system_prompts_dict[prompt_switcher.value]
            if request_block.value == "":
                ft_utils.set_attr(message_block, "value", "Запит не може бути пустим")
                return

            ft_utils.set_attr(message_block, "value", "Опрацювання запиту...")

            answer = await box.l9a.query(system_prompt, request_block.value)
            ft_utils.set_attr(answer_block, "value", answer)

            ft_utils.set_attr(message_block, "value", default_message_text)
            ft_utils.set_attr(request_block, "value", "")

        finally:
            ft_utils.set_attr(request_block, "disabled", False)
            ft_utils.set_attr(buttons_block, "disabled", False)

    async def _rerun() -> None:
        ft_utils.set_attr(message_block, "value", default_message_text)
        ft_utils.set_attr(request_block, "value", "")
        ft_utils.set_attr(answer_block, "value", "")

    model_block = ft.Text(
        f"Модель: {box.l9a.model}, температура: {box.l9a.temperature}, токени: {box.l9a.max_tokens}",
    )

    def _create_prompt_switcher_options() -> list[ft.DropdownOption]:
        prompts_dict = system_prompts_dict.copy()
        prompts_dict[PromptKey.EMPTY] = "Без системного промпту"
        return [ft.DropdownOption(key=k, text=v) for k, v in prompts_dict.items()]

    system_prompts_dict = box.prompt_loader.load()
    prompt_switcher_option = _create_prompt_switcher_options()

    prompt_switcher = ft.Dropdown(
        label_style=ft.TextStyle(size=style.settings.text_size),
        width=400,
        options=prompt_switcher_option,
        value=PromptKey.EMPTY,
        label="Системний промпт",
        # on_select=,
    )

    message_block = ft.Text(
        default_message_text := "Оберіть системний промпт та введіть свій запит",
        size=style.settings.text_size,
    )

    answer_block = ft.TextField(
        label="Тут буде відповідь",
        value="",
        multiline=True,
        min_lines=3,
        max_lines=10,
        width=400,
        bgcolor=style.settings.form_bg_color,
        border_color=style.settings.form_border_color,
        # disabled=True,
    )

    request_block = ft.TextField(
        label="Запит до ШІ",
        value="",
        hint_text="Запит до Lapathoniia",
        multiline=True,
        min_lines=3,
        max_lines=10,
        width=400,
        bgcolor=style.settings.form_bg_color,
        border_color=style.settings.form_border_color,
    )

    page.title = root.TITLE

    return ft.View(
        route=root.ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE, page),
            ft.Text(""),
            model_block,
            ft.Text(""),
            prompt_switcher,
            ft.Text(""),
            message_block,
            ft.Text(""),
            answer_block,
            request_block,
            ft.Text(""),
            buttons_block := ft.Row(
                [
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
        l9a=Lapathoniia(**lapathoniia.settings.model_dump()),
        prompt_loader=YamlPromptLoader(
            app.settings.assets_dir / "database" / "prompts.yaml"
        ),
    )

    # await asyncio.sleep(0.2)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await route_change()

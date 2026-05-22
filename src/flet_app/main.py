# -*- coding: utf-8 -*-


import asyncio
import logging
import uuid

import flet as ft
from flet_storage import FletStorage
from measurement_api import MeasurementAPI

from abstract.character_loader import CharacterLoader
from abstract.global_prompt_loader import GlobalPromptLoader
from config import app, lapathoniia
from config import measurement_api as m9t_config
from core.lapathoniia import Lapathoniia
from flet_app.routes import about, author, error404, root, settings
from flet_app.utils import elements, style
from flet_app.utils import utils as ft_utils
from flet_app.utils.models import PandorasBox
from models.character import CharacterDictKey
from models.logging import Analytics, EventName

logger = logging.getLogger(__name__)


async def build_main_view(
    page: ft.Page,
    box: PandorasBox,
) -> ft.View:
    """Будує головне вікно"""

    def _get_person_image(key: str) -> str:
        """Повертає відносний шлях до зображення (аватара) персонажа."""
        default_image_path = box.characters_dict[
            CharacterDictKey.DEFAULT
        ].image_filepath
        assets_dir = app.settings.assets_dir

        raw_path = box.characters_dict[key].image_filepath
        image_path = raw_path if raw_path else default_image_path

        if image_path.is_file():
            return str(image_path.relative_to(assets_dir))
        else:
            return str(default_image_path.relative_to(assets_dir))

    async def _change_person_picture():
        """Оновлює зображення персонажа на формі відповідно до вибору."""

        ft_utils.set_attr(
            person_picture, "src", _get_person_image(str(prompt_switcher.value))
        )
        await _rerun()

    async def _ok() -> None:
        """Опрацьовує надсилання текстового запиту користувача до обраного персонажа."""

        try:
            ft_utils.set_attr(request_block, "disabled", True)
            ft_utils.set_attr(buttons_block, "disabled", True)
            ft_utils.set_attr(prompt_switcher, "disabled", True)

            if request_block.value == "":
                ft_utils.set_attr(message_block, "value", "Запит не може бути пустим")
                return

            ft_utils.set_attr(message_block, "value", "Опрацювання запиту...")
            ft_utils.set_attr(answer_block, "disabled", True)

            custom_system_prompt = box.characters_dict[
                str(prompt_switcher.value)
            ].prompt
            final_system_prompt = f"{box.global_prompt}\n\n{custom_system_prompt}"

            answer = await box.l9a.query(final_system_prompt, request_block.value)

            await box.m9t.log_event(
                box.client_id,
                EventName.QUERY_SENT,
                character=str(prompt_switcher.value),
                model=box.l9a.model_key,
                max_tokens=box.l9a.max_tokens,
                temperature=box.l9a.temperature,
                platform=box.client_platform,
            )

            ft_utils.set_attr(answer_block, "value", answer)
            ft_utils.set_attr(answer_block, "disabled", False)

            ft_utils.set_attr(message_block, "value", default_message_text)
            ft_utils.set_attr(request_block, "value", "")

        finally:
            ft_utils.set_attr(request_block, "disabled", False)
            ft_utils.set_attr(buttons_block, "disabled", False)
            ft_utils.set_attr(prompt_switcher, "disabled", False)

    async def _rerun() -> None:
        """Очищує текстове поле відповіді та скидає стан діалогу."""
        ft_utils.set_attr(message_block, "value", default_message_text)
        ft_utils.set_attr(request_block, "value", "")
        ft_utils.set_attr(answer_block, "value", "")
        ft_utils.set_attr(answer_block, "disabled", True)

    model_block = ft.Text(
        f"Модель: {box.l9a.model}, "
        f"температура: {box.l9a.temperature}, "
        f"токени: {box.l9a.max_tokens}",
    )

    def _create_prompt_switcher_options() -> list[ft.DropdownOption]:
        """Формує список персонажів для випадаючого меню."""
        return [
            ft.DropdownOption(key=k, text=v.name)
            for k, v in box.characters_dict.items()
        ]

    prompt_switcher_option = _create_prompt_switcher_options()

    prompt_switcher = ft.Dropdown(
        label_style=ft.TextStyle(size=style.settings.text_size),
        width=400,
        options=prompt_switcher_option,
        value=CharacterDictKey.DEFAULT,
        label="Персонаж",
        on_select=_change_person_picture,
    )

    message_block = ft.Text(
        default_message_text := "Оберіть персонажа та введіть свій запит",
        size=style.settings.text_size,
    )

    answer_block = ft.TextField(
        label="Відповідь персонажа",
        value="",
        multiline=True,
        read_only=True,
        min_lines=5,
        max_lines=20,
        width=400,
        bgcolor=style.settings.form_bg_color,
        border_color=style.settings.form_border_color,
        disabled=True,
    )

    request_block = ft.TextField(
        label="Запит до ШІ Lapathoniia",
        hint_text="Запит до персонажа",
        value="",
        multiline=True,
        min_lines=2,
        max_lines=5,
        width=400,
        bgcolor=style.settings.form_bg_color,
        border_color=style.settings.form_border_color,
    )

    person_picture = ft.Image(
        src=_get_person_image(str(prompt_switcher.value)),
        width=200,
        height=200,
    )

    page.title = root.TITLE

    return ft.View(
        route=root.ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE, page),
            person_picture,
            message_block,
            ft.Text(""),
            prompt_switcher,
            answer_block,
            model_block,
            ft.Text(""),
            request_block,
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

        await box.m9t.log_event(
            box.client_id,
            EventName.ROUTE_CHANGE,
            page_path=page.route,
            platform=box.client_platform,
        )

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

    character_loader = CharacterLoader()
    global_prompt_loader = GlobalPromptLoader()

    box = PandorasBox(
        storage=FletStorage(app.settings.name),
        l9a=Lapathoniia(**lapathoniia.settings.model_dump()),
        characters_dict=character_loader.create_dict(),
        global_prompt=global_prompt_loader.get_prompt(),
        m9t=MeasurementAPI(**m9t_config.settings.model_dump()),
        client_id="",
        client_platform=page.platform.value if page.platform else Analytics.NO_PLATFORM,
    )

    await asyncio.sleep(0.2)

    try:
        box.client_id = await box.storage.get_or_default("client_id", str(uuid.uuid4()))
        if not await box.storage.contains_key("client_id"):
            await box.storage.set("client_id", box.client_id)
    except RuntimeError:
        logger.exception("Error reading client_id data")
        box.client_id = str(uuid.uuid4())

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await route_change()

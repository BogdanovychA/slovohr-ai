# Slovohr.AI — Agent Guide

## Stack

- **Python 3.12** · **Flet 0.85** (Flutter-based Python UI framework, not web/CLI)
- **LLM client**: `openai` AsyncOpenAI → [Lapathoniia](https://lapathoniia.top) (Ukrainian provider)
- **Package manager**: `uv` (not pip/poetry)

## Commands

```sh
uv sync                         # install deps (project + dev)
uv run python src/main.py       # run locally (launches Flet window)
docker compose up -d            # run in container → http://localhost:8009
ruff check src/                 # lint (rules E, F, I; ignores E501)
ruff format src/                # format (line-length 88, quote-style preserve)
pre-commit run --all-files      # full hook suite (lint+format+whitespace+yaml)
```

## Tests & Type Checking

**None configured.** No `tests/` directory, no pytest, no mypy/pyright/pytype. Do not add or run them.

## Architecture

| Layer | Path | Role |
|---|---|---|
| Entrypoint | `src/main.py` | Calls `ft.run(main, assets_dir=...)` |
| UI | `src/flet_app/` | Flet routes, views, utils |
| Config | `src/config/` | pydantic-settings singletons (see below) |
| Models | `src/models/` | Pydantic models + enums |
| Core | `src/core/` | LLM interaction, YAML parsing, managers |
| Data | `src/assets/database/` | YAML files (`characters.yaml`, `global_prompt.yaml`) — no database |

**Data is YAML-only, in-memory at runtime.** No ORM, no migrations, no DB.

## Config

All settings load from `src/assets/.env` via pydantic-settings. Each module uses a unique prefix:

| Module | Env prefix | Key vars |
|---|---|---|
| `config/app.py` | `APP__` | paths, version |
| `config/lapathoniia.py` | `LAPATHONIIA__` | `API_KEY`, `BASE_URL`, model IDs |
| `config/server.py` | `SERVER__` | `LOGGING_LEVEL` |
| `config/measurement_api.py` | `GOOGLE_ANALYTICS__` | `SECRET_KEY`, `ID` |

The root `.env` only has `APP_VERSION=v0.2.0` (for Docker compose). The real env is `src/assets/.env`.

**⚠️ `src/assets/.env` contains live API keys committed to the repo.** Treat with care.

## Conventions

- **UI is entirely in Ukrainian** — code comments, strings, error messages.
- **Dark mode only** — `page.theme_mode = ft.ThemeMode.DARK`.
- **Flet `View` / Route-based navigation** — views in `src/flet_app/routes/`.
- **Characters defined in YAML** — each has name, prompt, and avatar image (no model override).
- **Dockerfile** uses `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` builder + `python:3.12-slim-bookworm` final image, timezone `Europe/Kyiv`.

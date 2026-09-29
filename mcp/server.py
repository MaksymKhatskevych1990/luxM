"""MCP-сервер публічного контенту сайту Forma / LuxMeb.

Читає живий Django API (за замовчуванням http://127.0.0.1:8000/api).
Секрети адмінки та заявки з форми сюди не потрапляють: публічне API їх не віддає.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from mcp.server.fastmcp import FastMCP

DEFAULT_API_URL = "http://127.0.0.1:8000/api"

mcp = FastMCP(
    "luxmeb",
    instructions=(
        "Доступ лише на читання до публічного контенту сайту меблів на замовлення "
        "(бренд, SEO, секції, проєкти, матеріали, процес, майстерня). "
        "Дані беруться з живого API, а не з коду. "
        "Заявки клієнтів, токени Telegram і паролі адмінки недоступні. "
        "Якщо API недоступне, попросіть запустити ./run.sh."
    ),
)


class ApiError(RuntimeError):
    pass


def api_base() -> str:
    return os.environ.get("LUXMEB_API_URL", DEFAULT_API_URL).rstrip("/")


def dumps(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def api_get(path: str):
    url = f"{api_base()}/{path.lstrip('/')}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "luxmeb-mcp/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise ApiError(f"HTTP {exc.code} для {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ApiError(
            "Бекенд сайту недоступний. Запустіть його командою ./run.sh "
            f"(очікується {api_base()}). Деталі: {exc.reason}"
        ) from exc


def as_list(payload) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return payload["results"]
    return []


def project_summary(item: dict) -> dict:
    return {
        "slug": item.get("slug"),
        "title": item.get("title"),
        "subtitle": item.get("subtitle"),
        "category": item.get("category"),
        "year": item.get("year"),
        "area": item.get("area"),
        "location": item.get("location"),
        "short_description": item.get("short_description"),
        "is_featured": item.get("is_featured"),
        "show_in_detail_section": item.get("show_in_detail_section"),
    }


@mcp.tool()
def site_status() -> str:
    """Перевірити, що API сайту відповідає, і коротко сказати, що на головній."""
    home = api_get("home/")
    settings = home.get("settings") or {}
    return dumps(
        {
            "ok": True,
            "api": api_base(),
            "brand": settings.get("brand_name"),
            "tagline": settings.get("tagline"),
            "counts": {
                "projects": len(home.get("projects") or []),
                "materials": len(home.get("materials") or []),
                "sections": len(home.get("sections") or []),
                "process_steps": len(home.get("process_steps") or []),
                "navigation": len(home.get("navigation") or []),
            },
            "featured_project_slug": home.get("featured_project_slug"),
        }
    )


@mcp.tool()
def get_site_settings() -> str:
    """Повернути публічні налаштування сайту: бренд, hero, контакти, SEO, футер."""
    return dumps(api_get("settings/"))


@mcp.tool()
def list_sections() -> str:
    """Список видимих секцій головної: ключ, заголовки, CTA."""
    home = api_get("home/")
    sections = []
    for item in home.get("sections") or []:
        sections.append(
            {
                "key": item.get("key"),
                "section_id": item.get("section_id"),
                "eyebrow": item.get("eyebrow"),
                "title": item.get("title"),
                "title_line2": item.get("title_line2"),
                "title_emphasis": item.get("title_emphasis"),
                "subtitle": item.get("subtitle"),
                "cta_text": item.get("cta_text"),
                "cta_href": item.get("cta_href"),
                "order": item.get("order"),
            }
        )
    return dumps(sections)


@mcp.tool()
def list_navigation() -> str:
    """Пункти меню шапки та футера."""
    home = api_get("home/")
    return dumps(home.get("navigation") or [])


@mcp.tool()
def list_projects() -> str:
    """Короткий список опублікованих проєктів (без галереї та етапів)."""
    projects = as_list(api_get("projects/"))
    return dumps([project_summary(item) for item in projects])


@mcp.tool()
def get_project(slug: str) -> str:
    """Повний опублікований проєкт за slug: тексти, SEO, етапи, галерея."""
    return dumps(api_get(f"projects/{slug}/"))


@mcp.tool()
def list_materials() -> str:
    """Матеріали, які показуються на сайті."""
    return dumps(as_list(api_get("materials/")))


@mcp.tool()
def list_process_steps() -> str:
    """Кроки процесу виробництва."""
    return dumps(as_list(api_get("process-steps/")))


@mcp.tool()
def list_workshop() -> str:
    """Статистика та зображення майстерні, плюс деталі ремесла."""
    return dumps(
        {
            "stats": as_list(api_get("workshop-stats/")),
            "images": as_list(api_get("workshop-images/")),
            "craft_details": as_list(api_get("craft-details/")),
        }
    )


@mcp.tool()
def get_hero_scene() -> str:
    """Активна сцена героя: тексти простою та зони креслення."""
    home = api_get("home/")
    settings = home.get("settings") or {}
    return dumps(
        {
            "hero": {
                "eyebrow": settings.get("hero_eyebrow"),
                "title_line1": settings.get("hero_title_line1"),
                "title_emphasis": settings.get("hero_title_emphasis"),
                "title_line2": settings.get("hero_title_line2"),
                "subline": settings.get("hero_subline"),
                "cta_primary_text": settings.get("hero_cta_primary_text"),
                "cta_primary_href": settings.get("hero_cta_primary_href"),
                "cta_secondary_text": settings.get("hero_cta_secondary_text"),
                "cta_secondary_href": settings.get("hero_cta_secondary_href"),
            },
            "hero_stats": home.get("hero_stats") or [],
            "hero_scene": home.get("hero_scene"),
            "room_types": home.get("room_types") or [],
        }
    )


@mcp.tool()
def get_homepage() -> str:
    """Повний JSON головної сторінки (GET /api/home/). Велика відповідь."""
    return dumps(api_get("home/"))


@mcp.resource("luxmeb://homepage")
def homepage_resource() -> str:
    """Повний публічний payload головної сторінки."""
    return dumps(api_get("home/"))


@mcp.resource("luxmeb://settings")
def settings_resource() -> str:
    """Публічні налаштування сайту."""
    return dumps(api_get("settings/"))


@mcp.resource("luxmeb://projects/{slug}")
def project_resource(slug: str) -> str:
    """Один опублікований проєкт за slug."""
    return dumps(api_get(f"projects/{slug}/"))


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

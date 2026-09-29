"""Send new lead notifications to a Telegram chat via Bot API."""

from __future__ import annotations

import logging
from urllib import error, parse, request

from catalog.models import SiteSettings

from .models import Lead

logger = logging.getLogger(__name__)


def format_lead_message(lead: Lead) -> str:
    lines = [
        "🆕 Нова заявка з сайту ProProstir",
        "",
        f"👤 Ім'я: {lead.name}",
        f"📞 Телефон: {lead.phone}",
    ]
    if lead.email:
        lines.append(f"✉️ Email: {lead.email}")
    if lead.telegram:
        lines.append(f"💬 Telegram: {lead.telegram}")
    if lead.room_type:
        lines.append(f"🏠 Тип: {lead.room_type_label()}")
    if lead.message:
        lines.extend(["", "📝 Повідомлення:", lead.message])
    if lead.attachment:
        lines.extend(["", "📎 До заявки додано фото або план"])
    return "\n".join(lines)


def notify_telegram(lead: Lead) -> bool:
    """
    Best-effort notify. Never raises — lead is already saved on the site.
    Returns True if Telegram accepted the message.
    """
    try:
        settings = SiteSettings.load()
    except Exception:
        logger.exception("Failed to load site settings for Telegram notify")
        return False

    if not settings.telegram_notify_enabled:
        return False

    token = (settings.telegram_bot_token or "").strip()
    chat_id = (settings.telegram_notify_chat_id or "").strip()
    if not token or not chat_id:
        logger.warning(
            "Telegram notify enabled but bot token or chat id is missing"
        )
        return False

    payload = parse.urlencode(
        {
            "chat_id": chat_id,
            "text": format_lead_message(lead),
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with request.urlopen(req, timeout=8) as resp:
            ok = 200 <= getattr(resp, "status", 200) < 300
            if not ok:
                logger.warning("Telegram API returned status %s", resp.status)
            return ok
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        logger.warning("Telegram API HTTP error %s: %s", exc.code, body)
        return False
    except Exception:
        logger.exception("Failed to send Telegram lead notification")
        return False

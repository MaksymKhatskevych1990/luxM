"""Turn an Instagram post or CDN link into image bytes for the gallery."""

import io
import re
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from PIL import Image

from catalog.models import normalize_image_reference

MAX_IMAGE_BYTES = 15 * 1024 * 1024
USER_AGENT = "Mozilla/5.0 (compatible; ProProstir/1.0; +https://proprostir.com.ua)"
INSTAGRAM_HOSTS = {"instagram.com", "www.instagram.com", "m.instagram.com"}
POST_RE = re.compile(
    r"https?://(?:www\.|m\.)?instagram\.com/(p|reel|tv)/([A-Za-z0-9_-]+)",
    re.IGNORECASE,
)


class RemoteImageError(Exception):
    pass


def instagram_media_url(value: str) -> str | None:
    match = POST_RE.search(normalize_image_reference(value))
    if not match:
        return None
    kind, code = match.group(1).lower(), match.group(2)
    return f"https://www.instagram.com/{kind}/{code}/media/?size=l"


def _host(url: str) -> str:
    return (urlparse(url).hostname or "").lower()


def is_instagram_cdn(url: str) -> bool:
    host = _host(url)
    return host.endswith(".cdninstagram.com") or host.endswith(".fbcdn.net")


def is_instagram_page(url: str) -> bool:
    return _host(normalize_image_reference(url)) in INSTAGRAM_HOSTS


def _allowed(url: str, *, allow_page: bool) -> bool:
    host = _host(url)
    if host.endswith(".cdninstagram.com") or host.endswith(".fbcdn.net"):
        return True
    return allow_page and host in INSTAGRAM_HOSTS


class _StayOnInstagram(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _allowed(newurl, allow_page=True):
            raise RemoteImageError("Посилання веде не на фото Instagram.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_remote_image(url: str, *, allow_page: bool, opener=None) -> tuple[str, bytes]:
    if not _allowed(url, allow_page=allow_page):
        raise RemoteImageError("Посилання веде не на фото Instagram.")
    opener = opener or build_opener(_StayOnInstagram)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(request, timeout=20) as response:
            final_url = response.geturl()
            if not _allowed(final_url, allow_page=True):
                raise RemoteImageError("Посилання веде не на фото Instagram.")
            content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            data = response.read(MAX_IMAGE_BYTES + 1)
    except RemoteImageError:
        raise
    except (URLError, TimeoutError, OSError) as exc:
        raise RemoteImageError("Не вдалося завантажити фото з Instagram.") from exc
    if len(data) > MAX_IMAGE_BYTES:
        raise RemoteImageError("Фото з Instagram більше ніж 15 МБ.")
    if not content_type.startswith("image/"):
        raise RemoteImageError("Instagram не віддав файл зображення. Завантажте його з комп'ютера.")
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
    except Exception as exc:
        raise RemoteImageError("Instagram не віддав файл зображення. Завантажте його з комп'ютера.") from exc
    extension = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
        "image/gif": "gif",
    }.get(content_type, "jpg")
    return extension, data


def import_instagram_image(url: str) -> tuple[str, bytes] | None:
    """Return a filename and bytes, or None when the URL is not Instagram.

    A profile or other Instagram page raises RemoteImageError so it is not
    stored as a picture address.
    """
    normalized = normalize_image_reference(url)
    media_url = instagram_media_url(normalized)
    if media_url:
        shortcode = POST_RE.search(normalized).group(2)
        extension, data = fetch_remote_image(media_url, allow_page=True)
        return f"instagram-{shortcode}.{extension}", data
    if is_instagram_cdn(normalized):
        extension, data = fetch_remote_image(normalized, allow_page=False)
        return f"instagram-photo.{extension}", data
    if is_instagram_page(normalized):
        raise RemoteImageError(
            "Вставте посилання на пост або ріл (/p/ або /reel/), пряму адресу картинки, або завантажте файл з комп'ютера."
        )
    return None

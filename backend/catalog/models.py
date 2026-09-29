from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

MAX_VIDEO_BYTES = 100 * 1024 * 1024  # 100 MB


def validate_video_size(file_obj):
    if file_obj and getattr(file_obj, "size", 0) > MAX_VIDEO_BYTES:
        raise ValidationError("Розмір відео не може перевищувати 100 МБ.")


def project_video_upload_to(instance, filename):
    return f"projects/{instance.slug or 'project'}/video/{filename}"


def project_gallery_upload_to(instance, filename):
    slug = instance.project.slug if instance.project_id else "project"
    return f"projects/{slug}/gallery/{filename}"


def brand_upload_to(instance, filename):
    return f"brand/{filename}"


def hero_upload_to(instance, filename):
    return f"hero/{filename}"


def seo_upload_to(instance, filename):
    return f"seo/{filename}"


def drawing_upload_to(instance, filename):
    return f"drawing/{filename}"


def before_after_upload_to(instance, filename):
    return f"before_after/{filename}"


def materials_upload_to(instance, filename):
    return f"materials/{filename}"


def process_upload_to(instance, filename):
    return f"process/{filename}"


def craft_upload_to(instance, filename):
    return f"craft/{filename}"


def workshop_upload_to(instance, filename):
    return f"workshop/{filename}"


def hero_scene_upload_to(instance, filename):
    return f"hero_scenes/{filename}"


def project_stage_upload_to(instance, filename):
    return f"project_stages/{filename}"


def media_or_url(file_field, url_value: str = "") -> str:
    if file_field:
        try:
            return file_field.url
        except ValueError:
            pass
    return url_value or ""


HERO_BACKGROUND_DEFAULT = (
    "https://images.unsplash.com/photo-1782392440011-b0bb69d31a26"
    "?w=1800&h=1100&fit=crop&auto=format"
)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):
    brand_name = models.CharField(
        max_length=120, default="ProProstir", verbose_name="Назва бренду"
    )
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default="Від ідеї до вашого простору",
        verbose_name="Слоган",
    )
    founded_year = models.PositiveIntegerField(
        default=2018, verbose_name="Рік заснування"
    )

    header_logo = models.ImageField(
        upload_to=brand_upload_to,
        blank=True,
        null=True,
        verbose_name="Логотип (файл)",
        help_text="PNG/SVG/WebP. Якщо порожньо — показується графічний знак.",
    )
    header_logo_primary = models.CharField(
        max_length=80, default="ProProstir", verbose_name="Логотип (основний текст)"
    )
    header_logo_secondary = models.CharField(
        max_length=80, default="Від ідеї до вашого простору", verbose_name="Логотип (другий рядок)"
    )
    header_cta_text = models.CharField(
        max_length=120, default="Обговорити проєкт", verbose_name="CTA шапки"
    )
    header_cta_href = models.CharField(
        max_length=200, default="#контакти", verbose_name="Посилання CTA шапки"
    )

    hero_eyebrow = models.CharField(
        max_length=200,
        default="ProProstir · Від ідеї до вашого простору",
        verbose_name="Надзаголовок героя",
    )
    hero_title_line1 = models.CharField(
        max_length=120, default="Меблі,", verbose_name="Заголовок героя (рядок 1)"
    )
    hero_title_emphasis = models.CharField(
        max_length=120, default="створені", verbose_name="Заголовок героя (акцент)"
    )
    hero_title_line2 = models.CharField(
        max_length=120,
        default="під ваш простір.",
        verbose_name="Заголовок героя (рядок 2)",
    )
    hero_subline = models.CharField(
        max_length=255,
        default="Проєктування · Виробництво · Монтаж",
        verbose_name="Підзаголовок героя",
    )
    hero_cta_primary_text = models.CharField(
        max_length=120,
        default="Дивитись проєкти",
        verbose_name="Основна кнопка героя",
    )
    hero_cta_primary_href = models.CharField(
        max_length=200,
        default="#проєкти",
        verbose_name="Посилання основної кнопки героя",
    )
    hero_cta_secondary_text = models.CharField(
        max_length=120, default="Про процес", verbose_name="Друга кнопка героя"
    )
    hero_cta_secondary_href = models.CharField(
        max_length=200,
        default="#процес",
        verbose_name="Посилання другої кнопки героя",
    )
    hero_floorplan_caption = models.CharField(
        max_length=200,
        default="Технічне креслення · Масштаб 1:25",
        verbose_name="Підпис креслення",
    )
    hero_scroll_hint = models.CharField(
        max_length=80, default="Гортати", verbose_name="Підказка прокрутки"
    )
    hero_founded_prefix = models.CharField(
        max_length=80, default="Заснована", verbose_name="Префікс року заснування"
    )
    hero_background = models.ImageField(
        upload_to=hero_upload_to,
        blank=True,
        null=True,
        verbose_name="Фон героя (файл)",
        help_text="Завантажте зображення фону. Має пріоритет над URL.",
    )
    hero_background_image_url = models.URLField(
        blank=True,
        default=HERO_BACKGROUND_DEFAULT,
        verbose_name="Фон героя (URL)",
        help_text="Якщо файл не завантажено.",
    )
    hero_floorplan_image = models.ImageField(
        upload_to=hero_upload_to,
        blank=True,
        null=True,
        verbose_name="Креслення героя (файл)",
        help_text="Замініть стандартне SVG-креслення власним зображенням.",
    )

    phone = models.CharField(
        max_length=64, default="+38 (044) 555 12 34", verbose_name="Телефон"
    )
    email = models.EmailField(default="studio@forma.ua", verbose_name="Email")
    telegram = models.CharField(
        max_length=120,
        blank=True,
        default="@forma_studio",
        verbose_name="Telegram (відображення)",
        help_text="Наприклад @forma_studio — показується в блоці контактів.",
    )
    whatsapp = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="WhatsApp (відображення)",
        help_text="Номер для показу на сайті, наприклад +38 (050) 123 45 67.",
    )
    address = models.CharField(
        max_length=255,
        default="Київ · Стара Дарниця, вул. Промислова 14",
        verbose_name="Адреса",
    )
    instagram_url = models.URLField(
        blank=True,
        default="https://instagram.com/",
        verbose_name="Instagram URL",
        help_text="Повне посилання, наприклад https://instagram.com/forma_studio",
    )
    telegram_url = models.URLField(
        blank=True,
        default="https://t.me/",
        verbose_name="Telegram URL",
        help_text="Повне посилання, наприклад https://t.me/forma_studio",
    )
    whatsapp_url = models.URLField(
        blank=True,
        default="",
        verbose_name="WhatsApp URL",
        help_text="Необов'язково. Якщо порожньо — збереться з номера (wa.me).",
    )

    # Bot credentials stay in admin only — never exposed via public API.
    telegram_notify_enabled = models.BooleanField(
        default=False,
        verbose_name="Надсилати заявки в Telegram",
        help_text=(
            "Увімкніть після заповнення токена і Chat ID. "
            "Заявки завжди зберігаються на сайті; при увімкненні — ще й у Telegram."
        ),
    )
    telegram_bot_token = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Telegram Bot Token",
        help_text=(
            "Отримайте в @BotFather командою /newbot. "
            "Формат: 123456789:AA.... Не публікується на сайті."
        ),
    )
    telegram_notify_chat_id = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Telegram Chat ID",
        help_text=(
            "ID особистого чату (число) або групи (часто з «-», наприклад -100…). "
            "Дізнатися можна через @userinfobot / @getidsbot або getUpdates."
        ),
    )

    seo_title = models.CharField(
        max_length=80,
        default="Меблі на замовлення в Києві | ProProstir",
        verbose_name="SEO заголовок (title)",
        help_text="До 60–70 символів. Можна змінювати під бренд і сезон.",
    )
    seo_description = models.TextField(
        default=(
            "ProProstir — від ідеї до вашого простору. Меблі на замовлення в Києві: "
            "кухні, гардеробні, вітальні та кабінети. Проєктування, виробництво "
            "та монтаж."
        ),
        verbose_name="SEO опис (meta description)",
        help_text="До 155–160 символів. Показується в Google.",
    )
    seo_keywords = models.TextField(
        default=(
            "меблі на замовлення Київ, кухні на замовлення, гардеробні Київ, "
            "вбудовані меблі, меблі з масиву, проєктування меблів, "
            "виробництво меблів Київ, монтаж меблів, ProProstir"
        ),
        verbose_name="Ключові слова",
        help_text="Через кому. Можна оновлювати, коли змінюються послуги чи назва.",
    )
    seo_author = models.CharField(
        max_length=120,
        blank=True,
        default="ProProstir",
        verbose_name="Автор / видавець",
        help_text="Якщо порожньо — береться назва бренду.",
    )
    seo_canonical_path = models.CharField(
        max_length=200,
        default="/",
        verbose_name="Canonical шлях",
        help_text="Зазвичай /. Повний URL збереться автоматично.",
    )
    seo_robots = models.CharField(
        max_length=80,
        default="index, follow",
        verbose_name="Robots",
        help_text="Наприклад: index, follow або noindex, nofollow.",
    )
    seo_html_lang = models.CharField(
        max_length=10,
        default="uk",
        verbose_name="Мова HTML (lang)",
    )
    seo_locale = models.CharField(
        max_length=16,
        default="uk_UA",
        verbose_name="Локаль Open Graph",
    )
    seo_geo_region = models.CharField(
        max_length=16,
        blank=True,
        default="UA-30",
        verbose_name="Geo region",
        help_text="Код регіону, наприклад UA-30 для Києва.",
    )
    seo_geo_placename = models.CharField(
        max_length=80,
        blank=True,
        default="Київ",
        verbose_name="Geo placename",
    )
    og_title = models.CharField(
        max_length=80,
        blank=True,
        default="ProProstir — Від ідеї до вашого простору",
        verbose_name="Open Graph заголовок",
        help_text="Якщо порожньо — використовується SEO заголовок.",
    )
    og_description = models.TextField(
        blank=True,
        default=(
            "Унікальні кухні, гардеробні та корпусні меблі ручної роботи. "
            "Від креслення до монтажу — одна майстерня в Києві."
        ),
        verbose_name="Open Graph опис",
        help_text="Якщо порожньо — використовується SEO опис.",
    )
    og_type = models.CharField(
        max_length=40,
        default="website",
        verbose_name="Open Graph тип",
    )
    og_image = models.ImageField(
        upload_to=seo_upload_to,
        blank=True,
        null=True,
        verbose_name="OG зображення (файл)",
    )
    og_image_url = models.URLField(
        blank=True,
        verbose_name="OG зображення (URL)",
        help_text="Якщо файл не завантажено. Інакше візьметься фон героя.",
    )
    og_image_alt = models.CharField(
        max_length=160,
        blank=True,
        default="Меблі на замовлення ProProstir: від ідеї до вашого простору",
        verbose_name="OG зображення alt",
    )
    twitter_card = models.CharField(
        max_length=40,
        default="summary_large_image",
        verbose_name="Twitter card",
    )
    twitter_title = models.CharField(
        max_length=80,
        blank=True,
        default="",
        verbose_name="Twitter заголовок",
        help_text="Якщо порожньо — Open Graph або SEO заголовок.",
    )
    twitter_description = models.TextField(
        blank=True,
        default="",
        verbose_name="Twitter опис",
        help_text="Якщо порожньо — Open Graph або SEO опис.",
    )
    twitter_site = models.CharField(
        max_length=80,
        blank=True,
        default="",
        verbose_name="Twitter / X @username",
    )
    jsonld_name = models.CharField(
        max_length=160,
        blank=True,
        default="ProProstir",
        verbose_name="JSON-LD назва бізнесу",
        help_text="Якщо порожньо — назва бренду.",
    )
    jsonld_type = models.CharField(
        max_length=80,
        default="FurnitureStore",
        verbose_name="JSON-LD тип schema.org",
        help_text="Наприклад FurnitureStore, LocalBusiness, HomeAndConstructionBusiness.",
    )
    jsonld_description = models.TextField(
        blank=True,
        default=(
            "ProProstir — від ідеї до вашого простору. Майстерня меблів "
            "на замовлення в Києві: проєктування, виробництво та монтаж."
        ),
        verbose_name="JSON-LD опис",
        help_text="Якщо порожньо — SEO опис.",
    )
    jsonld_city = models.CharField(
        max_length=80, default="Київ", verbose_name="Місто"
    )
    jsonld_country = models.CharField(
        max_length=8, default="UA", verbose_name="Країна (ISO)"
    )
    jsonld_postal_code = models.CharField(
        max_length=16,
        blank=True,
        default="",
        verbose_name="Поштовий індекс",
    )
    jsonld_street = models.CharField(
        max_length=255,
        blank=True,
        default="вул. Промислова 14, Стара Дарниця",
        verbose_name="Вулиця для schema",
        help_text="Якщо порожньо — поле адреси.",
    )
    jsonld_price_range = models.CharField(
        max_length=16, default="$$$", verbose_name="Ціновий діапазон"
    )
    jsonld_area_served = models.CharField(
        max_length=160,
        blank=True,
        default="Київ, Україна",
        verbose_name="Зона обслуговування",
    )
    jsonld_opening_hours = models.CharField(
        max_length=120,
        blank=True,
        default="Mo-Fr 10:00-18:00",
        verbose_name="Години роботи (schema)",
        help_text="Формат schema.org, наприклад Mo-Fr 10:00-18:00.",
    )
    jsonld_latitude = models.CharField(
        max_length=24, blank=True, default="", verbose_name="Широта"
    )
    jsonld_longitude = models.CharField(
        max_length=24, blank=True, default="", verbose_name="Довгота"
    )
    jsonld_services = models.TextField(
        blank=True,
        default=(
            "Кухні на замовлення\n"
            "Гардеробні\n"
            "Вітальні\n"
            "Кабінети\n"
            "Проєктування меблів\n"
            "Виробництво\n"
            "Монтаж"
        ),
        verbose_name="Послуги (по одному в рядку)",
        help_text="Назви можна змінювати — вони потрапляють у schema.org OfferCatalog.",
    )

    stats_projects = models.CharField(
        max_length=16,
        default="147",
        verbose_name="Проєктів (застаріле)",
        help_text="Залишене для сумісності. Основні значення — у «Статистика героя».",
    )
    stats_years = models.CharField(
        max_length=16, default="08", verbose_name="Років (застаріле)"
    )
    stats_masters = models.CharField(
        max_length=16, default="24", verbose_name="Майстрів (застаріле)"
    )
    stats_production = models.CharField(
        max_length=16, default="100%", verbose_name="Виробництво (застаріле)"
    )

    workshop_quote = models.TextField(
        default=(
            "Ми не просто виготовляємо меблі. Ми створюємо предмети, "
            "які мають існувати саме у вашому просторі."
        ),
        verbose_name="Цитата майстерні",
    )
    workshop_author = models.CharField(
        max_length=120,
        default="Команда ProProstir",
        verbose_name="Автор цитати",
    )
    workshop_text = models.TextField(
        default=(
            "Наша майстерня площею 800 м² в Старій Дарниці обладнана точними "
            "верстатами ЧПУ та ручним інструментом. Кожен виріб — від першого "
            "ескізу до встановлення — проходить через руки одного майстра."
        ),
        verbose_name="Текст майстерні",
    )

    detail_eyebrow_prefix = models.CharField(
        max_length=120,
        default="Проєкт у деталях",
        verbose_name="Надзаголовок блоку деталей",
    )
    detail_section_title = models.CharField(
        max_length=200,
        default="Від ескізу до встановлення",
        verbose_name="Заголовок блоку деталей",
    )
    detail_number_prefix = models.CharField(
        max_length=80, default="Проєкт №", verbose_name="Префікс номера проєкту"
    )
    detail_cta_text = models.CharField(
        max_length=120, default="Схожий проєкт →", verbose_name="CTA блоку деталей"
    )
    detail_cta_href = models.CharField(
        max_length=200,
        default="#контакти",
        verbose_name="Посилання CTA блоку деталей",
    )
    meta_label_area = models.CharField(
        max_length=80, default="Площа", verbose_name="Мітка: площа"
    )
    meta_label_materials = models.CharField(
        max_length=80, default="Матеріали", verbose_name="Мітка: матеріали"
    )
    meta_label_duration = models.CharField(
        max_length=80, default="Тривалість", verbose_name="Мітка: тривалість"
    )
    meta_label_year = models.CharField(
        max_length=80, default="Рік", verbose_name="Мітка: рік"
    )
    meta_label_location = models.CharField(
        max_length=80, default="Локація", verbose_name="Мітка: локація"
    )
    featured_project = models.ForeignKey(
        "Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Проєкт у блоці деталей",
    )

    drawing_eyebrow = models.CharField(
        max_length=200,
        default="Від ескізу до реальності",
        verbose_name="Надзаголовок креслення",
    )
    drawing_title = models.CharField(
        max_length=200,
        default="Ідея, що стає простором",
        verbose_name="Заголовок креслення",
    )
    drawing_body = models.TextField(
        default=(
            "Прокрутіть — побачите трансформацію з технічного креслення "
            "в готовий інтер'єр"
        ),
        verbose_name="Текст креслення",
    )
    drawing_phase_1_label = models.CharField(
        max_length=80, default="Креслення", verbose_name="Фаза 1"
    )
    drawing_phase_2_label = models.CharField(
        max_length=80, default="Ескіз", verbose_name="Фаза 2"
    )
    drawing_phase_3_label = models.CharField(
        max_length=80, default="Результат", verbose_name="Фаза 3"
    )
    drawing_result_alt = models.CharField(
        max_length=120,
        default="Готова кухня",
        verbose_name="Alt зображення результату",
    )
    drawing_sketch = models.ImageField(
        upload_to=drawing_upload_to,
        blank=True,
        null=True,
        verbose_name="Ескіз (файл)",
    )
    drawing_sketch_image_url = models.URLField(
        blank=True,
        verbose_name="Ескіз (URL)",
        help_text="Якщо файл не завантажено.",
    )

    ba_eyebrow = models.CharField(
        max_length=200,
        default="Трансформація простору",
        verbose_name="Надзаголовок «До / Після»",
    )
    ba_title = models.CharField(
        max_length=200, default="До і після", verbose_name="Заголовок «До / Після»"
    )
    ba_hint = models.CharField(
        max_length=200,
        default="Перетягніть повзунок",
        verbose_name="Підказка повзунка",
    )
    ba_label_before = models.CharField(
        max_length=40, default="ДО", verbose_name="Мітка «До»"
    )
    ba_label_after = models.CharField(
        max_length=40, default="ПІСЛЯ", verbose_name="Мітка «Після»"
    )
    before_image = models.ImageField(
        upload_to=before_after_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення «До» (файл)",
    )
    before_image_url = models.URLField(
        blank=True,
        verbose_name="Зображення «До» (URL)",
        help_text="Якщо файл не завантажено.",
    )
    after_image = models.ImageField(
        upload_to=before_after_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення «Після» (файл)",
    )
    after_image_url = models.URLField(
        blank=True,
        verbose_name="Зображення «Після» (URL)",
        help_text="Якщо файл не завантажено.",
    )

    contact_eyebrow = models.CharField(
        max_length=120, default="Зв'язатися", verbose_name="Надзаголовок контактів"
    )
    contact_title_line1 = models.CharField(
        max_length=120, default="Розкажіть", verbose_name="Заголовок контактів (рядок 1)"
    )
    contact_title_line2 = models.CharField(
        max_length=120, default="про свій", verbose_name="Заголовок контактів (рядок 2)"
    )
    contact_title_emphasis = models.CharField(
        max_length=120, default="простір.", verbose_name="Заголовок контактів (акцент)"
    )
    contact_intro = models.TextField(
        default=(
            "Надішліть план приміщення, фотографію або просто ідею — "
            "ми зв'яжемося протягом одного робочого дня."
        ),
        verbose_name="Вступ контактів",
    )
    contact_room_heading = models.CharField(
        max_length=120, default="Що плануєте", verbose_name="Заголовок типів кімнат"
    )
    contact_message_placeholder = models.CharField(
        max_length=200,
        default="Розкажіть про ваш проєкт…",
        verbose_name="Плейсхолдер повідомлення",
    )
    contact_name_placeholder = models.CharField(
        max_length=80, default="Ім'я", verbose_name="Плейсхолдер імені"
    )
    contact_phone_placeholder = models.CharField(
        max_length=80, default="Телефон", verbose_name="Плейсхолдер телефону"
    )
    contact_email_placeholder = models.CharField(
        max_length=80, default="Email", verbose_name="Плейсхолдер email"
    )
    contact_telegram_placeholder = models.CharField(
        max_length=80, default="Telegram", verbose_name="Плейсхолдер Telegram"
    )
    contact_submit_text = models.CharField(
        max_length=120,
        default="Надіслати запит →",
        verbose_name="Текст кнопки надсилання",
    )
    contact_submit_loading = models.CharField(
        max_length=120,
        default="Надсилаємо…",
        verbose_name="Текст кнопки під час надсилання",
    )
    contact_success_eyebrow = models.CharField(
        max_length=80, default="Надіслано", verbose_name="Надзаголовок успіху"
    )
    contact_success_title = models.CharField(
        max_length=200,
        default="Дякуємо, ми отримали ваш запит.",
        verbose_name="Заголовок успіху",
    )
    contact_success_body = models.TextField(
        default=(
            "Зв'яжемося протягом одного робочого дня, щоб обговорити ваш простір."
        ),
        verbose_name="Текст успіху",
    )
    contact_validation_message = models.CharField(
        max_length=255,
        default="Будь ласка, вкажіть ім'я та телефон.",
        verbose_name="Повідомлення валідації",
    )
    contact_label_address = models.CharField(
        max_length=80, default="Адреса", verbose_name="Мітка адреси"
    )
    contact_label_phone = models.CharField(
        max_length=80, default="Телефон", verbose_name="Мітка телефону"
    )
    contact_label_email = models.CharField(
        max_length=80, default="Email", verbose_name="Мітка email"
    )
    contact_label_telegram = models.CharField(
        max_length=80, default="Telegram", verbose_name="Мітка Telegram"
    )
    contact_label_whatsapp = models.CharField(
        max_length=80, default="WhatsApp", verbose_name="Мітка WhatsApp"
    )
    contact_label_instagram = models.CharField(
        max_length=80, default="Instagram", verbose_name="Мітка Instagram"
    )

    footer_services_heading = models.CharField(
        max_length=80, default="Послуги", verbose_name="Заголовок послуг у футері"
    )
    footer_studio_heading = models.CharField(
        max_length=80, default="Студія", verbose_name="Заголовок студії у футері"
    )
    footer_contacts_heading = models.CharField(
        max_length=80, default="Контакти", verbose_name="Заголовок контактів у футері"
    )
    footer_copyright_suffix = models.CharField(
        max_length=120,
        default="Всі права захищено",
        verbose_name="Суфікс копірайту",
    )
    footer_location_tagline = models.CharField(
        max_length=200,
        default="Київ, Україна · Виготовлено з гордістю",
        verbose_name="Теглайн локації у футері",
    )

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return self.brand_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @staticmethod
    def digits_only(value: str) -> str:
        return "".join(ch for ch in (value or "") if ch.isdigit())

    @property
    def resolved_whatsapp_url(self) -> str:
        if self.whatsapp_url:
            return self.whatsapp_url
        digits = self.digits_only(self.whatsapp or self.phone)
        if digits:
            return f"https://wa.me/{digits}"
        return ""

    @property
    def resolved_telegram_url(self) -> str:
        if self.telegram_url:
            return self.telegram_url
        handle = (self.telegram or "").strip().lstrip("@")
        if handle:
            return f"https://t.me/{handle}"
        return ""

    @property
    def resolved_logo_url(self) -> str:
        return media_or_url(self.header_logo)

    @property
    def resolved_hero_background_url(self) -> str:
        return media_or_url(self.hero_background, self.hero_background_image_url)

    @property
    def resolved_hero_floorplan_url(self) -> str:
        return media_or_url(self.hero_floorplan_image)

    @property
    def resolved_og_image_url(self) -> str:
        return media_or_url(self.og_image, self.og_image_url) or self.resolved_hero_background_url

    @property
    def resolved_drawing_sketch_url(self) -> str:
        return media_or_url(self.drawing_sketch, self.drawing_sketch_image_url)

    @property
    def resolved_before_image_url(self) -> str:
        return media_or_url(self.before_image, self.before_image_url)

    @property
    def resolved_after_image_url(self) -> str:
        return media_or_url(self.after_image, self.after_image_url)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.select_related("featured_project").get_or_create(pk=1)
        return obj


class HeroStat(TimeStampedModel):
    value = models.CharField(max_length=16, verbose_name="Значення")
    label = models.CharField(max_length=120, verbose_name="Підпис")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Статистика героя"
        verbose_name_plural = "Статистика героя"

    def __str__(self):
        return f"{self.value} — {self.label}"


class PageSection(TimeStampedModel):
    KEY_CHOICES = [
        ("projects", "Проєкти"),
        ("photography", "Фотографія"),
        ("materials", "Матеріали"),
        ("process", "Процес"),
        ("workshop", "Майстерня"),
        ("drawing", "Креслення"),
        ("before_after", "До / Після"),
        ("contact", "Контакти"),
    ]

    key = models.CharField(
        max_length=40, unique=True, choices=KEY_CHOICES, verbose_name="Ключ"
    )
    section_id = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Якір секції",
        help_text="Без #, напр. проєкти",
    )
    eyebrow = models.CharField(max_length=200, blank=True, verbose_name="Надзаголовок")
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок")
    title_line2 = models.CharField(
        max_length=255, blank=True, verbose_name="Заголовок (рядок 2)"
    )
    title_emphasis = models.CharField(
        max_length=255, blank=True, verbose_name="Заголовок (акцент)"
    )
    subtitle = models.TextField(blank=True, verbose_name="Підзаголовок")
    cta_text = models.CharField(
        max_length=120, blank=True, verbose_name="Текст кнопки / посилання"
    )
    cta_href = models.CharField(
        max_length=200, blank=True, verbose_name="Посилання кнопки"
    )
    is_visible = models.BooleanField(default=True, verbose_name="Видима")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Секція сторінки"
        verbose_name_plural = "Секції сторінки"

    def __str__(self):
        return self.get_key_display()


class NavItem(TimeStampedModel):
    LOCATION_HEADER = "header"
    LOCATION_FOOTER_SERVICES = "footer_services"
    LOCATION_FOOTER_STUDIO = "footer_studio"
    LOCATION_CHOICES = [
        (LOCATION_HEADER, "Шапка"),
        (LOCATION_FOOTER_SERVICES, "Футер · Послуги"),
        (LOCATION_FOOTER_STUDIO, "Футер · Студія"),
    ]

    label = models.CharField(max_length=120, verbose_name="Назва")
    href = models.CharField(max_length=200, verbose_name="Посилання")
    location = models.CharField(
        max_length=32,
        choices=LOCATION_CHOICES,
        default=LOCATION_HEADER,
        verbose_name="Розміщення",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_visible = models.BooleanField(default=True, verbose_name="Видимий")

    class Meta:
        ordering = ["location", "order", "id"]
        verbose_name = "Пункт навігації"
        verbose_name_plural = "Навігація"

    def __str__(self):
        return f"{self.get_location_display()}: {self.label}"


class RoomType(TimeStampedModel):
    value = models.SlugField(unique=True, verbose_name="Значення")
    label = models.CharField(max_length=80, verbose_name="Назва")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активний")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Тип кімнати"
        verbose_name_plural = "Типи кімнат"

    def __str__(self):
        return self.label


class Project(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name="Назва")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слаг")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="Підзаголовок")
    description = models.TextField(
        blank=True,
        verbose_name="Повний опис",
        help_text="Повний текст у модальному вікні проєкту",
    )
    short_description = models.TextField(
        blank=True, verbose_name="Короткий опис (картка)"
    )
    materials_label = models.CharField(
        max_length=200,
        blank=True,
        help_text="Напр.: ДУБ · КАМІНЬ · 2026",
        verbose_name="Матеріали (мітка)",
    )
    category = models.CharField(max_length=80, blank=True, verbose_name="Категорія")
    year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Рік")
    area = models.CharField(max_length=64, blank=True, verbose_name="Площа")
    duration = models.CharField(max_length=64, blank=True, verbose_name="Тривалість")
    location = models.CharField(max_length=120, blank=True, verbose_name="Локація")
    image_url = models.URLField(
        blank=True,
        verbose_name="Обкладинка (URL)",
        help_text="Зовнішній URL обкладинки, якщо немає завантаженого файлу",
    )
    cover_image = models.ImageField(
        upload_to="projects/covers/",
        blank=True,
        null=True,
        verbose_name="Обкладинка (файл)",
    )
    detail_image_url = models.URLField(blank=True, verbose_name="Зображення деталей (URL)")
    video = models.FileField(
        upload_to=project_video_upload_to,
        blank=True,
        null=True,
        validators=[validate_video_size],
        verbose_name="Відео (файл ≤ 100 МБ)",
        help_text="Відео від креслення до готового рішення. Максимум 100 МБ.",
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="Відео (зовнішній URL)",
        help_text="Альтернатива файлу: пряме посилання на mp4/webm",
    )
    video_poster_url = models.URLField(
        blank=True, verbose_name="Постер відео (URL)"
    )
    is_featured = models.BooleanField(default=True, verbose_name="Вибраний")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")
    show_in_detail_section = models.BooleanField(
        default=False, verbose_name="Показувати в блоці деталей"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    seo_title = models.CharField(max_length=70, blank=True, verbose_name="SEO заголовок")
    seo_description = models.TextField(blank=True, verbose_name="SEO опис")
    seo_keywords = models.CharField(
        max_length=255, blank=True, verbose_name="SEO ключові слова"
    )

    class Meta:
        ordering = ["order", "-year", "id"]
        verbose_name = "Проєкт"
        verbose_name_plural = "Проєкти"

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.video:
            validate_video_size(self.video)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "project"
            slug = base
            i = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def cover_url(self) -> str:
        if self.cover_image:
            return self.cover_image.url
        return self.image_url or ""

    @property
    def resolved_video_url(self) -> str:
        if self.video:
            return self.video.url
        return self.video_url or ""


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        related_name="gallery",
        on_delete=models.CASCADE,
        verbose_name="Проєкт",
    )
    image = models.ImageField(
        upload_to=project_gallery_upload_to,
        blank=True,
        null=True,
        verbose_name="Фото (файл)",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Фото (URL)",
        help_text="Якщо файл не завантажено",
    )
    caption = models.CharField(max_length=200, blank=True, verbose_name="Підпис")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковане")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото проєкту"
        verbose_name_plural = "Галерея проєкту"

    def __str__(self):
        return self.caption or f"{self.project.title} · фото {self.order}"

    @property
    def resolved_url(self) -> str:
        if self.image:
            return self.image.url
        return self.image_url or ""


class ProjectStage(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        related_name="stages",
        on_delete=models.CASCADE,
        verbose_name="Проєкт",
    )
    title = models.CharField(max_length=80, verbose_name="Назва")
    image = models.ImageField(
        upload_to=project_stage_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення (файл)",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Зображення (URL)",
        help_text="Якщо файл не завантажено.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Етап проєкту"
        verbose_name_plural = "Етапи проєкту"

    def __str__(self):
        return f"{self.project.title} — {self.title}"

    @property
    def resolved_image_url(self) -> str:
        return media_or_url(self.image, self.image_url)


class Material(TimeStampedModel):
    name_uk = models.CharField(max_length=80, verbose_name="Назва (укр.)")
    name_en = models.CharField(max_length=80, verbose_name="Назва (англ.)")
    description = models.TextField(verbose_name="Опис")
    image = models.ImageField(
        upload_to=materials_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення (файл)",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Зображення (URL)",
        help_text="Якщо файл не завантажено.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    def __str__(self):
        return self.name_uk

    @property
    def resolved_image_url(self) -> str:
        return media_or_url(self.image, self.image_url)


class ProcessStep(TimeStampedModel):
    title = models.CharField(max_length=120, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    duration = models.CharField(max_length=64, verbose_name="Тривалість")
    image = models.ImageField(
        upload_to=process_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення (файл)",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Зображення (URL)",
        help_text="Якщо файл не завантажено.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Крок процесу"
        verbose_name_plural = "Процес"

    def __str__(self):
        return self.title

    @property
    def resolved_image_url(self) -> str:
        return media_or_url(self.image, self.image_url)


class CraftDetail(TimeStampedModel):
    title = models.CharField(max_length=120, verbose_name="Назва")
    image = models.ImageField(
        upload_to=craft_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення (файл)",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Зображення (URL)",
        help_text="Якщо файл не завантажено.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Деталь майстерності"
        verbose_name_plural = "Деталі майстерності"

    def __str__(self):
        return self.title

    @property
    def resolved_image_url(self) -> str:
        return media_or_url(self.image, self.image_url)


class WorkshopStat(TimeStampedModel):
    value = models.CharField(max_length=64, verbose_name="Значення")
    label = models.CharField(max_length=120, verbose_name="Підпис")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Статистика майстерні"
        verbose_name_plural = "Статистика майстерні"

    def __str__(self):
        return f"{self.value} — {self.label}"


class WorkshopImage(TimeStampedModel):
    title = models.CharField(max_length=120, verbose_name="Назва")
    image = models.ImageField(
        upload_to=workshop_upload_to,
        blank=True,
        null=True,
        verbose_name="Зображення (файл)",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Зображення (URL)",
        help_text="Якщо файл не завантажено.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото майстерні"
        verbose_name_plural = "Фото майстерні"

    def __str__(self):
        return self.title

    @property
    def resolved_image_url(self) -> str:
        return media_or_url(self.image, self.image_url)


class HeroScene(TimeStampedModel):
    title = models.CharField(max_length=160, verbose_name="Назва сцени")
    image = models.ImageField(
        upload_to=hero_scene_upload_to,
        blank=True,
        null=True,
        verbose_name="Фото інтер'єру",
        help_text="Завантажте фото кімнати. Далі на ньому можна намалювати зони.",
    )
    image_url = models.URLField(
        blank=True,
        verbose_name="Фото (URL)",
        help_text="Якщо файл ще не завантажено.",
    )
    hint = models.CharField(
        max_length=255,
        blank=True,
        default="Наведіть курсор — дізнайтеся, які роботи ми пропонуємо для кожної зони простору.",
        verbose_name="Підказка під заголовком",
    )
    idle_eyebrow = models.CharField(
        max_length=80,
        blank=True,
        default="Зона простору",
        verbose_name="Картка: надзаголовок (без зони)",
    )
    idle_title = models.CharField(
        max_length=160,
        blank=True,
        default="Оберіть деталь інтер'єру",
        verbose_name="Картка: заголовок (без зони)",
    )
    idle_body = models.TextField(
        blank=True,
        default=(
            "Стеля, стіни, камін, меблі, підлога чи декор — підсвітіть зону "
            "і побачите, що саме ми реалізуємо."
        ),
        verbose_name="Картка: текст (без зони)",
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Показувати на головній",
        help_text="Активною може бути лише одна сцена.",
    )
    is_published = models.BooleanField(default=True, verbose_name="Опублікована")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Сцена героя"
        verbose_name_plural = "Сцени героя (фото + зони)"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            type(self).objects.exclude(pk=self.pk).filter(is_active=True).update(
                is_active=False
            )

    @property
    def resolved_image_url(self) -> str:
        return media_or_url(self.image, self.image_url)


class HeroZone(TimeStampedModel):
    scene = models.ForeignKey(
        HeroScene,
        on_delete=models.CASCADE,
        related_name="zones",
        verbose_name="Сцена",
    )
    name = models.CharField(max_length=120, verbose_name="Назва зони")
    service = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Послуга",
        help_text="Що саме робимо в цій зоні.",
    )
    materials = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Матеріали",
    )
    tag = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Тег",
        help_text="Наприклад Стелі, Стіни, Меблі. Однакові теги групуються.",
    )
    x = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
        verbose_name="X %",
        help_text="Лівий край зони, відсоток ширини фото.",
    )
    y = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
        verbose_name="Y %",
        help_text="Верхній край зони, відсоток висоти фото.",
    )
    width = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20,
        verbose_name="Ширина %",
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=15,
        verbose_name="Висота %",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Показувати")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Зона героя"
        verbose_name_plural = "Зони героя"

    def __str__(self):
        return self.name

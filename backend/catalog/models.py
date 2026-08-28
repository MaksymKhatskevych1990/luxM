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
        max_length=120, default="Форма Studio", verbose_name="Назва бренду"
    )
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default="Унікальні меблі на замовлення. Київ, Україна.",
        verbose_name="Слоган",
    )
    founded_year = models.PositiveIntegerField(
        default=2018, verbose_name="Рік заснування"
    )

    header_logo_primary = models.CharField(
        max_length=80, default="Форма", verbose_name="Логотип (основний)"
    )
    header_logo_secondary = models.CharField(
        max_length=80, default="STUDIO", verbose_name="Логотип (другий рядок)"
    )
    header_cta_text = models.CharField(
        max_length=120, default="Обговорити проєкт", verbose_name="CTA шапки"
    )
    header_cta_href = models.CharField(
        max_length=200, default="#контакти", verbose_name="Посилання CTA шапки"
    )

    hero_eyebrow = models.CharField(
        max_length=200,
        default="Форма Studio · Київ, Україна",
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
    hero_background_image_url = models.URLField(
        blank=True,
        default=HERO_BACKGROUND_DEFAULT,
        verbose_name="Фон героя (URL)",
    )

    phone = models.CharField(
        max_length=64, default="+38 (044) 555 12 34", verbose_name="Телефон"
    )
    email = models.EmailField(default="studio@forma.ua", verbose_name="Email")
    telegram = models.CharField(
        max_length=120, default="@forma_studio", verbose_name="Telegram"
    )
    address = models.CharField(
        max_length=255,
        default="Київ · Стара Дарниця, вул. Промислова 14",
        verbose_name="Адреса",
    )
    instagram_url = models.URLField(
        blank=True, default="https://instagram.com/", verbose_name="Instagram"
    )
    telegram_url = models.URLField(
        blank=True, default="https://t.me/", verbose_name="Посилання Telegram"
    )

    seo_title = models.CharField(
        max_length=70,
        default="Форма Studio — меблі на замовлення в Києві",
        verbose_name="SEO заголовок",
    )
    seo_description = models.TextField(
        default=(
            "Преміальні меблі на замовлення: проєктування, виробництво та монтаж. "
            "Кухні, гардеробні, вітальні та кабінети."
        ),
        verbose_name="SEO опис",
    )
    seo_keywords = models.CharField(
        max_length=255,
        default="меблі на замовлення, кухні Київ, гардеробні, Forma Studio",
        verbose_name="SEO ключові слова",
    )
    og_image_url = models.URLField(blank=True, verbose_name="OG зображення (URL)")
    jsonld_city = models.CharField(
        max_length=80, default="Київ", verbose_name="JSON-LD місто"
    )
    jsonld_country = models.CharField(
        max_length=8, default="UA", verbose_name="JSON-LD країна"
    )
    jsonld_price_range = models.CharField(
        max_length=16, default="$$$", verbose_name="JSON-LD ціновий діапазон"
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
        default="Андрій Коваль, засновник",
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
    drawing_sketch_image_url = models.URLField(
        blank=True, verbose_name="Ескіз (URL)"
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
    before_image_url = models.URLField(blank=True, verbose_name="Зображення «До»")
    after_image_url = models.URLField(blank=True, verbose_name="Зображення «Після»")

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
    image_url = models.URLField(verbose_name="Зображення")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Етап проєкту"
        verbose_name_plural = "Етапи проєкту"

    def __str__(self):
        return f"{self.project.title} — {self.title}"

class Material(TimeStampedModel):
    name_uk = models.CharField(max_length=80, verbose_name="Назва (укр.)")
    name_en = models.CharField(max_length=80, verbose_name="Назва (англ.)")
    description = models.TextField(verbose_name="Опис")
    image_url = models.URLField(verbose_name="Зображення")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    def __str__(self):
        return self.name_uk


class ProcessStep(TimeStampedModel):
    title = models.CharField(max_length=120, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    duration = models.CharField(max_length=64, verbose_name="Тривалість")
    image_url = models.URLField(verbose_name="Зображення")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Крок процесу"
        verbose_name_plural = "Процес"

    def __str__(self):
        return self.title


class CraftDetail(TimeStampedModel):
    title = models.CharField(max_length=120, verbose_name="Назва")
    image_url = models.URLField(verbose_name="Зображення")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_published = models.BooleanField(default=True, verbose_name="Опублікований")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Деталь майстерності"
        verbose_name_plural = "Деталі майстерності"

    def __str__(self):
        return self.title


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
    image_url = models.URLField(verbose_name="Зображення")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото майстерні"
        verbose_name_plural = "Фото майстерні"

    def __str__(self):
        return self.title

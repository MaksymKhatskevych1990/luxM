from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):
    brand_name = models.CharField(max_length=120, default="Форма Studio")
    tagline = models.CharField(
        max_length=255,
        blank=True,
        default="Унікальні меблі на замовлення. Київ, Україна.",
    )
    founded_year = models.PositiveIntegerField(default=2018)
    phone = models.CharField(max_length=64, default="+38 (044) 555 12 34")
    email = models.EmailField(default="studio@forma.ua")
    telegram = models.CharField(max_length=120, default="@forma_studio")
    address = models.CharField(
        max_length=255, default="Київ · Стара Дарниця, вул. Промислова 14"
    )
    instagram_url = models.URLField(blank=True, default="https://instagram.com/")
    telegram_url = models.URLField(blank=True, default="https://t.me/")
    seo_title = models.CharField(
        max_length=70, default="Форма Studio — меблі на замовлення в Києві"
    )
    seo_description = models.TextField(
        default=(
            "Преміальні меблі на замовлення: проєктування, виробництво та монтаж. "
            "Кухні, гардеробні, вітальні та кабінети."
        )
    )
    seo_keywords = models.CharField(
        max_length=255,
        default="меблі на замовлення, кухні Київ, гардеробні, Forma Studio",
    )
    stats_projects = models.CharField(max_length=16, default="147")
    stats_years = models.CharField(max_length=16, default="08")
    stats_masters = models.CharField(max_length=16, default="24")
    stats_production = models.CharField(max_length=16, default="100%")
    workshop_quote = models.TextField(
        default=(
            "Ми не просто виготовляємо меблі. Ми створюємо предмети, "
            "які мають існувати саме у вашому просторі."
        )
    )
    workshop_author = models.CharField(max_length=120, default="Андрій Коваль, засновник")
    workshop_text = models.TextField(
        default=(
            "Наша майстерня площею 800 м² в Старій Дарниці обладнана точними "
            "верстатами ЧПУ та ручним інструментом. Кожен виріб — від першого "
            "ескізу до встановлення — проходить через руки одного майстра."
        )
    )
    before_image_url = models.URLField(blank=True)
    after_image_url = models.URLField(blank=True)

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
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    materials_label = models.CharField(
        max_length=200, blank=True, help_text="Напр.: ДУБ · КАМІНЬ · 2026"
    )
    category = models.CharField(max_length=80, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    area = models.CharField(max_length=64, blank=True)
    duration = models.CharField(max_length=64, blank=True)
    location = models.CharField(max_length=120, blank=True)
    image_url = models.URLField()
    detail_image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "-year", "id"]
        verbose_name = "Проєкт"
        verbose_name_plural = "Проєкти"

    def __str__(self):
        return self.title

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


class ProjectStage(TimeStampedModel):
    project = models.ForeignKey(Project, related_name="stages", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    image_url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Етап проєкту"
        verbose_name_plural = "Етапи проєкту"

    def __str__(self):
        return f"{self.project.title} — {self.title}"


class Material(TimeStampedModel):
    name_uk = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80)
    description = models.TextField()
    image_url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Матеріал"
        verbose_name_plural = "Матеріали"

    def __str__(self):
        return self.name_uk


class ProcessStep(TimeStampedModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    duration = models.CharField(max_length=64)
    image_url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Крок процесу"
        verbose_name_plural = "Процес"

    def __str__(self):
        return self.title


class CraftDetail(TimeStampedModel):
    title = models.CharField(max_length=120)
    image_url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Деталь майстерності"
        verbose_name_plural = "Деталі майстерності"

    def __str__(self):
        return self.title


class WorkshopStat(TimeStampedModel):
    value = models.CharField(max_length=64)
    label = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Статистика майстерні"
        verbose_name_plural = "Статистика майстерні"

    def __str__(self):
        return f"{self.value} — {self.label}"


class WorkshopImage(TimeStampedModel):
    title = models.CharField(max_length=120)
    image_url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото майстерні"
        verbose_name_plural = "Фото майстерні"

    def __str__(self):
        return self.title

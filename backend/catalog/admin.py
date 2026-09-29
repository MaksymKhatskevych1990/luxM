from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    CraftDetail,
    HeroScene,
    HeroStat,
    HeroZone,
    Material,
    NavItem,
    PageSection,
    ProcessStep,
    Project,
    ProjectImage,
    ProjectStage,
    RoomType,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)


class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 0
    fields = ("title", "image", "image_url", "order")
    ordering = ("order", "id")
    verbose_name_plural = "Етапи (fallback, якщо немає відео)"


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2
    fields = ("image", "image_url", "caption", "order", "is_published")
    ordering = ("order", "id")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Бренд",
            {"fields": ("brand_name", "tagline", "founded_year")},
        ),
        (
            "Header",
            {
                "fields": (
                    "header_logo",
                    "header_logo_primary",
                    "header_logo_secondary",
                    "header_cta_text",
                    "header_cta_href",
                )
            },
        ),
        (
            "Hero",
            {
                "fields": (
                    "hero_background",
                    "hero_background_image_url",
                    "hero_floorplan_image",
                    "hero_eyebrow",
                    "hero_title_line1",
                    "hero_title_emphasis",
                    "hero_title_line2",
                    "hero_subline",
                    "hero_cta_primary_text",
                    "hero_cta_primary_href",
                    "hero_cta_secondary_text",
                    "hero_cta_secondary_href",
                    "hero_floorplan_caption",
                    "hero_scroll_hint",
                    "hero_founded_prefix",
                )
            },
        ),
        (
            "Контакти",
            {
                "fields": (
                    "phone",
                    "email",
                    "address",
                    "telegram",
                    "whatsapp",
                )
            },
        ),
        (
            "Соцмережі",
            {
                "description": (
                    "Посилання для футера та блоку контактів. "
                    "Якщо WhatsApp URL порожній — збереться з номера (wa.me)."
                ),
                "fields": (
                    "instagram_url",
                    "telegram_url",
                    "whatsapp_url",
                ),
            },
        ),
        (
            "Telegram-сповіщення заявок",
            {
                "description": mark_safe(
                    """
                    <div style="line-height:1.55;max-width:820px">
                      <p style="margin:0 0 10px">
                        <strong>Заявки з форми завжди зберігаються</strong> у розділі
                        «Заявки». Нижче — як дублювати їх у Telegram.
                      </p>
                      <ol style="margin:0 0 10px;padding-left:1.3em">
                        <li>
                          Відкрийте Telegram і знайдіть бота
                          <strong>@BotFather</strong>.
                        </li>
                        <li>
                          Надішліть команду <code>/newbot</code>, задайте ім’я та username бота
                          (має закінчуватися на <code>bot</code>).
                        </li>
                        <li>
                          Скопіюйте <strong>токен</strong> (вигляд:
                          <code>123456789:AA...</code>) і вставте в поле
                          <em>Telegram Bot Token</em>.
                        </li>
                        <li>
                          Напишіть своєму новому боту будь-яке повідомлення
                          (наприклад <code>старт</code>), щоб чат активувався.
                          Для групи: додайте бота в групу і зробіть його адміністратором
                          (щоб міг надсилати повідомлення).
                        </li>
                        <li>
                          Дізнайтесь <strong>Chat ID</strong>:
                          <ul style="margin:6px 0 0;padding-left:1.2em">
                            <li>
                              особистий чат — напишіть боту
                              <strong>@userinfobot</strong> або
                              <strong>@getidsbot</strong>, скопіюйте ваш Id;
                            </li>
                            <li>
                              група — додайте <strong>@getidsbot</strong> у групу
                              або відкрийте в браузері
                              <code>https://api.telegram.org/bot&lt;ТОКЕН&gt;/getUpdates</code>
                              після повідомлення в групі і знайдіть
                              <code>"chat":{"id":-100...}</code>
                              (для груп ID часто від’ємний).
                            </li>
                          </ul>
                        </li>
                        <li>
                          Вставте Chat ID у поле <em>Telegram Chat ID</em>,
                          увімкніть <em>Надсилати заявки в Telegram</em> і збережіть.
                        </li>
                        <li>
                          Перевірте: надішліть тестову заявку з сайту —
                          повідомлення має прийти в Telegram, а копія з’явиться в «Заявки».
                        </li>
                      </ol>
                      <p style="margin:0;color:#666">
                        Токен і Chat ID <strong>не публікуються</strong> на сайті
                        і не віддаються через API. Якщо сповіщення вимкнено або поля
                        порожні — заявки все одно зберігаються лише в адмінці.
                      </p>
                    </div>
                    """
                ),
                "fields": (
                    "telegram_notify_enabled",
                    "telegram_bot_token",
                    "telegram_notify_chat_id",
                ),
            },
        ),
        (
            "SEO",
            {
                "description": (
                    "Усі назви й тексти для Google, соцмереж і schema.org. "
                    "Змінюйте їх, коли оновлюєте бренд або послуги."
                ),
                "fields": (
                    "seo_title",
                    "seo_description",
                    "seo_keywords",
                    "seo_author",
                    "seo_canonical_path",
                    "seo_robots",
                    "seo_html_lang",
                    "seo_locale",
                    "seo_geo_region",
                    "seo_geo_placename",
                ),
            },
        ),
        (
            "Open Graph / Twitter",
            {
                "fields": (
                    "og_title",
                    "og_description",
                    "og_type",
                    "og_image",
                    "og_image_url",
                    "og_image_alt",
                    "twitter_card",
                    "twitter_title",
                    "twitter_description",
                    "twitter_site",
                )
            },
        ),
        (
            "Статистика",
            {
                "classes": ("collapse",),
                "description": (
                    "Застарілі значення. Актуальна статистика героя "
                    "редагується в розділі «Статистика героя»."
                ),
                "fields": (
                    "stats_projects",
                    "stats_years",
                    "stats_masters",
                    "stats_production",
                ),
            },
        ),
        (
            "Майстерня",
            {"fields": ("workshop_quote", "workshop_author", "workshop_text")},
        ),
        (
            "Проєкт у деталях",
            {
                "fields": (
                    "featured_project",
                    "detail_eyebrow_prefix",
                    "detail_section_title",
                    "detail_number_prefix",
                    "detail_cta_text",
                    "detail_cta_href",
                    "meta_label_area",
                    "meta_label_materials",
                    "meta_label_duration",
                    "meta_label_year",
                    "meta_label_location",
                )
            },
        ),
        (
            "Drawing",
            {
                "fields": (
                    "drawing_eyebrow",
                    "drawing_title",
                    "drawing_body",
                    "drawing_phase_1_label",
                    "drawing_phase_2_label",
                    "drawing_phase_3_label",
                    "drawing_result_alt",
                    "drawing_sketch",
                    "drawing_sketch_image_url",
                )
            },
        ),
        (
            "До / Після",
            {
                "fields": (
                    "ba_eyebrow",
                    "ba_title",
                    "ba_hint",
                    "ba_label_before",
                    "ba_label_after",
                    "before_image",
                    "before_image_url",
                    "after_image",
                    "after_image_url",
                )
            },
        ),
        (
            "Контактна форма",
            {
                "fields": (
                    "contact_eyebrow",
                    "contact_title_line1",
                    "contact_title_line2",
                    "contact_title_emphasis",
                    "contact_intro",
                    "contact_room_heading",
                    "contact_message_placeholder",
                    "contact_name_placeholder",
                    "contact_phone_placeholder",
                    "contact_email_placeholder",
                    "contact_telegram_placeholder",
                    "contact_submit_text",
                    "contact_submit_loading",
                    "contact_success_eyebrow",
                    "contact_success_title",
                    "contact_success_body",
                    "contact_validation_message",
                    "contact_label_address",
                    "contact_label_phone",
                    "contact_label_email",
                    "contact_label_telegram",
                    "contact_label_whatsapp",
                    "contact_label_instagram",
                )
            },
        ),
        (
            "Footer",
            {
                "fields": (
                    "footer_services_heading",
                    "footer_studio_heading",
                    "footer_contacts_heading",
                    "footer_copyright_suffix",
                    "footer_location_tagline",
                )
            },
        ),
        (
            "JSON-LD / schema.org",
            {
                "description": (
                    "Структуровані дані для пошуку. Назви бізнесу та послуг "
                    "можна змінювати без правки коду."
                ),
                "fields": (
                    "jsonld_name",
                    "jsonld_type",
                    "jsonld_description",
                    "jsonld_street",
                    "jsonld_city",
                    "jsonld_country",
                    "jsonld_postal_code",
                    "jsonld_price_range",
                    "jsonld_area_served",
                    "jsonld_opening_hours",
                    "jsonld_latitude",
                    "jsonld_longitude",
                    "jsonld_services",
                ),
            },
        ),
    )
    autocomplete_fields = ("featured_project",)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return HttpResponseRedirect(
            reverse("admin:catalog_sitesettings_change", args=[obj.pk])
        )


@admin.register(HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)
    search_fields = ("value", "label")
    ordering = ("order", "id")


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "section_id",
        "eyebrow",
        "title",
        "cta_text",
        "is_visible",
        "order",
    )
    list_editable = ("is_visible", "order")
    list_filter = ("is_visible",)
    search_fields = ("key", "section_id", "eyebrow", "title", "cta_text")
    ordering = ("order", "id")
    fieldsets = (
        (None, {"fields": ("key", "section_id", "order", "is_visible")}),
        (
            "Тексти",
            {
                "fields": (
                    "eyebrow",
                    "title",
                    "title_line2",
                    "title_emphasis",
                    "subtitle",
                )
            },
        ),
        ("Кнопка / посилання", {"fields": ("cta_text", "cta_href")}),
    )


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ("label", "href", "location", "is_visible", "order")
    list_editable = ("order", "is_visible")
    list_filter = ("location", "is_visible")
    search_fields = ("label", "href")
    ordering = ("location", "order", "id")


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "is_active", "order")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("value", "label")
    ordering = ("order", "id")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category",
        "year",
        "has_video",
        "gallery_count",
        "is_featured",
        "is_published",
        "order",
    )
    list_filter = (
        "is_published",
        "is_featured",
        "show_in_detail_section",
        "year",
        "category",
    )
    search_fields = (
        "title",
        "subtitle",
        "description",
        "short_description",
        "slug",
        "location",
        "seo_title",
        "seo_keywords",
    )
    list_editable = ("order", "is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline, ProjectStageInline]
    save_on_top = True
    fieldsets = (
        (
            "Основне",
            {
                "fields": (
                    "title",
                    "slug",
                    "subtitle",
                    "short_description",
                    "description",
                    "category",
                    "year",
                )
            },
        ),
        (
            "Метадані проєкту",
            {
                "fields": (
                    "materials_label",
                    "area",
                    "duration",
                    "location",
                )
            },
        ),
        (
            "Обкладинка",
            {"fields": ("cover_image", "image_url", "detail_image_url")},
        ),
        (
            "Відео (креслення → готове рішення)",
            {
                "fields": ("video", "video_url", "video_poster_url"),
                "description": "Завантажте файл до 100 МБ або вкажіть зовнішній URL.",
            },
        ),
        (
            "Публікація",
            {
                "fields": (
                    "is_featured",
                    "show_in_detail_section",
                    "is_published",
                    "order",
                )
            },
        ),
        (
            "SEO",
            {"fields": ("seo_title", "seo_description", "seo_keywords")},
        ),
    )

    @admin.display(boolean=True, description="Відео")
    def has_video(self, obj: Project) -> bool:
        return bool(obj.video or obj.video_url)

    @admin.display(description="Фото")
    def gallery_count(self, obj: Project) -> int:
        return obj.gallery.filter(is_published=True).count()


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name_uk", "name_en", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("name_uk", "name_en", "description")
    list_editable = ("order", "is_published")
    fields = (
        "name_uk",
        "name_en",
        "description",
        "image",
        "image_url",
        "order",
        "is_published",
    )


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    list_editable = ("order", "is_published")
    fields = (
        "title",
        "description",
        "duration",
        "image",
        "image_url",
        "order",
        "is_published",
    )


@admin.register(CraftDetail)
class CraftDetailAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("title",)
    list_editable = ("order", "is_published")
    fields = ("title", "image", "image_url", "order", "is_published")


@admin.register(WorkshopStat)
class WorkshopStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    search_fields = ("value", "label")
    list_editable = ("order",)


@admin.register(WorkshopImage)
class WorkshopImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    search_fields = ("title",)
    list_editable = ("order",)
    fields = ("title", "image", "image_url", "order")


class HeroZoneInline(admin.TabularInline):
    model = HeroZone
    extra = 1
    fields = (
        "name",
        "service",
        "materials",
        "tag",
        "x",
        "y",
        "width",
        "height",
        "order",
        "is_published",
    )
    ordering = ("order", "id")


@admin.register(HeroScene)
class HeroSceneAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_published", "order", "zone_count")
    list_editable = ("is_active", "is_published", "order")
    list_filter = ("is_active", "is_published")
    search_fields = ("title", "hint")
    inlines = (HeroZoneInline,)
    change_form_template = "admin/catalog/heroscene/change_form.html"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "image",
                    "image_url",
                    "is_active",
                    "is_published",
                    "order",
                )
            },
        ),
        (
            "Тексти на головній",
            {
                "fields": ("hint", "idle_eyebrow", "idle_title", "idle_body"),
            },
        ),
    )

    class Media:
        css = {"all": ("catalog/admin/hero-zone-editor.css",)}
        js = ("catalog/admin/hero-zone-editor.js",)

    @admin.display(description="Зони")
    def zone_count(self, obj: HeroScene) -> int:
        return obj.zones.count()

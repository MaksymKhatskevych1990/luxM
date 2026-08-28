from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import (
    CraftDetail,
    Material,
    ProcessStep,
    Project,
    ProjectStage,
    SiteSettings,
    WorkshopImage,
    WorkshopStat,
)


class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 1
    fields = ("title", "image_url", "order")
    ordering = ("order", "id")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Бренд",
            {"fields": ("brand_name", "tagline", "founded_year")},
        ),
        (
            "Контакти",
            {
                "fields": (
                    "phone",
                    "email",
                    "telegram",
                    "address",
                    "instagram_url",
                    "telegram_url",
                )
            },
        ),
        (
            "SEO",
            {"fields": ("seo_title", "seo_description", "seo_keywords")},
        ),
        (
            "Статистика",
            {
                "fields": (
                    "stats_projects",
                    "stats_years",
                    "stats_masters",
                    "stats_production",
                )
            },
        ),
        (
            "Майстерня",
            {"fields": ("workshop_quote", "workshop_author", "workshop_text")},
        ),
        (
            "До / Після",
            {"fields": ("before_image_url", "after_image_url")},
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return HttpResponseRedirect(
            reverse("admin:catalog_sitesettings_change", args=[obj.pk])
        )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "category",
        "year",
        "is_featured",
        "is_published",
        "order",
    )
    list_filter = ("is_published", "is_featured", "year", "category")
    search_fields = ("title", "subtitle", "description", "slug", "location")
    list_editable = ("order", "is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectStageInline]
    save_on_top = True
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "subtitle",
                    "description",
                    "category",
                    "year",
                )
            },
        ),
        (
            "Деталі проєкту",
            {
                "fields": (
                    "materials_label",
                    "area",
                    "duration",
                    "location",
                    "image_url",
                    "detail_image_url",
                )
            },
        ),
        (
            "Публікація",
            {"fields": ("is_featured", "is_published", "order")},
        ),
        (
            "SEO",
            {"fields": ("seo_title", "seo_description")},
        ),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name_uk", "name_en", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("name_uk", "name_en", "description")
    list_editable = ("order", "is_published")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("title", "description")
    list_editable = ("order", "is_published")


@admin.register(CraftDetail)
class CraftDetailAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order")
    list_filter = ("is_published",)
    search_fields = ("title",)
    list_editable = ("order", "is_published")


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

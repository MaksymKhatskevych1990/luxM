from django.contrib import admin
from django.utils.html import format_html

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "room_type_label_display",
        "is_processed",
        "created_at",
    )
    list_filter = ("is_processed", "room_type", "created_at")
    search_fields = ("name", "phone", "email", "telegram", "message", "room_type")
    list_editable = ("is_processed",)
    readonly_fields = ("created_at", "room_type_label_display", "attachment_preview")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    fieldsets = (
        (
            "Клієнт",
            {"fields": ("name", "phone", "email", "telegram")},
        ),
        (
            "Запит",
            {"fields": ("room_type", "room_type_label_display", "message", "attachment", "attachment_preview")},
        ),
        (
            "Статус",
            {"fields": ("is_processed", "created_at")},
        ),
    )

    @admin.display(description="Тип приміщення")
    def room_type_label_display(self, obj: Lead) -> str:
        return obj.room_type_label()

    @admin.display(description="Перегляд файлу")
    def attachment_preview(self, obj: Lead) -> str:
        if not obj.attachment:
            return "—"
        url = obj.attachment.url
        name = obj.attachment.name.lower()
        if name.endswith((".jpg", ".jpeg", ".png", ".webp")):
            return format_html(
                '<a href="{}" target="_blank" rel="noopener"><img src="{}" alt="" style="max-height:220px"></a>',
                url,
                url,
            )
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">{}</a>',
            url,
            obj.attachment.name,
        )

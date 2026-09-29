from rest_framework import serializers

from catalog.models import RoomType

from .models import Lead

MAX_ATTACHMENT_BYTES = 15 * 1024 * 1024
ALLOWED_ATTACHMENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/heic",
    "image/heif",
    "application/pdf",
}


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = (
            "id",
            "room_type",
            "message",
            "name",
            "phone",
            "email",
            "telegram",
            "attachment",
            "is_processed",
            "created_at",
        )
        read_only_fields = ("id", "is_processed", "created_at")

    def validate_room_type(self, value: str) -> str:
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Оберіть тип приміщення.")
        if not RoomType.objects.filter(value=value, is_active=True).exists():
            raise serializers.ValidationError("Невірний тип приміщення.")
        return value

    def validate_attachment(self, value):
        if not value:
            return value
        if value.size > MAX_ATTACHMENT_BYTES:
            raise serializers.ValidationError("Файл завеликий. Максимум 15 МБ.")
        content_type = getattr(value, "content_type", "") or ""
        if content_type not in ALLOWED_ATTACHMENT_TYPES:
            raise serializers.ValidationError(
                "Надішліть фото (JPG, PNG, WEBP) або PDF."
            )
        return value

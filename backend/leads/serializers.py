import os
import re

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
GENERIC_ATTACHMENT_TYPES = {"", "application/octet-stream", "binary/octet-stream"}
ALLOWED_ATTACHMENT_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".heic",
    ".heif",
    ".pdf",
}


class LeadSerializer(serializers.ModelSerializer):
    hp_field = serializers.CharField(required=False, allow_blank=True, write_only=True)

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
            "hp_field",
            "is_processed",
            "created_at",
        )
        read_only_fields = ("id", "is_processed", "created_at")

    def validate_name(self, value: str) -> str:
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("Вкажіть ім'я.")
        return value

    def validate_phone(self, value: str) -> str:
        value = (value or "").strip()
        digits = re.sub(r"\D", "", value)
        if len(digits) < 10 or len(digits) > 15:
            raise serializers.ValidationError("Вкажіть коректний телефон: щонайменше 10 цифр.")
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        honeypot = attrs.pop("hp_field", "")
        self.spam_honeypot = bool(str(honeypot or "").strip())
        return attrs

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
        extension = os.path.splitext(getattr(value, "name", "") or "")[1].lower()
        if extension not in ALLOWED_ATTACHMENT_EXTENSIONS:
            raise serializers.ValidationError(
                "Надішліть фото (JPG, PNG, WEBP, HEIC) або PDF."
            )
        content_type = (getattr(value, "content_type", "") or "").lower()
        if (
            content_type not in ALLOWED_ATTACHMENT_TYPES
            and content_type not in GENERIC_ATTACHMENT_TYPES
        ):
            raise serializers.ValidationError(
                "Надішліть фото (JPG, PNG, WEBP, HEIC) або PDF."
            )
        return value

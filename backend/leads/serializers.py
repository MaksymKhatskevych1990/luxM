from rest_framework import serializers

from catalog.models import RoomType

from .models import Lead


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

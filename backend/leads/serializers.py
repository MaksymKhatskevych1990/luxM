from rest_framework import serializers

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
